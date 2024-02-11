import numpy as np
import pandas as pd

from app.eduvis.constants import LANGUAGE
from app.eduvis.constants import RANDOM_NUMBER_STUDENTS
from app.eduvis.backend.connection_db import Connection_DB
from visualizations import V001

class Assignment:
    _user_id = None
    _dashboard_id = None
    _dashboard_type = None
    _conn = Connection_DB()
    _students = pd.DataFrame()
    _preprocessed_chart = True
    _view1 = V001.V001(type_result = "flask",language = LANGUAGE)

    def __init__(self,conn,user_id,dashboard_id,dashboard_type,preprocessed_chart=True):
        self._conn = conn
        self._user_id = user_id
        self._dashboard_id = dashboard_id
        self._dashboard_type = dashboard_type        
        self._preprocessed_chart = preprocessed_chart
        
        if not self._preprocessed_chart:
            self.number_students = RANDOM_NUMBER_STUDENTS
            names = pd.read_csv("app/eduvis/names.csv")        
            self._students = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.number_students)]
            self._students.sort()

            self._view1.generate_dataset(number_students = self.number_students, number_assigns = 10, rand_names = self._students)
    
    def title(self,focus_type):
        res = None
        if focus_type == "student": # Estudantes que fizeram e não fizeram as tarefas # 1.1 # T1
            res = self._conn.select("topics",(1,))
        elif focus_type == "assignment": # Tarefas feitas e não feitas pelos estudantes # 1.2 # T2
            res = self._conn.select("topics",(2,))

        return res[0][0]

    def topic(self,focus_type):
        if focus_type == "student": # Estudantes que fizeram e não fizeram as tarefas # 1.1 # T1
            return "T1"
        elif focus_type == "assignment": # Tarefas feitas e não feitas pelos estudantes # 1.2 # T2
            return "T2"

    def charts(self,focus_type,focus_chart): # focus_chart ["id","layout"]
        lst_charts = []
        if focus_type == "student": # Estudantes que fizeram e não fizeram as tarefas # 1.1 # T1        
            lst_charts = self._conn.select("topics_charts",(1,))
        elif focus_type == "assignment": # Tarefas feitas e não feitas pelos estudantes # 1.2 T2
            lst_charts = self._conn.select("topics_charts",(2,))
        
        print(lst_charts)
        charts = []
        for i in range(0, len(lst_charts)):
            curr = lst_charts[i][0].split("@")            
            id = int(curr[1])
            # print(id)
            if self._preprocessed_chart:
                charts.append(self._view1.get_preprocessed_chart(id)[focus_chart])
            else:
                charts.append(self._view1.get_chart(id)[focus_chart])                

        # if focus_type == "student": # Estudantes que fizeram e não fizeram as tarefas # 1.1
        #     charts = [self._view1.graph_01()[focus_chart],                                     #01
        #               self._view1.graph_02()[focus_chart],self._view1.graph_06()[focus_chart], #02
        #               self._view1.graph_04()[focus_chart],self._view1.graph_08()[focus_chart], #03
        #               self._view1.graph_10()[focus_chart],self._view1.graph_12()[focus_chart], #04
        #               self._view1.graph_26()[focus_chart],self._view1.graph_27()[focus_chart], #05
        #               self._view1.graph_29()[focus_chart],                                     #06
        #               self._view1.graph_31()[focus_chart],self._view1.graph_32()[focus_chart], #07
        #               self._view1.graph_34()[focus_chart],                                     #08
        #               self._view1.graph_35()[focus_chart],                                     #09
        #               self._view1.graph_38()[focus_chart],                                     #10
        #               self._view1.graph_44()[focus_chart],                                     #11
        #               self._view1.graph_47()[focus_chart]                                      #12
        #             ]
        # elif focus_type == "assignment": # Tarefas feitas e não feitas pelos estudantes # 1.2
        #     charts = [self._view1.graph_14()[focus_chart],self._view1.graph_18()[focus_chart], #01
        #               self._view1.graph_16()[focus_chart],self._view1.graph_20()[focus_chart], #02
        #               self._view1.graph_22()[focus_chart],self._view1.graph_24()[focus_chart], #03
        #               self._view1.graph_30()[focus_chart],                                     #04
        #               self._view1.graph_36()[focus_chart],                                     #05
        #               self._view1.graph_37()[focus_chart],                                     #06
        #               self._view1.graph_41()[focus_chart],                                     #07
        #               self._view1.graph_50()[focus_chart],                                     #08
        #               self._view1.graph_53()[focus_chart],                                     #09
        #             ]
        
        return charts

    def charts_active(self,focus_type):
        topic_id = None
        if focus_type == "student": # Estudantes que fizeram e não fizeram as tarefas # 1.1 # T1
            topic_id = 1
        elif focus_type == "assignment": # Tarefas feitas e não feitas pelos estudantes # 1.2 # T2
            topic_id = 2

        charts_value = []
        res_db = self._conn.select("user_dashboard_charts_active_by_topic",(self._user_id, self._dashboard_id, self._dashboard_type, topic_id))
        for i in range(0,len(res_db)):
            charts_value.append(res_db[i][6])

        return charts_value