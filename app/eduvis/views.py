from flask import Blueprint, request, render_template, flash, Response, g, session, redirect, url_for
from flask_wtf import Form
from sqlalchemy import and_, update

import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

import dateutil.parser
from datetime import datetime
from dateutil.relativedelta import relativedelta

# local application imports
from app.eduvis.constants import DEFAULT_USER_ID
from app.eduvis.constants import DEFAULT_STATIC_DASHBOARD_ID
from app.eduvis.constants import DEFAULT_CUSTOMIZABLE_DASHBOARD_ID
from app.eduvis.constants import STATIC_DASHBOARD_TYPE
from app.eduvis.constants import CUSTOMIZABLE_DASHBOARD_TYPE
from app.eduvis.constants import LST_VIEW_INFORMATION
from app.eduvis.constants import LST_EVALUATION_TAM

# from app import db
from app.eduvis.backend.dashboard import Dashboard
from app.eduvis.backend.connection_db import Connection_DB

from app.eduvis.backend.user import User

from app.eduvis.backend.access import Access
from app.eduvis.backend.assignment import Assignment
from app.eduvis.backend.cluster import Cluster
from app.eduvis.backend.prediction import Prediction
from app.eduvis.backend.material import Material
from app.eduvis.backend.forum import Forum
from app.eduvis.backend.video_access import Video_Access
from app.eduvis.backend.age import Age
from app.eduvis.backend.video_interaction import Video_Interaction
from app.eduvis.backend.video_understood import Video_Understood
from app.eduvis.backend.navigation import Navigation

mod = Blueprint("eduvis", __name__, url_prefix='/eduvis')

_conn = Connection_DB()

_user_id = None

def load_user_info():
    rule = request.url_rule
    print("Pagina:"+str(rule))
    if (str(rule) == "/eduvis/invite/" or str(rule) == "/eduvis/"):
        print('Reset session')
        session['user_eduvis'] = ""

    global _user_id
    print("----------------load_user_info()----------------")
    # session['user_eduvis'] = 'Sessão Works'
    # print(session['user_eduvis'])
    # session['user_eduvis'] = ""
    if session['user_eduvis'] != "":
        print("----------------_user_id = session[user_eduvis]----------------")
        _user_id = session['user_eduvis']
        print(_user_id)
    else:
        print("----------------_user_id = DEFAULT_USER_ID----------------")
        session['user_eduvis'] = ""
        _user_id = DEFAULT_USER_ID
        print(_user_id)
    
    # print("--------------------------------------------------")
    # print("load_user_info()")
    # print(_user_id)
    # print("--------------------------------------------------")

def left_menu_info_UNASUS():
    lst_left_menu_info = []
    lst_left_menu_info.append({"id":"assignments", "label_pt":"Atividades", "label_en":"Assignments completion", "sub_menu":["atividades completadas", "estudantes que completaram"], "view":1})
    lst_left_menu_info.append({"id":"materials", "label_pt":"Materiais acessados", "label_en":"Materials accessed", "sub_menu":["estudantes que acessaram", "materiais mais acessados"], "view":2})
    lst_left_menu_info.append({"id":"forum", "label_pt":"Uso do fórum", "label_en":"Forum usage", "sub_menu":[], "view":3})
    lst_left_menu_info.append({"id":"cluster", "label_pt":"Correlação entre notas", "label_en":"Student clusters", "sub_menu":["acessos ao ambiente", "atividades completadas", "materiais acessados", "acesso ao fórum", "postagens no fórum"], "view":5})
    lst_left_menu_info.append({"id":"prediction", "label_pt":"Predição de performance", "label_en":"Performance prediction", "sub_menu":[], "view":7})
    lst_left_menu_info.append({"id":"access", "label_pt":"Acesso dos estudantes", "label_en":"Student access", "sub_menu":["acessos por dia", "acessos por semana"], "view":8})

    # sorted_list = sorted(lst_left_menu_info, key=lambda k: k['label_en'])
    sorted_list = sorted(lst_left_menu_info, key=lambda k: k['label_pt'])
    return sorted_list

