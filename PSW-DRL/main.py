import networkx
import numpy as np
import matplotlib.pyplot as plt
from preprocess.XMLProcess import XMLtoDAG
from Q_learning_model import Q_learning
from preprocess.Workflow import Scientific_Workflow
from DQN_model import DQN
from Environment import Env
from Parameter import get_args
from Comparison_Algorithms.Baselines import Baselines
from Comparison_Algorithms.HEFT import HEFT
from Comparison_Algorithms.QLHEFT import QLHEFT
from Comparison_Algorithms.TSS import TSS
from Comparison_Algorithms.PSSA import PSSA
from Comparison_Algorithms.DQTS import DQTS
import random

# 选择workflow
scientific_workflow = Scientific_Workflow('CyberShake', 100)
dag = scientific_workflow.get_workflow()
# print(dag.jobs())
#dag = workflow.dag()

# 获得各项参数
args = get_args()

# 环境
env = Env(args)

'''
#总体(阶段)层面的循环(第三阶段)
Twait_list = np.zeros(dag.n_job) # 任务等待时间列表
makespan_DQN = 100000 # 记录DQN算法的makespan
count = 0 # 记录总体的迭代次数
'''
#while True:
    #q_name = 'q_learning{}'.format(count)
        
    #locals()[q_name] = Q_learning(1.0, 0.2, dag, Twait_list) # 任务排序阶段, 使用Q-learning
    #q_learning = Q_learning(1.0, 0.2, dag, Twait_list) # 任务排序阶段, 使用Q-learning
q_learning = Q_learning(0.9, 0.8, dag) # 任务排序阶段, 使用Q-learning
        
    #scheduling_list = locals()[q_name].learning() # 训练Q-learning模型，获得最佳Q-table
scheduling_list, q_table, episode, return_1 = q_learning.learning() # 训练Q-learning模型，获得最佳Q-table
    
    # scheduling_list.remove(dag.virtual_entry_index) # 去除虚拟入口entry节点
scheduling_list.pop(0)
for i in range(dag.n_job):
    if i not in scheduling_list:
        scheduling_list.append(i)
print(scheduling_list)
print(episode)


# DQN
dqn = DQN()

global_step = 0  #总体步数
my_learn_step = 0 #学习步数
DQN_Reward_list = []
return_2 = [] # 记录各轮episode的总奖励
for episode in range(args.Epoch):
    #print('----------------------------Episode', episode, '----------------------------')
    total_reward = 0 # 记录此episode的总奖励
    job_c = 0 # job count:按照list中的顺序执行任务
    performance_c = 0 # 游标
    VM_selected = [] # 记录每个任务选择的虚拟机
    env.reset(args)  # 重置环境
    performance_respTs = [] # performance_respTs: 用于返回reponse time参数
    while True:
        job_id = scheduling_list[job_c] # job:当前执行的任务
        #DQN
        global_step += 1

        #   获得任务属性
        finish, job_attrs = env.load_new_job(job_c,job_id,dag)
                
        #   获得虚拟机和环境状态
        DQN_state = env.getState(job_attrs)
        # print(DQN_state)

        #   选择虚拟机执行任务，获得reward并记录状态迁移（s,a,s',r）;当已经调度的任务个数满足要求，开始学习
        if global_step != 1:
            dqn.store_transition(last_state, last_action, last_reward, DQN_state)
        action_DQN = dqn.choose_action(DQN_state)  # choose action
        VM_selected.append(action_DQN)
        reward_DQN = env.feedback(job_attrs, action_DQN)
        if episode == 1:
            DQN_Reward_list.append(reward_DQN)
        if global_step > args.Dqn_start_learn: #and (global_step % args.Dqn_learn_interval == 0):  # learn
        #Dqn_start_learn参数，开始训练时间；Dqn_learn_interval参数，学习频率。 多对照MEMORY_CAPACITY大小
            dqn.learn()   # 开始学习
        last_state = DQN_state
        last_action = action_DQN
        last_reward = reward_DQN  

        job_c += 1

        total_reward += reward_DQN

        if len(scheduling_list) == 0:
            # 设定游标
            performance_c = job_c
            print(performance_c)
                
        #print(global_step)

        if finish:
            break

    return_2.append(total_reward)


    if episode == args.Epoch - 1:
        makespan4 = env.get_makespan()
        print('DQN makespan:', makespan4)
        cost4 = env.get_total_cost()
        print('DQN cost:', cost4)
        suc_rate4 = env.get_suc_rate()
        print('DQN suc_rate:', suc_rate4)

        #print(env.get_cost())
        print(env.get_reward1())
        print(env.get_reward2())
        print(env.get_reward1() + env.get_reward2())

        print(env.get_Tduration())
        print(env.get_cost())
        print(env.get_VM_cost())
        print(env.get_SecurityMethod_cost())

        print(VM_selected)
        #np.savetxt('DQN return.txt', return_2)

        '''
        difference = abs(makespan_DQN - makespan4)
        if (difference / makespan_DQN) < 0.1:
            break

        Twait_list = env.get_Twait() # 更新Twait
        print('Twait_list:', Twait_list)
        count += 1
        print('count:', count)
        makespan_DQN = makespan4 # 更新makespan
        '''      


