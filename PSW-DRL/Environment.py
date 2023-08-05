import numpy as np
import random
from preprocess.XMLProcess import XMLtoDAG
from preprocess.Workflow import Scientific_Workflow

'''
    混合云环境: 定义混合云、功能(反馈reward、记录数据等)、虚拟机VM、任务(任务的执行时间、任务的依赖关系等)
'''

# 定义云上的虚拟机
class VM:
    def __init__(self, vm_id, vm_type, vm_cost, vm_cpu, vm_capacity, vm_bandwidth):
        '''
        vm_id : 虚拟机的ID
        vm_type : 虚拟机的类型
        vm_cost : 虚拟机的成本
        vm_cpu : 虚拟机的CPU核心数量
        vm_capacity : 虚拟机的计算能力
        vm_bandwidth : 虚拟机的带宽
        idle=True : 判断是否空闲
        processing_task : 正在处理的任务编号
        remain_process : 剩余的处理时间
        '''

        self.vm_id = vm_id
        self.vm_type = vm_type
        self.vm_cost = vm_cost
        self.vm_cpu = vm_cpu
        self.vm_capacity = vm_capacity
        self.vm_bandwidth = vm_bandwidth
        self.idle = True
        self.processing_task = 0
        self.remain_process = 0


# 定义云集群
class Cloud_Cluster:
    def __init__(self, num_of_vm):
        '''
        num_of_vm : 一个云集群中虚拟机的数量
        self.core[] :云集群中的虚拟机实例
        '''

        self.num_of_vm = num_of_vm
        # 就绪的vm实例
        self.vm = []
        for i in range(self.num_of_vm):
            self.vm.append(VM())

    # 返回空闲虚拟机编号
    def idle_vm(self):
        for i in range(self.num_of_vm):
            if(self.vm[i].idle == True):
                return i
        
        return -1

    # 返回当前正在处理的任务的列表
    def processing_tasks(self):
        list = []
        
        for i in range(self.num_of_vm):
            if(self.vm[i].idle == False):
                list.append(self.vm[i].processing_task)
        
        return list


# 定义混合云环境（包含私有云集群和公有云集群）
class Hybrid_Cloud_Env:
    def __init__(self, num_of_private_cloud, num_of_public_cloud, num_of_vm, inout_ratio):
        '''
        num_of_private_cloud : 混合云环境中私有云的数量
        num_of_public_cloud : 混合云环境中公有云的数量
        num_of_vm : 一个云集群中虚拟机的数量
        inout_ratio : 集群外通信时间与集群内通信时间的比率
        cloud_cluster[]：混合云环境中的云群集
        '''

        self.num_of_private_cloud = num_of_private_cloud
        self.num_of_public_cloud = num_of_public_cloud
        self.num_of_vm = num_of_vm
        self.inout_ratio = inout_ratio
        # 已有的的云集群
        self.cloud_cluster = []
        for i in range(self.num_of_private_cloud + self.num_of_public_cloud):
            self.cloud_cluster.append(Cloud_Cluster(self.num_of_vm))

    # 返回当前正在处理的任务的列表
    def processing_tasks(self):
        processing_tasks = []
        
        for i in range(self.num_of_private_cloud + self.num_of_public_cloud):
            list = self.cloud_cluster[i].processing_tasks()
            processing_tasks = processing_tasks + list
        
        return processing_tasks
    
    # 判断云集群是否空闲(所有的虚拟机都空闲)
    def empty_cloud_cluster(self):
        for i in range(self.num_of_private_cloud + self.num_of_public_cloud):
            if(self.cloud_cluster[i].idle_vm() != -1):
                return True
        
        return False
    

'''
用一个def feedback()函数来实现对环境的反馈, 得到
'''

# def feedback():
    


