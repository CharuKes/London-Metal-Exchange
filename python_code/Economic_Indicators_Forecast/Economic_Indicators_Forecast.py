import streamlit as st
import mysql.connector as sql
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.statespace.sarimax import SARIMAX
from abc import ABC, abstractmethod


class EconomicForecastDashboardBase(ABC):
    def __init__(self):
        # Initialize instance variables
        self.df = None  # DataFrame to store fetched data
        self.fig = None  # Plotly figure for visualization

    @abstractmethod
    def fetch_data(self):
        """
        Abstract method to fetch data from a data source.
        """
        pass

    @abstractmethod
    def sarima_model_plot(self, column_name, subplot_index):
        """
        Abstract method to perform SARIMA modeling and plot for a specific variable.

        Parameters:
        - column_name (str): Name of the column/variable in the dataset.
        - subplot_index (int): Index of the subplot for visualization.
        """
        pass

    @abstractmethod
    def main(self):
        """
        Abstract method to define the main functionality of the economic forecast dashboard.
        """
        pass


class EconomicForecastDashboard(EconomicForecastDashboardBase):
    @property
    def data_frame(self):
        return self.df

    @data_frame.setter
    def data_frame(self, value):
        self.df = value

    def fetch_data(self):
        """
        Implementation of fetching data from a MySQL database and performing data preprocessing.
        """
        # Establish a connection to the MySQL database and fetch data
        mydb = sql.connect(host='localhost', user='root', port=3306, database='maverick', use_pure=True)
        mycursor = mydb.cursor()

        query = "SELECT Year, Month, Inflation, Interest_Rates, GDP_Growth FROM Monthly_metal_Prices_and_Economic_Indicators"
        mycursor.execute(query)

        data = mycursor.fetchall()
        columns = [desc[0] for desc in mycursor.description]
        self.df = pd.DataFrame(data, columns=columns)

        mydb.close()

        # Perform data preprocessing
        self.df['Date'] = pd.to_datetime(self.df[['Year', 'Month']].assign(DAY=1))
        self.df.set_index('Date', inplace=True)
        numeric_columns = ['Inflation', 'Interest_Rates', 'GDP_Growth']
        self.df[numeric_columns] = self.df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    def sarima_model_plot(self, column_name, subplot_index):
        """
        Implementation of SARIMA modeling and plotting for a specific variable.

        Parameters:
        - column_name (str): Name of the column/variable in the dataset.
        - subplot_index (int): Index of the subplot for visualization.
        """
        # Extract data for the specified variable
        sarima_data = self.df[column_name]

        # Fit SARIMA model
        model = SARIMAX(sarima_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        results = model.fit()

        # Make predictions using the SARIMA model
        pred = results.get_forecast(steps=120)

        # Plot original data
        self.fig.add_trace(go.Scatter(x=sarima_data.index, y=sarima_data, mode='lines', name=f'Original Data'),
                           row=1, col=subplot_index)

        # Plot forecast with a different line color (e.g., red)
        self.fig.add_trace(go.Scatter(x=pd.date_range(start=sarima_data.index[-1], periods=121, freq='M')[1:],
                                      y=pred.predicted_mean, mode='lines', name=f'Forecast', line=dict(color='black')),
                           row=1, col=subplot_index)

    def main(self):
        """
        Implementation of the main functionality of the economic forecast dashboard.
        """
        # Streamlit app main function
        st.title("Economic Indicators Forecast")

        # Fetch data from MySQL and perform SARIMA modeling for each variable
        self.fetch_data()

        # Create a subplot for each economic indicator
        self.fig = make_subplots(rows=1, cols=3, shared_xaxes=True,
                                 subplot_titles=["Inflation", "Interest Rates", "GDP Growth"])

        for i, column in enumerate(self.df.columns[2:]):
            self.sarima_model_plot(column, i + 1)

        # Display the Plotly figure in the Streamlit app
        st.plotly_chart(self.fig)


if __name__ == "__main__":
    # Run the Streamlit app when the script is executed
    dashboard = EconomicForecastDashboard()
    dashboard.main()
