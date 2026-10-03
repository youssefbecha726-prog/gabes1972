import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(
page_title="EcoSmart Gabès",
page_icon="🌍",
layout="wide"
)

LAT = 33.8815
LON = 10.0982

LANG = {
"العربية": {
"home": "الرئيسية",
"air": "جودة الهواء",
"analytics": "التحليلات",
"map": "الخريطة",
"prediction": "التوقعات",
"about": "حول المشروع",
"subtitle": "منصة ذكية لمراقبة البيئة وجودة الهواء في قابس",
"aqi": "مؤشر جودة الهواء",
"pm25": "PM2.5",
"pm10": "PM10",
"temp": "درجة الحرارة",
"humidity": "الرطوبة",
"wind": "سرعة الرياح",
"co2": "ثاني أكسيد الكربون",
"no2": "ثاني أكسيد النيتروجين",
"so2": "ثاني أكسيد الكبريت",
"o3": "الأوزون",
"choose": "اختر المؤشر",
"average": "المتوسط",
"maximum": "الأقصى",
"minimum": "الأدنى",
"industrial": "المنطقة الصناعية",
"coast": "المنطقة الساحلية",
"center": "وسط قابس",
"note": "بيانات جودة الهواء هي بيانات نمذجة وليست قياسات مباشرة من حساسات محلية.",
"source": "المصدر: Open-Meteo / CAMS"
},
"Français": {
"home": "Accueil",
"air": "Qualité de l'air",
"analytics": "Analyses",
"map": "Carte",
"prediction": "Prévisions",
"about": "À propos",
"subtitle": "Plateforme intelligente de surveillance environnementale à Gabès",
"aqi": "Indice de qualité de l'air",
"pm25": "PM2.5",
"pm10": "PM10",
"temp": "Température",
"humidity": "Humidité",
"wind": "Vitesse du vent",
"co2": "Dioxyde de carbone",
"no2": "Dioxyde d'azote",
"so2": "Dioxyde de soufre",
"o3": "Ozone",
"choose": "Choisir l'indicateur",
"average": "Moyenne",
"maximum": "Maximum",
"minimum": "Minimum",
"industrial": "Zone industrielle",
"coast": "Zone côtière",
"center": "Centre de Gabès",
"note": "Les données de qualité de l'air sont modélisées et non mesurées directement par des capteurs locaux.",
"source": "Source : Open-Meteo / CAMS"
},
"English": {
"home": "Home",
"air": "Air Quality",
"analytics": "Analytics",
"map": "Map",
"prediction": "Prediction",
"about": "About",
"subtitle": "Smart environmental monitoring platform for Gabès",
"aqi": "Air Quality Index",
"pm25": "PM2.5",
"pm10": "PM10",
"temp": "Temperature",
"humidity": "Humidity",
"wind": "Wind Speed",
"co2": "Carbon Dioxide",
"no2": "Nitrogen Dioxide",
"so2": "Sulfur Dioxide",
"o3": "Ozone",
"choose": "Choose indicator",
"average": "Average",
"maximum": "Maximum",
"minimum": "Minimum",
"industrial": "Industrial zone",
"coast": "Coastal zone",
"center": "Gabès center",
"note": "Air-quality data are modelled data and not direct measurements from local sensors.",
"source": "Source: Open-Meteo / CAMS"
}
}

if "language" not in st.session_state:
st.session_state.language = "العربية"

language = st.sidebar.selectbox(
"🌐 Language",
["العربية", "Français", "English"],
index=["العربية", "Français", "English"].index(
st.session_state.language
)
)

st.session_state.language = language
t = LANG[language]

st.markdown("""

<style>
.stApp {
    background:
    radial-gradient(circle at 10% 10%, rgba(0,180,216,.16), transparent 30%),
    radial-gradient(circle at 90% 20%, rgba(0,255,170,.10), transparent 30%),
    linear-gradient(135deg,#06111f,#0a1727,#07121f);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
}

.hero {
    padding: 35px;
    border-radius: 25px;
    margin-bottom: 25px;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.10);
}

.hero h1 {
    font-size: 44px;
    font-weight: 800;
}

.hero p {
    color: #aebdca;
    font-size: 18px;
}

.card {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: #718395;
    padding: 30px;
}
</style>

""", unsafe_allow_html=True)

