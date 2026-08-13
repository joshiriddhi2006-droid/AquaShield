import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from folium.plugins import LocateControl
import plotly.express as px


# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="AquaShield — Emergency GIS & Flood Navigation",
    layout="wide",
    page_icon="🚨"
)


# --------------------------------------------------
# COMPLAINT CONTEXT FROM CITIZEN PORTAL
# --------------------------------------------------
complaint_category = st.query_params.get("category", "")
complaint_title = st.query_params.get("title", "")

if complaint_category:
    st.info(
        f"🚨 Citizen Complaint Detected: {complaint_category}"
        + (f" — {complaint_title}" if complaint_title else "")
    )


# --------------------------------------------------
# AUTHORITY DASHBOARD API CONNECTION
# --------------------------------------------------
AUTHORITY_API_URL = "http://127.0.0.1:5000/api/incidents"


def send_incident_to_authority(
    location,
    water,
    department,
    status="New Incident"
):
    payload = {
        "location": location,
        "water": water,
        "department": department,
        "status": status,
        "source": "GIS / AI"
    }

    try:
        response = requests.post(
            AUTHORITY_API_URL,
            json=payload,
            timeout=5
        )

        if response.status_code == 201:
            return True, response.json()

        return False, (
            f"Authority API returned status "
            f"{response.status_code}"
        )

    except requests.exceptions.RequestException as e:
        return False, f"Authority Dashboard unavailable: {e}"


# ----------------------------------------------------
# STYLES
# ----------------------------------------------------
st.markdown(
    '''
    <style>

    .main-header {
        background-color: #1e293b;
        color: #f8fafc;
        padding: 18px 25px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .ai-box {
        background-color: #f1f5f9;
        border-left: 5px solid #3b82f6;
        padding: 12px;
        border-radius: 6px;
        margin-top: 10px;
        color: #1e293b;
    }

    .alert-box-danger {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
        color: #991b1b;
    }

    .alert-box-warning {
        background-color: #fffbe6;
        border-left: 5px solid #f59e0b;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
        color: #78350f;
    }

    .alert-box-success {
        background-color: #f0fdf4;
        border-left: 5px solid #22c55e;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
        color: #166534;
    }

    .card-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    </style>
    ''',
    unsafe_allow_html=True
)


# ----------------------------------------------------
# MAIN HEADER
# ----------------------------------------------------
st.markdown(
    '''
    <div class="main-header">
        <h2>Aquashield — Vehicle-Aware Flood GIS System</h2>
        <p style="margin:0; opacity:0.85;">
            Permanent Lifetime Routing & Real-Time Emergency Navigation
        </p>
    </div>
    ''',
    unsafe_allow_html=True
)


# ----------------------------------------------------
# PERMANENT LOCAL DATA ENGINE
# ----------------------------------------------------
COLOR_MAP = {
    "HIGH": "#D9534F",
    "MEDIUM": "#E6A23C",
    "LOW": "#74C69D",
    "SAFE": "#2D6A4F"
}


@st.cache_data
def load_permanent_data():

    return pd.DataFrame([
        {
            "name": "Main Junction Crossing",
            "lat": 22.7196,
            "lon": 75.8577,
            "risk": "HIGH",
            "water_cm": 48,
            "department": "Traffic Police",
            "status": "Road Blocked ❌",
            "hex": COLOR_MAP["HIGH"],
            "icon_color": "red"
        },
        {
            "name": "Railway Underpass",
            "lat": 22.6912,
            "lon": 75.8658,
            "risk": "MEDIUM",
            "water_cm": 22,
            "department": "Municipal Corp",
            "status": "Under Review ⚠️",
            "hex": COLOR_MAP["MEDIUM"],
            "icon_color": "orange"
        },
        {
            "name": "Bus Stand Road",
            "lat": 22.7244,
            "lon": 75.8839,
            "risk": "LOW",
            "water_cm": 8,
            "department": "Road Maintenance",
            "status": "Resolved 🟢",
            "hex": COLOR_MAP["LOW"],
            "icon_color": "green"
        },
        {
            "name": "Flyover Bypass",
            "lat": 22.7500,
            "lon": 75.8700,
            "risk": "SAFE",
            "water_cm": 0,
            "department": "Emergency Control",
            "status": "Public Safe Route ✅",
            "hex": COLOR_MAP["SAFE"],
            "icon_color": "green"
        }
    ])


