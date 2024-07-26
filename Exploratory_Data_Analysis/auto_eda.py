import pandas as pd
from IPython.display import display

class AutoEDA:
    def __init__(self):
        pass

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


    def explo_df(self, df, column=None):
        """
        Explores a DataFrame or a specific column and prints various statistics.
        
        Parameters:
        - df (DataFrame): The DataFrame to explore.
        - column (str or list, optional): The column or columns to explore. If None, explore the entire DataFrame.
        """
        if column is None:
            # General DataFrame exploration
            print("DataFrame Information:")
            display(df.info())
            print("\nFirst 10 rows of the DataFrame:")
            display(df.head(10))
            print("\nLast 10 rows of the DataFrame:")
            display(df.tail(10))
            print("\nStatistical description of the DataFrame (numeric):")
            display(df.describe().T)
            print("\nStatistical description of the DataFrame (categorical):")
            display(df.describe(include='object').T)
            print("\nCount of null values per column:")
            display(df.isnull().sum())
            print("\nPercentage of null values per column (only columns with nulls):")
            null_percentage = round(df.isnull().sum()/df.shape[0]*100, 2)
            display(null_percentage[null_percentage > 0])
            print("\nRows with all values as null:")
            all_null_rows = df[df.isnull().all(axis=1)]
            if not all_null_rows.empty:
                display(all_null_rows)
            else:
                print("There is no rows with all values as null.")
            print("\nCount of duplicate rows:")
            display(df.duplicated().sum())
        else:
            # Column(s) exploration
            if isinstance(column, str):
                column = [column]  # Convert to list if a single column is passed as a string
            for col in column:
                print(f"\nExploration of the column: {col}")
                if df[col].dtype in ['int64', 'float64']:
                    print("\nStatistical description (numeric):")
                    display(df[col].describe())
                else:
                    print("\nStatistical description (categorical):")
                    display(df[col].describe(include='object'))
                print("\nCount of null values:")
                display(df[col].isnull().sum())
                print("\nCount of unique values:")
                display(df[col].nunique())
                print("\nUnique values:")
                display(df[col].unique())
                print("\nValue Counts:")
                display(df[col].value_counts())
                print("\nMost frequent value (mode):")
                display(df[col].mode().iloc[0])
                print("\nCount of duplicates in the column:")
                display(df.duplicated(subset=[col]).sum())
