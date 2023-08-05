'''
import networkx
import xml.dom.minidom
import matplotlib.pyplot as plt

dom = xml.dom.minidom.parse('PSW-DRL\DAG\CyberShake\CyberShake_30.xml')  # 读取xml文件
root = dom.documentElement  # 获取根节点
G = networkx.DiGraph()  # 创建有向图
for child in root.childNodes:  # 遍历子节点  
    if child.nodeName == "child":  # 获取子节点的名称
        child_node = child.getAttribute("ref")  # 获取子节点的属性
        for parent in child.childNodes:  
            if parent.nodeName == "parent":
                parent_node = parent.getAttribute("ref")  # 获取父节点的属性
                print("parent_{0} -> child_{1}".format(parent_node,child_node))
                G.add_edge(parent_node,child_node)  # 有向图中添加边
        node_list = list(networkx.topological_sort(G))  # 拓扑排序
        _map = {item:index+1 for index,item in enumerate(node_list)}  # 重新编号
        # print(_map)
        #G = networkx.relabel_nodes(G,_map)
        #print(list(G.nodes()))
networkx.draw_networkx(G)
plt.show()
'''

'''
a = Scientific_Workflow('CyberShake', 30)
a = a.get_workflow()
#a = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\CyberShake\CyberShake_30.xml')
#a.add_virtual_entry()
#print(a.precursor)
#print(a.successor)
#print(a.jobs)
jobs = a.jobs
print(jobs)
'''
'''
q_learning = Q_learning(1.0, 0.2, a)
a.add_virtual_entry()
current_state = 0
finish_vertexs = [0]
wait_vertexs = []
wait_vertexs += q_learning.check_succ(current_state, finish_vertexs, wait_vertexs)
selected_vertex = random.choice(wait_vertexs)
wait_vertexs.remove(selected_vertex)
finish_vertexs.append(selected_vertex) 
before_state = current_state  # 记录转换前的状态
current_state = selected_vertex  # 转换状态

print(wait_vertexs)
'''
'''
# 选择workflow
scientific_workflow = Scientific_Workflow('CyberShake', 30)
dag = scientific_workflow.get_workflow()
# print(dag.jobs())
#dag = workflow.dag()

q_learning = Q_learning(0.9, 0.8, dag)
scheduling_list, q_table, episode, return_1 = q_learning.learning() 
scheduling_list.pop(0)
for i in range(30):
    if i not in scheduling_list:
        scheduling_list.append(i)
np.savetxt('Q-learning reward.txt', return_1)
print(scheduling_list)
#print(q_table)
print(episode)
#print(return_1)
'''


'''
q_learning = Q_learning(1.0, 0.2, dag) # 任务排序阶段, 使用Q-learning
scheduling_list = q_learning.learning() # 训练Q-learning模型，获得最佳Q-table
# scheduling_list.remove(dag.virtual_entry_index) # 去除虚拟入口entry节点
scheduling_list.pop(0)
for i in range(30):
    if i not in scheduling_list:
        scheduling_list.append(i)
print(scheduling_list)
print(scheduling_list[0])
print(scheduling_list[1])
print(scheduling_list[2])
'''
'''
# 获得各项参数
args = get_args()

# 环境
env = Env(args)

# DQN
dqn = DQN()

global_step = 0  #总体步数
my_learn_step = 0 #学习步数
DQN_Reward_list = []

job_c = 0 # job count:按照list中的顺序执行任务
job_id = scheduling_list[job_c] # job:当前执行的任务
finish, job_attrs = env.load_new_job(job_c,job_id,dag)
DQN_state = env.getState(job_attrs) 
print(DQN_state)
action_DQN = dqn.choose_action(DQN_state)  # choose action
reward_DQN = env.feedback(job_attrs, action_DQN)
print(action_DQN)
print(reward_DQN)
'''



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
import random




#总体(阶段)层面的循环(第三阶段)
Twait_list = np.zeros(100) # 任务等待时间列表
makespan_DQN = 100000 # 记录DQN算法的makespan
count3 = 0 # 记录第三阶段总体的迭代次数
makespan = [] # 记录各轮迭代的makespan

for i in range(10): #第三阶段循环次数

    # 选择workflow
    scientific_workflow = Scientific_Workflow('CyberShake', 100)
    dag = scientific_workflow.get_workflow()
    # print(dag.jobs())
    #dag = workflow.dag()

    # 获得各项参数
    args = get_args()

    # 环境
    env = Env(args)

#while True:
    #q_name = 'q_learning{}'.format(count)
        
    #locals()[q_name] = Q_learning(1.0, 0.2, dag, Twait_list) # 任务排序阶段, 使用Q-learning
    q_learning = Q_learning(0.9, 0.8, dag, Twait_list) # 任务排序阶段, 使用Q-learning
#q_learning = Q_learning(0.9, 0.8, dag) # 任务排序阶段, 使用Q-learning
        
    #scheduling_list = locals()[q_name].learning() # 训练Q-learning模型，获得最佳Q-table
    scheduling_list, q_table, episode1, return_1 = q_learning.learning() # 训练Q-learning模型，获得最佳Q-table
    
    # scheduling_list.remove(dag.virtual_entry_index) # 去除虚拟入口entry节点
    scheduling_list.pop(0)
    for i in range(dag.n_job):
        if i not in scheduling_list:
            scheduling_list.append(i)
    print(scheduling_list)
    print(episode1)


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

            print(VM_selected) # 每个任务选择的虚拟机
            # 根据调度结果计算新的平均传输时长
            for i in range(len(VM_selected) - 1):
                TT = [] # 记录传输时长的临时列表
                if args.VM_Type[i] == args.VM_Type[i + 1]: # 如果两个任务选择的虚拟机平台相同
                    TT.append(dag.edges[VM_selected[i]][VM_selected[i+1]] / 100000)
                else: # 如果两个任务选择的虚拟机平台不同
                    TT.append(dag.edges[VM_selected[i]][VM_selected[i+1]] / 50000) # 跨平台带宽更小
                new_trans_time = np.mean(TT) # 计算新的平均传输时长

            #np.savetxt('DQN return.txt', return_2)

            '''
            difference = abs(makespan_DQN - makespan4)
            if (difference / makespan_DQN) < 0.1:
                break
            '''
            Twait_list = env.get_Twait() # 更新Twait
            print('Twait_list:', Twait_list)
            count3 += 1
            print('count:', count3)
            makespan_DQN = makespan4 # 更新makespan
            makespan.append(makespan_DQN)

np.savetxt('makespan.txt', makespan)