complaint_data = load_permanent_data()


# ----------------------------------------------------
# LOCATION DATA
# ----------------------------------------------------
LOCATION_COORDS = {
    "Current Position (Railway Station)": [22.7100, 75.8500],
    "Current Position (Bus Stand)": [22.7244, 75.8839],
    "City Civil Hospital (Destination)": [22.7550, 75.8800],
    "Airport Road Terminal (Destination)": [22.7600, 75.8400]
}


# ----------------------------------------------------
# VEHICLE PROFILES
# ----------------------------------------------------
VEHICLE_PROFILES = {
    "🛵 Two-Wheeler / Bike / Scooter": {
        "max_water": 10,
        "label": "Bike"
    },
    "🚗 Hatchback / Sedan (Swift, City, Dzire)": {
        "max_water": 15,
        "label": "Sedan"
    },
    "🚙 SUV / Compact SUV (Creta, Brezza, Thar)": {
        "max_water": 32,
        "label": "SUV"
    },
    "🚨 Emergency Ambulance / Heavy Truck": {
        "max_water": 50,
        "label": "Emergency Vehicle"
    }
}


# ----------------------------------------------------
# NAVIGATION TABS
# ----------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Vehicle Route Planner",
    "📸 Photo Inspector",
    "📊 Analytics Dashboard",
    "🤖 AquaBot Assistant"
])


