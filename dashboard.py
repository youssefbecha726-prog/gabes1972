import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="EcoSmart Gabès",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 25px;
        border-radius: 20px;
        background: linear-gradient(135deg, #0f766e, #2563eb);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
        opacity: 0.9;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.07);
        text-align: center;
    }

    .metric-title {
        color: #64748b;
        font-size: 15px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: bold;
        color: #0f172a;
    }

    .section-title {
        font-size: 25px;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #0f172a;
    }

    .footer {
        text-align: center;
        padding: 25px;
        color: #64748b;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌍 EcoSmart Gabès")

st.sidebar.markdown("---")

language = st.sidebar.selectbox(
    "Language / اللغة",
    ["English", "العربية", "Français"]
)

st.sidebar.markdown("---")

st.sidebar.subheader("Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🗺️ Pollution Map",
        "📊 Analytics",
        "🤖 AI Prediction",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "EcoSmart Gabès is an environmental monitoring concept "
    "for analyzing pollution and climate indicators in Gabès."
)

# =========================================================
# DATA
# =========================================================

np.random.seed(42)

dates = pd.date_range(
    end=datetime.now(),
    periods=30,
    freq="D"
)

pollution = np.random.randint(35, 85, 30)
co2 = np.random.randint(390, 520, 30)
temperature = np.random.uniform(17, 31, 30)
humidity = np.random.randint(45, 85, 30)

df = pd.DataFrame({
    "Date": dates,
    "Pollution": pollution,
    "CO2": co2,
    "Temperature": temperature,
    "Humidity": humidity
})

# Current values

current_pollution = int(df["Pollution"].iloc[-1])
current_co2 = int(df["CO2"].iloc[-1])
current_temperature = round(df["Temperature"].iloc[-1], 1)
current_humidity = int(df["Humidity"].iloc[-1])

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <h1>🌍 EcoSmart Gabès</h1>
    <p>Smart Environmental Monitoring & AI Dashboard</p>
    <p>Gabès, Tunisia • Environmental Intelligence</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# OVERVIEW
# =========================================================

if page == "🏠 Overview":

    st.markdown(
        '<div class="section-title">🌱 Environmental Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Pollution Index</div>
            <div class="metric-value">{current_pollution}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">CO₂</div>
            <div class="metric-value">{current_co2} ppm</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Temperature</div>
            <div class="metric-value">{current_temperature} °C</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Humidity</div>
            <div class="metric-value">{current_humidity}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📈 Environmental Trends</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Pollution"],
            mode="lines+markers",
            name="Pollution"
        )
    )

    fig.update_layout(
        title="Pollution Index — Last 30 Days",
        xaxis_title="Date",
        yaxis_title="Pollution %",
        template="plotly_white",
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:

        fig_co2 = go.Figure()

        fig_co2.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["CO2"],
                mode="lines",
                name="CO₂"
            )
        )

        fig_co2.update_layout(
            title="CO₂ Concentration",
            xaxis_title="Date",
            yaxis_title="CO₂ (ppm)",
            template="plotly_white"
        )

        st.plotly_chart(
            fig_co2,
            use_container_width=True
        )

    with col2:

        fig_temp = go.Figure()

        fig_temp.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["Temperature"],
                mode="lines",
                name="Temperature"
            )
        )

        fig_temp.update_layout(
            title="Temperature",
            xaxis_title="Date",
            yaxis_title="°C",
            template="plotly_white"
        )

        st.plotly_chart(
            fig_temp,
            use_container_width=True
        )

# =========================================================
# POLLUTION MAP
# =========================================================

