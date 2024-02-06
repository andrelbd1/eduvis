import numpy as np
import pandas as pd

from app.eduvis.constants import LANGUAGE
from app.eduvis.constants import RANDOM_NUMBER_STUDENTS
from app.eduvis.backend.connection_db import Connection_DB
from visualizations import V005

class Cluster:
    _user_id = None
    _dashboard_id = None
    _dashboard_type = None
    _conn = Connection_DB()
    _students = pd.DataFrame()
    _preprocessed_chart = True
    _view5 = V005.V005(type_result = "flask",language = LANGUAGE)

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

            self._view5.generate_dataset(number_students = self.number_students, rand_names = self._students)
        
    def title(self,focus_type):
        res = None
        if focus_type == "grades_access": # Correlação entre as notas e os dados de acesso no AVA # 5.1 # T7
            res = self._conn.select("topics",(7,))
        elif focus_type == "grades_access_materials": # Correlação entre as notas e os dados de acesso nos AVAs materiais do AVA # 5.2 # T8
            res = self._conn.select("topics",(8,))
        elif focus_type == "grades_assignments": # Correlação entre as notas e a quantidade de tarefas feitas # 5.3 # T9
            res = self._conn.select("topics",(9,))
        elif focus_type == "grades_access_forum": # Correlação entre as notas e os dados de acesso no fórum # 5.4 # T10
            res = self._conn.select("topics",(10,))
        elif focus_type == "grades_forum_post": # Correlação entre as notas e a quantidade de postagens no fórum  # 5.5 # T11
            res = self._conn.select("topics",(11,))
        elif focus_type == "grades_forum_reply": # Correlação entre as notas e a quantidade de postagens de respostas no fórum  # 5.6 # T12
            res = self._conn.select("topics",(12,))
        elif focus_type == "grades_forum_thread": # Correlação entre as notas e a quantidade de tópicos adicionados no fórum # 5.7 # T13
            res = self._conn.select("topics",(13,))

        return res[0][0]

    def topic(self,focus_type):
        if focus_type == "grades_access": # Correlação entre as notas e os dados de acesso no AVA # 5.1 # T7
            return "T7"
        elif focus_type == "grades_access_materials": # Correlação entre as notas e os dados de acesso nos AVAs materiais do AVA # 5.2 # T8
            return "T8"
        elif focus_type == "grades_assignments": # Correlação entre as notas e a quantidade de tarefas feitas # 5.3 # T9
            return "T9"
        elif focus_type == "grades_access_forum": # Correlação entre as notas e os dados de acesso no fórum # 5.4 # T10
            return "T10"
        elif focus_type == "grades_forum_post": # Correlação entre as notas e a quantidade de postagens no fórum  # 5.5 # T11
            return "T11"
        elif focus_type == "grades_forum_reply": # Correlação entre as notas e a quantidade de postagens de respostas no fórum  # 5.6 # T12
            return "T12"
        elif focus_type == "grades_forum_thread": # Correlação entre as notas e a quantidade de tópicos adicionados no fórum # 5.7 # T13
            return "T13"

    def charts(self,focus_type,focus_chart): # focus_chart ["id","layout"]
        lst_charts = []
        if focus_type == "grades_access": # Correlação entre as notas e os dados de acesso no AVA # 5.1 # T7
            lst_charts = self._conn.select("topics_charts",(7,))
        elif focus_type == "grades_access_materials": # Correlação entre as notas e os dados de acesso nos AVAs materiais do AVA # 5.2 # T8
            lst_charts = self._conn.select("topics_charts",(8,))
        elif focus_type == "grades_assignments": # Correlação entre as notas e a quantidade de tarefas feitas # 5.3 # T9
            lst_charts = self._conn.select("topics_charts",(9,))
        elif focus_type == "grades_access_forum": # Correlação entre as notas e os dados de acesso no fórum # 5.4 # T10
            lst_charts = self._conn.select("topics_charts",(10,))
        elif focus_type == "grades_forum_post": # Correlação entre as notas e a quantidade de postagens no fórum  # 5.5 # T11
            lst_charts = self._conn.select("topics_charts",(11,))
        elif focus_type == "grades_forum_reply": # Correlação entre as notas e a quantidade de postagens de respostas no fórum  # 5.6 # T12
            lst_charts = self._conn.select("topics_charts",(12,))
        elif focus_type == "grades_forum_thread": # Correlação entre as notas e a quantidade de tópicos adicionados no fórum # 5.7 # T13
            lst_charts = self._conn.select("topics_charts",(13,))
        
        print(lst_charts)
        charts = []
        for i in range(0, len(lst_charts)):
            curr = lst_charts[i][0].split("@")            
            id = int(curr[1])
            # print(id)
            if self._preprocessed_chart:
                charts.append(self._view5.get_preprocessed_chart(id)[focus_chart])
            else:
                charts.append(self._view5.get_chart(id)[focus_chart])

        # if focus_type == "grades_access": # Correlação entre as notas e os dados de acesso no AVA # 5.1
        #     charts = [self._view5.graph_01()[focus_chart], #1
        #               self._view5.graph_02()[focus_chart], #2
        #               self._view5.graph_09()[focus_chart], #3
        #               self._view5.graph_10()[focus_chart], #4
        #               self._view5.graph_17()[focus_chart], #5
        #               self._view5.graph_18()[focus_chart], #6
        #             ]

        # elif focus_type == "grades_access_materials": # Correlação entre as notas e os dados de acesso nos AVAs materiais do AVA # 5.2
        #     charts = [self._view5.graph_01()[focus_chart], #1
        #               self._view5.graph_03()[focus_chart], #2
        #               self._view5.graph_09()[focus_chart], #3
        #               self._view5.graph_11()[focus_chart], #4
        #               self._view5.graph_17()[focus_chart], #5
        #               self._view5.graph_19()[focus_chart], #6
        #             ]

        # elif focus_type == "grades_assignments": # Correlação entre as notas e a quantidade de tarefas feitas # 5.3
        #     charts = [self._view5.graph_01()[focus_chart], #1
        #               self._view5.graph_04()[focus_chart], #2
        #               self._view5.graph_09()[focus_chart], #3
        #               self._view5.graph_12()[focus_chart], #4
        #               self._view5.graph_17()[focus_chart], #5
        #               self._view5.graph_20()[focus_chart], #6
        #             ]

        # elif focus_type == "grades_access_forum": # Correlação entre as notas e os dados de acesso no fórum # 5.4
        #     charts = [self._view5.graph_01()[focus_chart], #1
        #               self._view5.graph_05()[focus_chart], #2
        #               self._view5.graph_09()[focus_chart], #3
        #               self._view5.graph_13()[focus_chart], #4
        #               self._view5.graph_17()[focus_chart], #5
        #               self._view5.graph_21()[focus_chart], #6
        #             ]

        # elif focus_type == "grades_forum_post": # Correlação entre as notas e a quantidade de postagens no fórum  # 5.5
        #     charts = [self._view5.graph_01()[focus_chart], #1
        #               self._view5.graph_06()[focus_chart], #2
        #               self._view5.graph_09()[focus_chart], #3
        #               self._view5.graph_14()[focus_chart], #4
        #               self._view5.graph_17()[focus_chart], #5
        #               self._view5.graph_22()[focus_chart], #6
        #             ]

        # elif focus_type == "grades_forum_reply": # Correlação entre as notas e a quantidade de postagens de respostas no fórum  # 5.6
        #     charts = [self._view5.graph_01()[focus_chart], #1
        #               self._view5.graph_07()[focus_chart], #2
        #               self._view5.graph_09()[focus_chart], #3
        #               self._view5.graph_15()[focus_chart], #4
        #               self._view5.graph_17()[focus_chart], #5
        #               self._view5.graph_23()[focus_chart], #6
        #             ]

        # elif focus_type == "grades_forum_thread": # Correlação entre as notas e a quantidade de tópicos adicionados no fórum # 5.7
        #     charts = [self._view5.graph_01()[focus_chart], #1
        #               self._view5.graph_08()[focus_chart], #2
        #               self._view5.graph_09()[focus_chart], #3
        #               self._view5.graph_16()[focus_chart], #4
        #               self._view5.graph_17()[focus_chart], #5
        #               self._view5.graph_24()[focus_chart], #6
        #             ]

        return charts

    def charts_active(self,focus_type):
        topic_id = None
        if focus_type == "grades_access": # Correlação entre as notas e os dados de acesso no AVA # 5.1 # T7
            topic_id = 7
        elif focus_type == "grades_access_materials": # Correlação entre as notas e os dados de acesso nos AVAs materiais do AVA # 5.2 # T8
            topic_id = 8
        elif focus_type == "grades_assignments": # Correlação entre as notas e a quantidade de tarefas feitas # 5.3 # T9
            topic_id = 9
        elif focus_type == "grades_access_forum": # Correlação entre as notas e os dados de acesso no fórum # 5.4 # T10
            topic_id = 10
        elif focus_type == "grades_forum_post": # Correlação entre as notas e a quantidade de postagens no fórum  # 5.5 # T11
            topic_id = 11
        elif focus_type == "grades_forum_reply": # Correlação entre as notas e a quantidade de postagens de respostas no fórum  # 5.6 # T12
            topic_id = 12
        elif focus_type == "grades_forum_thread": # Correlação entre as notas e a quantidade de tópicos adicionados no fórum # 5.7 # T13
            topic_id = 13

        charts_value = []
        res_db = self._conn.select("user_dashboard_charts_active_by_topic",(self._user_id, self._dashboard_id, self._dashboard_type, topic_id))
        for i in range(0,len(res_db)):
            charts_value.append(res_db[i][6])

        return charts_value