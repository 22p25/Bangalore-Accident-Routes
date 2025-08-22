# Updated version of streamline_app.py:
# - Replaced manual text input of area names for origin and destination 
#   with automatic coordinate fetching (geocoding).
# - Users no longer type area names directly; instead, the app retrieves 
#   the latitude and longitude values automatically for route calculations.

import time
from pathlib import Path
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd

# Lazy import heavy libs only when needed
def import_safest_route_utils():
    global build_and_route, load_accident_data, detect_hotspots_dbscan, build_graph, attach_risk_to_graph
    from safest_route_utils import build_and_route, load_accident_data, detect_hotspots_dbscan, build_graph, attach_risk_to_graph

import_safest_route_utils()

st.set_page_config(page_title="Bangalore Safest Route", layout="wide")
st.title("🚦 Bangalore Safest Route (OpenStreetMap + DBSCAN)")

st.markdown(
    "This app uses **OpenStreetMap**, **DBSCAN** for hotspots, "
    "and **risk-aware routing** to find a safer path."
)

geolocator = Nominatim(user_agent="bangalore_safest_route_app")


@st.cache_data(show_spinner=False)
def geocode_location_cached(place_name: str):
    try:
        location = geolocator.geocode(place_name + ", Bengaluru, Karnataka, India", timeout=10)
        if location:
            return location.latitude, location.longitude
        return None, None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None


@st.cache_data(show_spinner=False)
def load_accident_data_cached(path):
    return load_accident_data(path)


@st.cache_data(show_spinner=False)
def detect_hotspots_cached(df, eps_m, min_samples):
    start = time.perf_counter()
    clusters = detect_hotspots_dbscan(df, eps_m=eps_m, min_samples=min_samples)
    elapsed = time.perf_counter() - start
    return clusters, elapsed


@st.cache_resource(show_spinner=False)
def build_graph_cached(place):
    start = time.perf_counter()
    G = build_graph(place)
    elapsed = time.perf_counter() - start
    return G, elapsed


@st.cache_resource(show_spinner=False)
def attach_risk_cached(_G, clusters):
    start = time.perf_counter()
    G = attach_risk_to_graph(_G, clusters)
    elapsed = time.perf_counter() - start
    return G, elapsed


with st.sidebar:
    st.header("Route Inputs")

    origin_area = st.text_input("Origin area name", value="Hoodi")
    dest_area = st.text_input("Destination area name", value="Electronic City")

    st.header("Tradeoff")
    alpha = st.slider("Distance weight (alpha)", 0.1, 5.0, 1.0, 0.1)
    beta = st.slider("Risk weight (beta)", 0.0, 1000.0, 300.0, 50.0)

    st.header("Hotspots (DBSCAN)")
    recompute = st.checkbox("Recompute hotspots now", value=False)
    eps_m = st.slider("DBSCAN eps (meters)", 50, 300, 120, 10)
    min_samples = st.slider("DBSCAN min_samples", 5, 100, 25, 5)

    run_btn = st.button("Compute Safest Route")

st.markdown("---")

if run_btn:
    with st.spinner("Geocoding areas..."):
        origin_lat, origin_lon = geocode_location_cached(origin_area)
        dest_lat, dest_lon = geocode_location_cached(dest_area)

    if origin_lat is None or origin_lon is None:
        st.error(f"Could not find coordinates for origin area: '{origin_area}'. Please refine.")
    elif dest_lat is None or dest_lon is None:
        st.error(f"Could not find coordinates for destination area: '{dest_area}'. Please refine.")
    else:
        with st.spinner("Loading accident data..."):
            df = load_accident_data_cached(Path("../outputs/data_prepared.csv"))

        if recompute or not Path("../outputs/hotspots.csv").exists():
            with st.spinner("Detecting hotspots..."):
                clusters, hotspot_time = detect_hotspots_cached(df, eps_m, min_samples)
                clusters.to_csv("../outputs/hotspots.csv", index=False)
                st.info(f"Hotspot detection took {hotspot_time:.2f} seconds")
        else:
            clusters = pd.read_csv("../outputs/hotspots.csv")
            hotspot_time = 0.0

        with st.spinner("Building graph..."):
            G, graph_build_time = build_graph_cached("Bengaluru, Karnataka, India")
            st.info(f"Graph building took {graph_build_time:.2f} seconds")

        with st.spinner("Attaching risk scores..."):
            G, risk_attach_time = attach_risk_cached(G, clusters)
            st.info(f"Risk attachment took {risk_attach_time:.2f} seconds")

        with st.spinner("Computing route and rendering map..."):
            start_route = time.perf_counter()
            out_path, clusters, n = build_and_route(
                origin_lat, origin_lon, dest_lat, dest_lon,
                place="Bengaluru, Karnataka, India",
                alpha=alpha, beta=beta,
                data_path=Path("../outputs/data_prepared.csv"),
                hotspots_csv=Path("../outputs/hotspots.csv"),
                save_map_path=Path("../outputs/route_map.html"),
                recompute_hotspots=False,
                eps_m=eps_m, min_samples=min_samples
            )
            route_time = time.perf_counter() - start_route

        st.success(f"Done! Accidents used: {n:,} • Hotspots: {len(clusters)}")
        st.info(f"Route computation took {route_time:.2f} seconds")
        st.caption(f"Map file: {out_path}")

        if Path(out_path).exists():
            html = Path(out_path).read_text(encoding="utf-8")
            st.components.v1.html(html, height=680, scrolling=True)
else:
    st.info("Fill inputs on the left and click **Compute Safest Route**.")

st.markdown("---")
st.write("**Tip:** Increase **beta** to avoid hotspots more aggressively. Tune DBSCAN for coarser/finer hotspot detection.")
