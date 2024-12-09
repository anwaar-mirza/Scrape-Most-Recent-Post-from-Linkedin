import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dateutil.relativedelta import relativedelta
from fake_useragent import UserAgent
from datetime import datetime
import pandas as pd
import pickle as pk
import random
import time
import os
import csv
import re



class LinkedinMostRecentPostScrape:
    def __init__(self):
        self.ua = UserAgent()
        self.option = Options()
        self.option.add_argument(f"user-agent={self.ua.random}")
        self.option.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()) ,options=self.option)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        self.action = ActionChains(self.driver)
        self.driver.get("https://www.linkedin.com/login")
        self.driver.implicitly_wait(5)
        with open("cookies.pkl", "rb") as file:
            cookies = pk.load(file)
            for c in cookies:
                self.driver.add_cookie(c)
        self.driver.refresh()

    def date_process(self, date):
        now = datetime.now()
        if "h" in date or "H" in date:
            return datetime.now().date()
        elif "d" in date or "D" in date:
            date = re.sub(r"[^0-9]", "", date)
            final_date = now - relativedelta(days=int(date))
            return final_date.date()
        elif "mo" in date or "MO" in date or "Mo" in date:
            date = re.sub(r"[^0-9]", "", date)
            final_date = now - relativedelta(months=int(date))
            return final_date.date()
        elif "w" in date or "W" in date:
            date = re.sub(r"[^0-9]", "", date)
            final_date = now - relativedelta(weeks=int(date))
            return final_date.date()
        elif "y" in date or "Y" in date:
            date = re.sub(r"[^0-9]", "", date)
            final_date = now - relativedelta(years=int(date))
            return final_date.date()

    def land_on_target_url(self, target_url):
        self.driver.get(target_url)
        self.driver.implicitly_wait(3)
        self.driver.execute_script("document.body.style.zoom='33%'")

    def click_on_post_button(self):
        try:
            post_btn = self.driver.find_element(By.XPATH, '//a[text()="Posts"]')
            self.driver.implicitly_wait(5)
            self.action.click(post_btn).perform()
        except:
            print("Failed to click on post button")

    def get_most_recent_post(self, num):
        post = {}
        try:
            # get first post box
            post_box = self.driver.find_element(By.XPATH, '//div[@class="fie-impression-container"]')
            self.driver.implicitly_wait(3)
            post_wait = WebDriverWait(post_box, 10)
            # post by
            try:
                post_by = post_wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "update-components-actor__title")]/span/span/span/span'))).text
                post['Posted By'] = post_by.split("\n")[0]
            except:
                post['Posted By'] = ""
                print("Post By Not Found")

            # get Total Followers
            try:
                followers = post_wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "update-components-actor__description")]/span[not(contains(@class, "visually-hidden")) and contains(text(), "follower")]'))).text
                post['Followers'] = followers
            except:
                post['Followers'] = ""
                print("Followers Not Found")

            # post time
            try:
                post_time = post_wait.until(EC.presence_of_element_located((By.XPATH, './/a[contains(@class, "update-components-actor__sub-description-link")]/span/span'))).text
                post['Posted On'] = self.date_process(post_time.strip())
            except Exception as e:
                post['Posted On'] = ""
                print(e)
                print("Post Time Not Found")

            # get post description
            try:
                # more btn if available
                try:
                    more = post_wait.until(EC.element_to_be_clickable((By.XPATH, './/button[span[contains(text(), "…more")]]')))
                    self.action.click(more).perform()
                    time.sleep(random.randrange(1, 3))
                except:
                    print("Post description has no more button")

                # lets get description
                try:
                    post_description = post_box.find_element(By.XPATH, './/div[contains(@class, "update-components-text")]//span[@dir="ltr"]').text
                    post_description = re.sub(r'[^\x00-\x7F]+', '', post_description)
                    self.driver.implicitly_wait(3)
                    post['Description'] = post_description.strip()
                except:
                    try:
                        post_description = post_box.find_element(By.XPATH, './/div[contains(@class, "update-components-text")]//span[@dir="ltr"]').text
                        post_description = re.sub(r'[^\x00-\x7F]+', '', post_description)
                        self.driver.implicitly_wait(3)
                        post['Description'] = post_description.strip()
                    except Exception as e:
                        post['Description'] = ""
                        print(e)
                        print("Post Description Not Found")
            except:
                print("Issue in Description")

            time.sleep(random.randrange(1, 5))
            if num == 1:
                try:
                    like = post_wait.until(EC.presence_of_element_located((By.XPATH, './/button[contains(@class, "social-actions-button") and @aria-label="React Like"]')))
                    self.action.click(like).perform()
                    time.sleep(random.randrange(1, 4))
                except:
                    print("Fail to like")
            elif num == 2:
                try:
                    comment = post_wait.until(EC.presence_of_element_located((By.XPATH, './/button[contains(@class, "social-actions-button") and @aria-label="Comment"]')))
                    self.action.click(comment).perform()
                    time.sleep(random.randrange(1, 4))
                except:
                    print("Fail to comment")
            elif num == 3:
                try:
                    total_likes = post_wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "social-details-social-counts__reactions-count")]')))
                    self.action.click(total_likes).perform()
                    time.sleep(random.randrange(1, 4))
                except:
                    print("Fail to open")
            elif num == 4:
                try:
                    three_dot = post_wait.until(EC.presence_of_element_located((By.XPATH, './/button[contains(@aria-label, "Open control menu for")]')))
                    self.action.click(three_dot).perform()
                    time.sleep(random.randrange(1, 3))
                except:
                    print("Failed to click 3 dots")
            else:
                print("Invalid Choice")

            # move data into file
            post['Profile Url'] = self.driver.current_url.strip()
            if post['Posted By'] !="":
                for k, v in post.items():
                    print(k,": ",v)
                p = pd.DataFrame([post])
                p.to_csv("test.csv", mode='a', header=not os.path.exists("test.csv"), index=False)
            else:
                pass

        except:
            print("Action Stop")

    def get_remaining_links(self, index, link):
        file_path = os.path.join(os.getcwd(), "remaining_links.csv")
        columns = ["Index", "Company Linkedin Url"]
        if not os.path.exists(file_path):
            with open(file_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                for i, j in zip(index, link):
                    writer.writerow([i, j])
        else:
            os.remove(file_path)
            with open(file_path, mode='a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                for i, j in zip(index, link):
                    writer.writerow([i, j])
    
    def quit_the_driver(self):
        try:
            try:
                self.driver.quit()
            except:
                self.driver.quit()
            print("Driver quite Successfully, Please Wait 5 minutes to initializing new driver")
        except Exception as e:
            print(f"Error while quitting driver: {e}")
    
    def __del__(self):
        print("Cleanup called via __del__")

error_occurred = False
index = []
links = []
bot = LinkedinMostRecentPostScrape()
with open(r"remaining_links.csv", mode="r", encoding="utf-8", errors="replace") as file:
    reader = csv.DictReader(file)
    for i, r in enumerate(reader, start=1):
        updated_url = r['Company Linkedin Url'].split("/posts/")[0] if "/posts/" in r['Company Linkedin Url'] else r['Company Linkedin Url']
        if error_occurred:
            index.append(i)
            links.append(updated_url)
            continue
        
        try:
            if i % 100 == 0:
                print(f"Processing URL: {updated_url}")
                bot.land_on_target_url(updated_url.strip()+"/posts/")
                bot.get_most_recent_post(random.randrange(1, 5))
                time.sleep(5)
                bot.quit_the_driver()
                bot.__del__()
                time.sleep(300)
                bot = LinkedinMostRecentPostScrape()
                print("Driver reinitialized.")
            else:
                bot.land_on_target_url(updated_url.strip()+"/posts/")
                bot.get_most_recent_post(random.randrange(1, 5))
                print(f"Scraped: {updated_url}"+"/posts/")
        except:
            error_occurred = True

file.close()

try:
    bot.get_remaining_links(index, links)
    index.clear()
    links.clear()
except:
    print("Issue with get_remaining_links()")