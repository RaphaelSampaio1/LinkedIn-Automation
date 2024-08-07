from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

class Bot_Likedin:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.site = self.start_chrome()

    def start_chrome(self):
        # Inicialize the Chrome Driver
        option = Options()
        option.add_argument('--start-maximized')
        site = webdriver.Chrome(options=option)
        # Open LinkedIn page
        name_company = input('Input the FULL link of the company : ') # exemple : https://www.linkedin.com/company/folks-la/
        site.get(name_company)
        return site

    def login_acess(self):
        # Locate and click in "Log In" button
        to_enter = self.site.find_element(By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[1]/button')
        to_enter.click()
        # Fill in the email and password fields
        while True:
            try:
                cemail = self.site.find_element(By.XPATH, '//*[@id="base-sign-in-modal_session_key"]')
                cpassword = self.site.find_element(By.XPATH, '//*[@id="base-sign-in-modal_session_password"]')
                cemail.send_keys(self.email)
                cpassword.send_keys(self.password)
                break
            except:
                time.sleep(1)
                print("I'm looking for the login screen")
        # Find and click the login button
        to_enter_tt = self.site.find_element(By.XPATH, '//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button')
        to_enter_tt.click()
        time.sleep(2)

    def mininize(self):
        fator_zoom = 0.5
        self.site.execute_script(f"document.body.style.zoom = '{fator_zoom}';")

    def number_employees(self):
        print('Iniciando ação')
        try:
            # Explicit wait to ensure element is present
            element = WebDriverWait(self.site, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "org-page-navigation__item-anchor") and text()="Pessoas"]')) # If you use in inglish, change the "Pessoas" per "Peoples"
            )
            # Click on the element
            self.site.execute_script("arguments[0].click();", element)
        except Exception as e:
            print(f"Error when clicking on the 'People' element : {e}")

        while True:
            try:
                time.sleep(5.2)
                employees = self.site.find_element(By.XPATH, '//h2[@class="text-heading-xlarge"]')
                if employees.is_displayed():
                    break
                else:
                    print("I didn't find 'People'")
                    break
            except:
                # Scroll down
                time.sleep(1)
                print("I didn't find 'People'")

        # Capturing the employee field
        n_employees = self.site.find_element(By.XPATH, '//h2[@class="text-heading-xlarge"]')
        # Extracting just the number
        n_employees = n_employees.text.split()[0]
        print(f'The number of employees is {n_employees}')

    def url_hashtag(self,hashtag):
        url = f"https://www.linkedin.com/search/results/all/?keywords=%23{hashtag}&origin=GLOBAL_SEARCH_HEADER"
        self.site.get(url)

    def capture_link_peoples(self):
        time.sleep(8)

        # Open more publish


        links = self.site.find_elements(By.XPATH,'//a[contains(@href, "linkedin.com/in/")]')

        unique_hrefs = []
        [unique_hrefs.append(link.get_attribute('href')) for link in links if link.get_attribute('href') not in unique_hrefs]     # capture hrefs of the links with list comprehension 

        with open('linkedIn_profiles.TXT', 'w') as file:     # create a file TXT for write the links
            file.write('\n'.join(unique_hrefs))

        # acess and envite message 

        

    # General activation function
    def main(self): # If you don´t want someone functions, just use '#' before the function
        self.login_acess()
        self.mininize()
        self.url_hashtag('dashboard')
        self.capture_link_peoples()
        # self.number_employees()

# use
bot = Bot_Likedin('raphaelsantos.jan@gmail.com', '24Raphael01.')
bot.main()
input('input [ENTER] to exit')