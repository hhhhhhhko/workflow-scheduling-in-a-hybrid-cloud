from preprocess.Workflow import Scientific_Workflow
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
import copy
from Parameter import get_args

args = get_args()

#超参数 Hyper Parameters
BATCH_SIZE = 32             # 
LR = 0.01                   # learning rate
EPSILON = 0.9               # greedy policy
GAMMA = 0.9                 # reward discount
MEMORY_CAPACITY = 2000      # 记忆库大小
TARGET_REPLACE_ITER = 100   # target update frequency Q-target网络的更新频率
# env = gym.make('CartPole-v0')
# env = env.unwrapped
N_ACTIONS = args.VM_Num
N_STATES = 1 + args.VM_Num # N_STATES = env.observation_space.shape[0]

# 定义神经网络
class Net11(nn.Module):
    def __init__(self):
        super(Net11, self).__init__()
        self.fc1 = nn.Linear(N_STATES, 50)     # 定义神经网络线性层, 输入神经元个数为state的个数, 输出神经元个数为10(隐藏层（hidden layer）设为10个神经元)
        self.fc1.weight.data.normal_(0, 0.1)   # initialization
        self.out = nn.Linear(50, N_ACTIONS)    # 输入神经元个数为10, 输出神经元个数为action的个数
        self.out.weight.data.normal_(0, 0.1)   # initialization

        # Dueling DQN
        # 优势函数
        self.advantage = nn.Sequential(
            nn.Linear(50, 50),
            nn.ReLU(),
            nn.Linear(50, N_ACTIONS) 
        )

        # 价值函数
        self.value = nn.Sequential(
            nn.Linear(50, 50),
            nn.ReLU(),
            nn.Linear(50, 1)
        )
        

    # 调用 forward 方法，返回前向传播的结果
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)

        
        # Dueling DQN
        '''
        x = x.view(x.size(0), -1)
        advantage = self.advantage(x)
        value = self.value(x)
        return value + advantage - advantage.mean()
        '''
        return actions_value

class DQTS():
    def __init__(self):
        super(DQTS, self).__init__()
        self.eval_net, self.target_net = Net11(), Net11() # 要建立两个神经网络, 一个是目标网络 (Target Net), 一个是估计网络 (Eval Net)
        self.learn_step_counter = 0                                     # for target updating 用于 target 更新计时
        self.memory_counter = 0                                         # for storing memory 记忆库记数
        self.memory = np.zeros((MEMORY_CAPACITY, N_STATES * 2 + 2))     # initialize memory 初始化记忆库
        # why the NUM_STATE*2 +2
        # When we store the memory, we put the state, action, reward and next_state in the memory
        # here reward and action is a number, state is a ndarray
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR) # torch 的优化器
        self.loss_func = nn.MSELoss() # 误差公式

    # 动作的选择
    def choose_action(self, state):
        state = torch.unsqueeze(torch.FloatTensor(state), 0) # 获得一个一维数组
        # input only one sample 这里只输入一个 sample
        if np.random.uniform() < EPSILON:   # greedy policy 选最优动作
            actions_value = self.eval_net.forward(state)
            action = np.argmax(actions_value.detach().numpy())     # return the argmax 选择Q-value值最大的action
            # action = torch.max(actions_value, 1)[1].data.numpy()[0]     # return the argmax 选择Q-value值最大的action
        else:   # random policy 选随机动作
            action = np.random.randint(0, N_ACTIONS)
        return action

    # 存储转换状态至replay memory
    def store_transition(self, state, action, reward, next_state):
        transition = np.hstack((state, [action, reward], next_state))
        # replace the old memory with new memory 如果记忆库满了, 就覆盖老数据
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

    def learn(self):
        # update target parameters 即target net 参数更新
        if self.learn_step_counter % TARGET_REPLACE_ITER == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter += 1

        # sample batch transitions from memory 抽取记忆库中的批数据
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)
        batch_memory = self.memory[sample_index, :]
        batch_state = torch.FloatTensor(batch_memory[:, :N_STATES])
        batch_action = torch.LongTensor(batch_memory[:, N_STATES:N_STATES+1].astype(int))
        batch_reward = torch.FloatTensor(batch_memory[:, N_STATES+1:N_STATES+2])
        batch_next_state = torch.FloatTensor(batch_memory[:,-N_STATES:])

        # q_eval w.r.t the action in experience
        # 针对做过的动作b_a, 来选 q_eval 的值, (q_eval 原本有所有动作的值)
        
        # DQN
        q_eval = self.eval_net(batch_state).gather(1, batch_action)  # shape (batch, 1)
        q_next = self.target_net(batch_next_state).detach()  # detach from graph, don't backpropagate, q_next 不进行反向传递误差, 所以 detach
        q_target = batch_reward + GAMMA * q_next.max(1)[0].view(BATCH_SIZE, 1)  # shape (batch, 1)
        

        # Double DQN
        '''
        q_eval = self.eval_net(batch_state).gather(1, batch_action)  # shape (batch, 1)
        q_next = self.target_net(batch_next_state).detach()  # detach from graph, don't backpropagate, q_next 不进行反向传递误差, 所以 detach
        q_target = batch_reward + GAMMA * q_next.gather(1, torch.max(q_eval, 1)[1].view(BATCH_SIZE, 1))  # shape (batch, 1)
        '''
        loss = self.loss_func(q_eval, q_target)

        # 计算, 更新 eval net
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
