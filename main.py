# Imports 📚
#%%
import pandas as pd
from src.data_transformer import DataTransformer as data
from src.database_creation import CreateDatabase as db
from src import queries as query
from datetime import datetime


# FIRST STEP: EXTRACT DATA
df = pd.read_csv("data/hr_raw_data.csv", index_col=0)
df.head()


# SECOND STEP: TRANSFORMATION
abc_data = data(df)

abc_data.rename_columns() # rename columns

abc_data.convert_age_to_numbers() # convert number written in letters into into numbers written in numbers

abc_data.convert_to_numeric ("age","integer") # convert column to "int"

abc_data.fix_negative_distances() # fix negative data into a column

abc_data.correct_env_satisfaction_values() # correct data into normalize survey data

abc_data.replace_gender_values() # replace wrong values

abc_data.correct_hourly_rate() # replace wrong values

abc_data.transform_to_float("monthly_income") # transform to float

abc_data.transform_to_float("performance_rating")

abc_data.transform_to_float("total_working_years")

abc_data.transform_to_float("work_life_balance")

abc_data.correct_typos_marital_status() # correct gramatical errors

abc_data.convert_object_to_float_eliminate_dolar("daily_rate") # transform to float and normalize column

abc_data.map_column_remote_work() # change values 

abc_data.convert_role_to_department_normalize_job_role() # replace values with de column job role and normalize it

columns_to_delete = ["employee_count", "same_as_monthly_income", "salary", "number_children", "standard_hours", "years_in_current_role", "over_18", "role_departament"]

abc_data.drop_redundant_columns(columns_to_delete) # delete columns

abc_data.transform_to_float("employee_number") # transform to float

abc_data.impute_with_group_mean_and_knn('monthly_income', 'job_role') # eliminate nulls with mean value and knn

columns_modify = ["business_travel", "education_field", "marital_status", "over_time", "employee_number", "department"]
abc_data.change_null_for_unknown(columns_modify) # eliminate nulls with a new category Unknown

columns_modify = ["daily_rate", "hourly_rate"]
abc_data.change_null_for_mean(columns_modify) # eliminate nulls with mean value

columns_modify = ["performance_rating", "environment_satisfaction","work_life_balance"]
abc_data.change_null_for_median(columns_modify) # eliminate nulls with median value

columns_modify = ["total_working_years"]
abc_data.change_null_for_mean(columns_modify) # eliminate nulls with mean value

abc_data.create_csv("data/hr_data_transformed.csv") # create csv with transformed data

hr_data = pd.read_csv("data/hr_data_transformed.csv") # create dataframe with transformed data


# THIRD STEP: LOAD TO MySQL DATABASE
db_hr = db(user ="root", password="AlumnaAdalab", host= "127.0.0.1", database="HR_optimization") # gives parameters to the database

db_hr.clean_dataframe(hr_data) # clean dataframe to use it at last step

db_hr.create_database() # createdatabase

db_hr.connect("HR_optimization") # connect to MySQL database

db_hr.create_table("departments",query.schema1) # create tables

db_hr.create_table("education_fields",query.schema2)

db_hr.create_table("employees",query.schema3)

db_hr.create_table("job_roles",query.schema4 )

db_hr.insert_unique_values('job_roles', 'job_role_id', 'job_role_name', hr_data['job_role'].unique()) # Insert unique values

db_hr.insert_unique_values('departments', 'department_id', 'department_name', hr_data['department'].unique())

db_hr.insert_unique_values('education_fields', 'education_field_id', 'education_field_name', hr_data['education_field'].unique())

db_hr.bulk_insert_data(hr_data, 'employees') # insert masive data with a bulk function

db_hr.close()
