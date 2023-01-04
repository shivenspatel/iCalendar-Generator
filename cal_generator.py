import pandas as pd
import icalendar as ical
import datetime
import pytz
import uuid

class calendar():
    def __init__(self):
        self.cal = ical.Calendar()
  
        self.cal.add('version', 2.0)   
        self.cal.add('prodid', 'Shiven//Python iCal Creator//EN')

    def add_duration(self, duration_input):
        self.duration = datetime.timedelta(minutes=float(duration_input))
        self.cal.add('duration', self.duration)

    def add_event(self, event_input):
        self.cal.add_component(event_input)

    def print_ics(self):
        return self.cal.to_ical().decode('utf-8')

    def build_file(self, name):
        file = open(f"{name}.ics", "w", encoding="utf-8")
        file.write(self.cal.to_ical().decode('utf-8'))
        file.close()


class event():
    def single_day(self, start_date_input, start_month_input, start_year_input, summary_input):
        self.start_date = datetime.datetime(int(start_year_input), int(start_month_input), int(start_date_input))
        self.summary = summary_input

        self.type = "single_day"

    def time_event(self, start_date_input, start_month_input, start_year_input, start_hour_input, start_minute_input, end_hour_input, end_minute_input, timezone_input, summary_input):
        self.start_date = datetime.datetime(int(start_year_input), int(start_month_input), int(start_date_input), int(start_hour_input), int(start_minute_input))
        self.end_date = datetime.datetime(int(start_year_input), int(start_month_input), int(start_date_input), int(end_hour_input), int(end_minute_input))
        self.summary = summary_input

        self.timezone = timezone_input

        self.type = "time_event"

    def multi_day(self, start_date_input, start_month_input, start_year_input, end_date_input, end_month_input, end_year_input, summary_input):
        self.start_date = datetime.datetime(int(start_year_input), int(start_month_input), int(start_date_input))
        self.end_date = datetime.datetime(int(end_year_input), int(end_month_input), int(end_date_input))

        self.summary = summary_input

        self.type = "multi_day"

    def build(self):
        ical_event = ical.Event()
        # ical_event.add('dtstart', self.start_date)

        if self.type == "time_event":
            tz = pytz.timezone(self.timezone)

            ical_event['dtstart'] = ical.vDatetime(tz.localize(self.start_date))
            ical_event['dtend'] = ical.vDatetime(tz.localize(self.end_date))
        elif self.type == "multi_day":
            ical_event['dtstart'] = ical.vDate(self.start_date)
            ical_event['dtend'] = ical.vDate(self.end_date + datetime.timedelta(days=1))
        elif self.type == "single_day":
            ical_event['dtstart'] = ical.vDate(self.start_date)
            ical_event['dtend'] = ical.vDate(self.start_date + datetime.timedelta(days=1))

        # ical_event.add('summary', self.summary)
        ical_event['summary'] = self.summary
        ical_event['uid'] = uuid.uuid4()
        ical_event['dtstamp'] = ical.vDatetime(datetime.datetime.utcnow())

        return ical_event