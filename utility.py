import pandas as pd
import streamlit as st

def preparation_main_chart(dict_aggregate, name):
    source = pd.concat(dict_aggregate[name].values(), axis=1, keys=[str(x) for x in dict_aggregate[name].keys()])
    source = source.melt(value_vars=source.columns, ignore_index=False).rename({"variable":"flow"}, axis=1)
    source.reset_index(drop=False, inplace=True)
    return source

def space(n):
    for i in range(n):
        st.write("")
    return

def create_description(dict_aggregate, flow, filters_features):

    dict_description = {key:dict_aggregate[key][flow].describe() for key in filters_features}
    return pd.DataFrame.from_dict(dict_description)

def multiselect_flow(flows, features):
    col1, col2 = st.beta_columns(2)
    filters = col1.multiselect("Select Flow Compare", flows)
    filters_features = col2.multiselect("Select Features", features)
    return filters, filters_features

