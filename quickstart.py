from instaminer import InstaMiner

dont_like = ['food', 'girl', 'hot']
ignore_words = ['pizza']
friend_list = ['friend1', 'friend2', 'friend3']

#InstaPy(username='<username>', password='<password>')\
#  .login()\
#  .set_do_comment(True, percentage=10) \
#  .set_comments(['Cool!', 'Awesome!', 'Nice!']) \
#  .set_dont_include(friend_list) \
#  .set_dont_like(dont_like) \
#  .set_ignore_if_contains(ignore_words) \
#  .like_by_tags(['dog', '#cat'], amount=100) \
#  .end()

InstaMiner(username='gmanzoli')\
    .login() \
    .set_post_discovery(True)\
    .set_hashtag_discovery(True) \
    .run() \
    .end()
