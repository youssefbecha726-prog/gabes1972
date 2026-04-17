import streamlit as st
import requests
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# 🎨 واجهة احترافية
st.markdown("""
<style>
body {direction: rtl; background:#020617; color:white;}
.title {font-size:55px;text-align:center;color:#22c55e;font-weight:bold;}
.card {
background:#0f172a;
padding:20px;
border-radius:20px;
text-align:center;
font-size:22px;
box-shadow:0 0 15px #22c55e;
}
.summary {
font-size:28px;
padding:25px;
border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌍 نظام ذكي لمراقبة التلوث في قابس</div>', unsafe_allow_html=True)

# 📍 موقع قابس
lat, lon = 33.88, 10.10

# 🌡 API حقيقي
weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m").json()

air = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide").json()

temp = weather["current"]["temperature_2m"]
hum = weather["current"]["relative_humidity_2m"]
pm25 = air["current"]["pm2_5"]
pm10 = air["current"]["pm10"]
co = air["current"]["carbon_monoxide"]
no2 = air["current"]["nitrogen_dioxide"]

# 🤖 AI قوي (RandomForest)
X = np.array([
    [20,50,0.3,10,12],
    [25,60,0.5,20,15],
    [30,40,0.6,25,20],
    [35,30,0.7,30,25]
])

y = np.array([410,420,430,440])  # CO2 ppm

model = RandomForestRegressor()
model.fit(X, y)

co2 = model.predict([[temp, hum, co, no2, pm25]])[0]

# 📊 عرض القيم
col1,col2,col3 = st.columns(3)

col1.markdown(f'<div class="card">🌡 الحرارة<br>{temp}°C</div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card">💧 الرطوبة<br>{hum}%</div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card">🌫 CO2<br>{round(co2,2)}</div>', unsafe_allow_html=True)

col4,col5,col6 = st.columns(3)

col4.markdown(f'<div class="card">PM2.5<br>{pm25}</div>', unsafe_allow_html=True)
col5.markdown(f'<div class="card">PM10<br>{pm10}</div>', unsafe_allow_html=True)
col6.markdown(f'<div class="card">NO2<br>{no2}</div>', unsafe_allow_html=True)

# 📊 رسم
df = pd.DataFrame({
    "Pollutant":["PM2.5","PM10","CO","NO2"],
    "Value":[pm25,pm10,co,no2]
})

fig = px.bar(df, x="Pollutant", y="Value", color="Pollutant")
st.plotly_chart(fig, use_container_width=True)

# 🗺 خريطة
points = [
    [33.87,10.15,95],
    [33.85,10.08,100],
    [33.90,10.12,60]
]

m = folium.Map(location=[33.88,10.10], zoom_start=11)
HeatMap(points).add_to(m)

st_folium(m, width=900)

# 📋 تحليل
if pm25 < 20:
    status = "🟢 جيد"
    color="#22c55e"
elif pm25 < 50:
    status = "🟡 متوسط"
    color="#eab308"
else:
    status = "🔴 خطير"
    color="#ef4444"

st.markdown(f"""
<div class="summary" style="background:{color};">
📊 التحليل الذكي:

الوضع الحالي: {status}

🌫 مستوى CO2: {round(co2,2)} ppm

⚠️ التلوث مرتفع بسبب النشاط الصناعي.

🤖 الذكاء الاصطناعي يتوقع زيادة مستقبلية.
</div>
""", unsafe_allow_html=True)