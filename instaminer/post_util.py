from time import sleep
from selenium import webdriver

from .time_util import current_timestamp

def get_post_data(browser, post_code):
    # type: (webdriver.Chrome, str) -> dict
    url = 'https://www.instagram.com/p/'+post_code
    print 'Checking post:', post_code, url

    browser.get(url)
    sleep(2)
    # window._sharedData.entry_data.PostPage[0].media
    code = browser.execute_script("return window._sharedData.entry_data.PostPage[0].media.code")
    print '--> Code:', code
    caption = browser.execute_script("return window._sharedData.entry_data.PostPage[0].media.caption")
    caption = caption.replace('\n', ' ')
    print '--> Caption:', caption

    comments_count = browser.execute_script("return window._sharedData.entry_data.PostPage[0].media.comments.count")
    print '--> Comments count:', comments_count

    date = browser.execute_script("return window._sharedData.entry_data.PostPage[0].media.date")
    print '--> Date:', date

    likes_count = browser.execute_script("return window._sharedData.entry_data.PostPage[0].media.likes.count")
    print '--> Like count:', likes_count

    res = {'code': code, 'caption':caption, 'comments_count':comments_count, 'date':date, 'likes_count': likes_count}

    return res


def extract_post_hashtags(post_caption):
    # type: (str) -> [str]
    words = post_caption.split(' ')
    words = [w for w in words if w.startswith('#')]
    words = [w.replace('#', '') for w in words]
    print '--> Hashtags found: ', words
    return words