# Q-learning algorithm

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import time
from preprocess.Workflow import Scientific_Workflow

'''
输入工作流属性，输出工作流中任务的排序（要符合约束）
'''

class Q_learning():
    
    #def __init__(self, alpha, gamma, dag, Twait_list):
    def __init__(self, alpha, gamma, dag):
        '''
        alpha : 学习率
        gamma : 折扣因子
        dag : 工作流DAG对象, 含有工作流的属性num_of_vertex、vertex、edge、pred、succ、entry、exit、ranku
        q_sa : Q-table
        reward[i] : 选择第i个任务时的即时奖励
        Twait_list
        '''
        self.alpha = alpha
        self.gamma = gamma
        self.dag = dag # 引入XMLProcess.py中的XMLtoDAG类
        self.q_sa = [[0 for j in range(self.dag.n_job)] for i in range(self.dag.n_job)]
        self.reward = []
        self.eplsilon = 0.9 # greedy policy
        #self.reward_calc(Twait_list)
        self.reward_calc()

    # 获得最佳Q-table
    def learning(self):
        convergence_flag = 0 # 判断是否收敛
        episode = 0 # 记录episode次数
        return_1 = []
        q_table = [[0 for j in range(self.dag.n_job)] for i in range(self.dag.n_job)] # 初始化Q-table
        total_reward = 0 # 记录总奖励
        while(True):
            #total_reward = 0 # 记录总奖励
            '''
            current_state : 当前状态
            finish_vertexs : 已选定的任务
            wait_vertexs : 可供选择的任务
            selected_vertex : 选择的任务
            before_state : 转换前的状态
            r : 动作获得的即时奖励
            max_q_value : 最大Q值
            max_value_action : 从过渡后状态的角度看，具有最大动作价值的动作
            virtual_entry_index : 虚拟入口任务的任务号
            '''
            
            if episode == 0:
                self.dag.add_virtual_entry()  # 添加虚拟入口任务
                self.dag.add_virtual_exit()  # 添加虚拟出口任务
            current_state = -1
            # current_state = self.dag.virtual_entry_index  # 初始状态是虚拟入口任务
            finish_vertexs = [-1]
            #finish_vertexs = [self.dag.virtual_entry_index()]  # 虚拟入口任务被选中
            wait_vertexs = []
            wait_vertexs += self.check_succ(current_state, finish_vertexs, wait_vertexs)  # 使用def check_succ()函数检查
            '''
            wait_vertexs = wait_vertexs + self.check_succ(current_state, finish_vertexs, wait_vertexs)
            +表示连接两个列表，而不是加法运算
            '''
            no_update_flag = 0  #
            
            for k in range(self.dag.n_job - 1):
                
                '''
                if np.random.uniform() > self.eplsilon:  # 以epsilon的概率选择动作
                    selected_vertex = random.choice(wait_vertexs)  # 随机决定动作
                else:
                    if current_state == -1:
                        #state_actions = 0
                        selected_vertex = random.choice(wait_vertexs)
                    else:
                        state_actions = q_table[current_state]
                        max_legal_value = max (state_actions[i] for i in wait_vertexs)
                        if max_legal_value == 0:
                            selected_vertex = random.choice(wait_vertexs)
                        else:
                            selected_vertex = state_actions.index(max_legal_value)
                '''
                        
                        
                        # state_actions = q_table[current_state]  # 获得当前状态下的所有动作,
                        # legal_vertex = [state_actions[i] for i in wait_vertexs]  # 获得当前状态下的所有合法动作的q值
                        # max_value_action = np.argmax(legal_vertex)  # 返回可取合法索引对应值的索引号
                        # selected_vertex = np.where(legal_vertex == max_value_action)[0][0]  # 选择具有最大Q值的合法的动作,即最大索引号在state_actions中的索引号
                        # selected_vertex = state_actions.index(max_value_action)  👈0会重复,所以不准确
                        
                selected_vertex = random.choice(wait_vertexs)
                
                wait_vertexs.remove(selected_vertex)  # 从可供选择的任务中删除被选走的任务
                finish_vertexs.append(selected_vertex)  # 将被选中的任务加入已选定的任务中
                before_state = current_state  # 记录转换前的状态
                current_state = selected_vertex  # 转换状态
                r = self.reward[selected_vertex]  # 获得即时奖励
                wait_vertexs += self.check_succ(current_state, finish_vertexs, wait_vertexs)  # 使用def check_succ()函数检查

                max_q_value = 0
                max_value_action = 0

                for n in range(self.dag.n_job):  # 更新最大Q值
                    if(q_table[current_state][n] >= max_q_value):  
                        max_q_value = q_table[current_state][n]
                        max_value_action = n

                # 更新Q-table
                before_q_sa = q_table[before_state][selected_vertex]  # 记录更新前的Q-table
                q_table[before_state][selected_vertex] = q_table[before_state][selected_vertex] + self.alpha * (r + self.gamma * max_q_value - q_table[before_state][selected_vertex])
                
                # 记录return(一个episode中的总奖励)
                total_reward += self.alpha * (r + self.gamma * max_q_value - q_table[before_state][selected_vertex])
                #total_reward += r
                

                if(abs(q_table[before_state][selected_vertex] - before_q_sa) <= 1):  # 如果更新量小于1
                    no_update_flag+=1

            return_1.append(total_reward)

            #return finish_vertexs
            # 循环结束的判定条件
            # if(no_update_flag == self.dag.num_of_vertex * (self.dag.num_of_vertex - 1)):  # 如果Q-table在一轮中没有更新
            episode += 1
            if(no_update_flag == (self.dag.n_job - 1)):    
                convergence_flag+=1
                if(convergence_flag == 100000):  
                    # 1000个任务1000000有点大
                    #100个任务需要大约500000/600000。70需要200000。50需要100000/200000, 30需要10000/20000。 看情况调整
                    break
            
        return finish_vertexs, q_table, episode, return_1

    # 返回一个 "n个后续任务合法且不在wait_vertexs中 "的任务的列表
    def check_succ(self, n, finish_vertexs, wait_vertexs):
        list = []
        
        #for succ_n in range(len(self.dag.successor)):
        for succ_n in self.dag.successor[n+1]:
            if(self.legal(succ_n, finish_vertexs) and succ_n not in wait_vertexs):
                list.append(succ_n)
        
        return list
    
    # 判断任务n是否合法
    def legal(self, n, finish_vertexs):
        for pred_n in self.dag.precursor[n+1]:
        #for pred_n in range(len(self.dag.precursor[n])):
            if(pred_n not in finish_vertexs):
                return False
        
        return True
    
    # 奖励的确定(设置ranku为reward)
    #def reward_calc(self, Twait_list):
    def reward_calc(self):
        #scientific_workflow = Scientific_Workflow('CyberShake', 100)
        #dag = scientific_workflow.get_workflow()
        #ranku = dag.get_ranku()
        ranku = self.dag.get_ranku()
        for i in range(self.dag.n_job):
        #for i in range(dag.n_job):
            #self.reward.append(ranku[i] + 0.001 * Twait_list[i])
            #self.reward.append(self.dag.ranku[i])
            self.reward.append(ranku[i])

    # 表示q_sa（转换为整数形式）
    def print_q_sa_int(self):
        q_sa_int = [[0 for j in range(self.dag.n_job)] for i in range(self.dag.n_job)]
        
        for i in range(self.dag.n_job):
            for j in range(self.dag.n_job):
                q_sa_int[i][j] = int(self.q_sa[i][j])
        
        print("q_sa_int = ", end = "")
        for i in range(self.dag.n_job):
            print(q_sa_int[i])