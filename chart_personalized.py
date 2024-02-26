import pandas as pd
import altair as alt
import streamlit as st
from utility import space

def hist_and_CDF(source, flow_id, x=None, y_left=None, y_right=None):

    col1, col2 = st.columns(2)
    fig = alt.Chart(source).transform_window(
        cumulative_count="count()",
        sort=[{"field": flow_id}],
    ).mark_area(fillOpacity=0.3, line=True).encode(
        y="cumulative_count:Q",
        x=f"{flow_id}:Q",
    ).interactive().configure_axis(
    labelFontSize=20,
    titleFontSize=20
    )
    fig.encoding.x.title = x
    fig.encoding.y.title = y_left
    col1.altair_chart(fig, use_container_width=True)
    #PDF
    bar = alt.Chart(source).transform_density(
        flow_id,
        as_=[flow_id, 'density'],
    ).mark_area(fillOpacity=0.3, line=True).encode(
        x=f"{flow_id}:Q",
        y='density:Q',
    ).interactive()

    rule = alt.Chart(source).mark_rule(color='red').encode(
       y=f'mean{flow_id}:Q'
    )
    bar.encoding.x.title = x
    bar.encoding.y.title = y_right
    fig_2 = alt.layer(bar + rule).configure_axis(
    labelFontSize=20,
    titleFontSize=20
    )

    col2.altair_chart(fig_2, use_container_width=True)


def main_chart(source, width, heigth, title_x=None, title_y=None):
    selection = alt.selection_multi(fields=['flow'], bind='legend')
    fig = alt.Chart(source).mark_line().encode(  #kbps_series_plot_melt
        alt.X('timestamps', axis=alt.Axis(title=title_x)), #"Time"
        alt.Y('value', axis=alt.Axis(title=title_y)), #"Bitrate [kbit/s]"
        color='flow',
        strokeDash='flow',
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))

    ).properties(
        width=width,
        height=heigth
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20
    ).add_selection(
        selection
    ).interactive()
    st.altair_chart(fig, use_container_width=True)
    space(3)