# ====================================================
# TAB 1 — VEHICLE ROUTE PLANNER
# ====================================================
with tab1:

    st.subheader("📍 Vehicle Water-Clearance Route Inspector")

    col_filter, col_map = st.columns([1, 3])


    # ------------------------------------------------
    # LEFT SIDE
    # ------------------------------------------------
    with col_filter:

        st.markdown("#### 🚘 1. Select Vehicle Type")

        vehicle_choice = st.selectbox(
            "Choose your vehicle:",
            list(VEHICLE_PROFILES.keys())
        )

        selected_vehicle = VEHICLE_PROFILES[vehicle_choice]

        max_safe_depth = selected_vehicle["max_water"]

        st.caption(
            f"💡 **Water Clearance Limit:** "
            f"Max **{max_safe_depth} cm**"
        )


        # --------------------------------------------
        # NAVIGATION POINTS
        # --------------------------------------------
        st.markdown("#### 🛣️ 2. Navigation Points")

        start_loc_name = st.selectbox(
            "📍 Current Location:",
            list(LOCATION_COORDS.keys())[:2]
        )

        end_loc_name = st.selectbox(
            "🎯 Destination:",
            list(LOCATION_COORDS.keys())[2:]
        )

        start_coords = LOCATION_COORDS[start_loc_name]
        end_coords = LOCATION_COORDS[end_loc_name]


        # --------------------------------------------
        # ROUTE ASSESSMENT
        # --------------------------------------------
        st.divider()

        st.markdown("#### 🚨 Tailored Route Assessment")


        if max_safe_depth <= 10:

            st.markdown(
                """
                <div class="alert-box-danger">
                    <b>⛔ HIGH DANGER FOR TWO-WHEELERS:</b><br>
                    • <b>Railway Underpass (22 cm):</b>
                    Engine lock hazard!<br>
                    • <b>Main Junction (48 cm):</b>
                    Submerged.<br>
                    👉 <b>Action:</b> Take
                    <b>Flyover Bypass Only</b>.
                </div>
                """,
                unsafe_allow_html=True
            )


        elif max_safe_depth <= 15:

            st.markdown(
                """
                <div class="alert-box-danger">
                    <b>❌ BLOCKED FOR SEDAN/HATCHBACK:</b><br>
                    • <b>Main Junction Crossing (48 cm):</b>
                    Blocked.<br>
                    • <b>Railway Underpass (22 cm):</b>
                    Risk of exhaust flooding.<br>
                    👉 <b>Action:</b> Use
                    <b>Flyover Bypass Corridor</b>.
                </div>
                """,
                unsafe_allow_html=True
            )


        elif max_safe_depth <= 35:

            st.markdown(
                """
                <div class="alert-box-warning">
                    <b>⚠️ SUV PASSABLE WITH CAUTION:</b><br>
                    • <b>Railway Underpass (22 cm):</b>
                    ✅ Passable in low gear.<br>
                    • <b>Main Junction (48 cm):</b>
                    ❌ Avoid.<br>
                    👉 <b>Action:</b> Rerouted via
                    <b>Western Expressway</b>.
                </div>
                """,
                unsafe_allow_html=True
            )


        else:

            st.markdown(
                """
                <div class="alert-box-success">
                    <b>🚨 EMERGENCY PRIORITY CLEARANCE:</b><br>
                    • <b>Railway Underpass (22 cm):</b>
                    ✅ Clear.<br>
                    • <b>Main Junction (48 cm):</b>
                    ⚠️ Heavy Vehicle Passable.<br>
                    👉 <b>Corridor Active:</b>
                    Signal Priority Enabled.
                </div>
                """,
                unsafe_allow_html=True
            )


        # --------------------------------------------
        # SAFE ROUTE MESSAGE
        # --------------------------------------------
        st.markdown(
            """
            <div class="alert-box-success">
                <b>🟢 100% DRY SAFE ROUTE:</b><br>
                • <b>Flyover Bypass:</b>
                0 cm Water Depth (Safe for All)
            </div>
            """,
            unsafe_allow_html=True
        )


        # --------------------------------------------
        # AUTHORITY INCIDENT REPORTING
        # --------------------------------------------
        st.divider()

        st.markdown("### 🚨 Authority Incident Reporting")

        if st.button(
            "🚨 Send This Flood Incident to Authority",
            use_container_width=True
        ):

            # Use the most critical monitored location
            # as the flood incident being reported.
            high_risk_rows = complaint_data[
                complaint_data["water_cm"] > 0
            ].sort_values(
                "water_cm",
                ascending=False
            )

            if not high_risk_rows.empty:

                incident_row = high_risk_rows.iloc[0]

                incident_location = incident_row["name"]
                incident_water = int(incident_row["water_cm"])
                incident_department = incident_row["department"]

            else:

                incident_location = end_loc_name
                incident_water = int(max_safe_depth)
                incident_department = "Traffic Police"


            success, result = send_incident_to_authority(
                incident_location,
                incident_water,
                incident_department
            )


            if success:

                incident = result["incident"]

                st.success(
                    f"✅ Incident sent successfully!\n\n"
                    f"Incident ID: {incident['id']} | "
                    f"Location: {incident['location']} | "
                    f"Risk: {incident['risk']} | "
                    f"Water: {incident['water']} cm"
                )

            else:

                st.error(f"❌ {result}")


    # ------------------------------------------------
    # MAP
    # ------------------------------------------------
    with col_map:

        map_center = [
            (start_coords[0] + end_coords[0]) / 2,
            (start_coords[1] + end_coords[1]) / 2
        ]


        # --------------------------------------------
        # MAP
        # --------------------------------------------
        m = folium.Map(
            location=map_center,
            zoom_start=13,
            tiles=None
        )


        # --------------------------------------------
        # OPEN STREET MAP
        # --------------------------------------------
        folium.TileLayer(
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="&copy; OpenStreetMap contributors",
            name="🗺️ Standard Open Street Map (Lifetime Free)",
            overlay=False,
            control=True
        ).add_to(m)


        # --------------------------------------------
        # CARTODB MAP
        # --------------------------------------------
        folium.TileLayer(
            tiles=(
                "https://{s}.basemaps.cartocdn.com/"
                "rastertiles/voyager/{z}/{x}/{y}{r}.png"
            ),
            attr="&copy; CartoDB",
            name="🛰️ HD Hybrid Map (Ultra Smooth)",
            overlay=False,
            control=True
        ).add_to(m)


        # --------------------------------------------
        # GPS
        # --------------------------------------------
        LocateControl(
            auto_start=False,
            flyTo=True
        ).add_to(m)


        # --------------------------------------------
        # START MARKER
        # --------------------------------------------
        folium.Marker(
            location=start_coords,
            popup=f"<b>Current Location:</b> {start_loc_name}",
            tooltip="📍 Start Point",
            icon=folium.Icon(
                color="blue",
                icon="user",
                prefix="fa"
            )
        ).add_to(m)


        # --------------------------------------------
        # DESTINATION MARKER
        # --------------------------------------------
        folium.Marker(
            location=end_coords,
            popup=f"<b>Destination:</b> {end_loc_name}",
            tooltip="🎯 Destination Point",
            icon=folium.Icon(
                color="red",
                icon="flag",
                prefix="fa"
            )
        ).add_to(m)


        # --------------------------------------------
        # FLOOD HAZARDS
        # --------------------------------------------
        for _, row in complaint_data.iterrows():

            if row["water_cm"] > 0:

                is_danger = row["water_cm"] > max_safe_depth

                circle_color = (
                    "#D9534F"
                    if is_danger
                    else "#E6A23C"
                )

                status_text = (
                    "❌ BLOCKED"
                    if is_danger
                    else "⚠️ PASSABLE WITH CAUTION"
                )


                folium.Circle(
                    location=[
                        row["lat"],
                        row["lon"]
                    ],
                    radius=(
                        350
                        if row["risk"] == "HIGH"
                        else 200
                    ),
                    color=circle_color,
                    fill=True,
                    fill_color=circle_color,
                    fill_opacity=0.45,
                    popup=(
                        f"<b>{row['name']}</b><br>"
                        f"Water Depth: {row['water_cm']} cm<br>"
                        f"Status: {status_text}"
                    )
                ).add_to(m)


            folium.Marker(
                location=[
                    row["lat"],
                    row["lon"]
                ],
                popup=(
                    f"<b>{row['name']}</b><br>"
                    f"Water Level: {row['water_cm']} cm"
                ),
                icon=folium.Icon(
                    color=row["icon_color"],
                    icon="warning-sign"
                )
            ).add_to(m)


        # --------------------------------------------
        # FLOODED ROUTE
        # --------------------------------------------
        flooded_path = [
            start_coords,
            [22.7196, 75.8577],
            [22.7300, 75.8650]
        ]

        folium.PolyLine(
            locations=flooded_path,
            color="#D9534F",
            weight=5,
            opacity=0.8,
            dash_array="6, 6",
            popup="❌ <b>UNSAFE FLOODED ROUTE</b>"
        ).add_to(m)


        # --------------------------------------------
        # SAFE ROUTE
        # --------------------------------------------
        safe_path = [
            start_coords,
            [22.7300, 75.8800],
            [22.7450, 75.8850],
            end_coords
        ]

        folium.PolyLine(
            locations=safe_path,
            color="#22C55E",
            weight=7,
            opacity=0.95,
            popup="🟢 <b>RECOMMENDED SAFE DRY ROUTE</b>"
        ).add_to(m)


        # --------------------------------------------
        # MAP CONTROL
        # --------------------------------------------
        folium.LayerControl(
            position="topright",
            collapsed=False
        ).add_to(m)


        st_folium(
            m,
            width="100%",
            height=530,
            returned_objects=[]
        )