def left_menu_info():
    lst = LST_VIEW_INFORMATION
    
    lst_left_menu_info = []
    for i in range(len(lst)):
        sub_menu=[]
        lst_question = lst[i]["Questions"]
        if len(lst_question) > 1:
            for j in range(len(lst_question)):
                sub_menu.append(lst_question[j]["Label_pt"])
            # sub_menu = sorted(sub_menu)

        curr_dict = {"id":lst[i]["id"], "label_pt":lst[i]["Label_pt"], "label_en":lst[i]["Label_en"],"view":int(lst[i]["View"].replace("V","")),"sub_menu":sub_menu}

        lst_left_menu_info.append(curr_dict)

    # sorted_list = sorted(lst_left_menu_info, key=lambda k: k['label_en'])
    sorted_list = sorted(lst_left_menu_info, key=lambda k: k['label_pt'])
    return sorted_list

@mod.before_request
def before_request():
    # app_before_request()
    load_user_info()

@mod.route('/')
def index():
    # Redirecionar para a tela de entrevista inicial    
    return redirect('/eduvis/invite/')
    # return redirect('/eduvis/interview/aboutyou/')
    # return redirect('/eduvis/interview/avaxp/')
    # return redirect('/eduvis/interview/data/')
    # return redirect('/eduvis/dashboard/')

@mod.route('/invite/')
def invite():    
    return render_template('eduvis/frontend/invite.html')

@mod.route('/post_invite/', methods=['POST'])
def invite_data():
    if request.method == 'POST':
        print("--------------------------------post_invite--------------------------------")
    else:
        pass
    
    return redirect('/eduvis/interview/aboutyou/')

def check_data(data):
    return '' in list(data.values())

@mod.route('/interview/aboutyou/')
def aboutyou():
    return render_template('eduvis/frontend/interview/aboutyou.html', data={})

@mod.route('/interview/aboutyou/save/', methods=['POST'])
def aboutyou_save():
    if request.method == 'POST':        
        print("--------------------------------post_aboutyou--------------------------------")
        data = {'nomecompleto':request.form['nomecompleto'],
                'idade':request.form['idade'],
                'localorigem':request.form['localorigem'],
                'localtrabalho':request.form['localtrabalho'],
                'areaformacao':request.form['areaformacao'],
                'escolaridade':request.form['escolaridade'],
                'profissao':request.form['profissao'],
                'avaxp':request.form['avaxp']}
        print(data)
        
        print("----------------Set Session----------------")
        if '' in list(data.values()):
            return render_template('eduvis/frontend/interview/aboutyou.html', data=data)
        else:
            user = User(_conn)
            if session['user_eduvis'] == "":
                user_id = user.record_about_user(data)
                session['user_eduvis'] = user_id
                print("----------------user_id----------------")
                print(user_id)
                print("----------------Session----------------")
                print(session['user_eduvis'])
            else:
                user_id = session['user_eduvis']
                user.record_about_user(data, user_id)
            
            if int(data['avaxp'])==0:
                return redirect('/eduvis/interview/data/')
        print("----------------End Set Session----------------")
    else:
        pass

    return redirect('/eduvis/interview/avaxp/')

@mod.route('/interview/avaxp/')
def avaxp():
    return render_template('eduvis/frontend/interview/avaxp.html', data={})

@mod.route('/interview/avaxp/save/', methods=['POST'])
def avaxp_save():
    if request.method == 'POST':
        print("--------------------------------post_avaxp--------------------------------")
        data = {'papeisavas':request.form['papeisavas'],
                'tempoexpavas':request.form['tempoexpavas'],
                'instituicao':request.form['instituicao'],
                'disciplinas':request.form['disciplinas'],
                'avaxp':request.form['avaxp'],
                'avasusados':request.form['avasusados'],
                'recursosusados':request.form['recursosusados'],
                'idadealunos':request.form['idadealunos'],
                'inforelevante':request.form['inforelevante']}
        print(data)

        if '' in list(data.values()):
            return render_template('eduvis/frontend/interview/avaxp.html', data=data)
        else:
            user = User(_conn)
            user.record_ava_xp(data, _user_id)
    else:
        pass
    
    return redirect('/eduvis/interview/data/')

