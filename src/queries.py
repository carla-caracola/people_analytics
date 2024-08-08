schema1 = """`department_id` INT NOT NULL,
            `department_name` VARCHAR(80) DEFAULT NULL,
            PRIMARY KEY (`department_id`)
            """

schema2= """`education_field_id` INT NOT NULL AUTO_INCREMENT,
            `education_field_name` VARCHAR(80) NOT NULL,
            PRIMARY KEY (`education_field_id`),
            UNIQUE INDEX `education_field_name` (`education_field_name`)
            """

schema3= """`employee_id` INT NOT NULL AUTO_INCREMENT,
            `age` INT DEFAULT NULL,
            `attrition` VARCHAR(3) DEFAULT NULL,
            `business_travel` VARCHAR(50) DEFAULT NULL,
            `daily_rate` FLOAT DEFAULT NULL,
            `department` VARCHAR(80) DEFAULT NULL,
            `distance_from_home` INT DEFAULT NULL,
            `education` INT DEFAULT NULL,
            `education_field` VARCHAR(80) DEFAULT NULL,
            `employee_number` VARCHAR(50) DEFAULT NULL,
            `environment_satisfaction` INT DEFAULT NULL,
            `gender` VARCHAR(10) DEFAULT NULL,
            `hourly_rate` FLOAT DEFAULT NULL,
            `job_involvement` INT DEFAULT NULL,
            `job_level` INT DEFAULT NULL,
            `job_role` VARCHAR(50) DEFAULT NULL,
            `job_satisfaction` INT DEFAULT NULL,
            `marital_status` VARCHAR(30) DEFAULT NULL,
            `monthly_income` FLOAT DEFAULT NULL,
            `monthly_rate` FLOAT DEFAULT NULL,
            `num_companies_worked` INT DEFAULT NULL,
            `over_time` VARCHAR(10) DEFAULT NULL,
            `percent_salary_hike` FLOAT DEFAULT NULL,
            `performance_rating` INT DEFAULT NULL,
            `relationship_satisfaction` INT DEFAULT NULL,
            `stock_option_level` INT DEFAULT NULL,
            `total_working_years` INT DEFAULT NULL,
            `training_times_last_year` INT DEFAULT NULL,
            `work_life_balance` INT DEFAULT NULL,
            `years_at_company` INT DEFAULT NULL,
            `years_since_last_promotion` INT DEFAULT NULL,
            `years_with_curr_manager` INT DEFAULT NULL,
            `date_birth` varchar(10) DEFAULT NULL,
            `remote_work` VARCHAR(10) DEFAULT NULL,
            PRIMARY KEY (`employee_id`)
            """

schema4 = """`job_role_id` INT NOT NULL AUTO_INCREMENT,
            `job_role_name` VARCHAR(50) NOT NULL,
            PRIMARY KEY (`job_role_id`),
            UNIQUE INDEX `job_role_name` (`job_role_name`)
            """