from confidential_informaion import *
import praw
import datetime
import vk
import json
import schedule
import requests


def get_photos_from_reddit():
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         password=password,
                         user_agent="bruh by /u/haliaven",
                         username="haliaven")
    return [x.url for x in list(reddit.get('r/hmmm/hot'))]


def save_photos_on_pc(posts):
    i = 0
    current_photo = open(f'photos/0.jpg', 'rb').read()
    old_photos = open('photos/old_photos', 'r').read()
    while current_photo == requests.get(posts[i]).content or posts[i] in old_photos:
        i += 1
    with open(f'photos/0.jpg', 'wb') as f:
        f.write(requests.get(posts[i]).content)
    with open('photos/old_photos', 'a') as f:
        f.write(posts[i])
        f.write('\n')


def upload_photo_vk():
    photo_data = requests.post(post_url['upload_url'], files={'photo': ('0.jpg', open(r'photos/0.jpg', 'rb'))}).content
    photo_data = json.loads(photo_data)
    media = vkapi.photos.saveWallPhoto(server=photo_data['server'], photo=photo_data['photo'],
                                       hash=photo_data['hash'], group_id=198109544, v='5.122')[0]['id']
    print(f'Posted at {datetime.datetime.now()}')
    vkapi.wall.post(owner_id=-198109544, from_group=1, attachments=f'photo145145860_{media}', message='hmm🤔', v='5.122')


def execute_all_functions():
    save_photos_on_pc(get_photos_from_reddit())
    upload_photo_vk()


def authorize():
    session = vk.AuthSession(app_id=7575969, user_login=login, user_password=password_vk, scope=140488159)
    session.oauth2_authorization()
    return vk.API(session)


if __name__ == '__main__':
    # backup = 7575969, main = 7574961
    vkapi = authorize()
    post_url = vkapi.photos.getWallUploadServer(group_id=198109544, v='5.122')
    execute_all_functions()

    schedule.every(45).minutes.do(execute_all_functions)
    while True:
        schedule.run_pending()
