# Imports 📚
#%%
import pandas as pd
from src import auto_eda as AutoEDA
from src import data_transformer as data
from src import database_creation as db

#%%
# First step :EDA Analysis

eda = AutoEDA() # Class that automates all EDA analysys

#%%
df = eda.read_file('../data/hr_data_transformed_2024-08-02_16:14:18.csv')
eda.explo_df(df)


df_corr = (eda.identify_correlations(df))['spearman'] # Returns dict with pearce or spearman method as key and df as value
df_corr

eda.classify_correlations(df_corr)
eda.plot_histogram(df, 'years_with_curr_manager')

eda.plot_scatter(df, 'years_with_curr_manager', 'years_at_company')
eda.plot_boxplot(df, 'years_since_last_promotion')
eda.visualize_pairplot(df, ['years_at_company', 'years_since_last_promotion', 'job_level'], hue='gender')

eda.visualize_categorical_counts(df, ['business_travel', 'department', 'marital_status', 'remote_work'])

eda.visualize_facet_grid(df, col_names=['business_travel','job_role','department'], x_values=['daily_rate','monthly_income','total_working_years'], hue='gender')

df_heatmap1=df.groupby(['job_role','job_satisfaction']).monthly_income.mean().unstack(level=1)
df_heatmap2=df.groupby(['job_involvement','job_level']).monthly_rate.mean().unstack(level=1)

eda.visualize_general_statistics(df, df_heatmap1, df_heatmap2)
eda.visualize_pairplot(df, ['monthly_income','job_level','total_working_years','monthly_rate','age'], hue='gender')
#%%
# Second step: Data transformation



