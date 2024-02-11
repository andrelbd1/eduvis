import dash
import dash_core_components as dcc
import dash_html_components as html

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

class V006:
    NUMBER_STUDENTS = 50
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
            self.DATASET = pd.DataFrame(columns=["Estudantes","Idade","Acesso ao Fórum","Postagens no Fórum","Réplicas no Fórum","Adição de Tópicos no Fórum","Cluster"])
        else: 
            self.DATASET = pd.DataFrame(columns=["Students","Age","Forum Access","Forum Post","Forum Replies","Forum Add Thread","Cluster"])

        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)

        self.DATASET[self.DATASET.columns[1]] = np.random.triangular(18,30,70,self.NUMBER_STUDENTS)
        self.DATASET[self.DATASET.columns[1]] = self.DATASET.apply(self.convert_to_int, axis=1)

        for i in range(0,self.NUMBER_STUDENTS):
            self.DATASET.loc[i,self.DATASET.columns[0]] = rand_names[i]

            if (self.DATASET.loc[i,self.DATASET.columns[1]] <= 25):
                self.DATASET.loc[i,self.DATASET.columns[3]] = np.random.randint(0,4)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(0,4)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,4)

                self.DATASET.loc[i,self.DATASET.columns[2]] =  self.DATASET.loc[i,self.DATASET.columns[3]] + self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + np.random.randint(0,7)
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 1

            elif (self.DATASET.loc[i,self.DATASET.columns[1]] <= 30):
                self.DATASET.loc[i,self.DATASET.columns[3]] = np.random.randint(0,8)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(0,8)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,4)

                self.DATASET.loc[i,self.DATASET.columns[2]] = self.DATASET.loc[i,self.DATASET.columns[3]] + self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + np.random.randint(0,22)
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 2

            elif (self.DATASET.loc[i,self.DATASET.columns[1]] <= 40):
                self.DATASET.loc[i,self.DATASET.columns[3]] = np.random.randint(1,12)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(0,12)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,8)

                self.DATASET.loc[i,self.DATASET.columns[2]] =  self.DATASET.loc[i,self.DATASET.columns[3]] + self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + np.random.randint(2,26)
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 3

            elif (self.DATASET.loc[i,self.DATASET.columns[1]] <= 50):
                self.DATASET.loc[i,self.DATASET.columns[3]] = np.random.randint(2,21)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(2,21)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,7)

                self.DATASET.loc[i,self.DATASET.columns[2]] =  self.DATASET.loc[i,self.DATASET.columns[3]] + self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + np.random.randint(4,31)
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 4

            elif (self.DATASET.loc[i,self.DATASET.columns[1]] <= 60):
                self.DATASET.loc[i,self.DATASET.columns[3]] = np.random.randint(5,36)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(5,36)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(1,11)

                self.DATASET.loc[i,self.DATASET.columns[2]] =  self.DATASET.loc[i,self.DATASET.columns[3]] + self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + np.random.randint(6,36)
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 5

            else:
                self.DATASET.loc[i,self.DATASET.columns[3]] = np.random.randint(10,41)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(10,41)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(3,14)

                self.DATASET.loc[i,self.DATASET.columns[2]] =  self.DATASET.loc[i,self.DATASET.columns[3]] + self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + np.random.randint(10,41)
                self.DATASET.loc[i,self.DATASET.columns[len(self.DATASET.columns)-1]] = 6

    def convert_to_int(self,row):
        return int(row[self.DATASET.columns[1]])

    # Table presenting raw data
    def graph_01(self):
        legend = {"title":"Relação entre as notas dos estudantes e seus acessos no AVA"}
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and their access in the VLE"}
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
                id='V006@1',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Scatter
    def graph_02(self):
        legend = {"title":"Relação entre a idade dos estudantes e seus acessos no fórum",
                    "xaxis":"Acessos no fórum",
                    "yaxis":"Idade",
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' age and their access in the forum",
                        "xaxis":"Access in the forum",
                        "yaxis":"Age",
                    }        
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self.DATASET[self.DATASET.columns[2]][i]], #Acesso ao fórum
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Age
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name
                    hovertext = '<b>'+self.DATASET[self.DATASET.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(self.DATASET[self.DATASET.columns[2]][i])+'<br>'+legend['yaxis']+": "+str(self.DATASET[self.DATASET.columns[1]][i]),
                    hoverinfo='text',
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],
                    marker=dict(
                        size=12,
                        symbol=self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]][i]-1,
                        color = color[self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]][i]-1],
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
                range = [0, self.DATASET[self.DATASET.columns[2]].max()+10],
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
                range = [0, self.DATASET[self.DATASET.columns[1]].max()+10],
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
                id='V006@2',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_03(self):
        legend = {"title":"Relação entre a idade dos estudantes e suas postagens no fórum",
                    "xaxis":"Postagens no fórum",
                    "yaxis":"Idade",
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' age and their posts in the forum",
                        "xaxis":"Posts in the forum",
                        "yaxis":"Age",
                    }
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self.DATASET[self.DATASET.columns[3]][i]], #Posts
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Age
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name
                    hovertext = '<b>'+self.DATASET[self.DATASET.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(self.DATASET[self.DATASET.columns[3]][i])+'<br>'+legend['yaxis']+": "+str(self.DATASET[self.DATASET.columns[1]][i]),
                    hoverinfo='text',
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],                    
                    marker=dict(
                        size=12,                        
                        symbol=self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]][i]-1,
                        color = color[self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]][i]-1],
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
                range = [0, self.DATASET[self.DATASET.columns[3]].max()+10],
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
                range = [0, self.DATASET[self.DATASET.columns[1]].max()+10],
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
                id='V006@3',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_04(self):
        legend = {"title":"Relação entre a idade dos estudantes e suas réplicas no fórum",
                    "xaxis":"Réplicas no fórum",
                    "yaxis":"Idade",
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' age and their replies in the forum",
                        "xaxis":"Replies in the forum",
                        "yaxis":"Age",
                    }
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self.DATASET[self.DATASET.columns[4]][i]], #Replies
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Age
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name
                    hovertext = '<b>'+self.DATASET[self.DATASET.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(self.DATASET[self.DATASET.columns[4]][i])+'<br>'+legend['yaxis']+": "+str(self.DATASET[self.DATASET.columns[1]][i]),
                    hoverinfo='text',
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],                    
                    marker=dict(
                        size=12,                        
                        symbol=self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]][i]-1,
                        color = color[self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]][i]-1],
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
                range = [0, self.DATASET[self.DATASET.columns[1]].max()+10],
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
                id='V006@4',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_05(self):
        legend = {"title":"Relação entre a idade dos estudantes e seus tópicos adicionados no fórum",
                    "xaxis":"Tópicos no fórum",
                    "yaxis":"Idade",
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' age and their threads added in the forum",
                        "xaxis":"Threads in the forum",
                        "yaxis":"Age",
                    }
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self.DATASET[self.DATASET.columns[5]][i]], #Init threads in forum
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Age
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name
                    hovertext = '<b>'+self.DATASET[self.DATASET.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(self.DATASET[self.DATASET.columns[5]][i])+'<br>'+legend['yaxis']+": "+str(self.DATASET[self.DATASET.columns[1]][i]),
                    hoverinfo='text',
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],                    
                    marker=dict(
                        size=12,                        
                        symbol=self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]][i]-1,
                        color = color[self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]][i]-1],
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
                range = [0, self.DATASET[self.DATASET.columns[5]].max()+10],
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
                range = [0, self.DATASET[self.DATASET.columns[1]].max()+10],
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
                id='V006@5',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@5","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Box
    def graph_06(self):
        legend = {"title":"Variação de acessos no fórum por idade",
                    "xaxis":"",
                    "yaxis":"Acessos no fórum",
                    "age":{1:"até 25 anos", 2:"26 à 30 anos", 3:"31 à 40 anos", 4: "41 à 50 anos", 5: "51 à 60 anos", 6: "mais de 60 anos"},
                    'hovertext':'Idade'
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' access in the forum by age",
                        "xaxis":"",
                        "yaxis":"Access in the forum",
                        "age":{1:"until 25 years", 2:"26 to 30 years", 3:"31 to 40 years", 4: "41 to 50 years", 5: "51 to 60 years", 6: "over 60 years"},
                        'hovertext':'Age'
                    }
        df = self.DATASET.sort_values(by=self.DATASET.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_feat = df[df.columns[2]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_age = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_feat,
                    # y=df[df.columns[2]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    name=legend['age'][i+1],
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_feat[j])+'<br>'+legend['hovertext']+': '+str(lst_age[j]) for j in range(len(lst_names))],
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
                range = [-1, self.DATASET[self.DATASET.columns[2]].max()+10],
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
                id='V006@6',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@6","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_07(self):
        legend = {"title":"Variação de postagens no fórum por idade",
                    "xaxis":"",
                    "yaxis":"Postagens no fórum",
                    "age":{1:"até 25 anos", 2:"26 à 30 anos", 3:"31 à 40 anos", 4: "41 à 50 anos", 5: "51 à 60 anos", 6: "mais de 60 anos"},
                    'hovertext':'Idade'
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' posts in the forum by age",
                        "xaxis":"",
                        "yaxis":"Posts in the forum",
                        "age":{1:"until 25 years", 2:"26 to 30 years", 3:"31 to 40 years", 4: "41 to 50 years", 5: "51 to 60 years", 6: "over 60 years"},
                        'hovertext':'Age'
                    }
        df = self.DATASET.sort_values(by=self.DATASET.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_feat = df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_age = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_feat,
                    # y=df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    name=legend['age'][i+1],
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_feat[j])+'<br>'+legend['hovertext']+': '+str(lst_age[j]) for j in range(len(lst_names))],
                    # text=df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
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
                id='V006@7',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@7","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_08(self):
        legend = {"title":"Variação de réplicas no fórum por idade",
                    "xaxis":"",
                    "yaxis":"Réplicas no fórum",
                    "age":{1:"até 25 anos", 2:"26 à 30 anos", 3:"31 à 40 anos", 4: "41 à 50 anos", 5: "51 à 60 anos", 6: "mais de 60 anos"},
                    'hovertext':'Idade'
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' replies in the forum by age",
                        "xaxis":"",
                        "yaxis":"Replies in the forum",
                        "age":{1:"until 25 years", 2:"26 to 30 years", 3:"31 to 40 years", 4: "41 to 50 years", 5: "51 to 60 years", 6: "over 60 years"},
                        'hovertext':'Age'
                    }
        df = self.DATASET.sort_values(by=self.DATASET.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_feat = df[df.columns[4]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_age = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_feat,
                    # y=df[df.columns[4]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    name=legend['age'][i+1],
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_feat[j])+'<br>'+legend['hovertext']+': '+str(lst_age[j]) for j in range(len(lst_names))],
                    # text=df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
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
                range = [-1, self.DATASET[self.DATASET.columns[4]].max()+10],
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
                id='V006@8',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@8","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_09(self):
        legend = {"title":"Variação de tópicos adicionados no fórum por idade",
                    "xaxis":"",
                    "yaxis":"Tópicos no fórum",
                    "age":{1:"até 25 anos", 2:"26 à 30 anos", 3:"31 à 40 anos", 4: "41 à 50 anos", 5: "51 à 60 anos", 6: "mais de 60 anos"},
                    'hovertext':'Idade'
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' threads added in the forum by age",
                        "xaxis":"",
                        "yaxis":"Threads in the forum",
                        "age":{1:"until 25 years", 2:"26 to 30 years", 3:"31 to 40 years", 4: "41 to 50 years", 5: "51 to 60 years", 6: "over 60 years"},
                        'hovertext':'Age'
                    }
        df = self.DATASET.sort_values(by=self.DATASET.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_feat = df[df.columns[5]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_age = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_feat,
                    # y=df[df.columns[5]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    name=legend['age'][i+1],
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_feat[j])+'<br>'+legend['hovertext']+': '+str(lst_age[j]) for j in range(len(lst_names))],
                    # text=df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
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
                range = [-1, self.DATASET[self.DATASET.columns[5]].max()+10],
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
                id='V006@9',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@9","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Violin
    def graph_10(self):
        legend = {"title":"Variação de acessos no fórum por idade",
                    "xaxis":"",
                    "yaxis":"Acessos no fórum",
                    "age":{1:"até 25 anos", 2:"26 à 30 anos", 3:"31 à 40 anos", 4: "41 à 50 anos", 5: "51 à 60 anos", 6: "mais de 60 anos"},
                    'hovertext':'Idade'
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' access in the forum by age",
                        "xaxis":"",
                        "yaxis":"Access in the forum",
                        "age":{1:"until 25 years", 2:"26 to 30 years", 3:"31 to 40 years", 4: "41 to 50 years", 5: "51 to 60 years", 6: "over 60 years"},
                        'hovertext':'Age'
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self.DATASET.sort_values(by=self.DATASET.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_feat = df[df.columns[2]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_age = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":[legend['age'][i+1]]*len(df.loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":lst_feat,
                    "name":legend['age'][i+1],                    
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_feat[j])+'<br>'+legend['hovertext']+': '+str(lst_age[j]) for j in range(len(lst_names))],
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
                range = [-15, self.DATASET[self.DATASET.columns[2]].max()+10],                
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
                id='V006@10',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@10","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_11(self):
        legend = {"title":"Variação de postagens no fórum por idade",
                    "xaxis":"",
                    "yaxis":"Postagens no fórum",
                    "age":{1:"até 25 anos", 2:"26 à 30 anos", 3:"31 à 40 anos", 4: "41 à 50 anos", 5: "51 à 60 anos", 6: "mais de 60 anos"},
                    'hovertext':'Idade'
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' posts in the forum by age",
                        "xaxis":"",
                        "yaxis":"Posts in the forum",
                        "age":{1:"until 25 years", 2:"26 to 30 years", 3:"31 to 40 years", 4: "41 to 50 years", 5: "51 to 60 years", 6: "over 60 years"},
                        'hovertext':'Age'
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self.DATASET.sort_values(by=self.DATASET.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_feat = df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_age = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":[legend['age'][i+1]]*len(df.loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    # "y":df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]],
                    "y":lst_feat,
                    "name":legend['age'][i+1],
                    # "text":df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_feat[j])+'<br>'+legend['hovertext']+': '+str(lst_age[j]) for j in range(len(lst_names))],
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
                id='V006@11',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@11","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_12(self):
        legend = {"title":"Variação de réplicas no fórum por idade",
                    "xaxis":"",
                    "yaxis":"Réplicas no fórum",
                    "age":{1:"até 25 anos", 2:"26 à 30 anos", 3:"31 à 40 anos", 4: "41 à 50 anos", 5: "51 à 60 anos", 6: "mais de 60 anos"},
                    'hovertext':'Idade'
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' replies in the forum by age",
                        "xaxis":"",
                        "yaxis":"Replies in the forum",
                        "age":{1:"until 25 years", 2:"26 to 30 years", 3:"31 to 40 years", 4: "41 to 50 years", 5: "51 to 60 years", 6: "over 60 years"},
                        'hovertext':'Age'
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self.DATASET.sort_values(by=self.DATASET.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_feat = df[df.columns[4]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_age = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":[legend['age'][i+1]]*len(df.loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    # "y":df[df.columns[4]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]],
                    "y":lst_feat,
                    "name":legend['age'][i+1],
                    # "text":df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_feat[j])+'<br>'+legend['hovertext']+': '+str(lst_age[j]) for j in range(len(lst_names))],
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
                range = [-15, self.DATASET[self.DATASET.columns[4]].max()+10],                
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
                id='V006@12',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@12","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_13(self):
        legend = {"title":"Variação de tópicos adicionados no fórum por idade",
                    "xaxis":"",
                    "yaxis":"Tópicos no fórum",
                    "age":{1:"até 25 anos", 2:"26 à 30 anos", 3:"31 à 40 anos", 4: "41 à 50 anos", 5: "51 à 60 anos", 6: "mais de 60 anos"},
                    'hovertext':'Idade'
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' threads added in the forum by age",
                        "xaxis":"",
                        "yaxis":"Threads in the forum",
                        "age":{1:"until 25 years", 2:"26 to 30 years", 3:"31 to 40 years", 4: "41 to 50 years", 5: "51 to 60 years", 6: "over 60 years"},
                        'hovertext':'Age'
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self.DATASET.sort_values(by=self.DATASET.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(127,0,0)","rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,127,127)","rgb(0,255,0)"]
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_feat = df[df.columns[5]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            lst_age = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":[legend['age'][i+1]]*len(df.loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    # "y":df[df.columns[5]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]],
                    "y":lst_feat,
                    "name":legend['age'][i+1],
                    # "text":df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist(),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_feat[j])+'<br>'+legend['hovertext']+': '+str(lst_age[j]) for j in range(len(lst_names))],
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
                range = [-15, self.DATASET[self.DATASET.columns[5]].max()+10],                
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
                id='V006@13',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V006@13","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def get_chart(self,id):
        if id == 1:
            return self.graph_01()
        elif id == 2:
            return self.graph_02()
        elif id == 3:
            return self.graph_03()
        elif id == 4:
            return self.graph_04()
        elif id == 5:
            return self.graph_05()
        elif id == 6:
            return self.graph_06()
        elif id == 7:
            return self.graph_07()
        elif id == 8:
            return self.graph_08()
        elif id == 9:
            return self.graph_09()
        elif id == 10:
            return self.graph_10()
        elif id == 11:
            return self.graph_11()
        elif id == 12:
            return self.graph_12()
        elif id == 13:
            return self.graph_13()        
        else:
            print("V006@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V006_'+str(id)+'.pkl'
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
        
        file_name = 'V006_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)
        f = open(file_path,'wb')
        pickle.dump(self.get_chart(id),f)
        f.close()

        self._type_result = aux_type_result

    def print_all_graphs(self,language="pt"):
        self._language = language
        self.graph_01() #Table
        self.graph_02() #Scatter
        self.graph_03()
        self.graph_04()
        self.graph_05()
        self.graph_06() #Box
        self.graph_07()
        self.graph_08()
        self.graph_09()
        self.graph_10() #Violin
        self.graph_11()
        self.graph_12()
        self.graph_13()

# instance = V006()
# instance.generate_dataset(number_students = 60)
# instance.print_all_graphs("pt")
# instance.print_all_graphs("en")