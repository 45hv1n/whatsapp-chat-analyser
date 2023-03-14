import data_preprocessing as dp
import analysis 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud

import emoji
from collections import Counter

from transformers import pipeline

import streamlit as st

plt.style.use("dark_background")

### #29d15e, #19b349 , #0b8331,  #0f7f33fc , #046021fc , #024016fc , #02270efc , #011708fc ,#010b04

plot_clr = "#0b8331"

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


st.sidebar.title("Whatsapps Chat Analyzer")
st.title("Whatsapps Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    df = dp.process_data()

    user_lists = df.name.unique().tolist()
    user_lists.remove("Notification")
    user_lists.sort()
    user_lists.insert(0,"Overall")

    

    selected_user = st.sidebar.selectbox("Participants" , user_lists)

    if st.sidebar.button("Start Analysis"):
        st.markdown("""---""")

        df = df[df['name'] == selected_user] if(selected_user != 'Overall') else df
        
        col1 , col2 , col3 , col4  = st.columns(4)

        with col1:
            #st.subheader("Participants")
            #st.subheader(len(df["name"].unique()))
            st.metric("Participants" , value = len(df["name"].unique()))

        with col2:
            #st.subheader("Messages")
            #st.subheader(df.shape[0])
            st.metric("Message" , value = df.shape[0])
        
        with col3:
            #st.subheader("Media Files")
            #st.subheader(len(df["message"][df["message"] == " <Media omitted>"]))
            st.metric("Media Files" , value = len(df["message"][df["message"] == " <Media omitted>"]))

        with col4:
            #st.subheader("Words")
            #st.subheader(sum(df["message"].apply(lambda x : len(x.split()) if(x!= " <Media omitted>" ) else  0)))
            st.metric("Words" , value = sum(df["message"].apply(lambda x : len(x.split()) if(x!= " <Media omitted>" ) else  0)))

        st.markdown("""---""")

        ### ------------------------------------------------

        acol1 , acol2 = st.columns(2)

        with acol1:
            ### Analysis of chats over a period of week
            st.markdown("#### Weekly Analysis")
            fig, ax = plt.subplots()

        
            days_arr = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
            ax = sns.countplot(df["week_day"],order = days_arr , palette = [plot_clr])
            ax.set(xlabel = "weeks" , ylabel = "Number of messages")
            plt.xticks(rotation = 90)
            st.pyplot(fig)
            #st.markdown("""---""")
            
        ### ------------------------------------------------
        with acol2:

            ### Analysis of chats over a period of Month
            st.markdown("#### Monthly Analysis")
            fig, ax = plt.subplots()
        
            month_arr = ['January','Febraury','March','April','May','June','July','August','September','October','November','December']
            plt.xticks(rotation = 90)
            ax.set(xlabel = "month" , ylabel = "Number of messages")
            ax = sns.countplot(df["month"], order = month_arr , palette=[plot_clr])

            st.pyplot(fig)
        
        st.markdown("""---""")

        ### ------------------------------------------------


        ### ------------------------------------------------

        ### Timeline of the month
        st.markdown("#### Monthly Timeline")
        fig, ax = plt.subplots(figsize = (15,8))
    
        month_timeline = df["month_year"].value_counts().to_dict()
        plt.xticks(rotation = 90)
        ax = sns.lineplot(data = df,x = 'month_year', y = df["month_year"].map(month_timeline) , markers = True , marker = 'o' , color = plot_clr )

        st.pyplot(fig)

        st.markdown("""---""")

        ### ------------------------------------------------

        ### Timeline of the every day
        st.markdown("#### Daily Timeline")
        fig, ax = plt.subplots(figsize = (15,8))

        df["only_date"] = df["date"].dt.date
        date_timeline = df["only_date"].value_counts().to_dict()
        plt.xticks(rotation = 90)
        ax = sns.lineplot(data = df,x = 'only_date', y = df["only_date"].map(date_timeline) , color = plot_clr)

        st.pyplot(fig)
        st.markdown("""---""")

        ### Word Clouds 
        st.markdown("#### Word Clouds")
        fig, ax = plt.subplots()
        str_arr = " ".join([msg for msg in df["message"] if msg != ' <Media omitted>' and "This message was deleted" not in msg])

        ax = WordCloud(background_color= "black").generate(str_arr)
        #plt.title(x,fontdict={'fontsize': 10})
        plt.axis("off")
        plt.imshow(ax)
        st.pyplot(fig)
        st.markdown("""---""")

        ### Overall analysis
        if selected_user == "Overall":
            ### ------------------------------------------------

            ### Analysis of the Participants who sent the maximum message
            st.markdown("#### Participants who sent the maximum number of messages")
            fig, ax = plt.subplots(figsize = (10,5))

            plt.xticks(rotation= 90)
            ax = sns.countplot(y = 'name' , data = df , order = df["name"].value_counts().nlargest(15).index, palette = ["#0b8331"])

            st.pyplot(fig)
            st.markdown("""---""")

            ### ------------------------------------------------

            ### Analysis of contributuion the Participants 

            ### ------------------------------------------------

            ### Overall contributuion of top Participants over a period of a week
            st.subheader("Analysis Of Top 3 Participants")

            con_col1 , con_col2 = st.columns(2)

            with con_col1:
                st.markdown("#### Weekly Analysis")

                top_participants_df = analysis.top_participants(df)

                fig, ax = plt.subplots()

                day_explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05)
                plt.pie(top_participants_df["week_day"].value_counts(), labels = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],wedgeprops=dict(width = 0.5),startangle= -40 , autopct= "%0.2f%%",pctdistance= 0.75,explode = day_explode, colors = ["#4deb7f", "#2cd361", "#29d15e","#19b349","#0b8331", "#0f7f33fc", "#046021fc", "#024016fc" ,"#02270efc", "#011708fc" ,"#010b04","#046a24", "#035e20"])

                st.pyplot(fig)
                #st.markdown("""---""")

            ### ------------------------------------------------
            with con_col2:
                    
                ### Overall contributuion of the Participants over a period of a week
    
                month_explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05)
                st.markdown("#### Monthly Analysis")
                
                fig, ax = plt.subplots()
                ax = plt.pie(top_participants_df["month"].value_counts(), labels = ['January','Febraury','March','April','May','June','July','August','September','October','November','December'],wedgeprops=dict(width = 0.5),startangle= -40 ,autopct= "%0.2f%%",pctdistance= 0.75,explode = month_explode , colors = ["#4deb7f", "#2cd361", "#29d15e","#19b349","#0b8331", "#0f7f33fc", "#046021fc", "#024016fc" ,"#02270efc", "#011708fc" ,"#010b04","#046a24", "#035e20"]);

                st.pyplot(fig)
            st.markdown("""---""")

            ### ------------------------------------------------
            ### Individual contribution of top participants
            st.markdown("#### Individual Analysis Of The Top Participants")
            
            analysis.plot_analysis(df)
            st.markdown("""---""")

            ### ------------------------------------------------
            ### Individual contribution of top participants [WordClouds]
            st.markdown("#### Word Cloud Of The Top Participants")
            analysis.top_participants_wordclouds(df)

            ### ------------------------------------------------
            tpcol1 , tpcol2 = st.columns(2)

            with tpcol1:
                ### Pivot table for top participants
                
                st.markdown("#### Distribution Of The Messages On A Monthly Basis")
                
                fig, ax = plt.subplots()

                month_arr = ['January','Febraury','March','April','May','June','July','August','September','October','November','December']
                ax = sns.heatmap(pd.pivot_table(top_participants_df , index = "month" , columns= "name", values = "message" , aggfunc= "count" ,sort=False).fillna(0).reindex(index = month_arr) , cmap = "Greens_r")
                st.pyplot(fig)

            with tpcol2:
                ### ------------------------------------------------
                ### Pivot table for top participants
                
                st.markdown("#### Distribution Of The Messages On A Daily Basis")
                
                fig, ax = plt.subplots()

                days_arr = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
                ax = sns.heatmap(pd.pivot_table(top_participants_df , index = "week_day" , columns= "name", values = "message" , aggfunc= "count" ,sort=False).fillna(0).reindex(index = days_arr), cmap = "Greens_r")
                st.pyplot(fig)
            st.markdown("""---""")

        ###Emoji analysis

        st.markdown("#### Frequently Used Emojis")
        emo_df = analysis.emoji_analysis(df)

        #fig = px.pie(data_frame=emo_df , values = emo_df['count'] , names= emo_df['emoji'], title = 'Emoji Analysis' , hole= 0.5, color = ["#4deb7f", "#2cd361", "#29d15e","#19b349","#0b8331", "#0f7f33fc", "#046021fc", "#024016fc" ,"#02270efc", "#011708fc"])

        fig = px.pie(data_frame=emo_df , values = emo_df['count'] , names= emo_df['emoji'], hole= 0.5 ,  color_discrete_sequence= px.colors.sequential.Greens_r)
        fig.update_traces(textposition = 'inside' , textinfo = 'percent+label')
        st.plotly_chart(fig) 
        st.markdown("""---""")

        ### Pivot Tablea

        st.markdown("#### Time Spent By Participant")
            
        fig, ax = plt.subplots(figsize = (10,5))

        period_arr = ['0-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9','9-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23','23-0']
        ax = sns.heatmap(pd.pivot_table(df , index = "week_day" , columns= "period", values = "message" , aggfunc= "count" ,sort=False).fillna(0).reindex(index = days_arr , columns = period_arr),cmap = "Greens_r" )

        st.pyplot(fig)
        st.markdown("""---""")

        

        ### Pivot Chart wrt month vs week days

        st.markdown("#### Number Of Messages Sent By Participant On Daily Basis")
            
        fig, ax = plt.subplots(figsize = (10,5))

        ax = sns.heatmap(pd.pivot_table(df , index = "week_day" , columns= "month_year", values = "message" , aggfunc= "count" ,sort=False).fillna(0).reindex(index = days_arr), cmap= "Greens_r")
        st.pyplot(fig)
        st.markdown("""---""")

    if(selected_user != 'Overall'):

        sent_analysis = pipeline("sentiment-analysis")

        ### Sentiment Analysis
        st.markdown("### Sentiment Analysis")

        st.markdown("#### Monthly Sentiment Analysis")
        arr = []

        new_df = df[df["name"] == selected_user]

        for x in new_df.message:
            if x ==  " <Media omitted>" or "This message was deleted" in x:
                arr.append("Neutral")
            else:
                arr.append(sent_analysis(x)[0]['label'])
        
        new_df["sentiment"] = arr

        fig, ax = plt.subplots(figsize = (10,5))

        ax = sns.heatmap(pd.pivot_table(data = new_df , index = "sentiment" , columns = "month_year" , values = "message", aggfunc = "count").fillna(0)  , cmap = "Greens_r")
        st.pyplot(fig)
        st.markdown("""---""")

        st.markdown("#### Daily Sentiment Analysis")

        fig, ax = plt.subplots(figsize = (15,5))

        ax = sns.heatmap(pd.pivot_table(data = new_df , index = "sentiment" , columns = "only_date" , values = "message", aggfunc = "count").fillna(0), cmap = "Greens_r")        
        st.pyplot(fig)
        st.markdown("""---""")