# 定义混合云环境
class Env:
    # 虚拟机和工作流任务的参数定义
    def __init__(self, args):
        scientific_workflow = Scientific_Workflow('CyberShake', 100)
        self.dag = scientific_workflow.get_workflow()

        # 虚拟机
        self.VMnum = args.VM_Num # 虚拟机数量
        self.PrivateCloudNum = args.Private_Cloud_Num # 私有云数量
        self.PublicCloudNum = args.Public_Cloud_Num # 公有云数量
        self.PrivateCloudVMCost = args.Private_Cloud_VM_Cost # 私有云虚拟机价格
        self.PublicCloudVMCost = args.Public_Cloud_VM_Cost # 公有云虚拟机价格
        self.PrivateCloudVMCapacity = args.Private_Cloud_VM_Capacity # 私有云虚拟机计算能力
        self.PublicCloudVMCapacity = args.Public_Cloud_VM_Capacity # 公有云虚拟机计算能力
        self.VMType = args.VM_Type # 虚拟机类型：私有云或公有云

        # 工作流
        self.WorkflowNum = args.Workflow_Num # 工作流数量
        self.lamda = args.lamda # 工作流平均到达速度
        self.WorkflowddL = args.Workflow_ddl # 工作流 QoS 响应时间要求
        self.Workflowddlfactor = args.Workflow_Deadline_Factor

        # 边
        self.EdgeNum = args.Edge_Num # 边数量
        '''
        self.EdgeSecurityLevel1 = np.ones(self.EdgeNum) * random.random() # 边的用户认证安全等级
        self.EdgeSecurityLevel2 = np.ones(self.EdgeNum) * random.random() # 边的保密性安全等级
        self.EdgeSecurityLevel3 = np.ones(self.EdgeNum) * random.random() # 边的完整性安全等级
        self.PrivacyFactor = args.Privacy_Factor # Privacy Factor
        self.EdgeTag = np.ones(self.EdgeNum) * np.random.choice([1,2,3], p=[args.Privacy_Factor,(1-args.Privacy_Factor)/2, (1-args.Privacy_Factor)/2])
        '''

        # 任务
        self.JobNum = args.Job_Num # 任务数量
        
        self.JobSecurityLevel1 = np.ones(self.JobNum) * 0.2 # 任务的用户认证安全等级
        self.JobSecurityLevel2 = np.ones(self.JobNum) * 0.2 # 任务的保密性安全等级
        self.JobSecurityLevel3 = np.ones(self.JobNum) * 0.2 # 任务的完整性安全等级
        '''
        self.JobSecurityLevel1 = np.ones(self.JobNum) * random.random() # 任务的用户认证安全等级
        self.JobSecurityLevel2 = np.ones(self.JobNum) * random.random() # 任务的保密性安全等级
        self.JobSecurityLevel3 = np.ones(self.JobNum) * random.random() # 任务的完整性安全等级
        '''
        self.JobPFactor = args.Job_Privacy_Factor # Privacy Factor
        self.JobTag = np.ones(self.JobNum) * np.random.choice([1,2,3], p=[args.Job_Privacy_Factor,(1-args.Job_Privacy_Factor)/2, (1-args.Job_Privacy_Factor)/2])
                                   # 任务的隐私安全(调度)标签
        

        # 环境
        '''
        self.SecurityMethodNum = args.Security_Method_Num # 安全方法数量
        self.SecurityMethodCost = args.Security_Method_Cost # 安全方法成本
        self.SecurityMethodSpeed = args.Security_Method_Speed # 安全方法速度
        self.SecurityMethodType = args.Security_Method_Type # 安全方法类型
        self.SecurityMethodLevel = args.Security_Method_Level # 安全方法的安全等级
        '''   
        self.UserAuthenticationNum = args.User_Authentication_Num # 用户认证方法数量
        self.UserAuthenticationLevel = args.User_Authentication_Security_Level # 用户认证方法的安全等级
        self.UserAuthenticationOverhead = args.User_Authentication_Overhead # 用户认证方法的成本
        self.UserAuthenticationCost = args.User_Authentication_Cost # 用户认证方法的成本
        self.CryptographicMethodNum = args.Cryptographic_Method_Num # 保密性加密算法方法数量
        self.CryptographicScurityLevel = args.Cryptographic_Security_Level # 保密性加密算法方法的安全等级
        self.CryptographicMethodSpeed = args.Cryptographic_Method_Speed # 保密性加密算法方法的速度
        self.CryptographicMethodCost = args.Cryptographic_Method_Cost # 保密性加密算法方法的成本
        self.HashFunctionNum = args.Hash_Function_Num # 完整性哈希函数方法数量
        self.HashFunctionScurityLevel = args.Hash_Function_Security_Level # 完整性哈希函数方法的安全等级
        self.HashFunctionSpeed = args.Hash_Function_Speed # 完整性哈希函数方法的速度
        self.HashFunctionCost = args.Hash_Function_Cost # 完整性哈希函数方法的成本

        # 记录状态state
        self.DQN_events = np.zeros((12, self.JobNum))
        self.DQN_VM_events = np.zeros((2, self.VMnum))

        # 还需要补充👇


    #  生成工作负载（任务的隐私安全等级、）
    # def gen_workload(self):  


    #  重置环境
    def reset(self, args):
        self.VMType = args.VM_Type
        
        self.JobSecurityLevel1 = np.ones(self.JobNum) * 0.2 # 任务的用户认证安全等级
        self.JobSecurityLevel2 = np.ones(self.JobNum) * 0.2 # 任务的保密性安全等级
        self.JobSecurityLevel3 = np.ones(self.JobNum) * 0.2 # 任务的完整性安全等级
        '''
        self.JobSecurityLevel1 = np.ones(self.JobNum) * random.random() # 任务的用户认证安全等级
        self.JobSecurityLevel2 = np.ones(self.JobNum) * random.random() # 任务的保密性安全等级
        self.JobSecurityLevel3 = np.ones(self.JobNum) * random.random() # 任务的完整性安全等级
        '''
        self.JobTag = np.ones(self.JobNum) * np.random.choice([1,2,3], p=[args.Job_Privacy_Factor,(1-args.Job_Privacy_Factor)/2, (1-args.Job_Privacy_Factor)/2])
        # 还需要补充👇

        self.DQN_events = np.zeros((12, self.JobNum)) # DQN
        self.DQN_VM_events = np.zeros((2, self.VMnum))
  

    # 读取新的任务
    def load_new_job(self, job_count, job_id, dag):
        jobs = [row for row in dag.jobs if row['id'] == job_id]
        if job_count == self.JobNum - 1:
            finish = True
        else:
            finish = False
        job_attrs = jobs
        return finish, job_attrs

    
    # 任务执行结束后，计算reward并记录虚拟机和任务记录
    def feedback(self, job_attrs, action):
        job_id = job_attrs[0]['id']
        job_name = job_attrs[0]['name']
        job_namespace = job_attrs[0]['namespace']
        job_runtime = job_attrs[0]['runtime']
        job_inputfilesize = job_attrs[0]['inputfilesize']
        job_outputfilesize = job_attrs[0]['outputfilesize']
        job_privacy_security_level = job_attrs[0]['privacy_security_level']
        # 还需要补什么👇 cost、makespan、deadline····，选择是公还是私，哪个VM，cost是什么
        arrival_time = 0 # 到达时间

        # 选择安全方法
        user_authentication = self.UserAuthenticationLevel[1]
        cryptographic_method = self.CryptographicScurityLevel[5]
        hash_function = self.HashFunctionScurityLevel[5]

        # 判断是否满足安全等级
        
        
        '''
        edges = self.dag.edges
        if edges[action] #👈应该是按边来的
        '''
        security = 0
        if job_privacy_security_level == 2:
            if user_authentication >= self.JobSecurityLevel1[job_id] and cryptographic_method >= self.JobSecurityLevel2[job_id] and hash_function >= self.JobSecurityLevel3[job_id]:
                security = 1
        elif job_privacy_security_level == 3:
            if hash_function >= self.JobSecurityLevel3[job_id]:
                security = 1
            

        #判别调度是否符合模型
        suc = 0 
        if job_privacy_security_level == 1:
            if self.VMType[action] == 0:
                suc = 1
        #elif job_privacy_security_level == 2 and security == 1:
        elif job_privacy_security_level == 2:
            if self.VMType[action] == 0:
                suc = 1
            else:
                if security == 1:
                    suc = 1
        elif job_privacy_security_level == 3:
            if self.VMType[action] == 0:
                suc = 1
            else:
                if security == 1:
                    suc = 1

        # 计算任务执行时间
        Texe = 0
        if self.VMType[action] == 0:
            Texe = job_runtime / self.PrivateCloudVMCapacity[action]
        else:
            Texe = job_runtime / self.PublicCloudVMCapacity[action - 8] ###

        # 计算真实任务执行时间(加上安全方法的时间) 👇如何考虑不同的云传输速度
        real_Texe = 0
        if self.VMType[action] == 0: # 若分配至私有云则不用选择安全方法
            real_Texe = Texe
        else: # 若分配至公有云则选择安全方法
            if job_privacy_security_level == 3: # 3的话只用选择HashFunction
                real_Texe = Texe + (job_inputfilesize + job_outputfilesize) / (self.HashFunctionSpeed[5] *1000000)
            else: # 1的话虽然已调度失败，但还是和2一样选择安全方法
                real_Texe = Texe + self.UserAuthenticationOverhead[1] + (job_inputfilesize + job_outputfilesize) / (self.CryptographicMethodSpeed[5] *1000000) + (job_inputfilesize + job_outputfilesize) / (self.HashFunctionSpeed[5] *1000000)
        '''
        real_Texe = 0
        if job_privacy_security_level == 1:
            real_Texe = Texe 
        elif job_privacy_security_level == 2:
            real_Texe = Texe + self.UserAuthenticationOverhead[1] + (job_inputfilesize + job_outputfilesize) / (self.CryptographicMethodSpeed[5] *1000000) + (job_inputfilesize + job_outputfilesize) / (self.HashFunctionSpeed[5] *1000000)
        elif job_privacy_security_level == 3:
            real_Texe = Texe + (job_inputfilesize + job_outputfilesize) / (self.HashFunctionSpeed[5] *1000000)
        '''

        # VM的空闲时间  
        Tidle = self.DQN_VM_events[0, action] 

        # 边上数据的传输时间


        # 计算任务的等待时间和开始时间
        if Tidle <= arrival_time:
            Twait = 0
            Tstart = arrival_time
        else:
            Twait = Tidle - arrival_time
            Tstart = Tidle

        Tduration = Twait + real_Texe # 任务的响应时间
        Tleave = Tstart + real_Texe # 任务的离开时间
        Tnew_idle = Tleave # VM的新的空闲时间

        # 计算成本
        VM_cost = (self.PrivateCloudVMCost[action] if self.VMType[action] == 0 else self.PublicCloudVMCost[action - 8]) * Texe
        #SecurityMethod_cost = (self.SecurityMethodCost[action]) * Texe  # 👈这个该如何选择？随机？如何计算？
        SecurityMethod_cost = 0
        if self.VMType[action] == 0: # 若分配至私有云则不用选择安全方法,且时间为texe
            SecurityMethod_cost = 0
        else: # 若分配至公有云则选择安全方法
            if job_privacy_security_level == 3: # 3的话只用选择HashFunction
                SecurityMethod_cost = self.HashFunctionCost[5] * real_Texe
            else: # 1的话虽然已调度失败，但还是和2一样选择安全方法
                SecurityMethod_cost = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * real_Texe
        '''
        SecurityMethod_cost = 0
        if job_privacy_security_level == 2:
            SecurityMethod_cost = self.UserAuthenticationCost[1] + (self.CryptographicMethodCost[5] + self.HashFunctionCost[5]) * real_Texe
        elif job_privacy_security_level == 3:
            SecurityMethod_cost = self.HashFunctionCost[5] * real_Texe
        '''
        cost = VM_cost + SecurityMethod_cost
        
        # 计算makespan，其为最后一个任务的离开时间

        # 计算reward
        '''
        #r1 = (1 + np.exp(1 + suc)) * (0.2) / Tduration  # R1考虑了任务的响应时间和调度成功与否
        #r1 = (1 + np.exp(10 + suc)) * (real_Texe) / Tduration  # R1考虑了任务的响应时间和调度成功与否
        #r1 = (1 + np.exp(2 + suc)) * (real_Texe) / Tduration  # R1考虑了任务的响应时间和调度成功与否
        #r1 = (1 + np.exp(5 + suc)) * (real_Texe) / Tduration  # R1考虑了任务的响应时间和调度成功与否
        '''
        #r1 = (1 + np.exp(5 + suc)) * (real_Texe) / Tduration  # R1考虑了任务的响应时间和调度成功与否
        if suc == 0:
            #r1 = - ((1 + np.exp(5 + suc)) * (real_Texe) / Tduration)
            #r1 = - np.exp(-(Tduration))
            #r1 = 0
            r1 = - 10 * (np.exp(0.01 * Tduration))
            #r1 =  5 * (- Tduration)
        else:
            #r1 = (1 + np.exp(4 + suc)) * (real_Texe) / Tduration
            #r1 = (1 + np.exp(1 + suc)) * (real_Texe) / Tduration
            #r1 = (1 + np.exp(3 + suc)) * (real_Texe) / Tduration
            #r1 = (np.exp(-(Tduration)))
            #r1 = 10000 * (np.exp(-(0.01 * Tduration)))
            #r1 = 10000 / Tduration
            #r1 = 10 * np.exp(-(Tduration))
            r1 = 1000 * (np.exp(-(0.01 * Tduration)))
            #r1 = - Tduration
        '''
        #r2 = (1 + np.exp(1.5 - cost)) * (Texe) / Tduration # R2考虑了成本(包括虚拟机成本和安全方法成本)
        #r2 = (1 + np.exp(300 - cost)) * (real_Texe) / Tduration # R2考虑了成本(包括虚拟机成本和安全方法成本)
        #r2 = (1 + np.exp(10 - cost)) * (real_Texe) / Tduration # R2考虑了成本(包括虚拟机成本和安全方法成本)
        #r2 = (1 + np.exp(5 - cost)) * (real_Texe) / Tduration # R2考虑了成本(包括虚拟机成本和安全方法成本)
        #r2 = (1 + np.exp(10 - cost)) * (real_Texe) / Tduration # R2考虑了成本(包括虚拟机成本和安全方法成本)
        '''
        #r2 = (1 + np.exp(5 - cost)) * (real_Texe) / Tduration # R2考虑了成本(包括虚拟机成本和安全方法成本)
        #r2 = 1 + np.exp(1.5 - cost)
        #r2 = 1 + np.exp(2.5 - cost)

        if suc == 0:
            #r2 = 0
            r2 = - 100
            #r2 =  - 500 * cost
        else:
            #r2 = 0.1 * np.exp( -(0.1 * cost))
            #r2 = 10 * np.exp(-(cost))
            r2 = 100 * np.exp( -(0.1 * cost))
            #r2 =  - 100 * cost

        #reward = 0.5 * r1 + 0.5 * r2
        reward = r1 + r2


        self.DQN_events[0, job_id] = action
        self.DQN_events[1, job_id] = Tstart
        self.DQN_events[2, job_id] = Twait
        self.DQN_events[3, job_id] = Tduration
        self.DQN_events[4, job_id] = Tleave
        self.DQN_events[5, job_id] = r1
        self.DQN_events[6, job_id] = Texe
        self.DQN_events[7, job_id] = cost
        self.DQN_events[8, job_id] = suc
        self.DQN_events[9, job_id] = r2
        self.DQN_events[10, job_id] = VM_cost
        self.DQN_events[11, job_id] = SecurityMethod_cost

        self.DQN_VM_events[0, action] = Tnew_idle
        self.DQN_VM_events[1, action] += 1
        
        return reward

        # wf_ddl = job_attrs[0]
        # wf_makespan = 
    
    # 获取虚拟机执行结束时间
    def get_VM_idleT(self):
        idleTimes = self.DQN_VM_events[0, :]
        return idleTimes 

    # 获取虚拟机和任务的状态state
    def getState(self, job_attrs):
        '''
        job_id = job_attrs[0]['id']
        job_name = job_attrs[1]['name']
        job_namespace = job_attrs[2]['namespace']
        job_runtime = job_attrs[3]['runtime']
        job_inputfilesize = job_attrs[4]['inputfilesize']
        job_outputfilesize = job_attrs[5]['outputfilesize']
        job_privacy_security_level = job_attrs[7]['privacy_security_level']
        '''
        job_id = job_attrs[0]['id']
        job_name = job_attrs[0]['name']
        job_namespace = job_attrs[0]['namespace']
        job_runtime = job_attrs[0]['runtime']
        job_inputfilesize = job_attrs[0]['inputfilesize']
        job_outputfilesize = job_attrs[0]['outputfilesize']
        job_privacy_security_level = job_attrs[0]['privacy_security_level']
        #job其他需要公式计算的属性👇  EST EFT等
        
        # state_job为需要返回的任务状态
        state_job = [job_privacy_security_level]

        idleTimes = self.get_VM_idleT()
        
        Tarrival = 0 # 到达时间
        waitTimes = [t - Tarrival for t in idleTimes]
        waitTimes = np.maximum(waitTimes, 0)
        state = np.hstack((state_job, waitTimes))
        return state
    

    # 用于计算各类指标用于实验评估的方法👇
    
    # 1.获取积累奖励大小
    def get_accumulate_rewards(self, start, end):  
        rewards = sum(self.DQN_events[5, start:end])
        return rewards

    # 2.获取最大完成时间(就是makespan?)
    def get_finishtime(self, start, end):
        finishtime = max(self.DQN_events[4, start:end])
        return finishtime
    
    # 3.获取平均执行时间
    def get_execute_time(self, start, end):
        execute_time = np.mean(self.DQN_events[6, start:end])
        return execute_time
    
    # 4.获取平均等待时间
    def get_wait_time(self, start, end):
        wait_time = np.mean(self.DQN_events[2, start:end])
        return wait_time
    
    # 5.获取平均响应时间
    def get_response_time(self, start, end):
        response_time = np.mean(self.DQN_events[3, start:end])
        return response_time
    
    # 获取makespan(也就是最后一个任务的离开时间)
    def get_makespan(self):
        makespan = max(self.DQN_events[4, :])
        return makespan

    # 获取总成本
    def get_total_cost(self):
        cost = sum(self.DQN_events[7, :])
        return cost
    
    # 获取调度模型成功率
    def get_suc_rate(self):
        suc_rate = np.sum(self.DQN_events[8, :]) / self.JobNum
        return suc_rate
    
    # 获取Twait一维数组
    def get_Twait(self):
        Twait = self.DQN_events[2, :]
        return Twait
    
    # 获取cost一维数组
    def get_cost(self):
        cost = self.DQN_events[7, :]
        return cost
    
    # 获取r1一维数组
    def get_reward1(self):
        reward1 = self.DQN_events[5, :]
        return reward1
    
    # 获取r2一维数组
    def get_reward2(self):
        reward2 = self.DQN_events[9, :]
        return reward2

    # 获取Tduration一维数组
    def get_Tduration(self):
        Tduration = self.DQN_events[3, :]
        return Tduration
    
    # 获取VM_cost一维数组
    def get_VM_cost(self):
        VM_cost = self.DQN_events[10, :]
        return VM_cost
    
    # 获取SecurityMethod_cost一维数组
    def get_SecurityMethod_cost(self):
        SecurityMethod_cost = self.DQN_events[11, :]
        return SecurityMethod_cost