#import all the necessary modules.
import streamlit as st
from datetime import timedelta, date
import yfinance as yf
from plotly import graph_objs as go
from dateutil.relativedelta import relativedelta


start_date = date.today() - relativedelta(months=3)
todays_date = date.today()

st.title("TradeTutor")

user_input = st.text_input('Enter NSE Label:')

def generate_info_table(tickername):
    info = yf.Ticker(tickername+".NS")
    Stockinfo = info.info
    print(Stockinfo)
    Address = Stockinfo['address1']+', '+ Stockinfo['address2']
    Origin = Stockinfo['country'] +', '+ Stockinfo['city']
    Sector = Stockinfo['sector']
    Website = Stockinfo['website']
    values = [['Address', 'Origin', 'Sector', 'Website', ], #1st col
  [Address,Origin,Sector,Website]]
    fig = go.Figure(data=[go.Table(
  columnorder = [1,2],
  columnwidth = [100,400],
  header = dict(
    values = [['<b>Company Details</b><br>as of July 2017'],
                  ['<b>Info</b>']],
    line_color='black',
    fill_color='#F45F5F',
    align=['center'],
    font=dict(color='black', size=15),
    height=40
  ),
  cells=dict(
    values=values,
    line_color='darkslategray',
    fill=dict(color=['white', 'white']),
    align=['center'],
    font_size=15,
    height=30)
    )
])
    
    return fig
data = generate_info_table(user_input)
st.write(data)