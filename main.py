# AUTOGENERATED! DO NOT EDIT! File to edit: schedule.ipynb.

# %% auto 0
__all__ = []

# %% schedule.ipynb 0
from datetime import datetime
from datetime import timedelta
import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm
import pandas as pd
import numpy as np
import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time
import calendar
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from bs4 import BeautifulSoup

# %% schedule.ipynb 1
st.set_page_config(layout="wide")

st.title("UP Athletic")

#sidebar
with st.sidebar:
    link_date = "https://docs.google.com/spreadsheets/d/1FiixrbbdR_8fsHtxwRynmj1cXT0e67or/edit?usp=sharing&ouid=101732481532297287492&rtpof=true&sd=true"
    this_date = "this"
    text1 = "The files to be uploaded need to look exactly like "
    text2 = " for schedule and like "
    link_schedule = "https://docs.google.com/spreadsheets/d/1BMSWHCWxgj6D3PplQZpFQHMmWYQtcANB/edit?usp=sharing&ouid=101732481532297287492&rtpof=true&sd=true"
    this_schedule = "this "
    text3 = " for date."
    line = "\n"
    text4 = "You can download the templates above."
    st.write(f"{text1}[{this_schedule}]({link_schedule}){text2}[{this_date}]({link_date}){text3}{line}{line}{text4}")

    fall_start = st.date_input("Fall start date", datetime.today())
    # Convert the selected date to the desired format
    formatted_fall_start = pd.to_datetime(fall_start)


    fall_end = st.date_input("Fall end date", datetime.today())
    # Convert the selected date to the desired format
    formatted_fall_end = pd.to_datetime(fall_end)


    spring_start = st.date_input("Spring start date", datetime.today())
    # Convert the selected date to the desired format
    formatted_spring_start = pd.to_datetime(spring_start)


    spring_end = st.date_input("Spring end date", datetime.today())
    # Convert the selected date to the desired format
    formatted_spring_end = pd.to_datetime(spring_end)
        

selected = option_menu(
    menu_title=None,
    options=["File Uploader","Estimate"],
    icons=["file-earmark-excel-fill","patch-question"],
    orientation="horizontal"
)

cols = st.columns(6)
total_games_placeholder = cols[0].metric(label="Total Game", value=None)
home_games_placeholder = cols[1].metric(label="Home Game", value=None)
away_games_placeholder = cols[2].metric(label="Away Game", value=None)
class_day_placeholder = cols[3].metric(label="Number of class day missed", value=None)
monday_placeholder = cols[4].metric(label="Class missed on monday", value=None)
friday_placeholder = cols[5].metric(label="Class missed on friday", value=None)


def game_func():
    # # SPLIT
    split_data = df['Location'].str.split(",", expand=True)

    if len(split_data.columns) == 3:
        df[['City', 'State', 'Country']] = split_data
    else:
        # If split_data has two columns (City, State), add 'NaN' values for 'Country'
        df['City'] = split_data[0]
        df['State'] = split_data[1]
        df['Country'] = np.nan

    # # ADD DISTANCE
    geolocator = Nominatim(user_agent="my_geocoder")

    city1 = "Great Falls"

    def calculate_distance(city2):
        away = geolocator.geocode(city2)
        home = geolocator.geocode(city1)

        if home and away:
            coordinates1 = (home.latitude, home.longitude)
            coordinates2 = (away.latitude, away.longitude)
            distance = (geodesic(coordinates1, coordinates2).miles) * 1.2
            return round(distance, 2)
        else:
            return None

    # Apply function to calculate distance and create the 'Distance' column
    df['Distance in mile'] = df['Location'].apply(calculate_distance)

    time.sleep(2)


    # # PRINT
    with st.expander("See DataFrame..."):
        # Display the DataFrame
        st.dataframe(df)


    # # GAME COUNT
    home = df[df["Distance in mile"] == 0.0]
    away = df[df["Distance in mile"] != 0.0]

    home_count = len(home)
    away_count = len(away)
    total_games = home_count + away_count

    # Update metric value
    total_games_placeholder.metric(label="Total Game", value=total_games)
    home_games_placeholder.metric(label="Home Game", value=home_count)
    away_games_placeholder.metric(label="Away Game", value=away_count)

    labels = [f'Home Games: {home_count}', f'Away Games: {away_count}']
    sizes = [home_count, away_count]
    colors = ['blue', 'green']

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', startangle=140)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    ax.set_title('Home Games vs Away Games')

    # Annotate the total games count below the pie chart
    ax.text(0.5, 0, f'Total Games: {total_games}', fontsize=12, color='black',
             fontweight='bold', ha='center', va='center', transform=ax.transAxes)

    with st.expander("Games"):
        # Display the plot using st.pyplot
        st.pyplot(fig)

    # # CITY
    city_most_game_away = df[df['City'] != "Great Falls"]
    city_most_game_away = city_most_game_away['City'].value_counts().reset_index()
    city_most_game_away.columns = ['City', 'Count']
    with st.expander("Most visited cities"):
        city_most_game_away

    # List of cities
    cities = df['Location']

    # Geocoder instance
    geolocator = Nominatim(user_agent="my_geocoder")
    # Get coordinates for cities
    coordinates = []
    for city in cities:
        location = geolocator.geocode(city)
        if location:
            coordinates.append((location.latitude, location.longitude))

    # Calculate mean coordinates
    mean_latitude = sum(lat for lat, lon in coordinates) / len(coordinates)
    mean_longitude = sum(lon for lat, lon in coordinates) / len(coordinates)

    # Create a map centered at the mean coordinates
    m = folium.Map(location=[mean_latitude, mean_longitude], zoom_start=4, min_zoom=4)  # Adjust zoom level as needed

    # Plot markers for cities on the map
    for city, (lat, lon) in zip(cities, coordinates):
        popup_text = f"<b>{city}</b>"  # Customize the popup content here
        folium.Marker(location=[lat, lon], tooltip=popup_text).add_to(m)


    # Display the map
    folium_static(m)
            
