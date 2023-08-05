import numpy as np
import heapq

class TSS:
    def __init__(self, dag, args):
        self.dag = dag
        self.args = args

    def tss(self):
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

        task_heap = []  # 用于存储任务的最小堆
        assigned_tasks = []  # 用于存储已分配的任务
        tasks = [i for i in range(self.dag.n_job)] # 任务列表
        for task in tasks:
            heapq.heappush(task_heap, task)

        # 判断是否符合DAG依赖性👇
        
        # 记录执行时间、成本、success
        Total_Texe = []
        Total_cost = []
        Total_suc = []

        VM_idle = np.zeros(PrivateCloudNum)  # 用于存储私有云VM是否空闲, 0表示空闲，1表示忙碌
        VM_idle_public = np.zeros(PublicCloudNum)  # 用于存储公有云VM是否空闲, 0表示空闲，1表示忙碌
        while task_heap:
            current_task = heapq.heappop(task_heap)
            if np.any(VM_idle == 0): # 判断私有云是否有空闲VM
                Texe = 0; cost = 0; suc = 0 # 初始化
                suitable_vms = [i for i in range(PrivateCloudNum) if VM_idle[i] == 0] # 找到空闲的VM
                best_vm = max(suitable_vms, key=lambda x: PrivateCloudVMCapacity[x]) # 找到计算能力最大的VM
                VM_idle[best_vm] = 1 # 将VM设置为忙碌
                Texe = runtime[current_task] / PrivateCloudVMCapacity[best_vm] # 计算任务执行时间
                
                if VMType[best_vm] == 0:
                    real_Texe = Texe
                else:
                    if privacy_security_level[current_task] == 3:
                        Texe + (inputfilesize[current_task] + inputfilesize[current_task]) / (HashFunctionSpeed[5] *1000000)
                    else:
                        real_Texe = Texe + UserAuthenticationOverhead[1] + (inputfilesize[current_task] + outputfilesize[current_task]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[current_task] + outputfilesize[current_task]) / (HashFunctionSpeed[5] *1000000)
                '''
                if privacy_security_level[current_task] == 1:
                    real_Texe = Texe
                elif privacy_security_level[current_task] == 2:
                    real_Texe = Texe + UserAuthenticationOverhead[1] + (inputfilesize[current_task] + outputfilesize[current_task]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[current_task] + outputfilesize[current_task]) / (HashFunctionSpeed[5] *1000000)
                elif privacy_security_level[current_task] == 3:
                    real_Texe = Texe + (inputfilesize[current_task] + inputfilesize[current_task]) / (HashFunctionSpeed[5] *1000000)
                '''

                Total_Texe.append(real_Texe)
                cost = PrivateCloudVMCost[best_vm] * real_Texe # 私有云中都满足隐私安全需求，只需考虑VM成本，且为成功调度suc=1
                Total_cost.append(cost)
                suc = 1
                Total_suc.append(suc)
                assigned_tasks.append((current_task, best_vm))
            else:
                # 还得考虑texe、tleave、tidle等👇
                Texe = 0; cost = 0; suc = 0; cost1 = 0; cost2 = 0 # 初始化
                # 👇要考虑离开时间等
                suitable_vms = [i for i in range(PublicCloudNum) if VM_idle_public[i] == 0] # 找到空闲的VM
                best_public_vm = min(suitable_vms, key=lambda x: PublicCloudVMCost[x])  # 私有云资源不足，则找到公有云中成本最低的VM
                # VM_idle_public[best_public_vm] = 1 # 将VM设置为忙碌
                Texe = runtime[current_task] / PublicCloudVMCapacity[best_public_vm] # 计算任务执行时间
                
                if VMType[best_public_vm] == 0:
                    real_Texe = Texe
                else:
                    if privacy_security_level[current_task] == 3:
                        real_Texe = Texe + (inputfilesize[current_task] + inputfilesize[current_task]) / (HashFunctionSpeed[5] *1000000)
                    else:
                        real_Texe = Texe + UserAuthenticationOverhead[1] + (inputfilesize[current_task] + outputfilesize[current_task]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[current_task] + outputfilesize[current_task]) / (HashFunctionSpeed[5] *1000000)
                '''
                if privacy_security_level[current_task] == 1:
                    real_Texe = Texe
                elif privacy_security_level[current_task] == 2:
                    real_Texe = Texe + UserAuthenticationOverhead[1] + (inputfilesize[current_task] + outputfilesize[current_task]) / (CryptographicMethodSpeed[5] *1000000) + (inputfilesize[current_task] + outputfilesize[current_task]) / (HashFunctionSpeed[5] *1000000)
                elif privacy_security_level[current_task] == 3:
                    real_Texe = Texe + (inputfilesize[current_task] + inputfilesize[current_task]) / (HashFunctionSpeed[5] *1000000)
                '''
                Total_Texe.append(real_Texe)
                cost1 = PublicCloudVMCost[best_public_vm] * real_Texe # 公有云中还要考虑安全方法成本
                
                if privacy_security_level[current_task] == 1:
                    suc = 0
                    cost2 = 0 

                elif privacy_security_level[current_task] == 2:
                    cost2 = UserAuthenticationCost[1] + (CryptographicMethodCost[5] + HashFunctionCost[5]) * real_Texe
                    if user_authentication >= JobSecurityLevel1[current_task] and cryptographic_method >= JobSecurityLevel2[current_task] and hash_function >= JobSecurityLevel3[current_task]:
                        suc = 1
                    else:
                        suc = 0
            
                elif privacy_security_level[current_task] == 3:
                    cost2 = HashFunctionCost[5] * real_Texe
                    if hash_function >= JobSecurityLevel3[current_task]:
                        suc = 1
                    else:
                        suc = 0
                cost = cost1 + cost2
                Total_cost.append(cost)
                Total_suc.append(suc)
                assigned_tasks.append((current_task, best_public_vm))

        # 计算makespan、cost、success
        makespan = np.sum(Total_Texe)
        cost = np.sum(Total_cost)
        suc_rate = np.sum(Total_suc) / self.dag.n_job

        return makespan, cost, suc_rate