import threading
import traceback
import server_login
import server_create_account
import server_feed
import server_upload_feed
import server_search
import server_friend
import server_change_settings
import server_like
import server_scout


def start_server_feed():
    server_feed.main()
    
def start_server_login():
    server_login.main()

def start_server_create_account():
    server_create_account.main()
    
def start_server_search():
    server_search.main()

def start_server_friend():
   server_friend.main()
    
def start_server_change_settings():
    server_change_settings.main()

def start_server_like():
    server_like.main()

def start_server_scout():
    server_scout.main()

if __name__ == '__main__':
    threads = []

    create_account = threading.Thread(target= start_server_create_account)
    threads.append(create_account)
    login = threading.Thread(target= start_server_login)
    threads.append(login)
    feed = threading.Thread(target= start_server_feed)
    threads.append(feed)
    search = threading.Thread(target= start_server_search)
    threads.append(search)
    friend = threading.Thread(target= start_server_friend)
    threads.append(friend)
    change_settings = threading.Thread(target= start_server_change_settings)
    threads.append(change_settings)
    like = threading.Thread(target= start_server_like)
    threads.append(like)
    scout = threading.Thread(target= start_server_scout)
    threads.append(scout)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
