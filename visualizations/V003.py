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

class V003:
    NUMBER_STUDENTS = 21
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
            self.DATASET = pd.DataFrame(columns=["Estudantes","Curtidas","Postagens","Acesso","Total"])
        else:
            self.DATASET = pd.DataFrame(columns=["Students","Likes","Posts","Access","Total"])
        
        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)

        for i in range(1,self.NUMBER_STUDENTS+1):
            self.DATASET.loc[i] = [np.random.randint(0,21) for n in range(len(self.DATASET.columns))]
            self.DATASET.loc[i,self.DATASET.columns[0]] = rand_names[i-1]

        self.DATASET[self.DATASET.columns[3]] = self.DATASET.apply(self.sum_row,axis=1)
        self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]] = self.DATASET.apply(self.sum_row,axis=1)

    def sum_row(self,row):
        total = 0
        for i in range(1, len(row[1:])):
            total += row[i]

        return total

    # Table presenting raw data
    def graph_01(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante"}
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student"}

        df = self.DATASET.iloc[:,0:len(self.DATASET.columns[1:])]
        
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
                id='V003@1',
                figure={"data": data}
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Grouped Bar
    def graph_02(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"Número de acessos, postagens e curtidas",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"",
                        "yaxis":"Number of access, posts and likes",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        
        df = self.DATASET.iloc[:,0:len(self.DATASET.columns[1:])]
        trace = []
        for i in range(1,len(df.columns)): 
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext'][i] for j in range(len(df))],
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
                id='V003@2',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_03(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"Número de acessos, postagens e curtidas",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"",
                        "yaxis":"Number of access, posts and likes",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        
        df = self.DATASET.sort_values(by=[self.DATASET.columns[3],self.DATASET.columns[0]]).iloc[:,0:len(self.DATASET.columns[1:])]
        trace = []
        for i in range(1,len(df.columns)): 
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext'][i] for j in range(len(df))],
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
                id='V003@3',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    # Stacked Bar
    def graph_04(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"Número de acessos, postagens e curtidas",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"",
                        "yaxis":"Number of access, posts and likes",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        df = self.DATASET.iloc[:,0:len(self.DATASET.columns[1:])]
        trace = []
        for i in range(1,len(df.columns)):         
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext'][i] for j in range(len(df))],
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
                id='V003@4',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_05(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"Número de acessos, postagens e curtidas",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"",
                        "yaxis":"Number of access, posts and likes",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        df = self.DATASET.sort_values(by=["Total",self.DATASET.columns[0]]).iloc[:,0:len(self.DATASET.columns[1:])]        
        trace = []
        for i in range(1,len(df.columns)):         
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext'][i] for j in range(len(df))],
                    hoverinfo='text',
                    name=legend['columns'][i]
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
                id='V003@5',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@5","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_06(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"Número de acessos, postagens e curtidas",
                    "yaxis":"",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"Number of access, posts and likes",
                        "yaxis":"",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        df = self.DATASET
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext'][i] for j in range(len(df))],
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
                id='V003@6',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@6","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_07(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"Número de acessos, postagens e curtidas",
                    "yaxis":"",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"Number of access, posts and likes",
                        "yaxis":"",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        df = self.DATASET.sort_values(by=["Total",self.DATASET.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(                    
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext'][i] for j in range(len(df))],
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
                id='V003@7',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@7","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Scatter
    def graph_08(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        max_value=0
        for i in range(0, len(df)): #Take the max value in whole dataframe
            if max(df.iloc[:,1:len(df.columns)].values[i]) > max_value:
                max_value = max(df.iloc[:,1:len(df.columns)].values[i])
        
        sizeref = 0.2

        trace = []        
        
        for i in range(0, len(df)):
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*(len(df.columns[1:])), #student
                    y=[legend["columns"][k] for k in range (1,4)],
                    hovertext=['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,j])+legend['hovertext'][j] for j in range(1,len(df.columns)-1)],
                    hoverinfo='text',
                    mode='markers',
                    # name=df.iloc[i,0], #student name
                    # text = df.iloc[i,1:len(df.columns)].values.tolist(),
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,1:len(df.columns)-1].values.tolist(),
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=2
                        )
                    )
                )
            )

        layout = Layout(
            title = legend["title"],
            hovermode = "closest",
            showlegend = False,
            xaxis = dict(
                title = legend["xaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(self.DATASET)],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            yaxis = dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                autorange = False,
                # categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(self.DATASET.columns[1:])],
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
                id='V003@8',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@8","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    #Heatmap
    def graph_09(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)-1):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext'][i] for j in range(len(values))])
        
        trace = Heatmap(z=z,
                        y=[legend["columns"][i] for i in range (1,4)],
                        x=df.iloc[:,0], #Students
                        hovertext = hovervalue,
                        hoverinfo='text',
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        showscale = True
                    )
        
        layout = Layout(
                title = legend["title"],
                # autosize=False,
                # width=950,
                # height=350,
                hovermode = "closest",                
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
                id='V003@9',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@9","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_10(self):
        legend = {"title":"Número de acessos, postagens e curtidas agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    "columns":{1:"Curtidas", 2:"Postagens", 3:"Acessos"},
                    'hovertext':{1:' curtida(s)',2:' postagem(s)',3:' acesso(s)'}
                }
        if (self._language == "en"):
            legend = {"title":"Number of access, posts and likes grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        "columns":{1:"Likes", 2:"Posts", 3:"Access"},
                        'hovertext':{1:' like(s)',2:' post(s)',3:' access'}
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        z = []
        hovervalue=[]
        max_value = 0

        for i in range (1, len(df.columns)-1):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext'][i] for j in range(len(values))])
            max_local = max(values)
            max_value = max(max_local,max_value)
        
        trace = Heatmap(z=z,
                        y=[legend["columns"][i] for i in range (1,4)],
                        x=df.iloc[:,0], #Students
                        hovertext = hovervalue,
                        hoverinfo='text',
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        showscale = True
                    )

        annotations=[]
        for i in range(1,len(df.columns)-1):
            for j in range(0,len(df)):
                color = 'rgb(0,0,0)'
                if df.iloc[j,i] > max_value/2:
                    color = 'rgb(255,255,255)'
                annotations.append({
                    "text":str(df.iloc[j,i]),
                    # "y":df.columns.values[i],
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
                title = legend["title"],
                # autosize=False,
                # width=950,
                # height=350,
                hovermode = "closest",
                xaxis=dict(
                    title = legend["xaxis"],
                    titlefont=dict(
                        # family='Arial, sans-serif',
                        # size=18,
                        color='rgb(180,180,180)',
                    ),
                ),
                yaxis=dict(
                    title = legend["xaxis"],
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

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V003@10',
                figure=fig
            )
        elif self._type_result == "flask":            
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V003@10","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

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
        else:
            print("V003@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V003_'+str(id)+'.pkl'
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
        
        file_name = 'V003_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)
        f = open(file_path,'wb')
        pickle.dump(self.get_chart(id),f)
        f.close()

        self._type_result = aux_type_result

    def print_all_graphs(self,language="pt"):
        self._language = language
        self.graph_01() #Table
        self.graph_02() #Grouped Bar
        self.graph_03()
        self.graph_04() #Stacked Bar
        self.graph_05()
        self.graph_06()
        self.graph_07() 
        self.graph_08() #Scatter
        self.graph_09() #Heatmap
        self.graph_10()

# instance = V003()
# instance.generate_dataset(number_students = 20)
# instance.print_all_graphs("pt")
# instance.print_all_graphs("en")