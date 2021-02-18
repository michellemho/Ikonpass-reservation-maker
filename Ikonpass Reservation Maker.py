## Ikon Pass reservation maker bot

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import date
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(4)

email = input("Email: ")
password = input("Password: ")
resort = input("Resort: ")
friends_and_fam = input("Use friends and family pass? (Yes or No): ")
day_number = int(input("Day: "))
month_number = int(input("Month: "))

if friends_and_fam == "Yes":
    friends_and_fam = True
else:
    friends_and_fam = False
    
day_xpath = "//*[text()='" + str(day_number) + "']"

right_arrow_clicks = month_number - int(str(date.today())[5:7])

driver.get('https://account.ikonpass.com/en/login')

cookie_button = driver.find_element_by_xpath('/html/body/div[2]/div/a')
cookie_button.click()

email_field = driver.find_element_by_id("email")
email_field.clear()
email_field.send_keys(email)

password_field = driver.find_element_by_id("sign-in-password")
password_field.clear()
password_field.send_keys(password)
password_field.submit()

time.sleep(3)

driver.get('https://account.ikonpass.com/myaccount/add-reservations/')

need_reservation = True
tries = 1

while need_reservation:
    search_bar = driver.find_element_by_css_selector('input[placeholder="Search"]')
    search_bar.send_keys(resort)

    crystal_mountain = driver.find_element_by_id("react-autowhatever-resort-picker-section-0-item-0")
    crystal_mountain.click()

    time.sleep(5)
    
    continue_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[2]/div[2]/button')
    continue_button.click()

    for i in range(right_arrow_clicks):
        right_arrow = driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/button[2]')
        right_arrow.click()

    day = driver.find_element_by_xpath(day_xpath)
    day.click()

    try:
        # Look for all checkboxes on the screen
        checkboxes = driver.find_elements_by_css_selector("input[type='checkbox']")
        for checkbox in checkboxes:
            # The account that is signed in has checkbox already default checked
            if not checkbox.is_selected():
                # Click checkboxes for all other linked family accounts
                checkbox.click()
        save_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[2]/div/div[3]/button[1]')
        need_reservation = False
        
    except NoSuchElementException:
        driver.refresh()
        tries += 1
        print(tries)
        time.sleep(10)

if friends_and_fam:
    time.sleep(5)
    checkbox = driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[3]/div[1]/div[2]/div/div[3]/label[1]/input')
    checkbox.click
    time.sleep(5)

save_button.click()

time.sleep(5)

continue_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[3]/div[2]/button')
continue_button.click()

time.sleep(5)

checkbox = driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[4]/div/div[4]/label/input')
checkbox.click()

time.sleep(5)

confirm_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/main/section[2]/div/div[2]/div[4]/div/div[5]/button')
confirm_button.click()

print("it took ",tries," tries to complete your reservation")

