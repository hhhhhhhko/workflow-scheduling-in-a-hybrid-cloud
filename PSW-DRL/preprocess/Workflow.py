'''
用来选择工作流workflow
'''
import numpy as np
from preprocess.XMLProcess import XMLtoDAG
#from preprocess.Subtask import SubTask

'''
# 用到的工作流的集合
WFS = ['./datasets/Sipht_29.xml', './datasets/Montage_25.xml', './datasets/Inspiral_30.xml', './datasets/Epigenomics_24.xml',
        './datasets/CyberShake_30.xml']
# 工作流的任务数集合
N = [29, 25, 30, 24, 30]
TASK_TYPE = []
for wf, n in zip(WFS, N):
        # temps.append(XMLtoDAG(wf, n))
        # Jobs.append(XMLtoDAG(wf, n).jobs())
        # TYPES += XMLtoDAG(wf, n).types()[0]
        TASK_TYPE.append(XMLtoDAG(wf).types()[1])

class Workflow:
    def __init__(self, num):
        self.id = num + 1
        self.type = WFS[num]
        self.size = N[num]
        self.subTask = [SubTask((num + 1) * 1000 + i + 1, TASK_TYPE[num][i]) for i in range(self.size)]  # 子任务

        dag = XMLtoDAG(self.type, self.size)
        self.structure = dag.get_dag()  # 带权DAG
        self.precursor = dag.get_precursor()
'''

# 选择科学工作流
class Scientific_Workflow:
    def __init__(self, name, n_jobs):
        self.name = name
        self.n_jobs = n_jobs
    
    def get_workflow(self):
        CyberShake_30 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\CyberShake\CyberShake_30.xml') 
        CyberShake_50 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\CyberShake\CyberShake_50.xml') 
        CyberShake_100 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\CyberShake\CyberShake_100.xml') 
        CyberShake_1000 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\CyberShake\CyberShake_1000.xml') 
        
        Epigenomics_24 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\Epigenomics\Epigenomics_24.xml') 
        Epigenomics_47 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\Epigenomics\Epigenomics_47.xml') 
        Epigenomics_100 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\Epigenomics\Epigenomics_100.xml') 
        Epigenomics_997 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\Epigenomics\Epigenomics_997.xml') 

        Inspiral_30 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\LIGO\Inspiral_30.xml') 
        Inspiral_50 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\LIGO\Inspiral_50.xml')
        Inspiral_100 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\LIGO\Inspiral_100.xml')
        Inspiral_1000 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\LIGO\Inspiral_1000.xml')

        Montage_25 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\Montage\Montage_25.xml')
        Montage_50 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\Montage\Montage_50.xml')
        Montage_100 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\Montage\Montage_100.xml')
        Montage_1000 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\Montage\Montage_1000.xml')

        Sipht_29 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\SIPHT\Sipht_29.xml')
        Sipht_58 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\SIPHT\Sipht_58.xml')
        Sipht_97 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\SIPHT\Sipht_97.xml')
        Sipht_968 = XMLtoDAG('PSW-DRL\XML_Scientific_Workflow\SIPHT\Sipht_968.xml')

        if self.name == 'CyberShake':
            if self.n_jobs == 30:
                return CyberShake_30
            if self.n_jobs == 50:
                return CyberShake_50
            if self.n_jobs == 100:
                return CyberShake_100
            if self.n_jobs == 1000:
                return CyberShake_1000
        
        if self.name == 'Epigenomics':
            if self.n_jobs == 24:
                return Epigenomics_24
            if self.n_jobs == 47:
                return Epigenomics_47
            if self.n_jobs == 100:
                return Epigenomics_100
            if self.n_jobs == 997:
                return Epigenomics_997
        

        if self.name == 'Inspiral':
            if self.n_jobs == 30:
                return Inspiral_30
            if self.n_jobs == 50:
                return Inspiral_50
            if self.n_jobs == 100:
                return Inspiral_100
            if self.n_jobs == 1000:
                return Inspiral_1000
        
        if self.name == 'Montage':
            if self.n_jobs == 25:
                return Montage_25
            if self.n_jobs == 50:
                return Montage_50
            if self.n_jobs == 100:
                return Montage_100
            if self.n_jobs == 1000:
                return Montage_1000
        
        if self.name == 'Sipht':
            if self.n_jobs == 29:
                return Sipht_29
            if self.n_jobs == 58:
                return Sipht_58
            if self.n_jobs == 97:
                return Sipht_97
            if self.n_jobs == 968:
                return Sipht_968
        


# 选择随机工作流
# class Random_Workflow:


