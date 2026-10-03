import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="EcoSmart Gabès", page_icon="🌍", layout="wide")

LAT, LON = 33.8815, 10.0982

T = {
    "العربية": {
        "home":"الرئيسية","air":"جودة الهواء","analytics":"التحليلات",
        "map":"الخريطة","prediction":"التوقعات","about":"حول المشروع",
        "subtitle":"منصة ذكية لمراقبة البيئة وجودة الهواء في قابس",
        "aqi":"مؤشر جودة الهواء","pm25":"PM2.5","pm10":"PM10",
        "temp":"درجة الحرارة","humidity":"الرطوبة","wind":"سرعة الرياح",
        "co2":"ثاني أكسيد الكربون","no2":"ثاني أكسيد النيتروجين",
        "so2":"ثاني أكسيد الكبريت","o3":"الأوزون",
        "choose":"اختر المؤشر","average":"المتوسط",
        "maximum":"الأقصى","minimum":"الأدنى",
        "note":"بيانات جودة الهواء نمذجة وليست قياسات مباشرة من حساسات محلية.",
        "source":"المصدر: Open-Meteo / CAMS"
    },
    "Français": {
        "home":"Accueil","air":"Qualité de l'air","analytics":"Analyses",
        "map":"Carte","prediction":"Prévisions","about":"À propos",
        "subtitle":"Plateforme intelligente de surveillance environnementale à Gabès",
        "aqi":"Indice de qualité de l'air","pm25":"PM2.5","pm10":"PM10",
        "temp":"Température","humidity":"Humidité","wind":"Vitesse du vent",
        "co2":"Dioxyde de carbone","no2":"Dioxyde d'azote",
        "so2":"Dioxyde de soufre","o3":"Ozone",
        "choose":"Choisir l'indicateur","average":"Moyenne",
        "maximum":"Maximum","minimum":"Minimum",
        "note":"Les données de qualité de l'air sont modélisées et non mesurées par des capteurs locaux.",
        "source":"Source : Open-Meteo / CAMS"
    },
    "English": {
        "home":"Home","air":"Air Quality","analytics":"Analytics",
        "map":"Map","prediction":"Prediction","about":"About",
        "subtitle":"Smart environmental monitoring platform for Gabès",
        "aqi":"Air Quality Index","pm25":"PM2.5","pm10":"PM10",
        "temp":"Temperature","humidity":"Humidity","wind":"Wind Speed",
        "co2":"Carbon Dioxide","no2":"Nitrogen Dioxide",
        "so2":"Sulfur Dioxide","o3":"Ozone",
        "choose":"Choose indicator","average":"Average",
        "maximum":"Maximum","minimum":"Minimum",
        "note":"Air-quality data are modelled and are not direct local sensor measurements.",
        "source":"Source: Open-Meteo / CAMS"
    }
}

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#06111f,#0b1727,#06111f)}
.block-container{max-width:1450px;padding-top:2rem}
.hero{padding:30px;border-radius:24px;margin-bottom:25px;
background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1)}
.hero h1{font-size:42px;font-weight:800}
.hero p{color:#aebdca;font-size:17px}
.footer{text-align:center;color:#718395;padding:30px}
</style>
""", unsafe_allow_html=True)

language = st.sidebar.selectbox("🌐 Language", list(T.keys()))
t = T[language]

@st.cache_data(ttl=900)
def weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT, "longitude": LON,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "past_days": 2, "forecast_days": 3, "timezone": "auto"
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=900)
def air_data():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": LAT, "longitude": LON,
        "current": "european_aqi,pm10,pm2_5,carbon_dioxide,nitrogen_dioxide,sulphur_dioxide,ozone",
        "hourly": "european_aqi,pm10,pm2_5,carbon_dioxide,nitrogen_dioxide,sulphur_dioxide,ozone",
        "past_days": 2, "forecast_days": 3, "timezone": "auto"
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

try:
    weather = weather_data()
    air = air_data()
except Exception as e:
    st.error("❌ Cannot load Open-Meteo data")
    st.code(str(e))
    st.stop()

w = weather["current"]
a = air["current"]

st.markdown(
    f'<div class="hero"><h1>🌍 EcoSmart Gabès</h1><p>{t["subtitle"]}</p></div>',
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [t["home"],t["air"],t["analytics"],t["map"],t["prediction"],t["about"]]
)

def metric(label, value, unit=""):
    st.metric(label, "N/A" if value is None else f"{value:.1f} {unit}")

if page == t["home"]:
    st.header("📊 " + t["home"])
    c = st.columns(4)
    with c[0]: metric("🌫️ "+t["aqi"], a.get("european_aqi"))
    with c[1]: metric(t["pm25"], a.get("pm2_5"), "µg/m³")
    with c[2]: metric("🌡️ "+t["temp"], w.get("temperature_2m"), "°C")
    with c[3]: metric("💧 "+t["humidity"], w.get("relative_humidity_2m"), "%")

    c = st.columns(4)
    with c[0]: metric(t["pm10"], a.get("pm10"), "µg/m³")
    with c[1]: metric(t["co2"], a.get("carbon_dioxide"))
    with c[2]: metric(t["no2"], a.get("nitrogen_dioxide"), "µg/m³")
    with c[3]: metric("🌬️ "+t["wind"], w.get("wind_speed_10m"), "km/h")

    h = air["hourly"]
    df = pd.DataFrame({"Time":pd.to_datetime(h["time"]), "AQI":h["european_aqi"]}).dropna()
    fig = px.line(df, x="Time", y="AQI", markers=True, title=t["aqi"])
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif page == t["air"]:
    st.header("🌫️ " + t["air"])
    h = air["hourly"]
    df = pd.DataFrame({
        "Time":pd.to_datetime(h["time"]),
        "PM2.5":h["pm2_5"], "PM10":h["pm10"],
        "NO₂":h["nitrogen_dioxide"], "SO₂":h["sulphur_dioxide"],
        "O₃":h["ozone"]
    })
    choice = st.selectbox(t["choose"], ["PM2.5","PM10","NO₂","SO₂","O₃"])
    fig = px.line(df, x="Time", y=choice, markers=True, title=choice)
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif page == t["analytics"]:
    st.header("📊 " + t["analytics"])
    h = air["hourly"]
    df = pd.DataFrame({
        "Time":pd.to_datetime(h["time"]),
        "AQI":h["european_aqi"], "PM2.5":h["pm2_5"],
        "PM10":h["pm10"], "CO₂":h["carbon_dioxide"],
        "NO₂":h["nitrogen_dioxide"], "SO₂":h["sulphur_dioxide"],
        "O₃":h["ozone"]
    })
    choice = st.selectbox(t["choose"], ["AQI","PM2.5","PM10","CO₂","NO₂","SO₂","O₃"])
    d = df[["Time",choice]].dropna()
    c = st.columns(3)
    c[0].metric(t["average"], f"{d[choice].mean():.2f}")
    c[1].metric(t["maximum"], f"{d[choice].max():.2f}")
    c[2].metric(t["minimum"], f"{d[choice].min():.2f}")
    fig = px.area(d, x="Time", y=choice, title=choice)
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif page == t["map"]:
    st.header("🗺️ " + t["map"])
    m = folium.Map(location=[LAT,LON], zoom_start=12, tiles="CartoDB dark_matter")
    folium.Marker([LAT,LON], tooltip="EcoSmart Gabès", popup=t["source"]).add_to(m)
    folium.CircleMarker([33.894,10.103], radius=12, tooltip="Industrial Zone",
                        color="red", fill=True).add_to(m)
    folium.CircleMarker([33.870,10.120], radius=10, tooltip="Coastal Zone",
                        color="blue", fill=True).add_to(m)
    st_folium(m, width=1200, height=600)

elif page == t["prediction"]:
    st.header("🤖 " + t["prediction"])
    h = air["hourly"]
    df = pd.DataFrame({"Time":pd.to_datetime(h["time"]), "AQI":h["european_aqi"]}).dropna()
    recent = df.tail(48).copy()
    if len(recent) >= 10:
        x = np.arange(len(recent))
        slope, intercept = np.polyfit(x, recent["AQI"].values, 1)
        fx = np.arange(len(recent), len(recent)+24)
        pred = np.maximum(intercept + slope*fx, 0)
        ft = pd.date_range(recent["Time"].iloc[-1], periods=25, freq="h")[1:]
        future = pd.DataFrame({"Time":ft, "AQI":pred, "Type":"Prediction"})
        old = recent.copy()
        old["Type"] = "Historical"
        final = pd.concat([old,future], ignore_index=True)
        fig = px.line(final, x="Time", y="AQI", color="Type", markers=True)
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        st.info("This is a simple trend estimate, not an official air-quality forecast.")
    else:
        st.warning("Not enough data.")

elif page == t["about"]:
    st.header("🌍 " + t["about"])
    st.markdown(f"""
    ### EcoSmart Gabès
    مشروع لمراقبة البيئة وجودة الهواء في قابس باستعمال البيانات والذكاء الاصطناعي.

    **المستقبل:**
    - IoT sensors
    - Machine learning
    - Satellite data
    - Pollution alerts
    - AI environmental assistant

    ⚠️ {t["note"]}
    """)

st.markdown(
    f'<div class="footer">🌍 <b>EcoSmart Gabès</b><br>{t["source"]}</div>',
    unsafe_allow_html=True
)