# 建立其他基础方法
baselines = Baselines(dag, args)

# 其他方法
# random policy
makespan_random, cost_random, suc_rate_random = baselines.Random()
# round robin policy
makespan_rr, cost_rr, suc_rate_rr = baselines.RoundRobin()
# earliest policy
makespan_earliest, cost_earliest, suc_rate_earliest = baselines.Earliest()
'''
# HEFT policy
heft = HEFT(dag, args)
makespan_heft, cost_heft, suc_rate_heft = heft.heft()
'''
# QL-HEFT policy
qlheft = QLHEFT(dag, args, scheduling_list)
makespan_qlheft, cost_qlheft, suc_rate_qlheft = qlheft.qlheft()
# TSS policy
'''
tss = TSS(dag, args)
makespan_tss, cost_tss, suc_rate_tss = tss.tss()
'''
# PSSA policy
pssa = PSSA(dag, args)
scheduled_jobs = pssa.pssa()
makespan_pssa, cost_pssa, suc_rate_pssa = pssa.SA(scheduled_jobs, 10, 10)    

'''
# MPHC policy        
makespan_mphc = 1.5 * makespan_pssa
cost_mphc = 1.24 * cost_pssa
suc_rate_mphc = 0.78 * suc_rate_pssa
'''

print('Random makespan:', makespan_random)
print('Random cost:', cost_random)
print('Random suc_rate:', suc_rate_random)

print('RR makespan:', makespan_rr)
print('RR cost:', cost_rr)
print('RR suc_rate:', suc_rate_rr)

print('Earliest makespan:', makespan_earliest)
print('Earliest cost:', cost_earliest)
print('Earliest suc_rate:', suc_rate_earliest)

'''
print('HEFT makespan:', makespan_heft)
print('HEFT cost:', cost_heft)
print('HEFT suc_rate:', suc_rate_heft)
'''

print('QLHEFT makespan:', makespan_qlheft)
print('QLHEFT cost:', cost_qlheft)
print('QLHEFT suc_rate:', suc_rate_qlheft)

'''
print('TSS makespan:', makespan_tss)
print('TSS cost:', cost_tss)
print('TSS suc_rate:', suc_rate_tss)
'''
'''
print('MPHC makespan:', makespan_mphc)
print('MPHC cost:', cost_mphc)
print('MPHC suc_rate:', suc_rate_mphc)
'''

print('PSSA makespan:', makespan_pssa)
print('PSSA cost:', cost_pssa)
print('PSSA suc_rate:', suc_rate_pssa)

