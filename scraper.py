import csv
import os
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from config import USERNAME, PASSWORD, DEVELOPMENT_TESTING, HEADLESS_MODE
import time

class CongaIdeasScraper:
    def __init__(self):
        chrome_options = Options()
        if HEADLESS_MODE:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)

    def get_ideas(self):
        if self._login():
            if self._close_popups():
                index_file = "reports/index.csv"
                if os.path.exists(index_file):
                    self._log(f"Using existing index file: {index_file}")
                    all_ideas = self._scrape_all_ideas()
                else:
                    self._log(f"Index file not found. Scraping idea links.")
                    self._scrape_idea_links()
                    all_ideas = self._scrape_all_ideas()

                categorized_ideas = self._categorize_ideas_by_project(all_ideas)
                os.makedirs("reports/ideas-data", exist_ok=True)
                for project_name, project_ideas in categorized_ideas.items():
                    project_file = f"reports/ideas-data/{project_name}_ideas.json"
                    self._save_ideas_to_json(project_ideas, project_file)

                self.driver.quit()  # Close the browser after scraping
                return categorized_ideas
            else:
                self._log("Failed to close popups. Aborting scraping.")
        else:
            self._log("Login failed. Aborting scraping.")

        self.driver.quit()
        return {}

    def _login(self):
        self._log("Navigating to the ideas list page...")
        self.driver.get("https://community.conga.com/s/ideaslist")

        self._log("Entering login credentials...")
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.send_keys(USERNAME)

        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        password_input.submit()

        # Wait for the ideas page to load
        if not self._wait_for_page_load():
            self._log("Login page load timeout. Aborting login.")
            return False

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
            self._log("Main popup closed.")
        except:
            self._log("Main popup not found or already closed.")

        try:
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_button.click()
            self._log("Cookies accepted.")
        except:
            self._log("Cookies agreement not found or already accepted.")

        if "ideas" in self.driver.current_url:
            self._log("Popups closed successfully.")
            return True
        else:
            self._log("Failed to close popups.")
            return False




    def _scrape_idea_links(self):
        index_file = "reports/index.csv"
        fieldnames = ["url", "title", "product", "author", "votes"]

        if os.path.exists(index_file):
            self._log(f"Using existing index file: {index_file}")
            with open(index_file, "r") as file:
                reader = csv.DictReader(file)
                existing_urls = [row["url"] for row in reader]
        else:
            self._log(f"Creating new index file: {index_file}")
            existing_urls = []

        current_page = 1
        new_ideas = []

        while True:
            self._log(f"Scraping idea links from page {current_page}...")
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            idea_elements = soup.select('.slds-grid.slds-grid_vertical.perRowCss.slds-container_fluid')

            for idea_element in idea_elements:
                url_element = idea_element.select_one('.rowTitle')
                url = f"https://community.conga.com/s/ideadetail?id={url_element['data-value']}"
                if url not in existing_urls:
                    title = url_element.text.strip()
                    product_element = idea_element.select_one('.ideaStatus')
                    product = product_element.text.strip() if product_element else ""
                    author_element = idea_element.select_one('.userName')
                    author = author_element.text.strip() if author_element else ""
                    votes_element = idea_element.select_one('.noOfVotes')
                    votes = votes_element.text.strip() if votes_element else ""

                    idea_data = {
                        "url": url,
                        "title": title,
                        "product": product,
                        "author": author,
                        "votes": votes
                    }
                    new_ideas.append(idea_data)

            with open(index_file, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerows(new_ideas)

            self._log(f"Scraped links added to {index_file}")

            new_ideas = []

            try:
                last_page_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'slds-p-right_x-small')]/a")
                last_page = int(last_page_element.get_attribute('data-value'))

                if current_page < last_page and (not DEVELOPMENT_TESTING or current_page < 1):
                    next_button = self.driver.find_element(By.XPATH, "//a[@class='nextPage']")
                    next_button.click()
                    # Wait for the next page to load
                    if not self._wait_for_page_load():
                        self._log("Next page load timeout. Proceeding with partial data.")
                        break
                    current_page += 1
                else:
                    break
            except Exception as e:
                self._log(f"Error occurred while navigating to the next page: {str(e)}. Proceeding with partial data.")
                break



    def _scrape_idea_details(self, idea_url):
        self._log(f"Navigating to idea: {idea_url}")

        try:
            self.driver.get(idea_url)

            # Wait for the idea details page to load and the title to be present
            title = ""
            max_attempts = 10
            attempts = 0
            while not title and attempts < max_attempts:
                idea_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                title_element = idea_soup.select_one('.rowTitle')
                title = title_element.text.strip() if title_element else ""
                if not title:
                    time.sleep(1)  # Wait for a short interval before checking again
                attempts += 1

            if not title:
                raise TimeoutException("Idea details page load timeout.")

            self._log("Parsing idea details page source with BeautifulSoup...")


            author_element = idea_soup.select_one('a.UserPage')
            author = author_element.text.strip() if author_element else ""

            product_element = idea_soup.select_one('span.wordBreak')
            product = product_element.get('data-value', '').strip() if product_element else ""
            # Replace offending characters with underscores in the product name
            product = re.sub(r'[\s\-/\\]', '_', product)

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
                'product': product,
                'content': content,
                'votes': votes,
                'comments': comments
            }


            # Save the idea data to the corresponding project's JSON file
            os.makedirs("reports/ideas-data", exist_ok=True)
            project_file = f"reports/ideas-data/{product}_ideas.json"
            
            if os.path.exists(project_file):
                with open(project_file, "r") as file:
                    project_ideas = json.load(file)
            else:
                project_ideas = []

            # Check if the idea title already exists in the project ideas
            existing_titles = [idea['title'] for idea in project_ideas]
            if title not in existing_titles:
                project_ideas.append(idea_data)

            with open(project_file, "w") as file:
                json.dump(project_ideas, file, indent=2)

            return idea_data
        except TimeoutException:
            self._log(f"Skipping idea {idea_url} due to timeout.")
            return None


    def _scrape_all_ideas(self):
        ideas_file = "reports/ideas-data/ideas.json"
        
        if os.path.exists(ideas_file):
            self._log(f"Using existing ideas file: {ideas_file}")
            with open(ideas_file, "r") as file:
                all_ideas = json.load(file)
        else:
            self._log(f"Ideas file not found. Scraping idea details.")
            all_ideas = []

            with open("reports/index.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    idea_url = row["url"]
                    idea_data = self._scrape_idea_details(idea_url)
                    if idea_data is not None:
                        all_ideas.append(idea_data)

            os.makedirs("reports/ideas-data", exist_ok=True)
            self._save_ideas_to_json(all_ideas, ideas_file)

        return all_ideas



    
    def _categorize_ideas_by_project(self, ideas):
        categorized_ideas = {}
        for idea in ideas:
            if idea is not None:
                project_name = idea.get("product", "Unknown")
                if project_name not in categorized_ideas:
                    categorized_ideas[project_name] = []
                categorized_ideas[project_name].append(idea)
        return categorized_ideas




    def _wait_for_page_load(self, timeout=10, check_interval=1):
        max_attempts = timeout // check_interval
        attempts = 0
        while attempts < max_attempts:
            page_loaded = self.driver.execute_script("return document.readyState == 'complete';")
            if page_loaded:
                return True
            time.sleep(check_interval)
            attempts += 1
        return False


    def _save_ideas_to_json(self, ideas, filename):
        with open(filename, "w") as file:
            json.dump(ideas, file, indent=2)
        self._log(f"Ideas saved to {filename}")


    def _log(self, message):
        print(f"[LOGGING] {message}")

