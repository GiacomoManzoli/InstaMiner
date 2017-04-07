from time import sleep
from selenium import webdriver

from .time_util import current_timestamp

def get_hashtag_count(browser, hashtag):
    # type: (webdriver.Chrome, str) -> int

    url = 'https://www.instagram.com/explore/tags/' \
                + (hashtag[1:] if hashtag[:1] == '#' else hashtag)
    print 'Checking hashtag:', hashtag, url

    browser.get(url)

    sleep(2)

    count = browser.execute_script("return window._sharedData.entry_data.TagPage[0].tag.media.count")
    print '--> Post count:', str(count), 'at ', current_timestamp()
    return int(count)
