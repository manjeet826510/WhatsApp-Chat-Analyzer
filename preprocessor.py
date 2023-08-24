import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # pattern =  '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s'
    # message = re.split(pattern,data)[1:]
    # dates = re.findall(pattern,data)

    # df = pd.DataFrame({'user_message': message, 'message_date': dates})
    # df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')

    lines = data.strip().split('\n')
    pattern = r'(\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2})\s-\s'

    matches = []
    for line in lines:
        match = re.findall(pattern, line)
        if match:
            matches.append(match[0])
        else:
            matches.append('')

    message = []
    for line in lines:
        parts = re.split(pattern, line)
        if len(parts) > 1:
            message.append(parts[1])
        else:
            message.append('')  # Add an empty string as a placeholder

    df = pd.DataFrame({'user_message': message, 'message_date': matches})

    # Parse date and time components manually
    dates = []
    for match in matches:
        if match:
            dt_obj = datetime.strptime(match, '%m/%d/%y, %I:%M %p')
            dates.append(dt_obj)
        else:
            dates.append(None)  # Use None for rows with no match

    df['message_date'] = dates


    users = []
    messages = []
    for i in df['user_message']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])


    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # df['only_date'] = df['date'].dt.date
    # df['year'] = df['date'].dt.year
    # df['month_num'] = df['date'].dt.month
    # df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day
    # df['day_name'] = df['date'].dt.day_name()
    # df['hour'] = df['date'].dt.hour
    # df['minute'] = df['date'].dt.minute

    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    # period = []
    # for hour in df[['day_name', 'hour']]['hour']:
    #     if hour == 23:
    #         period.append(str(hour) + "-" + str('00'))
    #     elif hour == 0:
    #         period.append(str('00') + "-" + str(hour + 1))
    #     else:
    #         period.append(str(hour) + "-" + str(hour + 1))
    #
    # df['period'] = period


    return df