@mod.route('/interview/data/')
def data(data={}):
    lst = LST_VIEW_INFORMATION
    
    lst_topics = []
    for i in range(len(lst)):
        sub_topic=[]
        lst_question = lst[i]["Questions"]
    
        for j in range(len(lst_question)):
            sub_topic.append({"id":lst_question[j]["id"],"label_pt":lst_question[j]["Sub_topic"]})
    
        curr_dict = {"label_pt":lst[i]["Label_pt"],"view":int(lst[i]["View"].replace("V","")),"sub_topic":sub_topic}
    
        lst_topics.append(curr_dict)
    
    sorted_list = sorted(lst_topics, key=lambda k: k['label_pt'])
    
    return render_template('eduvis/frontend/interview/data.html', selecting=sorted_list, data=data)

@mod.route('/interview/data/save/', methods=['POST'])
def data_save():
    if request.method == 'POST':
        print("--------------------------------post_data--------------------------------")
        keys = []
        form = request.form
        for key in form.keys():
            keys.append(key)
            
        print(keys)

        data = {}
        lst = LST_VIEW_INFORMATION
        for i in range(len(lst)):
            lst_question = lst[i]["Questions"]
            for j in range(len(lst_question)):
                if lst_question[j]["id"] in keys:
                    data[lst_question[j]["id"]] = request.form[lst_question[j]["id"]]
                else:
                    data[lst_question[j]["id"]] = ''

        data['gostariadado'] = request.form['gostariadado']
        data['comoapresentar'] = request.form['comoapresentar']
        print(data)

        if '' in list(data.values()):
            lst_topics = []
            for i in range(len(lst)):
                sub_topic = []
                lst_question = lst[i]["Questions"]
            
                for j in range(len(lst_question)):
                    sub_topic.append({"id":lst_question[j]["id"],"label_pt":lst_question[j]["Sub_topic"]})
            
                curr_dict = {"label_pt":lst[i]["Label_pt"],"view":int(lst[i]["View"].replace("V","")),"sub_topic":sub_topic}
            
                lst_topics.append(curr_dict)
            
            sorted_list = sorted(lst_topics, key=lambda k: k['label_pt'])
            return render_template('eduvis/frontend/interview/data.html', selecting=sorted_list, data=data)
        else:
            user = User(_conn)
            user.record_data(data, _user_id)
    else:
        pass
    
    return redirect('/eduvis/interview/visualizationxp/')

@mod.route('/interview/visualizationxp/')
def visualizationxp():
    return render_template('eduvis/frontend/interview/visualizationxp.html', data={})

@mod.route('/interview/visualizationxp/save/', methods=['POST'])
def visualizationxp_save():
    if request.method == 'POST':
        print("--------------------------------post_visualizationxp--------------------------------")
        data = {'frequencialeitura':request.form['frequencialeitura'],
                'frequenciacria':request.form['frequenciacria']}
        print(data)

        if '' in list(data.values()):
            return render_template('eduvis/frontend/interview/visualizationxp.html', data=data)
        else:
            user = User(_conn)
            user.record_visualization_xp(data, _user_id)
    else:
        pass
    
    return redirect('/eduvis/static_dashboard/')

