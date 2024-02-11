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

class V010:
    NUMBER_STUDENTS = 20
    NUMBER_VIDEOS = 10
    DATASET = pd.DataFrame()
    
    _language = "pt"
    _type_result="jupyter-notebook"
    _understood = 1
    _misunderstood = 0
    _video_name = []
    _video_dur = []
    _df_sum_feedback = pd.DataFrame()
    _preprocessed_folder = os.path.join('Preprocessed')
    
    def __init__(self, language="pt", type_result = "jupyter-notebook"):
        self._language = language
        self._type_result = type_result

    def generate_dataset(self, number_students = 20, number_video = 10, rand_names = []):
        self.NUMBER_STUDENTS = number_students
        self.NUMBER_VIDEOS = number_video

        if (self._language == "pt"):
            video_label = "Vídeo "
            students_label = "Estudantes"
            self._df_sum_feedback = pd.DataFrame(columns=[video_label,"Entendido","Não entendido","Total"])
        else:
            video_label = "Video "
            students_label = "Students"
            self._df_sum_feedback = pd.DataFrame(columns=[video_label,"Understood","Misunderstood","Total"])

        self._video_dur = [np.random.randint(240,600) for n in range(self.NUMBER_VIDEOS)] #video duration ranging between 240 and 600 seconds
        self._video_name = [video_label+str(i+1) for i in range (0, self.NUMBER_VIDEOS)]
        
        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)

        self.DATASET = pd.DataFrame(columns=self._video_name)
        self.DATASET.insert(0,students_label, rand_names)
        
        for i in range(1,len(self.DATASET.columns)):
            self.DATASET.iloc[:,i] = [self._understood]*self.NUMBER_STUDENTS #Adding 'well-understanding' to Video[i]
            number_doubts = np.random.randint(0,self.NUMBER_STUDENTS+1) #Get a random number of students with doubts in Video[i]
            index = np.random.randint(0,self.NUMBER_STUDENTS,number_doubts) #Get a random students index with doubts in Video[i]
            for j in range(0, number_doubts):
                self.DATASET.iloc[int(index[j]),i] = self._misunderstood #Adding doubt to Video[i] for student with index[j]

        self._df_sum_feedback[self._df_sum_feedback.columns[0]] = self.DATASET.columns[1:].tolist()
        self._df_sum_feedback[self._df_sum_feedback.columns[1]] = self.sum_feedback(True) # Sum all understood feedback
        self._df_sum_feedback[self._df_sum_feedback.columns[2]] = self.sum_feedback(False) # Sum all misunderstood feedback
        self._df_sum_feedback[self._df_sum_feedback.columns[3]] = [len(self.DATASET)]*len(self.DATASET.columns[1:])

    def sum_feedback(self, understood=True):
        if understood == True:
            feedback = self._understood
        else:
            feedback = self._misunderstood

        lst = []
        for i in range(1,len(self.DATASET.columns)):
            key = self.DATASET.columns[i]
            lst.append(len(self.DATASET.loc[self.DATASET[key]==feedback]))
    
        return lst

    # Table presenting raw data
    def graph_01(self):
        legend = {"title":"Número de estudantes que entenderam os vídeos"}
        if (self._language == "en"):
            legend = {"title":"Number of students who understood the video"}
        df = self.DATASET

        trace = [Table(
            header=dict(
                values=list(df.columns)+["Total"],
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[df[i].tolist() for i in df.columns]+[[sum(df.iloc[j,1:]) for j in range(len(df))]],
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
                id='V010@1',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_02(self):
        legend = {"title":"Número de estudantes que entenderam os vídeos"}
        if (self._language == "en"):
            legend = {"title":"Number of students who understood the video"}
        df = self._df_sum_feedback

        trace = [Table(
            header=dict(
                values=list(df.columns),
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[df[i].tolist() for i in df.columns],
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
                id='V010@2',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Bar    
    def graph_03(self):
        legend = {"title":"Número de estudantes que entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    'hovertext':' estudantes entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood the video",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        'hovertext':' students understood'
                    }

        df = self._df_sum_feedback
        trace = [Bar(
            x=df[df.columns[0]].values,
            y=df[df.columns[1]].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
        )]

        data = trace
        layout = Layout(
            title = legend["title"],
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=5,
                # ticklen=5,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@3',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_04(self):
        legend = {"title":"Número de estudantes que entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    'hovertext':' estudantes entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood the video",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        'hovertext':' students understood'
                    }

        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[1],self._df_sum_feedback.columns[0]])
        trace = [Bar(
            x=df[df.columns[0]].values,
            y=df[df.columns[1]].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
        )]

        data = trace
        layout = Layout(
            title = legend["title"],
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=5,
                # ticklen=5,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@4',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_05(self):
        legend = {"title":"Número de estudantes que <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    'hovertext':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who do <b>not</b> understood the video",
                        "xaxis":"",
                        "yaxis":"Number of students",
                    'hovertext':' students do <b>not</b> understood'
                    }

        df = self._df_sum_feedback
        trace = [Bar(
            x=df[df.columns[0]].values,
            y=df[df.columns[2]].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,2])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
            marker=dict(
                color='rgb(255,126,24)',                
            ),
        )]

        data = trace
        layout = Layout(
            title = legend["title"],
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=5,
                # ticklen=5,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@5',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@5","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_06(self):
        legend = {"title":"Número de estudantes que <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    'hovertext':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who do <b>not</b> understood the video",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        'hovertext':' students do <b>not</b> understood'
                    }

        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[2],self._df_sum_feedback.columns[0]])
        trace = [Bar(
            x=df[df.columns[0]].values,
            y=df[df.columns[2]].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,2])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
            marker=dict(
                color='rgb(255,126,24)',                
            ),
        )]

        data = trace
        layout = Layout(
            title = legend["title"],
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=5,
                # ticklen=5,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@6',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@6","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_07(self):
        legend = {"title":"Número de estudantes que entenderam os vídeos",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    'hovertext':' estudantes entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood the video",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        'hovertext':' students understood'
                    }

        df = self._df_sum_feedback
        trace = [Bar(
            x=df[df.columns[1]].values,
            y=df[df.columns[0]].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
            orientation='h'
        )]

        data = trace
        layout = Layout(
            title = legend["title"],
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=1,
                # ticklen=5,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@7',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@7","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_08(self):
        legend = {"title":"Número de estudantes que entenderam os vídeos",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    'hovertext':' estudantes entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood the video",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        'hovertext':' students understood'
                    }

        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[1],self._df_sum_feedback.columns[0]])
        trace = [Bar(
            x=df[df.columns[1]].values,
            y=df[df.columns[0]].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
            orientation='h'
        )]

        data = trace
        layout = Layout(
            title = legend["title"],
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=1,
                # ticklen=5,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@8',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@8","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_09(self):
        legend = {"title":"Número de estudantes que <b>não</b> entenderam os vídeos",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    'hovertext':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who do not understood the video",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        'hovertext':' students do <b>not</b> understood'
                    }

        df = self._df_sum_feedback
        trace = [Bar(
            x=df[df.columns[2]].values,
            y=df[df.columns[0]].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,2])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
            orientation='h',
            marker=dict(
                color='rgb(255,126,24)',                
            ),
        )]

        data = trace
        layout = Layout(
            title = legend["title"],
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=1,
                # ticklen=5,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@9',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@9","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_10(self):
        legend = {"title":"Número de estudantes que <b>não</b> entenderam os vídeos",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    'hovertext':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who do <b>not</b> understood the video",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        'hovertext':' students do <b>not</b> understood'
                    }

        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[2],self._df_sum_feedback.columns[0]])
        trace = [Bar(
            x=df[df.columns[2]].values,
            y=df[df.columns[0]].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,2])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
            orientation='h',
            marker=dict(
                color='rgb(255,126,24)',
            ),
        )]

        data = trace
        layout = Layout(
            title = legend["title"],
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=1,
                # ticklen=5,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@10',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@10","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Lollipop
    def graph_11(self):
        legend = {"title":"Número de estudantes que entenderam os vídeos",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "text_s":"estudante",
                    "text_p":"estudantes",
                    'hovertext':' estudantes entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood the video",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "text_s":"student",
                        "text_p":"students",
                        'hovertext':' students understood'
                    }
        df = self._df_sum_feedback
        
        trace = []
        trace.append(
            Bar(
                x=df[df.columns[1]].values,
                y=df[df.columns[0]].values,
                width=[0.07]*len(df[df.columns[1]].values),
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',                        
                    )
            )
        )
        
        for i in range(0, max(df[df.columns[1]].values.tolist())+1):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df[df.columns[0]]),
                    y=df[df.columns[0]].loc[df[df.columns[1]]==i].values.tolist(),
                    mode='markers',
                    name = "",
                    text=text*len(df[df.columns[0]].loc[df[df.columns[1]]==i]),
                    hovertext = '<b>'+df[df.columns[0]].loc[df[df.columns[1]]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=2,
                            color = 'rgb(0,0,255)',
                        )
                    )                
                )                        
            )

        data = trace
        
        layout = Layout(
            title = legend["title"],
            showlegend=False,
            # showgrid=False,
            hovermode = "closest",
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                tick0=0,
                dtick=1,
                showgrid=True
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=1,
                showgrid=False,
                # ticklen=4,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Lollipop')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@11',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@11","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_12(self):
        legend = {"title":"Número de estudantes que entenderam os vídeos",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "text_s":"estudante",
                    "text_p":"estudantes",
                    'hovertext':' estudantes entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood the video",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "text_s":"student",
                        "text_p":"students",
                        'hovertext':' students understood'
                    }
        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[1],self._df_sum_feedback.columns[0]])
        
        trace = []
        trace.append(
            Bar(
                x=df[df.columns[1]].values,
                y=df[df.columns[0]].values,
                width=[0.07]*len(df[df.columns[1]].values),
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',                        
                    )
            )
        )
        
        for i in range(0, max(df[df.columns[1]].values.tolist())+1):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df[df.columns[0]]),
                    y=df[df.columns[0]].loc[df[df.columns[1]]==i].values.tolist(),
                    mode='markers',
                    name = "",                 
                    text=text*len(df[df.columns[0]].loc[df[df.columns[1]]==i]),                    
                    hovertext = '<b>'+df[df.columns[0]].loc[df[df.columns[1]]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=2,
                            color = 'rgb(0,0,255)',
                        )
                    )                
                )                        
            )

        data = trace
        
        layout = Layout(
            title = legend["title"],
            showlegend=False,
            # showgrid=False,
            hovermode = "closest",
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                tick0=0,
                dtick=1,
                showgrid=True
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=1,
                showgrid=False,
                # ticklen=4,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Lollipop')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@12',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@12","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_13(self):
        legend = {"title":"Número de estudantes que <b>não</b> entenderam os vídeos",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "text_s":"estudante",
                    "text_p":"estudantes",
                    'hovertext':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who do <b>not</b> understood the video",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "text_s":"student",
                        "text_p":"students",
                        'hovertext':' students do <b>not</b> understood'
                    }
        df = self._df_sum_feedback
        
        trace = []
        trace.append(
            Bar(
                x=df[df.columns[2]].values,
                y=df[df.columns[0]].values,
                width=[0.07]*len(df[df.columns[2]].values),
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',                        
                    )
            )
        )
        
        for i in range(0, max(df[df.columns[2]].values.tolist())+1):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df[df.columns[0]]),
                    y=df[df.columns[0]].loc[df[df.columns[2]]==i].values.tolist(),
                    mode='markers',
                    name = "",                 
                    text=text*len(df[df.columns[0]].loc[df[df.columns[2]]==i]),                    
                    hovertext = '<b>'+df[df.columns[0]].loc[df[df.columns[2]]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color='rgb(255,126,24)',
                        line=dict(
                            width=2,
                            color='rgb(255,126,24)',
                        )
                    )                
                )                        
            )

        data = trace
        
        layout = Layout(
            title = legend["title"],
            showlegend=False,
            # showgrid=False,
            hovermode = "closest",
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                tick0=0,
                dtick=1,
                showgrid=True
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=1,
                showgrid=False,
                # ticklen=4,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Lollipop')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@13',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@13","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_14(self):
        legend = {"title":"Número de estudantes que <b>não</b> entenderam os vídeos",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "text_s":"estudante",
                    "text_p":"estudantes",
                    'hovertext':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who do <b>not</b> understood the video",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "text_s":"student",
                        "text_p":"students",
                        'hovertext':' students do <b>not</b> understood'
                    }
        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[2],self._df_sum_feedback.columns[0]])
        
        trace = []
        trace.append(
            Bar(
                x=df[df.columns[2]].values,
                y=df[df.columns[0]].values,
                width=[0.07]*len(df[df.columns[2]].values),
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',                        
                    )
            )
        )
        
        for i in range(0, max(df[df.columns[2]].values.tolist())+1):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df[df.columns[0]]),
                    y=df[df.columns[0]].loc[df[df.columns[2]]==i].values.tolist(),
                    mode='markers',
                    name = "",                 
                    text=text*len(df[df.columns[0]].loc[df[df.columns[2]]==i]),                    
                    hovertext = '<b>'+df[df.columns[0]].loc[df[df.columns[2]]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color='rgb(255,126,24)',
                        line=dict(
                            width=2,
                            color='rgb(255,126,24)',
                        )
                    )                
                )                        
            )

        data = trace
        
        layout = Layout(
            title = legend["title"],
            showlegend=False,
            # showgrid=False,
            hovermode = "closest",
            xaxis=dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                tick0=0,
                dtick=1,
                showgrid=True
            ),
            yaxis=dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                showticklabels=True,
                tick0=0,
                dtick=1,
                showgrid=False,
                # ticklen=4,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 4.1]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Lollipop')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@14',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@14","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Scatter
    def graph_15(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Vídeos entendidos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' entendeu '
                }
        if (self._language == "en"):
            legend = {"title":"Understood videos by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' understood '
                    }
        df = self.DATASET

        sizeref = 0.01
        
        trace = []
        for i in range(0, len(df)):                    
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns), #student
                    y=df.columns[1:], #assigns
                    mode='markers',
                    # name=df.iloc[i,0], #each student name
                    name=df.iloc[i,0], #student name
                    # text = df.iloc[i,1:].values.tolist(),
                    hovertext = ['<b>'+df.iloc[i,0]+'</b>'+legend['hovertext']+df.columns[j+1] if df.iloc[i,j+1] > 0 else '' for j in range(len(df.columns[1:]))],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,1:].values.tolist(),
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=2,
                            color='rgb(0,0,255)',
                        )
                    )
                )
            )

        layout = Layout(
            title=legend['title'],
            # title='Number of access in the materials grouped by student',
            hovermode = "closest",
            showlegend = False,
            xaxis = dict(
                title = legend['xaxis'],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(df)],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            yaxis = dict(
                title = legend['yaxis'],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(df.columns[1:])],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            margin = dict(
                b=150,
            )
        )

        data = trace
        fig=Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@15',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@15","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_16(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Vídeos <b>não</b> entendidos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' <b>não</b> entendeu '
                }
        if (self._language == "en"):
            legend = {"title":"Misunderstood videos by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' do <b>not</b> understood '
                    }
        df = self.DATASET

        sizeref = 0.01
        
        trace = []
        for i in range(0, len(df)):
            x = df.iloc[i,1:].values.tolist()
            y = [-1]*len(df.columns[1:])
            z = [i + j for i, j in zip(x, y)]
            values = [i*(-1) for i in z]
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns), #student
                    y=df.columns[1:], #assigns
                    mode='markers',
                    name=df.iloc[i,0], #student name
                    # text = df.iloc[i,1:].values.tolist(),
                    hovertext = ['<b>'+df.iloc[i,0]+'</b>'+legend['hovertext']+df.columns[j+1] if df.iloc[i,j+1] == 0 else '' for j in range(len(df.columns[1:]))],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=values,
                        color='rgb(255,126,24)',
                        line=dict(
                            width=2,
                            color='rgb(255,126,24)',
                        )
                    )
                )
            )

        layout = Layout(
            title=legend['title'],
            # title='Number of access in the materials grouped by student',
            hovermode = "closest",
            showlegend = False,
            xaxis = dict(
                title = legend['xaxis'],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(df)],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            yaxis = dict(
                title = legend['yaxis'],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(df.columns[1:])],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            margin = dict(
                b=150,
            )
        )

        data = trace
        fig=Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@16',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@16","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_17(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Vídeos entendidos e <b>não</b> entendidos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext_done':' entendeu ',
                    'hovertext_undone':' <b>não</b> entendeu '
                }
        if (self._language == "en"):
            legend = {"title":"Understood and misunderstood videos by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext_done':' understood ',
                        'hovertext_undone':' do <b>not</b> understood '
                    }
        df = self.DATASET

        sizeref = 0.01
        
        trace = []
        for i in range(0, len(df)):                    
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns), #student
                    y=df.columns[1:], #assigns
                    hovertext = ['<b>'+df.iloc[i,0]+'</b>'+legend['hovertext_done']+df.columns[j+1] if df.iloc[i,j+1] > 0 else '' for j in range(len(df.columns[1:]))],
                    hoverinfo='text',
                    mode='markers',
                    # name=df.iloc[i,0], #each student name
                    name=df.iloc[i,0], #student name
                    # text = df.iloc[i,1:].values.tolist(),
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,1:].values.tolist(),
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=2,
                            color='rgb(0,0,255)',
                        )
                    )
                )
            )
        for i in range(0, len(df)):
            x = df.iloc[i,1:].values.tolist()
            y = [-1]*len(df.columns[1:])
            z = [i + j for i, j in zip(x, y)]
            values = [i*(-1) for i in z]
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns), #student
                    y=df.columns[1:], #assigns
                    hovertext = ['<b>'+df.iloc[i,0]+'</b>'+legend['hovertext_undone']+df.columns[j+1] if df.iloc[i,j+1] == 0 else '' for j in range(len(df.columns[1:]))],
                    hoverinfo='text',
                    mode='markers',
                    name=df.iloc[i,0], #student name
                    # text = df.iloc[i,1:].values.tolist(),
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=values,
                        color='rgb(255,126,24)',
                        line=dict(
                            width=2,
                            color='rgb(255,126,24)',
                        )
                    )
                )
            )

        layout = Layout(
            title=legend['title'],
            # title='Number of access in the materials grouped by student',
            hovermode = "closest",
            showlegend = False,
            xaxis = dict(
                title = legend['xaxis'],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(df)],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            yaxis = dict(
                title = legend['yaxis'],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(df.columns[1:])],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            margin = dict(
                b=150,
            )
        )

        data = trace
        fig=Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@17',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@17","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_18(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_done':' estudante(s) entendeu/entenderam o ',
                    'hovertext_undone':' estudante(s) <b>não</b> entendeu/entenderam o '
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and do <b>not</b> the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_done':' student(s) understood ',
                        'hovertext_undone':' student(s) do <b>not</b> understood '
                    }
        df = self._df_sum_feedback.iloc[:,0:3]
        sizeref = 0.03
        
        trace = []
        for i in range(0, len(df)):                    
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns), #videos
                    # y=df.columns[1:], #features ()
                    y=[legend["columns"][i] for i in range (1,2)],
                    mode='markers',                    
                    name=df.iloc[i,0], #videos
                    text = df.iloc[i,1:].values.tolist(),
                    hovertext = str(df.iloc[i,1])+legend['hovertext_done']+'<b>'+df.iloc[i,0]+'</b>',
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,1:].values.tolist(),
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=2
                        )
                    )
                )
            )
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns), #videos
                    # y=df.columns[1:], #features ()
                    y=[legend["columns"][i] for i in range (2,3)],
                    mode='markers',                    
                    name=df.iloc[i,0], #videos
                    text = df.iloc[i,2:].values.tolist(),
                    hovertext = str(df.iloc[i,2])+legend['hovertext_undone']+'<b>'+df.iloc[i,0]+'</b>',
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,2:].values.tolist(),
                        color='rgb(255,126,24)',
                        line=dict(
                            width=2
                        )
                    )
                )
            )

        layout = Layout(
            title=legend['title'],
            # title='Number of access in the materials grouped by student',
            hovermode = "closest",
            showlegend = False,
            xaxis = dict(
                title = legend['xaxis'],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(df)],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            yaxis = dict(
                title = legend['yaxis'],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(df.columns[1:])],
                rangemode = "normal",
                showline = True,                
                type = "category"
            )
        )

        data = trace
        fig=Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@18',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@18","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    #Heatmap
    def graph_19(self):
        legend = {"title":"Vídeos entendidos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext_understood':' entendeu o ',
                    'hovertext_misunderstood':' <b>não</b> entendeu o '
                }
        if (self._language == "en"):
            legend = {"title":"Understood videos by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext_understood':' understood ',
                        'hovertext_misunderstood':' do <b>not</b> understood '
                    }
        df = self.DATASET
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([df.iloc[j,0]+legend['hovertext_misunderstood']+df.columns[i] if values[j]==0 else df.iloc[j,0]+legend['hovertext_understood']+df.columns[i] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Videos
                        x=df.iloc[:,0], #Students
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        hovertext = hovervalue,
                        hoverinfo='text',
                        showscale = False
                    )
        
        layout = Layout(
                title = legend['title'],                
                # autosize=False,
                # width=950,
                # height=350,
                hovermode = "closest",
                xaxis=dict(
                    title = legend['xaxis'],
                    titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                ),                
                yaxis=dict(
                    title = legend['yaxis'],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    type="category",                    
                    tick0=0,
                    dtick=1,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',                    
                ),
                margin = dict(
                    b=150,
                )
            )

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@19',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@19","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_20(self):
        legend = {"title":"Vídeos <b>não</b> entendidos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext_understood':' entendeu o ',
                    'hovertext_misunderstood':' <b>não</b> entendeu o '
                }
        if (self._language == "en"):
            legend = {"title":"Misunderstood videos by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext_understood':' understood ',
                        'hovertext_misunderstood':' do <b>not</b> understood '
                    }
        df = self.DATASET
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            x = df.iloc[:,i].values.tolist()
            y = [-1]*len(x)
            f = [a + b for a, b in zip(x, y)]   
            values = [a*(-1) for a in f]         
            z.append(values)
            hovervalue.append([df.iloc[j,0]+legend['hovertext_understood']+df.columns[i] if values[j]==0 else df.iloc[j,0]+legend['hovertext_misunderstood']+df.columns[i] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Videos
                        x=df.iloc[:,0], #Students
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(255,126,24)']],
                        hovertext = hovervalue,
                        hoverinfo='text',
                        showscale = False,
                    )
        
        layout = Layout(
                title = legend['title'],                
                # autosize=False,
                # width=950,
                # height=350,
                hovermode = "closest",
                xaxis=dict(
                    title = legend['xaxis'],
                    titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                ),                
                yaxis=dict(
                    title = legend['yaxis'],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    type="category",                    
                    tick0=0,
                    dtick=1,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',                    
                ),
                margin = dict(
                    b=150,
                )
            )

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@20',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@20","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_21(self):
        legend = {"title":"Vídeos entendidos e <b>não</b> entendidos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext_understood':' entendeu o ',
                    'hovertext_misunderstood':' <b>não</b> entendeu o '
                }
        if (self._language == "en"):
            legend = {"title":"Understood and misunderstood videos by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext_understood':' understood ',
                        'hovertext_misunderstood':' do <b>not</b> understood '
                    }
        df = self.DATASET
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([df.iloc[j,0]+legend['hovertext_misunderstood']+df.columns[i] if values[j]==0 else df.iloc[j,0]+legend['hovertext_understood']+df.columns[i] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Videos
                        x=df.iloc[:,0], #Students
                        colorscale=[[0, 'rgb(255,126,24)'], [1, 'rgb(0,0,255)']],
                        hovertext = hovervalue,
                        hoverinfo='text',
                        showscale = False
                    )
        
        layout = Layout(
                title = legend['title'],                
                # autosize=False,
                # width=950,
                # height=350,
                hovermode = "closest",
                xaxis=dict(
                    title = legend['xaxis'],
                    titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                ),                
                yaxis=dict(
                    title = legend['yaxis'],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    type="category",                    
                    tick0=0,
                    dtick=1,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',                    
                ),
                margin = dict(
                    b=150,
                )
            )

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@21',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@21","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_22(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendederam", 2:"Não<br>entenderam"},
                    'hovertext_understood':' estudantes entenderam o ',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam o '
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and do <b>not</b> understood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }
        df = self._df_sum_feedback.iloc[:,0:3]
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([str(values[j])+legend['hovertext_understood']+df.iloc[j,0] if i==1 else str(values[j])+legend['hovertext_misunderstood']+df.iloc[j,0] for j in range(len(values))])
        
        trace = []
        trace.append(Heatmap(z=z,
                        y=[legend["columns"][i] for i in range (1,len(df.columns))],
                        x=df.iloc[:,0], #Students
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        hovertext = hovervalue,
                        hoverinfo='text',
                        showscale = True
                    ))

        layout = Layout(
                title = legend['title'],                
                # autosize=False,
                # width=950,
                # height=350,
                hovermode = "closest",
                xaxis=dict(
                    title = legend['xaxis'],
                    titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                ),                
                yaxis=dict(
                    title = legend['yaxis'],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    type="category",                    
                    tick0=0,
                    dtick=1,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',                    
                ),
                margin = dict(
                    l=125,
                    b=150,
                )
            )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@22',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@22","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_23(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendederam", 2:"Não<br>entenderam"},
                    'hovertext_understood':' estudantes entenderam o ',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam o '
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and do <b>not</b> understood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }
        df = self._df_sum_feedback.iloc[:,0:3]
        z = []
        hovervalue=[]
        max_value = 0
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([str(values[j])+legend['hovertext_understood']+df.iloc[j,0] if i==1 else str(values[j])+legend['hovertext_misunderstood']+df.iloc[j,0] for j in range(len(values))])            
            max_local = max(values)
            max_value = max(max_local,max_value)
        
        trace = []
        trace.append(Heatmap(z=z,
                        y=[legend["columns"][i] for i in range (1,len(df.columns))],
                        x=df.iloc[:,0], #Students
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        hovertext = hovervalue,
                        hoverinfo='text',
                        showscale = True
                    ))

        annotations=[]
        for i in range(1,len(df.columns)):
            for j in range(0,len(df)):
                color = 'rgb(0,0,0)'
                if df.iloc[j,i] > max_value/2:
                    color = 'rgb(255,255,255)'
                annotations.append({
                    "text":str(df.iloc[j,i]),
                    "y":legend["columns"][i],
                    "x":df.iloc[j,0],
                    "xref":'x1', 
                    "yref":'y1',
                    "showarrow":False,
                    "font":{
                        # family='Courier New, monospace',
                        # size=16,
                        "color":color
                    }
                })

        layout = Layout(
                title = legend['title'],                
                # autosize=False,
                # width=950,
                # height=350,
                hovermode = "closest",
                xaxis=dict(
                    title = legend['xaxis'],
                    titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                ),                
                yaxis=dict(
                    title = legend['yaxis'],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    type="category",                    
                    tick0=0,
                    dtick=1,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',                    
                ),
                margin = dict(
                    l=125,
                    b=150,
                ),
                annotations = annotations
            )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@23',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@23","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Grouped Bar
    def graph_24(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }
        
        df = self._df_sum_feedback
        
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])): 
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    name=legend['columns'][i],
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
            ))            

        data = trace
        layout = Layout(
                title=legend["title"],
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=5,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@24',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@24","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_25(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }
        
        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[1],self._df_sum_feedback.columns[0]])
        
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])): 
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=legend['columns'][i]
            ))            

        data = trace
        layout = Layout(
                title=legend["title"],
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=5,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@25',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@25","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_26(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }
        
        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[2],self._df_sum_feedback.columns[0]])
        
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])): 
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=legend['columns'][i]
            ))            

        data = trace
        layout = Layout(
                title=legend["title"],
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=5,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@26',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@26","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Stacked Bar
    def graph_27(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }

        df = self._df_sum_feedback
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):         
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=legend['columns'][i]
            ))

        data = trace
        layout = Layout(
                title=legend["title"],
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                barmode='stack',
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=5,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@27',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@27","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_28(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }

        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[1],self._df_sum_feedback.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):         
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=legend['columns'][i]
            ))

        data = trace
        layout = Layout(
                title=legend["title"],
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                barmode='stack',
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=5,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@28',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@28","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_29(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }

        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[2],self._df_sum_feedback.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):         
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',                    
                    name=legend['columns'][i]
            ))

        data = trace
        layout = Layout(
                title=legend["title"],
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                barmode='stack',
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=5,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@29',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@29","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_30(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }

        df = self._df_sum_feedback
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=legend['columns'][i],
                    orientation = 'h'
            ))

        data = trace
        layout = Layout(
                title=legend["title"],
                barmode='stack',
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=1,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@30',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@30","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_31(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }

        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[1],self._df_sum_feedback.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=legend['columns'][i],
                    orientation = 'h'
            ))

        data = trace
        layout = Layout(
                title=legend["title"],
                barmode='stack',
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=1,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@31',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@31","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_32(self):
        legend = {"title":"Número de estudantes que entenderam e <b>não</b> entenderam os vídeos",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Entendidos", 2:"Não<br>entendidos"},
                    'hovertext_understood':' estudantes entenderam',
                    'hovertext_misunderstood':' estudantes <b>não</b> entenderam'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who understood and misunderstood the videos",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Understood", 2:"Misunderstood"},
                        'hovertext_understood':' students understood ',
                        'hovertext_misunderstood':' students do <b>not</b> understood '
                    }

        df = self._df_sum_feedback.sort_values(by=[self._df_sum_feedback.columns[2],self._df_sum_feedback.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_understood'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_misunderstood'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=legend['columns'][i],
                    orientation = 'h'
            ))

        data = trace
        layout = Layout(
                title=legend["title"],
                barmode='stack',
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                yaxis=dict(
                    title = legend["yaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                    showticklabels=True,
                    tick0=0,
                    dtick=1,
        #             ticklen=4,
        #             tickwidth=4,
                    exponentformat='e',
                    showexponent='all',
                    gridcolor='#bdbdbd',
        #             range=[0, 4.1]
                )
            )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V010@32',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V010@32","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

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
        elif id == 25:
            return self.graph_25()
        elif id == 26:
            return self.graph_26()
        elif id == 27:
            return self.graph_27()
        elif id == 28:
            return self.graph_28()
        elif id == 29:
            return self.graph_29()
        elif id == 30:
            return self.graph_30()
        elif id == 31:
            return self.graph_31()
        elif id == 32:
            return self.graph_32()
        else:
            print("V010@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V010_'+str(id)+'.pkl'
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
        
        file_name = 'V010_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)
        f = open(file_path,'wb')
        pickle.dump(self.get_chart(id),f)
        f.close()

        self._type_result = aux_type_result

    def print_all_graphs(self,language="pt"):
        self._language = language
        self.graph_01() # Table
        self.graph_02()
        self.graph_03() #Bar
        self.graph_04() 
        self.graph_05() 
        self.graph_06()
        self.graph_07() 
        self.graph_08()
        self.graph_09() 
        self.graph_10()
        self.graph_11() #Lollipop
        self.graph_12() 
        self.graph_13()
        self.graph_14()
        self.graph_15() #Scatter
        self.graph_16() 
        self.graph_17()
        self.graph_18()
        self.graph_19() #Heatmap
        self.graph_20()
        self.graph_21()
        self.graph_22()
        self.graph_23()
        self.graph_24() #Grouped Bar
        self.graph_25()
        self.graph_26() 
        self.graph_27() #Stacked Bar
        self.graph_28()
        self.graph_29()
        self.graph_30()
        self.graph_31()
        self.graph_32()
  
# instance = V010()
# instance.generate_dataset(number_students=35, number_video=10)
# instance.print_all_graphs("pt")
# instance.print_all_graphs("en")