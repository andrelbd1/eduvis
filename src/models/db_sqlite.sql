CREATE TABLE `tb_user`(
	`cl_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `cl_name` varchar(200) DEFAULT NULL,
	`cl_age` varchar(20) DEFAULT NULL,
	`cl_birth_place` varchar(500) DEFAULT NULL,
	`cl_work_place` varchar(500) DEFAULT NULL,	
	`cl_formation_area` varchar(500) DEFAULT NULL,
	`cl_education_level` varchar(50) DEFAULT NULL,
	`cl_job` varchar(500) DEFAULT NULL,
	`cl_record_date` datetime DEFAULT NULL
);

CREATE TABLE `tb_user_background`(
    `cl_user_id` INTEGER NOT NULL,
	`cl_ava_xp` tinyint(1) NOT NULL DEFAULT '1',
	`cl_ava_roles` varchar(500) DEFAULT NULL,
	`cl_ava_time_xp` varchar(500) DEFAULT NULL,
	`cl_ava_institution` varchar(500) DEFAULT NULL,
	`cl_ava_subject` varchar(500) DEFAULT NULL,
	`cl_ava_modality_xp` varchar(50) DEFAULT NULL,
	`cl_ava_system` varchar(500) DEFAULT NULL,
	`cl_ava_resources` varchar(500) DEFAULT NULL,
	`cl_ava_student_age` varchar(500) DEFAULT NULL,
	`cl_ava_student_information` varchar(500) DEFAULT NULL,
	`cl_ava_data_meaningful` varchar(500) DEFAULT NULL,
	`cl_ava_data_analyze` varchar(500) DEFAULT NULL,
	`cl_freq_interpretation_chart` varchar(50) DEFAULT NULL,
	`cl_freq_creation_chart` varchar(50) DEFAULT NULL,
	FOREIGN KEY (`cl_user_id`) REFERENCES `tb_user` (`cl_id`)
);

CREATE TABLE `tb_topic`(
	`cl_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `cl_label` varchar(200) NOT NULL
);

CREATE TABLE `tb_evaluate`(
	`cl_user_id` INTEGER NOT NULL,
	`cl_topic_id` INTEGER NOT NULL,
	`cl_value` varchar(3) NOT NULL,
    FOREIGN KEY (`cl_user_id`) REFERENCES `tb_user` (`cl_id`),
	FOREIGN KEY (`cl_topic_id`) REFERENCES `tb_topic` (`cl_id`)
);

CREATE TABLE `tb_dashboard`(
	`cl_id` INTEGER PRIMARY KEY AUTOINCREMENT,
	`cl_user_id` INTEGER,
    `cl_name` varchar(200) NOT NULL,
	`cl_type` tinyint(1) NOT NULL DEFAULT '1',
	`cl_language` tinyint(1) NOT NULL DEFAULT '1',
	`cl_record_date` datetime DEFAULT NULL,
	FOREIGN KEY (`cl_user_id`) REFERENCES `tb_user` (`cl_id`)
);

CREATE TABLE `tb_chart`(
	`cl_id` INTEGER PRIMARY KEY AUTOINCREMENT,
	`cl_chart_value` varchar(10) NOT NULL
);

CREATE TABLE `tb_topic_chart`(
	`cl_id` INTEGER PRIMARY KEY AUTOINCREMENT,
	`cl_chart_id` INTEGER NOT NULL,
	`cl_topic_id` INTEGER NOT NULL,
	FOREIGN KEY (`cl_chart_id`) REFERENCES `tb_chart` (`cl_id`),
	FOREIGN KEY (`cl_topic_id`) REFERENCES `tb_topic` (`cl_id`)
);

CREATE TABLE `tb_dashboard_topic_chart`(
	`cl_id` INTEGER PRIMARY KEY AUTOINCREMENT,
	`cl_dashboard_id` INTEGER NOT NULL,
	`cl_topic_chart_id` INTEGER NOT NULL,
	`cl_order` INTEGER NOT NULL,
	`cl_feedback` longtext NULL,
	`cl_value` varchar(3) NOT NULL,
	`cl_active` tinyint(1) NOT NULL DEFAULT '1',
	FOREIGN KEY (`cl_dashboard_id`) REFERENCES `tb_dashboard` (`cl_id`),
	FOREIGN KEY (`cl_topic_chart_id`) REFERENCES `tb_topic_chart` (`cl_id`)
);

CREATE TABLE `tb_question_dashboard`(
	`cl_id` INTEGER PRIMARY KEY AUTOINCREMENT,
	`cl_dashboard_id` INTEGER NOT NULL,
	`cl_question` longtext NULL,
	`cl_feedback` longtext NULL,
	FOREIGN KEY (`cl_dashboard_id`) REFERENCES `tb_dashboard` (`cl_id`)
);
