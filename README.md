# UP Team Travel Analysis Tool

## Overview

This tool is a web application built with Streamlit that provides tools for analyzing and estimating team schedules based on uploaded files and external website data.

The application presents two distinct menu items: the ' **File Uploader** ' and the ' **Estimate** .' Each menu item employs different techniques, they collectively contribute to achieving the same overarching goal.

## Getting Started

### Inactivity Warning
Sometimes, the app may display an inactivity warning due to inactivity. If encountered, click the "Yes, get this app back up" button. If the issue persists after 2 minutes, reload the page.

![back up](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/f33e0fca-0d28-44bc-a73a-942fbafdafb4)

## How To Use It

### File Uploader

**1. Download and Modify Files**
The files required for upload can be accessed at the top of the side bar. Download and modify the files:

![Files](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/7253766e-299a-4482-9264-787b2c400f71)


* Schedule.csv: Add the team schedule with date and location, like in this format.

![Excel Schedule](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/54926af0-06dd-4b9b-8b77-fd073428876c)


* Away Date.csv: Add the dates when the team is away, like in this format.

![Excel Date](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/1bacfcea-7cab-49fe-b74e-c172d7116084)


**Note:** Ensure that the **column names** remain unchanged for accurate processing.

**2. Adjust Academic Calendar Dates**
In the side bar, adjust dates based on the academic calendar:

![Dates](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/9c15fd08-3bfb-44cc-a76d-3b8e7b66e5f5)

* Fall start date = Start date of the fall semester
* Fall end date = End date of the fall semester
* Spring start date = Start date of the spring semester
* Spring end date = End date of the spring semester

**3. Upload Files**
Use the left file uploader for Schedule and the right file uploader for Away Date. Results will be displayed after a few minutes.
![File Uploader](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/8b40cb20-5294-43a0-82b0-9412a69986db)


### Estimate

**1. Adjust Academic Calendar Dates**
In the side bar, adjust dates based on the academic calendar:

![Dates](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/9c15fd08-3bfb-44cc-a76d-3b8e7b66e5f5)

* Fall start date = Start date of the fall semester
* Fall end date = End date of the fall semester
* Spring start date = Start date of the spring semester
* Spring end date = End date of the spring semester


**2. Input Team Schedule Link**
* Go to the website and the team schedule of any team

![Link Schedule](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/1ed9a998-e9fe-4779-b5e8-248b8bc1bcbe)


* Copy the link from the website

![link](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/084f4379-b15d-4461-8df0-0470cfad96bf)


* Paste it in the provided input field.

![Estimate](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/96bcc04f-57a7-4c83-a1e7-078380fac377)


**3. Adjust Academic Year**
Set the academic year to the fall year (e.g., if 2020- 2021 , put 2020).

![Estimate](https://github.com/xxedrixx/UP-athletic-schedule-analysis/assets/105680488/96bcc04f-57a7-4c83-a1e7-078380fac377)


## How It Works

### File Uploader
1 .  Schedule File Uploader: Reads the CSV file, counts the number of games, and plots the
cities visited on a map.

2. Away Date File Uploader: Reads the CSV file, calculates various days (days traveled,
    missed class days, etc.).

### Estimate
Sends a request to the provided link, scrapes the website, retrieves the schedule, adds
distance from the team's city, and estimates away dates based on distance. Cities over 250 miles away may require an overnight stay.


## Limitations
The limitations mainly affect the Estimate option:
1 .  Distance between cities is an estimate based on a straight line with a 20% margin.

2. Estimated away dates are not accurate due to factors like weather and transportation
    modes.
3 .  The reliability of data extraction are directly influenced by the consistency of the website
    to standardized formats.



## Conclusion
The file uploader menu provides accurate results but requires manual input from those
familiar with the team's schedule. <br>
The estimate menu provides estimated away dates based on website data and distance
between cities.


## Technologies Used
Python (backend) <br>
Streamlit (web interface) <br>
Open Street Map API (distance calculation) <br>
Pandas (file reading and analysis) <br>
Beautiful Soup (website scraping) <br>
Folium (map plotting) <br>

## Links
App: https://xxedrixx-up-athletic-schedule-analysis-main-6bmu9r.streamlit.app <br>
Source code: https://github.com/xxedrixx/UP-athletic-schedule-analysis


## License
This project is licensed under the MIT License.
