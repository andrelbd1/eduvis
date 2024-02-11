import dash
import dash_core_components as dcc
import dash_html_components as html

import os
import pandas as pd
import numpy as np

from random import randrange
import datetime, requests

import pickle
import json

from plotly.utils import PlotlyJSONEncoder
from plotly.graph_objs import Figure, Layout, Bar, Table, Heatmap, Scatter, Box, Violin
from plotly.offline import init_notebook_mode, iplot

init_notebook_mode(connected=True) # initiate notebook for offline plot

class V009:
    NUMBER_STUDENTS = 10
    VIDEO_SIZE = 45
    DATASET = pd.DataFrame()

    _language = "pt"
    _type_result="jupyter-notebook"

    _df_chronology = pd.DataFrame()
    _preprocessed_folder = os.path.join('Preprocessed')
    textAction = []

    def __init__(self, language="pt", type_result = "jupyter-notebook"):
        self._language = language
        self._type_result = type_result

    def load_dataset(self, url):
        pass

    def generate_dataset(self, number_actions = 100, video_size = 30, number_students = 20, rand_names = []):
        self.NUMBER_STUDENTS = number_students
        self.NUMBER_ACTIONS = number_actions
        self.VIDEO_SIZE = video_size

        if (self._language == "pt"):
            self.DATASET = pd.DataFrame(columns=["Estudantes","Tempo (segundos)","Play","Pause","Seek de","Seek para","Abandono"])
            self._df_chronology = pd.DataFrame(columns=[self.DATASET.columns[0],'Tempo','Ação'])
            self.textAction = ['Play aos ', 'Pause aos ', 'Seek de ', ' para ', 'Abandono aos ']
        else:
            self.DATASET = pd.DataFrame(columns=["Students","Time (seconds)","Play","Pause","Seek from","Seek to","Dropout"])
            self._df_chronology = pd.DataFrame(columns=[self.DATASET.columns[0],'Timestamp','Action'])
            self.textAction = ['Play at ', 'Pause at ', 'Seek from ', ' to ', 'Dropout at ']

        if len(rand_names) == 0:
            names = pd.read_csv("assets/names.csv")
            rand_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,self.NUMBER_STUDENTS)]
            rand_names.sort()
        else:
            self.NUMBER_STUDENTS = len(rand_names)

        lst = [ [rand_names[i]]*(video_size+1) for i in range(0,self.NUMBER_STUDENTS)]
        names = []
        for i in range(0, len(lst)):
            names = names+lst[i]
        
        self.DATASET[self.DATASET.columns[0]] = names
        
        curr = ''
        time = 0

        #Generate actions time
        lst_play = np.random.randint(0, self.VIDEO_SIZE+1, size=int(self.VIDEO_SIZE/1.5)).tolist()
        lst_pause = np.random.randint(0, self.VIDEO_SIZE+1, size=int(self.VIDEO_SIZE/1.5)).tolist()
        lst_seek_from = np.random.randint(0, self.VIDEO_SIZE+1, size=int(self.VIDEO_SIZE/2)).tolist()
        lst_seek_to = np.random.randint(0, self.VIDEO_SIZE+1, size=int(self.VIDEO_SIZE/2)).tolist()
        lst_dropout = np.random.randint(0, self.VIDEO_SIZE+1, size=int(self.VIDEO_SIZE/3)).tolist()

        for i in range(0,len(names)):
            if time in lst_play:
                self.DATASET.loc[i,self.DATASET.columns[2]] = np.random.randint(0, 2, size=1)[0] #Play
            else:
                self.DATASET.loc[i,self.DATASET.columns[2]] = 0 #Play

            if time in lst_pause:
                self.DATASET.loc[i,self.DATASET.columns[3]] = np.random.randint(0, 2, size=1)[0] #Pause
            else:
                self.DATASET.loc[i,self.DATASET.columns[3]] = 0 #Pause

            if time in lst_seek_from:
                self.DATASET.loc[i,self.DATASET.columns[4]] = np.random.randint(0, 4, size=1)[0] #Seek from
            else:
                self.DATASET.loc[i,self.DATASET.columns[4]] = 0 #Seek from

            if time in lst_seek_to:
                self.DATASET.loc[i,self.DATASET.columns[5]] = np.random.randint(0, 4, size=1)[0] #Seek to
            else:
                self.DATASET.loc[i,self.DATASET.columns[5]] = 0 #Seek to

            if time in lst_dropout:
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0, 2, size=1)[0] #Dropout
            else:
                self.DATASET.loc[i,self.DATASET.columns[6]] = 0 #Dropout

            if names[i] != curr:
                curr = names[i]
                time = 0
                self.DATASET.loc[i,self.DATASET.columns[2]] = np.random.randint(1, 20, size=1)[0]

            self.DATASET.loc[i,self.DATASET.columns[1]] = time
            time = time+1

            if time == self.VIDEO_SIZE-3:
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0, 4, size=1)[0]
            elif time == self.VIDEO_SIZE-2:
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0, 5, size=1)[0]
            elif time == self.VIDEO_SIZE-1:
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0, 6, size=1)[0]
            elif time == self.VIDEO_SIZE:
                self.DATASET.loc[i,self.DATASET.columns[6]] = np.random.randint(0, 7, size=1)[0]

        
        length = len(self.DATASET)
        actions = self.DATASET.columns[2:].tolist()
        lst_students = []
        lst_timestamp = []
        lst_action = []
        for i in range(0, length):
            student = self.DATASET.iloc[i,0]
            for j in range(0,len(actions)):
                if (self.DATASET.iloc[i,j+2] == 0):
                    continue

                if(j == 3): #Seek to
                    continue

                lst_students.append(student)
                lst_timestamp.append(datetime.datetime(year=2019, month=np.random.randint(1, 6, size=1)[0], day=np.random.randint(1, 27, size=1)[0], hour=np.random.randint(0, 23, size=1)[0], minute=np.random.randint(0, 59, size=1)[0], second=np.random.randint(0, 59, size=1)[0]))
                
                action = self.textAction[j]+str(self.DATASET.iloc[i,1])+"s"
                if(j == 2): #Seek from adding seek to
                    action = action+self.textAction[3]+str(np.random.randint(0, self.VIDEO_SIZE, size=1)[0])+"s"

                lst_action.append(action)

        self._df_chronology[self._df_chronology.columns[0]] = lst_students
        self._df_chronology[self._df_chronology.columns[1]] = lst_timestamp
        self._df_chronology[self._df_chronology.columns[2]] = lst_action

        self._df_chronology = self._df_chronology.sort_values(by=[self._df_chronology.columns[0],self._df_chronology.columns[1]])

    def get_b1(self, b0, b2):
        # b0, b1 list of x, y coordinates
        if len(b0) != len(b2) != 2:
            raise ValueError('b0, b1 must be lists of two elements')
        b1 = 0.5 * (np.asarray(b0)+np.asarray(b2))+\
            0.5 * np.array([0,1.0]) * np.sqrt(3) * np.linalg.norm(np.array(b2)-np.array(b0))
        return b1.tolist()

    def dim_plus_1(self, b, w):#lift the points b0, b1, b2 to 3D points a0, a1, a2
        #b is a list of 3 lists of 2D points, i.e. a list of three 2-lists 
        #w is a list of numbers (weights) of len equal to the len of b
        if not isinstance(b, list) or  not isinstance(b[0], list):
            raise ValueError('b must be a list of three 2-lists')
        if len(b) != len(w)   != 3:
            raise ValueError('the number of weights must be  equal to the nr of points')
        else:
            a = np.array([point + [w[i]] for (i, point) in enumerate(b)])
            a[1, :2] *= w[1]
            return a

    def bezier_curve(self, bz, nr): #the control point coordinates are passed in a list bz=[bz0, bz1, bz2] 
        # bz is a list of three 2-lists 
        # nr is the number of points to be computed on each arc
        t = np.linspace(0, 1, nr)
        #for each parameter t[i] evaluate a point on the Bezier curve with the de Casteljau algorithm
        N = len(bz) 
        points = [] # the list of points to be computed on the Bezier curve
        for i in range(nr):
            aa = np.copy(bz) 
            for r in range(1, N):
                aa[:N-r,:] = (1-t[i]) * aa[:N-r,:] + t[i] * aa[1:N-r+1,:]  # convex combination of points
            points.append(aa[0,:])
        return np.array(points)

    def rational_bezier_curve(self, a, nr):
        discrete_curve = self.bezier_curve(a, nr)
        return [p[:2]/p[2] for p in discrete_curve]

    # Table presenting raw data
    def graph_01(self):
        legend = {"title":"Número de interações por estudante a cada segundo do vídeo"}
        if (self._language == "en"):
            legend = {"title":"Number of interaction by student in each video time"}
        
        
        trace = [Table(
            header=dict(
                values=list(self.DATASET.columns[:len(self.DATASET.columns)]),
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[self.DATASET[i].tolist() for i in self.DATASET.columns[:len(self.DATASET.columns)]],
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
                id='V009@1',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V009@1","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_02(self):
        legend = {"title":"Número de interações por tempo do vídeo"}
        if (self._language == "en"):
            legend = {"title":"Number of interaction by video time"}
        
        df = pd.DataFrame(columns=self.DATASET.columns[1:].tolist())
        
        for i in range(0,self.VIDEO_SIZE+1):
            df_aux = self.DATASET[self.DATASET.columns[2:]].loc[self.DATASET[self.DATASET.columns[1]] == i].apply(np.sum)
            df.loc[i] = df_aux.append(pd.Series([i],index=[self.DATASET.columns[1]]))

        trace = [Table(
            header=dict(
                values=list(df.columns[:len(df.columns)]),
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[df[i].tolist() for i in df.columns[:len(df.columns)]],
                fill = dict(color='#F5F8FF'),
                align = ['center','center']
            )
        )]

        data = trace
        layout = Layout( title = legend["title"] )
        
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(data, filename = 'pandas_table')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V009@2',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V009@2","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    def graph_03(self):
        legend = {"title":"Cronologia de interações dos alunos"}
        if (self._language == "en"):
            legend = {"title":"Chronology of students' interaction"}

        trace = [Table(
            header=dict(
                values=list(self._df_chronology.columns[:len(self._df_chronology.columns)]),
                fill = dict(color='#C2D4FF'),
                align = 'center'
            ),
            cells=dict(
                values=[self._df_chronology[i].tolist() for i in self._df_chronology.columns[:len(self._df_chronology.columns)]],
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
                id='V009@2',
                figure={"data": data}
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V009@3","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

    #Area Chart
    def graph_04(self):
        legend = {"title":"Número de interações por tempo do vídeo",
                    "xaxis":"Tempo do vídeo em segundos",
                    "yaxis":"Interação",
                }
        if (self._language == "en"):
            legend = {"title":"Number of interaction by video time",
                        "xaxis":"Video time in seconds",
                        "yaxis":"Interaction",
                    }
        
        df = pd.DataFrame(columns=self.DATASET.columns[1:].tolist())
        
        for i in range(0,self.VIDEO_SIZE+1):
            df_aux = self.DATASET[self.DATASET.columns[2:]].loc[self.DATASET[self.DATASET.columns[1]] == i].apply(np.sum)
            df.loc[i] = df_aux.append(pd.Series([i],index=[self.DATASET.columns[1]]))

        color = ["rgb(0,127,127)", "rgb(0,255,0)", "rgb(127,0,127)", "rgb(255,0,0)", "rgb(0,0,255)", "rgb(100,100,100)"]
        trace = []
        for i in range(1,len(df.columns.tolist())):
            trace.append(
                Scatter(
                    x=df[df.columns[0]],
                    y=df[df.columns[i]],
                    # hoverinfo='x+y',
                    hoverinfo='text',
                    hovertext=['<b>'+str(df[df.columns[0]][j])+"s</b>: "+str(df[df.columns[i]][j])+' '+df.columns[i] for j in range(len(df))],
                    mode='lines',
                    name=df.columns[i],
                    text = [df.columns[i]],
                    line=dict(width=0.5, 
                                color=color[i]),
                    stackgroup='one'
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
                # autorange = False,
                # fixedrange = False,
                # range = [0, self.DATASET["AVA Access"].max()+10],
                # rangemode = "normal",
                # zeroline= False,
                # showline = True,
            ),
            yaxis = dict(
                title = legend["yaxis"],
                titlefont=dict(
                    # family='Arial, sans-serif',
                    # size=18,
                    color='rgb(180,180,180)',
                ),
                # autorange = False,
                # fixedrange = False,
                # range = [0, self.DATASET["Predicted Grade"].max()+10],
                # rangemode = "normal",
                # showline = True,
            )
        )

        data = trace
        fig = Figure(data=data, layout=layout)
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='stacked-area')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V009@3',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V009@4","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}
    
    #Arc Diagram
    def graph_05(self):
        legend = {"title":"Interações de seek forward e seek backward por tempo de vídeo"}
        label_from = 'Origem'
        label_to = 'Destino'
        label_prep = ' de '
        if (self._language == "en"):
            legend = {"title":"Interactions of seek forward and seek backward by time"}
            label_from = 'Origin'
            label_to = 'Target'
            label_prep = ' of '

        df_seek = self._df_chronology.loc[(self._df_chronology[self._df_chronology.columns[2]].str.contains('Seek'))]
        df_seek.insert(column='From', loc=len(df_seek.columns), value=df_seek[df_seek.columns[len(df_seek.columns)-1]].apply(lambda x: int(x.replace(self.textAction[2],'').replace('s','').split(self.textAction[3])[0]))) #Get From of each seek
        df_seek.insert(column='To', loc=len(df_seek.columns), value=df_seek[df_seek.columns[len(df_seek.columns)-2]].apply(lambda x: int(x.replace(self.textAction[2],'').replace('s','').split(self.textAction[3])[1]))) #Get to of each seek
        df_seek.insert(column='Type', loc=len(df_seek.columns), value=df_seek.apply(lambda x: 'Forward' if x['From'] < x['To'] else 'Backward', axis=1)) #Classifying seek by Forward or Backward

        values = labels = list(range(self.VIDEO_SIZE+1))

        lst_count_forward_from = [0]*len(values)
        lst_count_forward_to = [0]*len(values)
        lst_count_backward_from = [0]*len(values)
        lst_count_backward_to = [0]*len(values)
        for i in range(len(values)):
            lst_count_forward_from[i] = len(df_seek.loc[(df_seek['Type']=='Forward') & (df_seek['From']==i)])
            lst_count_forward_to[i] = len(df_seek.loc[(df_seek['Type']=='Forward') & (df_seek['To']==i)])
            lst_count_backward_from[i] = len(df_seek.loc[(df_seek['Type']=='Backward') & (df_seek['From']==i)])
            lst_count_backward_to[i] = len(df_seek.loc[(df_seek['Type']=='Backward') & (df_seek['To']==i)])

        #Transform 'from' and 'to' in edge
        se_forward = df_seek.loc[df_seek['Type'] == 'Forward'].apply(lambda x: (x['From'],x['To']), axis=1) 
        se_backward = df_seek.loc[df_seek['Type'] == 'Backward'].apply(lambda x: (x['From'],x['To']), axis=1)

        #Get unique edges
        lst_edge_forward = se_forward.unique().tolist()
        lst_edge_backward = se_backward.unique().tolist()

        #Count how many time each edge is presented
        lst_edge_forward_value = [0]*len(lst_edge_forward)
        lst_edge_backward_value = [0]*len(lst_edge_backward)

        for edge in se_forward.iteritems():
            idx = lst_edge_forward.index(edge[1])
            lst_edge_forward_value[idx] = lst_edge_forward_value[idx] + 1

        for edge in se_backward.iteritems():
            idx = lst_edge_backward.index(edge[1])
            lst_edge_backward_value[idx] = lst_edge_backward_value[idx] + 1
        
        edge_range_value = sorted(set(lst_edge_backward_value+lst_edge_forward_value))
        widths = [0.5+k*0.25 for k in range(5)] + [2+k*0.25 for k in range(4)]+[3, 3.25, 3.75, 4.25, 5, 5.25, 7] #Make list of widths
        d = dict(zip(edge_range_value, widths)) #Match edge_range_value with list of widths
        edge_forward_widths = [d[val] for val in lst_edge_forward_value]
        edge_backward_widths = [d[val] for val in lst_edge_backward_value]

        # Define the trace for nodes placed on the x-axis. The nodes are colored with the colorscale `pl_density`: 
        # pl_density = [[0.0, 'rgb(230,240,240)'],
        #                 [0.1, 'rgb(187,220,228)'],
        #                 [0.2, 'rgb(149,197,226)'],
        #                 [0.3, 'rgb(123,173,227)'],
        #                 [0.4, 'rgb(115,144,227)'],
        #                 [0.5, 'rgb(119,113,213)'],
        #                 [0.6, 'rgb(120,84,186)'],
        #                 [0.7, 'rgb(115,57,151)'],
        #                 [0.8, 'rgb(103,35,112)'],
        #                 [0.9, 'rgb(82,20,69)'],
        #                 [1.0, 'rgb(54,14,36)']]
        trace = []
        # xx = []
        # yy = []

        X = list(range(len(values))) # node x-coordinates
        nr = 75 
        for i, (j, k) in enumerate(lst_edge_forward):            
            b0 = [X[j], 0.0]
            b2 = [X[k], 0.0]
            b1 = self.get_b1(b0, b2)
            a = self.dim_plus_1([b0, b1, b2], [1, 0.5, 1])
            pts = self.rational_bezier_curve(a, nr)
            # xx.append(pts[nr//2][0]) #abscissa of the middle point on the computed arc
            # yy.append(pts[nr//2][1]) #ordinate of the same point
            x,y = zip(*pts)
            
            trace.append( #Forward arcs
                        Scatter(
                            x=x, 
                            y=y, 
                            name='',
                            mode='lines', 
                            line=dict(width=edge_forward_widths[i], color='rgb(0,0,255)', shape='spline'),
                            hoverinfo='none',
                            showlegend = False,
                            )
                        )

        for i, (j, k) in enumerate(lst_edge_backward):
            b0 = [X[j], 0.0]
            b2 = [X[k], 0.0]
            b1 = self.get_b1(b0, b2)
            a = self.dim_plus_1([b0, b1, b2], [1, 0.5, 1])
            pts = self.rational_bezier_curve(a, nr)
            # xx.append(pts[nr//2][0]) #abscissa of the middle point on the computed arc
            # yy.append(pts[nr//2][1]) #ordinate of the same point
            x,y = zip(*pts)
            y = tuple([-1*iterator for iterator in y]) #Make opposite axes            
            
            trace.append( #Backward arcs
                        Scatter(
                            x=x, 
                            y=y, 
                            name='',
                            mode='lines', 
                            line=dict(width=edge_backward_widths[i], color='rgb(255,0,0)', shape='spline'),
                            hoverinfo='none',
                            showlegend = False
                            )
                        )

        trace.append( #Nodes
                    Scatter(
                        x=list(range(len(values))),
                        y=[0]*len(values),
                        mode='markers+text',
                        # name="Cluster"+str(i+1), #each cluster name
                        text = [str(i)+'s' for i in range(len(values))],
                        textposition='middle center',
                        hovertext = ['<b>Seek Forward</b><br>'+label_from+label_prep+str(lst_count_forward_from[i])+" seek(s)<br>"+label_to+label_prep+str(lst_count_forward_to[i])+" seek(s)<br><br><b>"+str(i)+"s</b><br><br><b>Seek Backward</b><br>"+label_from+label_prep+str(lst_count_backward_from[i])+" seek(s)<br>"+label_to+label_prep+str(lst_count_backward_to[i])+" seek(s)" for i in range(len(values))],
                        # lst_count_forward[i]
                        # lst_count_backward[i]
                        hoverinfo='text',
                        # hoverlabel_align = 'right',
                        showlegend = False,
                        # marker=dict(size=20, color = 'rgb(100,100,100)', symbol='circle', line=dict(color='rgb(0,0,255)', width=3.75))
                        marker=dict(size=25, color = 'rgb(200,200,200)', symbol='circle')
                    )
                )

        trace.append( #Legend
                    Scatter(
                        x=[len(values)-2]*2,
                        y=[5,-5],
                        mode='markers+text',
                        # name="Cluster"+str(i+1), #each cluster name
                        text = ['<b> Seek Forward</b>', '<b> Seek Backward</b>'],
                        textposition='middle right',
                        hoverinfo='none',
                        showlegend = False,
                        marker=dict(size=[20]*2, color = ['rgb(0,0,255)','rgb(255,0,0)'], symbol=141, line=dict(width=3))
                    )
                )

        layout=Layout(
                title = legend["title"],
                autosize=True,
                font=dict(size=10), 
                # width=1500,
                # height=1250,
                showlegend=True,
                hovermode='closest',
                xaxis=dict(anchor='y', showline=False, zeroline=False, showgrid=False, 
                            showticklabels=False, tickvals=list(range(len(values))), ticktext=labels, tickangle=50,
                            ),
                yaxis=dict(visible=False),
                margin=dict(t=80, b=110, l=10, r=10),                
                # annotations=[dict(showarrow=False, 
                #         #    text=anno_text,
                #            xref='paper',     
                #            yref='paper',     
                #            x=0.05,  
                #            y=-0.3,  
                #            xanchor='left',   
                #            yanchor='bottom',  
                #            font=dict(size=11 ))
                #                   ]
            )
        
        data = trace
        fig = Figure(data=data, layout=layout)
        
        if self._type_result == "jupyter-notebook":
            iplot(fig, filename='Scatter')
        elif self._type_result == "dash":
            return dcc.Graph(
                id='V009@5',
                figure=fig
            )
        elif self._type_result == "flask":
            modeBarButtonsToRemove = ['toImage', 'sendDataToCloud', 'hoverCompareCartesian', 'lasso2d', 'hoverClosestCartesian', 'toggleHover', 'hoverClosest3d', 'hoverClosestGeo', 'hoverClosestGl2d', 'hoverClosestPie']
            config = {"displaylogo": False, "responsive": True, "displayModeBar": True, "modeBarButtonsToRemove": modeBarButtonsToRemove}
            return {"id":"V009@5","layout":json.dumps({"data": data, "layout": layout, "config": config}, cls=PlotlyJSONEncoder)}

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
        else:
            print("V009@"+str(id)+" not found")

    def get_preprocessed_chart(self,id):
        if not os.path.exists(self._preprocessed_folder):
            print('There is no preprocessed folder')
            return
        
        file_name = 'V009_'+str(id)+'.pkl'
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
        
        file_name = 'V009_'+str(id)+'.pkl'
        file_path = os.path.join(self._preprocessed_folder,file_name)
        f = open(file_path,'wb')
        pickle.dump(self.get_chart(id),f)
        f.close()

        self._type_result = aux_type_result

    def print_all_graphs(self,language="pt"):
        self._language = language
        self.graph_01() #Raw Table
        self.graph_02() 
        self.graph_03()
        self.graph_04() #Area Chart
        self.graph_05() #Arc Diagram

# instance = V009()
# instance.generate_dataset(number_actions = 100, video_size = 30)
# res = instance.graph_03()