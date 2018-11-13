import threading
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
    try:
        1/0
        server_feed.main()
    except Exception as e:
        print('server_feed raised exception :',end = ' ')
        print(e)

def start_server_login():
    try:
        server_login.main()
    except Exception as e:
        print('server_login raised exception :',end = ' ')
        print(e)

def start_server_create_account():
    try:    
        server_create_account.main()
    except Exception as e:
        print('server_create_account raised exception :',end = ' ')
        print(e)

def start_server_upload_feed():
    try:
        server_upload_feed.main()
    except Exception as e:
        print('server_upload_feed raised exception :',end = ' ')
        print(e)

def start_server_search():
    try:
        server_search.main()
    except Exception as e:
        print('server_search raised exception :',end = ' ')
        print(e)

def start_server_friend():
    try:
        server_friend.main()
    except Exception as e:
        print('server_friend raised exception :',end = ' ')
        print(e)

def start_server_change_settings():
    try:
        server_change_settings.main()
    except Exception as e:
        print('server_change_settings raised exception :',end = ' ')
        print(e)

def start_server_like():
    try:
        server_like.main()
    except Exception as e:
        print('server_like raised exception :',end = ' ')
        print(e)

def start_server_scout():
    try:
        server_scout.main()
    except Exception as e:
        print('server_scout raised exception :',end = ' ')
        print(e)

if __name__ == '__main__':
    threads = []

    create_account = threading.Thread(target= start_server_create_account)
    threads.append(create_account)
    login = threading.Thread(target= start_server_login)
    threads.append(login)
    feed = threading.Thread(target= start_server_feed)
    threads.append(feed)
    upload_feed = threading.Thread(target= start_server_upload_feed)
    threads.append(upload_feed)
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