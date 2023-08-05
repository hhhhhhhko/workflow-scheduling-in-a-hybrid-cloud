import numpy as np
from preprocess.Workflow import Scientific_Workflow

class HEFT:
    def __init__(self, dag, args):
        self.dag = dag
        self.args = args

    def heft(self):
        # 虚拟机VM
        VMnum = self.args.VM_Num # 虚拟机数量
        PrivateCloudNum = self.args.Private_Cloud_Num # 私有云数量
        PublicCloudNum = self.args.Public_Cloud_Num # 公有云数量
        PrivateCloudVMCost = self.args.Private_Cloud_VM_Cost # 私有云虚拟机价格
        PublicCloudVMCost = self.args.Public_Cloud_VM_Cost # 公有云虚拟机价格
        PrivateCloudVMCapacity = self.args.Private_Cloud_VM_Capacity # 私有云虚拟机计算能力
        PublicCloudVMCapacity = self.args.Public_Cloud_VM_Capacity # 公有云虚拟机计算能力
        VMType = self.args.VM_Type # 虚拟机类型：私有云或公有云

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

        earliest_finish_times = np.zeros((VMnum, self.dag.n_job)) # 每个处理器上每个任务的最早完成时间
        
        scientific_workflow = Scientific_Workflow('CyberShake', 100)
        dag = scientific_workflow.get_workflow()
        ranking_list = dag.get_ranku() # ranku数组
        
        scheduled_jobs = np.zeros(self.dag.n_job) # 记录每个任务调度到的处理器

        UserAuthenticationOverhead = self.args.User_Authentication_Overhead
        CryptographicMethodSpeed = self.args.Cryptographic_Method_Speed
        HashFunctionSpeed = self.args.Hash_Function_Speed

        inputfilesize = self.dag.inputfilesize
        outputfilesize = self.dag.outputfilesize

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
                if privacy_security_level[task_index] == 1:
                    finish_time = computation_costs[task_index][j] + max(earliest_finish_times[j])
                elif privacy_security_level[task_index] == 2:
                    finish_time = computation_costs[task_index][j] + UserAuthenticationOverhead[1] + (inputfilesize[task_index] + outputfilesize[task_index]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[task_index] + outputfilesize[task_index]) / (HashFunctionSpeed[5] *1000000) + max(earliest_finish_times[j])
                elif privacy_security_level[task_index] == 3:
                    finish_time = computation_costs[task_index][j] + (inputfilesize[task_index] + inputfilesize[task_index]) / (HashFunctionSpeed[5] *1000000) + max(earliest_finish_times[j])
                if finish_time < earliest_finish_time:
                    earliest_finish_time = finish_time
                    earliest_VM = j
            
            # 更新所选处理器的最早完成时间和任务调度
            if privacy_security_level[task_index] == 1:
                earliest_finish_times[earliest_VM] += computation_costs[task_index][earliest_VM]
            elif privacy_security_level[task_index] == 2:
                earliest_finish_times[earliest_VM] += computation_costs[task_index][earliest_VM] + UserAuthenticationOverhead[1] + (inputfilesize[task_index] + outputfilesize[task_index]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[task_index] + outputfilesize[task_index]) / (HashFunctionSpeed[5] *1000000)
            elif privacy_security_level[task_index] == 3:
                earliest_finish_times[earliest_VM] += computation_costs[task_index][earliest_VM] + (inputfilesize[task_index] + inputfilesize[task_index]) / (HashFunctionSpeed[5] *1000000)
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

        # 计算调度方案的成功率
        suc_count = 0
        for i in range(self.dag.n_job):
            suc = 0
            if privacy_security_level[int(sorted_jobs[i])] == 1:
                if VMType[int(scheduled_jobs[i])] == 0:
                    suc = 1
            elif privacy_security_level[int(sorted_jobs[i])] == 2:
                if VMType[int(scheduled_jobs[i])] == 0:
                    suc = 1
                else:
                    if user_authentication >= JobSecurityLevel1[int(sorted_jobs[i])] and cryptographic_method >= JobSecurityLevel2[int(sorted_jobs[i])] and hash_function >= JobSecurityLevel3[int(sorted_jobs[i])]:
                        suc = 1
            elif privacy_security_level[int(sorted_jobs[i])] == 3:
                if VMType[int(scheduled_jobs[i])] == 0:
                    suc = 1
                else:
                    if hash_function >= JobSecurityLevel3[int(sorted_jobs[i])]:
                        suc = 1
            suc_count += suc
        '''
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
        '''
        suc_rate = suc_count / self.dag.n_job
        
        Security_cost = 0
        for i in range(self.dag.n_job):
            cost1 = 0
            if VMType[int(scheduled_jobs[i])] == 0:
                cost1 = 0
            else:
                if privacy_security_level[int(sorted_jobs[i])] == 3:
                    cost1 = HashFunctionCost[5] * (computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])] + (inputfilesize[int(sorted_jobs[i])] + inputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000))
                else:
                    cost1 = UserAuthenticationCost[1] + (CryptographicMethodCost[5] + HashFunctionCost[5]) * (computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])] + UserAuthenticationOverhead[1] + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000))
            Security_cost += cost1
        '''
        for i in range(self.dag.n_job):
            cost1 = 0
            if privacy_security_level[int(sorted_jobs[i])] == 2:
                cost1 = UserAuthenticationCost[1] + (CryptographicMethodCost[5] + HashFunctionCost[5]) * (computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])] + UserAuthenticationOverhead[1] + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[int(sorted_jobs[i])] + outputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000))
            elif privacy_security_level[int(sorted_jobs[i])] == 3:
                cost1 = HashFunctionCost[5] * (computation_costs[int(sorted_jobs[i])][int(scheduled_jobs[i])] + (inputfilesize[int(sorted_jobs[i])] + inputfilesize[int(sorted_jobs[i])]) / (HashFunctionSpeed[5] *1000000))
            Security_cost += cost1
        '''
        cost = VM_cost + Security_cost


        return makespan, cost, suc_rate
        