# Default values
DEFAULT_USER_ID = 1
DEFAULT_STATIC_DASHBOARD_ID = 1
DEFAULT_CUSTOMIZABLE_DASHBOARD_ID = 2
STATIC_DASHBOARD_TYPE = 0
CUSTOMIZABLE_DASHBOARD_TYPE = 1

LANGUAGE = 'pt'
# LANGUAGE = 'en'
RANDOM_NUMBER_STUDENTS = 30

LST_VIEW_INFORMATION = []
LST_VIEW_INFORMATION.append({"View":"V001","Topic":"Tarefas", "id":"assignments", "Label_pt":"Atividades", "Label_en":"Assignments completion",
                             "Questions":[{"id":"1","Question":"Quais estudantes fizeram e não fizeram as tarefas?","Sub_topic":"Estudantes que fizeram e não fizeram as tarefas","Label_pt":"estudantes que completaram"},
                                          {"id":"2","Question":"Quais tarefas foram e não foram feitas pelos estudantes?","Sub_topic":"Tarefas feitas e não feitas pelos estudantes","Label_pt":"atividades completadas"}]})
LST_VIEW_INFORMATION.append({"View":"V002","Topic":"Acesso dos estudantes aos materiais (ex: videos, ebooks, etc)", "id":"materials", "Label_pt": "Materiais acessados", "Label_en": "Materials accessed",
                             "Questions":[{"id":"3","Question":"Quais os estudantes que mais acessaram os materias?","Sub_topic":"Acesso dos estudantes aos materiais (ex: videos, ebooks, etc)","Label_pt":"estudantes que acessaram"},
                                          {"id":"4","Question":"Quais os materiais mais acessados pelos estudantes?","Sub_topic":"Materiais mais acessados pelos estudantes (ex: videos, ebooks, etc)","Label_pt":"materiais mais acessados"}]})
LST_VIEW_INFORMATION.append({"View":"V003","Topic":"Interação dos estudantes no fórum (ex: postagens, acessos, etc)", "id":"forum", "Label_pt": "Uso do fórum", "Label_en": "Forum usage",
                             "Questions":[{"id":"5","Question":"Qual o número de acessos, postagens e curtidas dos estudantes?","Sub_topic":"Número de acessos, postagens e curtidas dos estudantes","Label_pt":"Uso do fórum"}]})
LST_VIEW_INFORMATION.append({"View":"V004","Topic":"Tempo de permanência dos estudantes nos vídeos", "id":"video_access", "Label_pt": "Videos accessados", "Label_en": "Video accessed",
                             "Questions":[{"id":"6","Question":"Qual tempo de permanência dos estudantes nos vídeos?","Sub_topic":"Tempo de permanência dos estudantes nos vídeos","Label_pt":"Videos accessados"}]})
LST_VIEW_INFORMATION.append({"View":"V005","Topic":"Correlação entre as notas e os dados de acesso/interação dos estudantes", "id":"cluster", "Label_pt": "Correlação entre notas", "Label_en": "Student clusters",
                             "Questions":[{"id":"7","Question":"Qual a correlação entre as notas e os dados de acesso no AVA?","Sub_topic":"Correlação entre as notas e os dados de acesso no AVA","Label_pt":"acesso ao AVA"},
                                          {"id":"9","Question":"Qual a correlação entre as notas e a quantidade de tarefas feitas?","Sub_topic":"Correlação entre as notas e a quantidade de tarefas feitas","Label_pt": "atividades completadas"},
                                          {"id":"8","Question":"Qual a correlação entre as notas e os dados de acesso nos materiais do AVA?","Sub_topic":"Correlação entre as notas e os dados de acesso nos materiais do AVA","Label_pt": "materiais acessados"},
                                          {"id":"10","Question":"Qual a correlação entre as notas e os dados de acesso no fórum?","Sub_topic":"Correlação entre as notas e os dados de acesso no fórum","Label_pt":"acesso ao fórum"},
                                          {"id":"11","Question":"Qual a correlação entre as notas e a quantidade de postagens no fórum ?","Sub_topic":"Correlação entre as notas e a quantidade de postagens no fórum ","Label_pt":"postagens no fórum"},
                                          {"id":"12","Question":"Qual a correlação entre as notas e a quantidade de postagens de respostas no fórum ?","Sub_topic":"Correlação entre as notas e a quantidade de postagens de respostas no fórum ","Label_pt":"respostas no fórum"},
                                          {"id":"13","Question":"Qual a correlação entre as notas e a quantidade de tópicos adicionados no fórum?","Sub_topic":"Correlação entre as notas e a quantidade de tópicos adicionados no fórum","Label_pt":"tópicos no fórum"}]})
