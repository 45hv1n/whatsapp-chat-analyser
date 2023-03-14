import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import emoji

from wordcloud import WordCloud
from transformers import pipeline

from collections import Counter


'''
sent_arr = []

for x in df.message:
  if x != " <Media omitted>" and "This message was deleted" not in x:
    sent_arr.append(sentiment(x)[0]['label'])
    print(sentiment(x)[0]['label'])
    
sent_arr

sns.countplot(sent_arr)

'''


def top_participants(df):
    top_arr = df["name"].value_counts().nlargest(3).index
    top_participants_df = pd.DataFrame()

    for x in top_arr:
        top_participants_df = pd.concat([top_participants_df , df[df["name"] == x]])

    return top_participants_df

def plot_analysis(df):
    top_arr = df["name"].value_counts().nlargest(3).index
    
    for x in top_arr:        
        
        top_df = df[df["name"] == x]

        st.markdown("##### "+x)

        ### Week Analysis
        fig , ax  = plt.subplots(1,2)
        #st.write(x + " - Weekly Analysis")
        day_explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05)
        ax[0].pie(top_df["week_day"].value_counts(), labels = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],wedgeprops=dict(width = 0.5),startangle= -40 , autopct= "%0.2f%%",pctdistance= 0.75,explode = day_explode,textprops = {"fontsize":6.5}, colors = ["#4deb7f", "#2cd361", "#29d15e","#19b349","#0b8331", "#0f7f33fc", "#046021fc", "#024016fc" ,"#02270efc", "#011708fc" ,"#010b04","#046a24", "#035e20"]);
        ax[0].set_title(x + " - Weekly Analysis",size = 8)

        explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05)
        ax[1].pie(top_df["month"].value_counts(), labels = ['January','Febraury','March','April','May','June','July','August','September','October','November','December'],wedgeprops=dict(width = 0.5),startangle= -40 ,autopct= "%0.2f%%",pctdistance= 0.75,explode = explode, textprops = {"fontsize":6.5},colors = ["#4deb7f", "#2cd361", "#29d15e","#19b349","#0b8331", "#0f7f33fc", "#046021fc", "#024016fc" ,"#02270efc", "#011708fc" ,"#010b04","#046a24", "#035e20"]);
        ax[1].set_title(x + " - Monthly Analysis", size = 8)    
        st.pyplot(fig)


def top_participants_wordclouds(df):
    top_arr = df["name"].value_counts().nlargest(3).index

    for x in top_arr:
        str_arr = ''
        
        fig , ax = plt.subplots()

        top_df = df[df["name"] == x]
        str_arr = " ".join([msg for msg in top_df["message"] if msg != ' <Media omitted>' and "This message was deleted" not in msg])
        
        
        ax = WordCloud(background_color= "black").generate(str_arr)
        st.markdown("##### " + x + "-Word Cloud")
        plt.axis("off")
        plt.imshow(ax)
        st.pyplot(fig)
        st.markdown("""---""")


def emoji_analysis(df):
    return pd.DataFrame(Counter([c for msg in df.message for c in msg if emoji.is_emoji(c)]).most_common(10), columns = ['emoji','count'])


