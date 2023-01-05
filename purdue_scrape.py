import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import cal_generator

page = requests.get("https://www.purdue.edu/registrar/calendars/2023-24-Academic-Calendar.html")
soup = bs(page.content, 'html.parser') 

month_list = soup.find_all('h4', {'class':''})
events = soup.find_all('tbody', {'class':''})

df = pd.DataFrame(columns=['start_month', 'start_date', 'start_year', 'start_hour', 'start_minute', 'end_month', 'end_date', 'end_year', 'end_hour', 'end_minute', 'description'])

for table, table_index in zip(events, range(len(events))):
    event_list = table.find_all('tr', {'class':''})

    for event, event_index in zip(event_list, range(len(event_list))):
        month = str(month_list[table_index].text)
        date = str(event.find_all('td', {'class':'day noGutterLeft col-lg-1 col-md-2 col-sm-2 col-xs-3'})[0].text)
        if table_index < 5:
            year = 2023
        else:
            year = 2024
        description = event.find_all('td', {'class':'description col-lg-11 col-md-10 col-sm-10 col-xs-9'})[0]
        
        if len(date) > 2:
            split_string = date.split("-")

            if len(split_string[0]) > 2 or len(split_string[1]) > 2:
                start = split_string[0].split(" ")
                start_month = start[0]
                start_date = start[1]

                end = start = split_string[1].split(" ")
                end_month = end[0]
                end_date = end[1]

                if "a.m." in str(description) or "p.m." in str(description):
                    cut_string = description.text.split(".m.")
                    df.loc[len(df)] = [start_month, int(start_date), year, '', '', end_month, end_date, year, '', '', str(cut_string[1]).strip()]
                else:
                    df.loc[len(df)] = [start_month, int(start_date), year, '', '', end_month, end_date, year, '', '',str(description.text).strip()]
            else:
                start_month = month
                start_date = split_string[0]

                end_month = month
                end_date = split_string[1]

                df.loc[len(df)] = [start_month, int(start_date), year, '', '', end_month, end_date, year, '', '', str(description.text.strip())]

        elif "a.m." in str(description):
            split_string = description.text.split("a.m.")

            def split_check():
                try:
                    return split_string[1].strip() + split_string[2]
                except:
                    return split_string[1]
    
            if ":" in split_string[0]:
                time = split_string[0].split(":")
                
                hour = int(time[0])
                minute = int(time[1])

                if hour == 12:
                    hour = hour + 12
                else:
                    hour = hour + 0

                df.loc[len(df)] = [month, int(date), year, hour, minute, '', '', '', (hour + 1), minute, split_check().strip()]
            else:
                time = split_string[0].split(":")
                
                hour = int(time[0])
                minute = 0

                if hour == 12:
                    hour = hour + 12
                else:
                    hour = hour + 0

                df.loc[len(df)] = [month, int(date), year, hour, minute, '', '', '', (hour + 1), minute, split_check().strip()]

        elif "p.m." in str(description):
            split_string = description.text.split("p.m.")
            
            if ":" in split_string[0]:
                time = split_string[0].split(":")
                
                hour = int(time[0])
                minute = int(time[1])

                if hour == 12:
                    hour = hour + 0
                else:
                    hour = hour + 12

                df.loc[len(df)] = [month, int(date), year, hour, minute, '', '', '', (hour + 1), minute, split_check().strip()]
            else:
                time = split_string[0].split(":")
                
                hour = int(time[0])
                minute = 0

                if hour == 12:
                    hour = hour + 0
                else:
                    hour = hour + 12

                df.loc[len(df)] = [month, int(date), year, hour, minute, '', '', '', (hour + 1), minute, split_check().strip()]

        else:
            df.loc[len(df)] = [month, int(date), year, '', '', '', '', '', '', '', description.text.strip()]

df['start_code'] = None
df['end_code'] = None

def code_generator(month):
    if month.title() == "Jan":
        return 1
    elif month.title() == "Feb":
        return 2
    elif month.title() == "Mar":
        return 3
    elif month.title() == "Apr":
        return 4
    elif month.title() == "May":
        return 5
    elif month.title() == "Jun":
        return 6
    elif month.title() == "Jul":
        return 7
    elif month.title() == "Aug":
        return 8
    elif month.title() == "Sep":
        return 9
    elif month.title() == "Oct":
        return 10
    elif month.title() == "Nov":
        return 11
    elif month.title() == "Dec":
        return 12

for start_month, end_month, index in zip(list(df['start_month']), list(df['end_month']), list(df.index)):
    if df.at[int(index), 'start_month'] == "":
        df.at[int(index), 'start_code'] = code_generator(start_month[0:3])
    else:
        df.at[int(index), 'start_code'] = code_generator(start_month[0:3])
        df.at[int(index), 'end_code'] = code_generator(end_month[0:3])
        
calendar = cal_generator.calendar()

for index in list(df.index):
    if df.at[index, 'end_hour'] == '':
        if df.at[index, 'end_date'] == '':
            # all-day event goes here
            date = df.at[index, 'start_date']
            month = df.at[index, 'start_code']
            year = df.at[index, 'start_year']
            description = df.at[index, 'description']

            event = cal_generator.event()
            event.single_day(date, month, year, description)
            built_event = event.build()
            calendar.add_event(built_event)
        else:
            # multi-day goes here
            start_date = df.at[index, 'start_date']
            start_month = df.at[index, 'start_code']
            start_year = df.at[index, 'start_year']
            end_date = df.at[index, 'end_date']
            end_month = df.at[index, 'end_code']
            end_year = df.at[index, 'end_year']
            description = df.at[index, 'description']

            event = cal_generator.event()
            event.multi_day(start_date, start_month, start_year, end_date, end_month, end_year, description)
            built_event = event.build()
            calendar.add_event(built_event)
    else:
        # time event goes here
        date = df.at[index, 'start_date']
        month = df.at[index, 'start_code']
        year = df.at[index, 'start_year']
        start_hour = df.at[index, 'start_hour']
        start_minute = df.at[index, 'start_minute']
        end_hour = df.at[index, 'end_hour']
        end_minute = df.at[index, 'end_minute']
        timezone = 'America/Indianapolis'
        description = df.at[index, 'description']

        event = cal_generator.event()
        event.time_event(date, month, year, start_hour, start_minute, end_hour, end_minute, timezone, description)
        built_event = event.build()
        calendar.add_event(built_event)

calendar.build_file('Purdue-University-Academic-Calendar')