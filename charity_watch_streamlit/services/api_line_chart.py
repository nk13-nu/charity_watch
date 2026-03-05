import pandas as pd
import plotly.express as px
import streamlit as st

def build_charity_income_line_chart(charity_name: str, df: pd.DataFrame) -> None:
    """
    Plots the financial history for the given charity's financial data
    """
    #if the dataframe is empty, that is there is no data we raise a streamlit warning
    if df.empty:
        st.warning("There is non Financial Data in the Charity Commission for this Charity.")
        return

    #we need to melt the data so that plotly can work on long format taking year as the id and the three financial categories as values variables
    df = df.melt(id_vars="Year", value_vars=["Income", "Expenditure", "Govt Grants"], var_name="Category", value_name="Amount")

    #now we define the plotly express figure
    fig = px.line(df, x="Year", y="Amount", color="Category", markers=True, title=f"{charity_name} 5-year financial history", labels={"Amount": "Amount (£)", "Year": "Year"},)

    #finally we update the layout to show all years, reformat the financial values and adjust the tooltip for better interaction
    fig.update_layout(xaxis=dict(dtick=1), yaxis=dict(tickformat=",.0f", tickprefix="£"), hovermode="x unified",)

    #and we plot the chart using streamlit
    st.plotly_chart(fig, use_container_width=True)

