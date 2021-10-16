import re
import csv 
from getpass import getpass 
from time import sleep 
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException 
from msedge.selenium_tools import Edge, EdgeOptions 

options = EdgeOptions()
options.use_chromium = True 
driver = Edge(executable_path=r'F:\Web Scraping\edgedriver_win64\msedgedriver.exe', options=options)
driver.get('https://twitter.com/i/flow/login?')

def get_username():
    username = driver.find_element_by_xpath('//input[@name="username"]')
    user = input('username: ')
    username.send_keys(user) 
    username.send_keys(Keys.RETURN)

def get_password():
    passfield = driver.find_element_by_xpath('//input[@name="password"]')
    password = getpass('Password: ') 
    passfield.send_keys(password)
    passfield.send_keys(Keys.RETURN)

def search():
    search_term = input('Search Query: ') 
    search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
    search_input.send_keys(search_term) 
    search_input.send_keys(Keys.RETURN)

def open_detail():
    driver.find_element_by_xpath('//a[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]').click() 

def get_tweet_data(card):
    """Extract data from tweet data"""
    username = card.find_element_by_xpath('.//span').text 
    handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text 
    try: 
        postdate = card.find_element_by_xpath('//time').get_attribute('datetime')
    except:
        return 
    text = card.find_element_by_xpath('.//div[@class="css-1dbjc4n"]').text 
    reply_count = card.find_element_by_xpath('.//div[@data-testid="reply"]').text 
    retweet_count = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text 
    like_count = card.find_element_by_xpath('.//div[@data-testid="like"]').text 
    
    tweet = (username, handle, postdate, text, reply_count, retweet_count, like_count) 
    print(tweet)
    return tweet 

def start_scraping():
    data = [] 
    tweet_ids = set() 
    last_position = driver.execute_script("return window.pageYOffset;") 
    scrolling = True 

    while scrolling:
        page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
        for card in page_cards[-15:]:
            tweet = get_tweet_data(card) 
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet) 
        
        scroll_attempt = 0 
        while True:
            # check scroll position 
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(1)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1 

                # end of scroll region 
                if scroll_attempt >= 3:
                    scrolling = False 
                    break 
                else: 
                    sleep(2) # attempt to scroll again 
            else:
                last_position = curr_position 
                break 
    print(data) 

if __name__ == '__main__':
    done = input('Done?') 
    get_username() 
    done = input('Done?') 
    get_password() 
    done = input('Done?') 
    search() 
    done = input('Done?') 
    open_detail() 
    done = input('Done?')
    start_scraping() 