@mod.route('/evaluation_static_dashboard/')
def evaluation_static_dashboard():
    user = User(_conn)
    dashboard = Dashboard(_conn, _user_id, user.get_static_dashboard_id(_user_id), STATIC_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/evaluate.html', userName=user.get_name(_user_id), dashboardType='static', charts_topic=dashboard.topic(), charts_id=dashboard.charts("id"), charts_layout=dashboard.charts("layout"), titleCharts=dashboard.title(), post_action="/eduvis/evaluation_static_dashboard/save/", data={})

@mod.route('/evaluation_static_dashboard/save/', methods=['POST'])
def evaluation_static_dashboard_save():
    if request.method == 'POST':
        print("--------------------------------post_evaluation_static_dashboard--------------------------------")

        user = User(_conn)
        dashboard = Dashboard(_conn, _user_id, user.get_static_dashboard_id(_user_id), STATIC_DASHBOARD_TYPE)
        topics = dashboard.topic()
        charts = dashboard.charts("id")

        keys = []
        form = request.form
        for key in form.keys():
            keys.append(key)

        data = {}
        for i in range(0,len(charts)):
            name = "T"+str(topics[i])+"@"+str(charts[i])
            data[name] = request.form[name]
            
            name = "T"+str(topics[i])+"@"+str(charts[i])+"#Radio"
            if name in keys:
                data[name] = request.form[name]
            else:
                data[name] = ''
        print(data)

        if '' in list(data.values()):
            return render_template('eduvis/frontend/dashboard/evaluate.html', userName=user.get_name(_user_id), dashboardType='static', charts_topic=dashboard.topic(), charts_id=dashboard.charts("id"), charts_layout=dashboard.charts("layout"), titleCharts=dashboard.title(), post_action="/eduvis/evaluation_static_dashboard/save/", data=data)
        else:
            user.record_evaluation_dashboard(STATIC_DASHBOARD_TYPE, data, _user_id)
    else:
        pass

    return redirect('/eduvis/customizable_dashboard/')

@mod.route('/evaluation_customizable_dashboard/')
def evaluation_customizable_dashboard():
    user = User(_conn)
    dashboard = Dashboard(_conn, _user_id, user.get_customizable_dashboard_id(_user_id), CUSTOMIZABLE_DASHBOARD_TYPE)

    if (dashboard.has_active_without_default_charts()):
        return render_template('eduvis/frontend/dashboard/evaluate.html', userName=user.get_name(_user_id), dashboardType='customizable', charts_topic=dashboard.topic(without_default_charts=True), charts_id=dashboard.charts("id",without_default_charts=True), charts_layout=dashboard.charts("layout",without_default_charts=True), titleCharts=dashboard.title(without_default_charts=True), post_action="/eduvis/evaluation_customizable_dashboard/save/", data={})
    elif (dashboard.has_inactive_default_charts()):
        return redirect('/eduvis/modification_customizable_dashboard/')
    else:
        return redirect('/eduvis/interview/evaluation/')

@mod.route('/evaluation_customizable_dashboard/save/', methods=['POST'])
def evaluation_customizable_dashboard_save():
    if request.method == 'POST':
        print("--------------------------------post_evaluation_customizable_dashboard--------------------------------")

        user = User(_conn)
        dashboard = Dashboard(_conn, _user_id, user.get_customizable_dashboard_id(_user_id), CUSTOMIZABLE_DASHBOARD_TYPE)
        topics = dashboard.topic(without_default_charts=True)
        charts = dashboard.charts("id",without_default_charts=True)

        keys = []
        form = request.form
        for key in form.keys():
            keys.append(key)

        data = {}
        for i in range(0,len(charts)):
            name = "T"+str(topics[i])+"@"+str(charts[i])
            data[name] = request.form[name]

            name = "T"+str(topics[i])+"@"+str(charts[i])+"#Radio"
            if name in keys:
                data[name] = request.form[name]
            else:
                data[name] = ''
        print(data)

        if '' in list(data.values()):
            return render_template('eduvis/frontend/dashboard/evaluate.html', userName=user.get_name(_user_id), dashboardType='customizable', charts_topic=dashboard.topic(without_default_charts=True), charts_id=dashboard.charts("id",without_default_charts=True), charts_layout=dashboard.charts("layout",without_default_charts=True), titleCharts=dashboard.title(without_default_charts=True), post_action="/eduvis/evaluation_customizable_dashboard/save/", data=data)
        else:
            user.record_evaluation_dashboard(CUSTOMIZABLE_DASHBOARD_TYPE, data, _user_id)
    else:
        pass
    
    if(dashboard.has_inactive_default_charts()):
        return redirect('/eduvis/modification_customizable_dashboard/')
    else:
        return redirect('/eduvis/interview/evaluation/')

@mod.route('/modification_customizable_dashboard/')
def modification_customizable_dashboard():
    user = User(_conn)
    dashboard = Dashboard(_conn, _user_id, user.get_customizable_dashboard_id(_user_id), CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/modification.html', userName=user.get_name(_user_id), dashboardType='customizable', charts_topic=dashboard.topic(default_charts_inactive=True), charts_id=dashboard.charts("id",default_charts_inactive=True), charts_layout=dashboard.charts("layout",default_charts_inactive=True), titleCharts=dashboard.title(default_charts_inactive=True), post_action="/eduvis/modification_customizable_dashboard/save/", data={})

@mod.route('/modification_customizable_dashboard/save/', methods=['POST'])
def modification_customizable_dashboard_save():
    if request.method == 'POST':
        print("--------------------------------post_modification_customizable_dashboard--------------------------------")

        user = User(_conn)
        dashboard = Dashboard(_conn, _user_id, user.get_customizable_dashboard_id(_user_id), CUSTOMIZABLE_DASHBOARD_TYPE)
        topics = dashboard.topic(default_charts_inactive=True)
        charts = dashboard.charts("id",default_charts_inactive=True)

        data = {}
        for i in range(0,len(charts)):
            name = "T"+str(topics[i])+"@"+str(charts[i])
            data[name] = request.form[name]

        print(data)

        if '' in list(data.values()):
            return render_template('eduvis/frontend/dashboard/modification.html', userName=user.get_name(_user_id), dashboardType='customizable', charts_topic=dashboard.topic(default_charts_inactive=True), charts_id=dashboard.charts("id",default_charts_inactive=True), charts_layout=dashboard.charts("layout",default_charts_inactive=True), titleCharts=dashboard.title(default_charts_inactive=True), post_action="/eduvis/modification_customizable_dashboard/save/", data=data)
        else:
            user.record_evaluation_dashboard(CUSTOMIZABLE_DASHBOARD_TYPE, data, _user_id, evaluation=False)            
    else:
        pass

    return redirect('/eduvis/interview/evaluation/')

@mod.route('/interview/evaluation/')
def evaluation_dashboard():
    user = User(_conn)
    return render_template('eduvis/frontend/interview/tam.html', userName=user.get_name(_user_id), questions=LST_EVALUATION_TAM, data={})

@mod.route('/interview/evaluation/save/', methods=['POST'])
def evaluation_dashboard_save():
    if request.method == 'POST':
        print("--------------------------------post_evaluation_dashboard--------------------------------")

        user = User(_conn)
        
        keys = []
        form = request.form
        print('form')
        print(form)
        for key in form.keys():
            keys.append(key)
        
        data = {}
        ids = list(LST_EVALUATION_TAM.keys())
        for i in range(0,len(ids)):
            name = str(ids[i])
            if name in keys:
                data[name] = request.form[name]
            else:
                data[name] = ''
        print(data)
        
        if '' in list(data.values()):
            return render_template('eduvis/frontend/interview/tam.html', userName=user.get_name(_user_id), questions=LST_EVALUATION_TAM, data=data)
        else:
            user.record_evaluation_tam(_user_id,CUSTOMIZABLE_DASHBOARD_TYPE, data)
    else:
        pass

    return redirect('/eduvis/thankyou/')

@mod.route('/static_dashboard/')
def static_dashboard():
    user = User(_conn)
    dashboard = Dashboard(_conn, _user_id, user.get_static_dashboard_id(_user_id), STATIC_DASHBOARD_TYPE)
    session['type_dashboard'] = STATIC_DASHBOARD_TYPE
    return render_template('eduvis/frontend/dashboard/dashboard.html', userName=user.get_name(_user_id), charts_topic=dashboard.topic(), charts_id=dashboard.charts("id"), charts_layout=dashboard.charts("layout"), titleCharts=dashboard.title(), enableLeftMenu=STATIC_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/customizable_dashboard/')
def customizable_dashboard():
    user = User(_conn)
    dashboard = Dashboard(_conn, _user_id, user.get_customizable_dashboard_id(_user_id), CUSTOMIZABLE_DASHBOARD_TYPE)
    session['type_dashboard'] = CUSTOMIZABLE_DASHBOARD_TYPE
    return render_template('eduvis/frontend/dashboard/dashboard.html', userName=user.get_name(_user_id), charts_topic=dashboard.topic(), charts_id=dashboard.charts("id"), charts_layout=dashboard.charts("layout"), titleCharts=dashboard.title(), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/thankyou/')
def thankyou():
    return render_template('eduvis/frontend/thankyou.html')    

@mod.route('/add_chart/', methods=['POST'])
def add_chart():
    raw_data = json.loads(request.data.decode("utf-8"))
    
    # print(raw_data)
    # print(type(raw_data))
    # print("-----------------------")
    # print(raw_data['chart'])
    # print(type(raw_data['chart']))
    # print("-----------------------")
    # print(raw_data['value'])
    # print(type(raw_data['value']))
    
    # now = datetime.now()
    # current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # # _conn.create_database()
    # # data = ""
    # data = ("André Luiz", current_time)
    # _conn.insert("tb_user",data)
    user = User(_conn)
    dashboard = Dashboard(_conn, _user_id, user.get_customizable_dashboard_id(_user_id), CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard.set_dashboard(raw_data)

    resp = Response(json.dumps('OK'), mimetype='application/json')
    resp.status_code = 200
    return resp

@mod.route('/set_order/', methods=['POST'])
def set_order():
    raw_data = json.loads(request.data.decode("utf-8"))
    
    print("Set Order")
    print(raw_data)
    
    user = User(_conn)

    if (session['type_dashboard'] == STATIC_DASHBOARD_TYPE):
        print('static_dashboard')
        dashboard = Dashboard(_conn, _user_id, user.get_static_dashboard_id(_user_id), STATIC_DASHBOARD_TYPE)
        dashboard.set_order(raw_data)
    elif (session['type_dashboard'] == CUSTOMIZABLE_DASHBOARD_TYPE):
        print('customizable_dashboard')
        dashboard = Dashboard(_conn, _user_id, user.get_customizable_dashboard_id(_user_id), CUSTOMIZABLE_DASHBOARD_TYPE)
        dashboard.set_order(raw_data)

    resp = Response(json.dumps('OK'), mimetype='application/json')
    resp.status_code = 200
    return resp

@mod.route('/access1/')
def access1(): # <!-- VG-08 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    access = Access(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=access.charts("day","id"), charts_layout=access.charts("day","layout"), titleCharts=access.title("day"), topic=access.topic("day"), charts_active=access.charts_active("day"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/access2/')
def access2(): # <!-- VG-08 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    access = Access(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=access.charts("week","id"), charts_layout=access.charts("week","layout"), titleCharts=access.title("week"), topic=access.topic("week"), charts_active=access.charts_active("week"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/assignments1/')
def assignments1(): # <!-- VG-01 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    assignment = Assignment(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=assignment.charts("student","id"), charts_layout=assignment.charts("student","layout"), titleCharts=assignment.title("student"), topic=assignment.topic("student"), charts_active=assignment.charts_active("student"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/assignments2/')
def assignments2(): # <!-- VG-01 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    assignment = Assignment(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=assignment.charts("assignment","id"), charts_layout=assignment.charts("assignment","layout"), titleCharts=assignment.title("assignment"), topic=assignment.topic("assignment"), charts_active=assignment.charts_active("assignment"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/cluster1/')
def cluster1(): # <!-- VG-05 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    cluster = Cluster(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=cluster.charts("grades_access","id"), charts_layout=cluster.charts("grades_access","layout"), titleCharts=cluster.title("grades_access"), topic=cluster.topic("grades_access"), charts_active=cluster.charts_active("grades_access"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/cluster2/')
def cluster2(): # <!-- VG-05 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    cluster = Cluster(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=cluster.charts("grades_assignments","id"), charts_layout=cluster.charts("grades_assignments","layout"), titleCharts=cluster.title("grades_assignments"), topic=cluster.topic("grades_assignments"), charts_active=cluster.charts_active("grades_assignments"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/cluster3/')
def cluster3(): # <!-- VG-05 -->    
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    cluster = Cluster(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=cluster.charts("grades_access_materials","id"), charts_layout=cluster.charts("grades_access_materials","layout"), titleCharts=cluster.title("grades_access_materials"), topic=cluster.topic("grades_access_materials"), charts_active=cluster.charts_active("grades_access_materials"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/cluster4/')
def cluster4(): # <!-- VG-05 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    cluster = Cluster(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=cluster.charts("grades_access_forum","id"), charts_layout=cluster.charts("grades_access_forum","layout"), titleCharts=cluster.title("grades_access_forum"), topic=cluster.topic("grades_access_forum"), charts_active=cluster.charts_active("grades_access_forum"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/cluster5/')
def cluster5(): # <!-- VG-05 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    cluster = Cluster(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=cluster.charts("grades_forum_post","id"), charts_layout=cluster.charts("grades_forum_post","layout"), titleCharts=cluster.title("grades_forum_post"), topic=cluster.topic("grades_forum_post"), charts_active=cluster.charts_active("grades_forum_post"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/cluster6/')
def cluster6(): # <!-- VG-05 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    cluster = Cluster(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=cluster.charts("grades_forum_reply","id"), charts_layout=cluster.charts("grades_forum_reply","layout"), titleCharts=cluster.title("grades_forum_reply"), topic=cluster.topic("grades_forum_reply"), charts_active=cluster.charts_active("grades_forum_reply"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/cluster7/')
def cluster7(): # <!-- VG-05 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    cluster = Cluster(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=cluster.charts("grades_forum_thread","id"), charts_layout=cluster.charts("grades_forum_thread","layout"), titleCharts=cluster.title("grades_forum_thread"), topic=cluster.topic("grades_forum_thread"), charts_active=cluster.charts_active("grades_forum_thread"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/prediction1/')
def prediction1(): # <!-- VG-07 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    prediction = Prediction(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=prediction.charts("id"), charts_layout=prediction.charts("layout"), titleCharts=prediction.title(), topic=prediction.topic(), charts_active=prediction.charts_active(), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/materials1/')
def materials1(): #  <!-- VG-02 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    material = Material(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=material.charts("access_students","id"), charts_layout=material.charts("access_students","layout"), titleCharts=material.title("access_students"), topic=material.topic("access_students"), charts_active=material.charts_active("access_students"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/materials2/')
def materials2(): #  <!-- VG-02 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    material = Material(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=material.charts("access_materials","id"), charts_layout=material.charts("access_materials","layout"), titleCharts=material.title("access_materials"), topic=material.topic("access_materials"), charts_active=material.charts_active("access_materials"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/forum1/')
def forum1(): # <!-- VG-03 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    forum = Forum(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=forum.charts("id"), charts_layout=forum.charts("layout"), titleCharts=forum.title(), topic=forum.topic(), charts_active=forum.charts_active(), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/video_access1/')
def video_access1(): # <!-- VG-04 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    video_access = Video_Access(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=video_access.charts("id"), charts_layout=video_access.charts("layout"), titleCharts=video_access.title(), topic=video_access.topic(), charts_active=video_access.charts_active(), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/age1/')
def age1(): # <!-- VG-06 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    age = Age(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=age.charts("age_access_forum","id"), charts_layout=age.charts("age_access_forum","layout"), titleCharts=age.title("age_access_forum"), topic=age.topic("age_access_forum"), charts_active=age.charts_active("age_access_forum"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/age2/')
def age2(): # <!-- VG-06 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    age = Age(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=age.charts("age_forum_post","id"), charts_layout=age.charts("age_forum_post","layout"), titleCharts=age.title("age_forum_post"), topic=age.topic("age_forum_post"), charts_active=age.charts_active("age_forum_post"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/age3/')
def age3(): # <!-- VG-06 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    age = Age(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=age.charts("age_forum_reply","id"), charts_layout=age.charts("age_forum_reply","layout"), titleCharts=age.title("age_forum_reply"), topic=age.topic("age_forum_reply"), charts_active=age.charts_active("age_forum_reply"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/age4/')
def age4(): # <!-- VG-06 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    age = Age(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=age.charts("age_forum_topic","id"), charts_layout=age.charts("age_forum_topic","layout"), titleCharts=age.title("age_forum_topic"), topic=age.topic("age_forum_topic"), charts_active=age.charts_active("age_forum_topic"), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/video_interaction1/')
def video_interaction1(): # <!-- VG-09 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    video_interaction = Video_Interaction(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=video_interaction.charts("id"), charts_layout=video_interaction.charts("layout"), titleCharts=video_interaction.title(), topic=video_interaction.topic(), charts_active=video_interaction.charts_active(), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/video_understood1/')
def video_understood1(): # <!-- VG-10 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    video_understood = Video_Understood(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=video_understood.charts("id"), charts_layout=video_understood.charts("layout"), titleCharts=video_understood.title(), topic=video_understood.topic(), charts_active=video_understood.charts_active(), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())

@mod.route('/navigation1/')
def navigation1(): # <!-- VG-11 -->
    user = User(_conn)
    customizable_dashboard_id = user.get_customizable_dashboard_id(_user_id)
    navigation = Navigation(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    dashboard = Dashboard(_conn, _user_id, customizable_dashboard_id, CUSTOMIZABLE_DASHBOARD_TYPE)
    return render_template('eduvis/frontend/dashboard/configure.html', userName=user.get_name(_user_id), charts_id=navigation.charts("id"), charts_layout=navigation.charts("layout"), titleCharts=navigation.title(), topic=navigation.topic(), charts_active=navigation.charts_active(), enableLeftMenu=CUSTOMIZABLE_DASHBOARD_TYPE, leftMenuInfo=left_menu_info(), amountSelectedVG=dashboard.amount_by_view())