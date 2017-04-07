import codecs
from os import environ
from random import randint
from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from .post_util import get_post_data, extract_post_hashtags
from .pages_utils import get_page_data, get_last_post
from .time_util import current_timestamp
from .login_util import login_user
from .hashtag_util import get_hashtag_count


class InstaMiner:
    def __init__(self, username=None, password=None, config_dir='./config'):
        # type: (str, str) -> None
        # self.display = Display(visible=0, size=(800, 600))
        # self.display.start()
        chrome_options = Options()
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
        self.browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)
        self.browser.implicitly_wait(10)

        self.logFile = open('./logs/miner_logFile.txt', 'a')
        self.logFile.write('Session started - %s\n' % (current_timestamp()))

        if username is None:
            self.username = environ.get('INSTA_USER')
        else:
            self.username = username

        if password is None:
            self.password = environ.get('INSTA_PW')
        else:
            self.password = password

        self.config_dir = config_dir
        self.__load_config(config_dir)

        self.hashtags_logs = codecs.open('./logs/miner_hashtags.csv', "a", "utf-8")
        self.pages_logs = codecs.open('./logs/miner_pages.csv', "a", "utf-8")
        self.posts_logs = codecs.open('./logs/miner_posts.csv', "a", "utf-8")

        self.post_discovery = True
        self.hashtag_discovery = True

    def login(self):
        # type: () -> InstaMiner
        """Used to login the user either with the username and password"""
        if not login_user(self.browser, self.username, self.password):
            print('Wrong login data!')
            self.logFile.write('Wrong login data!\n')
            self.aborting = True
        else:
            print('Logged in successfully!')
            self.logFile.write('Logged in successfully!\n')

        return self

    def set_post_discovery(self, value):
        self.post_discovery = value
        return self

    def set_hashtag_discovery(self, value):
        self.hashtag_discovery = value
        return self

    def run(self):
        self._run_pages(self.post_discovery)
        self._run_posts(self.hashtag_discovery)
        self._run_hashtags()
        return self

    def end(self):
        # type: () -> None
        """Closes the current session"""
        self.browser.delete_all_cookies()
        self.browser.close()
        # self.display.stop()

        print('')
        print('Session ended')
        print('-------------')

        self.logFile.write('\nSession ended - %s\n' \
                           % (current_timestamp()))
        self.logFile.write('-' * 20 + '\n\n')
        self.logFile.close()

    def _run_hashtags(self):
        print ''
        print "Checking hashtags..."
        for i, hashtag in enumerate(self.hashtags):
            print ''
            print '['+str(i+1)+'/'+ str(len(self.hashtags))+']'
            count = get_hashtag_count(self.browser, hashtag)
            self.hashtags_logs.write(hashtag+';'+str(count)+';'+current_timestamp()+'\n')
        return self

    def _run_pages(self, check_last_post = True):
        """check_last_post = True --> check if the page last post is being montiored, and if it isn't, adds it
        to posts list. """
        print ''
        print "Checking Pages..."
        for i, page in enumerate(self.pages):
            print ''
            print '['+str(i+1)+'/'+ str(len(self.pages))+']'
            res = get_page_data(self.browser, page)
            self.pages_logs.write(page + ';'
                                  + res['biography'] + ';'
                                  + res['external_url'] + ';'
                                  + str(res['post_count']) + ';'
                                  + str(res['followers']) + ';'
                                  + str(res['follows'])+'\n')

            if check_last_post:
                last_post_code = get_last_post(self.browser, page)
                if last_post_code != '' and last_post_code not in self.posts:
                    print "Found a new post: ", last_post_code
                    self.posts.append(last_post_code)
                    post_file = open(self.config_dir+'/posts', 'a')
                    post_file.write(last_post_code+'\n')
                    post_file.close()

        return self

    def _run_posts(self, hashtag_discovery):
        print ''
        print "Checking Posts..."
        for i, post in enumerate(self.posts):
            print ''
            print '['+str(i+1)+'/'+str(len(self.posts))+']'
            res = get_post_data(self.browser, post)
            self.posts_logs.write(post + ';'
                                  + res['caption'] + ';'
                                  + str(res['comments_count']) + ';'
                                  + str(res['likes_count']) + ';'
                                  + str(res['date']) + '\n')

            if hashtag_discovery:
                post_hashtags = extract_post_hashtags(res['caption'])
                for ph in post_hashtags:
                    hashtag_file = codecs.open(self.config_dir + '/hashtags', 'a', 'utf-8')
                    if ph not in self.hashtags:
                        self.hashtags.append(ph)
                        hashtag_file.write(ph + '\n')
                    hashtag_file.close()

        return self

    def __load_config(self, config_dir):
        # type: (str) -> None

        # HASHTAG
        self.hashtags = [line.rstrip('\n') for line in open(config_dir+'/hashtags','r')]
        print 'Hashtags:'
        for h in self.hashtags:
            print '\t', h

        # PAGES
        self.pages = [line.rstrip('\n') for line in open(config_dir + '/pages', 'r')]
        print 'Pages:'
        for p in self.pages:
            print '\t', p

        # POSTS
        self.posts = [line.rstrip('\n') for line in open(config_dir + '/posts', 'r')]
        print 'Posts:'
        for p in self.posts:
            print '\t', p

