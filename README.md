# iCalendar Generator

<h2>Overview</h2>
iCalendar is a standard for the storage and sharing of calendar events. Taking the format of .ics files, iCalendar files are ubiquitous within calendar applications and allow for the easy export and import of events between programs and calendars. 
<br></br>
The purpose of this project is to create a program that can use the <a href="https://icalendar.readthedocs.io/en/latest/">Python iCalendar library</a> to take simple data fed into it and export an iCalendar file that is ready to be imported into a calendar client. 

<h2>Purpose of Project</h2>
I wanted to be able to take the academic calendar my university has published on their website and add the events into my calendar app(s) of choice, helping me to organize and identify my schedule, especially in regard to breaks and exams. Last year, I entered the events manually into an Excel sheet and got them into my calendar by running it through various different programs. I wanted to automate this, as manually entereing and running files through multiple programs is not simple, streamlined, or practical, especially for a large number of events. 
<br></br>
I also wanted to do a few more projects that had an emphasis on object-oriented design, which I did not have in any of my existing published projects.

<h2>Event Types</h2>
The cal_generator.py file contains the classes that process entered data into an exported .ics file, ready for import. Currently, the program supports three type of events:

<ul>
<li><b>Standard All-Day Events: </b>Events that last one day and are marked as "All-Day" by most calendar clients. Contains date and description.</li>
<li><b>Time Events: </b>Events within one day with a start and end time. Requires timezone input. Contains date, start/end times, and description.</li>
<li><b>Multi-Day Events: </b>Events that have a start date and an end date. No time. Contains start/end dates and description.</li>
</ul>

<h2>Current Functionality</h2>
The web-scraping element that pulls the data from the university website and cleans it into a format that allows it to be processed by the backend is now live. The purdue_scrape.py file pulls the calendar webpage from the Purdue University website and runs it through a filter that sifts through the code and extracts information from each event. The data is stored in a Pandas DataFrame. Each DataFrame row is thus an event, and iterating over each row allows the program to create an event and add it to the calendar in the backend.

<h3>Basic Example of Functionality</h3>

<th><img width=100% alt="Calendar Example" src="https://user-images.githubusercontent.com/24969290/210479981-93b7b821-0cbe-4d6b-b6ca-df4b6f55fe24.png">

The test.py file demonstates the backend works. It creates three events, one of each type, and generates a single file containing all              of them. The one day event is classified as such by Apple Calendar. The time event, entered in with the timezone of Indianapolis (Eastern), was imported with that classification, allowing it to be easily converted to the user's current timezone. The screenshot was taken on a device in Chicago's timezone (Central), and the event's time was automatically changed within the calendar client to reflect that. The multi-day events span over the specified dates without issue.
