import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from scipy.stats import chi2_contingency
from IPython.display import display
from itertools import combinations
from scipy.stats import kstest, spearmanr, pearsonr
warnings.filterwarnings("ignore")


class AutoEDA:

    def __init__(self):
        self.colors = ["#2146B2", "#E0CA27", "#F8C895", "#D98162", "#F2EFEB", "#26261B"]

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


    def numeric_correlations(self, dataframe):
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


    def identify_categorical_cols(self, df):
        return df.select_dtypes(include='O').columns
 
    def __cramers_v(self, confusion_matrix):
        chi2 = chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum().sum()
        r, k = confusion_matrix.shape
        return np.sqrt(chi2 / (n * (min(k, r) - 1)))

    def categorical_correlations(self, df, categorical_columns):
        correlations = []
        processed_pairs = set()  # Para rastrear los pares ya procesados

        
        for col1 in categorical_columns:
            for col2 in categorical_columns:
                if col1 != col2 and (col2, col1) not in processed_pairs:
                    confusion_matrix = pd.crosstab(df[col1], df[col2])
                    correlation = self.__cramers_v(confusion_matrix)
                    correlations.append((col1, col2, correlation))
                    processed_pairs.add((col1, col2))  # Añadir el par a los procesados

        weak_correlations = [item for item in correlations if 0.1 <= item[2] < 0.3]
        moderate_correlations = [item for item in correlations if 0.3 <= item[2] < 0.5]
        strong_correlations = [item for item in correlations if item[2] >= 0.5]
    
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
        color = self.colors[0] # Choose a color from the color palette
        plt.figure(figsize=(8, 4))
        plt.hist(df[column].dropna(), bins=bins, edgecolor='k', color=color)
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
        color = self.colors[1] # Choose a color from the color palette
        plt.figure(figsize=(8, 4))
        plt.scatter(df[x_column], df[y_column], color=color)
        plt.title(title if title else f'Scatter Plot of {x_column} vs {y_column}')
        plt.xlabel(xlabel if xlabel else x_column)
        plt.ylabel(ylabel if ylabel else y_column)
        plt.show()


    def plot_boxplot(self, df, column1, column2=None, title=None, xlabel=None, ylabel='Value'):
        """
        Plot a boxplot for one column or a comparison of two columns in the DataFrame.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column1 : str
            The primary column for which the boxplot is to be plotted.
        column2 : str, optional
            The secondary column to compare with the primary column (for grouped boxplot).
        title : str, optional
            Title of the plot.
        xlabel : str, optional
            Label for the x-axis.
        ylabel : str, optional (default='Value')
            Label for the y-axis.
        """
        if column2 is None:
            # Single column boxplot
            plt.figure(figsize=(8, 4))
            sns.boxplot(y=df[column1], color=self.colors[3])
            plt.title(title if title else f'Boxplot of {column1}')
            plt.ylabel(ylabel)
            plt.show()
        else:
            # Comparison of two columns
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=df[column2], y=df[column1], palette=self.colors)
            plt.title(title if title else f'Boxplot of {column1} by {column2}')
            plt.xlabel(column2)
            plt.ylabel(ylabel)
            plt.show()




    def visualize_pairplot(self, dataframe, columns, hue=None, height=5):
        """
        Visualize pair plots for selected columns of the DataFrame.
        
        Parameters:
        -----------
        dataframe : pandas.DataFrame
            The DataFrame containing the data to be visualized.
        
        columns : list of str
            List of column names to be included in the pair plot.
        
        hue : str, optional, default: None
            Column name to be used for color encoding.
        
        height : int, optional, default: 5
            Height of each facet in inches.
        
        Returns:
        --------
        None
        """
        if not all(col in dataframe.columns for col in columns):
            raise ValueError("One or more columns are not in the DataFrame.")
        
        # Create the pairplot with the specified hue and color palette
        pairplot = sns.pairplot(dataframe[columns + [hue]] if hue else dataframe[columns], 
                               hue=hue, palette=self.colors, height=height)

        plt.tight_layout()
        plt.show()

    def visualize_categorical_counts(self, dataframe, categorical_cols):
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
        
        def count_plotter(ax, col, data, colors):
            counted = data[col].value_counts()
            palette = colors[:len(counted)]  # Use only as many colors as there are categories
            sns.barplot(ax=ax, x=counted.index, y=counted.values, width=0.9, palette=palette)
            ax.set_title(f"{col} count graph")
            if col in ['JobRole', 'EducationField']:
                ax.set_xticklabels(labels=counted.index, rotation=90, fontsize=6)
            else:
                ax.set_xticklabels(labels=counted.index, fontsize=8)

        for i, category in enumerate(categorical_cols):
            if i < len(ax):
                count_plotter(ax[i], category, data=dataframe, colors=self.colors)
            else:
                # Hide unused subplots
                ax[i].axis('off')

        plt.show()

    def visualize_facet_grid(self, df, col_names, x_values, hue='gender'):
        """
        Create FacetGrid plots for given categorical columns and numerical values.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the data to be visualized.
        
        col_names : list of str
            List of categorical column names to be used for facets.
        
        x_values : list of str
            List of numerical column names to be plotted on the x-axis.
        
        hue : str, optional, default: 'Gender'
            Column name to be used for color encoding.
        
        Returns:
        --------
        None
        """
        if len(col_names) != len(x_values):
            raise ValueError("Length of col_names and x_values must be the same.")
        
        for col_name, x_value in zip(col_names, x_values):
            facet = sns.FacetGrid(df, col=col_name, hue=hue, aspect=1, palette=self.colors, col_wrap=3)
            facet.map(sns.kdeplot, x_value, fill=True)
            facet.set(xlim=[0, df[x_value].max()])
            facet.add_legend(label_order=df[hue].unique())
            plt.tight_layout()
            plt.show()

    def visualize_general_statistics(self, df, df_heatmap1, df_heatmap2):
        """
        Create a series of general statistics visualizations using subplots.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the data to be visualized.
        
        df_heatmap1 : pandas.DataFrame
            DataFrame for the first heatmap.
        
        df_heatmap2 : pandas.DataFrame
            DataFrame for the second heatmap.
        
        Returns:
        --------
        None
        """
        fig, ax = plt.subplots(3, 2, figsize=(15, 13))
        fig.suptitle('General Statistics')
        fig.subplots_adjust(wspace=0.4, hspace=0.5)
        
        # Boxplot for Department vs. Total Working Years
        sns.boxplot(ax=ax[0, 0], data=df, y='department', x='total_working_years', hue='gender', palette=self.colors[:2])
        ax[0, 0].set_title('Ages by Department', fontsize=14)
        
        # Boxplot for Education Field vs. Age
        sns.boxplot(ax=ax[0, 1], data=df, y='education_field', x='age', hue='gender', palette=self.colors[:2])
        ax[0, 1].set_title('Ages by Education Field', fontsize=14)
        
        # Heatmap for Job Role-Satisfaction Mapping
        sns.heatmap(ax=ax[1, 0], data=df_heatmap1, square=True, linewidth=1, cmap='Reds')
        ax[1, 0].set_title('Job Role-Satisfaction Mapping', fontsize=14)
        
        # Heatmap for Job Level-Involvement Mapping
        sns.heatmap(ax=ax[1, 1], data=df_heatmap2, square=True, linewidth=1, cmap='Blues')
        ax[1, 1].set_title('Job Level-Involvement Mapping', fontsize=14)
        
        # Histogram for Distribution of Salary Percent Hike
        sns.histplot(ax=ax[2, 0], data=df, x='percent_salary_hike', hue='gender', multiple='stack', palette=self.colors)
        ax[2, 0].set_title('Distribution of Salary Percent Hike', fontsize=14)
        
        # Histogram for Distribution of Years at Company
        sns.histplot(ax=ax[2, 1], data=df, x='years_at_company', hue='gender', multiple='stack', palette=self.colors)
        ax[2, 1].set_title('Distribution of Years at Company', fontsize=14)
        
        plt.show()


    def pieplot(self, data, columns, titles=None, explode_ratio=0.05):
        """
        Generates pie plots for specified columns in the dataframe and arranges them in a single row.

        Parameters:
        - data: pd.DataFrame, the dataframe containing the data.
        - columns: list of str, the names of the columns to plot.
        - titles: list of str, optional, titles for each pie plot.
        - explode_ratio: float, optional, the fraction by which to offset each wedge.

        Returns:
        - None, displays the pie plots.
        """
        num_columns = len(columns)
        
        if titles is None:
            titles = [None] * num_columns
        
        if num_columns == 0:
            raise ValueError("The 'columns' list must contain at least one column.")
        
        # Determine layout for subplots
        fig, axs = plt.subplots(1, num_columns, figsize=(num_columns * 5, 5))
        
        # Handle the case where there is only one column
        if num_columns == 1:
            axs = [axs]
        
        for ax, col, title in zip(axs, columns, titles):
            # Calculate the distribution
            distribution = data[col].value_counts()
            
            # Create the explode configuration
            explode = [explode_ratio] * len(distribution)
            
            # Generate the pie plot
            wedges, texts, autotexts = ax.pie(
                distribution,
                labels=distribution.index,
                autopct='%1.1f%%',
                startangle=140,
                colors=self.colors[:len(distribution)],
                explode=explode,
                shadow=True
            )
            
            # Set title if provided
            if title:
                ax.set_title(title, fontsize=16)
        
        plt.tight_layout()
        plt.show()


    def boxplot_distribution(self, data, category_column, value_column, title=None):
        """
        Generates a boxplot to show the distribution of a numerical value across different categories.

        Parameters:
        - data: pd.DataFrame, the dataframe containing the data.
        - category_column: str, the name of the categorical column (e.g., products).
        - value_column: str, the name of the numerical column (e.g., price).
        - title: str, optional, the title of the plot.

        Returns:
        - None, displays the boxplot.
        """
        plt.figure(figsize=(12, 6))
        
        # Create the boxplot using seaborn
        sns.boxplot(x=data[category_column], y=data[value_column], palette=self.colors)
        
        # Add title if provided
        if title:
            plt.title(title, fontsize=16)
        
        # Add labels
        plt.xlabel(category_column.capitalize())
        plt.ylabel(value_column.capitalize())
        
        plt.xticks(rotation=45)  # Rotate x-axis labels if needed for better readability
        plt.tight_layout()
        plt.show()
        

    def plot_comparative_analysis(self, df):
        """
        Generate a series of comparative plots to answer key questions about employee attrition.

        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        """
        
        # 2. Relationship between remote work and attrition
        plt.figure(figsize=(15, 8))
        plt.subplot(2, 2, 1)
        sns.barplot(x='remote_work', y='attrition', data=df, palette=self.colors)
        plt.title('Attrition by Remote Work Status')
        plt.xlabel('Remote Work')
        plt.ylabel('Attrition')

        # 3. Attrition by department
        plt.subplot(2, 2, 2)
        df['department'] = df['department'].astype(str)  # Ensure department is treated as a categorical variable
        sns.barplot(x='department', y='attrition', data=df, palette=self.colors)
        plt.title('Attrition by Department')
        plt.xlabel('Department')
        plt.ylabel('Attrition')
        plt.xticks(rotation=45)

        # 4. Attrition based on overtime (boxplot)
        plt.subplot(2, 2, 3)
        sns.boxplot(x='over_time', y='attrition', data=df, palette=self.colors)
        plt.title('Attrition by Overtime Status')
        plt.xlabel('Over Time')
        plt.ylabel('Attrition')

        # 5. Attrition by job role
        plt.subplot(2, 2, 4)
        df['job_role'] = df['job_role'].astype(str)  # Ensure job_role is treated as a categorical variable
        sns.barplot(x='job_role', y='attrition', data=df, palette=self.colors)
        plt.title('Attrition by Job Role')
        plt.xlabel('Job Role')
        plt.ylabel('Attrition')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

        # 8. Education level or field of study affecting attrition
        plt.figure(figsize=(15, 8))
        
        # Education level
        plt.subplot(1, 2, 1)
        sns.boxplot(x='education', y='attrition', data=df, palette=self.colors)
        plt.title('Attrition by Education Level')
        plt.xlabel('Education Level')
        plt.ylabel('Attrition')

        # Education field
        plt.subplot(1, 2, 2)
        df['education_field'] = df['education_field'].astype(str)  # Ensure education_field is treated as a categorical variable
        sns.barplot(x='education_field', y='attrition', data=df, palette=self.colors)
        plt.title('Attrition by Education Field')
        plt.xlabel('Education Field')
        plt.ylabel('Attrition')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

