import dash
import dash_core_components as dcc
import dash_html_components as html

import os
import pandas as pd
import numpy as np

import pickle
import json

from plotly.utils import PlotlyJSONEncoder
from plotly.graph_objs import Figure, Layout, Table, Scatter, Box, Violin
from plotly.offline import init_notebook_mode, iplot

from sklearn import metrics
from sklearn.cluster import KMeans


init_notebook_mode(connected=True) # initiate notebook for offline plot

class V005:
    NUMBER_STUDENTS = 50
    DATASET = pd.DataFrame()

    _language = "pt"
    _type_result="jupyter-notebook"
    _df_sum = pd.DataFrame()
    _preprocessed_folder = os.path.join('Preprocessed')

    def __init__(self, language="pt", type_result = "jupyter-notebook"):
        self._language = language
        self._type_result = type_result

    def generate_dataset(self, number_students = 20, rand_names = []):
        self.NUMBER_STUDENTS = number_students
        
        if (self._language == "pt"):
            self.DATASET = pd.DataFrame(columns=["Estudantes","Notas","Acesso ao AVA",
                                                "Acesso ao Fórum","Postagens no Fórum","Réplicas no Fórum","Adição de Tópicos no Fórum", 
                                                "Atividade 1","Atividade 2","Atividade 3","Atividade 4","Vídeo 1","Vídeo 2", 
                                                "Quiz 1","Quiz 2","Pdf 1","Pdf 2","Ebook 1","Ebook 2",])
            self._df_sum = pd.DataFrame(columns=["Estudantes","Notas","Atividades Concluidas","Acessos de Materiais"])
        else:
            self.DATASET = pd.DataFrame(columns=["Students","Grade","AVA Access",
                                                "Forum Access","Forum Post","Forum Replies","Forum Add Thread", 
                                                "Assign 1","Assign 2","Assign 3","Assign 4","Video 1","Video 2", 
                                                "Quiz 1","Quiz 2","Pdf 1","Pdf 2","Ebook 1","Ebook 2",])
            self._df_sum = pd.DataFrame(columns=["Students","Grade","Completed Assigns","Material Access"])
        
        
        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)
        
        self.DATASET[self.DATASET.columns[1]] = np.random.triangular(0,85,100,self.NUMBER_STUDENTS)
        self.DATASET[self.DATASET.columns[1]] = self.DATASET.apply(self.convert_to_int, axis=1)
        
        for i in range(0,self.NUMBER_STUDENTS):
            self.DATASET.loc[i,self.DATASET.columns[0]] = rand_names[i]
            
            if (self.DATASET.loc[i,self.DATASET.columns[1]] <= 50):
                self.DATASET.loc[i,self.DATASET.columns[2]] = np.random.randint(5,26)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(0,4)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,4)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0,4)

                self.DATASET.loc[i,self.DATASET.columns[7]] = int(0)
                self.DATASET.loc[i,self.DATASET.columns[8]] = int(0)
                self.DATASET.loc[i,self.DATASET.columns[9]] = int(0)
                self.DATASET.loc[i,self.DATASET.columns[10]] = int(0)

                self.DATASET.loc[i,self.DATASET.columns[11]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[12]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[13]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[14]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[15]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[16]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[17]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[18]] = np.random.randint(0,2)

                self.DATASET.loc[i,self.DATASET.columns[3]] =  self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + np.random.randint(0,7)
                self._df_sum.loc[i,self._df_sum.columns[2]] = self.DATASET.loc[i,self.DATASET.columns[7]] + self.DATASET.loc[i,self.DATASET.columns[8]] + self.DATASET.loc[i,self.DATASET.columns[9]] + self.DATASET.loc[i,self.DATASET.columns[10]]
                self._df_sum.loc[i,self._df_sum.columns[3]] = self.DATASET.loc[i,self.DATASET.columns[11]] + self.DATASET.loc[i,self.DATASET.columns[12]] + self.DATASET.loc[i,self.DATASET.columns[13]] + self.DATASET.loc[i,self.DATASET.columns[14]] + self.DATASET.loc[i,self.DATASET.columns[15]] + self.DATASET.loc[i,self.DATASET.columns[16]] + self.DATASET.loc[i,self.DATASET.columns[17]] + self.DATASET.loc[i,self.DATASET.columns[18]]  

            elif (self.DATASET.loc[i,self.DATASET.columns[1]] <= 60):
                self.DATASET.loc[i,self.DATASET.columns[2]] = np.random.randint(20,41)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(0,8)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,8)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0,4)

                self.DATASET.loc[i,self.DATASET.columns[7]] = int(1)
                self.DATASET.loc[i,self.DATASET.columns[8]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[9]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[10]] = np.random.randint(0,2)

                self.DATASET.loc[i,self.DATASET.columns[11]] = np.random.randint(0,5)
                self.DATASET.loc[i,self.DATASET.columns[12]] = np.random.randint(0,5)
                self.DATASET.loc[i,self.DATASET.columns[13]] = np.random.randint(0,5)
                self.DATASET.loc[i,self.DATASET.columns[14]] = np.random.randint(0,5)
                self.DATASET.loc[i,self.DATASET.columns[15]] = np.random.randint(0,5)
                self.DATASET.loc[i,self.DATASET.columns[16]] = np.random.randint(0,5)
                self.DATASET.loc[i,self.DATASET.columns[17]] = np.random.randint(0,5)
                self.DATASET.loc[i,self.DATASET.columns[18]] = np.random.randint(0,5)

                self.DATASET.loc[i,self.DATASET.columns[3]] = self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + np.random.randint(0,22)
                self._df_sum.loc[i,self._df_sum.columns[2]] = self.DATASET.loc[i,self.DATASET.columns[7]] + self.DATASET.loc[i,self.DATASET.columns[8]] + self.DATASET.loc[i,self.DATASET.columns[9]] + self.DATASET.loc[i,self.DATASET.columns[10]]
                self._df_sum.loc[i,self._df_sum.columns[3]] = self.DATASET.loc[i,self.DATASET.columns[11]] + self.DATASET.loc[i,self.DATASET.columns[12]] + self.DATASET.loc[i,self.DATASET.columns[13]] + self.DATASET.loc[i,self.DATASET.columns[14]] + self.DATASET.loc[i,self.DATASET.columns[15]] + self.DATASET.loc[i,self.DATASET.columns[16]] + self.DATASET.loc[i,self.DATASET.columns[17]] + self.DATASET.loc[i,self.DATASET.columns[18]]

            elif (self.DATASET.loc[i,self.DATASET.columns[1]] <= 70):
                self.DATASET.loc[i,self.DATASET.columns[2]] = np.random.randint(35,57)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(1,12)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0,12)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0,8)

                self.DATASET.loc[i,self.DATASET.columns[7]] = int(1)
                self.DATASET.loc[i,self.DATASET.columns[8]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[9]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[10]] = int(1)

                self.DATASET.loc[i,self.DATASET.columns[11]] = np.random.randint(0,6)
                self.DATASET.loc[i,self.DATASET.columns[12]] = np.random.randint(0,6)
                self.DATASET.loc[i,self.DATASET.columns[13]] = np.random.randint(0,6)
                self.DATASET.loc[i,self.DATASET.columns[14]] = np.random.randint(0,6)
                self.DATASET.loc[i,self.DATASET.columns[15]] = np.random.randint(0,6)
                self.DATASET.loc[i,self.DATASET.columns[16]] = np.random.randint(0,6)
                self.DATASET.loc[i,self.DATASET.columns[17]] = np.random.randint(0,6)
                self.DATASET.loc[i,self.DATASET.columns[18]] = np.random.randint(0,6)

                self.DATASET.loc[i,self.DATASET.columns[3]] =  self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + np.random.randint(2,26)
                self._df_sum.loc[i,self._df_sum.columns[2]] = self.DATASET.loc[i,self.DATASET.columns[7]] + self.DATASET.loc[i,self.DATASET.columns[8]] + self.DATASET.loc[i,self.DATASET.columns[9]] + self.DATASET.loc[i,self.DATASET.columns[10]]
                self._df_sum.loc[i,self._df_sum.columns[3]] = self.DATASET.loc[i,self.DATASET.columns[11]] + self.DATASET.loc[i,self.DATASET.columns[12]] + self.DATASET.loc[i,self.DATASET.columns[13]] + self.DATASET.loc[i,self.DATASET.columns[14]] + self.DATASET.loc[i,self.DATASET.columns[15]] + self.DATASET.loc[i,self.DATASET.columns[16]] + self.DATASET.loc[i,self.DATASET.columns[17]] + self.DATASET.loc[i,self.DATASET.columns[18]]

            elif (self.DATASET.loc[i,self.DATASET.columns[1]] <= 80):
                self.DATASET.loc[i,self.DATASET.columns[2]] = np.random.randint(50,71)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(2,21)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(2,21)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0,7)

                self.DATASET.loc[i,self.DATASET.columns[7]] = int(1)
                self.DATASET.loc[i,self.DATASET.columns[8]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[9]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[10]] = int(1)

                self.DATASET.loc[i,self.DATASET.columns[11]] = np.random.randint(0,11)
                self.DATASET.loc[i,self.DATASET.columns[12]] = np.random.randint(1,11)
                self.DATASET.loc[i,self.DATASET.columns[13]] = np.random.randint(0,11)
                self.DATASET.loc[i,self.DATASET.columns[14]] = np.random.randint(1,11)
                self.DATASET.loc[i,self.DATASET.columns[15]] = np.random.randint(0,11)
                self.DATASET.loc[i,self.DATASET.columns[16]] = np.random.randint(1,11)
                self.DATASET.loc[i,self.DATASET.columns[17]] = np.random.randint(0,11)
                self.DATASET.loc[i,self.DATASET.columns[18]] = np.random.randint(1,11)

                self.DATASET.loc[i,self.DATASET.columns[3]] =  self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + np.random.randint(4,31)
                self._df_sum.loc[i,self._df_sum.columns[2]] = self.DATASET.loc[i,self.DATASET.columns[7]] + self.DATASET.loc[i,self.DATASET.columns[8]] + self.DATASET.loc[i,self.DATASET.columns[9]] + self.DATASET.loc[i,self.DATASET.columns[10]]
                self._df_sum.loc[i,self._df_sum.columns[3]] = self.DATASET.loc[i,self.DATASET.columns[11]] + self.DATASET.loc[i,self.DATASET.columns[12]] + self.DATASET.loc[i,self.DATASET.columns[13]] + self.DATASET.loc[i,self.DATASET.columns[14]] + self.DATASET.loc[i,self.DATASET.columns[15]] + self.DATASET.loc[i,self.DATASET.columns[16]] + self.DATASET.loc[i,self.DATASET.columns[17]] + self.DATASET.loc[i,self.DATASET.columns[18]]

            elif (self.DATASET.loc[i,self.DATASET.columns[1]] <= 90):
                self.DATASET.loc[i,self.DATASET.columns[2]] = np.random.randint(65,86)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(5,36)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(5,36)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(1,11)

                self.DATASET.loc[i,self.DATASET.columns[7]] = int(1)
                self.DATASET.loc[i,self.DATASET.columns[8]] = int(1)
                self.DATASET.loc[i,self.DATASET.columns[9]] = np.random.randint(0,2)
                self.DATASET.loc[i,self.DATASET.columns[10]] = int(1)

                self.DATASET.loc[i,self.DATASET.columns[11]] = np.random.randint(1,10)
                self.DATASET.loc[i,self.DATASET.columns[12]] = np.random.randint(3,14)
                self.DATASET.loc[i,self.DATASET.columns[13]] = np.random.randint(1,10)
                self.DATASET.loc[i,self.DATASET.columns[14]] = np.random.randint(3,14)
                self.DATASET.loc[i,self.DATASET.columns[15]] = np.random.randint(1,10)
                self.DATASET.loc[i,self.DATASET.columns[16]] = np.random.randint(3,14)
                self.DATASET.loc[i,self.DATASET.columns[17]] = np.random.randint(1,10)
                self.DATASET.loc[i,self.DATASET.columns[18]] = np.random.randint(3,14)

                self.DATASET.loc[i,self.DATASET.columns[3]] =  self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + np.random.randint(6,36)
                self._df_sum.loc[i,self._df_sum.columns[2]] = self.DATASET.loc[i,self.DATASET.columns[7]] + self.DATASET.loc[i,self.DATASET.columns[8]] + self.DATASET.loc[i,self.DATASET.columns[9]] + self.DATASET.loc[i,self.DATASET.columns[10]]
                self._df_sum.loc[i,self._df_sum.columns[3]] = self.DATASET.loc[i,self.DATASET.columns[11]] + self.DATASET.loc[i,self.DATASET.columns[12]] + self.DATASET.loc[i,self.DATASET.columns[13]] + self.DATASET.loc[i,self.DATASET.columns[14]] + self.DATASET.loc[i,self.DATASET.columns[15]] + self.DATASET.loc[i,self.DATASET.columns[16]] + self.DATASET.loc[i,self.DATASET.columns[17]] + self.DATASET.loc[i,self.DATASET.columns[18]]

            else:
                self.DATASET.loc[i,self.DATASET.columns[2]] = np.random.randint(80,101)
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(10,41)
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(10,41)
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(3,14)

                self.DATASET.loc[i,self.DATASET.columns[7]] = int(1)
                self.DATASET.loc[i,self.DATASET.columns[8]] = int(1)
                self.DATASET.loc[i,self.DATASET.columns[9]] = int(1)
                self.DATASET.loc[i,self.DATASET.columns[10]] = int(1)

                self.DATASET.loc[i,self.DATASET.columns[11]] = np.random.randint(2,13)
                self.DATASET.loc[i,self.DATASET.columns[12]] = np.random.randint(4,15)
                self.DATASET.loc[i,self.DATASET.columns[13]] = np.random.randint(2,13)
                self.DATASET.loc[i,self.DATASET.columns[14]] = np.random.randint(4,15)
                self.DATASET.loc[i,self.DATASET.columns[15]] = np.random.randint(2,13)
                self.DATASET.loc[i,self.DATASET.columns[16]] = np.random.randint(4,15)
                self.DATASET.loc[i,self.DATASET.columns[17]] = np.random.randint(2,13)
                self.DATASET.loc[i,self.DATASET.columns[18]] = np.random.randint(4,15)

                self.DATASET.loc[i,self.DATASET.columns[3]] =  self.DATASET.loc[i,self.DATASET.columns[4]] + self.DATASET.loc[i,self.DATASET.columns[5]] + self.DATASET.loc[i,self.DATASET.columns[6]] + np.random.randint(10,41)
                self._df_sum.loc[i,self._df_sum.columns[2]] = self.DATASET.loc[i,self.DATASET.columns[7]] + self.DATASET.loc[i,self.DATASET.columns[8]] + self.DATASET.loc[i,self.DATASET.columns[9]] + self.DATASET.loc[i,self.DATASET.columns[10]]
                self._df_sum.loc[i,self._df_sum.columns[3]] = self.DATASET.loc[i,self.DATASET.columns[11]] + self.DATASET.loc[i,self.DATASET.columns[12]] + self.DATASET.loc[i,self.DATASET.columns[13]] + self.DATASET.loc[i,self.DATASET.columns[14]] + self.DATASET.loc[i,self.DATASET.columns[15]] + self.DATASET.loc[i,self.DATASET.columns[16]] + self.DATASET.loc[i,self.DATASET.columns[17]] + self.DATASET.loc[i,self.DATASET.columns[18]]  


        df_k = self.DATASET.iloc[:,1:] #Selecting features to cluster
        kmeans = KMeans(n_clusters=4, init='random').fit(df_k) #Clustering
        
        self._df_sum[self.DATASET.columns[0]] = self.DATASET[self.DATASET.columns[0]]
        self._df_sum[self.DATASET.columns[1]] = self.DATASET[self.DATASET.columns[1]]
        self._df_sum[self.DATASET.columns[2]] = self.DATASET[self.DATASET.columns[2]]
        self._df_sum[self.DATASET.columns[3]] = self.DATASET[self.DATASET.columns[3]]
        self._df_sum[self.DATASET.columns[4]] = self.DATASET[self.DATASET.columns[4]]
        self._df_sum[self.DATASET.columns[5]] = self.DATASET[self.DATASET.columns[5]]
        self._df_sum[self.DATASET.columns[6]] = self.DATASET[self.DATASET.columns[6]]
        self._df_sum["Cluster"] = np.asarray(kmeans.labels_)

    def convert_to_int(self,row):
        return int(row[self.DATASET.columns[1]])

    # Table presenting raw data
    def graph_01(self):
        legend = {"title":"Relação entre as notas dos estudantes e seus acessos no AVA"}
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and their access in the VLE"}

        df = self._df_sum
        
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
                id='V005@1',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Scatter
    def graph_02(self):
        legend = {"title":"Relação entre as notas dos estudantes e seus acessos no AVA",
                    "xaxis":"Acessos no AVA",
                    "yaxis":"Notas",
                    'hovertext':'Nota'
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and their access in the VLE",
                        "xaxis":"Access in the VLE",
                        "yaxis":"Grades",
                        'hovertext':'Grade'
                    }
        
        df = self._df_sum.sort_values(by=[self._df_sum.columns[len(self._df_sum.columns)-1]])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(0,0,255)","rgb(127,0,127)","rgb(0,255,0)"]        
        color[Clusters[0]] = "rgb(255,0,0)"
        color[Clusters[1]] = "rgb(127,0,127)"
        color[Clusters[2]] = "rgb(0,0,255)"        
        color[Clusters[3]] = "rgb(0,255,0)"

        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            # print(df[df.columns[0]][i]) #print students
            trace.append(
                Scatter(
                    x=[df[df.columns[4]][i]], #Access
                    y=[df[df.columns[1]][i]], #Grade
                    hovertext = '<b>'+df[df.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(df[df.columns[4]][i])+'<br>'+legend['hovertext']+": "+str(df[df.columns[1]][i])+'<br>Cluster: '+str(df[df.columns[len(df.columns)-1]][i]+1),
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
            title=legend["title"],            
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
                # type = "category"
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
                # type = "category",
            )
        )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V005@2',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_03(self):
        legend = {"title":"Relação entre as notas dos estudantes e seus acessos nos materiais",
                    "xaxis":"Acessos nos materiais",
                    "yaxis":"Notas",
                    'hovertext':'Nota'
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and their access in the materials",
                        "xaxis":"Access in the materials",
                        "yaxis":"Grades",
                        'hovertext':'Grade'
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(0,0,255)","rgb(127,0,127)","rgb(0,255,0)"]
        color[Clusters[0]] = "rgb(255,0,0)"
        color[Clusters[1]] = "rgb(127,0,127)"
        color[Clusters[2]] = "rgb(0,0,255)"
        color[Clusters[3]] = "rgb(0,255,0)"

        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self._df_sum[self._df_sum.columns[3]][i]], #Material Access
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Grade
                    hovertext = '<b>'+df[df.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(df[df.columns[3]][i])+'<br>'+legend['hovertext']+": "+str(df[df.columns[1]][i])+'<br>Cluster: '+str(df[df.columns[len(df.columns)-1]][i]+1),
                    hoverinfo='text',
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],
                    marker=dict(
                        size=12,
                        symbol=self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i],
                        color = color[self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i]],
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
                range = [0, self._df_sum[self._df_sum.columns[3]].max()+10],
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
                id='V005@3',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_04(self):
        legend = {"title":"Relação entre as notas dos estudantes e as atividades concluídas por eles",
                    "xaxis":"Atividades concluídas",
                    "yaxis":"Notas",
                    'hovertext':'Nota'
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and the activities completed by them",
                        "xaxis":"Activities completed",
                        "yaxis":"Grades",
                        'hovertext':'Grade'
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(0,0,255)","rgb(127,0,127)","rgb(0,255,0)"]
        color[Clusters[0]] = "rgb(255,0,0)"
        color[Clusters[1]] = "rgb(127,0,127)"
        color[Clusters[2]] = "rgb(0,0,255)"        
        color[Clusters[3]] = "rgb(0,255,0)"

        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self._df_sum[self._df_sum.columns[2]][i]], #AssignAnswered
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Grade
                    hovertext = '<b>'+df[df.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(df[df.columns[2]][i])+'<br>'+legend['hovertext']+": "+str(df[df.columns[1]][i])+'<br>Cluster: '+str(df[df.columns[len(df.columns)-1]][i]+1),
                    hoverinfo='text',
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name                    
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],                    
                    marker=dict(
                        size=12,
                        symbol=self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i],
                        color = color[self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i]],
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
                range = [0, self._df_sum[self._df_sum.columns[2]].max()+10],
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
                id='V005@4',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_05(self):
        legend = {"title":"Relação entre as notas dos estudantes e seus acessos no fórum",
                    "xaxis":"Acessos no fórum",
                    "yaxis":"Notas",
                    'hovertext':'Nota'
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and their access in the forum",
                        "xaxis":"Access in the forum",
                        "yaxis":"Grades",
                        'hovertext':'Grade'
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(0,0,255)","rgb(127,0,127)","rgb(0,255,0)"]        
        color[Clusters[0]] = "rgb(255,0,0)"
        color[Clusters[1]] = "rgb(127,0,127)"
        color[Clusters[2]] = "rgb(0,0,255)"        
        color[Clusters[3]] = "rgb(0,255,0)"

        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self.DATASET[self.DATASET.columns[5]][i]], #Acesso ao fórum
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Grade
                    hovertext = '<b>'+df[df.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(df[df.columns[5]][i])+'<br>'+legend['hovertext']+": "+str(df[df.columns[1]][i])+'<br>Cluster: '+str(df[df.columns[len(df.columns)-1]][i]+1),
                    hoverinfo='text',
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name                    
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],                    
                    marker=dict(
                        size=12,
                        symbol=self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i],
                        color = color[self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i]],
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
                id='V005@5',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@5","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_06(self):
        legend = {"title":"Relação entre as notas dos estudantes e suas postagens no fórum",
                    "xaxis":"Postagens no fórum",
                    "yaxis":"Notas",
                    'hovertext':'Nota'
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and their posts in the forum",
                        "xaxis":"Posts in the forum",
                        "yaxis":"Grades",
                        'hovertext':'Grade'
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(0,0,255)","rgb(127,0,127)","rgb(0,255,0)"]        
        color[Clusters[0]] = "rgb(255,0,0)"
        color[Clusters[1]] = "rgb(127,0,127)"
        color[Clusters[2]] = "rgb(0,0,255)"        
        color[Clusters[3]] = "rgb(0,255,0)"

        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self.DATASET[self.DATASET.columns[6]][i]], #Postagem no fórum
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Grade
                    hovertext = '<b>'+df[df.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(df[df.columns[6]][i])+'<br>'+legend['hovertext']+": "+str(df[df.columns[1]][i])+'<br>Cluster: '+str(df[df.columns[len(df.columns)-1]][i]+1),
                    hoverinfo='text',
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name                    
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],                    
                    marker=dict(
                        size=12,
                        symbol=self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i],
                        color = color[self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i]],
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
                id='V005@6',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@6","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_07(self):
        legend = {"title":"Relação entre as notas dos estudantes e suas réplicas no fórum",
                    "xaxis":"Réplicas no fórum",
                    "yaxis":"Notas",
                    'hovertext':'Nota'
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and their replies in the forum",
                        "xaxis":"Replies in the forum",
                        "yaxis":"Grades",
                        'hovertext':'Grade'
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(0,0,255)","rgb(127,0,127)","rgb(0,255,0)"]        
        color[Clusters[0]] = "rgb(255,0,0)"
        color[Clusters[1]] = "rgb(127,0,127)"
        color[Clusters[2]] = "rgb(0,0,255)"        
        color[Clusters[3]] = "rgb(0,255,0)"

        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self.DATASET[self.DATASET.columns[7]][i]], #Replies
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Grade
                    hovertext = '<b>'+df[df.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(df[df.columns[7]][i])+'<br>'+legend['hovertext']+": "+str(df[df.columns[1]][i])+'<br>Cluster: '+str(df[df.columns[len(df.columns)-1]][i]+1),
                    hoverinfo='text',
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name                    
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],                    
                    marker=dict(
                        size=12,
                        symbol=self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i],
                        color = color[self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i]],
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
                id='V005@7',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@7","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_08(self):
        legend = {"title":"Relação entre as notas dos estudantes e seus tópicos adicionados no fórum",
                    "xaxis":"Tópicos no fórum",
                    "yaxis":"Notas",
                    'hovertext':'Nota'
                }
        if (self._language == "en"):
            legend = {"title":"Relation between either students' grades and their threads added in the forum",
                        "xaxis":"Threads in the forum",
                        "yaxis":"Grades",
                        'hovertext':'Grade'
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(0,0,255)","rgb(127,0,127)","rgb(0,255,0)"]
        color[Clusters[0]] = "rgb(255,0,0)"
        color[Clusters[1]] = "rgb(127,0,127)"
        color[Clusters[2]] = "rgb(0,0,255)"        
        color[Clusters[3]] = "rgb(0,255,0)"
        
        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[self.DATASET[self.DATASET.columns[8]][i]], #Init threads in forum
                    y=[self.DATASET[self.DATASET.columns[1]][i]], #Grade
                    hovertext = '<b>'+df[df.columns[0]][i]+'</b><br>'+legend['xaxis']+": "+str(df[df.columns[8]][i])+'<br>'+legend['hovertext']+": "+str(df[df.columns[1]][i])+'<br>Cluster: '+str(df[df.columns[len(df.columns)-1]][i]+1),
                    hoverinfo='text',
                    mode='markers',
                    name=self.DATASET[self.DATASET.columns[0]][i], #each student name                    
                    text = [str(self.DATASET[self.DATASET.columns[0]][i])],                    
                    marker=dict(
                        size=12,
                        symbol=self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i],
                        color = color[self._df_sum[self._df_sum.columns[len(self._df_sum.columns)-1]][i]],
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
                range = [0, self.DATASET[self.DATASET.columns[6]].max()+10],
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
                id='V005@8',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@8","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Box
    def graph_09(self):
        legend = {"title":"Variação de notas dos estudantes por cluster",
                    "xaxis":"",
                    "yaxis":"Notas",
                    'hovertext':'Nota'
                }
        if (self._language == "en"):
            legend = {"title":"Students' grades variation by cluster",
                        "xaxis":"",
                        "yaxis":"Grades",
                        'hovertext':'Grade'
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_grades = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #Grades
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_grades, #Grades
                    name="Cluster "+str(i+1),
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
                range = [-1, self.DATASET[self.DATASET.columns[1]].max()+10],
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
                id='V005@9',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@9","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_10(self):
        legend = {"title":"Variação de acessos no AVA por cluster",
                    "xaxis":"",
                    "yaxis":"Acessos no AVA",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' access in the VLE by cluster",
                        "xaxis":"",
                        "yaxis":"Access in the VLE",
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[4]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #Access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_access, #Access
                    name="Cluster "+str(i+1),
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                id='V005@10',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@10","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_11(self):
        legend = {"title":"Variação de acessos nos materiais por cluster",
                    "xaxis":"",
                    "yaxis":"Acessos nos materiais",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' access in the materials by cluster",
                        "xaxis":"",
                        "yaxis":"Access in the materials",
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #Access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_access, #Access
                    name="Cluster "+str(i+1),
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                range = [-1, self._df_sum[self._df_sum.columns[3]].max()+10],
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
                id='V005@11',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@11","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_12(self):
        legend = {"title":"Variação de atividades concluídas por cluster",
                    "xaxis":"",
                    "yaxis":"Atividades concluídas",
                }
        if (self._language == "en"):
            legend = {"title":"Activities completed variation by cluster",
                        "xaxis":"",
                        "yaxis":"Activities completed",
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_assigns = df[df.columns[2]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #Assigns
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_assigns,
                    name="Cluster "+str(i+1),
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_assigns[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                range = [-1, df[df.columns[2]].max()+10],
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
                id='V005@12',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@12","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_13(self):
        legend = {"title":"Variação de acessos no fórum por cluster",
                    "xaxis":"",
                    "yaxis":"Acessos no fórum",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' access in the forum by cluster",
                        "xaxis":"",
                        "yaxis":"Access in the forum",
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[5]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #Access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_access,
                    name="Cluster "+str(i+1),
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                id='V005@13',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@13","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_14(self):
        legend = {"title":"Variação de postagens no fórum por cluster",
                    "xaxis":"",
                    "yaxis":"Postagens no fórum",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' posts in the forum by cluster",
                        "xaxis":"",
                        "yaxis":"Posts in the forum",
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_posts = df[df.columns[6]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #Posts
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_posts,
                    name="Cluster "+str(i+1),
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_posts[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                id='V005@14',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@14","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_15(self):
        legend = {"title":"Variação de réplicas no fórum por cluster",
                    "xaxis":"",
                    "yaxis":"Réplicas no fórum",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' replies in the forum by cluster",
                        "xaxis":"",
                        "yaxis":"Replies in the forum",
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_replies = df[df.columns[7]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #Replies
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_replies,
                    name="Cluster "+str(i+1),
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_replies[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                id='V005@15',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@15","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_16(self):
        legend = {"title":"Variação de tópicos adicionados no fórum por cluster",
                    "xaxis":"",
                    "yaxis":"Tópicos no fórum",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' threads added in the forum by cluster",
                        "xaxis":"",
                        "yaxis":"Threads in the forum",
                    }
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_threads = df[df.columns[8]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #threads
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                Box(
                    y=lst_threads,
                    name="Cluster "+str(i+1),
                    text=['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_threads[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                range = [-1, self.DATASET[self.DATASET.columns[6]].max()+10],
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
                id='V005@16',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@16","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Violin
    def graph_17(self):
        legend = {"title":"Variação de notas dos estudantes por cluster",
                    "xaxis":"",
                    "yaxis":"Notas",
                    'hovertext':"Nota"
                }
        if (self._language == "en"):
            legend = {"title":"Students' grades variation by cluster",
                        "xaxis":"",
                        "yaxis":"Grades",
                        'hovertext':"Grade"
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_grades = df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #grades
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":lst_grades,
                    "name":"Cluster "+str(i+1),
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
                range = [-15, self.DATASET[self.DATASET.columns[1]].max()+10],                
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
                id='V005@17',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@17","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_18(self):
        legend = {"title":"Variação de acessos no AVA por cluster",
                    "xaxis":"",
                    "yaxis":"Acessos no AVA",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' access in the VLE by cluster",
                        "xaxis":"",
                        "yaxis":"Access in the VLE",
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[4]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":df[df.columns[4]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]],
                    "name":"Cluster "+str(i+1),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
            # title='Variação de acessos por cluster',
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
                id='V005@18',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@18","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_19(self):
        legend = {"title":"Variação de acessos nos materiais por cluster",
                    "xaxis":"",
                    "yaxis":"Acessos nos materiais",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' access in the materials by cluster",
                        "xaxis":"",
                        "yaxis":"Access in the materials",
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[3]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":lst_access,
                    "name":"Cluster "+str(i+1),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                range = [-15, self._df_sum[self._df_sum.columns[3]].max()+10],
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
                id='V005@19',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@19","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_20(self):
        legend = {"title":"Variação de atividades concluídas por cluster",
                    "xaxis":"",
                    "yaxis":"Atividades concluídas",
                }
        if (self._language == "en"):
            legend = {"title":"Activities completed variation by cluster",
                        "xaxis":"",
                        "yaxis":"Activities completed",
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[2]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":lst_access,
                    "name":"Cluster "+str(i+1),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                range = [-15, df[df.columns[2]].max()+10],                
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
                id='V005@20',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@20","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_21(self):
        legend = {"title":"Variação de acessos no fórum por cluster",
                    "xaxis":"",
                    "yaxis":"Acessos no fórum",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' access in the forum by cluster",
                        "xaxis":"",
                        "yaxis":"Access in the forum",
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[5]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":lst_access,
                    "name":"Cluster "+str(i+1),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                id='V005@21',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@21","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_22(self):
        legend = {"title":"Variação de postagens no fórum por cluster",
                    "xaxis":"",
                    "yaxis":"Postagens no fórum",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' posts in the forum by cluster",
                        "xaxis":"",
                        "yaxis":"Posts in the forum",
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[6]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":lst_access,
                    "name":"Cluster "+str(i+1),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                id='V005@22',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@22","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_23(self):
        legend = {"title":"Variação de réplicas no fórum por cluster",
                    "xaxis":"",
                    "yaxis":"Réplicas no fórum",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' replies in the forum by cluster",
                        "xaxis":"",
                        "yaxis":"Replies in the forum",
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[7]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":lst_access,
                    "name":"Cluster "+str(i+1),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                id='V005@23',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@23","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_24(self):
        legend = {"title":"Variação de tópicos adicionados no fórum por cluster",
                    "xaxis":"",
                    "yaxis":"Tópicos no fórum",
                }
        if (self._language == "en"):
            legend = {"title":"Variation of students' threads added in the forum by cluster",
                        "xaxis":"",
                        "yaxis":"Threads in the forum",
                    }
        # https://plot.ly/python/violin/#reference
        # https://plot.ly/python/reference/#violin
        df = self._df_sum.sort_values(by=self._df_sum.columns[1])
        Clusters = df[df.columns[len(df.columns)-1]].unique()
        color = ["rgb(255,0,0)","rgb(127,0,127)","rgb(0,0,255)","rgb(0,255,0)"]        
        # print(Clusters)
        trace = []
        for i in range(0,len(Clusters)):
            lst_access = df[df.columns[8]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist() #access
            lst_names = df[df.columns[0]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]].values.tolist()
            trace.append(
                {
                    "type":'violin',
                    "x":["Cluster "+str(i+1)]*len(df[df.columns[1]].loc[df[df.columns[len(df.columns)-1]]==Clusters[i]]),
                    "y":lst_access,
                    "name":"Cluster "+str(i+1),
                    'text':['<b>'+lst_names[j]+'</b><br>'+legend['yaxis']+": "+str(lst_access[j])+'<br>Cluster '+str(i+1) for j in range(len(lst_names))],
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
                range = [-15, self.DATASET[self.DATASET.columns[6]].max()+10],                
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
                id='V005@24',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V005@24","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

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
        elif id == 14:
            return self.graph_14()
        elif id == 15:
            return self.graph_15()
        elif id == 16:
            return self.graph_16()
        elif id == 17:
            return self.graph_17()
        elif id == 18:
            return self.graph_18()
        elif id == 19:
            return self.graph_19()
        elif id == 20:
            return self.graph_20()
        elif id == 21:
            return self.graph_21()
        elif id == 22:
            return self.graph_22()
        elif id == 23:
            return self.graph_23()
        elif id == 24:
            return self.graph_24()
        else:
            print("V005@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V005_'+str(id)+'.pkl'
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
        
        file_name = 'V005_'+str(id)+'.pkl'
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
        self.graph_06()
        self.graph_07()
        self.graph_08()
        self.graph_09() #Box
        self.graph_10()
        self.graph_11()
        self.graph_12()
        self.graph_13()
        self.graph_14()
        self.graph_15()
        self.graph_16()
        self.graph_17() #Violin
        self.graph_18()
        self.graph_19()
        self.graph_20()
        self.graph_21()
        self.graph_22()
        self.graph_23()
        self.graph_24()

# instance = V005()
# instance.generate_dataset(number_students = 30)
# instance.print_all_graphs("pt")
# instance.print_all_graphs("en")

# *[MP-017] Students can be clustered into different groups based on their access or interaction patterns.
# *[MP-020] Students with a satisfatory performance ignore part of the materials in distance courses.
# *[MP-028] Student groups that use more forums tend to have a good performance.
# *[MP-030] Students groups that do more replies in forums tend to have a good performance.
# *[MP-031] Students groups that init threads in forums tend to have a good performance.
# *[MP-035] Successful students are more frequently and regularly participating and engaged in online activities.
# [MP-106] Student groups that have more posts are more likely to complete the course.
# *[RQ-02] Identify student access patterns (e.g., login, materials).
# *[RQ-03] Identify student performance patterns.
# *[RQ-04] Identify student interest patterns on the course.
# *[RQ-05] Identify student usage patterns on the forum.
# *[RQ-07] Identify student interaction patterns (e.g., materials).
# *[RQ-08] Identify student participation patterns on the course.
# [RQ-09] Identify student drop out patterns.
# [RQ-14] Identify pace learning student.
# [RQ-17] Relate both students' navigation and performance.
# [RQ-18] Relate video length and student performance.
# [RQ-21] Relate video script and student performance.
