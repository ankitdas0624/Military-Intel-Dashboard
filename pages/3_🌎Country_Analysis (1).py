import streamlit as st
import plotly.express as px

from dataloader.data_loader import load_data
from theme_manager import apply_global_theme


st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌎",
    layout="wide"
)

apply_global_theme()


@st.cache_data
def get_countries():
    df = load_data()

    return sorted(
        df["country_txt"]
        .dropna()
        .unique()
        .tolist()
    )


@st.cache_data
def get_country_data(country):
    df = load_data()

    return df.loc[
        df["country_txt"] == country
    ].copy()


@st.cache_data
def get_country_statistics(country):
    country_df = get_country_data(country)

    incidents = len(country_df)

    fatalities = int(
        country_df["nkill"]
        .fillna(0)
        .sum()
    )

    injured = int(
        country_df["nwound"]
        .fillna(0)
        .sum()
    )

    groups_count = country_df["gname"].nunique()

    yearly = (
        country_df
        .groupby("iyear")
        .size()
        .reset_index(name="Attacks")
    )

    attack = (
        country_df
        .groupby("attacktype1_txt")
        .size()
        .reset_index(name="Count")
        .sort_values(
            "Count",
            ascending=False
        )
    )

    groups = (
        country_df
        .groupby("gname")
        .size()
        .reset_index(name="Attacks")
        .sort_values(
            "Attacks",
            ascending=False
        )
        .head(10)
    )

    weapon = (
        country_df
        .groupby("weaptype1_txt")
        .size()
        .reset_index(name="Count")
        .sort_values(
            "Count",
            ascending=False
        )
    )

    return (
        country_df,
        incidents,
        fatalities,
        injured,
        groups_count,
        yearly,
        attack,
        groups,
        weapon
    )


@st.cache_data
def get_map_data(country):
    country_df = get_country_data(country)

    map_df = country_df.dropna(
        subset=[
            "latitude",
            "longitude"
        ]
    )

    max_points = 5000

    if len(map_df) > max_points:
        map_df = map_df.sample(
            n=max_points,
            random_state=42
        )

    return map_df


@st.cache_data
def create_country_csv(country):
    country_df = get_country_data(country)

    return country_df.to_csv(
        index=False
    ).encode("utf-8")


st.title("🌎 Country Analysis")


countries = get_countries()


country = st.sidebar.selectbox(
    "Select Country",
    countries
)


(
    country_df,
    incidents,
    fatalities,
    injured,
    groups_count,
    yearly,
    attack,
    groups,
    weapon
) = get_country_statistics(country)


st.header(
    f"Intelligence Report : {country}"
)


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Incidents",
    f"{incidents:,}"
)

c2.metric(
    "Fatalities",
    f"{fatalities:,}"
)

c3.metric(
    "Injured",
    f"{injured:,}"
)

c4.metric(
    "Groups",
    f"{groups_count:,}"
)


st.divider()


left, right = st.columns(2)


with left:

    fig = px.line(
        yearly,
        x="iyear",
        y="Attacks",
        markers=True,
        title="Attacks Over Years"
    )

    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


with right:

    fig = px.pie(
        attack,
        names="attacktype1_txt",
        values="Count",
        title="Attack Types"
    )

    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


st.divider()


left, right = st.columns(2)


with left:

    fig = px.bar(
        groups,
        x="Attacks",
        y="gname",
        orientation="h",
        title="Top Terrorist Organizations"
    )

    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


with right:

    fig = px.bar(
        weapon,
        x="weaptype1_txt",
        y="Count",
        title="Weapon Types"
    )

    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


st.divider()


st.subheader("Incident Locations")


map_df = get_map_data(country)


fig = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    hover_name="city",
    hover_data={
        "country_txt": True,
        "iyear": True,
        "attacktype1_txt": True,
        "gname": True,
        "nkill": True,
        "latitude": False,
        "longitude": False
    },
    color="attacktype1_txt",
    projection="natural earth",
    title=f"Incidents in {country}",
    height=550
)


fig.update_layout(
    margin=dict(
        l=0,
        r=0,
        t=50,
        b=0
    )
)


st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


st.caption(
    f"Displaying {len(map_df):,} locations on the map."
)


st.divider()


st.subheader("Incident Details")


cols = [
    "iyear",
    "city",
    "attacktype1_txt",
    "targtype1_txt",
    "weaptype1_txt",
    "gname",
    "nkill",
    "nwound"
]


display_df = country_df[cols].head(1000)


st.dataframe(
    display_df,
    use_container_width=True,
    height=450
)


if len(country_df) > 1000:

    st.caption(
        f"Showing first 1,000 of {len(country_df):,} records."
    )


st.divider()


if st.button(
    "Prepare Country Data for Download",
    use_container_width=True
):

    csv = create_country_csv(country)

    st.download_button(
        "⬇️ Download Country Data",
        csv,
        file_name=f"{country}.csv",
        mime="text/csv",
        use_container_width=True
    )