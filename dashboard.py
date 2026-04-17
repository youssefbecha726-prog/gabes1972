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
# 🔐 LOGIN
# -------------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("<h1 style='text-align:center;color:#22c55e;'>🌍 EcoSmart Gabès</h1>", unsafe_allow_html=True)
    password = st.text_input("🔐 كلمة السر", type="password")

    if st.button("دخول"):
        if password == "1972":
            st.session_state.login = True
        else:
            st.error("❌ كلمة السر خاطئة")

    st.stop()

# -------------------
# 🎨 STYLE
# -------------------
st.markdown("""
<style>
body {direction: rtl; background:#020617; color:white;}
.title {font-size:50px;text-align:center;color:#22c55e;font-weight:bold;}

.custom-table {
    width:100%;
    border-collapse:collapse;
    font-size:22px;
}
.custom-table th, .custom-table td {
    padding:10px;
    border-bottom:1px solid #333;
}
.ar {text-align:right;font-weight:bold;}
.val {text-align:center;}
.fr {text-align:left;color:#9ca3af;}

.summary {
    font-size:26px;
    padding:20px;
    border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌍 نظام مراقبة التلوث في قابس</div>', unsafe_allow_html=True)

# -------------------
# 📡 API
# -------------------
lat, lon = 33.88, 10.10

weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m").json()
air = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide").json()

temp = weather["current"]["temperature_2m"]
hum = weather["current"]["relative_humidity_2m"]
pm25 = air["current"]["pm2_5"]
pm10 = air["current"]["pm10"]
co = air["current"]["carbon_monoxide"]
no2 = air["current"]["nitrogen_dioxide"]

# -------------------
# 📊 TABLE
# -------------------
st.markdown(f"""
<table class="custom-table">
<tr>
<th class="ar">العنصر</th>
<th class="val">القيمة</th>
<th class="fr">Français</th>
</tr>

<tr><td class="ar">الحرارة</td><td class="val">{temp} °C</td><td class="fr">Température</td></tr>
<tr><td class="ar">الرطوبة</td><td class="val">{hum} %</td><td class="fr">Humidité</td></tr>
<tr><td class="ar">PM2.5</td><td class="val">{pm25}</td><td class="fr">PM2.5</td></tr>
<tr><td class="ar">PM10</td><td class="val">{pm10}</td><td class="fr">PM10</td></tr>
<tr><td class="ar">CO</td><td class="val">{co}</td><td class="fr">CO</td></tr>
<tr><td class="ar">NO2</td><td class="val">{no2}</td><td class="fr">NO2</td></tr>
</table>
""", unsafe_allow_html=True)

# -------------------
# 🤖 AI Prediction
# -------------------
X = np.array([[1],[2],[3],[4],[5]])
y = np.array([temp-2,temp-1,temp,temp+1,temp+2])

model = LinearRegression()
model.fit(X,y)

future = model.predict([[6],[7],[8]])

st.subheader("🤖 التنبؤ")

col1,col2,col3 = st.columns(3)
col1.metric("قريب", round(future[0],2))
col2.metric("بعد قليل", round(future[1],2))
col3.metric("لاحقاً", round(future[2],2))

# -------------------
# 📊 CHART
# -------------------
df_chart = pd.DataFrame({
    "النوع":["Temp","Hum","PM2.5","PM10","CO","NO2"],
    "القيم":[temp,hum,pm25,pm10,co,no2]
})

fig = px.bar(df_chart, x="النوع", y="القيم", color="النوع")
st.plotly_chart(fig, use_container_width=True)

# -------------------
# 🗺 MAP
# -------------------
points = [
    [33.87,10.15,95],
    [33.85,10.08,100],
    [33.90,10.12,60]
]

m = folium.Map(location=[33.88,10.10], zoom_start=11)
HeatMap(points).add_to(m)

st_folium(m, width=900)

# -------------------
# 📋 SUMMARY
# -------------------
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

⚠️ التلوث مرتبط بالنشاط الصناعي.

🤖 التوقعات تشير إلى تغيرات مستقبلية.
</div>
""", unsafe_allow_html=True)