import os
import random

import requests
from dotenv import load_dotenv


def get_last_comic_num():
    xkcd_url = 'https://xkcd.com/info.0.json'
    response = requests.get(xkcd_url)
    response.raise_for_status()
    return response.json().get('num')


def get_comic_details(comic_num):
    xkcd_url = f'https://xkcd.com/{comic_num}/info.0.json'
    response = requests.get(xkcd_url)
    response.raise_for_status()
    return response.json()


def download_image(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_img_filepath(url, folder='images'):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.basename(url)
    filepath = os.path.join(folder, filename)
    return filepath


def get_upload_server_url(access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': access_token,
        'v': 5.131,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_error(response.json())
    upload_server = response.json().get('response')
    return upload_server.get('upload_url')


def upload_image(upload_url, filepatch):
    with open(filepatch, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        check_for_error(response)
    return response.json()


def save_photo_in_album(access_token, upload_details):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': access_token,
        'server': upload_details.get('server'),
        'photo': upload_details.get('photo'),
        'hash': upload_details.get('hash'),
        'v': 5.131,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    check_for_error(response)
    return response.json().get('response')[0]


def publish_post(access_token, group_id, photo, text):
    url = 'https://api.vk.com/method/wall.post'
    attachments = f"photo{photo.get('owner_id')}_{photo.get('id')}"
    payload = {
        'access_token': access_token,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': attachments,
        'message': text,
        'v': 5.131,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    check_for_error(response)


def check_for_error(response):
    if 'error' in response:
        raise requests.RequestException


def main():
    load_dotenv()
    group_id = os.getenv('GROUP_ID')
    access_token = os.getenv('ACCESS_TOKEN')
    comic_num = random.randint(1, get_last_comic_num())
    comic_details = get_comic_details(comic_num)
    image_url = comic_details.get('img')
    post_text = comic_details.get('alt')
    filepatch = get_img_filepath(image_url)
    download_image(image_url, filepatch)
    try:
        upload_url = get_upload_server_url(access_token)
        upload_details = upload_image(upload_url, filepatch)
        photo = save_photo_in_album(access_token, upload_details)
        publish_post(access_token, group_id, photo, post_text)
    except requests.RequestException:
        print('Ошибка в запросе')
    os.remove(filepatch)


if __name__ == '__main__':
    main()
