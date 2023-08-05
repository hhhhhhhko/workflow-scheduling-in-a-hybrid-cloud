import numpy as np
import random
import math
from preprocess.Workflow import Scientific_Workflow

class PSSA:
    def __init__(self, dag, args):
        self.dag = dag
        self.args = args

    def pssa(self):
        # 虚拟机VM
        VMnum = self.args.VM_Num # 虚拟机数量
        PrivateCloudNum = self.args.Private_Cloud_Num # 私有云数量
        PublicCloudNum = self.args.Public_Cloud_Num # 公有云数量
        PrivateCloudVMCost = self.args.Private_Cloud_VM_Cost # 私有云虚拟机价格
        PublicCloudVMCost = self.args.Public_Cloud_VM_Cost # 公有云虚拟机价格
        PrivateCloudVMCapacity = self.args.Private_Cloud_VM_Capacity # 私有云虚拟机计算能力
        PublicCloudVMCapacity = self.args.Public_Cloud_VM_Capacity # 公有云虚拟机计算能力
        VMType = self.args.VM_Type # 虚拟机类型：私有云或公有云

        earliest_finish_times = np.zeros((VMnum, self.dag.n_job)) # 每个处理器上每个任务的最早完成时间
        
        scientific_workflow = Scientific_Workflow('CyberShake', 100)
        dag = scientific_workflow.get_workflow()
        ranking_list = dag.get_ranku() # ranku数组
        
        scheduled_jobs = np.zeros(self.dag.n_job) # 记录每个任务调度到的处理器

        # 按照ranku数组从小到大排序的任务列表进行任务调度
        sorted_jobs = np.argsort(ranking_list) 
        runtime = self.dag.runtime 
        computation_costs = np.zeros((self.dag.n_job, VMnum))   # 运算时间的二维数组
        for i in range(self.dag.n_job):
            for j in range(VMnum):
                if VMType[j] == 0: # 私有云
                    computation_costs[i][j] = runtime[i] / PrivateCloudVMCapacity[j]
                else: # 公有云
                    computation_costs[i][j] = runtime[i] / PublicCloudVMCapacity[j - 8]
       
        for i in range(self.dag.n_job):
            task_index = sorted_jobs[i]
            # 选择最早可用的处理器进行调度
            earliest_VM = -1 # 初始化
            earliest_finish_time = float('inf') # 初始化为无穷大
            for j in range(VMnum):
                finish_time = computation_costs[task_index][j] + max(earliest_finish_times[j])
                if finish_time < earliest_finish_time:
                    earliest_finish_time = finish_time
                    earliest_VM = j
            
            # 更新所选处理器的最早完成时间和任务调度
            earliest_finish_times[earliest_VM] += computation_costs[task_index][earliest_VM]
            scheduled_jobs[task_index] = earliest_VM

            # 计算调度方案的makespan
            if i == self.dag.n_job - 1:
                makespan = earliest_finish_times[earliest_VM][0]
        
        # 计算调度方案的成本
        VM_cost = 0
        for i in range(self.dag.n_job):
            cost =0
            if VMType[int(scheduled_jobs[i])] == 0: # 私有云
                cost = computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])] * PrivateCloudVMCost[int(scheduled_jobs[i])]
            else: # 公有云
                cost = computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])] * PublicCloudVMCost[int(scheduled_jobs[i]) - 8]
            VM_cost += cost
        
        privacy_security_level = self.dag.privacy_security_level
        JobSecurityLevel1 = np.ones(self.dag.n_job) * 0.2 # 任务的用户认证安全等级
        JobSecurityLevel2 = np.ones(self.dag.n_job) * 0.2 # 任务的保密性安全等级
        JobSecurityLevel3 = np.ones(self.dag.n_job) * 0.2 # 任务的完整性安全等级

        user_authentication = self.args.User_Authentication_Security_Level[1]
        cryptographic_method = self.args.Cryptographic_Security_Level[5]
        hash_function = self.args.Hash_Function_Security_Level[5]

        UserAuthenticationCost = self.args.User_Authentication_Cost # 用户认证方法的成本 
        CryptographicMethodCost = self.args.Cryptographic_Method_Cost # 保密性加密算法方法的成本
        HashFunctionCost = self.args.Hash_Function_Cost # 完整性哈希函数方法的成本

        # 计算调度方案的成功率
        suc_count = 0
        for i in range(self.dag.n_job):
            suc = 0
            if privacy_security_level[int(sorted_jobs[i])] == 1:
                if VMType[int(scheduled_jobs[i])] == 0:
                    suc = 1
            elif privacy_security_level[int(sorted_jobs[i])] == 2 and user_authentication >= JobSecurityLevel1[int(sorted_jobs[i])] and cryptographic_method >= JobSecurityLevel2[int(sorted_jobs[i])] and hash_function >= JobSecurityLevel3[int(sorted_jobs[i])]:
                suc = 1
            elif privacy_security_level[int(sorted_jobs[i])] == 3 and hash_function >= JobSecurityLevel3[int(sorted_jobs[i])]:
                suc = 1
            suc_count += suc
        suc_rate = suc_count / self.dag.n_job

        Security_cost = 0
        for i in range(self.dag.n_job):
            cost = 0
            if privacy_security_level[int(sorted_jobs[i])] == 2:
                cost = UserAuthenticationCost[1] + (CryptographicMethodCost[5] + HashFunctionCost[5]) * computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])]
            elif privacy_security_level[int(sorted_jobs[i])] == 3:
                cost = HashFunctionCost[5] * computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])]
            Security_cost += cost
        
        cost = VM_cost + Security_cost

        return scheduled_jobs
    

    def SA(self, scheduled_jobs, initial_temperature, num_iterations):
        # 虚拟机VM
        VMnum = self.args.VM_Num # 虚拟机数量
        PrivateCloudNum = self.args.Private_Cloud_Num # 私有云数量
        PublicCloudNum = self.args.Public_Cloud_Num # 公有云数量
        PrivateCloudVMCost = self.args.Private_Cloud_VM_Cost # 私有云虚拟机价格
        PublicCloudVMCost = self.args.Public_Cloud_VM_Cost # 公有云虚拟机价格
        PrivateCloudVMCapacity = self.args.Private_Cloud_VM_Capacity # 私有云虚拟机计算能力
        PublicCloudVMCapacity = self.args.Public_Cloud_VM_Capacity # 公有云虚拟机计算能力
        VMType = self.args.VM_Type # 虚拟机类型：私有云或公有云
        runtime = self.dag.runtime 
        privacy_security_level = self.dag.privacy_security_level

        JobSecurityLevel1 = np.ones(self.dag.n_job) * 0.2 # 任务的用户认证安全等级
        JobSecurityLevel2 = np.ones(self.dag.n_job) * 0.2 # 任务的保密性安全等级
        JobSecurityLevel3 = np.ones(self.dag.n_job) * 0.2 # 任务的完整性安全等级

        user_authentication = self.args.User_Authentication_Security_Level[1]
        cryptographic_method = self.args.Cryptographic_Security_Level[5]
        hash_function = self.args.Hash_Function_Security_Level[5]

        UserAuthenticationCost = self.args.User_Authentication_Cost # 用户认证方法的成本 
        CryptographicMethodCost = self.args.Cryptographic_Method_Cost # 保密性加密算法方法的成本
        HashFunctionCost = self.args.Hash_Function_Cost # 完整性哈希函数方法的成本

        UserAuthenticationOverhead = self.args.User_Authentication_Overhead
        CryptographicMethodSpeed = self.args.Cryptographic_Method_Speed
        HashFunctionSpeed = self.args.Hash_Function_Speed

        inputfilesize = self.dag.inputfilesize
        outputfilesize = self.dag.outputfilesize


        computation_costs = np.zeros((self.dag.n_job, VMnum))   # 运算时间的二维数组
        for i in range(self.dag.n_job):
            for j in range(VMnum):
                if VMType[j] == 0: # 私有云
                    computation_costs[i][j] = runtime[i] / PrivateCloudVMCapacity[j]
                else: # 公有云
                    computation_costs[i][j] = runtime[i] / PublicCloudVMCapacity[j - 8]


        initial_solution = scheduled_jobs
        current_solution = initial_solution
        best_solution = current_solution
        temperature = initial_temperature
        
        scientific_workflow = Scientific_Workflow('CyberShake', 100)
        dag = scientific_workflow.get_workflow()
        ranking_list = dag.get_ranku() # ranku数组
        sorted_jobs = np.argsort(ranking_list) 

        min_makespan = float('inf')
        min_Total_cost = float('inf')
        min_suc_rate = float('inf')
        for iteration in range(num_iterations):
            makespan = 0
            VM_cost = 0
            Security_cost = 0
            suc_rate = 0
            suc_count = 0
            Total_cost = 0

            neighbor_solution = self.get_neighborhood(current_solution)
            for i in range(self.dag.n_job):
                if VMType[int(neighbor_solution[i])] == 0:
                    texe = runtime[int(sorted_jobs[i])] / PrivateCloudVMCapacity[int(neighbor_solution[i])]
                elif VMType[int(neighbor_solution[i])] == 1:
                    texe = runtime[int(sorted_jobs[i])] / PublicCloudVMCapacity[int(neighbor_solution[i]) - 8]
                
                if VMType[int(neighbor_solution[i])] == 0:
                    real_Texe = texe
                else:
                    if privacy_security_level[int(sorted_jobs[i])] == 3:
                        real_Texe = texe + (inputfilesize[int(sorted_jobs[i])] + inputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000)
                    else:
                        real_Texe = texe + UserAuthenticationOverhead[1] + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000)
                '''
                if privacy_security_level[int(sorted_jobs[i])] == 1:
                    real_Texe = texe
                elif privacy_security_level[int(sorted_jobs[i])] == 2:
                    real_Texe = texe + UserAuthenticationOverhead[1] + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000)
                elif privacy_security_level[int(sorted_jobs[i])] == 3:
                    real_Texe = texe + (inputfilesize[int(sorted_jobs[i])] + inputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000)
                '''
                makespan = makespan + real_Texe

                cost = 0
                if VMType[int(neighbor_solution[i])] == 0: # 私有云
                    cost = computation_costs[int(sorted_jobs[i])][int(neighbor_solution[i])] * PrivateCloudVMCost[int(neighbor_solution[i])]
                else: # 公有云
                    cost = computation_costs[int(sorted_jobs[i])][int(neighbor_solution[i])] * PublicCloudVMCost[int(neighbor_solution[i]) - 8]
                VM_cost += cost

                cost1 = 0
                if VMType[int(neighbor_solution[i])] == 0:
                    cost1 = 0
                else:
                    if privacy_security_level[int(sorted_jobs[i])] == 3:
                        cost1 = HashFunctionCost[5] * real_Texe
                    else:
                        cost1 = UserAuthenticationCost[1] + (CryptographicMethodCost[5] + HashFunctionCost[5]) * real_Texe

                '''
                cost1 = 0
                if privacy_security_level[int(sorted_jobs[i])] == 2:
                    cost1 = UserAuthenticationCost[1] + (CryptographicMethodCost[5] + HashFunctionCost[5]) * (computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])] + UserAuthenticationOverhead[1] + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000))
                elif privacy_security_level[int(sorted_jobs[i])] == 3:
                    cost1 = HashFunctionCost[5] * (computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])] + (inputfilesize[int(sorted_jobs[i])] + inputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000))
                '''
                Security_cost += cost1
                
                suc = 0
                if privacy_security_level[int(sorted_jobs[i])] == 1:
                    if VMType[int(neighbor_solution[i])] == 0:
                        suc = 1
                elif privacy_security_level[int(sorted_jobs[i])] == 2:
                    if VMType[int(neighbor_solution[i])] == 0:
                        suc = 1
                    elif user_authentication >= JobSecurityLevel1[int(sorted_jobs[i])] and cryptographic_method >= JobSecurityLevel2[int(sorted_jobs[i])] and hash_function >= JobSecurityLevel3[int(sorted_jobs[i])]:
                        suc = 1
                elif privacy_security_level[int(sorted_jobs[i])] == 3:
                    if VMType[int(neighbor_solution[i])] == 0:
                        suc = 1
                    elif hash_function >= JobSecurityLevel3[int(sorted_jobs[i])]:
                        suc = 1
                '''
                suc = 0
                if privacy_security_level[int(sorted_jobs[i])] == 1:
                    if VMType[int(neighbor_solution[i])] == 0:
                        suc = 1
                elif privacy_security_level[int(sorted_jobs[i])] == 2 and user_authentication >= JobSecurityLevel1[int(sorted_jobs[i])] and cryptographic_method >= JobSecurityLevel2[int(sorted_jobs[i])] and hash_function >= JobSecurityLevel3[int(sorted_jobs[i])]:
                    suc = 1
                elif privacy_security_level[int(sorted_jobs[i])] == 3 and hash_function >= JobSecurityLevel3[int(sorted_jobs[i])]:
                    suc = 1
                '''
                suc_count += suc
                
            
            Total_cost = VM_cost + Security_cost
            suc_rate = suc_count / self.dag.n_job

            if makespan < min_makespan:
                min_makespan = makespan
            if Total_cost < min_Total_cost:    
                min_Total_cost = Total_cost
            if suc_rate < min_suc_rate:    
                min_suc_rate = suc_rate
                


            # 判断条件👇


            '''
            energy_delta = evaluate_solution(neighbor_solution) - evaluate_solution(current_solution)
            
            if energy_delta < 0 or random.random() < math.exp(-energy_delta / temperature):
                current_solution = neighbor_solution
                
            if evaluate_solution(current_solution) < evaluate_solution(best_solution):
                best_solution = current_solution
                
            temperature *= cooling_rate
            '''
        return min_makespan, min_Total_cost, min_suc_rate
    
    # 生成邻域新解
    def get_neighborhood(self, current_solution):
        numbers = len(current_solution)
        #随机生成两个不重复的点
        positions = np.random.choice(list(range(numbers)), replace=False, size = 2)
        lower_position = min(positions[0], positions[1])
        upper_position = max(positions[0], positions[1])
        
        reversed_list = list(reversed(current_solution[lower_position:upper_position]))
        current_solution[lower_position:upper_position] = reversed_list
        neighbor_solution = current_solution
        '''
        #将数列中段逆转
        mid_reversed = current_solution[lower_position:upper_position + 1]
        mid_reversed.reverse()
        #拼接生成新的数列
        neighbor_solution = current_solution[:lower_position]
        neighbor_solution.extend(mid_reversed)
        neighbor_solution.extend(current_solution[upper_position + 1:])
        '''
        return neighbor_solution
