python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from datetime import datetime
import folium
from streamlit_folium import st_folium

# ============================================================
# ECO SMART GABES
# ============================================================

st.set_page_config(
    page_title="EcoSmart Gabès",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOCATION
# ============================================================

LATITUDE = 33.8815
LONGITUDE = 10.0982

# ============================================================
# TRANSLATIONS
# ============================================================

translations = {
    "العربية": {
        "home": "الرئيسية",
        "air": "جودة الهواء",
        "analytics": "التحليلات",
        "map": "الخريطة",
        "prediction": "التوقعات",
        "about": "حول المشروع",
        "title": "EcoSmart قابس",
        "subtitle": "منصة ذكية لمراقبة البيئة وجودة الهواء في قابس",
        "aqi": "مؤشر جودة الهواء",
        "pm25": "الجسيمات PM2.5",
        "pm10": "الجسيمات PM10",
        "temperature": "درجة الحرارة",
        "humidity": "الرطوبة",
        "wind": "سرعة الرياح",
        "co2": "ثاني أكسيد الكربون",
        "no2": "ثاني أكسيد النيتروجين",
        "so2": "ثاني أكسيد الكبريت",
        "o3": "الأوزون",
        "real_data": "بيانات حقيقية",
        "last_update": "آخر تحديث",
        "trend": "التغير خلال الساعات الأخيرة",
        "select": "اختر المؤشر",
        "forecast": "توقعات مؤشر جودة الهواء",
        "source": "مصدر البيانات",
        "about_text": "EcoSmart Gabès هو مشروع يهدف إلى استعمال البيانات والذكاء الاصطناعي لمتابعة البيئة في قابس.",
        "model_note": "بيانات جودة الهواء تعتمد على نماذج CAMS وليست قياسات مباشرة من حساسات داخل قابس.",
        "industrial": "المنطقة الصناعية",
        "coast": "المنطقة الساحلية",
        "center": "وسط قابس",
        "average": "المتوسط",
        "maximum": "الأقصى",
        "minimum": "الأدنى",
    },

    "Français": {
        "home": "Accueil",
        "air": "Qualité de l'air",
        "analytics": "Analyses",
        "map": "Carte",
        "prediction": "Prévisions",
        "about": "À propos",
        "title": "EcoSmart Gabès",
        "subtitle": "Plateforme intelligente de surveillance environnementale à Gabès",
        "aqi": "Indice de qualité de l'air",
        "pm25": "Particules PM2.5",
        "pm10": "Particules PM10",
        "temperature": "Température",
        "humidity": "Humidité",
        "wind": "Vitesse du vent",
        "co2": "Dioxyde de carbone",
        "no2": "Dioxyde d'azote",
        "so2": "Dioxyde de soufre",
        "o3": "Ozone",
        "real_data": "Données réelles",
        "last_update": "Dernière mise à jour",
        "trend": "Évolution récente",
        "select": "Choisir l'indicateur",
        "forecast": "Prévision de la qualité de l'air",
        "source": "Source des données",
        "about_text": "EcoSmart Gabès est un projet utilisant les données et l'intelligence artificielle pour surveiller l'environnement à Gabès.",
        "model_note": "Les données de qualité de l'air proviennent de modèles CAMS et non de capteurs locaux directs.",
        "industrial": "Zone industrielle",
        "coast": "Zone côtière",
        "center": "Centre de Gabès",
        "average": "Moyenne",
        "maximum": "Maximum",
        "minimum": "Minimum",
    },

    "English": {
        "home": "Home",
        "air": "Air Quality",
        "analytics": "Analytics",
        "map": "Map",
        "prediction": "Prediction",
        "about": "About",
        "title": "EcoSmart Gabès",
        "subtitle": "Smart environmental monitoring platform for Gabès",
        "aqi": "Air Quality Index",
        "pm25": "PM2.5 Particles",
        "pm10": "PM10 Particles",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "wind": "Wind Speed",
        "co2": "Carbon Dioxide",
        "no2": "Nitrogen Dioxide",
        "so2": "Sulfur Dioxide",
        "o3": "Ozone",
        "real_data": "Real data",
        "last_update": "Last update",
        "trend": "Recent trend",
        "select": "Select indicator",
        "forecast": "Air quality forecast",
        "source": "Data source",
        "about_text": "EcoSmart Gabès is a project using data and artificial intelligence to monitor the environment in Gabès.",
        "model_note": "Air quality data comes from CAMS models and not from direct local sensors.",
        "industrial": "Industrial zone",
        "coast": "Coastal zone",
        "center": "Gabès center",
        "average": "Average",
        "maximum": "Maximum",
        "minimum": "Minimum",
    }
}

# ============================================================
# LANGUAGE
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "العربية"

language = st.sidebar.selectbox(
    "🌐 Language / اللغة / Langue",
    ["العربية", "Français", "English"],
    index=["العربية", "Français", "English"].index(
        st.session_state.language
    )
)

st.session_state.language = language
t = translations[language]

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Cairo', 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(0, 180, 216, 0.16),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(0, 255, 170, 0.10),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #06111f 0%,
            #0a1727 50%,
            #07121f 100%
        );
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: rgba(4, 12, 22, 0.97);
}

