'''
定义虚拟机、任务(从xml文件中提取后合并至args中)、DQN训练参数
'''

import argparse
from preprocess.XMLProcess import XMLtoDAG

# 参数设置
def parameter_parser():
    parser = argparse.ArgumentParser(description="SAIRL")

    """
    add_argument()方法

        name or flags - 一个命名或者一个选项字符串的列表
        
        action - 表示该选项要执行的操作
        
        default - 当参数未在命令行中出现时使用的值
        
        dest - 用来指定参数的位置
        
        type - 为参数类型,例如int
        
        choices - 用来选择输入参数的范围。例如choice = [1, 5, 10], 表示输入参数只能为1,5 或10
        
        help - 用来描述这个选项的作用
    """

    # 训练参数
    # 训练周期
    parser.add_argument("--Epoch",
                        type=int,
                        default=1000,
                        help="Training Epochs")
    
    '''
    DQN参数
    '''
    #   开始训练时间
    parser.add_argument("--Dqn_start_learn",
                        type=int,
                        default=2000, # 15 5000
                        help="Iteration start Learn for normal dqn")
    #   学习频率
    parser.add_argument("--Dqn_learn_interval",
                        type=int,
                        default=1,
                        help="Dqn's learning interval")
    #   学习率
    parser.add_argument("--Lr_DDQN",
                        type=float,
                        default=0.001,
                        help="Dueling DQN Lr")

    
    '''
    虚拟机参数
    '''
    # 虚拟机数量
    
    parser.add_argument("--VM_Num",
                        type=int,
                        default=16,
                        help="VM Num")
    '''
    parser.add_argument("--VM_Num",
                        type=int,
                        default=32,
                        help="VM Num")
    '''
    # 私有云数量
    
    parser.add_argument("--Private_Cloud_Num",
                        type=int,
                        default=8,
                        help="Private Cloud Num")
    '''
    parser.add_argument("--Private_Cloud_Num",
                        type=int,
                        default=16,
                        help="Private Cloud Num")
    '''
    
    # 公有云数量
    parser.add_argument("--Public_Cloud_Num",
                        type=int,
                        default=8,
                        help="Public Cloud Num")
    '''
    parser.add_argument("--Public_Cloud_Num",
                        type=int,
                        default=16,
                        help="Public Cloud Num")
    '''
    # 私有云虚拟机价格
    parser.add_argument("--Private_Cloud_VM_Cost",
                        type=list,
                        default=[0.024, 0.039, 0.056, 0.075, 0.096, 0.122, 0.151, 0.189],
                        help="Private Cloud VM Cost")
    '''
    parser.add_argument("--Private_Cloud_VM_Cost",
                        type=list,
                        default=[0.024, 0.039, 0.056, 0.075, 0.096, 0.122, 0.151, 0.189,0.024, 0.039, 0.056, 0.075, 0.096, 0.122, 0.151, 0.189],
                        help="Private Cloud VM Cost")
    '''
    # 公有云虚拟机价格
    parser.add_argument("--Public_Cloud_VM_Cost",
                        type=list,
                        default=[0.12, 0.195, 0.28, 0.375, 0.48, 0.61, 0.755, 0.945],
                        help="Public Cloud VM Cost")
    '''
    parser.add_argument("--Public_Cloud_VM_Cost",
                        type=list,
                        default=[0.12, 0.195, 0.28, 0.375, 0.48, 0.61, 0.755, 0.945,0.12, 0.195, 0.28, 0.375, 0.48, 0.61, 0.755, 0.945],
                        help="Public Cloud VM Cost")
    '''
    # 私有云虚拟机计算能力
    parser.add_argument("--Private_Cloud_VM_Capacity",
                        type=list,
                        default=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],
                        help="Private Cloud VM Capacity")
    '''
    parser.add_argument("--Private_Cloud_VM_Capacity",
                        type=list,
                        default=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5,1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],
                        help="Private Cloud VM Capacity")
    '''
    # 公有云虚拟机计算能力
    parser.add_argument("--Public_Cloud_VM_Capacity",
                        type=list,
                        default=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],
                        help="Public Cloud VM Capacity")
    '''
    parser.add_argument("--Public_Cloud_VM_Capacity",
                        type=list,
                        default=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5,1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5],
                        help="Public Cloud VM Capacity")
    '''
    # 区分私有云VM和公有云VM
    parser.add_argument("--VM_Type",
                        type=list,
                        default=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                        help="VM Type")
    '''
    parser.add_argument("--VM_Type",
                        type=list,
                        default=[0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0,1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1],
                        help="VM Type")


    
    工作流参数
    '''
    # 工作流平均到达速度
    parser.add_argument("--lamda",
                        type=int,
                        default=20,
                        help="The parameter used to control the length of each workflows.")
    # 工作流数量
    parser.add_argument("--Workflow_Num",
                        type=int,
                        default=8000,
                        help="The number of workflows.")
    # 工作流 QoS 响应时间要求
    parser.add_argument("--Workflow_ddl",
                        type=float,
                        default=0.25,
                        help="Deadline time of each workflows")
    # 工作流deadline factor
    parser.add_argument("--Workflow_Deadline_Factor",
                        type=float,
                        default=0.5,
                        help="Deadline factor of each workflows")


    '''
    边edge参数
    '''
    # 边数量
    parser.add_argument("--Edge_Num",
                        type=int,
                        default=380,
                        help="Edge Num")

    '''
    任务参数
    '''
    # 任务数量
    parser.add_argument("--Job_Num",
                        type=int,
                        default=100,
                        help="Job Num")
    # 任务安全级别(每个任务随机生成一个级别)
    parser.add_argument("--Job_Security_Level",
                        type=list,
                        default=[1, 2, 3, 1, 2, 1, 2, 3, 1, 2],
                        help="Job Security Level")
    # 任务隐私安全类别比例(L1,L2,L3)
    parser.add_argument("--Job_Tag",
                        type=int,
                        default=0.33,
                        help="Privacy-security tag of each jobs")
    # 任务隐私安全标签privacy factor
    '''
    代表中间数据被授予等级L1的概率(即高隐私需求),越高代表工作流中有更多隐私任务,L2和L3概率为(1-privacy_factor)/2
    '''

    '''
    # privacy factor
    parser.add_argument("--Privacy_Factor",
                        type=int,
                        default=0.5,
                        help="Privacy factor of each edges")
    '''
    
    parser.add_argument("--Job_Privacy_Factor",
                        type=int,
                        default=0.5,
                        help="Privacy factor of each jobs")
    

    '''
    环境参数
    '''

    '''
    # 安全方法数量 
    parser.add_argument("--Security_Method_Num",
                        type=int,
                        default=8,
                        help="Security Method Num")
    
    # 安全方法成本
    parser.add_argument("--Security_Method_Cost",
                        type=list,
                        default=[0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1],
                        help="Security Method Cost")
    '''
    
    # 安全方法 
    '''
    用户认证(user authentication): HMAC-MD5, HMAC-SHA1, CBC-MAC-AES
    保密性(confidentiality)加密算法: SEAL, RC4, Blowfish, Kunfu/Khafre, RC5, Rijndael, DES, IDEA
    完整性(integrity)哈希函数: MD4, MD5, RIPEMD, RIPEMD-128, SHA-1, RIPEMD-160, Tiger
    速度单位: KB/ms
    '''
    # 用户认证(user authentication)
    parser.add_argument("--User_Authentication_Num",
                        type=int,
                        default=3,
                        help="User Authentication Num")
    parser.add_argument("--User_Authentication_Security_Level",
                        type=list,
                        default=[0.55, 0.91, 1.00],
                        help="Security Method Security Level")
    parser.add_argument("--User_Authentication_Overhead",
                        type=list,
                        default=[0.9, 1.48, 1.63],
                        help="Security Method Overhead(s)")
    parser.add_argument("--User_Authentication_Cost",
                        type=list,
                        default=[0.5, 0.5, 0.5],
                        help="User_Authentication_Cost")
    # 保密性(confidentiality)加密算法
    parser.add_argument("-Cryptographic_Method_Num",
                        type=int,
                        default=8,
                        help="Cryptographic Method Num")
    parser.add_argument("--Cryptographic_Security_Level",
                        type=list,
                        default=[0.08, 0.14, 0.36, 0.40, 0.46, 0.64, 0.90, 1.00],
                        help="Cryptographic Method Security Level")
    parser.add_argument("--Cryptographic_Method_Speed",
                        type=list,
                        default=[168.75, 96.43, 37.5, 33.75, 29.35, 21.09, 15, 13.5],
                        help="Cryptographic Method Speed(KB/ms)")
    parser.add_argument("--Cryptographic_Method_Cost",
                        type=list,
                        default=[0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1],
                        help="Cryptographic Method Cost")
    # 完整性(integrity)哈希函数
    parser.add_argument("--Hash_Function_Num",
                        type=int,
                        default=7,
                        help="Hash Function Num")
    parser.add_argument("--Hash_Function_Security_Level",
                        type=list,
                        default=[0.18, 0.26, 0.36, 0.45, 0.63, 0.77, 1.00],
                        help="Hash Function Security Level")
    parser.add_argument("--Hash_Function_Speed",
                        type=list,
                        default=[23.90, 17.09, 12.00, 9.73, 6.88, 5.69, 4.36],
                        help="Hash Function Speed(KB/ms)")
    parser.add_argument("--Hash_Function_Cost",
                        type=list,
                        default=[0.5, 0.5, 0.5, 0.5, 1, 1, 1],
                        help="Hash Function Cost")
    '''
    # 安全方法类型(对应保密性1、完整性2、可用性3)
    parser.add_argument("--Security_Method_Type",
                        type=list,
                        default=[1, 1, 1, 2, 2, 3, 3, 3],
                        help="Security Method Type")
    # 安全方法安全级别 
    parser.add_argument("--Security_Method_Level",
                        type=list,
                        default=[1, 2, 3, 1, 2, 1, 2, 3],
                        help="Security Method Level")
    '''

    return parser.parse_args()



# 获取参数
def get_args():
    args = parameter_parser()
    return args