elif page == "🗺️ Pollution Map":

    st.markdown(
        '<div class="section-title">🗺️ Gabès Pollution Map</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Interactive visualization of environmental monitoring zones in Gabès."
    )

    # Gabès coordinates
    gabes_lat = 33.8815
    gabes_lon = 10.0982

    m = folium.Map(
        location=[gabes_lat, gabes_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # Main Gabès marker

    folium.Marker(
        [gabes_lat, gabes_lon],
        tooltip="Gabès",
        popup="EcoSmart Gabès Monitoring Center",
        icon=folium.Icon(
            color="blue",
            icon="info-sign"
        )
    ).add_to(m)

    # Industrial zone

    industrial_lat = 33.894
    industrial_lon = 10.103

    folium.Circle(
        location=[industrial_lat, industrial_lon],
        radius=2500,
        color="red",
        fill=True,
        fill_opacity=0.25,
        popup="Industrial Monitoring Zone"
    ).add_to(m)

    folium.Marker(
        [industrial_lat, industrial_lon],
        tooltip="Industrial Zone",
        popup="Pollution Monitoring Zone",
        icon=folium.Icon(
            color="red",
            icon="warning-sign"
        )
    ).add_to(m)

    # Coastal zone

    coastal_lat = 33.870
    coastal_lon = 10.120

    folium.Circle(
        location=[coastal_lat, coastal_lon],
        radius=1500,
        color="green",
        fill=True,
        fill_opacity=0.2,
        popup="Coastal Monitoring Zone"
    ).add_to(m)

    folium.Marker(
        [coastal_lat, coastal_lon],
        tooltip="Coastal Zone",
        popup="Coastal Environmental Monitoring",
        icon=folium.Icon(
            color="green",
            icon="leaf"
        )
    ).add_to(m)

    st_folium(
        m,
        width=None,
        height=550
    )

# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="section-title">📊 Environmental Analytics</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.markdown(
        '<div class="section-title">📈 Indicators Comparison</div>',
        unsafe_allow_html=True
    )

    indicator = st.selectbox(
        "Choose indicator",
        [
            "Pollution",
            "CO2",
            "Temperature",
            "Humidity"
        ]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Date"],
            y=df[indicator],
            name=indicator
        )
    )

    fig.update_layout(
        title=f"{indicator} Analysis",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        '<div class="section-title">📌 Statistics</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Average",
            round(df[indicator].mean(), 2)
        )

    with c2:
        st.metric(
            "Maximum",
            round(df[indicator].max(), 2)
        )

    with c3:
        st.metric(
            "Minimum",
            round(df[indicator].min(), 2)
        )

# =========================================================
# AI PREDICTION
# =========================================================

elif page == "🤖 AI Prediction":

    st.markdown(
        '<div class="section-title">🤖 AI Environmental Prediction</div>',
        unsafe_allow_html=True
    )

    st.write(
        "This section provides a simple demonstration of environmental "
        "trend prediction using recent pollution data."
    )

    days = st.slider(
        "Prediction horizon",
        min_value=1,
        max_value=30,
        value=7
    )

    x = np.arange(len(df))

    coefficients = np.polyfit(
        x,
        df["Pollution"],
        1
    )

    model = np.poly1d(coefficients)

    future_x = np.arange(
        len(df),
        len(df) + days
    )

    prediction = model(future_x)

    prediction = np.clip(
        prediction,
        0,
        100
    )

    future_dates = pd.date_range(
        start=df["Date"].iloc[-1] + pd.Timedelta(days=1),
        periods=days,
        freq="D"
    )

    prediction_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted Pollution": prediction
    })

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Pollution"],
            mode="lines+markers",
            name="Historical"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=prediction,
            mode="lines+markers",
            name="AI Prediction"
        )
    )

    fig.update_layout(
        title="Pollution Prediction",
        xaxis_title="Date",
        yaxis_title="Pollution %",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("🔮 Prediction Data")

    st.dataframe(
        prediction_df,
        use_container_width=True
    )

    average_prediction = float(
        prediction.mean()
    )

    if average_prediction < 40:

        st.success(
            f"Predicted average pollution: {average_prediction:.1f}%"
        )

    elif average_prediction < 70:

        st.warning(
            f"Predicted average pollution: {average_prediction:.1f}%"
        )

    else:

        st.error(
            f"Predicted average pollution: {average_prediction:.1f}%"
        )

# =========================================================
# ABOUT
# =========================================================

elif page == "ℹ️ About":

    st.markdown(
        '<div class="section-title">🌍 About EcoSmart Gabès</div>',
        unsafe_allow_html=True
    )

    st.write("""
    **EcoSmart Gabès** is a concept for an environmental intelligence
    platform designed to monitor and analyze environmental indicators
    in Gabès, Tunisia.
    """)

    st.markdown("### 🎯 Main Objectives")

    st.markdown("""
    - 🌫️ Monitor pollution indicators
    - 🌡️ Monitor temperature
    - 💧 Monitor humidity
    - 🌍 Monitor CO₂
    - 🗺️ Visualize environmental zones
    - 📊 Analyze historical data
    - 🤖 Predict future pollution trends
    - 🌱 Support environmental awareness
    """)

    st.markdown("### 📍 Location")

    st.write(
        "Gabès, Tunisia — approximately 33.8815° N, 10.0982° E"
    )

    st.markdown("### 🚀 Future Development")

    st.markdown("""
    Future versions could connect the dashboard to:

    - IoT environmental sensors
    - Real-time weather APIs
    - Satellite data
    - Air-quality APIs
    - Machine-learning models
    - Industrial monitoring systems
    - Mobile applications
    """)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    🌍 EcoSmart Gabès • Environmental Intelligence Platform<br>
    Built with Python + Streamlit + Folium + Plotly
</div>
""", unsafe_allow_html=True)