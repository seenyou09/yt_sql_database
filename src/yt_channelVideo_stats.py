#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 17:11:01 2023

@author: seanyoo
"""

import json
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

api_key = "AIzaSyDqYcV4mJWQImAteWnLeIzVgO4X9fO-mIY"
#api_key = "AIzaSyAQ5NOVTp3LuGQZTb3RC_RREpTe3JGpvdg"
youtube = build("youtube", "v3", developerKey=api_key)
filename = "channel_stat_df.json"

class yt_channel_vid_statistic:
    def __init__(self, url, api_key, youtube, my_categ):
        self.url = url
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.my_categ = my_categ
        
        # Get YouTube id from URL
        self.id = self.get_youtube_Id_fromUrl()
        
        # YouTube Channel Statistic
        self.channelStatistic_dic = self.get_youtubeChannelStatistic()
        
        # Get upload_id & video_list for video_statistic:
        self.channel_name, self.upload_id = self.get_upload_id()
        self.video_list = self.get_video_list()
        self.video_statistic_list = self.get_video_details()
        

    
    def get_youtube_Id_fromUrl(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rss_link = soup.find('link', {'rel': 'alternate', 'type': 'application/rss+xml'})
        if rss_link:
            rss_url = rss_link.get('href')
            rss_url = rss_url.split("channel_id=", 1)[1]
            return rss_url
        else:
            return ""
    
    
    #Function to get Channel_statistic 
    def get_youtubeChannelStatistic(self):
        request = self.youtube.channels().list(
            part="snippet,statistics,brandingSettings,topicDetails",
            id=self.id
        )
        response = request.execute()

        cn = response['items'][0]['snippet']['title']
        s = response['items'][0]['statistics']['subscriberCount']
        v = response['items'][0]['statistics']['viewCount']
        tv = response['items'][0]['statistics']['videoCount']
        try:
            cg = response['items'][0]['topicDetails']['topicCategories']
        except:
            cg = ""
        try:
            k = response['items'][0]['brandingSettings']['channel']['keywords']
        except:
            k = ""
        self.channelStatistic_dic = dict(Channel_name=cn, Channel_id = self.id, Video_statistic = [], Channel_Statistic={
            "Subscribers": s,
            "Views": v,
            "Total_videos": tv,
            "Categories": cg,
            "Keywords": k,
            "Manual_category": self.my_categ
        })

        return self.channelStatistic_dic
    
    
    
    
    #Function to get Video_details

    def get_upload_id(self):
        request = youtube.channels().list(
            part="snippet,contentDetails",
            id=self.id
        )
        response = request.execute()
        self.channel_name=response['items'][0]['snippet']['title']
        self.upload_id = response["items"][0]['contentDetails']['relatedPlaylists']['uploads']
        
        
        return self.channel_name, self.upload_id

    def get_video_list(self):
        self.video_list = []
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=self.upload_id,
            maxResults=25
        )
        response = request.execute()
        data = response['items']

        for video in data:
            video_id = video['contentDetails']['videoId']
            if video_id not in self.video_list:
                self.video_list.append(video_id)
    
        return self.video_list
    
    
    def get_video_details(self): 
        self.video_statistic_list = []
        for i in range(0, len(self.video_list)):
            request= youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=self.video_list[i]
            )
    
            data = request.execute()
            for video in data['items']:
                title=video['snippet']['title']
                published=video['snippet']['publishedAt']
                description=video['snippet']['description']
                try:
                    tag_count= len(video['snippet']['tags'])
                except:
                    tag_count= " "
                view_count=video['statistics'].get('viewCount',0)
                like_count=video['statistics'].get('likeCount',0)
                try:
                    dislike_count=video['statistics'].get('dislikeCount',0)
                except:
                    dislike_count= " "
                try:    
                    comment_count=video['statistics'].get('commentCount',0)
                except:
                    comment_count= " "
                stats_dict=dict(name=self.channel_name, title=title, description=description, published=published, tag_count=tag_count, view_count=view_count, like_count=like_count, dislike_count=dislike_count, comment_count=comment_count)
                self.video_statistic_list.append(stats_dict)  
    
        return self.video_statistic_list
    
    
    
    #Combine
    def final_stats(self):        
        self.channelStatistic_dic["Video_statistic"].extend(self.video_statistic_list)
        return self.channelStatistic_dic
    
    
    
    
    def updateJson(self, filename):
        entry = self.final_stats()
        #read the file content 
        with open(filename, "r") as file:
            data = json.load(file)
            
        
        #Update the Json Content 
        #data.append(entry)
        key = entry["Channel_id"]
        data[key] = entry
        
        # write the JSon content 
        \
        with open(filename,"w") as file:
            json.dump(data, file, indent= 4)


#Sample 
if __name__ == "__main__":
    youtube = build("youtube", "v3", developerKey=api_key)
    filename = "/Users/seanyoo/Desktop/yt_sql_database/json/yt_channelVideo_stats.json"
    joshua = yt_channel_vid_statistic("https://www.youtube.com/@CiottiFPV", api_key, youtube, my_categ="whoop")
    yes = joshua.updateJson(filename)
    print(yes)


