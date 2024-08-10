from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time


class Bot_Likedin:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.site = self.start_chrome()

    def custom_print(self,value):
            tam = len(value) + 1
            print('\n')
            print('-' * tam)
            print(f'\033[1m{value}')
            print('-' * tam)

    def start_chrome(self):
        # Inicialize the Chrome Driver
        option = Options()
        option.add_argument('--start-maximized')
        site = webdriver.Chrome(options=option)
        # Open LinkedIn page
        name_company = 'https://www.linkedin.com/company/folks-la/' # exemple of company, just to start the login
        site.get(name_company)
        self.custom_print('Website accessed')
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
                self.custom_print('Written Email')
                cpassword.send_keys(self.password)
                self.custom_print('Written Password')
                break
            except:
                time.sleep(1)
                print("I'm looking for the login screen")
        # Find and click the login button
        to_enter_tt = self.site.find_element(By.XPATH, '//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button')
        to_enter_tt.click()
        self.custom_print('Entering...')
        time.sleep(2)

    def mininize(self):
        fator_zoom = 0.5
        self.site.execute_script(f"document.body.style.zoom = '{fator_zoom}';")
        self.custom_print('Minimized screen')

    def scroll_down(self, number_to_scroll, breathing_time):
        n = 0
        for _ in range(number_to_scroll):
            # Scroll the page down to the bottom of the visible content
            self.site.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            # Wait seconds before scrolling again
            time.sleep(breathing_time)
            n +=1
            self.custom_print(f'Scroll Down {n} time')

    def number_employees(self):
        print('Starting action')
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
        self.custom_print('Entering in the hashtag URL...')

    
    def connection_peoples(self,subject):
        # acess the url
        url = f'https://www.linkedin.com/search/results/people/?keywords={subject}&origin=SWITCH_SEARCH_VERTICAL&searchId=23d3caca-af27-400c-a975-130437f3b353&sid=7z8'
        self.site.get(url)
        self.custom_print('Entering in the subject URL...')

        n_max = 50
        n = 0
        while n < n_max:  # Do connection
            try:
                time.sleep(7)
                connection = self.site.find_element(By.XPATH, "//button/span[text()='Conectar']")
                if connection:
                    connection.click()
                    time.sleep(1.7)

                    # Send without note
                    try:
                        without_note = self.site.find_element(By.XPATH, '//button[@aria-label="Enviar sem nota"]')
                        if without_note:
                            without_note.click()
                            n += 1
                            self.custom_print(f'Done {n} connections')
                    except NoSuchElementException:
                        print('Send without note button not found')
                        continue  # Proceed with the next iteration

            except (NoSuchElementException, ElementClickInterceptedException) as e:
                print(f'Connection button not found or clickable: {str(e)}')
                self.scroll_down(3, 0.5)

                # Navigate to next page
                try:
                    next_page = self.site.find_element(By.XPATH, '//button[@aria-label="Avançar"]')
                    if next_page:
                        next_page.click()
                        time.sleep(2)
                except NoSuchElementException:
                    print('Next page button not found or no more pages')
                    break

                time.sleep(3)

        print('Reached maximum connections or no more connections available')


    def capture_link_peoples(self):
        time.sleep(6)
        links = self.site.find_elements(By.XPATH,'//a[contains(@href, "linkedin.com/in/")]')
        self.custom_print("Wait, i'm capturing the links")
        unique_hrefs = []
        [unique_hrefs.append(link.get_attribute('href')) for link in links if link.get_attribute('href') not in unique_hrefs]     # capture hrefs of the links with list comprehension 


        with open('linkedIn_profiles.TXT', 'w') as file:     # create a file TXT for write the links
            file.write('\n'.join(unique_hrefs))
        print('TXT File created\n')
        time.sleep(5)

    def view_all_results(self):
        while True:
            try:
                button = self.site.find_element(By.XPATH,"//a[contains(text(),'Ver todos os resultados de publicações')]") # if you are in inglish, change the words of the "contains"
                if button:
                    button.click()
                    self.custom_print('Click to view more posts')
                    time.sleep(5)
                    break
                else:
                    self.scroll_down(1)
            except:
                time.sleep(1)
                print('More Results not found still')

    def send_message(self):  # To change the message, edit within this function
        # Read URLs from the file
        with open('linkedIn_profiles.TXT', 'r') as file:
            urls = file.readlines()
        
        # Iterate over each URL
        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespace
            
            # Open the LinkedIn profile
            self.site.get(url)
            time.sleep(5)  # Wait for the page to load
            self.custom_print('Open linkedIn profile')

            try:
                # Name of the people
                name_element = self.site.find_element(By.XPATH, "//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']")
                full_name = name_element.text
                first_name = full_name.split()[0]
                self.custom_print('Name coleted')

                # Find and click the 'Connect' button
                connect = self.site.find_element(By.XPATH, '//button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action"]')  
                time.sleep(2)
                if connect:
                    connect.click()
                    self.custom_print('Connection sent')
                    time.sleep(2)  # Wait for the connection modal to appear

                    # Check if 'Add a note' option is available
                    with_note = self.site.find_element(By.XPATH, '//button[@aria-label="Adicionar nota"]')
                    with_note.click()
                    time.sleep(1.5)

                    # Create and send the message
                    your_name = '' # Fill with your name
                    knowledge = '' # Fill with your knowlegde
                    # Don´t can pass of 200 words
                    message = f"""
    Olá {first_name}!
    Me chamo {your_name} e estou estudando sobre {knowledge}. Vi seu perfil e me interessei pelos posts!
    Vamos manter contato para compartilharmos conhecimento!
    """
                    message_field = self.site.find_element(By.XPATH, '//textarea[@id="custom-message"]')
                    message_field.send_keys(message)
                    time.sleep(5)
                    send = self.site.find_element(By.XPATH, '//button[@aria-label="Enviar convite"]')
                    send.click()
                    self.custom_print('Message sent')
                    time.sleep(5)
                else:
                    print(f"Connect button not found for {url}")

            except Exception as e:
                print(f"Error sending message to {url}: {e}")

    # General activation function
    def main(self): # If you don´t want someone functions, just use '#' before the function
        self.login_acess()
        self.mininize()
        # self.url_hashtag('dashboard')
        self.connection_peoples('python')
        # self.view_all_results()
        # self.scroll_down(30, 5) 
        # self.capture_link_peoples()
        # self.send_message()
        # self.number_employees()

# use
bot = Bot_Likedin('YourEmail.com', 'YourPassoword')
bot.main()
input('input [ENTER] to exit')
