import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title='bubbleBIZ', page_icon='💰', layout='wide')

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] {font-family: Inter, sans-serif;}
h1,h2,h3,.brand {font-family: 'Space Grotesk', sans-serif;}
.stApp {background: linear-gradient(180deg,#ffffff 0%,#f7faf7 100%);} 
.card {padding:1rem;border-radius:22px;background:white;box-shadow:0 10px 25px rgba(0,0,0,.06);border:1px solid #eef2ee;}
.metric {font-size:2rem;font-weight:700;}
</style>
''', unsafe_allow_html=True)

if 'sales' not in st.session_state: st.session_state.sales=[]
if 'expenses' not in st.session_state: st.session_state.expenses=[]
if 'budget' not in st.session_state: st.session_state.budget=1000.0

st.markdown("<h1 class='brand'>bubbleBIZ 💰</h1>", unsafe_allow_html=True)
st.caption('Business Control System for Small Food Businesses')

with st.sidebar:
    st.header('Control Panel')
    page = st.radio('Navigate',['Dashboard','Add Sale','Add Expense','Data','Settings'])
    st.session_state.budget = st.number_input('Monthly Budget',0.0,100000.0,st.session_state.budget,50.0)
    if st.button('Reset Demo Data'):
        st.session_state.sales=[]; st.session_state.expenses=[]; st.rerun()

def sales_df(): return pd.DataFrame(st.session_state.sales)
def exp_df(): return pd.DataFrame(st.session_state.expenses)

if page=='Add Sale':
    st.subheader('➕ Add Sale')
    with st.form('sale'):
        c1,c2=st.columns(2)
        item=c1.text_input('Item Name')
        category=c2.text_input('Category')
        c3,c4=st.columns(2)
        qty=c3.number_input('Qty',1,1000,1)
        price=c4.number_input('Unit Price',0.0,10000.0,0.0,0.5)
        pay=st.selectbox('Payment Method',['Cash','Card','Mobile'])
        if st.form_submit_button('Save Sale'):
            st.session_state.sales.append({'date':datetime.now(),'item':item,'category':category,'qty':qty,'price':price,'amount':qty*price,'payment':pay})
            st.success('Sale added')

elif page=='Add Expense':
    st.subheader('➖ Add Expense')
    with st.form('exp'):
        c1,c2=st.columns(2)
        cat=c1.selectbox('Expense Type',['Ingredients','Labor','Fuel','Rent','Marketing','Misc'])
        amt=c2.number_input('Amount',0.0,100000.0,0.0,1.0)
        note=st.text_input('Note')
        if st.form_submit_button('Save Expense'):
            st.session_state.expenses.append({'date':datetime.now(),'category':cat,'amount':amt,'note':note})
            st.success('Expense added')

elif page=='Data':
    st.subheader('📄 Records')
    st.write('Sales')
    st.dataframe(sales_df(), use_container_width=True)
    st.write('Expenses')
    st.dataframe(exp_df(), use_container_width=True)

elif page=='Settings':
    st.subheader('⚙️ Settings')
    st.info('Connect Supabase / Stripe in next version.')
    st.write('Current Budget:', st.session_state.budget)

else:
    s=sales_df(); e=exp_df()
    revenue = s['amount'].sum() if not s.empty else 0
    expenses = e['amount'].sum() if not e.empty else 0
    profit = revenue-expenses
    c1,c2,c3=st.columns(3)
    for c,title,val in [(c1,'Revenue',revenue),(c2,'Expenses',expenses),(c3,'Profit',profit)]:
        c.markdown(f"<div class='card'><div>{title}</div><div class='metric'>${val:,.0f}</div></div>", unsafe_allow_html=True)
    st.write('')
    if expenses>st.session_state.budget:
        st.error('🚨 Over budget. Reduce spending now.')
    else:
        st.success('✅ Spending within budget.')
    c4,c5=st.columns(2)
    if not e.empty:
        pie=e.groupby('category')['amount'].sum().reset_index()
        c4.plotly_chart(px.pie(pie,names='category',values='amount',title='Where Spending Goes'), use_container_width=True)
    if not s.empty:
        bar=s.groupby('item')['amount'].sum().reset_index().sort_values('amount',ascending=False)
        c5.plotly_chart(px.bar(bar,x='item',y='amount',title='Top Sellers'), use_container_width=True)
    if not s.empty:
        s['hour']=pd.to_datetime(s['date']).dt.hour
        hourly=s.groupby('hour')['amount'].sum().reset_index()
        st.plotly_chart(px.line(hourly,x='hour',y='amount',markers=True,title='Best Selling Hours'), use_container_width=True)
