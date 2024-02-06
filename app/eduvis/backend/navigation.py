import numpy as np
import pandas as pd

from app.eduvis.constants import LANGUAGE
from app.eduvis.constants import RANDOM_NUMBER_STUDENTS
from app.eduvis.backend.connection_db import Connection_DB
from visualizations import V011

class Navigation:
    _user_id = None
    _dashboard_id = None
    _dashboard_type = None
    _conn = Connection_DB()
    _students = pd.DataFrame()
    _preprocessed_chart = True
    _view11 = V011.V011(type_result = "flask",language = LANGUAGE)

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

            self._view11.generate_dataset(number_students = self.number_students, rand_names = self._students)

    def title(self):
        res = None
        # Padrão de navegação dos estudantes no AVA # 11.1 # T23
        res = self._conn.select("topics",(23,))
        return res[0][0]
    
    def topic(self):
        return "T23"
    
    def charts(self,focus_chart): # focus_chart ["id","layout"]
        lst_charts = []
        # Padrão de navegação dos estudantes no AVA # 11.1 # T23
        lst_charts = self._conn.select("topics_charts",(23,))

        print(lst_charts)
        charts = []
        for i in range(0, len(lst_charts)):
            curr = lst_charts[i][0].split("@")            
            id = int(curr[1])
            # print(id)
            if self._preprocessed_chart:
                charts.append(self._view11.get_preprocessed_chart(id)[focus_chart])
            else:
                charts.append(self._view11.get_chart(id)[focus_chart])

        # charts = [self._view11.graph_01()[focus_chart], #1
        #           self._view11.graph_02()[focus_chart], #2
        #           self._view11.graph_03()[focus_chart], #3
        #           self._view11.graph_04()[focus_chart], #4
        #         #   self._view11.graph_05()[focus_chart], #5
        #          ]
        
        return charts

    def charts_active(self):
        topic_id = 23 # Padrão de navegação dos estudantes no AVA # 11.1 # T23

        charts_value = []
        res_db = self._conn.select("user_dashboard_charts_active_by_topic",(self._user_id, self._dashboard_id, self._dashboard_type, topic_id))
        for i in range(0,len(res_db)):
            charts_value.append(res_db[i][6])

        return charts_value