LST_VIEW_INFORMATION.append({"View":"V006","Topic":"Correlação entre o perfil (idade, cidade de origem, etc.) e os logs de acesso/interação dos estudantes no fórum", "id":"age", "Label_pt": "Correlação entre idade", "Label_en": "Student profiles",
                             "Questions":[{"id":"14","Question":"Qual a correlação entre a idade dos alunos e os dados de acesso no Fórum?","Sub_topic":"Correlação entre a idade dos alunos e os dados de acesso no Fórum","Label_pt":"acesso ao fórum"},
                                          {"id":"15","Question":"Qual a correlação entre a idade dos alunos e a quantidade de postagens no Fórum?","Sub_topic":"Correlação entre a idade dos alunos e a quantidade de postagens no Fórum","Label_pt":"postagens no fórum"},
                                          {"id":"16","Question":"Qual a correlação entre a idade dos alunos e a quantidade de postagens de respostas no Fórum?","Sub_topic":"Correlação entre a idade dos alunos e a quantidade de postagens de respostas no Fórum","Label_pt":"respostas no fórum"},
                                          {"id":"17","Question":"Qual a correlação entre a idade dos alunos e a quantidade de tópicos adicionados no fórum?","Sub_topic":"Correlação entre a idade dos alunos e a quantidade de tópicos adicionados no fórum","Label_pt":"tópicos no fórum"}]})
LST_VIEW_INFORMATION.append({"View":"V007","Topic":"Predição das notas e dos estudantes desistentes", "id":"prediction", "Label_pt": "Predição de performance", "Label_en": "Performance prediction",
                             "Questions":[{"id":"18","Question":"Qual a previsão de notas e dos estudantes desistentes?","Sub_topic":"Predição das notas e dos estudantes desistentes","Label_pt":"Predição de performance"}]})
LST_VIEW_INFORMATION.append({"View":"V008","Topic":"Acesso dos estudantes no AVA", "id":"access", "Label_pt": "Acesso dos estudantes", "Label_en": "Student access",
                             "Questions":[{"id":"19","Question":"Qual a quantidade de acesso dos estudantes por dia?","Sub_topic":"Quantidade de acesso dos estudantes por dia","Label_pt":"acessos por dia"},
                                          {"id":"20","Question":"Qual a quantidade de acesso dos estudantes por semana?","Sub_topic":"Quantidade de acesso dos estudantes por semana","Label_pt":"acessos por semana"}]})
LST_VIEW_INFORMATION.append({"View":"V009","Topic":"Interação dos estudantes nos vídeos (play, pause, seek backward, seek forward)", "id":"video_interaction", "Label_pt": "Interação no vídeo", "Label_en": "Video interaction",
                             "Questions":[{"id":"21","Question":"Como os alunos interagem no player de vídeo (play, pause, seek backward, seek forward)?","Sub_topic":"Interação dos estudantes nos vídeos (play, pause, seek backward, seek forward)","Label_pt":"Interação no vídeo"}]})
LST_VIEW_INFORMATION.append({"View":"V010","Topic":"Entendimento dos vídeos pelos estudantes", "id":"video_understood", "Label_pt": "Entendimento do vídeo", "Label_en": "Video understood",
                             "Questions":[{"id":"22","Question":"Quais vídeos os estudantes entenderam e não entenderam?","Sub_topic":"Vídeos que os estudantes entenderam e não entenderam","Label_pt":"Entendimento do vídeo"}]})
LST_VIEW_INFORMATION.append({"View":"V011","Topic":"Padrão de navegação dos estudantes no AVA", "id":"navigation", "Label_pt": "Navegação dos estudantes", "Label_en": "Student navigation",
                             "Questions":[{"id":"23","Question":"Qual o padrão de navegação dos estudantes no AVA?","Sub_topic":"Padrão de navegação dos estudantes no AVA","Label_pt":"Navegação dos estudantes"}]})

SUB_TOPIC = []
for i in range(len(LST_VIEW_INFORMATION)): #Get all subtopics
    lst_question = LST_VIEW_INFORMATION[i]["Questions"]

    for j in range(len(lst_question)):
        SUB_TOPIC.append({"id":lst_question[j]["id"],"label_pt":lst_question[j]["Sub_topic"]})

LST_DEFAULT_TOPIC_CHART_ID = [15,27,30,40,42,55,64,70,76,88,117,126,154]

LST_EVALUATION_TAM = {}
# Utilidade
LST_EVALUATION_TAM[1] = "ele permite configurar rapidamente um dashboard"
LST_EVALUATION_TAM[2] = "ele pode melhorar o desempenho do meu trabalho"
LST_EVALUATION_TAM[3] = "ele pode aumentar a minha produtividade"
LST_EVALUATION_TAM[4] = "ele pode aumentar a eficiência no meu trabalho"
LST_EVALUATION_TAM[5] = "ele poderia tornar mais fácil o trabalho"
LST_EVALUATION_TAM[6] = "em geral, ele pode ser vantajoso no meu trabalho"
# Facilidade de Uso
LST_EVALUATION_TAM[7] = "ele é fácil de aprender"
LST_EVALUATION_TAM[8] = "ele é simples e entendível"
LST_EVALUATION_TAM[9] = "ele é fácil de utilizar"
# Intenção de Uso
LST_EVALUATION_TAM[10] = "assumindo que o ele estará disponível no meu trabalho, eu o utilizaria regularmente no futuro"