@st.cache_data(ttl=900)
def get_weather():

```
url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": LAT,
    "longitude": LON,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "past_days": 2,
    "forecast_days": 3,
    "timezone": "auto"
}

r = requests.get(url, params=params, timeout=30)
r.raise_for_status()

return r.json()
```

@st.cache_data(ttl=900)
def get_air():

```
url = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": LAT,
    "longitude": LON,
    "current": "european_aqi,pm10,pm2_5,carbon_monoxide,carbon_dioxide,nitrogen_dioxide,sulphur_dioxide,ozone",
    "hourly": "european_aqi,pm10,pm2_5,carbon_monoxide,carbon_dioxide,nitrogen_dioxide,sulphur_dioxide,ozone",
    "past_days": 2,
    "forecast_days": 3,
    "timezone": "auto"
}

r = requests.get(url, params=params, timeout=30)
r.raise_for_status()

return r.json()
```

try:
weather = get_weather()
air = get_air()
except Exception as e:
st.error("❌ Error while loading data")
st.write(str(e))
st.stop()

wc = weather["current"]
ac = air["current"]

aqi = ac.get("european_aqi")
pm25 = ac.get("pm2_5")
pm10 = ac.get("pm10")
co2 = ac.get("carbon_dioxide")
no2 = ac.get("nitrogen_dioxide")
so2 = ac.get("sulphur_dioxide")
o3 = ac.get("ozone")

temperature = wc.get("temperature_2m")
humidity = wc.get("relative_humidity_2m")
wind = wc.get("wind_speed_10m")

st.markdown(
f""" <div class="hero"> <h1>🌍 EcoSmart Gabès</h1> <p>{t["subtitle"]}</p> </div>
""",
unsafe_allow_html=True
)

page = st.sidebar.radio(
"Navigation",
[
t["home"],
t["air"],
t["analytics"],
t["map"],
t["prediction"],
t["about"]
]
)

if page == t["home"]:

```
st.header("📊 " + t["home"])

c1, c2, c3, c4 = st.columns(4)

c1.metric(t["aqi"], f"{aqi:.1f}" if aqi is not None else "N/A")
c2.metric(t["pm25"], f"{pm25:.1f} µg/m³" if pm25 is not None else "N/A")
c3.metric(t["temp"], f"{temperature:.1f} °C" if temperature is not None else "N/A")
c4.metric(t["humidity"], f"{humidity:.0f} %" if humidity is not None else "N/A")

st.write("")

c1, c2, c3, c4 = st.columns(4)

c1.metric(t["pm10"], f"{pm10:.1f}" if pm10 is not None else "N/A")
c2.metric(t["co2"], f"{co2:.1f}" if co2 is not None else "N/A")
c3.metric(t["no2"], f"{no2:.1f}" if no2 is not None else "N/A")
c4.metric(t["wind"], f"{wind:.1f} km/h" if wind is not None else "N/A")

hourly = air["hourly"]

df = pd.DataFrame({
    "Time": pd.to_datetime(hourly["time"]),
    "AQI": hourly["european_aqi"],
    "PM2.5": hourly["pm2_5"],
    "PM10": hourly["pm10"]
})

st.subheader("📈 Air Quality")

fig = px.line(
    df,
    x="Time",
    y="AQI",
    markers=True,
    title=t["aqi"]
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)
```

elif page == t["air"]:

```
st.header("🌫️ " + t["air"])

hourly = air["hourly"]

df = pd.DataFrame({
    "Time": pd.to_datetime(hourly["time"]),
    "PM2.5": hourly["pm2_5"],
    "PM10": hourly["pm10"],
    "NO2": hourly["nitrogen_dioxide"],
    "SO2": hourly["sulphur_dioxide"],
    "O3": hourly["ozone"]
})

choice = st.selectbox(
    t["choose"],
    ["PM2.5", "PM10", "NO2", "SO2", "O3"]
)

fig = px.line(
    df,
    x="Time",
    y=choice,
    markers=True,
    title=choice
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)
```

elif page == t["analytics"]:

