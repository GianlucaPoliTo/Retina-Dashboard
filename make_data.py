import pandas as pd
def make_rtp_data(dict_flow_data, PT, IP_s, IP_d, LONG):
    packets_per_second = {}
    kbps_series = {}
    inter_packet_gap_s = {}
    inter_rtp_timestamp_gap = {}
    len_frame = {}
    rtp_timestamp = {}
    interarrival_min = {}
    interarrival_max = {}

    for flow_id in dict_flow_data.keys():
        if ((flow_id[5] in PT) or not PT) and\
             ((flow_id[1] in IP_s) or not IP_s) and\
                 ((flow_id[2] in IP_d) or not IP_d) and\
                     len(dict_flow_data[flow_id])>int(LONG):
                        # If the index is already datetime
            if isinstance(dict_flow_data[flow_id].index, pd.DatetimeIndex):
                inner_df = dict_flow_data[flow_id].sort_index().reset_index()
            else:
                inner_df = dict_flow_data[flow_id].sort_values('timestamps')

            datetime = pd.to_datetime(inner_df['timestamps'], unit='s')
            inner_df = inner_df.set_index(datetime)

            packets_per_second[flow_id] = inner_df.iloc[:, 0].resample('S').count()
            kbps_series[flow_id] = inner_df['len_frame'].resample('S').sum() * 8 / 1024
            inter_packet_gap_s[flow_id] = inner_df['timestamps'].diff().dropna()
            interarrival_min[flow_id] = inter_packet_gap_s[flow_id].resample('S').min()
            interarrival_max[flow_id] = inter_packet_gap_s[flow_id].resample('S').max()
            inter_rtp_timestamp_gap[flow_id] = inner_df['rtp_timestamp'].diff().dropna()
            len_frame[flow_id] = inner_df["len_frame"].copy()
            rtp_timestamp[flow_id] = inner_df["rtp_timestamp"].copy()

    return {"Packet/s":packets_per_second, "kbps":kbps_series, "Interarrival [s]":inter_packet_gap_s, "RTP interarrival":inter_rtp_timestamp_gap,
            "frame length":len_frame, "RTP timestamp":rtp_timestamp,
            "interarrival min":interarrival_min, "interarrival max":interarrival_max}