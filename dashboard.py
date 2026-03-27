import streamlit as st
import requests
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# -------------------
# 🔐 LOGIN PAGE
# -------------------

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.markdown("""
    <style>
    body {background-color:#0f172a;color:white}
    .title {text-align:center;font-size:60px;color:#22c55e}
    .box {text-align:center;margin-top:100px}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">🌍 EcoSmart Gabès</div>', unsafe_allow_html=True)

    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Industrial_pollution.jpg")

    password = st.text_input("🔐 أدخل كلمة السر", type="password")

    if st.button("دخول"):
        if password == "1972":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("❌ كلمة السر خاطئة")

    st.stop()

# -------------------
# 🌍 DASHBOARD
# -------------------

st.title("🌍 EcoSmart Gabès AI Dashboard")

lat, lon = 33.88, 10.10

weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m").json()
air = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide").json()

temp = weather["current"]["temperature_2m"]
hum = weather["current"]["relative_humidity_2m"]

pm25 = air["current"]["pm2_5"]
pm10 = air["current"]["pm10"]
co = air["current"]["carbon_monoxide"]
no2 = air["current"]["nitrogen_dioxide"]

# 🧠 AI CO2 estimation
X = np.array([[20,50,0.3,10,12],[22,55,0.4,15,15],[25,45,0.35,12,10]])
y = np.array([415,420,418])

model = LinearRegression()
model.fit(X, y)

co2 = model.predict([[temp, hum, co, no2, pm25]])[0]

# عرض القيم
col1, col2, col3 = st.columns(3)

col1.metric("🌡 Temp", f"{temp}°C")
col1.metric("💧 Humidity", f"{hum}%")

col2.metric("PM2.5", pm25)
col2.metric("PM10", pm10)

col3.metric("CO", co)
col3.metric("NO2", no2)
col3.metric("CO2 (AI)", round(co2,2))

# 📊 بيانات تاريخية
years = [1973,1980,1990,2000,2010,2020,2024]
pollution = [20,30,45,55,70,65,60]

df = pd.DataFrame({"Year":years,"Pollution":pollution})

fig = px.line(df,x="Year",y="Pollution",markers=True,title="Pollution Evolution")

st.plotly_chart(fig,use_container_width=True)

# 🗺 Heatmap
st.subheader("🗺 Pollution Heatmap")

points = [
    [33.88, 10.10, 80],
    [33.90, 10.12, 70],
    [33.85, 10.08, 90],
    [33.87, 10.15, 60],
    [33.89, 10.05, 85]
]

m = folium.Map(location=[33.88,10.10],zoom_start=10)
HeatMap(points).add_to(m)

st_folium(m, width=900)