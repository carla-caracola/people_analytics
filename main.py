# Imports 📚
#%%
import pandas as pd
from src.data_transformer import DataTransformer as data
from src.database_creation import CreateDatabase as db
from src import queries as query
from datetime import datetime

#%%
# FIRST STEP: EXTRACT DATA

df = pd.read_csv("data/HR RAW DATA.csv", index_col=0)
df.head()
hr_data = pd.read_csv("data/hr_data_transformed_2024-08-02_161418.csv")

#%%
# SECOND STEP: TRANSFORMATION
abc_data = data(df)

abc_data.rename_columns()
#%%
# convert number written in letters into into numbers written in numbers

abc_data.convert_age_to_numbers()

# convert column to "int"

abc_data.convert_to_numeric ("age","integer")

#%%
abc_data.fix_negative_distances()
#%%
abc_data.correct_env_satisfaction_values()

#%%
abc_data.replace_gender_values()
#%%
abc_data.correct_hourly_rate()
#%%
abc_data.transform_to_float("monthly_income")

#%%
abc_data.transform_to_float("performance_rating")
#%%
abc_data.transform_to_float("total_working_years")
#%%
abc_data.transform_to_float("work_life_balance")
#%%
abc_data.correct_typos_marital_status()

#%%
abc_data.convert_object_to_float_eliminate_dolar("daily_rate")
#%%
abc_data.map_column_remote_work()
#%%
abc_data.convert_role_to_department_normalize_job_role()
#%%
columns_to_delete = ["employee_count", "same_as_monthly_income", "salary", "number_children", "standard_hours", "years_in_current_role", "over_18", "role_departament"]

abc_data.drop_redundant_columns(columns_to_delete)
#%%
abc_data.transform_to_float("employee_number")

#%%
abc_data.impute_with_group_mean_and_knn('monthly_income', 'job_role')
#%%
columns_modify = ["business_travel", "education_field", "marital_status", "over_time", "employee_number", "department"]
abc_data.change_null_for_unknown(columns_modify)
#%%
columns_modify = ["daily_rate", "hourly_rate"]
abc_data.change_null_for_mean(columns_modify)
#%%
columns_modify = ["performance_rating", "environment_satisfaction","work_life_balance"]
abc_data.change_null_for_median(columns_modify)
#%%
columns_modify = ["total_working_years"]
abc_data.change_null_for_mean(columns_modify)


#%%
# THIRD STEP: LOAD
db_hr = db(user ="root", password="AlumnaAdalab", host= "127.0.0.1", database="HR_optimization") # gives parameters to the database
db_hr.clean_dataframe(hr_data)

#%%
db_hr.create_database()
# %%
db_hr.connect("HR_optimization")
#%%
db_hr.create_table("departments",query.schema1)
db_hr.create_table("education_fields",query.schema2)
db_hr.create_table("employees",query.schema3)
db_hr.create_table("job_roles",query.schema4 )

#%%
# Insert unique values into 'job_roles'
db_hr.insert_unique_values('job_roles', 'job_role_id', 'job_role_name', hr_data['job_role'].unique())

db_hr.insert_unique_values('departments', 'department_id', 'department_name', hr_data['department'].unique())

db_hr.insert_unique_values('education_fields', 'education_field_id', 'education_field_name', hr_data['education_field'].unique())

#%%

db_hr.bulk_insert_data(hr_data, 'employees')
db_hr.close()

#%%