# Updated version of streamline_app.py:
# - Replaced manual text input of area names for origin and destination 
#   with automatic coordinate fetching (geocoding).
# - Users no longer type area names directly; instead, the app retrieves 
#   the latitude and longitude values automatically for route calculations.


import os
from pathlib import Path
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from safest_route_utils import build_and_route

st.set_page_config(page_title="Bangalore Safest Route", layout="wide")
st.title("🚦 Bangalore Safest Route (OpenStreetMap + DBSCAN)")

st.markdown(
    "This app uses **OpenStreetMap**, **DBSCAN** for hotspots, "
    "and **risk-aware routing** to find a safer path."
)

geolocator = Nominatim(user_agent="bangalore_safest_route_app")

def geocode_location(place_name: str):
    try:
        location = geolocator.geocode(place_name + ", Bengaluru, Karnataka, India", timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None

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
    with st.spinner("Geocoding areas and computing route..."):
        origin_lat, origin_lon = geocode_location(origin_area)
        dest_lat, dest_lon = geocode_location(dest_area)

        if origin_lat is None or origin_lon is None:
            st.error(f"Could not find coordinates for origin area: '{origin_area}'. Please refine.")
        elif dest_lat is None or dest_lon is None:
            st.error(f"Could not find coordinates for destination area: '{dest_area}'. Please refine.")
        else:
            with st.spinner("Computing route and rendering map..."):
                out_path, clusters, n = build_and_route(
                    origin_lat, origin_lon, dest_lat, dest_lon,
                    place="Bengaluru, Karnataka, India",
                    alpha=alpha, beta=beta,
                    data_path=Path("../outputs/data_prepared.csv"),
                    hotspots_csv=Path("../outputs/hotspots.csv"),
                    save_map_path=Path("../outputs/route_map.html"),
                    recompute_hotspots=recompute,
                    eps_m=eps_m, min_samples=min_samples
                )
            st.success(f"Done! Accidents used: {n:,} • Hotspots: {len(clusters)}")
            st.caption(f"Map file: {out_path}")

            if Path(out_path).exists():
                html = Path(out_path).read_text(encoding="utf-8")
                st.components.v1.html(html, height=680, scrolling=True)
else:
    st.info("Fill inputs on the left and click **Compute Safest Route**.")

st.markdown("---")
st.write("**Tip:** Increase **beta** to avoid hotspots more aggressively. Tune DBSCAN for coarser/finer hotspot detection.")
