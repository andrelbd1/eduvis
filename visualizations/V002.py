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

class V002:
    NUMBER_STUDENTS = 21
    DATASET = pd.DataFrame()
    _df_sum_access = pd.DataFrame()
    
    _language = "pt"
    _type_result="jupyter-notebook"
    _preprocessed_folder = os.path.join('Preprocessed')

    def __init__(self, language="pt", type_result = "jupyter-notebook"):
        self._language = language
        self._type_result = type_result
    
    def generate_dataset(self, number_students = 20, rand_names = []):
        self.NUMBER_STUDENTS = number_students

        if (self._language == "pt"):
            self.DATASET = pd.DataFrame(columns=["Estudantes","Video 1","Video 2",'Quiz 1','Quiz 2','Pdf 1','Pdf 2','Ebook 1','Ebook 2','Total'])
            self._df_sum_access = pd.DataFrame(columns=['Materiais','Acesso'])
        else:
            self.DATASET = pd.DataFrame(columns=["Students","Video 1","Video 2",'Quiz 1','Quiz 2','Pdf 1','Pdf 2','Ebook 1','Ebook 2','Total'])
            self._df_sum_access = pd.DataFrame(columns=['Materials','Access'])
        
        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)

        for i in range(1,self.NUMBER_STUDENTS+1):
            self.DATASET.loc[i] = [np.random.randint(0,30) for n in range(len(self.DATASET.columns))]
            self.DATASET.loc[i,self.DATASET.columns[0]] = rand_names[i-1]
        
        self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]] = self.DATASET.apply(self.sum_row,axis=1)        
        
        self._df_sum_access[self._df_sum_access.columns[0]] = self.DATASET.columns[1:len(self.DATASET.columns)-1].tolist()

        lst_aux = []
        for material in self._df_sum_access[self._df_sum_access.columns[0]]:
            lst_aux.append(sum(self.DATASET[material].tolist()))
        self._df_sum_access[self._df_sum_access.columns[1]] = lst_aux


    def sum_row(self,row):
        total = 0
        for i in range(1, len(row[1:])):
            total += row[i]

        return total

    # Table presenting raw data    
    def graph_01(self):
        legend = {"title":"Número de acessos nos materiais agrupados por estudante"}
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials grouped by student"}
        
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        
        trace = [Table(
            header=dict(
                values=list(df.columns[:len(df.columns)]),
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[df[i].tolist() for i in df.columns[:len(df.columns)]],
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
                id='V002@1',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Grouped Bar
    def graph_02(self):
        legend = {"title":"Número de acessos nos materiais agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"Número de acessos",
                    'hovertext':' acessos em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials grouped by student",
                        "xaxis":"",
                        "yaxis":"Number of access",
                        'hovertext':' access on '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    name=df.columns[i],
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
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
                id='V002@2',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Stacked Bar
    def graph_03(self):
        legend = {"title":"Número de acessos nos materiais agrupados por estudante",
                    "xaxis":"",
                    "yaxis":"Número de acessos",
                    'hovertext':' acesso(s) em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials grouped by student",
                        "xaxis":"",
                        "yaxis":"Number of access",
                        'hovertext':' access on '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=df.columns[i]
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
                    dtick=15,
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
                id='V002@3',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_04(self):
        legend = {"title":"Número de acessos nos materiais agrupados por estudante e ordenados pelo total de acesso",
                    "xaxis":"",
                    "yaxis":"Número de acessos",
                    'hovertext':' acesso(s) em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials grouped by student sorted by total access",
                        "xaxis":"",
                        "yaxis":"Number of access",
                        'hovertext':' access on '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[len(self.DATASET.columns)-1],self.DATASET.columns[0]])
        
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=df.columns[i]
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
                    dtick=15,
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
                id='V002@4',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_05(self):
        legend = {"title":"Número de acessos nos materiais agrupados por estudante",
                    "xaxis":"Número de acessos",
                    "yaxis":"",
                    'hovertext':' acesso(s) em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials grouped by student",
                        "xaxis":"Number of access",
                        "yaxis":"",
                        'hovertext':' access on '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    name=df.columns[i],
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
                id='V002@5',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@5","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_06(self):
        legend = {"title":"Número de acessos nos materiais agrupados por estudante e ordenados pelo total de acesso",
                    "xaxis":"Número de acessos",
                    "yaxis":"",
                    'hovertext':' acesso(s) em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials grouped by student sorted by total access",
                        "xaxis":"Number of access",
                        "yaxis":"",
                        'hovertext':' access on '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[len(self.DATASET.columns)-1],self.DATASET.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:len(df.columns)])):
            trace.append(Bar(
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    name=df.columns[i],
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
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
                id='V002@6',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@6","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Heatmap
    def graph_07(self):
        legend = {"title":"Número de acessos nos materiais por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' acesso(s) em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' access on '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)-1):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+df.columns[i] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:len(df.columns)-1], #Assigns
                        x=df.iloc[:,0], #Students
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        hovertext = hovervalue,
                        hoverinfo='text',
                        showscale = True
                    )
        
        layout = Layout(
                # title='Número de acessos nos materiais por estudante',
                title=legend["title"],
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
                id='V002@7',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@7","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_08(self):
        legend = {"title":"Número de acessos nos materiais por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' acesso(s) em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' access on '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        z = []
        max_value = 0
        hovervalue=[]
        for i in range (1, len(df.columns)-1):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+df.columns[i] for j in range(len(values))])
            max_local = max(values)
            max_value = max(max_local,max_value)
        
        trace = Heatmap(z=z,
                        y=df.columns[1:len(df.columns)-1],
                        x=df.iloc[:,0], #Students
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        hovertext = hovervalue,
                        hoverinfo='text',
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
                    "y":df.columns.values[i],
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
                ),
                annotations = annotations
            )

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V002@8',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@8","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_09(self):
        legend = {"title":"Número de acessos nos materiais por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' acesso(s) em ',
                    'hovertext_total':' total de acessos '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' access on ',
                        'hovertext_total':' total of access '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)            
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+df.columns[i] if i < len(df.columns)-1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_total'] for j in range(len(values))])
        
        trace = Heatmap(z=z,
                        y=df.columns[1:len(df.columns)], #Assigns
                        x=df.iloc[:,0], #Students
                        hovertext = hovervalue,
                        hoverinfo='text',
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        showscale = True
                    )
        
        layout = Layout(
                # title='Número de acessos nos materiais por estudante',
                title=legend["title"],
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
                id='V002@9',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@9","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_10(self):
        legend = {"title":"Número de acessos nos materiais por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' acessos em ',
                    'hovertext_total':' total de acessos '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' access on ',
                        'hovertext_total':' total of access '
                    }
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        z = []
        hovervalue=[]
        max_value = 0        
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)            
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+df.columns[i] if i < len(df.columns)-1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_total'] for j in range(len(values))])
            max_local = max(values)
            max_value = max(max_local,max_value)
        
        trace = Heatmap(z=z,
                        y=df.columns[1:len(df.columns)],
                        x=df.iloc[:,0], #Students
                        hovertext = hovervalue,
                        hoverinfo='text',
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        showscale = True
                    )

        annotations=[]
        for i in range(1,len(df.columns)):
            for j in range(0,len(df)):
                color = 'rgb(0,0,0)'
                if df.iloc[j,i] > max_value/2:
                    color = 'rgb(255,255,255)'
                annotations.append({
                    "text":str(df.iloc[j,i]),
                    "y":df.columns.values[i],
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
                ),
                annotations = annotations
            )

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V002@10',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@10","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Scatter
    def graph_11(self):
        legend = {"title":"Número de acessos nos materiais por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' acesso(s) em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' access on '
                    }
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])
        
        sizeref = 0.05
        # print (sizeref)

        trace = []
        for i in range(0, len(df)):                    
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*(len(df.columns)-2), #student
                    y=df.columns[1:len(df.columns)-1], #materials
                    mode='markers',
                    hovertext=['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,j])+legend['hovertext']+df.columns[j] for j in range(1,len(df.columns)-1)],
                    hoverinfo='text',
                    name=df.iloc[i,0], #student name
                    text = df.iloc[i,1:len(df.columns)-1].values.tolist(),
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=[j/2 for j in df.iloc[i,1:len(df.columns)-1].values.tolist()],
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=2
                        )
                    )
                )
            )

        layout = Layout(
            title=legend["title"],
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
                categoryorder = "category ascending",
                # domain = [0, 1],
                fixedrange = False,
                range = [-1, len(self.DATASET.columns[1:])],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            margin = dict(
                b=150,
            ),
        )

        data = trace
        fig=Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V002@11',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@11","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_12(self):
        legend = {"title":"Número de acessos nos materiais por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' acesso(s) em '
                }
        if (self._language == "en"):
            legend = {"title":"Number of access in the materials grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' access on '
                    }
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        df = self.DATASET.sort_values(by=[self.DATASET.columns[0]])        
        
        sizeref = 0.3
        
        trace = []
        for i in range(0, len(df)):                    
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*(len(df.columns[1:])), #student
                    y=df.columns[1:len(df.columns)], #materials
                    mode='markers',
                    hovertext=['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,j])+legend['hovertext']+df.columns[j] for j in range(1,len(df.columns))],
                    hoverinfo='text',
                    name=df.iloc[i,0], #student name
                    text = df.iloc[i,1:len(df.columns)].values.tolist(),
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=[j/2 for j in df.iloc[i,1:len(df.columns)].values.tolist()],
                        color = 'rgb(0,0,255)',
                        line=dict(
                            width=2
                        )
                    )
                )
            )

        layout = Layout(
            title=legend["title"],
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
                range = [-1, len(self.DATASET.columns)],
                rangemode = "normal",
                showline = True,                
                type = "category"
            ),
            margin = dict(
                b=150,
            ),
        )

        data = trace
        fig=Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V002@12',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@12","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Barchart
    def graph_13(self):
        legend = {"title":"Número de acessos por material",
                    "xaxis":"",
                    "yaxis":"Número de acessos",
                    'hovertext':' acesso(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of access by material",
                        "xaxis":"",
                        "yaxis":"Number of access",
                        'hovertext':' access'
                    }

        trace = []
        trace.append(Bar(
            x=self._df_sum_access.iloc[:,0].values,
            y=self._df_sum_access.iloc[:,1].values,
            hovertext=['<b>'+self._df_sum_access.iloc[j,0]+'</b><br>'+str(self._df_sum_access.iloc[j,1])+legend['hovertext'] for j in range(len(self._df_sum_access))],
            hoverinfo='text',
        ))

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
                    id='V002@13',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@13","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_14(self):
        legend = {"title":"Número de acessos por material",
                    "xaxis":"",
                    "yaxis":"Número de acessos",
                    'hovertext':' acesso(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of access by material",
                        "xaxis":"",
                        "yaxis":"Number of access",
                        'hovertext':' access'
                    }

        df = self._df_sum_access.sort_values(by=[self._df_sum_access.columns[1]])

        trace = []
        trace.append(Bar(
            x=df.iloc[:,0].values,
            y=df.iloc[:,1].values,
            hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,1])+legend['hovertext'] for j in range(len(df))],
            hoverinfo='text',
        ))

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
                    id='V002@14',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@14","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_15(self):
        legend = {"title":"Número de acessos por material",
                    "xaxis":"Número de acessos",
                    "yaxis":"",
                    'hovertext':' acesso(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of access by material",
                        "xaxis":"Number of access",
                        "yaxis":"",
                        'hovertext':' access'
                    }

        trace = []
        trace.append(Bar(
            x=self._df_sum_access.iloc[:,1].values,
            y=self._df_sum_access.iloc[:,0].values,
            hovertext=['<b>'+self._df_sum_access.iloc[j,0]+'</b><br>'+str(self._df_sum_access.iloc[j,1])+legend['hovertext'] for j in range(len(self._df_sum_access))],
            hoverinfo='text',
            orientation = 'h'
        ))

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
                    id='V002@15',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@15","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    def graph_16(self):
        legend = {"title":"Número de acessos por material",
                    "xaxis":"Número de acessos",
                    "yaxis":"",
                    'hovertext':' acesso(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of access by material",
                        "xaxis":"Number of access",
                        "yaxis":"",
                        'hovertext':' access'
                    }
        
        df = self._df_sum_access.sort_values(by=[self._df_sum_access.columns[1]])

        trace = []
        trace.append(Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,1])+legend['hovertext'] for j in range(len(df))],
            hoverinfo='text',
            orientation = 'h'
        ))

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
                    id='V002@16',
                    figure=fig
                )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@16","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_17(self):
        legend = {"title":"Número de acessos por material",
                    "xaxis":"Número de acessos",
                    "yaxis":"",
                    'hovertext':' acesso(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of access by material",
                        "xaxis":"Number of access",
                        "yaxis":"",
                        'hovertext':' access'
                    }

        trace = []
        trace.append(Bar(
            x=self._df_sum_access.iloc[:,1].values,
            y=self._df_sum_access.iloc[:,0].values,
            hoverinfo='none',
            orientation = 'h',
            width=[0.04]*len(self._df_sum_access.iloc[:,1].values),
            name="",
            text="",
            marker=dict(
                    color = 'lightgray'
                )
        ))
        
        trace.append(
            Scatter(
                x=self._df_sum_access.iloc[:,1].values,
                y=self._df_sum_access.iloc[:,0].values,
                mode='markers',
                name = "",
                hovertext=['<b>'+self._df_sum_access.iloc[j,0]+'</b><br>'+str(self._df_sum_access.iloc[j,1])+legend['hovertext'] for j in range(len(self._df_sum_access))],
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
                # tick0=0,
                # dtick=1,
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
                id='V002@17',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@17","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_18(self):
        legend = {"title":"Número de acessos por material",
                    "xaxis":"Número de acessos",
                    "yaxis":"",
                    'hovertext':' acesso(s)'
                }
        if (self._language == "en"):
            legend = {"title":"Number of access by material",
                        "xaxis":"Number of access",
                        "yaxis":"",
                        'hovertext':' access'
                    }

        df = self._df_sum_access.sort_values(by=[self._df_sum_access.columns[1]])

        trace = []
        trace.append(Bar(
            x=df.iloc[:,1].values,
            y=df.iloc[:,0].values,
            hoverinfo='none',
            orientation = 'h',
            width=[0.04]*len(df.iloc[:,1].values),
            name="",
            text="",
            marker=dict(
                    color = 'lightgray'
                )
        ))
        
        trace.append(
            Scatter(
                x=df.iloc[:,1].values,
                y=df.iloc[:,0].values,
                mode='markers',
                name = "",
                hovertext=['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,1])+legend['hovertext'] for j in range(len(df))],
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
                # tick0=0,
                # dtick=1,
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
                id='V002@18',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V002@18","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

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
        else:
            print("V002@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V002_'+str(id)+'.pkl'
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
        
        file_name = 'V002_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)
        f = open(file_path,'wb')
        pickle.dump(self.get_chart(id),f)
        f.close()

        self._type_result = aux_type_result

    def print_all_graphs(self,language="pt"):
        self._language = language
        self.graph_01() #Table
        self.graph_02() #Grouped Bar
        self.graph_03() #Stacked Bar
        self.graph_04()
        self.graph_05()
        self.graph_06()
        self.graph_07() #Heatmap
        self.graph_08()
        self.graph_09()
        self.graph_10()
        self.graph_11() #Scatter
        self.graph_12()
        self.graph_13() #Barchart
        self.graph_14()
        self.graph_15()
        self.graph_16()
        self.graph_17() #Lollipop
        self.graph_18()

        #Fazer Heatmap e Scatter apresentando total tbm.

# instance = V002()
# instance.generate_dataset(number_students = 20)
# instance.print_all_graphs("pt")
# # instance.print_all_graphs("en")