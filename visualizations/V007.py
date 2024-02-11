import dash
import dash_core_components as dcc
import dash_html_components as html
import random

import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

import os
import pandas as pd
import numpy as np

import pickle
import json

from plotly.utils import PlotlyJSONEncoder
from plotly.graph_objs import Figure, Layout, Bar, Table, Heatmap, Scatter, Box, Violin
from plotly.offline import init_notebook_mode, iplot

from sklearn import metrics
from sklearn.cluster import KMeans


init_notebook_mode(connected=True) # initiate notebook for offline plot
plotly.__version__

class V007:
    NUMBER_ACTIONS = 50
    COUNTDATA = pd.DataFrame()
    DATASET = pd.DataFrame()

    _language = "pt"
    _type_result="jupyter-notebook"
    _preprocessed_folder = os.path.join('Preprocessed')

    def __init__(self, language="pt", type_result = "jupyter-notebook"):
        self._language = language
        self._type_result = type_result

    def generate_dataset(self, number_students = 20, rand_names = []):
        self.NUMBER_STUDENTS = number_students
        if (self._language == "pt"):
            self.COUNTDATA = pd.DataFrame(0, index=range(0,1), columns=["Desistência", "0 - 60", "61 - 70", "71 - 80", "81 - 90", "91 - 100"])
            self.DATASET = pd.DataFrame(columns=["Estudantes","Predição de Cluster","Predição de Desistência","Predição de Nota",
        	                                        "Acesso ao AVA","Postagens no Fórum","Respostas no Fórum","Adição de Tópicos no Fórum","Acesso ao Fórum", "Cluster"])
        else:
            self.COUNTDATA = pd.DataFrame(0, index=range(0,1), columns=["Dropout", "0 - 60", "61 - 70", "71 - 80", "81 - 90", "91 - 100"])
            self.DATASET = pd.DataFrame(columns=["Students","Predicted Cluster","Predicted Dropout","Predicted Grade",
        	                                        "AVA Access","Forum Post","Forum Replies","Forum Add Thread","Forum Access", "Cluster"])

        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)

        for i in range(0,self.NUMBER_STUDENTS):
            self.DATASET.loc[i,self.DATASET.columns[0]] = rand_names[i]
            self.DATASET.loc[i,self.DATASET.columns[1]] = random.choice(self.COUNTDATA.columns.tolist())
            if self.DATASET.loc[i,self.DATASET.columns[1]] == self.COUNTDATA.columns.tolist()[0]:
                self.DATASET.loc[i,self.DATASET.columns[2]] = True
                self.DATASET.loc[i,self.DATASET.columns[3]] = np.random.randint(0,5)
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 0

                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(5,26)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,4)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0,4)
                self.DATASET.loc[i,self.DATASET.columns[7]] = np.random.randint(0,4)
                self.DATASET.loc[i,self.DATASET.columns[8]] =  self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + self.DATASET.loc[i,self.DATASET.columns[7]] + np.random.randint(0,7)

            elif self.DATASET.loc[i,self.DATASET.columns[1]] == self.COUNTDATA.columns.tolist()[1]:
                self.DATASET.loc[i,self.DATASET.columns[2]] = False
                self.DATASET.loc[i,self.DATASET.columns[3]] = int(random.triangular(0,30,60))
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 1
                self.COUNTDATA.loc[0,self.COUNTDATA.columns[1]] += 1

                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(20,41)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,8)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0,8)
                self.DATASET.loc[i,self.DATASET.columns[7]] = np.random.randint(0,4)
                self.DATASET.loc[i,self.DATASET.columns[8]] = self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + self.DATASET.loc[i,self.DATASET.columns[7]] + np.random.randint(0,22)

            elif self.DATASET.loc[i,self.DATASET.columns[1]] == self.COUNTDATA.columns.tolist()[2]:
                self.DATASET.loc[i,self.DATASET.columns[2]] = False
                self.DATASET.loc[i,self.DATASET.columns[3]] = int(random.triangular(61,65,70))
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 2
                self.COUNTDATA.loc[0,self.COUNTDATA.columns[2]] += 1

                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(35,57)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(1,12)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0,12)
                self.DATASET.loc[i,self.DATASET.columns[7]] = np.random.randint(0,8)
                self.DATASET.loc[i,self.DATASET.columns[8]] =  self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + self.DATASET.loc[i,self.DATASET.columns[7]] + np.random.randint(2,26)

            elif self.DATASET.loc[i,self.DATASET.columns[1]] == self.COUNTDATA.columns.tolist()[3]:
                self.DATASET.loc[i,self.DATASET.columns[2]] = False
                self.DATASET.loc[i,self.DATASET.columns[3]] = int(random.triangular(71,75,80))
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 3
                self.COUNTDATA.loc[0,self.COUNTDATA.columns[3]] += 1

                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(50,71)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(2,21)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(2,21)
                self.DATASET.loc[i,self.DATASET.columns[7]] = np.random.randint(0,7)
                self.DATASET.loc[i,self.DATASET.columns[8]] =  self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + self.DATASET.loc[i,self.DATASET.columns[7]] + np.random.randint(4,31)

            elif self.DATASET.loc[i,self.DATASET.columns[1]] == self.COUNTDATA.columns.tolist()[4]:
                self.DATASET.loc[i,self.DATASET.columns[2]] = False
                self.DATASET.loc[i,self.DATASET.columns[3]] = int(random.triangular(81,85,90))
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 4
                self.COUNTDATA.loc[0,self.COUNTDATA.columns[4]] += 1

                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(65,86)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(5,36)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(5,36)
                self.DATASET.loc[i,self.DATASET.columns[7]] = np.random.randint(1,11)
                self.DATASET.loc[i,self.DATASET.columns[8]] =  self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + self.DATASET.loc[i,self.DATASET.columns[7]] + np.random.randint(6,36)

            elif self.DATASET.loc[i,self.DATASET.columns[1]] == self.COUNTDATA.columns.tolist()[5]:
                self.DATASET.loc[i,self.DATASET.columns[2]] = False
                self.DATASET.loc[i,self.DATASET.columns[3]] = int(random.triangular(91,95,100))
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 5
                self.COUNTDATA.loc[0,self.COUNTDATA.columns[5]] += 1

                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(80,101)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(10,41)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(10,41)
                self.DATASET.loc[i,self.DATASET.columns[7]] = np.random.randint(3,14)
                self.DATASET.loc[i,self.DATASET.columns[8]] =  self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + self.DATASET.loc[i,self.DATASET.columns[7]] + np.random.randint(10,41)

    def graph_01(self):
        legend = {"title":"Previsão das notas relacionado com o número de acessos no AVA"}
        if (self._language == "en"):
            legend = {"title":"Predicted grades related with the number of VLE access"}
        df = self.DATASET

        trace = [Table(
            header=dict(
                values=list(df.columns[:len(df.columns)-1]),
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[df[i].tolist() for i in df.columns[:len(df.columns)-1]],
                fill = dict(color='#F5F8FF'),
                align = ['left','center']
            )
        )]

        data = trace
        layout = Layout( title = legend["title"] )
        
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(data, filename = 'pandas_table')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V007@1',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V007@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Scatter
    def graph_02(self):
        legend = {"title":"Previsão das notas relacionado com o número de acessos no AVA",
                    "xaxis":"Acesso ao AVA",
                    "yaxis":"Previsão das Notas",
                    'hovertext':'Nota Prevista'
                }
        if (self._language == "en"):
            legend = {"title":"Predicted grades related with the number of VLE access",
                        "xaxis":"AVA Access",
                        "yaxis":"Predicted Grades",
                        'hovertext':'Predicted Grade'
                    }
        
        df = self.DATASET.sort_values(by=[self.DATASET.columns[3]])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(100,100,100)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        color[Clusters[0]] = "rgb(100,100,100)"
        color[Clusters[1]] = "rgb(255,0,0)"
        color[Clusters[2]] = "rgb(127,0,127)"
        color[Clusters[3]] = "rgb(0,0,255)"
        color[Clusters[4]] = "rgb(0,127,127)"
        color[Clusters[5]] = "rgb(0,255,0)"

        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            # print(df[df.columns[0]][i])
            trace.append(
                Scatter(
                    x=[df[df.columns[4]][i]], #Access
                    y=[df[df.columns[3]][i]], #Grade
                    hovertext = '<b>'+df[df.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(df[df.columns[4]][i])+'<br>'+legend['hovertext']+": "+str(df[df.columns[3]][i])+'<br>Cluster: '+str(df[df.columns[len(df.columns)-1]][i]+1),
                    hoverinfo='text',
                    mode='markers',
                    name=df[df.columns[0]][i], #each student name
                    text = [str(df[df.columns[0]][i])],
                    marker=dict(
                        size=12,
                        symbol=df[df.columns[len(df.columns)-1]][i],
                        color = color[df[df.columns[len(df.columns)-1]][i]],
                        colorscale='Viridis',
                        line=dict(
                            width=2
                        )
                    )                    
                )
            )

        layout = Layout(
            title=legend['title'],
            hovermode = "closest",
            showlegend = True,
            xaxis = dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                fixedrange = False,
                range = [0, self.DATASET[self.DATASET.columns[4]].max()+10],
                rangemode = "normal",
                zeroline= False,
                showline = True,
            ),
            yaxis = dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                fixedrange = False,
                range = [0, self.DATASET[self.DATASET.columns[3]].max()+10],
                rangemode = "normal",
                showline = True,
            )
        )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V007@2',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V007@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Box
    def graph_03(self):
        legend = {"title":"Variação da previsão de notas dos estudantes por cluster",
                    "xaxis":"",
                    "yaxis":"Previsão das Notas",
                    "cluster":["Desistentes",'Notas entre 0 e 60','Notas entre 61 e 70', 'Notas entre 71 e 80', 'Notas entre 81 e 90', 'Notas entre 91 e 100'],
                    'hovertext':'Nota Prevista'
                }
        if (self._language == "en"):
            legend = {"title":"Student predicted grades variation by cluster",
                        "xaxis":"",
                        "yaxis":"Predicted Grades",
                        "cluster":["Dropout",'Grades between 0 and 60','Grades between 61 and 70', 'Grades between 71 and 80', 'Grades between 81 and 90', 'Grades between 91 and 100'],
                        'hovertext':'Predicted Grade'
                    }
        
        df = self.DATASET.sort_values(by=[self.DATASET.columns[3]])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(100,100,100)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_grades = df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #Grades
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_grades,
                    # y=df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(), #Access
                    name=legend["cluster"][i],
                    # text=df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['hovertext']+": "+str(lst_grades[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
                    boxpoints = 'all',
                    marker=dict(
                        color = color[i],
                        line=dict(
                            width=1
                        )
                    ),
                    boxmean=True
                )
            )

        layout = Layout(
            title=legend['title'],
            # hovermode = "closest",
            showlegend = True,
            xaxis = dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis = dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                fixedrange = False,
                range = [-1, self.DATASET[self.DATASET.columns[3]].max()+10],
                rangemode = "normal",
                # showline = True,
                zeroline = False,
            )
        )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Box')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V007@3',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V007@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Violin
    def graph_04(self):
        legend = {"title":"Variação da previsão de notas dos estudantes por cluster",
                    "xaxis":"",
                    "yaxis":"Previsão das Notas",
                    "cluster":["Desistentes",'Notas entre 0 e 60','Notas entre 61 e 70', 'Notas entre 71 e 80', 'Notas entre 81 e 90', 'Notas entre 91 e 100'],
                    'hovertext':'Nota Prevista'
                }
        if (self._language == "en"):
            legend = {"title":"Student predicted grades variation by cluster",
                        "xaxis":"",
                        "yaxis":"Predicted Grades",
                        "cluster":["Dropout",'Grades between 0 and 60','Grades between 61 and 70', 'Grades between 71 and 80', 'Grades between 81 and 90', 'Grades between 91 and 100'],
                        'hovertext':'Predicted Grade'
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self.DATASET.sort_values(by=[self.DATASET.columns[3]])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(100,100,100)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        color[Clusters[0]] = "rgb(100,100,100)"
        color[Clusters[1]] = "rgb(255,0,0)"
        color[Clusters[2]] = "rgb(127,0,127)"
        color[Clusters[3]] = "rgb(0,0,255)"
        color[Clusters[4]] = "rgb(0,127,127)"
        color[Clusters[5]] = "rgb(0,255,0)"
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_grades = df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #grades
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]],
                    "name":legend["cluster"][i],
                    # "text":df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['hovertext']+": "+str(lst_grades[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
                    "box":{
                        "visible":True
                        },
                    "points": 'all',
                    "meanline":{
                        "visible":True
                        },
                    "line":{
                        "color":color[i],
                    },
                    "marker": {
                        "line": {
                            "width": 1,
                        }
                    },
                }
            )

        layout = Layout(
            title=legend['title'],
            hovermode = "closest",
            showlegend = True,
            xaxis = dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis = dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                fixedrange = False,
                range = [-15, self.DATASET[self.DATASET.columns[3]].max()+10],
                rangemode = "normal",
                zeroline = False,
            )
        )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Violin')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V007@4',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V007@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def get_chart(self,id):
        if id == 1:
            return self.graph_01()
        elif id == 2:
            return self.graph_02()
        elif id == 3:
            return self.graph_03()
        elif id == 4:
            return self.graph_04()
        else:
            print("V007@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V007_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)

        if not os.path.exists(file_path):
            print('There is no preprocessed chart')
            return

        f = open(file_path,'rb')
        data = pickle.load(f)
        f.close()
        
        return data

    def save_chart(self,id):
        aux_type_result = self._type_result
        self._type_result = "flask"
        
        if not os.path.exists(self._preprocessed_folder):
            os.mkdir(self._preprocessed_folder)
        
        file_name = 'V007_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)
        f = open(file_path,'wb')
        pickle.dump(self.get_chart(id),f)
        f.close()

        self._type_result = aux_type_result

    def print_all_graphs(self,language="pt"):
        self._language = language
        self.graph_01() #Table
        self.graph_02() #Scatter
        self.graph_03() #Box
        self.graph_04() #Violin

# instance = V007()
# instance.generate_dataset(number_students = 20)