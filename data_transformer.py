# # Psssss READ ME! 👋👓
# The objective of the following code it to clean and transform ABC Coorporation data to make it available for a subsequent analysis. 
# The transformation methods of the data_transformer were developed based on the conclusions from the preliminary Exploratory Data Analysis of the raw data provided by the HR department of BC Coorporation.
# The highlevel code structure is as follows: 
    # 1) Import of packages and data
    # 2) Definition of the DataTransformer class, this is the core of the transformation
    # 3) Execution of the transformation with follows this structure:
        # 3.1) Creation of an object from DataTransformer class
        # 3.2) Rename all columns
        # 3.3) Drop unnecessary columns
        # 3.4) Transform data per column
# Testing code: 
    # For each step of the process the program prints the result so that it can be reviewed and confirm that is working correctly


# Imports 📥

# Packages
#-----------------------------------------------------------------------
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

# Visualization
# -----------------------------------------------------------------------
import seaborn as sns
import matplotlib.pyplot as plt

# Settings
# -----------------------------------------------------------------------
pd.set_option('display.max_columns', None) # para poder visualizar todas las columnas de los DataFrames



# DataTransformer class definition ✍️

class DataTransformer:
    def __init__(self, dataframe):
        self.df = dataframe

    def rename_columns (self): 
        """Transform columns' names to snake format. E.g. 'EducationField' to 'education_field' """
        columns_names = {
            'Age': 'age',
            'Attrition': 'attrition',
            'BusinessTravel': 'business_travel',
            'DailyRate': 'daily_rate',
            'Department': 'department',
            'DistanceFromHome': 'distance_from_home',
            'Education': 'education',
            'EducationField': 'education_field',
            'employeecount': 'employee_count',
            'employeenumber': 'employee_number',
            'EnvironmentSatisfaction': 'environment_satisfaction',
            'Gender': 'gender',
            'HourlyRate': 'hourly_rate',
            'JobInvolvement': 'job_involvement',
            'JobLevel': 'job_level',
            'JobRole': 'job_role',
            'JobSatisfaction': 'job_satisfaction',
            'MaritalStatus': 'marital_status',
            'MonthlyIncome': 'monthly_income',
            'MonthlyRate': 'monthly_rate',
            'NUMCOMPANIESWORKED': 'num_companies_worked',
            'Over18': 'over_18',
            'OverTime': 'over_time',
            'PercentSalaryHike': 'percent_salary_hike',
            'PerformanceRating': 'performance_rating',
            'RelationshipSatisfaction': 'relationship_satisfaction',
            'StandardHours': 'standard_hours',
            'StockOptionLevel': 'stock_option_level',
            'TOTALWORKINGYEARS': 'total_working_years',
            'TrainingTimesLastYear': 'training_times_last_year',
            'WORKLIFEBALANCE': 'work_life_balance',
            'YearsAtCompany': 'years_at_company',
            'YearsInCurrentRole': 'years_in_current_role',
            'YearsSinceLastPromotion': 'years_since_last_promotion',
            'YEARSWITHCURRMANAGER': 'years_with_curr_manager',
            'SameAsMonthlyIncome': 'same_as_monthly_income',
            'DateBirth': 'date_birth',
            'Salary': 'salary',
            'RoleDepartament': 'role_departament',
            'NUMBERCHILDREN': 'number_children',
            'RemoteWork': 'remote_work'
        }
        self.df = self.df.rename(columns=columns_names)

    def replace_gender_values(self):
        """Replaces the values in the Gender column with 'Male' and 'Female'."""
        self.df['gender'] = self.df['gender'].replace({0: 'Male', 1: 'Female'})
    
    def convert_age_to_numbers(self):
        """Converts numbers written in letters (e.g: 'thirty-two') into numbers written in numbers ('32'). It does NOT change the data type!"""
        # create a dictionary with numbers written in letters as keys and numbers in numbers as values
        conversion_dictionary = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "twenty-one": 21,
        "twenty-two": 22,
        "twenty-three": 23,
        "twenty-four": 24,
        "twenty-five": 25,
        "twenty-six": 26,
        "twenty-seven": 27,
        "twenty-eight": 28,
        "twenty-nine": 29,
        "thirty": 30,
        "thirty-one": 31,
        "thirty-two": 32,
        "thirty-three": 33,
        "thirty-four": 34,
        "thirty-five": 35,
        "thirty-six": 36,
        "thirty-seven": 37,
        "thirty-eight": 38,
        "thirty-nine": 39,
        "forty": 40,
        "forty-one": 41,
        "forty-two": 42,
        "forty-three": 43,
        "forty-four": 44,
        "forty-five": 45,
        "forty-six": 46,
        "forty-seven": 47,
        "forty-eight": 48,
        "forty-nine": 49,
        "fifty": 50,
        "fifty-one": 51,
        "fifty-two": 52,
        "fifty-three": 53,
        "fifty-four": 54,
        "fifty-five": 55,
        "fifty-six": 56,
        "fifty-seven": 57,
        "fifty-eight": 58,
        "fifty-nine": 59,
        "sixty": 60,
        "sixty-one": 61,
        "sixty-two": 62,
        "sixty-three": 63,
        "sixty-four": 64,
        "sixty-five": 65,
        "sixty-six": 66,
        "sixty-seven": 67,
        "sixty-eight": 68,
        "sixty-nine": 69,
        "seventy": 70,
        "seventy-one": 71,
        "seventy-two": 72,
        "seventy-three": 73,
        "seventy-four": 74,
        "seventy-five": 75,
        "seventy-six": 76,
        "seventy-seven": 77,
        "seventy-eight": 78,
        "seventy-nine": 79,
        "eighty": 80,
        "eighty-one": 81,
        "eighty-two": 82,
        "eighty-three": 83,
        "eighty-four": 84,
        "eighty-five": 85,
        "eighty-six": 86,
        "eighty-seven": 87,
        "eighty-eight": 88,
        "eighty-nine": 89,
        "ninety": 90,
        "ninety-one": 91,
        "ninety-two": 92,
        "ninety-three": 93,
        "ninety-four": 94,
        "ninety-five": 95,
        "ninety-six": 96,
        "ninety-seven": 97,
        "ninety-eight": 98,
        "ninety-nine": 99,
        "one hundred": 100
        }
        for index, value in enumerate(self.df["age"].values): 
            if value in conversion_dictionary:
                self.df["age"][index] = conversion_dictionary[value]
                print (f"Value '{value}' was transformed into '{conversion_dictionary[value]}'")
                
    def convert_to_numeric(self, column_name, downcast):
        """Converts a column to numeric type. Downcast = 'integer' or 'float'"""
        self.df[column_name] = pd.to_numeric(self.df[column_name], errors='raise', downcast=downcast)

    def fix_negative_distances(self):
        """Corrects negative values in the DistanceFromHome column."""
        self.df['distance_from_home'] = self.df['distance_from_home'].abs()

    def drop_redundant_columns(self, columns):
            """Drops redundant columns like 'same_as_monthly_income'. Param columns is a list of columns to de dropped"""
            self.df.drop(columns=columns, inplace=True, errors='ignore')

    def correct_env_satisfaction_values(self):
        """Transform values higher than 4 into NaN"""
        self.df['environment_satisfaction'] = self.df['environment_satisfaction'].apply(lambda x: x if x <= 4 else np.nan)

    def correct_hourly_rate(self):
        """Transform all values from the column into into numeric and 'Not Available' into NaN"""
        
        def transform_hourly_rate_individual (value):
            """Transform a value into numeric and 'Not Available' into NaN"""
            if value == "Not Available":
                value = np.nan
            return float(value)

        self.df['hourly_rate'] = self.df['hourly_rate'].apply(transform_hourly_rate_individual)

    def transform_to_float(self,column_name):
        """Transform strings with format '3579,0' in float"""

        self.df[column_name] = self.df[column_name].str.replace(',','.').astype(float)

    def correct_typographical_errors(self):
        """Corrects typographical errors in the marital_status column."""
        self.df['marital_status'] = self.df['marital_status'].replace({'Marreid': 'Married','divorced':'Divorced'})

    def convert_role_to_department_normalize_job_role(self):
        # First change de type of data to be capitalize and the same way
        self.df['JobRole'] = self.df['JobRole'].str.title()
        self.df['Department'] = self.df['Department'].str.title()
       # Clean empty spaces
        self.df['JobRole'] = self.df['JobRole'].str.strip()
        self.df['Department'] = self.df['Department'].str.strip()
        
        conversion_dictionary = {
        'Healthcare Representative': 'Research & Development',
        'Sales Executive': 'Sales',
        'Healthcare Representative': 'Research & Development',
        'Laboratory Technician': 'Research & Development',
        'Manufacturing Director': 'Research & Development',
        'Research Scientist': 'Research & Development',
        'Sales Executive': 'Sales',
        'Sales Representative':'Sales',
        'Research Director': 'Research & Development',
        'Human Resources': 'Human Resources',
         }
        # Iterate over the rows of the DataFrame
        for index, row in self.df.iterrows():
            job_role = row['JobRole']
            # Assign the corresponding value to Department using the dictionary
            if job_role in conversion_dictionary:
                self.df.at[index, 'Department'] = conversion_dictionary[job_role]
                print(f"Value '{job_role}' was transformed into '{conversion_dictionary[job_role]}'")

    def change_marital_status(self):
        
        self.df['MaritalStatus'] = self.df['MaritalStatus'].replace({
        "Marreid": "Married",
        "divorced": "Divorced"})
        self.df["MaritalStatus"] = self.df["MaritalStatus"].fillna("Unknown")
        
    def map_column_remote_work(self):
        dicc = {1: "True", 0: "False", "Yes": "True"}

        # Replace the values in the RemoteWork column according to the dictionary
        self.df["RemoteWork"] = self.df["RemoteWork"].replace(dicc)

    def change_null_for_unknown(self, column_list): # when doesnt exist a dominant category in categorical variable
        # Iterate through the list of columns to replace nulls with "Unknown"
        for column in column_list:
            if column in self.df.columns:
                # Replace nulls with the value "Unknown" for each column in the list
                self.df[column] = self.df[column].fillna("Unknown")
            else:
                print(f"Warning: The column '{column}' does not exist in the DataFrame.")
        return self.df
    
    def change_null_for_mode(self, column_list): # When we have a dominant category in categorical variables
        for column in column_list:
            if column in self.df.columns:
                # Calculate the mode of the column
                mode = self.df[column].mode()[0]
                # Replace nulls with the mode for each column in the list
                self.df[column] = self.df[column].fillna(mode)
            else:
                print(f"Warning: The column '{column}' does not exist in the DataFrame.")
        return self.df
    
    def change_null_for_mean(self, column_list): # when we have a 0-10% of nulls in numerical category and distribution is normal
        # Iterate through the list of columns to replace nulls with mean
        for column in column_list:
            if column in self.df.columns:
                    mean= self.df[column].mean()
                # Replace nulls with the mode for each column in the list
                    self.df[column] = self.df[column].fillna(mean)
            else:
                print(f"Warning: The column '{column}' does not exist in the DataFrame.")
        return self.df
    
    def change_null_for_median(self, column_list): # when we have a 0-10% of nulls in numerical category and distribution is atypical
        # Iterate through the list of columns to replace nulls with median
        for column in column_list:
            if column in self.df.columns:
                    median= self.df[column].median()
                # Replace nulls with the mode for each column in the list
                    self.df[column] = self.df[column].fillna(median)
            else:
                print(f"Warning: The column '{column}' does not exist in the DataFrame.")
        return self.df
    
    def impute_with_knn(self, column_list, n_neighbors=5): # when we have a numerical variable with more than 10% of nulls
        # Create an instance of KNNImputer
        imputer_knn = KNNImputer(n_neighbors=n_neighbors)

        # Fit and transform the data
        imputed_data = imputer_knn.fit_transform(self.df[column_list])

        # Convert the result to a DataFrame
        imputed_df = pd.DataFrame(imputed_data, columns=column_list)

        # Add the imputed columns to the original DataFrame
        for column in column_list:
            self.df[f"{column}_knn"] = imputed_df[column]

        return self.df
    
    def remove_duplicates(self):
        """Removes rows with duplicated employee_number, keeping the last appearance. Rows with NaN values are kept"""
        # Separate rows with NaN from those without NaN
        df_na = self.df[self.df["employee_number"].isna()]
        df_no_na = self.df[self.df["employee_number"].notna()]
        # Delete duplicates from rows without NaN
        df_no_na_unique = df_no_na.drop_duplicates(subset=['employee_number'], keep='last')
        # Rebuild original DataFrame
        self.df = pd.concat([df_no_na_unique, df_na]).sort_index()

    def quick_check(self,column_name):
        """ This function is for testing purposes, to quicky check data type and unique values of a column"""
        print (f"Column name: {column_name}")
        print (f"Data type: {self.df[column_name].dtype}")
        print (f"Unique values: {self.df[column_name].unique()}")
        print (f"Not null count: {self.df[column_name].notnull().sum()}")
        print (f"Null count: {self.df[column_name].isnull().sum()}")
        print (f"Duplicated values: {self.df[column_name].duplicated().sum()}")
        
    def get_dataframe(self):
        """Returns the transformed DataFrame."""
        return self.df
    
    def create_csv(self):
         self.df.to_csv("hr_data_transformed.csv")



