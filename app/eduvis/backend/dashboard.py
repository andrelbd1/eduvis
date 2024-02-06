import numpy as np
import pandas as pd
import json

from app.eduvis.constants import LANGUAGE
from app.eduvis.constants import RANDOM_NUMBER_STUDENTS
from app.eduvis.constants import LST_DEFAULT_TOPIC_CHART_ID
from app.eduvis.backend.connection_db import Connection_DB
from visualizations import V001, V002, V003, V004, V005, V006, V007, V008, V009, V010, V011

class Dashboard:
    _user_id = None
    _dashboard_id = None
    _dashboard_type = None
    _conn = Connection_DB()
    _language = LANGUAGE
    _students = pd.DataFrame()
    _preprocessed_chart = True
    _view1 = None
    _view2 = None
    _view3 = None
    _view4 = None
    _view5 = None
    _view6 = None
    _view7 = None
    _view8 = None
    _view9 = None
    _view10 = None
    _view11 = None
    lst_default_topic_chart_id = [15,27,30,40,42,55,64,70,76,88,117,126,154]

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

    def set_dashboard(self,data):
        # print("-----------------------------")
        print(data)
        # print(data["chart"])
        # print(data["value"])
        # print("-----------------------------")
        raw = data["chart"].split("@")
        topic = int(raw[0].replace("T",""))
        chart_value = raw[1]+"@"+raw[2]
        value_active = int(data["value"])        
        res_db = self._conn.select("chart",(chart_value,))
        chart_id = res_db[0][0]
        
        print("topic_id: "+str(topic))
        print("chart_id: "+str(chart_id))

        res_db = self._conn.select("user_dashboard_charts",(self._user_id, self._dashboard_id, self._dashboard_type, topic, chart_id))
        print(res_db)
        if len(res_db) == 0 and value_active == 1: # "insert"
            res_db = self._conn.select("topic_chart_id",(topic, chart_id))
            topic_chart_id = res_db[0][0]
            print("topic_chart_id: "+str(topic_chart_id))
            res_db = self._conn.select("max_order_user_dashboard_charts",(self._user_id, self._dashboard_id, self._dashboard_type))
            curr_max_order = res_db[0][0]
            self._conn.insert("tb_dashboard_topic_chart",(self._dashboard_id, topic_chart_id, curr_max_order+1, "", "", value_active))
            
        elif len(res_db) != 0: # "update"
            if value_active != res_db[0][8]:
                dashboard_topic_chart_id = res_db[0][0]
                self._conn.update("dashboard_charts_active",(value_active,dashboard_topic_chart_id))
                if value_active:
                    res_db = self._conn.select("max_order_user_dashboard_charts",(self._user_id, self._dashboard_id, self._dashboard_type))
                    curr_max_order = res_db[0][0]
                    self._conn.update("dashboard_charts_order",(curr_max_order+1,dashboard_topic_chart_id))
                # print(res_db[0][8])
        # print("-----------------------------")

        # "user_dashboard_charts"

    def set_order(self,data):
        # print("-----------------------------")
        print(data)
        # print(data["chart"])
        # print(data["value"])
        # print("-----------------------------")
        raw = data["chart"].split("@")
        topic = int(raw[0].replace("T",""))
        chart_value = raw[1]+"@"+raw[2]
        value_action = data["value"]
        res_db = self._conn.select("chart",(chart_value,))
        chart_id = res_db[0][0]
        
        print("topic_id: "+str(topic))
        print("chart_id: "+str(chart_id))

        res_db = self._conn.select("user_dashboard_charts_active_by_topic_chart",(self._user_id, self._dashboard_id, self._dashboard_type, topic, chart_id))
        curr_id = res_db[0][0]
        curr_order = res_db[0][4]
        
        print("curr_id: "+str(curr_id))
        print("curr_order: "+str(curr_order))

        if value_action == 'up':            
            res_db = self._conn.select("prev_user_dashboard_charts_active_by_topic_chart",(self._user_id, self._dashboard_id, self._dashboard_type, curr_order))
            prev_id = res_db[0][0]
            prev_order = res_db[0][4]
            print("prev_id: "+str(prev_id))
            print("prev_order: "+str(prev_order))
            self._conn.update("dashboard_charts_order",(int(prev_order),curr_id))
            self._conn.update("dashboard_charts_order",(int(curr_order),prev_id))
            
        elif value_action == 'down':
            res_db = self._conn.select("next_user_dashboard_charts_active_by_topic_chart",(self._user_id, self._dashboard_id, self._dashboard_type, curr_order))
            next_id = res_db[0][0]
            next_order = res_db[0][4]
            print("next_id: "+str(next_id))
            print("next_order: "+str(next_order))
            self._conn.update("dashboard_charts_order",(int(next_order),curr_id))
            self._conn.update("dashboard_charts_order",(int(curr_order),next_id))

        elif value_action == 'top':
            res_db = self._conn.select("first_user_dashboard_charts_active_by_topic_chart",(self._user_id, self._dashboard_id, self._dashboard_type, self._dashboard_id)) # Pega o chart ativo de menor order
            prev_id = res_db[0][0]
            prev_order = res_db[0][4]
            print("prev_id: "+str(prev_id))
            print("prev_order: "+str(prev_order))
            self._conn.update("dashboard_charts_order",(int(prev_order)-1,curr_id))
            # self._conn.update("dashboard_charts_order",(int(curr_order),prev_id))
        
        elif value_action == 'bottom':
            res_db = self._conn.select("last_user_dashboard_charts_active_by_topic_chart",(self._user_id, self._dashboard_id, self._dashboard_type, self._dashboard_id)) # Pega o chart ativo de maior order
            next_id = res_db[0][0]
            next_order = res_db[0][4]
            print("next_id: "+str(next_id))
            print("next_order: "+str(next_order))
            self._conn.update("dashboard_charts_order",(int(next_order)+1,curr_id))
            # self._conn.update("dashboard_charts_order",(int(curr_order),next_id))

    def load_views(self,view):
        if view == "V001" and self._view1 == None:
            self._view1 = V001.V001(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view1.generate_dataset(number_students = self.number_students, number_assigns = 10, rand_names = self._students)
        elif view == "V002" and self._view2 == None:
            self._view2 = V002.V002(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view2.generate_dataset(number_students = self.number_students, rand_names = self._students)
        elif view == "V003" and self._view3 == None:
            self._view3 = V003.V003(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view3.generate_dataset(number_students = self.number_students, rand_names = self._students)
        elif view == "V004" and self._view4 == None:
            self._view4 = V004.V004(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view4.generate_dataset(number_students = self.number_students, rand_names = self._students)
        elif view == "V005" and self._view5 == None:
            self._view5 = V005.V005(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view5.generate_dataset(number_students = self.number_students, rand_names = self._students)
        elif view == "V006" and self._view6 == None:
            self._view6 = V006.V006(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view6.generate_dataset(number_students = self.number_students, rand_names = self._students)
        elif view == "V007" and self._view7 == None:
            self._view7 = V007.V007(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view7.generate_dataset(number_students = self.number_students, rand_names = self._students)
        elif view == "V008" and self._view8 == None:
            self._view8 = V008.V008(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view8.generate_dataset(number_students = self.number_students, number_weeks=7, rand_names = self._students)
        elif view == "V009" and self._view9 == None:
            self._view9 = V009.V009(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view9.generate_dataset(number_actions = 100, video_size = 30, number_students = self.number_students, rand_names = self._students)
        elif view == "V010" and self._view10 == None:
            self._view10 = V010.V010(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view10.generate_dataset(number_students = self.number_students, number_video=10, rand_names = self._students)
        elif view == "V011" and self._view11 == None:
            self._view11 = V011.V011(type_result = "flask",language = self._language)
            if not self._preprocessed_chart:
                self._view11.generate_dataset(number_students = self.number_students, rand_names = self._students)

    def has_active_without_default_charts(self):
        lst_dash_charts = self._conn.select("user_dashboard_charts_active",(self._user_id, self._dashboard_id, self._dashboard_type))

        for i in range(0, len(lst_dash_charts)):
                if lst_dash_charts[i][7] in LST_DEFAULT_TOPIC_CHART_ID:
                    continue
                else:
                    return True

        return False

    def has_inactive_default_charts(self):
        lst_dash_charts = self._conn.select("user_dashboard_charts_inactive",(self._user_id, self._dashboard_id, self._dashboard_type))

        for i in range(0, len(lst_dash_charts)):
                if lst_dash_charts[i][7] in LST_DEFAULT_TOPIC_CHART_ID:
                    return True

        return False

    def title(self,default_charts_inactive=False,without_default_charts=False):
        lst_title = []
        if default_charts_inactive:
            lst_dash_charts = self._conn.select("user_dashboard_charts_inactive",(self._user_id, self._dashboard_id, self._dashboard_type))

            for i in range(0, len(lst_dash_charts)):
                if lst_dash_charts[i][7] in LST_DEFAULT_TOPIC_CHART_ID:
                    lst_title.append(lst_dash_charts[i][4])

        else:
            lst_dash_charts = self._conn.select("user_dashboard_charts_active",(self._user_id, self._dashboard_id, self._dashboard_type))

            for i in range(0, len(lst_dash_charts)):
                if without_default_charts:
                    if lst_dash_charts[i][7] in LST_DEFAULT_TOPIC_CHART_ID:
                        continue
                lst_title.append(lst_dash_charts[i][4])

        print(lst_title)
        return lst_title

    def topic(self,default_charts_inactive=False,without_default_charts=False):
        lst_topic = []
        if default_charts_inactive:
            lst_dash_charts = self._conn.select("user_dashboard_charts_inactive",(self._user_id, self._dashboard_id, self._dashboard_type))

            for i in range(0, len(lst_dash_charts)):
                if lst_dash_charts[i][7] in LST_DEFAULT_TOPIC_CHART_ID:
                    lst_topic.append(lst_dash_charts[i][5])

        else:
            lst_dash_charts = self._conn.select("user_dashboard_charts_active",(self._user_id, self._dashboard_id, self._dashboard_type))

            for i in range(0, len(lst_dash_charts)):
                if without_default_charts:
                    if lst_dash_charts[i][7] in LST_DEFAULT_TOPIC_CHART_ID:
                        continue
                lst_topic.append(lst_dash_charts[i][5])

        print(lst_topic)
        return lst_topic

    def amount_by_view(self):
        lst_dash_charts = self._conn.select("user_dashboard_charts_active",(self._user_id, self._dashboard_id, self._dashboard_type))
        
        lst_topic = [0]*11
        for i in range(0, len(lst_dash_charts)):
            raw = lst_dash_charts[i][6]
            view = int(raw.replace("V","").split("@")[0])
            lst_topic[view-1] += 1 
        
        # lst_topic = [x if x!=0 else "" for x in lst_topic]

        return lst_topic

    def charts(self,focus_chart, default_charts_inactive=False, without_default_charts=False): # focus_chart ["id","layout"]
        lst_charts = []
        if default_charts_inactive:
            lst_dash_charts = self._conn.select("user_dashboard_charts_inactive",(self._user_id, self._dashboard_id, self._dashboard_type))

            for i in range(0, len(lst_dash_charts)):
                if lst_dash_charts[i][7] in LST_DEFAULT_TOPIC_CHART_ID:
                    lst_charts.append(lst_dash_charts[i][6])        
        else:
            lst_dash_charts = self._conn.select("user_dashboard_charts_active",(self._user_id, self._dashboard_id, self._dashboard_type))
        
            for i in range(0, len(lst_dash_charts)):
                if without_default_charts:
                    if lst_dash_charts[i][7] in LST_DEFAULT_TOPIC_CHART_ID:
                        continue
                lst_charts.append(lst_dash_charts[i][6])

        print(lst_charts)
        # print(len(lst_charts))
        
        charts = []
        for i in range(0, len(lst_charts)):
            curr = lst_charts[i].split("@")
            print(curr[0])
            id = int(curr[1])            
            self.load_views(curr[0])
            if curr[0] == "V001":
                if self._preprocessed_chart:
                    charts.append(self._view1.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view1.get_chart(id)[focus_chart])
            elif curr[0] == "V002":
                if self._preprocessed_chart:
                    charts.append(self._view2.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view2.get_chart(id)[focus_chart])
            elif curr[0] == "V003":
                if self._preprocessed_chart:
                    charts.append(self._view3.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view3.get_chart(id)[focus_chart])
            elif curr[0] == "V004":
                if self._preprocessed_chart:
                    charts.append(self._view4.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view4.get_chart(id)[focus_chart])
            elif curr[0] == "V005":
                if self._preprocessed_chart:
                    charts.append(self._view5.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view5.get_chart(id)[focus_chart])
            elif curr[0] == "V006":
                if self._preprocessed_chart:
                    charts.append(self._view6.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view6.get_chart(id)[focus_chart])
            elif curr[0] == "V007":
                if self._preprocessed_chart:
                    charts.append(self._view7.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view7.get_chart(id)[focus_chart])
            elif curr[0] == "V008":
                if self._preprocessed_chart:
                    charts.append(self._view8.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view8.get_chart(id)[focus_chart])
            elif curr[0] == "V009":
                if self._preprocessed_chart:
                    charts.append(self._view9.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view9.get_chart(id)[focus_chart])
            elif curr[0] == "V010":
                if self._preprocessed_chart:
                    charts.append(self._view10.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view10.get_chart(id)[focus_chart])
            elif curr[0] == "V011":
                if self._preprocessed_chart:
                    charts.append(self._view11.get_preprocessed_chart(id)[focus_chart])
                else:
                    charts.append(self._view11.get_chart(id)[focus_chart])
        
        # Estudantes que fizeram e não fizeram as tarefas # 1.1
        
        # charts = [self._view1.graph_01()[focus_chart],                                     #01
        #           self._view1.graph_02()[focus_chart],self._view1.graph_06()[focus_chart], #02
        #           self._view1.graph_04()[focus_chart],self._view1.graph_08()[focus_chart], #03
        #           self._view1.graph_10()[focus_chart],self._view1.graph_12()[focus_chart], #04
        #           self._view1.graph_26()[focus_chart],self._view1.graph_27()[focus_chart], #05
        #           self._view1.graph_29()[focus_chart],                                     #06
        #           self._view1.graph_31()[focus_chart],self._view1.graph_32()[focus_chart], #07
        #           self._view1.graph_34()[focus_chart],                                     #08
        #           self._view1.graph_35()[focus_chart],                                     #09
        #           self._view1.graph_38()[focus_chart],                                     #10
        #           self._view1.graph_44()[focus_chart],                                     #11
        #           self._view1.graph_47()[focus_chart]                                      #12
        #         ]

        # Tarefas feitas e não feitas pelos estudantes # 1.2
        # charts = [self._view1.graph_14(),self._view1.graph_18(), #1
        #           self._view1.graph_16(),self._view1.graph_20(), #2
        #           self._view1.graph_22(),self._view1.graph_24(), #3
        #           self._view1.graph_30(),                        #4
        #           self._view1.graph_36(),                        #5
        #           self._view1.graph_37(),                        #6
        #           self._view1.graph_41(),                        #7
        #           self._view1.graph_50(),                        #8
        #           self._view1.graph_53(),                        #9
        #         ]
        
        # Acesso dos estudantes aos materiais (ex: videos, ebooks, etc) # 2.1
        # charts = [self._view2.graph_01(), #1
        #           self._view2.graph_02(), #2
        #           self._view2.graph_03(), #3
        #           self._view2.graph_05(), #4
        #           self._view2.graph_07(), #5
        #           self._view2.graph_08(), #6
        #           self._view2.graph_09(), #7
        #           self._view2.graph_10(), #8
        #           self._view2.graph_11(), #9
        #           self._view2.graph_12(), #10
        #         ]

        # Materiais mais acessados pelos estudantes (ex: videos, ebooks, etc) # 2.2

        # Número de acessos, postagens e curtidas dos estudantes # 3.1
        # charts = [self._view3.graph_01(), #1
        #           self._view3.graph_02(), #2
        #           self._view3.graph_04(), #3
        #           self._view3.graph_06(), #4
        #           self._view3.graph_08(), #5
        #           self._view3.graph_09(), #6
        #           self._view3.graph_10(), #7
        #          ] 

        # Tempo de permanência dos estudantes nos vídeos # 4.1
        # charts = [self._view4.graph_01(), #1
        #           self._view4.graph_02(), #2
        #           self._view4.graph_03(), #3
        #           self._view4.graph_04(), #4
        #           self._view4.graph_05(), #5
        #           self._view4.graph_06(), #6
        #           self._view4.graph_07(), #7
        #           self._view4.graph_08(), #8
        #           self._view4.graph_09(), #9
        #           self._view4.graph_11(), #10
        #          ]

        # Correlação entre as notas e os dados de acesso no AVA # 5.1
        # charts = [self._view5.graph_01(), #1
        #           self._view5.graph_02(), #2
        #           self._view5.graph_09(), #3
        #           self._view5.graph_10(), #4
        #           self._view5.graph_17(), #5
        #           self._view5.graph_18(), #6
        #          ]

        # Correlação entre as notas e os dados de acesso nos AVAs materiais do AVA # 5.2
        # charts = [self._view5.graph_01(), #1
        #           self._view5.graph_03(), #2
        #           self._view5.graph_09(), #3
        #           self._view5.graph_11(), #4
        #           self._view5.graph_17(), #5
        #           self._view5.graph_19(), #6
        #          ]

        # Correlação entre as notas e a quantidade de tarefas feitas # 5.3
        # charts = [self._view5.graph_01(), #1
        #           self._view5.graph_04(), #2
        #           self._view5.graph_09(), #3
        #           self._view5.graph_12(), #4
        #           self._view5.graph_17(), #5
        #           self._view5.graph_20(), #6
        #          ]

        # Correlação entre as notas e os dados de acesso no fórum # 5.4
        # charts = [self._view5.graph_01(), #1
        #           self._view5.graph_05(), #2
        #           self._view5.graph_09(), #3
        #           self._view5.graph_13(), #4
        #           self._view5.graph_17(), #5
        #           self._view5.graph_21(), #6
        #          ]

        # Correlação entre as notas e a quantidade de postagens no fórum  # 5.5
        # charts = [self._view5.graph_01(), #1
        #           self._view5.graph_06(), #2
        #           self._view5.graph_09(), #3
        #           self._view5.graph_14(), #4
        #           self._view5.graph_17(), #5
        #           self._view5.graph_22(), #6
        #          ]

        # Correlação entre as notas e a quantidade de postagens de respostas no fórum  # 5.6
        # charts = [self._view5.graph_01(), #1
        #           self._view5.graph_07(), #2
        #           self._view5.graph_09(), #3
        #           self._view5.graph_15(), #4
        #           self._view5.graph_17(), #5
        #           self._view5.graph_23(), #6
        #          ]

        # Correlação entre as notas e a quantidade de tópicos adicionados no fórum # 5.7
        # charts = [self._view5.graph_01(), #1
        #           self._view5.graph_08(), #2
        #           self._view5.graph_09(), #3
        #           self._view5.graph_16(), #4
        #           self._view5.graph_17(), #5
        #           self._view5.graph_24(), #6
        #          ]

        # Correlação entre a idade dos alunos e os dados de acesso no Fórum # 6.1
        # charts = [self._view6.graph_01(), #1
        #           self._view6.graph_02(), #2
        #           self._view6.graph_06(), #3
        #           self._view6.graph_10(), #4
        #          ]

        # Correlação entre a idade dos alunos e a quantidade de postagens no Fórum # 6.2
        # charts = [self._view6.graph_01(), #1
        #           self._view6.graph_03(), #2
        #           self._view6.graph_07(), #3
        #           self._view6.graph_11(), #4
        #          ]

        # Correlação entre a idade dos alunos e a quantidade de postagens de respostas no Fórum # 6.3
        # charts = [self._view6.graph_01(), #1
        #           self._view6.graph_04(), #2
        #           self._view6.graph_08(), #3
        #           self._view6.graph_12(), #4
        #          ]

        # Correlação entre a idade dos alunos e a quantidade de tópicos adicionados no fórum # 6.4
        # charts = [self._view6.graph_01(), #1
        #           self._view6.graph_05(), #2
        #           self._view6.graph_09(), #3
        #           self._view6.graph_13(), #4
        #          ]

        # Predição das notas e dos estudantes desistentes # 7.1
        # charts = [self._view7.graph_01(), #1
        #           self._view7.graph_02(), #2
        #           self._view7.graph_03(), #3
        #           self._view7.graph_04(), #4
        #          ]

        # Quantidade de acesso dos estudantes por dia # 8.1
        # charts = [self._view8.graph_01(), #1
        #           self._view8.graph_02(), #2
        #           self._view8.graph_04(), #3
        #           self._view8.graph_05(), #4
        #           self._view8.graph_08(), #5
        #           self._view8.graph_10(), #6
        #           ]

        # Quantidade de acesso dos estudantes por semana # 8.2
        # charts = [self._view8.graph_03(), #1
        #           self._view8.graph_06(), #2
        #           self._view8.graph_07(), #3
        #           self._view8.graph_09(), #4
        #           self._view8.graph_11(), #5
        #           ]

        # Interação dos estudantes nos vídeos (play, pause, seek backward, seek forward) # 9.1
        # charts = [self._view9.graph_01(), #1
        #           self._view9.graph_02(), #2
        #           self._view9.graph_03(), #3
        #           self._view9.graph_05(), #4
        #          ]

        # Vídeos que os estudantes entenderam e não entenderam # 10.1
        # charts = [self._view10.graph_01(),                   #1
        #           self._view10.graph_02(),                   #2
        #           self._view10.graph_03(),self._view10.graph_05(), #3
        #           self._view10.graph_07(),self._view10.graph_09(), #4
        #           self._view10.graph_11(),self._view10.graph_13(), #5
        #           self._view10.graph_15(),self._view10.graph_16(), #6
        #           self._view10.graph_18(),                   #7
        #           self._view10.graph_19(),self._view10.graph_20(), #8
        #           self._view10.graph_22(),                   #9
        #           self._view10.graph_23(),                   #10
        #           self._view10.graph_24(),                   #11
        #           self._view10.graph_27(),                   #12
        #           self._view10.graph_30(),                   #13
        #          ]

        # Padrão de navegação dos estudantes no AVA # 11.1
        # charts = [self._view11.graph_01(), #1
        #           self._view11.graph_02(), #2
        #           self._view11.graph_03(), #3
        #           self._view11.graph_04(), #4
        #         #   self._view11.graph_05(), #5
        #          ]

        return charts