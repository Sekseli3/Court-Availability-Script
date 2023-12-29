# Tennis Court Availability Checker

This Python script allows you to check the availability of tennis courts without having to manually open and navigate the website. It uses web scraping to automatically retrieve and display the available time slots for each court. Court availability can be checked from Targa-Arena(Kauniainen, Grani), Tali and Taivallahti and Meilahti. The place you want to check the availability for can be changed
with command-line parameters (Default is Tali). Additionally, the day you want to check the availability for can be changed with command-line paramenters(Default is for today).

## How it Works

The script uses Selenium WebDriver to interact with the website in the background. It navigates to the page with the court schedules, extracts the available time slots, and prints them in a structured format.

The main function, `getTimes(courts)`, takes a list of courts and prints the available time slots for each court. If no courts are available, it prints a message to indicate this.

The script begins by parsing command line arguments, which can be used to specify the number of days ahead to check for court availability. It then constructs the URL of the page to scrape based on these arguments.

The script uses Selenium to open a browser window in the background, navigate to the specified URL, and wait for the page to load. It then finds the table that contains the court schedules and extracts its contents.

The extracted data is a list of strings, each representing a row in the table. The script processes this list to extract the court names and available time slots. It then sorts the courts and prints the available times for each one.

## Dependencies

This script requires the following Python packages:

- Selenium: For automating web browser interaction from Python.
- datetime: For working with dates and times.

You can install these packages using pip:
pip install selenium

## Usage
To run the script, use the following command:

python tennis_court_availability.py

You can specify the number of days ahead to check for court availability using the --days argument and the place using --place. For example, to check availability 3 days from now in Meilahti use:

python tennis_court_availability.py --days 3 --place Meilahti

--days is limited to the number of days the website can be navigated to and --place is limited to Kauniainen, Tali, Taivallahti, Meilahti

## Output 
Output looks something like this on 29.12.2023
Available courts on January 02 are:

Taivis1:
available from 22:30 to 23:00

Taivis2:
available from 22:30 to 23:00

Taivis3:
available from 21:30 to 22:00
available from 22:00 to 23:00

Taivis4:
available from 6:30 to 07:00
available from 22:00 to 23:00

Taivis5:
available from 6:30 to 07:00
available from 8:30 to 09:00
available from 11:00 to 12:00
available from 22:00 to 23:00

Taivis6:
available from 6:30 to 07:00
available from 7:00 to 08:00
available from 22:00 to 23:00

with command:

python tennis_court_availability.py --days 4 --place Taivallahti
