import numpy as np
import pandas as pd

from app.eduvis.constants import LANGUAGE
from app.eduvis.constants import RANDOM_NUMBER_STUDENTS
from app.eduvis.backend.connection_db import Connection_DB
from visualizations import V004

class Video_Access:
    _user_id = None
    _dashboard_id = None
    _dashboard_type = None
    _conn = Connection_DB()
    _students = pd.DataFrame()
    _preprocessed_chart = True
    _view4 = V004.V004(type_result = "flask",language = LANGUAGE)

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

            self._view4.generate_dataset(number_students = self.number_students, rand_names = self._students)
    
    def title(self):
        res = None
        # Tempo de permanência dos estudantes nos vídeos # 4.1 # T6
        res = self._conn.select("topics",(6,))
        return res[0][0]

    def topic(self):
        return "T6"

    def charts(self,focus_chart): # focus_chart ["id","layout"]
        lst_charts = []
        lst_charts = self._conn.select("topics_charts",(6,))
         
        print(lst_charts)
        charts = []
        for i in range(0, len(lst_charts)):
            curr = lst_charts[i][0].split("@")            
            id = int(curr[1])
            # print(id)
            if self._preprocessed_chart:
                charts.append(self._view4.get_preprocessed_chart(id)[focus_chart])
            else:
                charts.append(self._view4.get_chart(id)[focus_chart])

        # Tempo de permanência dos estudantes nos vídeos # 4.1
        # charts = [self._view4.graph_01()[focus_chart], #1
        #           self._view4.graph_02()[focus_chart], #2
        #           self._view4.graph_03()[focus_chart], #3
        #           self._view4.graph_04()[focus_chart], #4
        #           self._view4.graph_05()[focus_chart], #5
        #           self._view4.graph_06()[focus_chart], #6
        #           self._view4.graph_07()[focus_chart], #7
        #           self._view4.graph_08()[focus_chart], #8
        #           self._view4.graph_09()[focus_chart], #9
        #           self._view4.graph_11()[focus_chart], #10
        #          ]
        
        return charts

    def charts_active(self):
        topic_id = 6 # Tempo de permanência dos estudantes nos vídeos # 4.1 # T6
        
        charts_value = []
        res_db = self._conn.select("user_dashboard_charts_active_by_topic",(self._user_id, self._dashboard_id, self._dashboard_type, topic_id))
        for i in range(0,len(res_db)):
            charts_value.append(res_db[i][6])

        return charts_value