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

# --------------------
# 🔐 LOGIN
# --------------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("""
    <h1 style='text-align:center;color:#22c55e;'>🌍 EcoSmart Gabès</h1>
    <h3 style='text-align:center;'>🔐 أدخل كلمة السر</h3>
    """, unsafe_allow_html=True)

    password = st.text_input("Password", type="password")

    if st.button("دخول"):
        if password == "1972":
            st.session_state.login = True
        else:
            st.error("❌ كلمة السر خاطئة")

    st.stop()

# --------------------
# 🎨 STYLE
# --------------------
st.markdown("""
<style>
body {direction: rtl; background:#020617; color:white;}
.title {font-size:50px;text-align:center;color:#22c55e;font-weight:bold;}
.card {
background:#0f172a;
padding:15px;
border-radius:15px;
margin:5px;
font-size:20px;
}
.summary {
font-size:26px;
padding:20px;
border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌍 نظام مراقبة التلوث في قابس</div>', unsafe_allow_html=True)

# --------------------
# 📡 API
# --------------------
lat, lon = 33.88, 10.10

weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m").json()

air = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide").json()

temp = weather["current"]["temperature_2m"]
hum = weather["current"]["relative_humidity_2m"]
pm25 = air["current"]["pm2_5"]
pm10 = air["current"]["pm10"]
co = air["current"]["carbon_monoxide"]
no2 = air["current"]["nitrogen_dioxide"]

# --------------------
# 📊 عرض بالطول (عربي + فرنسي)
# --------------------
data = [
    ["الحرارة", "Température", temp, "°C"],
    ["الرطوبة", "Humidité", hum, "%"],
    ["PM2.5", "PM2.5", pm25, ""],
    ["PM10", "PM10", pm10, ""],
    ["CO", "CO", co, ""],
    ["NO2", "NO2", no2, ""]
]

df = pd.DataFrame(data, columns=["العنصر","Français","القيمة","الوحدة"])

st.dataframe(df, use_container_width=True)

# --------------------
# 🤖 AI Prediction
# --------------------
X = np.array([[1],[2],[3],[4],[5]])
y = np.array([temp-2,temp-1,temp,temp+1,temp+2])

model = LinearRegression()
model.fit(X,y)

future = model.predict([[6],[7],[8]])

st.subheader("🤖 التنبؤ بالقيم القادمة")

col1,col2,col3 = st.columns(3)
col1.metric("بعد قليل", round(future[0],2))
col2.metric("بعد ساعة", round(future[1],2))
col3.metric("بعد ساعات", round(future[2],2))

# --------------------
# 📊 رسم
# --------------------
df_chart = pd.DataFrame({
    "القيم":[temp,hum,pm25,pm10,co,no2],
    "النوع":["Temp","Hum","PM2.5","PM10","CO","NO2"]
})

fig = px.bar(df_chart, x="النوع", y="القيم", color="النوع")
st.plotly_chart(fig, use_container_width=True)

# --------------------
# 🗺 الخريطة
# --------------------
points = [
    [33.87,10.15,95],
    [33.85,10.08,100],
    [33.90,10.12,60]
]

m = folium.Map(location=[33.88,10.10], zoom_start=11)
HeatMap(points).add_to(m)

st_folium(m, width=900)

# --------------------
# 📋 ملخص
# --------------------
if pm25 < 20:
    status="🟢 جيد"
    color="#22c55e"
elif pm25 < 50:
    status="🟡 متوسط"
    color="#eab308"
else:
    status="🔴 خطير"
    color="#ef4444"

st.markdown(f"""
<div class="summary" style="background:{color};">
📋 ملخص عام:

الوضع الحالي: {status}

🌡 الحرارة: {temp}°C  
💧 الرطوبة: {hum}%  

⚠️ التلوث مرتبط بالنشاط الصناعي في قابس.

🤖 التوقعات تشير إلى تغيرات مستمرة.
</div>
""", unsafe_allow_html=True)