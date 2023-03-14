import pandas as pd
import re


def process_data():
    file = open("/home/arvin/Desktop/p3r50n47/WTA/whatsapp_chat.txt",'r',encoding='utf-8')

    data = file.read()

    res = re.findall('(\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [AaPp][Mm]) - (.+)',data)

    date =[]
    message = []

    if res:
        for x in res:
            date.append(x[0])
            message.append(x[1])


    user = []
    msg = []

    for x in message:
        if ': ' in x:
            user.append(x.split(':',1)[0])
            msg.append(x.split(':',1)[1])
        else:
            user.append("Notification")
            msg.append(x)

    df= pd.DataFrame({'date':date , 'name':user, 'message':msg})

    df["date"] = pd.to_datetime(df["date"])

    month_map = {
        1 : 'January',
        2 : 'Febraury',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'October',
        11 : 'November',
        12 : 'December'
    }

    df['month'] = df["date"].dt.month.map(month_map)

    df['year'] = df['date'].dt.year

    ### optional
    df['day'] = df['date'].dt.day

    week_map = {
        0 : 'Sunday',
        1 : 'Monday',
        2 : 'Tuesday',
        3 : 'Wednesday',
        4 : 'Thursday',
        5 : 'Friday',
        6 : 'Saturday'
    }
    df['week_day'] = df['date'].dt.weekday.map(week_map)

    df['hours'] = df['date'].dt.hour

    df['minute'] = df['date'].dt.minute

    df["month_year"] = df["month"] + " " + df["year"].astype(str)

    df["period"] = df.hours.apply(lambda x : str(x) + "-0" if x==23 else str(x) + "-" + str(x+1))


    return df