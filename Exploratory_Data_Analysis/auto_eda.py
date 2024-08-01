import pandas as pd
import numpy as np
from IPython.display import display
from itertools import combinations
from scipy.stats import kstest, spearmanr, pearsonr


class AutoEDA:

    def read_file(self, file_path):
        """
        Reads a file and returns a pandas DataFrame.
        
        Parameters:
        - file_path (str): The path to the file.
        
        Returns:
        - DataFrame: A pandas DataFrame.
        """
        # Determine the file extension
        file_extension = file_path.split('.')[-1].lower()
        
        # Read the file based on the file extension
        try:
            if file_extension == 'csv':
                return pd.read_csv(file_path, index_col=0)
            elif file_extension in ['xls', 'xlsx']:
                return pd.read_excel(file_path)
            elif file_extension == 'json':
                return pd.read_json(file_path)
            elif file_extension == 'pkl':
                return pd.read_pickle(file_path)
            else:
                raise ValueError("Reading this format is not yet implemented.")
        except Exception as e:
            return f"File reading failed, error: {e}."


    def explo_df(self, DataFrame, column=None):
        """
        Explores a DataFrame or a specific column and prints various statistics.
        
        Parameters:
        - DataFrame: The DataFrame to explore.
        - column (str or list, optional): The column or columns to explore. If None, explore the entire DataFrame.
        """
        if column is None:
            # General DataFrame exploration
            print("DataFrame Information:")
            display(DataFrame.info())
            print("\nFirst 10 rows of the DataFrame:")
            display(DataFrame.head(10))
            print("\nLast 10 rows of the DataFrame:")
            display(DataFrame.tail(10))
            print("\nStatistical description of the DataFrame (numeric):")
            display(DataFrame.describe().T)
            print("\nStatistical description of the DataFrame (categorical):")
            display(DataFrame.describe(include='object').T)
            print("\nCount of null values per column:")
            display(DataFrame.isnull().sum())
            print("\nPercentage of null values per column (only columns with nulls):")
            null_percentage = round(DataFrame.isnull().sum()/DataFrame.shape[0]*100, 2)
            display(null_percentage[null_percentage > 0])
            print("\nRows with all values as null:")
            all_null_rows = DataFrame[DataFrame.isnull().all(axis=1)]
            if not all_null_rows.empty:
                display(all_null_rows)
            else:
                print("There is no rows with all values as null.")
            print("\nCount of duplicate rows:")
            display(DataFrame.duplicated().sum())
        else:
            # Column(s) exploration
            if isinstance(column, str):
                column = [column]  # Convert to list if a single column is passed as a string
            for col in column:
                print(f"\nExploration of the column: {col}")
                if DataFrame[col].dtype in ['int64', 'float64']:
                    print("\nStatistical description (numeric):")
                    display(DataFrame[col].describe())
                else:
                    print("\nStatistical description (categorical):")
                    display(DataFrame[col].describe(include='object'))
                print(f"\nCount of null values: {DataFrame[col].isnull().sum()}")
                print(f"\nUnique values: {DataFrame[col].unique()}")
                print(f"\nValue Counts: {DataFrame[col].value_counts()}")
                print(f"\nCount of duplicates in the column: {DataFrame.duplicated(subset=[col]).sum()}")

    
    def __identify_linearity(dataframe, column_combinations_list):
        """
        Identifies if the relationships between pairs of variables in a DataFrame are linear or not.

        Parameters:
        -----------
        dataframe : pandas.DataFrame
            The DataFrame containing the variables to be analyzed.

        column_combinations_list : list of tuples
            A list of tuples where each tuple contains two column names from the DataFrame to be analyzed.

        Returns:
        --------
        linear_relationships : list of tuples
            A list of tuples containing the names of the columns that have a linear relationship.

        non_linear_relationships : list of tuples
            A list of tuples containing the names of the columns that do not have a linear relationship.
        """
        linear_relationships = []
        non_linear_relationships = []

        for pair in column_combinations_list: 
            # Perform the normality test
            _, p_value1 = kstest(dataframe[pair[0]], "norm")
            _, p_value2 = kstest(dataframe[pair[1]], "norm")

            if p_value1 > 0.05 and p_value2 > 0.05:
                linear_relationships.append(pair)
            else:
                non_linear_relationships.append(pair)

        return linear_relationships, non_linear_relationships


    def identify_correlations(self, dataframe):
        numerics = dataframe.select_dtypes(include=np.number).columns
        num_combinations = list(combinations(numerics, 2))
        linear, non_linear = self.__identify_linearity(dataframe, num_combinations)

        # df_correlations = 

        # categorics = dataframe.select_dtypes(include=['object', 'category']).columns
        # cat_combinations = list(combinations(categorics, 2))







        # Correlaciones para variables numéricas
        pearson_corr = {}
        for col1, col2 in linear:
            corr, _ = pearsonr(dataframe[col1].dropna(), dataframe[col2].dropna())
            pearson_corr[(col1, col2)] = corr

        spearman_corr = {}
        for col1, col2 in non_linear:
            corr, _ = spearmanr(dataframe[col1].dropna(), dataframe[col2].dropna())
            spearman_corr[(col1, col2)] = corr

        # Correlaciones para variables categóricas

        return pearson_corr, spearman_corr

# # Uso de la clase
# auto_eda = AutoEda()
# pearson_corr, spearman_corr = auto_eda.correlations(df)

# print("Pearson Correlations (Linear Relationships):")
# print(pearson_corr)
# print("\nSpearman Correlations (Non-linear Relationships):")
# print(spearman_corr)



