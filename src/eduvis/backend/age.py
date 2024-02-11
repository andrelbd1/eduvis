import numpy as np
import pandas as pd

from app.eduvis.constants import LANGUAGE
from app.eduvis.constants import RANDOM_NUMBER_STUDENTS
from app.eduvis.backend.connection_db import Connection_DB
from visualizations import V006

class Age:
    _user_id = None
    _dashboard_id = None
    _dashboard_type = None
    _conn = Connection_DB()
    _students = pd.DataFrame()
    _preprocessed_chart = True
    _view6 = V006.V006(type_result = "flask",language = LANGUAGE)

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

            self._view6.generate_dataset(number_students = self.number_students, rand_names = self._students)
    
    def title(self,focus_type):
        res = None        
        if focus_type == "age_access_forum": # Correlação entre a idade dos alunos e os dados de acesso no Fórum # 6.1 # T14
            res = self._conn.select("topics",(14,))
        elif focus_type == "age_forum_post": # Correlação entre a idade dos alunos e a quantidade de postagens no Fórum # 6.2 # T15
            res = self._conn.select("topics",(15,))
        elif focus_type == "age_forum_reply": # Correlação entre a idade dos alunos e a quantidade de postagens de respostas no Fórum # 6.3 # T16
            res = self._conn.select("topics",(16,))
        elif focus_type == "age_forum_topic": # Correlação entre a idade dos alunos e a quantidade de tópicos adicionados no fórum # 6.4 # T17
            res = self._conn.select("topics",(17,))

        return res[0][0]

    def topic(self,focus_type):
        if focus_type == "age_access_forum": # Correlação entre a idade dos alunos e os dados de acesso no Fórum # 6.1 # T14
            return "T14"
        elif focus_type == "age_forum_post": # Correlação entre a idade dos alunos e a quantidade de postagens no Fórum # 6.2 # T15
            return "T15"
        elif focus_type == "age_forum_reply": # Correlação entre a idade dos alunos e a quantidade de postagens de respostas no Fórum # 6.3 # T16
            return "T16"
        elif focus_type == "age_forum_topic": # Correlação entre a idade dos alunos e a quantidade de tópicos adicionados no fórum # 6.4 # T17
            return "T17"

    def charts(self,focus_type,focus_chart): # focus_chart ["id","layout"]
        lst_charts = []
        if focus_type == "age_access_forum": # Correlação entre a idade dos alunos e os dados de acesso no Fórum # 6.1 # T14
            lst_charts = self._conn.select("topics_charts",(14,))
        elif focus_type == "age_forum_post": # Correlação entre a idade dos alunos e a quantidade de postagens no Fórum # 6.2 # T15
            lst_charts = self._conn.select("topics_charts",(15,))
        elif focus_type == "age_forum_reply": # Correlação entre a idade dos alunos e a quantidade de postagens de respostas no Fórum # 6.3 # T16
            lst_charts = self._conn.select("topics_charts",(16,))
        elif focus_type == "age_forum_topic": # Correlação entre a idade dos alunos e a quantidade de tópicos adicionados no fórum # 6.4 # T17
            lst_charts = self._conn.select("topics_charts",(17,))

        print(lst_charts)
        charts = []
        for i in range(0, len(lst_charts)):
            curr = lst_charts[i][0].split("@")            
            id = int(curr[1])
            # print(id)
            if self._preprocessed_chart:
                charts.append(self._view6.get_preprocessed_chart(id)[focus_chart])
            else:
                charts.append(self._view6.get_chart(id)[focus_chart])

        # if focus_type == "age_access_forum": # Correlação entre a idade dos alunos e os dados de acesso no Fórum # 6.1
        #     charts = [self._view6.graph_01()[focus_chart], #1
        #               self._view6.graph_02()[focus_chart], #2
        #               self._view6.graph_06()[focus_chart], #3
        #               self._view6.graph_10()[focus_chart], #4
        #              ]
        # elif focus_type == "age_forum_post": # Correlação entre a idade dos alunos e a quantidade de postagens no Fórum # 6.2
        #     charts = [self._view6.graph_01()[focus_chart], #1
        #               self._view6.graph_03()[focus_chart], #2
        #               self._view6.graph_07()[focus_chart], #3
        #               self._view6.graph_11()[focus_chart], #4
        #             ]
        # elif focus_type == "age_forum_reply": # Correlação entre a idade dos alunos e a quantidade de postagens de respostas no Fórum # 6.3
        #     charts = [self._view6.graph_01()[focus_chart], #1
        #               self._view6.graph_04()[focus_chart], #2
        #               self._view6.graph_08()[focus_chart], #3
        #               self._view6.graph_12()[focus_chart], #4
        #             ]
        # elif focus_type == "age_forum_topic": # Correlação entre a idade dos alunos e a quantidade de tópicos adicionados no fórum # 6.4
        #     charts = [self._view6.graph_01()[focus_chart], #1
        #               self._view6.graph_05()[focus_chart], #2
        #               self._view6.graph_09()[focus_chart], #3
        #               self._view6.graph_13()[focus_chart], #4
        #             ]

        return charts

    def charts_active(self,focus_type):
        topic_id = None
        if focus_type == "age_access_forum": # Correlação entre a idade dos alunos e os dados de acesso no Fórum # 6.1 # T14
            topic_id = 14
        elif focus_type == "age_forum_post": # Correlação entre a idade dos alunos e a quantidade de postagens no Fórum # 6.2 # T15
            topic_id = 15
        elif focus_type == "age_forum_reply": # Correlação entre a idade dos alunos e a quantidade de postagens de respostas no Fórum # 6.3 # T16
            topic_id = 16
        elif focus_type == "age_forum_topic": # Correlação entre a idade dos alunos e a quantidade de tópicos adicionados no fórum # 6.4 # T17
            topic_id = 17

        charts_value = []
        res_db = self._conn.select("user_dashboard_charts_active_by_topic",(self._user_id, self._dashboard_id, self._dashboard_type, topic_id))
        for i in range(0,len(res_db)):
            charts_value.append(res_db[i][6])

        return charts_value