```
st.header("📊 " + t["analytics"])

hourly = air["hourly"]

df = pd.DataFrame({
    "Time": pd.to_datetime(hourly["time"]),
    "AQI": hourly["european_aqi"],
    "PM2.5": hourly["pm2_5"],
    "PM10": hourly["pm10"],
    "CO2": hourly["carbon_dioxide"],
    "NO2": hourly["nitrogen_dioxide"],
    "SO2": hourly["sulphur_dioxide"],
    "O3": hourly["ozone"]
})

choice = st.selectbox(
    t["choose"],
    ["AQI", "PM2.5", "PM10", "CO2", "NO2", "SO2", "O3"]
)

data = df[["Time", choice]].dropna()

c1, c2, c3 = st.columns(3)

c1.metric(
    t["average"],
    f"{data[choice].mean():.2f}"
)

c2.metric(
    t["maximum"],
    f"{data[choice].max():.2f}"
)

c3.metric(
    t["minimum"],
    f"{data[choice].min():.2f}"
)

fig = px.area(
    data,
    x="Time",
    y=choice,
    title=choice
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(
    fig,
    use_container_width=True
)
```

elif page == t["map"]:

```
st.header("🗺️ " + t["map"])

m = folium.Map(
    location=[LAT, LON],
    zoom_start=12,
    tiles="CartoDB dark_matter"
)

folium.Marker(
    [LAT, LON],
    popup=t["center"],
    tooltip=t["center"]
).add_to(m)

folium.CircleMarker(
    [33.894, 10.103],
    radius=12,
    tooltip=t["industrial"],
    popup=t["industrial"],
    color="red",
    fill=True
).add_to(m)

folium.CircleMarker(
    [33.870, 10.120],
    radius=10,
    tooltip=t["coast"],
    popup=t["coast"],
    color="blue",
    fill=True
).add_to(m)

st_folium(
    m,
    width=1200,
    height=600
)
```

elif page == t["prediction"]:

```
st.header("🤖 " + t["prediction"])

hourly = air["hourly"]

df = pd.DataFrame({
    "Time": pd.to_datetime(hourly["time"]),
    "AQI": hourly["european_aqi"]
}).dropna()

recent = df.tail(48)

if len(recent) >= 10:

    x = np.arange(len(recent))
    y = recent["AQI"].values

    slope, intercept = np.polyfit(x, y, 1)

    future_x = np.arange(
        len(recent),
        len(recent) + 24
    )

    prediction = intercept + slope * future_x
    prediction = np.maximum(prediction, 0)

    future_time = pd.date_range(
        recent["Time"].iloc[-1],
        periods=25,
        freq="h"
    )[1:]

    future_df = pd.DataFrame({
        "Time": future_time,
        "AQI": prediction,
        "Type": "Prediction"
    })

    recent_df = recent.copy()
    recent_df["Type"] = "Historical"

    final_df = pd.concat(
        [recent_df, future_df],
        ignore_index=True
    )

    fig = px.line(
        final_df,
        x="Time",
        y="AQI",
        color="Type",
        markers=True,
        title=t["aqi"]
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "هذه توقعات رياضية بسيطة اعتمادًا على الاتجاه الأخير، "
        "وليست توقعًا رسميًا لجودة الهواء."
    )
```

elif page == t["about"]:

```
st.header("🌍 " + t["about"])

st.markdown(
    f"""
    <div class="card">

    <h2>EcoSmart Gabès</h2>

    <p>
    مشروع يهدف إلى استعمال البيانات والذكاء الاصطناعي
    لمراقبة البيئة وجودة الهواء في قابس.
    </p>

    <h3>📡 البيانات</h3>

    <p>
    Weather + Air Quality + AQI + Pollutants
    </p>

    <h3>🤖 المستقبل</h3>

    <ul>
    <li>IoT Sensors</li>
    <li>Machine Learning</li>
    <li>Satellite Data</li>
    <li>Pollution Alerts</li>
    <li>AI Environmental Assistant</li>
    </ul>

    <p>
    ⚠️ {t["note"]}
    </p>

    </div>
    """,
    unsafe_allow_html=True
)
```

st.markdown(
f""" <div class="footer">
🌍 <b>EcoSmart Gabès</b><br>
{t["source"]} </div>
""",
unsafe_allow_html=True
)
