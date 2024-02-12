-- CREATE DATABASE IF NOT EXISTS Eduvis;
-- use Eduvis

-- DROP TABLE IF EXISTS `tb_user`;
-- DROP TABLE IF EXISTS `tb_user_background`;
-- DROP TABLE IF EXISTS `tb_topic`;
-- DROP TABLE IF EXISTS `tb_evaluate`;
-- DROP TABLE IF EXISTS `tb_dashboard`;
-- DROP TABLE IF EXISTS `tb_chart`;
-- DROP TABLE IF EXISTS `tb_topic_chart`;
-- DROP TABLE IF EXISTS `tb_dashboard_topic_chart`;
-- DROP TABLE IF EXISTS `tb_question_dashboard`;
-- DROP TABLE IF EXISTS `tb_question_chart`;

CREATE TABLE `tb_user`(
	`cl_id` bigint(11) NOT NULL AUTO_INCREMENT,
    `cl_name` varchar(200) DEFAULT NULL,
	`cl_age` varchar(20) DEFAULT NULL,
	`cl_birth_place` varchar(500) DEFAULT NULL COMMENT 'local de nascimento',
	`cl_work_place` varchar(500) DEFAULT NULL COMMENT 'local onde trabalha',
	`cl_formation_area` varchar(500) DEFAULT NULL COMMENT 'área de formação',
	`cl_education_level` varchar(50) DEFAULT NULL COMMENT 'escolaridade',
	`cl_job` varchar(500) DEFAULT NULL COMMENT 'profissão',
	`cl_record_date` datetime DEFAULT NULL,
	PRIMARY KEY (`cl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1464410 DEFAULT CHARSET=utf8 COMMENT='tabela de cadastro dos usuários instrutores';

CREATE TABLE `tb_user_background`(
	`cl_user_id` bigint(11) NOT NULL COMMENT 'chave estrangeira da tb_user',
	`cl_ava_xp` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'experiência com AVA (0 = não, 1 = sim)',
	`cl_ava_roles` varchar(500) DEFAULT NULl COMMENT 'papeis desempenhados na utilização de AVAs',
	`cl_ava_time_xp` varchar(500) DEFAULT NULL COMMENT 'tempo de experiência na utilização de AVAs',
	`cl_ava_institution` varchar(500) DEFAULT NULL COMMENT 'instituições de ensino que trabalha (e que trabalhou) utilizando AVAs',
	`cl_ava_subject` varchar(500) DEFAULT NULL COMMENT 'disciplinas ensinadas utilizando AVAs',
	`cl_ava_modality_xp` varchar(50) DEFAULT NULL COMMENT 'experiência com qual modalidade de ensino utilizando AVAs',
	`cl_ava_system` varchar(500) DEFAULT NULL COMMENT 'AVAs que utiliza (e que já utilizou)',
	`cl_ava_resources` varchar(500) DEFAULT NULL COMMENT 'recursos que utiliza e que já utilizou nos AVAs (videos, ebooks, fórum, chat, badges, etc.)',
	`cl_ava_student_age` varchar(500) DEFAULT NULL COMMENT 'faixa etária dos alunos que ensina (e que já ensinou) utilizando  AVAs',
	`cl_ava_student_information` varchar(500) DEFAULT NULL COMMENT 'quais informações dos alunos você considera relevante',
	`cl_ava_data_meaningful` varchar(500) DEFAULT NULL COMMENT 'que outros dados você considera importantes que não foram apresentados',
	`cl_ava_data_analyze` varchar(500) DEFAULT NULL COMMENT 'como você gostaria que esses dados fossem apresentados (em uma tabela, em gráfico de barra, etc)',
	`cl_freq_interpretation_chart` varchar(50) DEFAULT NULL COMMENT 'em geral, com que frequência você lê e interpreta gráficos',
	`cl_freq_creation_chart` varchar(50) DEFAULT NULL COMMENT 'em geral, com que frequência você cria gráficos',
    KEY `fk_user_id` (`cl_user_id`),
	CONSTRAINT `tb_user_background_fk_user_id` FOREIGN KEY (`cl_user_id`) REFERENCES `tb_user` (`cl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='tabela de cadastro do background dos instrutores';

CREATE TABLE `tb_topic`(
	`cl_id` bigint(11) NOT NULL AUTO_INCREMENT,
    `cl_label` varchar(200) NOT NULL COMMENT 'descrição do tópico',
	PRIMARY KEY (`cl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1464410 DEFAULT CHARSET=utf8 COMMENT='tabela de cadastro dos tópicos de informações dos logs dos estudantes que podem ser analisados pelos instrutores';

CREATE TABLE `tb_evaluate`(
	`cl_user_id` bigint(11) NOT NULL COMMENT 'chave estrangeira da tb_user',
	`cl_topic_id` bigint(11) NOT NULL COMMENT 'chave estrangeira da tb_topic',
	`cl_value` varchar(3) NOT NULL COMMENT 'valor da avaliação do usuário na escala likert (1 à 7)',
	KEY `fk_user_id` (`cl_user_id`),
	KEY `fk_topic_id` (`cl_topic_id`),
	CONSTRAINT `tb_evaluate_fk_user_id` FOREIGN KEY (`cl_user_id`) REFERENCES `tb_user` (`cl_id`),
	CONSTRAINT `tb_evaluate_fk_topic_id` FOREIGN KEY (`cl_topic_id`) REFERENCES `tb_topic` (`cl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='tabela que armazena a avaliação dos tópicos pelos instrutores';

CREATE TABLE `tb_dashboard`(
	`cl_id` bigint(11) NOT NULL AUTO_INCREMENT,
	`cl_user_id` bigint(11) COMMENT 'chave estrangeira da tb_user',
    `cl_name` varchar(200) NOT NULL COMMENT 'nome do dashboard',	
	`cl_type` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'tipo do dashboard (0 = estático, 1 = customizável)',
	`cl_language` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'tipo do dashboard (0 = en, 1 = pt-br)',
	`cl_record_date` datetime DEFAULT NULL,
	PRIMARY KEY (`cl_id`),
	KEY `fk_user_id` (`cl_user_id`),
	CONSTRAINT `tb_dashboard_fk_user_id` FOREIGN KEY (`cl_user_id`) REFERENCES `tb_user` (`cl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1464410 DEFAULT CHARSET=utf8 COMMENT='tabela de dashboards dos instrutores';

CREATE TABLE `tb_chart`(
	`cl_id` bigint(11) NOT NULL AUTO_INCREMENT,
	`cl_chart_value` varchar(10) NOT NULL COMMENT '',
	PRIMARY KEY (`cl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1464410 DEFAULT CHARSET=utf8 COMMENT='tabela dos gráficos';

CREATE TABLE `tb_topic_chart`(
	`cl_id` bigint(11) NOT NULL AUTO_INCREMENT,
	`cl_chart_id` bigint(11) NOT NULL COMMENT 'chave estrangeira da tb_chart',
	`cl_topic_id` bigint(11) NOT NULL COMMENT 'chave estrangeira da tb_topic',
	PRIMARY KEY (`cl_id`),
	KEY `fk_chart_id` (`cl_chart_id`),
	KEY `fk_topic_id` (`cl_topic_id`),
	CONSTRAINT `tb_topic_chart_fk_chart_id` FOREIGN KEY (`cl_chart_id`) REFERENCES `tb_chart` (`cl_id`),
	CONSTRAINT `tb_topic_chart_fk_topic_id` FOREIGN KEY (`cl_topic_id`) REFERENCES `tb_topic` (`cl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1464410 DEFAULT CHARSET=utf8 COMMENT='tabela que relaciona os tópicos com os gráficos';

CREATE TABLE `tb_dashboard_topic_chart`(
	`cl_id` bigint(11) NOT NULL AUTO_INCREMENT,
	`cl_dashboard_id` bigint(11) NOT NULL COMMENT 'chave estrangeira da tb_dashboard',
	`cl_topic_chart_id` bigint(11) NOT NULL COMMENT 'chave estrangeira da tb_topic_chart',
	`cl_order` bigint(11) NOT NULL  COMMENT 'indica a posição que o chart aparece no dashboard',
	`cl_feedback` longtext NULL COMMENT 'duas informações que você consegue extrair com esse gráfico',
	`cl_value` varchar(3) NOT NULL COMMENT 'valor da avaliação do usuário na escala likert (1 à 7)',
	`cl_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'indica se aquele topico e chart estão ativos no dashboard',
	PRIMARY KEY (`cl_id`),
	KEY `fk_dashboard_id` (`cl_dashboard_id`),
	KEY `fk_topic_chart_id` (`cl_topic_chart_id`),
	CONSTRAINT `tb_dashboard_topic_chart_fk_dashboard_id` FOREIGN KEY (`cl_dashboard_id`) REFERENCES `tb_dashboard` (`cl_id`),
	CONSTRAINT `tb_dashboard_topic_chart_fk_topic_chart_id` FOREIGN KEY (`cl_topic_chart_id`) REFERENCES `tb_topic_chart` (`cl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1464410 DEFAULT CHARSET=utf8 COMMENT='tabela que relaciona os gráficos com os dashboards dos usuários';

CREATE TABLE `tb_question_dashboard`(
	`cl_id` bigint(11) NOT NULL AUTO_INCREMENT,
	`cl_dashboard_id` bigint(11) NOT NULL  COMMENT 'chave estrangeira da tb_dashboard',
	`cl_question` longtext NULL COMMENT 'questões sobre o dashboard',
	`cl_feedback` longtext NULL COMMENT 'fatos extraídos com o dashboard',
	PRIMARY KEY (`cl_id`),
	KEY `fk_dashboard_id` (`cl_dashboard_id`),
	CONSTRAINT `tb_question_dashboard_fk_dashboard_id` FOREIGN KEY (`cl_dashboard_id`) REFERENCES `tb_dashboard` (`cl_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1464410 DEFAULT CHARSET=utf8 COMMENT='tabela que armazena a avaliação feita pelos instrutores em relação ao dashboard';
