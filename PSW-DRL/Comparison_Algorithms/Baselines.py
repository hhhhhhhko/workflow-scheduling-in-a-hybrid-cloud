import numpy as np

class Baselines:
    def __init__(self, dag, args):
        self.dag = dag
        self.args = args
        # 虚拟机VM
        self.VMnum = self.args.VM_Num # 虚拟机数量
        self.PrivateCloudNum = self.args.Private_Cloud_Num # 私有云数量
        self.PublicCloudNum = self.args.Public_Cloud_Num # 公有云数量
        self.PrivateCloudVMCost = self.args.Private_Cloud_VM_Cost # 私有云虚拟机价格
        self.PublicCloudVMCost = self.args.Public_Cloud_VM_Cost # 公有云虚拟机价格
        self.PrivateCloudVMCapacity = self.args.Private_Cloud_VM_Capacity # 私有云虚拟机计算能力
        self.PublicCloudVMCapacity = self.args.Public_Cloud_VM_Capacity # 公有云虚拟机计算能力
        self.VMType = self.args.VM_Type # 虚拟机类型：私有云或公有云
        self.runtime = self.dag.runtime 
        self.privacy_security_level = self.dag.privacy_security_level

        self.JobSecurityLevel1 = np.ones(self.dag.n_job) * 0.2 # 任务的用户认证安全等级
        self.JobSecurityLevel2 = np.ones(self.dag.n_job) * 0.2 # 任务的保密性安全等级
        self.JobSecurityLevel3 = np.ones(self.dag.n_job) * 0.2 # 任务的完整性安全等级

        self.user_authentication = self.args.User_Authentication_Security_Level[1]
        self.cryptographic_method = self.args.Cryptographic_Security_Level[5]
        self.hash_function = self.args.Hash_Function_Security_Level[5]

        self.UserAuthenticationCost = self.args.User_Authentication_Cost # 用户认证方法的成本 
        self.CryptographicMethodCost = self.args.Cryptographic_Method_Cost # 保密性加密算法方法的成本
        self.HashFunctionCost = self.args.Hash_Function_Cost # 完整性哈希函数方法的成本

        self.UserAuthenticationOverhead = self.args.User_Authentication_Overhead
        self.CryptographicMethodSpeed = self.args.Cryptographic_Method_Speed
        self.HashFunctionSpeed = self.args.Hash_Function_Speed

        self.inputfilesize = self.dag.inputfilesize
        self.outputfilesize = self.dag.outputfilesize

        self.computation_costs = np.zeros((self.dag.n_job, self.VMnum))   # 运算时间的二维数组
        for i in range(self.dag.n_job):
            for j in range(self.VMnum):
                if self.VMType[j] == 0: # 私有云
                    self.computation_costs[i][j] = self.runtime[i] / self.PrivateCloudVMCapacity[j]
                else: # 公有云
                    self.computation_costs[i][j] = self.runtime[i] / self.PublicCloudVMCapacity[j - 8]

    # 随机调度策略
    def Random(self):
        makespan = 0
        VM_cost = 0
        Security_cost = 0
        suc_count = 0
        Total_cost = 0
        suc_rate = 0
        for i in range(self.dag.n_job):
            VM_selected = np.random.randint(self.VMnum)
            
            # 计算makespan
            Texe = 0
            if self.VMType[VM_selected] == 0:
                Texe = self.runtime[i] / self.PrivateCloudVMCapacity[VM_selected]
            elif self.VMType[VM_selected] == 1:
                Texe = self.runtime[i] / self.PublicCloudVMCapacity[VM_selected - 8]
            

            real_Texe = 0
            if self.VMType[VM_selected] == 0:
                real_Texe = Texe
            else:
                if self.privacy_security_level[i] == 3:
                    real_Texe = Texe + (self.inputfilesize[i] + self.inputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
                else:
                    real_Texe = Texe + self.UserAuthenticationOverhead[1] + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.CryptographicMethodSpeed[5] *1000000) + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            '''
            real_Texe = 0
            if self.privacy_security_level[i] == 1:
                real_Texe = Texe
            elif self.privacy_security_level[i] == 2:
                real_Texe = Texe + self.UserAuthenticationOverhead[1] + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.CryptographicMethodSpeed[5] *1000000) + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            elif self.privacy_security_level[i] == 3:
                real_Texe = Texe + (self.inputfilesize[i] + self.inputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            '''
            makespan += real_Texe

            # 计算成本
            cost = 0
            if self.VMType[VM_selected] == 0: # 私有云
                cost = self.computation_costs[i][VM_selected] * self.PrivateCloudVMCost[VM_selected]
            else: # 公有云
                cost = self.computation_costs[i][VM_selected] * self.PublicCloudVMCost[VM_selected - 8]
            VM_cost += cost

            cost1 = 0
            if self.VMType[VM_selected] == 0:
                cost1 = 0
            else:
                if self.privacy_security_level[i] == 3:
                    cost1 = self.HashFunctionCost[5] * real_Texe
                else:
                    cost1 = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * real_Texe
            '''
            cost1 = 0
            if self.privacy_security_level[i] == 2:
                cost1 = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * real_Texe
            elif self.privacy_security_level[i] == 3:
                cost1 = self.HashFunctionCost[5] * real_Texe
            '''
            Security_cost += cost1

            # 计算成功率
            suc = 0
            if self.privacy_security_level[i] == 1:
                if self.VMType[VM_selected] == 0:
                    suc = 1
            elif self.privacy_security_level[i] == 2:
                if self.VMType[VM_selected] == 0:
                    suc = 1
                else:
                    if self.user_authentication >= self.JobSecurityLevel1[i] and self.cryptographic_method >= self.JobSecurityLevel2[i] and self.hash_function >= self.JobSecurityLevel3[i]:
                        suc = 1
            elif self.privacy_security_level[i] == 3:
                if self.VMType[VM_selected] == 0:
                    suc = 1
                else:
                    if self.hash_function >= self.JobSecurityLevel3[i]:
                        suc = 1
            '''
            suc = 0
            if self.privacy_security_level[i] == 1:
                if self.VMType[VM_selected] == 0:
                    suc = 1
            elif self.privacy_security_level[i] == 2 and self.user_authentication >= self.JobSecurityLevel1[i] and self.cryptographic_method >= self.JobSecurityLevel2[i] and self.hash_function >= self.JobSecurityLevel3[i]:
                suc = 1
            elif self.privacy_security_level[i] == 3 and self.hash_function >= self.JobSecurityLevel3[i]:
                suc = 1
            '''
            suc_count += suc

        Total_cost = VM_cost + Security_cost
        suc_rate = suc_count / self.dag.n_job

        return makespan, Total_cost, suc_rate
    

    # round robin调度策略
    def RoundRobin(self):
        makespan = 0
        VM_cost = 0
        Security_cost = 0
        suc_count = 0
        Total_cost = 0
        suc_rate = 0
        for i in range(self.dag.n_job):
            VM_selected = (self.dag.n_job - 1) % self.VMnum
            
            # 计算makespan
            if self.VMType[VM_selected] == 0:
                Texe = self.runtime[i] / self.PrivateCloudVMCapacity[VM_selected]
            elif self.VMType[VM_selected] == 1:
                Texe = self.runtime[i] / self.PublicCloudVMCapacity[VM_selected - 8]
            
            real_Texe = 0
            if self.VMType[VM_selected] == 0:
                real_Texe = Texe
            else:
                if self.privacy_security_level[i] == 3:
                    real_Texe = Texe + (self.inputfilesize[i] + self.inputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
                else:
                    real_Texe = Texe + self.UserAuthenticationOverhead[1] + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.CryptographicMethodSpeed[5] *1000000) + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            '''
            real_Texe = 0
            if self.privacy_security_level[i] == 1:
                real_Texe = Texe
            elif self.privacy_security_level[i] == 2:
                real_Texe = Texe + self.UserAuthenticationOverhead[1] + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.CryptographicMethodSpeed[5] *1000000) + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            elif self.privacy_security_level[i] == 3:
                real_Texe = Texe + (self.inputfilesize[i] + self.inputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            '''
            makespan += real_Texe

            # 计算成本
            cost = 0
            if self.VMType[VM_selected] == 0: # 私有云
                cost = self.computation_costs[i][VM_selected] * self.PrivateCloudVMCost[VM_selected]
            else: # 公有云
                cost = self.computation_costs[i][VM_selected] * self.PublicCloudVMCost[VM_selected - 8]
            VM_cost += cost

            cost1 = 0
            if self.VMType[VM_selected] == 0:
                cost1 = 0
            else:
                if self.privacy_security_level[i] == 3:
                    cost1 = self.HashFunctionCost[5] * real_Texe
                else:
                    cost1 = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * real_Texe
            '''
            cost1 = 0
            if self.privacy_security_level[i] == 2:
                #cost1 = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * self.computation_costs[i][VM_selected]
                cost1 = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * real_Texe
            elif self.privacy_security_level[i] == 3:
                cost1 = self.HashFunctionCost[5] * real_Texe
            '''
            Security_cost += cost1

            # 计算成功率
            suc = 0
            if self.privacy_security_level[i] == 1:
                if self.VMType[VM_selected] == 0:
                    suc = 1
            elif self.privacy_security_level[i] == 2:
                if self.VMType[VM_selected] == 0:
                    suc = 1
                else:
                    if self.user_authentication >= self.JobSecurityLevel1[i] and self.cryptographic_method >= self.JobSecurityLevel2[i] and self.hash_function >= self.JobSecurityLevel3[i]:
                        suc = 1
            elif self.privacy_security_level[i] == 3:
                if self.VMType[VM_selected] == 0:
                    suc = 1
                else:
                    if self.hash_function >= self.JobSecurityLevel3[i]:
                        suc = 1
            '''
            suc = 0
            if self.privacy_security_level[i] == 1:
                if self.VMType[VM_selected] == 0:
                    suc = 1
            elif self.privacy_security_level[i] == 2 and self.user_authentication >= self.JobSecurityLevel1[i] and self.cryptographic_method >= self.JobSecurityLevel2[i] and self.hash_function >= self.JobSecurityLevel3[i]:
                suc = 1
            elif self.privacy_security_level[i] == 3 and self.hash_function >= self.JobSecurityLevel3[i]:
                suc = 1
            '''
            suc_count += suc

        Total_cost = VM_cost + Security_cost
        suc_rate = suc_count / self.dag.n_job

        return makespan, Total_cost, suc_rate   
    
    # 最早调度策略
    def Earliest(self):
        makespan = 0
        VM_cost = 0
        Security_cost = 0
        suc_count = 0
        Total_cost = 0
        suc_rate = 0
        VM_idleTs = np.zeros(self.VMnum) # 存每个VM的最早空闲时间
        VM_update = 0
        VM_selected = 0
        for i in range(self.dag.n_job):
            VM_selected = np.argmin(VM_idleTs) # 选择新的最早空闲的VM
            
            # 更新完成任务对应的VM的最早空闲时间
            if i != 0:
                if self.VMType[VM_update] == 0:
                    VM_idleTs[VM_update] -= self.runtime[i] / self.PrivateCloudVMCapacity[VM_update]  
                elif self.VMType[VM_update] == 1:
                    VM_idleTs[VM_update] -= self.runtime[i] / self.PublicCloudVMCapacity[VM_update - 8]
            
            VM_update = VM_selected
            # 更新VM的最早空闲时间
            if self.VMType[VM_selected] == 0: 
                VM_idleTs[VM_selected] += self.runtime[i] / self.PrivateCloudVMCapacity[VM_selected] 
            elif self.VMType[VM_selected] == 1:
                VM_idleTs[VM_selected] += self.runtime[i] / self.PublicCloudVMCapacity[VM_selected - 8]
            
            # 计算makespan
            if self.VMType[VM_selected] == 0:
                Texe = self.runtime[i] / self.PrivateCloudVMCapacity[VM_selected]
            elif self.VMType[VM_selected] == 1:
                Texe = self.runtime[i] / self.PublicCloudVMCapacity[VM_selected - 8]
            
            real_Texe = 0
            if self.VMType[VM_selected] == 0:
                real_Texe = Texe
            else:
                if self.privacy_security_level[i] == 3:
                    real_Texe = Texe + (self.inputfilesize[i] + self.inputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
                else:
                    real_Texe = Texe + self.UserAuthenticationOverhead[1] + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.CryptographicMethodSpeed[5] *1000000) + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            '''
            real_Texe = 0
            if self.privacy_security_level[i] == 1:
                real_Texe = Texe
            elif self.privacy_security_level[i] == 2:
                real_Texe = Texe + self.UserAuthenticationOverhead[1] + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.CryptographicMethodSpeed[5] *1000000) + (self.inputfilesize[i] + self.outputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            elif self.privacy_security_level[i] == 3:
                real_Texe = Texe + (self.inputfilesize[i] + self.inputfilesize[i]) / (self.HashFunctionSpeed[5] *1000000)
            '''
            makespan += real_Texe

            # 计算成本
            cost = 0
            if self.VMType[VM_selected] == 0: # 私有云
                cost = self.computation_costs[i][VM_selected] * real_Texe
            else: # 公有云
                cost = self.computation_costs[i][VM_selected] * real_Texe
            VM_cost += cost

            cost1 = 0
            if self.VMType[VM_selected] == 0:
                cost1 = 0
            else:
                if self.privacy_security_level[i] == 3:
                    cost1 = self.HashFunctionCost[5] * real_Texe
                else:
                    cost1 = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * real_Texe
            '''
            cost1 = 0
            if self.privacy_security_level[i] == 2:
                cost1 = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * self.computation_costs[i][VM_selected]
            elif self.privacy_security_level[i] == 3:
                cost1 = self.HashFunctionCost[5] * self.computation_costs[i][VM_selected]
            '''
            Security_cost += cost1

            # 计算成功率
            suc = 0
            if self.privacy_security_level[i] == 1:
                if self.VMType[VM_selected] == 0:
                    suc = 1
            elif self.privacy_security_level[i] == 2:
                if self.VMType[VM_selected] == 0:
                    suc = 1
                else:
                    if self.user_authentication >= self.JobSecurityLevel1[i] and self.cryptographic_method >= self.JobSecurityLevel2[i] and self.hash_function >= self.JobSecurityLevel3[i]:
                        suc = 1
            elif self.privacy_security_level[i] == 3:
                if self.VMType[VM_selected] == 0:
                    suc = 1
                else:
                    if self.hash_function >= self.JobSecurityLevel3[i]:
                        suc = 1
            '''
            suc = 0
            if self.privacy_security_level[i] == 1:
                if self.VMType[VM_selected] == 0:
                    suc = 1
            elif self.privacy_security_level[i] == 2 and self.user_authentication >= self.JobSecurityLevel1[i] and self.cryptographic_method >= self.JobSecurityLevel2[i] and self.hash_function >= self.JobSecurityLevel3[i]:
                suc = 1
            elif self.privacy_security_level[i] == 3 and self.hash_function >= self.JobSecurityLevel3[i]:
                suc = 1
            '''
            suc_count += suc

        Total_cost = VM_cost + Security_cost
        suc_rate = suc_count / self.dag.n_job

        return makespan, Total_cost, suc_rate  