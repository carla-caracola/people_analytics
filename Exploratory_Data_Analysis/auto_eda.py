import pandas as pd
import numpy as np
from IPython.display import display
from itertools import combinations
from scipy.stats import kstest, spearmanr, pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

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

    
    def __identify_linearity(self, dataframe, column_combinations_list):
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
        """
        Identifies correlations among numeric columns in the dataframe using Pearson or Spearman methods.

        Parameters:
        -----------
        dataframe : pandas.DataFrame
            The DataFrame containing the variables to analyze.

        Returns:
        --------
        results : dict
            A dictionary containing the correlation DataFrames. The keys are 'pearson' and 'spearman'.
            If all relationships are either linear or non-linear, only one key will be present.
        """
        # Select numeric columns
        numerics = dataframe.select_dtypes(include=np.number).columns
        
        # Generate all possible combinations of numeric columns
        num_combinations = list(combinations(numerics, 2))
        
        # Identify if the relationships are linear or non-linear
        linear, non_linear = self.__identify_linearity(dataframe, num_combinations)
        
        # Initialize the results dictionary
        results = {}

        if linear:
            # Apply Pearson correlation for linear relationships
            linear_columns = set([item for sublist in linear for item in sublist])
            df_pearson = dataframe[list(linear_columns)].corr(method="pearson")
            results['pearson'] = df_pearson

        if non_linear:
            # Apply Spearman correlation for non-linear relationships
            non_linear_columns = set([item for sublist in non_linear for item in sublist])
            df_spearman = dataframe[list(non_linear_columns)].corr(method="spearman")
            results['spearman'] = df_spearman
        
        return results


    def classify_correlations(self, correlation_df):
        """
        Classify the correlations in the given DataFrame into weak, moderate, and strong correlations.
        
        Parameters:
        -----------
        correlation_df : pandas.DataFrame
            DataFrame containing the correlation values between pairs of variables.
        
        Returns:
        --------
        None
        """
        weak_correlations = []
        moderate_correlations = []
        strong_correlations = []

        # To avoid duplicates, use a set to register processed pairs
        processed_pairs = set()

        for row in correlation_df.index:
            for col in correlation_df.columns:
                if row != col and (col, row) not in processed_pairs:
                    corr_value = correlation_df.at[row, col]
                    processed_pairs.add((row, col))
                    processed_pairs.add((col, row))

                    if 0.1 <= abs(corr_value) < 0.3:
                        weak_correlations.append((row, col, corr_value))
                    elif 0.3 <= abs(corr_value) < 0.7:
                        moderate_correlations.append((row, col, corr_value))
                    elif abs(corr_value) >= 0.7:
                        strong_correlations.append((row, col, corr_value))

        # Print the results
        print("Weak Correlations:")
        for item in weak_correlations:
            print(f"Between {item[0]} and {item[1]}: {item[2]:.2f}")

        print("\nModerate Correlations:")
        for item in moderate_correlations:
            print(f"Between {item[0]} and {item[1]}: {item[2]:.2f}")

        print("\nStrong Correlations:")
        for item in strong_correlations:
            print(f"Between {item[0]} and {item[1]}: {item[2]:.2f}")

        # Return None, as we're only printing the results
        return None
        # return weak_correlations, moderate_correlations, strong_correlations
    

    def plot_histogram(self, df, column, bins=10, title=None, xlabel=None, ylabel='Frequency'):
        """
        Plot a histogram for a given column in the DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column for which the histogram is to be plotted.
        bins : int, optional (default=10)
            Number of bins for the histogram.
        title : str, optional
            Title of the plot.
        xlabel : str, optional
            Label for the x-axis.
        ylabel : str, optional (default='Frequency')
            Label for the y-axis.
        """
        plt.figure(figsize=(8, 4))
        plt.hist(df[column].dropna(), bins=bins, edgecolor='k')
        plt.title(title if title else f'Histogram of {column}')
        plt.xlabel(xlabel if xlabel else column)
        plt.ylabel(ylabel)
        plt.show()


    def plot_scatter(self, df, x_column, y_column, title=None, xlabel=None, ylabel=None):
        """
        Plot a scatter plot for two given columns in the DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        x_column : str
            The column for the x-axis.
        y_column : str
            The column for the y-axis.
        title : str, optional
            Title of the plot.
        xlabel : str, optional
            Label for the x-axis.
        ylabel : str, optional
            Label for the y-axis.
        """
        plt.figure(figsize=(8, 4))
        plt.scatter(df[x_column], df[y_column])
        plt.title(title if title else f'Scatter Plot of {x_column} vs {y_column}')
        plt.xlabel(xlabel if xlabel else x_column)
        plt.ylabel(ylabel if ylabel else y_column)
        plt.show()


    def plot_boxplot(self, df, column, title=None, xlabel=None, ylabel='Value'):
        """
        Plot a boxplot for a given column in the DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column for which the boxplot is to be plotted.
        title : str, optional
            Title of the plot.
        xlabel : str, optional
            Label for the x-axis.
        ylabel : str, optional (default='Value')
            Label for the y-axis.
        """
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=df[column])
        plt.title(title if title else f'Boxplot of {column}')
        plt.xlabel(xlabel if xlabel else column)
        plt.ylabel(ylabel)
        plt.show()


    def visualize_pairplot(self, dataframe, columns, height=5):
        """
        Visualize pair plots for selected columns of the DataFrame.
        
        Parameters:
        -----------
        dataframe : pandas.DataFrame
            The DataFrame containing the data to be visualized.
        
        columns : list of str
            List of column names to be included in the pair plot.
        
        height : int, optional, default: 5
            Height of each facet in inches.
        
        Returns:
        --------
        None
        """
        if not all(col in dataframe.columns for col in columns):
            raise ValueError("One or more columns are not in the DataFrame.")
        
        sns.pairplot(dataframe[columns], height=height)
        plt.tight_layout()
        plt.show()


    def visualize(self, df, plot_type, **kwargs):
        """
        Master method to visualize different types of plots.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        plot_type : str
            Type of plot ('histogram', 'scatter', 'correlation_matrix', 'boxplot').
        kwargs : dict
            Additional keyword arguments for the specific plot methods.

        Example usage:
        --------------
        Plot histogram
        eda.visualize(df, 'histogram', column='price', bins=20, title='Price Distribution')

        Plot scatter plot
        eda.visualize(df, 'scatter', x_column='price', y_column='units_sold', title='Price vs Units Sold')
        """
        if plot_type == 'histogram':
            self.plot_histogram(df, **kwargs)
        elif plot_type == 'scatter':
            self.plot_scatter(df, **kwargs)
        elif plot_type == 'pairplot':
            self.visualize_pairplot(df, **kwargs)
        elif plot_type == 'boxplot':
            self.plot_boxplot(df, **kwargs)
        else:
            print(f"Plot type '{plot_type}' is not supported.")


    def visualize_categorical_counts(self, dataframe, categorical_cols): # TEST PENDING
        """
        Visualize count plots for categorical columns in the DataFrame.
        
        Parameters:
        -----------
        dataframe : pandas.DataFrame
            The DataFrame containing the data to be visualized.
        
        categorical_cols : list of str
            List of categorical column names to be included in the count plots.
        
        Returns:
        --------
        None
        """
        num_cols = len(categorical_cols)
        num_rows = (num_cols + 1) // 2  # Calculate number of rows needed for subplots
        fig, ax = plt.subplots(num_rows, 2, figsize=(10, num_rows * 4))
        fig.subplots_adjust(hspace=0.5)
        
        # Flatten the axes array for easier indexing
        if num_rows > 1:
            ax = ax.flatten()
        else:
            ax = [ax]
        
        def count_plotter(ax, col, data):
            counted = data[col].value_counts()
            sns.barplot(ax=ax, x=counted.index, y=counted.values, width=0.9, palette='Set1')
            ax.set_title(f"{col} count graph")
            if col in ['JobRole', 'EducationField']:
                ax.set_xticklabels(labels=counted.index, rotation=90, fontsize=6)
            else:
                ax.set_xticklabels(labels=counted.index, fontsize=8)

        for i, category in enumerate(categorical_cols):
            if i < len(ax):
                count_plotter(ax[i], category, data=dataframe)
            else:
                # Hide unused subplots
                ax[i].axis('off')

        plt.show()

