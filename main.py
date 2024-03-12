#import all the necessary modules.
import streamlit as st
from datetime import timedelta, date
import yfinance as yf
from plotly import graph_objs as go
from dateutil.relativedelta import relativedelta
import time



start_date = date.today() - relativedelta(months=3)
end_date = date.today()


st.title("TradeInfo")

user_input = st.text_input('Enter NSE Code:')
user_input= user_input.strip()

# def validate_ticker(tickername):
#     IsTickerValid = False
    
#     ticker=yf.Ticker(ticker=tickername+'.NS')
    
#     try:
#         ticker=ticker.info
#         IsTickerValid=True
#     except HTTPError as err:
#         if err.code == 404:
#             IsTickerValid=False
#     return IsTickerValid
def generate_short_summary(tickername):
    summary = yf.Ticker(tickername+".NS")
    try:
        Stockinfo = summary.info
        Short_Description =  Stockinfo['longBusinessSummary']
    except:
        if tickername!='':
            Short_Description=st.subheader('Cannot get info, it probably does not exist')
        else:
            Short_Description= st.write('Processing data')
    return Short_Description

def generate_info_table(tickername):
    info = yf.Ticker(tickername + ".NS")
    try:
        Stockinfo = info.info
        Address = Stockinfo['address1'] + ', ' + Stockinfo['address2']
        Origin = Stockinfo['country'] + ', ' + Stockinfo['city']
        Sector = Stockinfo['sector']
        Website = Stockinfo['website']
        values = [['Address', 'Origin', 'Sector', 'Website'],  # 1st col
                  [Address, Origin, Sector, Website]]
        fig = go.Figure(data=[go.Table(
            columnorder=[1, 2],
            columnwidth=[50, 200],
            header=dict(
                values=[['<b>Company Details</b>'],
                        ['<b>Info</b>']],
                line_color='black',
                fill_color='#F45F5F',
                align=['center'],
                font=dict(color='black', size=15),
                height=30
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
    except:
        print("Error occurred:")
        fig = go.Figure()
    
    return fig


def generate_data(tickername):
    info= yf.Ticker(tickername+'.NS')
    history = info.history(period='3mo')
    return history


def generate_chart(tickername):
    tickername = tickername+'.NS'
    df= yf.download(tickername, start_date, end_date)
    figure= go.Figure(
        data=[
            go.Candlestick(
                x= df.index,
                low = df['Low'],
                high = df['High'],
                close = df['Close'],
                open = df['Open']
            )
        ]
    )
    figure.update_layout(xaxis_title='Date',yaxis_title='Price')
    return figure

def predict_rally(tickername):
    tickername = tickername+'.NS'
    data= yf.Ticker(ticker=tickername)
    tickerdata=data.info
    fiftydaymoving = yf.download(tickers=tickername, period='50d', interval='1d')
    dayavg= fiftydaymoving['Close']
    total= dayavg.sum()
    fiftydayavg= total/50  
    marketprice = tickerdata['currentPrice']
    if fiftydayavg > marketprice:
        analysis = '50Day Moving Avg = '+str(fiftydayavg)+'. Currently, the 50 Day Moving average is greater than current price. Thus, the stock is Bullish.'
    elif fiftydayavg < marketprice:
        analysis ='50Day Moving Avg = '+str(fiftydayavg)+ '. Currently, the 50 Day Moving average is smaller than current price. Thus, the stock is Bearish.'
    else:
        analysis ='50Day Moving Avg = '+str(fiftydayavg)+'. Currently, the stock is at support.'
    
    return analysis


print(predict_rally('HSCL'))
 
if user_input:
    
    st.write('Processing Data for you')
    time.sleep(0.65)
    st.subheader("Description:")
    companyinfo =generate_short_summary(user_input)
    try:
        st.write(companyinfo)
        st.subheader('Company Info:')
        data = generate_info_table(user_input)
        st.plotly_chart(data, unsafe_allow_html=True)
        st.subheader('Stock Details (Last 3 Months)')
        st.write(generate_data(user_input))
        st.subheader('Chart')
        st.plotly_chart(generate_chart(user_input))
        st.subheader('Suggestion')
        st.write(predict_rally(user_input))
    except Exception as e:
        print("Error Occured")

else: 
    st.write('Please Enter a Validate NSE Symbol')