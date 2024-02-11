import dash
import dash_core_components as dcc
import dash_html_components as html

import os
import pandas as pd
import numpy as np

import pickle
import json

from plotly.utils import PlotlyJSONEncoder
from plotly.graph_objs import Figure, Layout, Bar, Table, Heatmap, Scatter
from plotly.offline import init_notebook_mode, iplot

init_notebook_mode(connected=True) # initiate notebook for offline plot

class V001:
    NUMBER_STUDENTS = 20
    NUMBER_ASSIGNS = 4
    DATASET = pd.DataFrame()
    
    _language = "pt"
    _type_result="jupyter-notebook"
    _assign_name = []
    _students = pd.DataFrame()
    _assigns = pd.DataFrame()
    _map = pd.DataFrame()
    _preprocessed_folder = os.path.join('Preprocessed')

    def __init__(self, language="pt", type_result = "jupyter-notebook"):
        self._language = language
        self._type_result = type_result
        self.load_map_view()

    def generate_dataset(self, number_students = 20, number_assigns = 4, rand_names = []):
        self.NUMBER_STUDENTS = number_students
        self.NUMBER_ASSIGNS = number_assigns

        if (self._language == "pt"):
            assign_label = "Atividade "
            students_label = "Estudantes"
        else:
            assign_label = "Assign "
            students_label = "Students"

        self._assign_name = [assign_label+str(i+1) for i in range (0, self.NUMBER_ASSIGNS)]
        
        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)
        
        self.DATASET = pd.DataFrame(columns=self._assign_name)
        for i in range(0,self.NUMBER_STUDENTS):
            self.DATASET.loc[i] = [np.random.randint(0,2) for n in range(len(self.DATASET.columns))]
        
        self.DATASET.insert(0,students_label,rand_names)

        self.get_students_frame()
        self.get_assigns_frame()

    def sum_assigns_done(self,row):
        lst = self.DATASET.columns[1:].tolist()
        sum_value = 0
        for i in range(len(lst)):
            sum_value += row[lst[i]]

        return sum_value

    def sum_assigns_undone(self,row):
        lst = self.DATASET.columns[1:].tolist()
        sum_value = 0
        for i in range(len(lst)):
            sum_value += row[lst[i]]

        return len(lst)-sum_value

    def get_student(self, row):
        return row[self.DATASET.columns[0]]

    def get_students_frame(self):
        self._students = pd.DataFrame(columns=["Name","Total_Done","Total_Undone"])
        self._students["Total_Done"] = self.DATASET.apply(self.sum_assigns_done, axis=1)
        self._students["Total_Undone"] = self.DATASET.apply(self.sum_assigns_undone, axis=1)
        self._students["Name"] = self.DATASET.apply(self.get_student, axis=1)
        # print (self._students)

    def get_assigns_frame(self):
        self._assigns = pd.DataFrame(columns=["Name","Total_Done","Total_Undone"])
        for i in range (0, len(self.DATASET.columns[1:])):
            self._assigns.loc[i,"Name"] = self.DATASET.columns[i+1]
            self._assigns.loc[i,"Total_Done"] = self.DATASET[self.DATASET.columns[i+1]].sum()
            self._assigns.loc[i,"Total_Undone"] = len(self.DATASET) - self._assigns.loc[i,"Total_Done"]
        
    # Table presenting raw data
    def graph_01(self):
        legend = {"title":"Tarefas feitas por alunos"}
        if (self._language == "en"):
            legend = {"title":"Assigns completed by students"}

        df = self.DATASET
        
        trace = [Table(
            header=dict(
                values=list(df.columns)+["Total"],
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[df[i].tolist() for i in df.columns]+[self._students["Total_Done"].tolist()],
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
                    id='V001@1',
                    figure={"data": data}
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    # Barchart number of assign completed for each student
    def graph_02(self):
        legend = {"title":"Número de tarefas feitas por alunos",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    'hovertext':' tarefa(s) feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        'hovertext':' assign(s) completed'
                    }

        df = self._students.iloc[:,[0,1]]
        trace = [Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
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
                # tick0=0,
                # dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                    id='V001@2',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_03(self):
        legend = {"title":"Número de tarefas feitas por alunos",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    'hovertext':' tarefa(s) feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        'hovertext':' assign(s) completed'
                    }
                    
        df = self._students.sort_values(by=["Total_Done","Name"]).iloc[:,[0,1]]        
        trace = [Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
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
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                    id='V001@3',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_04(self):
        legend = {"title":"Número de tarefas feitas por alunos",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    'hovertext':' tarefa(s) feita(s)'
                    }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed by students",
                    "xaxis":"Number of assigns",
                    "yaxis":"",
                    'hovertext':' assign(s) completed'
                    }
        df = self._students.iloc[:,[0,1]]
        trace = [Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            orientation = 'h',
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
                tick0=0,
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                    id='V001@4',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_05(self):
        legend = {"title":"Número de tarefas feitas por alunos",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    'hovertext':' tarefa(s) feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        'hovertext':' assign(s) completed'
                    }
        df = self._students.sort_values(by=["Total_Done","Name"]).iloc[:,[0,1]]
        trace = [Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            orientation = 'h',
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
                tick0=0,
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":
            return dcc.Graph(
                    id='V001@5',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@5","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    # Barchart number of assign not completed for each student
    def graph_06(self):
        legend = {"title":"Número de tarefas <b>não</b> feitas por alunos",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    'hovertext':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        'hovertext':' assign(s) <b>not</b> completed'
                    }

        df = self._students.iloc[:,[0,2]]
        trace = [Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
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
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                    id='V001@6',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@6","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_07(self):
        legend = {"title":"Quantidade de tarefas <b>não</b> feitas por alunos",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    'hovertext':' tarefa(s) <b>não</b> feita(s)'
                    }
        if (self._language == "en"):
            legend = {"title":"Number of assigns <b>not</b> completed by students",
                    "xaxis":"",
                    "yaxis":"Number of assigns",
                    'hovertext':' assign(s) <b>not</b> completed'
                    }
                    
        df = self._students.sort_values(by=["Total_Undone","Name"]).iloc[:,[0,2]]        
        trace = [Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
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
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                    id='V001@7',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@7","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_08(self):
        legend = {"title":"Número de tarefas <b>não</b> feitas por alunos",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    'hovertext':' tarefa(s) <b>não</b> feita(s)'
                    }
        if (self._language == "en"):
            legend = {"title":"Number of assigns <b>not</b> completed by students",
                    "xaxis":"Number of assigns",
                    "yaxis":"",
                    'hovertext':' assign(s) <b>not</b> completed'
                    }
        df = self._students.iloc[:,[0,2]]
        trace = [Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
            hoverinfo='text',
            orientation = 'h',
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
                tick0=0,
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                    id='V001@8',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@8","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_09(self):
        legend = {"title":"Quantidade de tarefas <b>não</b> feitas por alunos",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    'hovertext':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns <b>not</b> completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        'hovertext':' assign(s) <b>not</b> completed'
                    }
        df = self._students.sort_values(by=["Total_Undone","Name"]).iloc[:,[0,2]]
        trace = [Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            orientation = 'h',
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
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
                tick0=0,
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                    id='V001@9',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@9","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    # Lollipop number of assign completed for each student
    def graph_10(self):
        legend = {"title":"Número de tarefas feitas por alunos",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    "text_s":"atividades",
                    "text_p":"atividades",
                    'hovertext':' tarefa(s) feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        "text_s":"assign",
                        "text_p":"assigns",
                        'hovertext':' assign(s) completed'
                    }
        df = self._students.iloc[:,[0,1]]
        trace = []
        trace.append(
            Bar(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                width=[0.07]*self.NUMBER_STUDENTS,
                orientation = 'h',
                name="",
                text="",                
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',                        
                    )
            )
        )
        
        for i in range(1, len(self.DATASET.columns)):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df.Name.loc[df["Total_Done"]==i]),
                    y=df.Name.loc[df["Total_Done"]==i].values.tolist(),
                    mode='markers',
                    name = "",
                    text=text*len(df.Name.loc[df["Total_Done"]==i]),
                    hovertext = '<b>'+df.Name.loc[df["Total_Done"]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=0
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
                    id='V001@10',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@10","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_11(self):
        legend = {"title":"Quantidade de tarefas feitas por alunos",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    "text_s":"atividades",
                    "text_p":"atividades",
                    'hovertext':' tarefa(s) feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        "text_s":"assign",
                        "text_p":"assigns",
                        'hovertext':' assign(s) completed'
                    }
        df = self._students.sort_values(by=["Total_Done","Name"]).iloc[:,[0,1]]
        trace = []
        trace.append(
            Bar(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                width=[0.07]*self.NUMBER_STUDENTS,
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',                        
                    )
            )
        )
        
        for i in range(1, len(self.DATASET.columns)):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df.Name.loc[df["Total_Done"]==i]),
                    # x=[3]*20, #student
                    y=df.Name.loc[df["Total_Done"]==i].values.tolist(),
                    mode='markers',
                    name = "",                    
                    text=text*len(df.Name.loc[df["Total_Done"]==i]),
                    hovertext = '<b>'+df.Name.loc[df["Total_Done"]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=0
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
                id='V001@11',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@11","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
        
    def graph_12(self):
        legend = {"title":"Número de tarefas <b>não</b> feitas por alunos",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    "text_s":"atividades",
                    "text_p":"atividades",
                    'hovertext':' tarefas(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns <b>not</b> completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        "text_s":"assign",
                        "text_p":"assigns",
                        'hovertext':' assign(s) <b>not</b> completed'
                    }
        df = self._students.iloc[:,[0,2]]
        trace = []
        trace.append(
            Bar(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                width=[0.07]*self.NUMBER_STUDENTS,
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',                        
                    )
            )
        )
        
        for i in range(1, len(self.DATASET.columns)):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df.Name.loc[df["Total_Undone"]==i]),
                    # x=[3]*20, #student
                    y=df.Name.loc[df["Total_Undone"]==i].values.tolist(),
                    mode='markers',
                    name = "",                    
                    text=text*len(df.Name.loc[df["Total_Undone"]==i]),
                    hovertext = '<b>'+df.Name.loc[df["Total_Undone"]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(255,126,24)',
                        line=dict(
                            width=0
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
                id='V001@12',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@12","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_13(self):
        legend = {"title":"Quantidade de tarefas <b>não</b> feitas por alunos",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    "text_s":"atividades",
                    "text_p":"atividades",
                    'hovertext':' tarefas(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns <b>not</b> completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        "text_s":"assign",
                        "text_p":"assigns",
                        'hovertext':' assign(s) <b>not</b> completed'
                    }
        df = self._students.sort_values(by=["Total_Undone","Name"]).iloc[:,[0,2]]
        trace = []
        trace.append(
            Bar(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                width=[0.07]*self.NUMBER_STUDENTS,
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',                        
                    )
            )
        )
        
        for i in range(1, len(self.DATASET.columns)):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df.Name.loc[df["Total_Undone"]==i]),
                    # x=[3]*20, #student
                    y=df.Name.loc[df["Total_Undone"]==i].values.tolist(),
                    mode='markers',
                    name = "",                    
                    text=text*len(df.Name.loc[df["Total_Undone"]==i]),
                    hovertext = '<b>'+df.Name.loc[df["Total_Undone"]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(255,126,24)',
                        line=dict(
                            width=0
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
                id='V001@13',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@13","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Barchart number of students that have completed each assign
    def graph_14(self):
        legend = {"title":"Quantidade de estudantes que fizeram as tarefas",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    'hovertext':' estudante(s) fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students that completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        'hovertext':' student(s) completed'
                    }
        df = self._assigns.iloc[:,[0,1]]
        trace = [Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
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
                dtick=1,
                # ticklen=4,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 13]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@14',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@14","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_15(self):
        legend = {"title":"Quantidade de alunos que fizeram as tarefas",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    'hovertext':' estudante(s) fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students that completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        'hovertext':' student(s) completed'
                    }
        df = self._assigns.sort_values(by=["Total_Done","Name"]).iloc[:,[0,1]]
        trace = [Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
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
                dtick=1,
                # ticklen=4,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 13]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@15',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@15","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
  
    def graph_16(self):
        legend = {"title":"Quantidade de estudantes que fizeram as tarefas",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    'hovertext':' estudante(s) fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students that completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        'hovertext':' student(s) completed'
                    }
        df = self._assigns.iloc[:,[0,1]]
        trace = [Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            orientation = 'h',
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
                tick0=0,
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@16',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@16","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_17(self):
        legend = {"title":"Quantidade de estudantes que fizeram as tarefas",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    'hovertext':' estudante(s) fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students that completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        'hovertext':' student(s) completed'
                    }
        df = self._assigns.sort_values(by=["Total_Done","Name"]).iloc[:,[0,1]]
        trace = [Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            orientation = 'h',
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
                tick0=0,
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@17',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@17","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_18(self):
        legend = {"title":"Quantidade de estudantes <b>não</b> que fizeram as tarefas",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    'hovertext':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        'hovertext':' student(s) <b>not</b> completed'
                    }
        df = self._assigns.iloc[:,[0,2]]
        trace = [Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
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
                dtick=1,
                # ticklen=4,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 13]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@18',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@18","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_19(self):
        legend = {"title":"Quantidade de alunos que <b>não</b> fizeram as tarefas",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    'hovertext':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who <b>não</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        'hovertext':' student(s) <b>not</b> completed'
                    }
        df = self._assigns.sort_values(by=["Total_Undone","Name"]).iloc[:,[0,2]]
        trace = [Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
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
                dtick=1,
                # ticklen=4,
                # tickwidth=4,
                exponentformat='e',
                showexponent='all',
                gridcolor='#bdbdbd',
                # range=[0, 13]
            )
        )

        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@19',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@19","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
  
    def graph_20(self):
        legend = {"title":"Quantidade de estudantes que <b>não</b> fizeram as tarefas",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    'hovertext':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who <b>not</b> completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        'hovertext':' student(s) <b>not</b> completed'
                    }
        df = self._assigns.iloc[:,[0,2]]
        trace = [Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            orientation = 'h',
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
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
                tick0=0,
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@20',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@20","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_21(self):
        legend = {"title":"Quantidade de estudantes que <b>não</b> fizeram as tarefas",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    'hovertext':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who <b>not</b> completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        'hovertext':' student(s) <b>not</b> completed'
                    }
        df = self._assigns.sort_values(by=["Total_Undone","Name"]).iloc[:,[0,2]]
        trace = [Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,            
            orientation = 'h',
            hovertext = ['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,1])+legend['hovertext'] for i in range(len(df.iloc[:,1].values))],
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
                tick0=0,
                dtick=1,
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
            iplot(fig, filename='Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@21',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@21","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Lollipop number of students that have completed each assign
    def graph_22(self):
        legend = {"title":"Quantidade de estudantes que fizeram as tarefas",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "text_s":"estudante",
                    "text_p":"estudantes",
                    'hovertext':' estudante(s) fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "text_s":"student",
                        "text_p":"students",
                        'hovertext':' student(s) completed'
                    }
        df = self._assigns.iloc[:,[0,1]]

        trace = []
        trace.append(
            Bar(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                width=[0.04]*len(df.iloc[:,1].values),
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',
                        # line=dict(
                        #     color = 'lightgray',
                        #     width=2
                        # )
                    )
            )
        )
        
        for i in range(0, max(df.Total_Done.tolist())+1):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df.Name.loc[df["Total_Done"]==i]),
                    y=df.Name.loc[df["Total_Done"]==i].values.tolist(),
                    hovertext = '<b>'+df.Name.loc[df["Total_Done"]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    mode='markers',
                    name = "",                    
                    text=text*len(df.Name.loc[df["Total_Done"]==i]),                    
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=0
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
                id='V001@22',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@22","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_23(self):
        legend = {"title":"Quantidade de estudantes que fizeram as tarefas",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "text_s":"estudante",
                    "text_p":"estudantes",
                    'hovertext':' estudante(s) fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "text_s":"student",
                        "text_p":"students",
                        'hovertext':' student(s) completed'
                    }
        df = self._assigns.sort_values(by=["Total_Done","Name"]).iloc[:,[0,1]]

        trace = []
        trace.append(
            Bar(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                width=[0.04]*len(df.iloc[:,1].values),
                orientation = 'h',
                name="",
                text="",
                hoverinfo='none',
                marker=dict(
                        color = 'lightgray',
                        # line=dict(
                        #     color = 'lightgray',
                        #     width=2
                        # )
                    )
            )
        )
        
        for i in range(0, max(df.Total_Done.tolist())+1):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df.Name.loc[df["Total_Done"]==i]),
                    y=df.Name.loc[df["Total_Done"]==i].values.tolist(),
                    hovertext = '<b>'+df.Name.loc[df["Total_Done"]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    mode='markers',
                    name = "",                    
                    text=text*len(df.Name.loc[df["Total_Done"]==i]),                    
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=0
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
                id='V001@23',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@23","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_24(self):
        legend = {"title":"Quantidade de estudantes que <b>não</b> fizeram as tarefas",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "text_s":"estudante",
                    "text_p":"estudantes",
                    'hovertext':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who <b>not</b> completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "text_s":"student",
                        "text_p":"students",
                        'hovertext':' student(s) <b>not</b> completed'
                    }
        df = self._assigns.iloc[:,[0,2]]
        
        trace = []
        trace.append(
            Bar(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                hoverinfo='none',
                width=[0.04]*len(df.iloc[:,1].values),
                orientation = 'h',
                name="",
                text="",
                marker=dict(
                        color = 'lightgray',
                        # line=dict(
                        #     color = 'lightgray',
                        #     width=2
                        # )
                    )
            )
        )
        
        for i in range(0, max(df.Total_Undone.tolist())+1):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df.Name.loc[df["Total_Undone"]==i]),
                    y=df.Name.loc[df["Total_Undone"]==i].values.tolist(),
                    hovertext = '<b>'+df.Name.loc[df["Total_Undone"]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    mode='markers',
                    name = "",                    
                    text=text*len(df.Name.loc[df["Total_Undone"]==i]),                    
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(255,126,24)',
                        line=dict(
                            width=0
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
                id='V001@24',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@24","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_25(self):
        legend = {"title":"Quantidade de estudantes <b>não</b> que fizeram as tarefas",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "text_s":"estudante",
                    "text_p":"estudantes",
                    'hovertext':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who <b>not</b> completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "text_s":"student",
                        "text_p":"students",
                        'hovertext':' student(s) <b>not</b> completed'
                    }
        df = self._assigns.sort_values(by=["Total_Undone","Name"]).iloc[:,[0,2]]

        trace = []
        trace.append(
            Bar(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                hoverinfo='none',
                width=[0.04]*len(df.iloc[:,1].values),
                orientation = 'h',
                name="",
                text="",
                marker=dict(
                        color = 'lightgray',
                        # line=dict(
                        #     color = 'lightgray',
                        #     width=2
                        # )
                    )
            )
        )
        
        for i in range(0, max(df.Total_Undone.tolist())+1):
            text=str(i)+" "+legend['text_p'],
            if i==1:
                text=str(i)+" "+legend['text_s'],

            trace.append(
                Scatter(
                    x=[i]*len(df.Name.loc[df["Total_Undone"]==i]),
                    y=df.Name.loc[df["Total_Undone"]==i].values.tolist(),
                    hovertext = '<b>'+df.Name.loc[df["Total_Undone"]==i]+'</b><br>'+str(i)+legend['hovertext'],
                    hoverinfo='text',
                    mode='markers',
                    name = "",                    
                    text=text*len(df.Name.loc[df["Total_Undone"]==i]),                    
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        color = 'rgb(255,126,24)',
                        line=dict(
                            width=0
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
                id='V001@25',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@25","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    # Scatter assigns completed by each students
    def graph_26(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Atividades feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' fez '
                }
        if (self._language == "en"):
            legend = {"title":"Assigns completed by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' completed '
                    }
        df = self.DATASET

        sizeref = 0.01
        # print (sizeref)

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
                        # size=df.iloc[:,i].values.tolist(),
                        size=df.iloc[i,1:].values.tolist(),
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=0
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
                id='V001@26',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@26","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_27(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Atividades <b>não</b> feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' <b>não</b> fez '
                }
        if (self._language == "en"):
            legend = {"title":"Assigns <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' <b>not</b> completed '
                    }
        df = self.DATASET

        sizeref = 0.01
        # print (sizeref)

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
                    hovertext = ['<b>'+df.iloc[i,0]+'</b>'+legend['hovertext']+df.columns[j+1] if df.iloc[i,j+1] == 0 else '' for j in range(len(df.columns[1:]))],
                    hoverinfo='text',
                    # name=df.iloc[i,0], #each student name
                    name=df.iloc[i,0], #student name
                    # text = df.iloc[i,1:].values.tolist(),
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        # size=df.iloc[:,i].values.tolist(),
                        size=values,
                        color = 'rgb(255,126,24)',
                        line=dict(
                            width=0
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
                id='V001@27',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@27","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_28(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Atividades feitas e <b>não</b> feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext_done':' fez ',
                    'hovertext_undone':' <b>não</b> fez '
                }
        if (self._language == "en"):
            legend = {"title":"Assigns completed and <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext_done':' completed ',
                        'hovertext_undone':' <b>not</b> completed '
                    }
        df = self.DATASET

        sizeref = 0.01
        # print (sizeref)

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
                        # size=df.iloc[:,i].values.tolist(),
                        size=df.iloc[i,1:].values.tolist(),
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=0
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
                    # name=df.iloc[i,0], #each student name
                    name=df.iloc[i,0], #student name
                    # text = df.iloc[i,1:].values.tolist(),
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        # size=df.iloc[:,i].values.tolist(),
                        size=values,
                        color = 'rgb(255,126,24)',
                        line=dict(
                            width=0
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
                id='V001@28',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@28","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_29(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' fez ',
                    'hovertext_undone':' <b>não</b> fez '
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed student",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not completed"},
                        'hovertext_done':' completed ',
                        'hovertext_undone':' <b>not</b> completed '
                    }
        df = self._students.iloc[:,0:3]
        sizeref = 0.05
        
        trace = []
        for i in range(0, len(df)):
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns),
                    y=[legend["columns"][i] for i in range (1,2)],
                    mode='markers',                    
                    name=df.iloc[i,0],
                    text = df.iloc[i,1].tolist(),
                    hovertext = '<b>'+df.iloc[i,0]+'</b>'+legend['hovertext_done']+str(df.iloc[i,1]),
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,1]*3,
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=0
                        )
                    )
                )
            )
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns),
                    y=[legend["columns"][i] for i in range (2,3)],
                    mode='markers',                    
                    name=df.iloc[i,0],
                    text = df.iloc[i,2].tolist(),
                    hovertext = '<b>'+df.iloc[i,0]+'</b>'+legend['hovertext_undone']+str(df.iloc[i,2]),
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,2]*3,
                        color='rgb(255,126,24)',
                        line=dict(
                            width=0
                        )
                    )
                )
            )

        layout = Layout(
            title=legend['title'],
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
                id='V001@29',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@29","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_30(self):
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        legend = {"title":"Número de estudantes que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' estudante(s) fez/fizeram ',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram '
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not completed"},
                        'hovertext_done':' student(s) completed ',
                        'hovertext_undone':' student(s) <b>not</b> completed '
                    }
        df = self._assigns.iloc[:,0:3]
        sizeref = 0.05
        
        trace = []
        for i in range(0, len(df)):                    
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns),
                    y=[legend["columns"][i] for i in range (1,2)],
                    mode='markers',                    
                    name=df.iloc[i,0],
                    hovertext = str(df.iloc[i,1])+legend['hovertext_done']+'<b>'+df.iloc[i,0]+'</b>',
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,1]*2,
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=0
                        )
                    )
                )
            )
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns),
                    y=[legend["columns"][i] for i in range (2,3)],
                    mode='markers',                    
                    name=df.iloc[i,0],
                    hovertext = str(df.iloc[i,2])+legend['hovertext_undone']+'<b>'+df.iloc[i,0]+'</b>',
                    hoverinfo='text',
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,2]*2,
                        color='rgb(255,126,24)',
                        line=dict(
                            width=0
                        )
                    )
                )
            )

        layout = Layout(
            title=legend['title'],
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
                id='V001@30',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@30","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Heatmap assigns completed by each students
    def graph_31(self):
        legend = {"title":"Atividades feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext_done':' fez ',
                    'hovertext_undone':' <b>não</b> fez '
                }
        if (self._language == "en"):
            legend = {"title":"Assigns completed by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext_done':' completed ',
                        'hovertext_undone':' <b>not</b> completed '
                    }
        df = self.DATASET
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([df.iloc[j,0]+legend['hovertext_undone']+df.columns[i] if values[j]==0 else df.iloc[j,0]+legend['hovertext_done']+df.columns[i] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Assigns
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
                id='V001@31',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@31","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_32(self):
        legend = {"title":"Atividades <b>não</b> feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext_done':' fez ',
                    'hovertext_undone':' <b>não</b> fez '
                }
        if (self._language == "en"):
            legend = {"title":"Assigns <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext_done':' completed ',
                        'hovertext_undone':' <b>not</b> completed '
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
            hovervalue.append([df.iloc[j,0]+legend['hovertext_done']+df.columns[i] if values[j]==0 else df.iloc[j,0]+legend['hovertext_undone']+df.columns[i] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Assigns
                        x=df.iloc[:,0], #Students
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(255,126,24)']],
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
                id='V001@32',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@32","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_33(self):
        legend = {"title":"Atividades feitas e <b>não</b> feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext_done':' fez ',
                    'hovertext_undone':' <b>não</b> fez '
                }
        if (self._language == "en"):
            legend = {"title":"Assigns completed and <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext_done':' completed ',
                        'hovertext_undone':' <b>not</b> completed '
                    }
        df = self.DATASET
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([df.iloc[j,0]+legend['hovertext_undone']+df.columns[i] if values[j]==0 else df.iloc[j,0]+legend['hovertext_done']+df.columns[i] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Assigns
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
                id='V001@33',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@33","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_34(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' fez ',
                    'hovertext_undone':' <b>não</b> fez '
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed student",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not completed"},
                        'hovertext_done':' completed ',
                        'hovertext_undone':' <b>not</b> completed '
                    }
        df = self._students.iloc[:,0:3]
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([df.iloc[j,0]+legend['hovertext_done']+str(values[j]) if i==1 else df.iloc[j,0]+legend['hovertext_undone']+str(values[j]) for j in range(len(values))])
        
        
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
                    b=150,
                )
            )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@34',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@34","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_35(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' fez ',
                    'hovertext_undone':' <b>não</b> fez '
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed student",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not completed"},
                        'hovertext_done':' completed ',
                        'hovertext_undone':' <b>not</b> completed '
                    }
        df = self._students.iloc[:,0:3]
        z = []
        hovervalue=[]
        max_value = 0
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([df.iloc[j,0]+legend['hovertext_done']+str(values[j]) if i==1 else df.iloc[j,0]+legend['hovertext_undone']+str(values[j]) for j in range(len(values))])
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
                id='V001@35',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@35","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_36(self):
        legend = {"title":"Número de estudantes que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' estudante(s) fez/fizeram ',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram '
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not completed"},
                        'hovertext_done':' student(s) completed ',
                        'hovertext_undone':' student(s) <b>not</b> completed '
                    }
        df = self._assigns.iloc[:,0:3]
        hovervalue=[]
        z = []
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([str(values[j])+legend['hovertext_done']+df.iloc[j,0] if i==1 else str(values[j])+legend['hovertext_undone']+df.iloc[j,0] for j in range(len(values))])

        trace = []
        trace.append(Heatmap(z=z,
                        y=[legend["columns"][i] for i in range (1,len(df.columns))],
                        x=df.iloc[:,0], #Students
                        hovertext = hovervalue,
                        hoverinfo='text',
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
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
                    b=150,
                )
            )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@36',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@36","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_37(self):
        legend = {"title":"Número de estudantes que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' estudante(s) fez/fizeram ',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram '
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not completed"},
                        'hovertext_done':' student(s) completed ',
                        'hovertext_undone':' student(s) <b>not</b> completed '
                    }
        df = self._assigns.iloc[:,0:3]
        z = []
        hovervalue=[]
        max_value = 0
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append([str(values[j])+legend['hovertext_done']+df.iloc[j,0] if i==1 else str(values[j])+legend['hovertext_undone']+df.iloc[j,0] for j in range(len(values))])
            max_local = max(df.iloc[:,i].values.tolist())
            max_value = max(max_local,max_value)
        
        trace = []
        trace.append(Heatmap(z=z,
                        y=[legend["columns"][i] for i in range (1,len(df.columns))],
                        x=df.iloc[:,0], #Students
                        hovertext = hovervalue,
                        hoverinfo='text',
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
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
                id='V001@37',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@37","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Grouped Bar
    def graph_38(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }
        
        df = self._students
        
        trace = []
        for i in range(1,len(df.columns)): 
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Grouped-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@38',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@38","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_39(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }
        
        df = self._students.sort_values(by=["Total_Done","Name"])
        
        trace = []
        for i in range(1,len(df.columns)): 
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Grouped-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@39',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@39","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_40(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }
        
        df = self._students.sort_values(by=["Total_Undone","Name"])
        
        trace = []
        for i in range(1,len(df.columns)): 
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Grouped-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@40',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@40","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_41(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns
        
        trace = []
        for i in range(1,len(df.columns)): 
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Grouped-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@41',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@41","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_42(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns.sort_values(by=["Total_Done","Name"])
        
        trace = []
        for i in range(1,len(df.columns)): 
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Grouped-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@42',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@42","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_43(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns.sort_values(by=["Total_Undone","Name"])
        
        trace = []
        for i in range(1,len(df.columns)): 
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Grouped-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@43',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@43","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Stacked Bar
    def graph_44(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }

        df = self._students
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@44',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@44","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_45(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }

        df = self._students.sort_values(by=["Total_Done","Name"])
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@45',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@45","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_46(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"",
                    "yaxis":"Número de atividades",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"",
                        "yaxis":"Number of assigns",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }

        df = self._students.sort_values(by=["Total_Undone","Name"])
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    # name=df.columns[i]
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@46',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@46","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_47(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }

        df = self._students
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df.Name.values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@47',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@47","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_48(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }

        df = self._students.sort_values(by=["Total_Done","Name"])
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df.Name.values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@48',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@48","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_49(self):
        legend = {"title":"Número de atividades feitas e <b>não</b> feitas por aluno",
                    "xaxis":"Número de atividades",
                    "yaxis":"",
                    "columns":{1:"Feitas", 2:"Não<br>feitas"},
                    'hovertext_done':' tarefa(s) feita(s)',
                    'hovertext_undone':' tarefa(s) <b>não</b> feita(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of assigns completed and <b>not</b> completed by students",
                        "xaxis":"Number of assigns",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' assign(s) completed',
                        'hovertext_undone':' assign(s) <b>not</b> completed'
                    }

        df = self._students.sort_values(by=["Total_Undone","Name"])
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df.Name.values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@49',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@49","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_50(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@50',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@50","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_51(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns.sort_values(by=["Total_Done","Name"])
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@51',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@51","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_52(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"",
                    "yaxis":"Número de estudantes",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"",
                        "yaxis":"Number of students",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns.sort_values(by=["Total_Undone","Name"])
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(
                    x=df.Name.values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@52',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@52","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_53(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df.Name.values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@53',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@53","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_54(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns.sort_values(by=["Total_Done","Name"])
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df.Name.values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@54',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@54","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_55(self):
        legend = {"title":"Número de alunos que fizeram e <b>não</b> fizeram as atividades",
                    "xaxis":"Número de estudantes",
                    "yaxis":"",
                    "columns":{1:"Fizeram", 2:"Não<br>fizeram"},
                    'hovertext_done':' estudante(s) fez/fizeram',
                    'hovertext_undone':' estudante(s) <b>não</b> fez/fizeram'
                }
        if (self._language == "en"):
            legend = {"title":"Number of students who completed and <b>not</b> completed the assigns",
                        "xaxis":"Number of students",
                        "yaxis":"",
                        "columns":{1:"Completed", 2:"Not<br>completed"},
                        'hovertext_done':' student(s) completed',
                        'hovertext_undone':' student(s) <b>not</b> completed'
                    }
        
        df = self._assigns.sort_values(by=["Total_Undone","Name"])
        trace = []
        for i in range(1,len(df.columns)):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df.Name.values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_done'] if i==1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_undone'] for j in range(len(df.iloc[:,i].values.tolist()))],
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
            iplot(fig, filename='Stacked-Bar')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V001@55',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V001@55","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def option_01(self, id_ref):
        return html.Br()

    def option_02(self, id_ref,values=['visible']):
        legend = {"title":"Valores visíveis"}
        if (self._language == "en"):
            legend = {"title":"Visible values"}
      
        return  dcc.Checklist(
                    id=id_ref,
                    options=[
                        {'label': legend["title"], 'value': 'visible'}
                    ],
                    values=values,
                    labelStyle={'display': 'inline-block'}
                )

    def get_option_values(self,index):
        return self._map.interactive_option_values.loc[self._map.id == index].tolist()[0]

    def get_option_index(self,index):
        return self._map.interactive_option.loc[self._map.id == index].tolist()[0]

    def get_family_graph(self,index):
        return self._map.chart_family.loc[self._map.id == index].tolist()[0]

    def get_chart_ref(self,index):
        return int(self._map.chart_ref.loc[self._map.id == index].to_string(index=False))

    def get_chart_type(self,index):
        return self._map.type.loc[self._map.id == index].to_string(index=False)

    def load_map_view(self):
        self._map = pd.DataFrame(columns=["id","type","chart_ref","chart_family","interactive_option","interactive_option_values"])

        self._map = self._map.append({self._map.columns[0]:1,
                                      self._map.columns[1]:"Table",
                                      self._map.columns[2]:1,
                                      self._map.columns[3]:[1],
                                      self._map.columns[4]:[1]}, ignore_index=True)

        self._map = self._map.append({self._map.columns[0]:2,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:2,
                                      self._map.columns[3]:[2,3],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:3,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:2,
                                      self._map.columns[3]:[2,3],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:4,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:4,
                                      self._map.columns[3]:[4,5],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:5,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:4,
                                      self._map.columns[3]:[4,5],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!
        
        self._map = self._map.append({self._map.columns[0]:6,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:6,
                                      self._map.columns[3]:[6,7],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:7,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:6,
                                      self._map.columns[3]:[6,7],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:8,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:8,
                                      self._map.columns[3]:[8,9],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:9,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:8,
                                      self._map.columns[3]:[8,9],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:10,
                                      self._map.columns[1]:"Lollipop",
                                      self._map.columns[2]:10,
                                      self._map.columns[3]:[10,11],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:11,
                                      self._map.columns[1]:"Lollipop",
                                      self._map.columns[2]:10,
                                      self._map.columns[3]:[10,11],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:12,
                                      self._map.columns[1]:"Lollipop",
                                      self._map.columns[2]:12,
                                      self._map.columns[3]:[12,13],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:13,
                                      self._map.columns[1]:"Lollipop",
                                      self._map.columns[2]:12,
                                      self._map.columns[3]:[12,13],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:14,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:14,
                                      self._map.columns[3]:[14,15],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:15,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:14,
                                      self._map.columns[3]:[14,15],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:16,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:16,
                                      self._map.columns[3]:[16,17],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!
        
        self._map = self._map.append({self._map.columns[0]:17,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:16,
                                      self._map.columns[3]:[16,17],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:18,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:18,
                                      self._map.columns[3]:[18,19],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:19,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:18,
                                      self._map.columns[3]:[18,19],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:20,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:20,
                                      self._map.columns[3]:[20,21],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:21,
                                      self._map.columns[1]:"Barchart",
                                      self._map.columns[2]:20,
                                      self._map.columns[3]:[20,21],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:22,
                                      self._map.columns[1]:"Lollipop",
                                      self._map.columns[2]:22,
                                      self._map.columns[3]:[22,23],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:23,
                                      self._map.columns[1]:"Lollipop",
                                      self._map.columns[2]:22,
                                      self._map.columns[3]:[22,23],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:24,
                                      self._map.columns[1]:"Lollipop",
                                      self._map.columns[2]:24,
                                      self._map.columns[3]:[24,25],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:25,
                                      self._map.columns[1]:"Lollipop",
                                      self._map.columns[2]:24,
                                      self._map.columns[3]:[24,25],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:26,
                                      self._map.columns[1]:"Scatter",
                                      self._map.columns[2]:26,
                                      self._map.columns[3]:[26,27,28],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:27,
                                      self._map.columns[1]:"Scatter",
                                      self._map.columns[2]:26,
                                      self._map.columns[3]:[26,27,28],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:28,
                                      self._map.columns[1]:"Scatter",
                                      self._map.columns[2]:26,
                                      self._map.columns[3]:[26,27,28],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:29,
                                      self._map.columns[1]:"Scatter",
                                      self._map.columns[2]:29,
                                      self._map.columns[3]:[29],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:30,
                                      self._map.columns[1]:"Scatter",
                                      self._map.columns[2]:30,
                                      self._map.columns[3]:[30],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:31,
                                      self._map.columns[1]:"Heatmap",
                                      self._map.columns[2]:31,
                                      self._map.columns[3]:[31,32,33],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:32,
                                      self._map.columns[1]:"Heatmap",
                                      self._map.columns[2]:31,
                                      self._map.columns[3]:[31,32,33],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:33,
                                      self._map.columns[1]:"Heatmap",
                                      self._map.columns[2]:31,
                                      self._map.columns[3]:[31,32,33],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:34,
                                      self._map.columns[1]:"Heatmap",
                                      self._map.columns[2]:34,
                                      self._map.columns[3]:[34,35],
                                      self._map.columns[4]:[2],
                                      self._map.columns[5]:[""]}, ignore_index=True)

        self._map = self._map.append({self._map.columns[0]:35,
                                      self._map.columns[1]:"Heatmap",
                                      self._map.columns[2]:34,
                                      self._map.columns[3]:[34,35],
                                      self._map.columns[4]:[2],
                                      self._map.columns[5]:["visible"]}, ignore_index=True)

        self._map = self._map.append({self._map.columns[0]:36,
                                      self._map.columns[1]:"Heatmap",
                                      self._map.columns[2]:34,
                                      self._map.columns[3]:[34,35],
                                      self._map.columns[4]:[2],
                                      self._map.columns[5]:[""]}, ignore_index=True)

        self._map = self._map.append({self._map.columns[0]:37,
                                      self._map.columns[1]:"Heatmap",
                                      self._map.columns[2]:36,
                                      self._map.columns[3]:[36,37],
                                      self._map.columns[4]:[2],
                                      self._map.columns[5]:["visible"]}, ignore_index=True)

        self._map = self._map.append({self._map.columns[0]:38,
                                      self._map.columns[1]:"Grouped Bar",
                                      self._map.columns[2]:38,
                                      self._map.columns[3]:[38,39,40],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:39,
                                      self._map.columns[1]:"Grouped Bar",
                                      self._map.columns[2]:38,
                                      self._map.columns[3]:[38,39,40],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:40,
                                      self._map.columns[1]:"Grouped Bar",
                                      self._map.columns[2]:38,
                                      self._map.columns[3]:[38,39,40],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:41,
                                      self._map.columns[1]:"Grouped Bar",
                                      self._map.columns[2]:41,
                                      self._map.columns[3]:[41,42,43],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:42,
                                      self._map.columns[1]:"Grouped Bar",
                                      self._map.columns[2]:41,
                                      self._map.columns[3]:[41,42,43],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:43,
                                      self._map.columns[1]:"Grouped Bar",
                                      self._map.columns[2]:41,
                                      self._map.columns[3]:[41,42,43],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:44,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:44,
                                      self._map.columns[3]:[44,45,46],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:45,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:44,
                                      self._map.columns[3]:[44,45,46],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:46,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:44,
                                      self._map.columns[3]:[44,45,46],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:47,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:47,
                                      self._map.columns[3]:[47,48,49],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:48,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:47,
                                      self._map.columns[3]:[47,48,49],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:49,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:47,
                                      self._map.columns[3]:[47,48,49],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:50,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:50,
                                      self._map.columns[3]:[50,51,52],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:51,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:50,
                                      self._map.columns[3]:[50,51,52],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:52,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:50,
                                      self._map.columns[3]:[50,51,52],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:53,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:53,
                                      self._map.columns[3]:[53,54,55],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:54,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:53,
                                      self._map.columns[3]:[53,54,55],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

        self._map = self._map.append({self._map.columns[0]:55,
                                      self._map.columns[1]:"Stacked Bar",
                                      self._map.columns[2]:53,
                                      self._map.columns[3]:[53,54,55],
                                      self._map.columns[4]:[1]}, ignore_index=True) #Change!

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
        elif id == 33:
            return self.graph_33()
        elif id == 34:
            return self.graph_34()
        elif id == 35:
            return self.graph_35()
        elif id == 36:
            return self.graph_36()
        elif id == 37:
            return self.graph_37()
        elif id == 38:
            return self.graph_38()
        elif id == 39:
            return self.graph_39()
        elif id == 40:
            return self.graph_40()
        elif id == 41:
            return self.graph_41()
        elif id == 42:
            return self.graph_42()
        elif id == 43:
            return self.graph_43()
        elif id == 44:
            return self.graph_44()
        elif id == 45:
            return self.graph_45()
        elif id == 46:
            return self.graph_46()
        elif id == 47:
            return self.graph_47()
        elif id == 48:
            return self.graph_48()
        elif id == 49:
            return self.graph_49()
        elif id == 50:
            return self.graph_50()
        elif id == 51:
            return self.graph_51()
        elif id == 52:
            return self.graph_52()
        elif id == 53:
            return self.graph_53()
        elif id == 54:
            return self.graph_54()
        elif id == 55:
            return self.graph_55()
        else:
            print("V001@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V001_'+str(id)+'.pkl'
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
        
        file_name = 'V001_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)
        f = open(file_path,'wb')
        pickle.dump(self.get_chart(id),f)
        f.close()

        self._type_result = aux_type_result

    def print_all_graphs(self,language="pt",type_result="jupyter-notebook"):
        self._language = language
        self._type_result = type_result
        self.graph_01() #Table
        self.graph_02() #Barchart
        self.graph_03()
        self.graph_04()
        self.graph_05()
        self.graph_06()
        self.graph_07()
        self.graph_08()
        self.graph_09()
        self.graph_10() #Lollipop
        self.graph_11()
        self.graph_12()
        self.graph_13()
        self.graph_14() #Barchart
        self.graph_15()
        self.graph_16()
        self.graph_17()
        self.graph_18()
        self.graph_19()
        self.graph_20()
        self.graph_21()
        self.graph_22() #Lollipop
        self.graph_23()
        self.graph_24()
        self.graph_25()
        self.graph_26() #Scatter
        self.graph_27()
        self.graph_28()
        self.graph_29()
        self.graph_30()
        self.graph_31() #Heatmap
        self.graph_32()
        self.graph_33()
        self.graph_34()
        self.graph_35()
        self.graph_36()
        self.graph_37()
        self.graph_38() #Grouped Bar
        self.graph_39()
        self.graph_40() 
        self.graph_41()
        self.graph_42()
        self.graph_43() 
        self.graph_44() #Stacked Bar
        self.graph_45()
        self.graph_46()
        self.graph_47()
        self.graph_48()
        self.graph_49()
        self.graph_50()
        self.graph_51()
        self.graph_52()
        self.graph_53()
        self.graph_54()
        self.graph_55()        

# instance = V001()
# instance.generate_dataset(number_students = 20, number_assigns = 10)
# instance.print_all_graphs("pt")
# instance.print_all_graphs("en")