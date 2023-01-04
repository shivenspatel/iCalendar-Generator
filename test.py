from cal_generator import calendar, event

def main():
    ics = calendar()

    one_day = event()
    one_day.single_day(7, 4, 2023, "One Day")
    x = one_day.build()

    ics.add_event(x)

    time_task = event()
    time_task.time_event(8, 4, 2023, 15, 0, 16, 0, "America/Indianapolis", "Time Event")
    y = time_task.build()

    ics.add_duration(60)
    ics.add_event(y)

    multi_event = event()
    multi_event.multi_day(9, 4, 2023, 13, 4, 2023, "Multi Day")
    
    z = multi_event.build()
    
    ics.add_event(z)
    
    ics.build_file('test')

main()