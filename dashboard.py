```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium

from streamlit_folium import st_folium
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlencode
import json


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EcoSmart Gabès",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GABÈS LOCATION
# ============================================================

LATITUDE = 33.8815
LONGITUDE = 10.0982
LOCATION_NAME = "Gabès, Tunisia"


# ============================================================
# SESSION STATE
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "العربية"


# ============================================================
# TRANSLATIONS
# ============================================================

TEXT = {

    "العربية": {

        "app": "EcoSmart Gabès",
        "subtitle": "منصة ذكية للمراقبة والتحليل البيئي",
        "location": "قابس، تونس",

        "translate": "🌐 تغيير اللغة",
        "language": "اللغة",

        "overview": "🏠 الرئيسية",
        "map": "🗺️ الخريطة",
        "analytics": "📊 التحليلات",
        "prediction": "🤖 التنبؤ",
        "about": "ℹ️ حول المشروع",

        "environment": "الوضع البيئي الحالي",

        "aqi": "مؤشر جودة الهواء",
        "pm25": "PM2.5",
        "pm10": "PM10",
        "co2": "CO₂",
        "temperature": "درجة الحرارة",
        "humidity": "الرطوبة",
        "wind": "سرعة الرياح",
        "no2": "NO₂",
        "so2": "SO₂",
        "o3": "O₃",

        "trends": "الاتجاهات البيئية",
        "air_quality": "جودة الهواء",
        "weather": "الطقس",

        "map_title": "الخريطة البيئية لقابس",
        "map_description": "موقع قابس ومناطق المراقبة البيئية.",

        "industrial": "المنطقة الصناعية",
        "coastal": "المنطقة الساحلية",
        "center": "مركز EcoSmart",

        "analytics_title": "تحليل البيانات الحقيقية",
        "choose": "اختر المؤشر",
        "last_hours": "الساعات الأخيرة",
        "average": "المتوسط",
        "maximum": "الأقصى",
        "minimum": "الأدنى",

        "prediction_title": "التنبؤ البيئي",
        "prediction_description":
            "توقع اتجاه مؤشر جودة الهواء اعتمادًا على البيانات المتوفرة.",
        "prediction_days": "عدد أيام التنبؤ",
        "historical": "البيانات الحالية",
        "forecast": "التوقع",

        "about_title": "حول EcoSmart Gabès",

        "about_text":
            "EcoSmart Gabès هو مشروع يهدف إلى استعمال البيانات البيئية "
            "والذكاء الاصطناعي لمراقبة البيئة في قابس.",

        "sources": "مصدر البيانات",
        "source_text":
            "بيانات الطقس وجودة الهواء يتم جلبها من Open-Meteo. "
            "بيانات جودة الهواء تعتمد على نماذج CAMS وليست قياسات مباشرة "
            "من حساس موجود داخل قابس.",

        "objectives": "أهداف المشروع",

        "objective1": "🌫️ مراقبة جودة الهواء",
        "objective2": "🌡️ مراقبة الطقس",
        "objective3": "📊 تحليل البيانات",
        "objective4": "🗺️ عرض البيانات على الخريطة",
        "objective5": "🤖 التنبؤ بالاتجاهات",
        "objective6": "🌱 دعم الوعي البيئي",

        "future": "التطوير المستقبلي",

        "future_text":
            "يمكن مستقبلاً ربط المشروع بحساسات IoT حقيقية، "
            "وإضافة بيانات الأقمار الصناعية، ونماذج ذكاء اصطناعي "
            "أكثر تطورًا.",

        "loading": "جاري تحميل البيانات...",
        "error": "تعذر الاتصال بمصدر البيانات.",
        "retry": "حاول تحديث الصفحة.",

        "good": "جيد",
        "fair": "مقبول",
        "moderate": "متوسط",
        "poor": "ضعيف",
        "very_poor": "ضعيف جدًا",
        "extreme": "خطير جدًا",

        "footer": "EcoSmart Gabès • Environmental Intelligence"
    },


    "Français": {

        "app": "EcoSmart Gabès",
        "subtitle": "Plateforme intelligente de surveillance environnementale",
        "location": "Gabès, Tunisie",

        "translate": "🌐 Changer la langue",
        "language": "Langue",

        "overview": "🏠 Accueil",
        "map": "🗺️ Carte",
        "analytics": "📊 Analyses",
        "prediction": "🤖 Prédiction",
        "about": "ℹ️ À propos",

        "environment": "Situation environnementale actuelle",

        "aqi": "Indice de qualité de l'air",
        "pm25": "PM2.5",
        "pm10": "PM10",
        "co2": "CO₂",
        "temperature": "Température",
        "humidity": "Humidité",
        "wind": "Vent",
        "no2": "NO₂",
        "so2": "SO₂",
        "o3": "O₃",

        "trends": "Tendances environnementales",
        "air_quality": "Qualité de l'air",
        "weather": "Météo",

        "map_title": "Carte environnementale de Gabès",
        "map_description":
            "Localisation de Gabès et zones de surveillance.",

        "industrial": "Zone industrielle",
        "coastal": "Zone côtière",
        "center": "Centre EcoSmart",

        "analytics_title": "Analyse des données réelles",
        "choose": "Choisir un indicateur",
        "last_hours": "Dernières heures",
        "average": "Moyenne",
        "maximum": "Maximum",
        "minimum": "Minimum",

        "prediction_title": "Prédiction environnementale",
        "prediction_description":
            "Prévision de la tendance de la qualité de l'air "
            "à partir des données disponibles.",

        "prediction_days": "Nombre de jours",
        "historical": "Données actuelles",
        "forecast": "Prévision",

        "about_title": "À propos d'EcoSmart Gabès",

        "about_text":
            "EcoSmart Gabès est un projet qui utilise les données "
            "environnementales et l'intelligence artificielle "
            "pour surveiller l'environnement à Gabès.",

        "sources": "Source des données",

        "source_text":
            "Les données météo et qualité de l'air proviennent "
            "d'Open-Meteo. Les données de qualité de l'air utilisent "
            "des modèles CAMS et ne sont pas des mesures directes "
            "effectuées par un capteur local à Gabès.",

        "objectives": "Objectifs",

        "objective1": "🌫️ Surveiller la qualité de l'air",
        "objective2": "🌡️ Surveiller la météo",
        "objective3": "📊 Analyser les données",
        "objective4": "🗺️ Cartographier les données",
        "objective5": "🤖 Prévoir les tendances",
        "objective6": "🌱 Sensibiliser à l'environnement",

        "future": "Développement futur",

        "future_text":
            "Le projet pourra être connecté à de vrais capteurs IoT, "
            "aux données satellites et à des modèles d'intelligence "
            "artificielle plus avancés.",

        "loading": "Chargement des données...",
        "error": "Impossible de récupérer les données.",
        "retry": "Essayez de rafraîchir la page.",

        "good": "Bon",
        "fair": "Acceptable",
        "moderate": "Modéré",
        "poor": "Mauvais",
        "very_poor": "Très mauvais",
        "extreme": "Extrêmement mauvais",

        "footer": "EcoSmart Gabès • Environmental Intelligence"
    },


    "English": {

        "app": "EcoSmart Gabès",
        "subtitle": "Smart Environmental Monitoring & Intelligence",
        "location": "Gabès, Tunisia",

        "translate": "🌐 Change language",
        "language": "Language",

        "overview": "🏠 Overview",
        "map": "🗺️ Map",
        "analytics": "📊 Analytics",
        "prediction": "🤖 Prediction",
        "about": "ℹ️ About",

        "environment": "Current Environmental Situation",

        "aqi": "Air Quality Index",
        "pm25": "PM2.5",
        "pm10": "PM10",
        "co2": "CO₂",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "wind": "Wind Speed",
        "no2": "NO₂",
        "so2": "SO₂",
        "o3": "O₃",

        "trends": "Environmental Trends",
        "air_quality": "Air Quality",
        "weather": "Weather",

        "map_title": "Gabès Environmental Map",
        "map_description":
            "Gabès location and environmental monitoring zones.",

        "industrial": "Industrial Zone",
        "coastal": "Coastal Zone",
        "center": "EcoSmart Center",

        "analytics_title": "Real Data Analytics",
        "choose": "Choose an indicator",
        "last_hours": "Recent Hours",
        "average": "Average",
        "maximum": "Maximum",
        "minimum": "Minimum",

        "prediction_title": "Environmental Prediction",
        "prediction_description":
            "Estimate air-quality trends using the available data.",

        "prediction_days": "Prediction Days",
        "historical": "Current Data",
        "forecast": "Forecast",

        "about_title": "About EcoSmart Gabès",

        "about_text":
            "EcoSmart Gabès is a project using environmental data "
            "and artificial intelligence to monitor the environment "
            "in Gabès.",

        "sources": "Data Source",

        "source_text":
            "Weather and air-quality data are retrieved from "
            "Open-Meteo. Air-quality data uses CAMS models and "
            "does not represent direct measurements from a local "
            "sensor in Gabès.",

        "objectives": "Project Objectives",

        "objective1": "🌫️ Monitor air quality",
        "objective2": "🌡️ Monitor weather",
        "objective3": "📊 Analyze data",
        "objective4": "🗺️ Map environmental data",
        "objective5": "🤖 Predict trends",
        "objective6": "🌱 Promote environmental awareness",

        "future": "Future Development",

        "future_text":
            "The project can later connect to real IoT sensors, "
            "satellite data and more advanced AI models.",

        "loading": "Loading data...",
        "error": "Unable to retrieve data.",
        "retry": "Try refreshing the page.",

        "good": "Good",
        "fair": "Fair",
        "moderate": "Moderate",
        "poor": "Poor",
        "very_poor": "Very poor",
        "extreme": "Extremely poor",

        "footer": "EcoSmart Gabès • Environmental Intelligence"
    }
}

t = TEXT[st.session_state.language]

rtl = st.session_state.language == "العربية"


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800'
        '&family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {{
        font-family:
            {"Cairo, sans-serif" if rtl else "Inter, sans-serif"};
    }}

    .stApp {{
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(16,185,129,0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(37,99,235,0.18),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #020617,
                #071827,
                #06121e
            );
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] {{
        background: rgba(2,6,23,0.96);
        border-right: 1px solid rgba(255,255,255,0.08);
    }}

    [data-testid="stSidebar"] * {{
        color: #e2e8f0 !important;
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    .hero {{
        padding: 38px;
        border-radius: 28px;
        margin-bottom: 25px;

        background:
            linear-gradient(
                135deg,
                rgba(16,185,129,0.25),
                rgba(37,99,235,0.22)
            );

        border: 1px solid rgba(255,255,255,0.12);

        box-shadow:
            0 20px 70px rgba(0,0,0,0.35);

        backdrop-filter: blur(20px);
    }}

    .hero h1 {{
        color: white;
        font-size: 46px;
        font-weight: 800;
        margin: 0;
    }}

    .hero p {{
        color: #cbd5e1;
        font-size: 17px;
        margin: 7px 0;
    }}

    .section-title {{
        color: white;
        font-size: 27px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 18px;
    }}

    .metric-card {{
        min-height: 150px;
        padding: 22px;
        border-radius: 22px;

        background: rgba(15,23,42,0.72);

        border:
            1px solid rgba(255,255,255,0.09);

        box-shadow:
            0 12px 40px rgba(0,0,0,0.22);

        backdrop-filter: blur(18px);
    }}

    .metric-icon {{
        font-size: 28px;
    }}

    .metric-title {{
        color: #94a3b8;
        font-size: 14px;
        margin-top: 8px;
    }}

    .metric-value {{
        color: white;
        font-size: 29px;
        font-weight: 800;
        margin-top: 4px;
    }}

    .live {{
        color: #5eead4;
        font-size: 12px;
        margin-top: 5px;
    }}

    .info-card {{
        padding: 25px;
        border-radius: 22px;

        background: rgba(15,23,42,0.70);

        border:
            1px solid rgba(255,255,255,0.08);

        color: #cbd5e1;

        line-height: 1.8;

        margin-bottom: 14px;
    }}

    .source {{
        padding: 18px;
        border-radius: 18px;

        background: rgba(14,116,144,0.12);

        border:
            1px solid rgba(34,211,238,0.15);

        color: #cbd5e1;
    }}

    .footer {{
        text-align: center;
        color: #64748b;
        padding: 35px 10px 10px;
        font-size: 13px;
    }}

    .stButton > button {{
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(15,23,42,0.8);
        color: white;
        font-weight: 700;
        min-height: 45px;
    }}

    .stButton > button:hover {{
        border-color: #2dd4bf;
        color: #5eead4;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LANGUAGE BUTTON
# ============================================================

language_order = [
    "العربية",
    "Français",
    "English"
]

if st.button(
    t["translate"],
    use_container_width=False
):

    current_index = language_order.index(
        st.session_state.language
    )

    next_index = (
        current_index + 1
    ) % len(language_order)

    st.session_state.language = language_order[next_index]

    st.rerun()


# ============================================================
# FETCH API
# ============================================================

@st.cache_data(ttl=900)
def get_air_quality():

    params = {

        "latitude": LATITUDE,
        "longitude": LONGITUDE,

        "current":
            "european_aqi,"
            "pm10,"
            "pm2_5,"
            "carbon_monoxide,"
            "carbon_dioxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone",

        "hourly":
            "european_aqi,"
            "pm10,"
            "pm2_5,"
            "carbon_monoxide,"
            "carbon_dioxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone",

        "past_days": 2,
        "forecast_days": 3,

        "timezone": "auto"
    }

    url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality?"
        + urlencode(params)
    )

    with urlopen(url, timeout=15) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


@st.cache_data(ttl=900)
def get_weather():

    params = {

        "latitude": LATITUDE,
        "longitude": LONGITUDE,

        "current":
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code",

        "hourly":
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m",

        "past_days": 2,
        "forecast_days": 3,

        "timezone": "auto"
    }

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        + urlencode(params)
    )

    with urlopen(url, timeout=15) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


# ============================================================
# LOAD DATA
# ============================================================

try:

    air = get_air_quality()
    weather = get_weather()

    api_error = False

except Exception as e:

    air = None
    weather = None
    api_error = True


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="text-align:center;padding:10px;">
        <div style="font-size:48px;">🌍</div>
        <h2>EcoSmart</h2>
        <p style="color:#64748b;">Gabès</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.write(
    f"**{t['language']}**"
)

st.sidebar.write(
    f"🌐 {st.session_state.language}"
)

st.sidebar.markdown("---")

pages = [
    t["overview"],
    t["map"],
    t["analytics"],
    t["prediction"],
    t["about"]
]

page = st.sidebar.radio(
    t["language"],
    pages,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "📡 Open-Meteo • CAMS • Gabès"
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero"
         dir="{'rtl' if rtl else 'ltr'}">

        <h1>🌍 {t["app"]}</h1>

        <p>{t["subtitle"]}</p>

        <p>📍 {t["location"]}</p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API ERROR
# ============================================================

if api_error:

    st.error(
        f"⚠️ {t['error']} {t['retry']}"
    )

    st.stop()


# ============================================================
# CURRENT VALUES
# ============================================================

air_current = air.get("current", {})
weather_current = weather.get("current", {})

aqi = air_current.get("european_aqi")
pm25 = air_current.get("pm2_5")
pm10 = air_current.get("pm10")
co2 = air_current.get("carbon_dioxide")
no2 = air_current.get("nitrogen_dioxide")
so2 = air_current.get("sulphur_dioxide")
o3 = air_current.get("ozone")

temperature = weather_current.get(
    "temperature_2m"
)

humidity = weather_current.get(
    "relative_humidity_2m"
)

wind = weather_current.get(
    "wind_speed_10m"
)


# ============================================================
# OVERVIEW
# ============================================================

if page == t["overview"]:

    st.markdown(
        f"""
        <div class="section-title">
            {t["environment"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    cols = st.columns(4)

    metrics = [

        (
            "🌍",
            t["aqi"],
            aqi,
            ""
        ),

        (
            "🌫️",
            t["pm25"],
            pm25,
            " μg/m³"
        ),

        (
            "🌡️",
            t["temperature"],
            temperature,
            " °C"
        ),

        (
            "💧",
            t["humidity"],
            humidity,
            "%"
        )
    ]

    for col, item in zip(cols, metrics):

        icon, title, value, unit = item

        with col:

            value_text = (
                "—"
                if value is None
                else f"{value:.1f}{unit}"
            )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        {icon}
                    </div>

                    <div class="metric-title">
                        {title}
                    </div>

                    <div class="metric-value">
                        {value_text}
                    </div>

                    <div class="live">
                        ● Live data
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    # Second row

    st.markdown(
        '<div style="height:15px;"></div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4)

    metrics2 = [

        (
            "🌫️",
            t["pm10"],
            pm10,
            " μg/m³"
        ),

        (
            "🫧",
            t["co2"],
            co2,
            " ppm"
        ),

        (
            "💨",
            t["wind"],
            wind,
            " km/h"
        ),

        (
            "🧪",
            t["no2"],
            no2,
            " μg/m³"
        )
    ]

    for col, item in zip(cols, metrics2):

        icon, title, value, unit = item

        with col:

            value_text = (
                "—"
                if value is None
                else f"{value:.1f}{unit}"
            )

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        {icon}
                    </div>

                    <div class="metric-title">
                        {title}
                    </div>

                    <div class="metric-value">
                        {value_text}
                    </div>

                    <div class="live">
                        ● Live data
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    # ========================================================
    # CHARTS
    # ========================================================

    st.markdown(
        f"""
        <div class="section-title">
            📈 {t["trends"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    hourly_air = air.get("hourly", {})

    air_df = pd.DataFrame(hourly_air)

    if not air_df.empty:

        air_df["time"] = pd.to_datetime(
            air_df["time"]
        )

        fig = go.Figure()

        if "european_aqi" in air_df:

            fig.add_trace(
                go.Scatter(
                    x=air_df["time"],
                    y=air_df["european_aqi"],
                    mode="lines",
                    name="European AQI",
                    line=dict(width=3)
                )
            )

        fig.update_layout(
            title=t["air_quality"],
            template="plotly_dark",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Weather chart

    hourly_weather = weather.get(
        "hourly",
        {}
    )

    weather_df = pd.DataFrame(
        hourly_weather
    )

    if not weather_df.empty:

        weather_df["time"] = pd.to_datetime(
            weather_df["time"]
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=weather_df["time"],
                y=weather_df["temperature_2m"],
                mode="lines",
                name=t["temperature"],
                line=dict(width=3)
            )
        )

        fig.update_layout(
            title=t["weather"],
            template="plotly_dark",
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# MAP
# ============================================================

elif page == t["map"]:

    st.markdown(
        f"""
        <div class="section-title">
            🗺️ {t["map_title"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        t["map_description"]
    )

    m = folium.Map(
        location=[
            LATITUDE,
            LONGITUDE
        ],
        zoom_start=12,
        tiles="CartoDB dark_matter"
    )

    # Main center

    folium.Marker(

        [
            LATITUDE,
            LONGITUDE
        ],

        tooltip=t["center"],

        popup=f"""
        <b>🌍 EcoSmart Gabès</b><br>
        {t["location"]}
        """,

        icon=folium.Icon(
            color="blue",
            icon="info-sign"
        )

    ).add_to(m)

    # Industrial zone

    industrial_lat = 33.894
    industrial_lon = 10.103

    folium.Circle(

        [
            industrial_lat,
            industrial_lon
        ],

        radius=2500,

        color="#ef4444",

        fill=True,

        fill_color="#ef4444",

        fill_opacity=0.20,

        popup=t["industrial"]

    ).add_to(m)

    folium.Marker(

        [
            industrial_lat,
            industrial_lon
        ],

        tooltip=t["industrial"],

        popup=t["industrial"],

        icon=folium.Icon(
            color="red",
            icon="warning-sign"
        )

    ).add_to(m)

    # Coastal zone

    coastal_lat = 33.870
    coastal_lon = 10.120

    folium.Circle(

        [
            coastal_lat,
            coastal_lon
        ],

        radius=1600,

        color="#22c55e",

        fill=True,

        fill_color="#22c55e",

        fill_opacity=0.18,

        popup=t["coastal"]

    ).add_to(m)

    folium.Marker(

        [
            coastal_lat,
            coastal_lon
        ],

        tooltip=t["coastal"],

        popup=t["coastal"],

        icon=folium.Icon(
            color="green",
            icon="leaf"
        )

    ).add_to(m)

    st_folium(
        m,
        width=None,
        height=600
    )


# ============================================================
# ANALYTICS
# ============================================================

elif page == t["analytics"]:

    st.markdown(
        f"""
        <div class="section-title">
            📊 {t["analytics_title"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    hourly_air = air.get(
        "hourly",
        {}
    )

    df = pd.DataFrame(
        hourly_air
    )

    if not df.empty:

        df["time"] = pd.to_datetime(
            df["time"]
        )

        indicators = {

            t["aqi"]: "european_aqi",

            t["pm25"]: "pm2_5",

            t["pm10"]: "pm10",

            t["co2"]: "carbon_dioxide",

            t["no2"]: "nitrogen_dioxide",

            t["so2"]: "sulphur_dioxide",

            t["o3"]: "ozone"
        }

        available = {
            name: column
            for name, column in indicators.items()
            if column in df.columns
        }

        selected = st.selectbox(
            t["choose"],
            list(available.keys())
        )

        column = available[selected]

        chart_df = df[
            [
                "time",
                column
            ]
        ].dropna()

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=chart_df["time"],
                y=chart_df[column],
                mode="lines+markers",
                name=selected,
                line=dict(width=3)
            )
        )

        fig.update_layout(
            title=selected,
            template="plotly_dark",
            height=450,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                t["average"],
                f"{chart_df[column].mean():.2f}"
            )

        with c2:

            st.metric(
                t["maximum"],
                f"{chart_df[column].max():.2f}"
            )

        with c3:

            st.metric(
                t["minimum"],
                f"{chart_df[column].min():.2f}"
            )

        st.dataframe(
            chart_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# AI PREDICTION
# ============================================================

elif page == t["prediction"]:

    st.markdown(
        f"""
        <div class="section-title">
            🤖 {t["prediction_title"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        t["prediction_description"]
    )

    hourly_air = air.get(
        "hourly",
        {}
    )

    df = pd.DataFrame(
        hourly_air
    )

    if "european_aqi" not in df.columns:

        st.warning(
            "AQI prediction data unavailable."
        )

        st.stop()

    df["time"] = pd.to_datetime(
        df["time"]
    )

    df = df[
        [
            "time",
            "european_aqi"
        ]
    ].dropna()

    days = st.slider(
        t["prediction_days"],
        min_value=1,
        max_value=3,
        value=2
    )

    # Use recent data

    recent = df.tail(48).copy()

    if len(recent) < 5:

        st.warning(
            "Not enough data."
        )

        st.stop()

    x = np.arange(
        len(recent)
    )

    y = recent[
        "european_aqi"
    ].values

    # Linear trend

    coefficients = np.polyfit(
        x,
        y,
        1
    )

    model = np.poly1d(
        coefficients
    )

    future_hours = days * 24

    future_x = np.arange(
        len(recent),
        len(recent) + future_hours
    )

    prediction = model(
        future_x
    )

    prediction = np.clip(
        prediction,
        0,
        None
    )

    future_dates = pd.date_range(

        start=
        recent["time"].iloc[-1]
        + pd.Timedelta(hours=1),

        periods=future_hours,

        freq="h"
    )

    prediction_df = pd.DataFrame({

        "time": future_dates,

        "predicted_aqi":
            prediction
    })

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=recent["time"],
            y=recent["european_aqi"],
            mode="lines",
            name=t["historical"],
            line=dict(width=3)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=prediction_df["time"],
            y=prediction_df["predicted_aqi"],
            mode="lines",
            name=t["forecast"],
            line=dict(
                width=3,
                dash="dash"
            )
        )
    )

    fig.update_layout(
        title=t["prediction_title"],
        template="plotly_dark",
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    average_prediction = (
        prediction_df[
            "predicted_aqi"
        ].mean()
    )

    if average_prediction <= 20:

        st.success(
            f"🟢 {t['good']} — "
            f"{average_prediction:.1f}"
        )

    elif average_prediction <= 40:

        st.info(
            f"🟢 {t['fair']} — "
            f"{average_prediction:.1f}"
        )

    elif average_prediction <= 60:

        st.warning(
            f"🟡 {t['moderate']} — "
            f"{average_prediction:.1f}"
        )

    elif average_prediction <= 80:

        st.warning(
            f"🟠 {t['poor']} — "
            f"{average_prediction:.1f}"
        )

    elif average_prediction <= 100:

        st.error(
            f"🔴 {t['very_poor']} — "
            f"{average_prediction:.1f}"
        )

    else:

        st.error(
            f"🚨 {t['extreme']} — "
            f"{average_prediction:.1f}"
        )

    st.dataframe(
        prediction_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ABOUT
# ============================================================

elif page == t["about"]:

    st.markdown(
        f"""
        <div class="section-title">
            🌍 {t["about_title"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="info-card">
            {t["about_text"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="section-title">
            🎯 {t["objectives"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    objectives = [

        t["objective1"],
        t["objective2"],
        t["objective3"],
        t["objective4"],
        t["objective5"],
        t["objective6"]
    ]

    cols = st.columns(2)

    for i, objective in enumerate(
        objectives
    ):

        with cols[i % 2]:

            st.markdown(
                f"""
                <div class="info-card">
                    {objective}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        f"""
        <div class="section-title">
            🚀 {t["future"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="info-card">
            {t["future_text"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="section-title">
            📡 {t["sources"]}
        </div>

        <div class="source">
            {t["source_text"]}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer">

        🌍 <b>EcoSmart Gabès</b><br>

        {t["footer"]}<br><br>

        Python • Streamlit • Plotly • Folium • Open-Meteo

    </div>
    """,
    unsafe_allow_html=True
)
```
