from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from config import USERNAME, PASSWORD, PAGE_DELAY, IDEA_DELAY, DEVELOPMENT_TESTING, HEADLESS_MODE

class CongaIdeasScraper:
    def __init__(self):
        chrome_options = Options()
        if HEADLESS_MODE:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)

    def get_ideas(self):
        if self._login():
            time.sleep(3)
            if self._close_popups():
                all_ideas = self._scrape_all_ideas()
                self.driver.quit() # Close the browser after scraping
                return all_ideas
            else:
                self._log("Failed to close popups. Aborting scraping.")
        else:
            self._log("Login failed. Aborting scraping.")

        self.driver.quit()
        return []

    def _login(self):
        self._log("Navigating to the ideas list page...")
        self.driver.get("https://community.conga.com/s/ideaslist")
        time.sleep(PAGE_DELAY)

        self._log("Entering login credentials...")
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.send_keys(USERNAME)

        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        password_input.submit()
        time.sleep(PAGE_DELAY)

        if "ideas" in self.driver.current_url:
            self._log("Login successful.")
            return True
        else:
            self._log("Login failed.")
            return False

    def _close_popups(self):
        try:
            close_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".slds-modal__close"))
            )
            close_button.click()
            time.sleep(1)
            self._log("Main popup closed.")
        except:
            self._log("Main popup not found or already closed.")

        try:
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_button.click()
            time.sleep(1)
            self._log("Cookies accepted.")
        except:
            self._log("Cookies agreement not found or already accepted.")

        if "ideas" in self.driver.current_url:
            self._log("Popups closed successfully.")
            return True
        else:
            self._log("Failed to close popups.")
            return False

    def _get_idea_links(self):
        idea_links = []
        current_page = 1

        while True:
            self._log(f"Scraping idea links from page {current_page}...")
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            idea_elements = soup.select('.rowTitle')

            for idea_element in idea_elements:
                idea_link = idea_element['data-value']
                idea_links.append(idea_link)

            last_page_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'slds-p-right_x-small')]/a")
            last_page = int(last_page_element.get_attribute('data-value'))

            if current_page < last_page and (not DEVELOPMENT_TESTING or current_page < 1):
                next_button = self.driver.find_element(By.XPATH, "//a[@class='nextPage']")
                next_button.click()
                time.sleep(PAGE_DELAY)
                current_page += 1
            else:
                break

        self._log(f"Found {len(idea_links)} idea links.")
        return idea_links

    def _scrape_idea_details(self, idea_link):
        idea_url = f"https://community.conga.com/s/ideadetail?id={idea_link}"
        self._log(f"Navigating to idea: {idea_url}")
        self.driver.get(idea_url)
        time.sleep(IDEA_DELAY)

        self._log("Parsing idea details page source with BeautifulSoup...")
        idea_soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        title_element = idea_soup.select_one('.rowTitle')
        title = title_element.text.strip() if title_element else ""

        author_element = idea_soup.select_one('.userName')
        author = author_element.text.strip() if author_element else ""

        content_element = idea_soup.select_one('.bodyText')
        content = content_element.text.strip() if content_element else ""

        votes_element = idea_soup.select_one('div.slds-p-top_x-small.slds-p-horizontal_small')
        votes = votes_element.text.strip() if votes_element else ""

        comments = []
        comment_elements = idea_soup.select('.commentBox')
        seen_comments = set()
        for comment_element in comment_elements:
            commenter_element = comment_element.select_one('a[style*="font-weight: bold"]')
            commenter = commenter_element.text.strip() if commenter_element else ""

            comment_content_element = comment_element.select_one('lightning-formatted-rich-text')
            comment_content = comment_content_element.text.strip() if comment_content_element else ""

            comment_key = (commenter, comment_content)
            if comment_key not in seen_comments:
                comments.append({
                    'commenter': commenter,
                    'content': comment_content
                })
                seen_comments.add(comment_key)

        idea_data = {
            'title': title,
            'author': author,
            'content': content,
            'votes': votes,
            'comments': comments
        }

        return idea_data

    def _scrape_all_ideas(self):
        all_ideas = []
        idea_links = self._get_idea_links()

        for idea_link in idea_links:
            idea_data = self._scrape_idea_details(idea_link)
            all_ideas.append(idea_data)

        return all_ideas

    def _log(self, message):
        print(f"[LOGGING] {message}")

