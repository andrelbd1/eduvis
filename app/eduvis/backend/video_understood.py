import numpy as np
import pandas as pd

from app.eduvis.constants import LANGUAGE
from app.eduvis.constants import RANDOM_NUMBER_STUDENTS
from app.eduvis.backend.connection_db import Connection_DB
from visualizations import V010

class Video_Understood:
    _user_id = None
    _dashboard_id = None
    _dashboard_type = None
    _conn = Connection_DB()
    _students = pd.DataFrame()
    _preprocessed_chart = True
    _view10 = V010.V010(type_result = "flask",language = LANGUAGE)

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

            self._view10.generate_dataset(number_students = self.number_students, number_video=10, rand_names = self._students)
    
    def title(self):
        res = None
        # Vídeos que os estudantes entenderam e não entenderam # 10.1 # T22
        res = self._conn.select("topics",(22,))
        return res[0][0]

    def topic(self):
        return "T22"

    def charts(self,focus_chart): # focus_chart ["id","layout"]
        lst_charts = []
        lst_charts = self._conn.select("topics_charts",(22,))
         
        print(lst_charts)
        charts = []
        for i in range(0, len(lst_charts)):
            curr = lst_charts[i][0].split("@")            
            id = int(curr[1])
            # print(id)
            if self._preprocessed_chart:
                charts.append(self._view10.get_preprocessed_chart(id)[focus_chart])
            else:
                charts.append(self._view10.get_chart(id)[focus_chart])
        
        # Vídeos que os estudantes entenderam e não entenderam # 10.1 # T22
        # charts = [self._view10.graph_01()[focus_chart],                                      #01
        #           self._view10.graph_02()[focus_chart],                                      #02
        #           self._view10.graph_03()[focus_chart],self._view10.graph_05()[focus_chart], #03
        #           self._view10.graph_07()[focus_chart],self._view10.graph_09()[focus_chart], #04
        #           self._view10.graph_11()[focus_chart],self._view10.graph_13()[focus_chart], #05
        #           self._view10.graph_15()[focus_chart],self._view10.graph_16()[focus_chart], #06
        #           self._view10.graph_18()[focus_chart],                                      #07
        #           self._view10.graph_19()[focus_chart],self._view10.graph_20()[focus_chart], #08
        #           self._view10.graph_22()[focus_chart],                                      #09
        #           self._view10.graph_23()[focus_chart],                                      #10
        #           self._view10.graph_24()[focus_chart],                                      #11
        #           self._view10.graph_27()[focus_chart],                                      #12
        #           self._view10.graph_30()[focus_chart],                                      #13
        #          ]

        return charts

    def charts_active(self):
        topic_id = 22 # Vídeos que os estudantes entenderam e não entenderam # 10.1 # T22
        
        charts_value = []
        res_db = self._conn.select("user_dashboard_charts_active_by_topic",(self._user_id, self._dashboard_id, self._dashboard_type, topic_id))
        for i in range(0,len(res_db)):
            charts_value.append(res_db[i][6])

        return charts_value