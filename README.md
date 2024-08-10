# LinkedIn-Automation

This project is an automation developed for LinkedIn, designed to facilitate various tasks on the platform. The main features include:

- **Sending messages** to LinkedIn users.
- **Capturing the number of employees** of a company.
- **Collecting links of multiple user profiles**.
- **Searching posts by specific hashtags**.
- **Make connections with peoples**
These functionalities help you connect with more people, fostering new friendships, knowledge exchange, and even potential job opportunities.

---

## Code Documentation

### Class `Bot_Likedin`

#### `__init__(self, email, password)`
This is the constructor of the `Bot_Likedin` class. It initializes an instance of the bot with the user's email and password to log into LinkedIn. It also calls the `start_chrome()` function to initialize the Chrome browser.

#### `start_chrome(self)`
This function sets up and initializes the Chrome browser using Selenium WebDriver. It prompts the user to input the complete LinkedIn company page URL they want to access and loads that page in the browser.

#### `login_acess(self)`
Logs into the LinkedIn account using the provided email and password. The function attempts to locate and fill in the email and password fields on the LinkedIn login page, clicking the login button to access the account.

#### `mininize(self)`
This function reduces the zoom level of the page where the bot is operating, allowing more content to be displayed on the screen, which can be useful for capturing more elements.

#### `scroll_down(self, number_to_scroll, breathing_time)`
The function scrolls down the page multiple times. `number_to_scroll` specifies how many times to scroll down, and `breathing_time` defines the waiting time in seconds between each scroll.

#### `number_employees(self)`
This function navigates to the "People" tab of the company's LinkedIn page and attempts to capture the number of employees of the company displayed on the page.

#### `url_hashtag(self, hashtag)`
Builds and navigates to a LinkedIn search URL based on a provided hashtag. This is useful for conducting hashtag searches directly on LinkedIn.

### `connection_peoples(self, subject)`
This function automates the process of sending connection requests to LinkedIn users based on a specific subject. It accesses the LinkedIn search results page for the given subject and iterates through the list of users, sending connection requests.

subject: The keyword or topic to search for on LinkedIn. The bot will send connection requests to users who appear in the search results for this keyword.
The function will attempt to connect with a maximum of 50 users. For each user, it clicks the "Connect" button, then sends the request without adding a note. If the "Connect" button is not found, the bot will scroll down the page to load more users and continue the process. If the maximum number of connections is reached or no more connections are available, the process ends.

#### `capture_link_peoples(self)`
Collects all profile links of users displayed on the current LinkedIn page and stores them in a text file named `linkedIn_profiles.TXT`. This function should be run before attempting to send messages, as it gathers the list of profile links to be used later.

#### `view_all_results(self)`
Looks for and clicks the "See all posts results" button on the LinkedIn page to expand and load more search results.

#### `send_message(self)`
This function reads the profile URLs from the `linkedIn_profiles.TXT` file, accesses each profile, and sends a personalized message to each person. The message is customized with the recipient's first name and includes an invitation to stay in touch.

**Note:** To run the message-sending bot, you must first execute the functions that gather profile links. Start by running `self.capture_link_peoples()` to store all profile links in the `linkedIn_profiles.TXT` file. Only after gathering these links should you proceed to run `send_message()` to ensure that the bot has the necessary data to send messages.

#### `main(self)`
The main function that coordinates the execution of the other functions in the `Bot_Likedin` class. Here, you can select which functions to run by commenting or uncommenting the calls within this function.

### Example of Usage
```python
bot = Bot_Likedin('your_email@gmail.com', 'your_password')
bot.main()
input('input [ENTER] to exit')
