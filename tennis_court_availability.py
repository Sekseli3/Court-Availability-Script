from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import datetime
import argparse
import json

def parse_arguments():
    #Parse command line arguments
    parser = argparse.ArgumentParser(description="Check tennis court availability")
    parser.add_argument('--days', type=int, default=0, help='Check for how many days in advance')
    parser.add_argument('--place', type=str, default='Tali', help='Place to check for availability')
    parser.add_argument('--browser', type=str, default='safari', help='Select browser to use safare or chrome')
    return parser.parse_args()

def get_Place(driver,place):
    #On some of tge websites a button has to be pressed to get to the correct page
    if place == 'Taivallahti':
        #Taivallahti and Tali operate on the same website, but a button moving user to taivallahti courts has to be pressed
        target_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div#root > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > button:nth-of-type(2)')))
        target_element.click()
        #Meilahti has indoor and bubble courts, but only bubble courts offer student prices so only check those courts, again button needs to be pressed
    elif place == 'Meikku' or place == 'Meilahti':
        target_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div#root > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div > button:nth-of-type(3)')))
        target_element.click()

#Function to extract the court times
def extract_court_times(data,court):
    court_times = []
    current_court = court
    for entry in data:
        if entry:
            if entry.startswith('K-'):
                # If the entry starts with 'K-', update the current court
                current_court = entry
            else:
                # Otherwise, consider it as a time slot and append it to the result
                start_time = entry.split('Varaa')[0].strip()
                end_time = f"{int(start_time.split(':')[0]) + 1:02d}:00"
                court_times.append(f"{current_court} is available from {start_time} to {end_time}")
    return court_times

#Function to scrape the website
def check_tennis_court_availability(url, browser, days=0, place='Tali'):
    # Create a new instance of the driver
    driver = None
    if browser == 'chrome':
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Safari()
    #wait for the page to load. With smaller times doesn't always work
    driver.implicitly_wait(15)
    # Navigate to the URL
    driver.get(url)
    
    #Get the correct page
    get_Place(driver,place)

    try:
        #Move to the desired day according to the given parameter days
        if days > 0:
            i = 0
            while i < days:
                target_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div#root > div > div:nth-of-type(2) > div > div > button:nth-of-type(2)')))
                target_element.click()
                i += 1
        # Click button on website to show the available times
        target_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div#root > div > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2)'))
        )
        # Click it 
        if target_element:
            target_element.click()

        # Wait for the table containing court availability information
        table = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div#root > div > div:nth-of-type(2) > div:nth-of-type(4) > div > div > table > tbody'))
        )
        #Get all the rows including information about the courts
        rows = table.find_elements(By.TAG_NAME, "tr")

        #I made a retry mechanism in case a web elemt is detached form the current DOM,
        #that selenium is interacting with. Withou this, the program would crash sometimes
        MAX_RETRIES = 3
        # Extracted information
        availability_info = []
        for row in rows:
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    #Get the number of the court
                    K = row.find_elements(By.TAG_NAME, "th")
                    #Get the times when the court is available
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        court = K[0].text.strip()
                        times_data = [cell.text for cell in cells]
                        court_times = extract_court_times(times_data,court)
                        availability_info.extend(court_times)
                    break
                except StaleElementReferenceException:
                    retries += 1
        return availability_info
    
    except Exception as e:
        # The element is not found, meaning website down or could not load
        print("No available courts D:")
        return None
    finally:
        # Close the browser window
        driver.quit()

def getTimes(courts):
    date = datetime.datetime.now()
    current_date = date + datetime.timedelta(days=args.days)
    if courts:
        print(f"Available courts on {current_date.strftime('%B %d')} are:")
        # For some reason courts in Tali(start with K-) are not sorted on the website, so sort them here
        if courts[0].startswith('K-'):
            courts = sorted(courts, key=lambda court: int(court.split('-')[1].split(' ')[0]))
        current_court = None
        for court in courts:
            court_name, time_slot = court.split(' is available from ')
            if court_name != current_court:
                current_court = court_name
                print(f"\n{current_court}:")
            print(f"available from {time_slot}")
    else:
        #If no courts available, print this
        return ["No available courts"]

if __name__ == "__main__":
    #Parse the arguments
    args = parse_arguments()
    # URL of site to scrape
    if args.place == 'Tali' or args.place == 'Taivallahti':
        tennis_court_url = 'https://talitaivallahti.feel.cintoia.com'
    elif args.place == 'Grani' or args.place == 'Kauniainen':
        tennis_court_url = 'https://targaarena.cintoia.com'
    elif args.place == 'Meilahti' or args.place == 'Meikku':
        tennis_court_url = 'https://meilahdenliikuntakeskus.cintoia.com'
    


    # Get the courts
    courts = check_tennis_court_availability(tennis_court_url, args.browser, args.days, args.place)

    # Extract the times
    getTimes(courts)