.hero {
    padding: 38px;
    border-radius: 28px;
    margin-bottom: 28px;

    background:
        linear-gradient(
            135deg,
            rgba(0, 200, 255, 0.13),
            rgba(0, 255, 170, 0.06)
        );

    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

.hero h1 {
    font-size: 44px;
    font-weight: 800;
    margin: 0;
}

.hero p {
    color: #aebdca;
    font-size: 17px;
    margin-top: 8px;
}

.card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.15);
}

.metric-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    min-height: 140px;
}

.metric-label {
    color: #9eafbf;
    font-size: 14px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 10px;
}

.metric-unit {
    color: #7f91a2;
    font-size: 12px;
}

.footer {
    text-align: center;
    color: #718395;
    margin-top: 40px;
    padding: 25px;
}

</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# API
# ============================================================

@st.cache_data(ttl=900)
def get_air_quality():

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,

        "current": (
            "european_aqi,"
            "pm10,"
            "pm2_5,"
            "carbon_monoxide,"
            "carbon_dioxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone"
        ),

        "hourly": (
            "european_aqi,"
            "pm10,"
            "pm2_5,"
            "carbon_monoxide,"
            "carbon_dioxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone"
        ),

        "past_days": 2,
        "forecast_days": 3,
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=900)
def get_weather():

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),

        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),

        "past_days": 2,
        "forecast_days": 3,
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# LOAD DATA
# ============================================================

try:

    air_data = get_air_quality()
    weather_data = get_weather()

except Exception as error:

    st.error("❌ Unable to load environmental data.")
    st.code(str(error))

    st.info(
        "Please refresh the page. If the problem continues, "
        "check the Streamlit Cloud logs."
    )

    st.stop()


# ============================================================
# CURRENT DATA
# ============================================================

air_current = air_data.get("current", {})
weather_current = weather_data.get("current", {})

aqi = air_current.get("european_aqi")
pm25 = air_current.get("pm2_5")
pm10 = air_current.get("pm10")
co2 = air_current.get("carbon_dioxide")
no2 = air_current.get("nitrogen_dioxide")
so2 = air_current.get("sulphur_dioxide")
o3 = air_current.get("ozone")

temperature = weather_current.get("temperature_2m")
humidity = weather_current.get("relative_humidity_2m")
wind = weather_current.get("wind_speed_10m")


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
<div class="hero">

<h1>🌍 {t["title"]}</h1>

<p>
{t["subtitle"]}
</p>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🌍 EcoSmart Gabès")

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

st.sidebar.markdown("---")

st.sidebar.info(
    f"{t['source']}: Open-Meteo / CAMS"
)


# ============================================================
# HOME
# ============================================================