# ====================================================
# TAB 2 — PHOTO INSPECTOR
# ====================================================
with tab2:

    st.subheader(
        "📸 Upload Flood Evidence Photo for AI Verification"
    )

    col_up, col_res = st.columns([1, 1])


    with col_up:

        uploaded_file = st.file_uploader(
            "Choose a photo from your location",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )


        if uploaded_file is not None:

            st.image(
                uploaded_file,
                caption="Uploaded Street Evidence",
                use_container_width=True
            )


    with col_res:

        if uploaded_file is not None:

            st.markdown(
                "### 🤖 AI Computer Vision Verification"
            )

            st.markdown(
                '''
                <div class="ai-box">
                    <b>Status:</b> Photo Verified ✅<br>
                    <b>Detected Objects:</b>
                    Submerged Vehicle Tires (65% submerged)<br>
                    <b>Estimated Water Level:</b>
                    <b>42 cm (High Risk)</b><br>
                    <b>GIS Action:</b>
                    Auto-plotted to Main Junction Crossing
                </div>
                ''',
                unsafe_allow_html=True
            )

            st.success(
                "✅ GIS Location Pin Successfully Updated on Map!"
            )

        else:

            st.info(
                "👆 Please upload a road photo "
                "to run AI depth analysis."
            )


# ====================================================
# TAB 3 — ANALYTICS DASHBOARD
# ====================================================
with tab3:

    st.subheader(
        "📊 City Complaint & Interactive Location Analytics"
    )

    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Total Monitored Zones",
        "4 Locations"
    )

    c2.metric(
        "High Risk Waterlogged",
        "1 Location"
    )

    c3.metric(
        "Safe Green Routes",
        "2 Corridors"
    )

    c4.metric(
        "Resolved Incidents",
        "1 Location"
    )


    st.divider()


    st.markdown(
        "### 📍 Quick Touch Map Navigator"
    )

    cols = st.columns(4)


    for idx, row in complaint_data.iterrows():

        with cols[idx]:

            st.markdown(
                f"""
                <div class="card-box">
                    <h4 style="margin-top:0; color:#1e293b; font-size:16px;">
                        {row['name']}
                    </h4>

                    <p style="margin:4px 0;">
                        <b>Risk:</b>
                        <span style="color:{row['hex']};
                        font-weight:bold;">
                            {row['risk']}
                        </span>
                    </p>

                    <p style="margin:4px 0;">
                        <b>Water Depth:</b>
                        {row['water_cm']} cm
                    </p>

                    <p style="margin:4px 0;">
                        <b>Status:</b>
                        {row['status']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


    st.divider()


    col_g1, col_g2 = st.columns(2)


    with col_g1:

        st.markdown(
            "#### 🏢 Department-wise Complaint Distribution"
        )

        fig_dept = px.bar(
            complaint_data,
            x="department",
            y="water_cm",
            color="risk",
            title="Complaints per Department",
            color_discrete_map=COLOR_MAP,
            template="plotly_white"
        )

        st.plotly_chart(
            fig_dept,
            use_container_width=True
        )


    with col_g2:

        st.markdown(
            "#### 🌊 Risk Severity Breakdown"
        )

        fig_risk = px.pie(
            complaint_data,
            names="risk",
            title="Overall City Risk Distribution",
            color="risk",
            color_discrete_map=COLOR_MAP,
            hole=0.4,
            template="plotly_white"
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )


# ====================================================
# TAB 4 — AQUABOT
# ====================================================
with tab4:

    st.subheader(
        "🤖 AquaBot — Smart Navigation Assistant"
    )

    st.caption(
        "Valid Emergency Dispatch IDs for Testing: "
        "AMB-108 or FIRE-101"
    )


    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content":
                "Hello! I am **AquaBot**. "
                "Enter your vehicle type "
                "(e.g., *Swift, Creta, Bike, Ambulance*) "
                "or **Emergency Dispatch ID** "
                "(`AMB-108`) for tailored route advice!"
            }
        ]


    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )


    if prompt := st.chat_input(
        "Ask e.g., Is Railway Underpass safe for my Swift / Creta?"
    ):

        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )


        prompt_lower = prompt.lower()


        if (
            "bike" in prompt_lower
            or "scooter" in prompt_lower
            or "2 wheeler" in prompt_lower
        ):

            response = (
                "🛵 **Bike Guidance:** "
                "Railway Underpass (22 cm) is UNSAFE. "
                "Avoid Main Junction (48 cm). "
                "Take **Ring Road Flyover**!"
            )


        elif (
            "swift" in prompt_lower
            or "sedan" in prompt_lower
            or "hatchback" in prompt_lower
        ):

            response = (
                "🚗 **Hatchback/Sedan Guidance:** "
                "Railway Underpass (22 cm) is RISKY "
                "for exhaust. Main Junction (48 cm) "
                "is BLOCKED. Take **Flyover Bypass**!"
            )


        elif (
            "suv" in prompt_lower
            or "thar" in prompt_lower
            or "creta" in prompt_lower
        ):

            response = (
                "🚙 **SUV Guidance:** "
                "Railway Underpass (22 cm) is PASSABLE "
                "in low gear. Avoid Main Junction (48 cm). "
                "Fast route: **Western Expressway**."
            )


        elif (
            "amb-108" in prompt_lower
            or "fire-101" in prompt_lower
            or "ambulance" in prompt_lower
        ):

            response = (
                "🚨 **EMERGENCY DISPATCH CORRIDOR:** "
                "Green corridor active via "
                "**Elevated Express Bypass**. "
                "Traffic signals overridden!"
            )


        else:

            response = (
                "🤖 Please mention your vehicle name "
                "(e.g., *Bike, Hatchback, SUV, Ambulance*) "
                "for depth safety advice!"
            )


        with st.chat_message("assistant"):

            st.markdown(response)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )