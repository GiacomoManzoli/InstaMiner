from time import sleep
from selenium import webdriver

from .time_util import current_timestamp

def get_page_data(browser, page_name):
    # type: (webdriver.Chrome, str) -> dict
    url = 'https://www.instagram.com/'+page_name
    print 'Checking page:', page_name, url

    browser.get(url)
    sleep(2)

    biography = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.biography")
    biography = biography.replace('\n', ' ')
    print '--> Biography:', biography
    external_url = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.external_url")
    if external_url is None:
        external_url = ''
    print '--> External url:', str(external_url)
    post_count = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.media.count")
    print '--> Post count:', str(post_count)
    followers = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.followed_by.count")
    print '--> Followers:', str(followers)
    follows = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.follows.count")
    print '--> Follows:', str(follows)
    res = {'biography': biography, 'external_url': external_url, 'post_count': post_count, 'followers': followers,
           'follows': follows}

    return res

def get_last_post(browser, page_name):
    # type: (webdriver.Chrome, str) -> str
    url = 'https://www.instagram.com/'+page_name
    print 'Retriving last post of', page_name, url

    browser.get(url)
    sleep(2)

    code = browser.execute_script("return window._sharedData.entry_data.ProfilePage[0].user.media.nodes[0].code")
    print '--> Last post code:', str(code)
    return code