if page == t["home"]:

    st.subheader("📊 " + t["home"])

    cols = st.columns(4)

    values = [
        (t["aqi"], aqi, ""),
        (t["pm25"], pm25, "µg/m³"),
        (t["temperature"], temperature, "°C"),
        (t["humidity"], humidity, "%")
    ]

    for col, (label, value, unit) in zip(cols, values):

        with col:

            if value is None:
                display_value = "N/A"
            else:
                display_value = f"{value:.1f}"

            st.markdown(
                f"""
                <div class="metric-card">

                <div class="metric-label">
                {label}
                </div>

                <div class="metric-value">
                {display_value}
                </div>

                <div class="metric-unit">
                {unit}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    cols = st.columns(4)

    values = [
        (t["pm10"], pm10, "µg/m³"),
        (t["co2"], co2, "µg/m³"),
        (t["no2"], no2, "µg/m³"),
        (t["wind"], wind, "km/h")
    ]

    for col, (label, value, unit) in zip(cols, values):

        with col:

            if value is None:
                display_value = "N/A"
            else:
                display_value = f"{value:.1f}"

            st.markdown(
                f"""
                <div class="metric-card">

                <div class="metric-label">
                {label}
                </div>

                <div class="metric-value">
                {display_value}
                </div>

                <div class="metric-unit">
                {unit}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # AQI chart

    hourly = air_data.get("hourly", {})

    if "time" in hourly and "european_aqi" in hourly:

        df = pd.DataFrame({
            "time": pd.to_datetime(hourly["time"]),
            "AQI": hourly["european_aqi"]
        })

        df = df.dropna()

        st.markdown(
            f"""
            <div class="card">
            <h3>📈 {t["trend"]}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        fig = px.line(
            df,
            x="time",
            y="AQI",
            markers=True,
            title=t["aqi"]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# AIR QUALITY
# ============================================================

elif page == t["air"]:

    st.subheader("🌫️ " + t["air"])

    cols = st.columns(4)

    air_values = [
        (t["aqi"], aqi, ""),
        (t["pm25"], pm25, "µg/m³"),
        (t["pm10"], pm10, "µg/m³"),
        (t["no2"], no2, "µg/m³")
    ]

    for col, (label, value, unit) in zip(cols, air_values):

        with col:

            value_text = (
                "N/A"
                if value is None
                else f"{value:.2f}"
            )

            st.metric(
                label,
                value_text,
                unit
            )

    st.write("")

    cols = st.columns(4)

    air_values = [
        (t["co2"], co2, "µg/m³"),
        (t["so2"], so2, "µg/m³"),
        (t["o3"], o3, "µg/m³"),
        (t["wind"], wind, "km/h")
    ]

    for col, (label, value, unit) in zip(cols, air_values):

        with col:

            value_text = (
                "N/A"
                if value is None
                else f"{value:.2f}"
            )

            st.metric(
                label,
                value_text,
                unit
            )

    st.write("")

    hourly = air_data.get("hourly", {})

    if "time" in hourly:

        df_air = pd.DataFrame({
            "time": pd.to_datetime(hourly["time"]),
            "PM2.5": hourly.get("pm2_5"),
            "PM10": hourly.get("pm10"),
            "NO2": hourly.get("nitrogen_dioxide"),
            "SO2": hourly.get("sulphur_dioxide"),
            "O3": hourly.get("ozone")
        })

        st.markdown(
            '<div class="card"><h3>📊 Pollutant evolution</h3></div>',
            unsafe_allow_html=True
        )

        selected = st.selectbox(
            t["select"],
            ["PM2.5", "PM10", "NO2", "SO2", "O3"]
        )

        df_plot = df_air[["time", selected]].dropna()

        fig = px.line(
            df_plot,
            x="time",
            y=selected,
            markers=True,
            title=selected
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# ANALYTICS
# ============================================================

elif page == t["analytics"]:

    st.subheader("📊 " + t["analytics"])

    hourly = air_data.get("hourly", {})

    df = pd.DataFrame({
        "time": pd.to_datetime(hourly.get("time", [])),
        "AQI": hourly.get("european_aqi", []),
        "PM2.5": hourly.get("pm2_5", []),
        "PM10": hourly.get("pm10", []),
        "CO2": hourly.get("carbon_dioxide", []),
        "NO2": hourly.get("nitrogen_dioxide", []),
        "SO2": hourly.get("sulphur_dioxide", []),
        "O3": hourly.get("ozone", [])
    })

    variable = st.selectbox(
        t["select"],
        ["AQI", "PM2.5", "PM10", "CO2", "NO2", "SO2", "O3"]
    )

    clean = df[["time", variable]].dropna()

    if len(clean) > 0:

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                t["average"],
                f"{clean[variable].mean():.2f}"
            )

        with c2:
            st.metric(
                t["maximum"],
                f"{clean[variable].max():.2f}"
            )

        with c3:
            st.metric(
                t["minimum"],
                f"{clean[variable].min():.2f}"
            )

        fig = px.area(
            clean,
            x="time",
            y=variable,
            title=variable
        )

        fig.update_layout(
            template="plotly_dark",
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

    st.subheader("🗺️ " + t["map"])

    gabes_map = folium.Map(
        location=[LATITUDE, LONGITUDE],
        zoom_start=12,
        tiles="CartoDB dark_matter"
    )

    folium.Marker(
        [LATITUDE, LONGITUDE],
        tooltip=t["center"],
        popup=f"""
        <b>EcoSmart Gabès</b><br>
        {t["aqi"]}: {aqi if aqi is not None else "N/A"}<br>
        PM2.5: {pm25 if pm25 is not None else "N/A"}
        """,
        icon=folium.Icon(
            color="green",
            icon="globe"
        )
    ).add_to(gabes_map)

    # Industrial area
    folium.CircleMarker(
        [33.894, 10.103],
        radius=12,
        tooltip=t["industrial"],
        popup=t["industrial"],
        color="#ff6b35",
        fill=True,
        fill_opacity=0.6
    ).add_to(gabes_map)

    # Coastal area
    folium.CircleMarker(
        [33.870, 10.120],
        radius=10,
        tooltip=t["coast"],
        popup=t["coast"],
        color="#00b4d8",
        fill=True,
        fill_opacity=0.6
    ).add_to(gabes_map)

    st_folium(
        gabes_map,
        width=None,
        height=600
    )


# ============================================================
# PREDICTION
# ============================================================

elif page == t["prediction"]:

    st.subheader("🤖 " + t["prediction"])

    hourly = air_data.get("hourly", {})

    if (
        "time" in hourly
        and "european_aqi" in hourly
    ):

        df = pd.DataFrame({
            "time": pd.to_datetime(hourly["time"]),
            "AQI": hourly["european_aqi"]
        }).dropna()

        recent = df.tail(48).copy()

        if len(recent) >= 10:

            x = np.arange(len(recent))
            y = recent["AQI"].values

            slope, intercept = np.polyfit(
                x,
                y,
                1
            )

            future_x = np.arange(
                len(recent),
                len(recent) + 24
            )

            predicted = (
                intercept +
                slope * future_x
            )

            predicted = np.maximum(
                predicted,
                0
            )

            future_times = pd.date_range(
                start=recent["time"].iloc[-1],
                periods=25,
                freq="h"
            )[1:]

            prediction_df = pd.DataFrame({
                "time": future_times,
                "AQI": predicted
            })

            combined = pd.concat(
                [
                    recent,
                    prediction_df
                ],
                ignore_index=True
            )

            combined["Type"] = (
                ["Historical"] * len(recent)
                + ["Prediction"] * len(prediction_df)
            )

            fig = px.line(
                combined,
                x="time",
                y="AQI",
                color="Type",
                markers=True,
                title=t["forecast"]
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.info(
                "ℹ️ This is a simple mathematical trend estimate, "
                "not an official air-quality forecast."
            )

        else:

            st.warning(
                "Not enough data for prediction."
            )


# ============================================================
# ABOUT
# ============================================================

elif page == t["about"]:

    st.subheader("🌍 " + t["about"])

    st.markdown(
        f"""
        <div class="card">

        <h2>EcoSmart Gabès</h2>

        <p>
        {t["about_text"]}
        </p>

        <hr>

        <h3>📡 {t["real_data"]}</h3>

        <p>
        Weather and air-quality information is retrieved
        automatically from Open-Meteo.
        </p>

        <h3>⚠️ Important</h3>

        <p>
        {t["model_note"]}
        </p>

        <h3>🤖 Future development</h3>

        <ul>
            <li>IoT environmental sensors</li>
            <li>Machine learning models</li>
            <li>Satellite data</li>
            <li>Historical environmental database</li>
            <li>Automatic pollution alerts</li>
            <li>AI environmental assistant</li>
        </ul>

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

    Environmental Intelligence • Gabès, Tunisia<br>

    {t["source"]}: Open-Meteo / CAMS

    </div>
    """,
    unsafe_allow_html=True
)
```
