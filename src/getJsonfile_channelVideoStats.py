
import pandas as pd
import json
from googleapiclient.discovery import build
from yt_channelVideo_stats import yt_channel_vid_statistic

#api_key = "AIzaSyAj5k5KzAy-rgnnZS-iVU-nLNsZ2Bltnos"
api_key = "AIzaSyAQ5NOVTp3LuGQZTb3RC_RREpTe3JGpvdg"
youtube = build("youtube", "v3", developerKey=api_key)



df = pd.read_csv('/Users/seanyoo/Desktop/yt_sql_database/csv/fpvpilot_ytInfluencer.csv')
df.columns
df2 = df.loc[df['Related/Not Related'] == "Related"]
df2 = df2[['Youtube_id','Type','Related/Not Related']]
video_info = dict(zip(df2['Youtube_id'], zip(df2['Type'], df2['Related/Not Related'])))



error_list = {}

for channel_id, categ in video_info.items():
    filename = '/Users/seanyoo/Desktop/yt_sql_database/json/yt_channelVideo_stats.json'
    try:
        yt_stats = yt_channel_vid_statistic(str(channel_id), api_key, youtube, categ[1])
        yt_stats.updateJson(filename)
    except:
        error_list[channel_id] = categ

        
    