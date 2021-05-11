import altair as alt
import pandas as pd
import streamlit as st
from sidebar import load_sidebar
import pickle
import altair as alt
from make_data import make_rtp_data
from chart_personalized import hist_and_CDF, main_chart
from utility import *
from collections import defaultdict

if __name__ == '__main__':
    #UPLOAD FILE
    st.set_page_config(page_title='Retina Plot Generator', layout='wide')
    st.title('Retina Plot Generator')
    uploaded_file = st.file_uploader("Choose a file", type="pickle")
    #DASHBOARD
    if uploaded_file is not None:
    # To read file as bytes:
        st.write(f'You selected {uploaded_file.name}')
        bytes_data = uploaded_file.getvalue()
    # To convert to a string based IO:
    #TABLE
        dict_flow_data = pickle.loads(bytes_data)
    else:
        st.write(f'You selected 3_p.pickle')
        with open(r"basic_example/3_p.pickle", "rb") as f:
            dict_flow_data = pickle.load(f)

    df_table = [list(key)+[dict_flow_data[key].shape[0], dict_flow_data[key]["len_frame"].mean()] for key in dict_flow_data]
    df_table = pd.DataFrame(df_table, columns=["SSRC", "IP SRC", "IP DST", "PORT SRC", "PORT DST", "PT", "DURATION", "PKT_AVG"])
    filter = defaultdict(list, {"pt" : df_table["PT"].unique(), "ip_s" : df_table["IP SRC"].unique(),
              "ip_d" : df_table["IP DST"].unique()})
    width, height, data_description, PT, IP_s, IP_d, LONG = load_sidebar(**filter)
    st.subheader("Flows inside pcap:")
    st.table(df_table)
#MAIN PLOT
    dict_aggregate, real_flow = make_rtp_data(dict_flow_data, PT, IP_s, IP_d, LONG)
    if all(dict_aggregate.values()):
        kbps_series_plot_melt = preparation_main_chart(dict_aggregate, "kbps")
        st.header("Bitrate Plot")
        space(2)
        main_chart(kbps_series_plot_melt, width, height, title_x="Time", title_y="Bitrate [kbit/s]")
        st.header("Packet/s Plot")
        space(2)
        packets_per_second_melt = preparation_main_chart(dict_aggregate, "Packet/s")
        main_chart(packets_per_second_melt, width, height, title_x="Time", title_y="Packet/s")
        selection2 = alt.selection_multi(fields=['variable'], bind='legend')
#CDF-PDF PLOT
    filters, filters_features = multiselect_flow(real_flow, list(dict_aggregate.keys()))
    for i in filters:
        st.header(f"{i} Graph")
        space(2)
        for j in filters_features:
            hist_and_CDF(dict_aggregate[j][i].to_frame(), dict_aggregate[j][i].name, x=j, y_left="CDF",
                         y_right="PDF")
        if data_description:
            table_description = create_description(dict_aggregate, i, filters_features)
            st.table(table_description)
        space(3)



