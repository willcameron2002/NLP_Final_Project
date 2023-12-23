from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

class Scraper:
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options = options)
        



    def scrape(self, search_term, start_date, end_date, suspicious_activity, your_username, your_password, your_email, your_path):
        
        self.driver.get('https://twitter.com')
        #self.driver.maximize_window()
        time.sleep(2)

        buttons = self.driver.find_elements(By.XPATH, "//a[@role='link']")
        buttons[4].click()
        time.sleep(1.5)

        username = self.driver.find_element(By.TAG_NAME, "input")
        username.send_keys(your_email)
        time.sleep(1.5)

        buttons = self.driver.find_elements(By.XPATH, "//div[@role='button']")
        self.driver.execute_script("arguments[0].click();", buttons[2])
        time.sleep(1.5)

        if suspicious_activity == 'Y':

            self.driver.find_element(By.TAG_NAME, "input").send_keys(your_username)
            time.sleep(1.5)

            buttons = self.driver.find_elements(By.XPATH, "//div[@style='color: rgb(15, 20, 25); text-overflow: unset;']")
            buttons[0].click()
            time.sleep(1.5)

        password = self.driver.find_element(By.XPATH, "//input[@type='password']")
        password.send_keys(your_password)
        time.sleep(1.5)

        buttons = self.driver.find_elements(By.XPATH, "//div[@style='color: rgb(15, 20, 25); text-overflow: unset;']")
        buttons[0].click()
        time.sleep(3)

        buttons = self.driver.find_elements(By.XPATH, "//div[@class='css-175oi2r r-sdzlij r-dnmrzs r-1awozwy r-18u37iz r-1777fci r-xyw6el r-o7ynqc r-6416eg']")
        buttons[1].click()
        time.sleep(1.5)

        search_input = search_term + ' until:' + end_date[6:10] + '-' + end_date[:5] + ' since:' + start_date[6:10] + '-' + start_date[:5]

        search = self.driver.find_element(By.XPATH, "//input[@type='text']")
        search.send_keys(search_input)
        time.sleep(3)
        listbox = self.driver.find_element(By.XPATH, "//div[@role='listbox']")
        buttons = listbox.find_elements(By.XPATH, "//div[@role='option']")
        buttons[0].click()
        time.sleep(4)

        Usernames = []
        Dates = []
        Tweets = []
        Retweets = []
        Likes = []

        articles = self.driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        while True:
            i=0
            while i < len(articles):
                UserTag = articles[i].find_element(By.XPATH,".//div[@data-testid='User-Name']").text.strip('\n').rsplit('@')[0][:-1]
                Usernames.append(UserTag)
        
                try:
                    TimeStamp = articles[i].find_element(By.XPATH,".//time").get_attribute('datetime')
                    Dates.append(TimeStamp)
                except:
                    Dates.append('???')
        
                Tweet = articles[i].find_element(By.XPATH,".//div[@data-testid='tweetText']").text.strip('\n')
                Tweets.append(Tweet)
        
                reTweet = articles[i].find_element(By.XPATH,".//div[@data-testid='retweet']").text
                if reTweet == '':
                    reTweet = '0'
                Retweets.append(reTweet)
        
                Like = articles[i].find_element(By.XPATH,".//div[@data-testid='like']").text
                if Like == '':
                    Like = '0'
                Likes.append(Like)

                i+=1

            before_scroll = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script('window.scrollTo(0,window.pageYOffset + 2250);')
            time.sleep(5)
            after_scroll = self.driver.execute_script("return document.body.scrollHeight")
            
            if before_scroll == after_scroll:
                break
            
            articles = self.driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
            
        
        df = pd.DataFrame(zip(Usernames, Dates, Tweets, Retweets, Likes),
                          columns = ['Username','Time','Tweet','Retweets','Likes'])
        
        df = df.drop_duplicates()

        path = your_path + str(search_term) + ".csv"
        df.to_csv(path_or_buf=path, index = False)





if __name__ == "__main__":
    
    search_term = input('Enter search term: ')
    start_date = input('Enter start date (MM-DD-YYYY): ')
    end_date = input('Enter end date (MM-DD-YYYY): ')
    suspicious_activity = input('Has Twitter flagged for suspicious activity? (Y/N): ')
    your_username = input('Enter your Twitter username in the format @username: ')
    your_password = input('Enter your Twitter password: ')
    your_email = input('Enter the email associated with your Twitter account: ')
    your_path = input('Enter the folder you would like the data to be saved: ')

    scraper = Scraper()
    scraper.scrape(search_term, start_date, end_date, suspicious_activity,
                   your_username, your_password, your_email, your_path)
