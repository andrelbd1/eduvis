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

class V004:
    NUMBER_STUDENTS = 20
    DATASET = pd.DataFrame()
    
    _language = "pt"
    _type_result="jupyter-notebook"
    _material_name = []
    _df_sum = []
    _preprocessed_folder = os.path.join('Preprocessed')

    def __init__(self, language="pt", type_result = "jupyter-notebook"):
        self._language = language
        self._type_result = type_result
    
    def generate_dataset(self, number_students = 20, rand_names = []):
        self.NUMBER_STUDENTS = number_students

        if (self._language == "pt"):
            assign_label = "Atividade "
            students_label = "Estudantes"
            self._material_name = ['Vídeo 1','Vídeo 2','Vídeo 3','Vídeo 4','Vídeo 5']
        else:
            assign_label = "Assign "
            students_label = "Students"
            self._material_name = ['Video 1','Video 2','Video 3','Video 4','Video 5']

        video_dur = []
        video_dur = [np.random.randint(240,600) for n in range(7)] #video duration ranging between 240 and 600 seconds        
        
        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)

        self.DATASET = pd.DataFrame(columns=[students_label,str(self._material_name[0])+' ('+str(video_dur[0])+'s)',
                        str(self._material_name[1])+' ('+str(video_dur[1])+'s)',str(self._material_name[2])+' ('+str(video_dur[2])+'s)',
                        str(self._material_name[3])+' ('+str(video_dur[3])+'s)',str(self._material_name[4])+' ('+str(video_dur[4])+'s)','Total'])
        
        list_aux = []
        for i in range(0,self.NUMBER_STUDENTS):
            for j  in range(0,len(self.DATASET.columns)):
                list_aux.append(
                        [np.random.randint(5,video_dur[j]) for n in range(np.random.randint(0,5))] #user access ranging between  
                    )                                                                       
            self.DATASET.loc[i] = list_aux
            self.DATASET.loc[i,self.DATASET.columns[0]] = rand_names[i]
            list_aux.clear()

        self.DATASET[self.DATASET.columns[len(self.DATASET.columns)-1]] = self.DATASET.apply(self.sum_times, axis=1)

        self._df_sum = pd.DataFrame(columns=self._material_name)
        self._df_sum.insert(loc=0,column=students_label,value=self.DATASET[self.DATASET.columns[0]])
        self._df_sum.insert(loc=len(self._material_name)+1,column="Total",value=self.DATASET.Total) #Add into the self._df_sum a column to assign Total values
        
        lst = self.DATASET.columns[1:].tolist() #Get all columns after students
        for i in range(0, self.NUMBER_STUDENTS):
            for j in range(0,len(lst)-1): #Iterate all columns, except Total                
                sum_value = sum(self.DATASET.loc[i,lst[j]])                
                self._df_sum.loc[i,self._material_name[j]] = sum_value
        
        # print(self._df_sum)

    def sum_times(self,row):
        lst = self.DATASET.columns[1:].tolist()
        sum_value = 0
        for i in range(len(lst)-1):
            sum_value += sum(row[lst[i]])

        return sum_value    

    # Table presenting raw data    
    def graph_01(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante"}
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student"}

        df = self.DATASET
        
        trace = [Table(
            header=dict(
                values=list(df.columns),
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[df[i].tolist() for i in df.columns[:]],                
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
                id='V004@1',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_02(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante"}
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student"}

        df = self._df_sum
        
        trace = [Table(
            header=dict(
                values=list(df.columns),
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[df[i].tolist() for i in df.columns[:]],                
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
                id='V004@2',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    # Scatter
    def graph_03(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' segundos de tempo de acesso no ',
                    'hovertext_total':' segundos de tempo total de acesso nos videos'
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' seconds of access length on ',
                        'hovertext_total':' seconds of total access length on the vides',
                    }
        # https://plot.ly/python/bubble-charts/
        # https://plot.ly/python/reference/#layout-xaxis
        # https://plot.ly/python/axes/#subcategory-axes
        df = self._df_sum
        max_value = 0
        sum_value = 0        
        for i in range(1,len(df.columns)-1): #Iterate all columns, except Total
            max_local = max(df.iloc[1:,i].values.tolist())
            max_value = max(max_local,max_value)
                
        sizeref=4.5*max_value/(max_value)*2
        trace = []
        for i in range(0, self.NUMBER_STUDENTS):
            trace.append(
                Scatter(
                    x=[df.iloc[i,0]]*len(df.columns[1:]), #student
                    y=df.columns[1:], #videos
                    hovertext=['<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,j])+legend['hovertext']+df.columns[j] if j<len(df.columns)-1 else '<b>'+df.iloc[i,0]+'</b><br>'+str(df.iloc[i,j])+legend['hovertext_total'] for j in range(1,len(df.columns))],
                    hoverinfo='text',
                    mode='markers',
                    name=df.iloc[i,0], #each student name                    
                    # orientation = "h",
                    text = df.iloc[i,1:].values.tolist(),
                    # text = str(s),
                    marker=dict(
                        symbol='circle',
                        sizemode='area',
                        sizeref=sizeref,
                        size=df.iloc[i,1:].values.tolist(),
                        color="rgb(0,0,255)",
                        line=dict(
                            width=2
                        )
                    )
                )
            )

        layout = Layout(
            title=legend['title'],
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
                range = [-1, len(df)],
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
                # categoryorder = "category descending",
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
                id='V004@3',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Heatmap
    def graph_04(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' segundos de tempo de acesso no ',
                    'hovertext_total':' segundos de tempo total de acesso nos videos'
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' seconds of access length on ',
                        'hovertext_total':' seconds of total access length on the vides'
                    }
        df = self._df_sum
        
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+df.columns[i] if i<len(df.columns)-1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_total'] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Videos
                        x=df.iloc[:,0], #Students
                        hovertext = hovervalue,
                        hoverinfo='text',
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        showscale = True
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
                id='V004@4',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_05(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' segundos de tempo de acesso no ',
                    'hovertext_total':' segundos de tempo total de acesso nos videos'
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' seconds of access length on ',
                        'hovertext_total':' seconds of total access length on the vides'
                    }
        df = self._df_sum
        
        z = []
        hovervalue=[]
        max_value = 0
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+df.columns[i] if i<len(df.columns)-1 else '<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext_total'] for j in range(len(values))])
            max_local = max(values)
            max_value = max(max_local,max_value)

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Videos
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
                    "y":df.columns[i],
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

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V004@5',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@5","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_06(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' segundos de tempo de acesso no ',
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' seconds of access length on ',
                    }
        df = self._df_sum.iloc[:,:len(self._df_sum.columns)-1]
        
        z = []
        hovervalue=[]
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+df.columns[i] for j in range(len(values))])

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Videos
                        x=df.iloc[:,0], #Students
                        hovertext = hovervalue,
                        hoverinfo='text',
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,0,255)']],
                        showscale = True
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
                )
            )

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V004@6',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@6","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_07(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"",
                    "yaxis":"",
                    'hovertext':' segundos de tempo de acesso no ',
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"",
                        "yaxis":"",
                        'hovertext':' seconds of access length on ',
                    }
        df = self._df_sum.iloc[:,:len(self._df_sum.columns)-1]
        
        z = []
        hovervalue=[]
        max_value = 0        
        for i in range (1, len(df.columns)):
            values = df.iloc[:,i].values.tolist()
            z.append(values)
            hovervalue.append(['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+df.columns[i] for j in range(len(values))])
            max_local = max(values)
            max_value = max(max_local,max_value)

        trace = Heatmap(z=z,
                        y=df.columns[1:], #Videos
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
                    "y":df.columns[i],
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
                annotations = annotations
            )

        data = [trace]
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Heatmap')
        elif self._type_result == "dash":            
            return dcc.Graph(
                id='V004@7',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@7","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Grouped Bar
    def graph_08(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"",
                    "yaxis":"Tempo de acesso em segundos",
                    'hovertext':' segundos de tempo de acesso no ',
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"",
                        "yaxis":"Length of access in seconds",
                        'hovertext':' seconds of access length on ',
                    }
        df = self._df_sum
        trace = []
        for i in range(1,len(df.columns[1:])):
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    name=df.columns[i],
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
            ))

        data = trace
        layout = Layout(
                title=legend['title'],
                xaxis = dict(
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
                    dtick=100,
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
                id='V004@8',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@8","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    # Stacked Bar
    def graph_09(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"",
                    "yaxis":"Tempo de acesso em segundos",
                    'hovertext':' segundos de tempo de acesso no ',
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"",
                        "yaxis":"Length of access in seconds",
                        'hovertext':' seconds of access length on ',
                    }
        df = self._df_sum
        trace = []
        for i in range(1,len(df.columns[1:])):
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    name=df.columns[i],
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
            ))

        data = trace
        layout = Layout(
                title=legend['title'],
                barmode='stack',
                xaxis = dict(
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
                    dtick=300,
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
                id='V004@9',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@9","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_10(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"",
                    "yaxis":"Tempo de acesso em segundos",
                    'hovertext':' segundos de tempo de acesso no ',
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"",
                        "yaxis":"Length of access in seconds",
                        'hovertext':' seconds of access length on ',
                    }        
        df = self._df_sum.sort_values(by=[self._df_sum.columns[len(self._df_sum.columns)-1],self._df_sum.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:])):
            trace.append(Bar(
                    x=df[df.columns[0]].values,
                    y=df.iloc[:,i].values,
                    name=df.columns[i],
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
            ))

        data = trace
        layout = Layout(
                title=legend['title'],
                barmode='stack',
                xaxis = dict(
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
                    dtick=300,
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
                id='V004@10',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@10","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_11(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"Tempo de acesso em segundos",
                    "yaxis":"",
                    'hovertext':' segundos de tempo de acesso no ',
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"Length of access in seconds",
                        "yaxis":"",
                        'hovertext':' seconds of access length on ',
                    }
        df = self._df_sum
        trace = []
        for i in range(1,len(df.columns[1:])):
            trace.append(Bar(
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    name=df.columns[i],
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    orientation = 'h'
                    # name=df.iloc[i,0], #each student name
            ))
        
        data = trace
        layout = Layout(
                title=legend['title'],
                barmode='stack',
                xaxis = dict(
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
                id='V004@11',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@11","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_12(self):
        legend = {"title":"Tempo de acesso aos vídeos por estudante",
                    "xaxis":"Tempo de acesso em segundos",
                    "yaxis":"",
                    'hovertext':' segundos de tempo de acesso no ',
                }
        if (self._language == "en"):
            legend = {"title":"Length of access to videos grouped by student",
                        "xaxis":"Length of access in seconds",
                        "yaxis":"",
                        'hovertext':' seconds of access length on ',
                    }
        df = self._df_sum.sort_values(by=[self._df_sum.columns[len(self._df_sum.columns)-1],self._df_sum.columns[0]])
        trace = []
        for i in range(1,len(df.columns[1:])):
            trace.append(Bar(
                    x=df.iloc[:,i].values,
                    y=df[df.columns[0]].values,
                    name=df.columns[i],
                    hovertext = ['<b>'+df.iloc[j,0]+'</b><br>'+str(df.iloc[j,i])+legend['hovertext']+str(df.columns[i]) for j in range(len(df.iloc[:,i].values.tolist()))],
                    hoverinfo='text',
                    orientation = 'h'
                    # name=df.iloc[i,0], #each student name
            ))
        
        data = trace
        layout = Layout(
                title=legend["title"],
                barmode='stack',
                xaxis = dict(
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
                id='V004@12',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V004@12","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

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
        else:
            print("V004@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V004_'+str(id)+'.pkl'
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
        
        file_name = 'V004_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)
        f = open(file_path,'wb')
        pickle.dump(self.get_chart(id),f)
        f.close()

        self._type_result = aux_type_result

    def print_all_graphs(self,language="pt"):
        self._language = language
        self.graph_01() #Table
        self.graph_02()
        self.graph_03() #Scatter
        self.graph_04() #Heatmap
        self.graph_05()
        self.graph_06()
        self.graph_07()
        self.graph_08() #Grouped Bar
        self.graph_09() #Stacked Bar 
        self.graph_10()
        self.graph_11()
        self.graph_12()

# instance = V004()
# instance.generate_dataset(number_students = 20)
# instance.print_all_graphs("pt")
# instance.print_all_graphs("en")