def day_func():
    # Function to convert weekday number to weekday name
    def get_weekday_name(date):
        return calendar.day_name[date.weekday()]

    # Filter the away_df DataFrame between the specified date ranges
    df['AwayDate'] = pd.to_datetime(df['AwayDate'])

    # Add a new column 'Weekday' containing the weekday names to the copied DataFrame
    df['Weekday'] = df['AwayDate'].apply(get_weekday_name)

    with st.expander("See dataframe..."):
        st.dataframe(df)

    days_traveled_semester = df[(df['AwayDate'] >= formatted_fall_start) & (df['AwayDate'] <= formatted_fall_end) |
                         (df['AwayDate'] >= formatted_spring_start) & (df['AwayDate'] <= formatted_spring_end)]


    monday_to_thursday_travel = days_traveled_semester[~days_traveled_semester['Weekday'].isin(['Friday', 'Saturday', 'Sunday'])].shape[0]
    friday_travel = days_traveled_semester[~days_traveled_semester['Weekday'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'])].shape[0]
    weekend_travel = days_traveled_semester[~days_traveled_semester['Weekday'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])].shape[0]
    class_day_travel = monday_to_thursday_travel + friday_travel
    days_traveled_break = len(df) - len(days_traveled_semester)

    ## NUMBER OF DAYS TRAVELED
    breaks = days_traveled_break
    semesters = len(days_traveled_semester)
    total_travel = breaks + semesters

    labels = [f'Number of days traveled \n during breaks: {breaks}', f'Number of days traveled \nduring semester: {semesters}']
    sizes = [breaks, semesters]
    colors = ['blue', 'green']

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', startangle=140)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    ax.set_title('Number of days traveled')

    # Annotate the total games count below the pie chart
    ax.text(0.5, 0, f'Total days traveled: {total_travel} days', fontsize=12, color='black',
             fontweight='bold', ha='center', va='center', transform=plt.gca().transAxes)

    with st.expander("Days Traveled"):
        # Display the plot in Streamlit
        st.pyplot(fig)

    if not days_traveled_semester.empty:
        ## TRAVEL DURING SEMESTER
        class_day = class_day_travel
        weekend = weekend_travel
        total_travel = len(days_traveled_semester)

        labels = [f'Number of class days traveled: {class_day}', f'Number of days \n on weekend traveled: {weekend}']
        sizes = [class_day, weekend]
        colors = ['blue', 'green']

        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', startangle=140)

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        ax.set_title('Days traveled during semesters', pad=30)

        # Annotate the total games count below the pie chart
        ax.text(0.5, -0.2, f'Total days traveled during semesters: {total_travel} days', fontsize=12, color='black',
                 fontweight='bold', ha='center', va='center', transform=plt.gca().transAxes)


        with st.expander("Days Traveled during semesters"):
            # Display the plot in Streamlit
            st.pyplot(fig)


        ## NUMBER OF CLASS DAY TRAVELED
        friday = friday_travel
        mon_to_thu = monday_to_thursday_travel
        total_class_days = class_day_travel

        # Update metric value
        class_day_placeholder.metric(label="Number of class day missed", value=total_class_days)
        monday_placeholder.metric(label="Class missed on monday", value=mon_to_thu)
        friday_placeholder.metric(label="Class missed on friday", value=friday)

        labels = [f'Number of days traveled \n that occurs on Friday: {friday}', f'Number of days traveled \n that occurs Monday-Thursday: {mon_to_thu}']
        sizes = [friday, mon_to_thu]
        colors = ['blue', 'green']

        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', startangle=140)

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        ax.set_title('Number of class days travel')

        # Annotate the total class days count below the pie chart
        ax.text(0.5, 0, f'Total class days traveleded: {total_class_days} days', fontsize=12, color='black',
                 fontweight='bold', ha='center', va='center', transform=plt.gca().transAxes)

        with st.expander("Class Day Traveled"):
            # Display the plot in Streamlit
            st.pyplot(fig)
    else:
        st.error("Enter valid date")
        st.warning("No class day missed because of breaks")
                

if selected == "File Uploader":
    c1, c2 = st.columns(2)
    with c1:
        schedule = st.file_uploader("Upload Schedule as CSV or EXCEL", type=["csv", "xlsx"])
    with c2:
        travel_period = st.file_uploader("Upload travel period as CSV or EXCEL", type=["csv", "xlsx"])


    with c1:  
        if schedule is not None:
            file_extension = schedule.name.split(".")[-1]

            if file_extension.lower() == "csv":
                df = pd.read_csv(schedule)
            elif file_extension.lower() == "xlsx":
                df = pd.read_excel(schedule)

            game_func()


    with c2:
        if travel_period is not None:
            file_extension = travel_period.name.split(".")[-1]

            if file_extension.lower() == "csv":
                df = pd.read_csv(travel_period)
            elif file_extension.lower() == "xlsx":
                df = pd.read_excel(travel_period)

            day_func()
else:
    ## WEB SCRAPING
    url = st.text_input("Paste link here")
    input_year = int (st.number_input("Academic year (Fall)", min_value = 2023))
    c1, c2 = st.columns(2)
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find elements related to Date
            date_elements = soup.find_all(class_='sidearm-schedule-game-opponent-date flex-item-1')

            Date = []
            for element in date_elements:
                spans_inside_element = element.find_all('span')
                span_text = spans_inside_element[0].text.strip() if spans_inside_element else ''
                if span_text:
                    Date.append(span_text)
                else:
                    second_span_text = spans_inside_element[1].text.strip() if len(spans_inside_element) > 1 else ''
                    Date.append(second_span_text)

            # Find elements related to Location
            location_elements = soup.find_all(class_='x-large-4 hide-on-large-down columns')

            Location = []
            for element in location_elements:
                spans_inside_element = element.find_all('span')
                span_text = spans_inside_element[0].text.strip() if spans_inside_element else ''
                if span_text:
                    Location.append(span_text)
                else:
                    second_span_text = spans_inside_element[1].text.strip() if len(spans_inside_element) > 1 else ''
                    Location.append(second_span_text)


            # Create a DataFrame containing both Date and Location
            df = pd.DataFrame({'Date': Date, 'Location': Location})
            df['Date'] = df['Date'].str.split(' \(').str[0]
        
                
            ## ADD YEAR 
            #'''Because the date from the website do not have year, this is to make every date after december 31st to be input_year+1'''
            
            start_date = datetime.strptime('08-01', '%m-%d')  # August 1st
            end_date = datetime.strptime('12-31', '%m-%d')  # December 31st

            # Convert DataFrame date strings to datetime objects with a default year
            df['Date'] = pd.to_datetime(df['Date'], format="%b %d", errors='coerce').apply(lambda x: x.replace(year=input_year))

            # Replace out-of-range dates with NaT
            for index, row in df.iterrows():
                if not (start_date.replace(year=input_year) <= row['Date'] <= end_date.replace(year=input_year)):
                    df.at[index, 'Date'] += pd.offsets.DateOffset(years=1)

            with c1:
                game_func()
                
                
            ## ESTIMATION TRAVEL PERIOD BASED ON DISTANCE
            df = df[df["Distance in mile"] != 0.0]
            df['Date'] = pd.to_datetime(df['Date'])

            # Sorting the dataframe by Date
            df = df.sort_values('Date').reset_index(drop=True)

            # Initialize a list to store away duration dates
            away_dates = []

            # Calculate away duration based on the updated logic
            for i in range(len(df)):
                current_date = df.loc[i, 'Date']
                departure_date = current_date - timedelta(days=1)
                arrival_date = current_date + timedelta(days=1)

                if df.loc[i, 'Distance in mile'] < 250:
                    away_dates.append(current_date)
                else:
                    if i > 0 and (current_date - df.loc[i - 1, 'Date']).days <= 2:
                        # Check if the previous game was less than 250 miles away
                        if df.loc[i - 1, 'Distance in mile'] < 250:
                            # If it was, don't pop the last date
                            departure_date = current_date - timedelta(days=1)
                        else:
                            # If it wasn't, pop the last date
                            away_dates.pop()
                            departure_date = away_dates.pop()
                    else:
                        # If there are more than 2 days between games, don't pop the last date
                        departure_date = current_date - timedelta(days=1)

                    # Add departure, all dates in between, and arrival to the list
                    for d in pd.date_range(departure_date, arrival_date):
                        away_dates.append(d)

            # Create a dataframe with away duration dates
            days_traveled = pd.DataFrame({'AwayDate': away_dates})
            days_traveled = days_traveled.drop_duplicates().sort_values('AwayDate').reset_index(drop=True)
            
            with c2:
                df=days_traveled
                day_func()
