import os
from instaloader import Instaloader, Post
import logging


logger = logging.getLogger()
L = Instaloader()
link = "https://www.instagram.com/p/Cz44st4sgkZ/?hl=en"


def download_post(link):
    extract_code = lambda link,item: link.split(f"/{item}/")[1].split("/")[0]
    try:
        code = extract_code(link, "p")
    except:
        code = extract_code(link, "reel")
    code = extract_code(link)
    post = Post.from_shortcode(L.context, code)
    try:
        L.download_post(post, code)
        is_successfull = True
    except Exception as e:
        print("Download failed. Reason", e)
        is_successfull = False
    return is_successfull,code


def get_caption(is_successfull,path):
    photos = []
    videos = []
    if is_successfull:    
        for item in (os.listdir(path)):
            if item.endswith("txt"):
                text_path = f'{path}/{item}'
                with open(text_path, encoding="utf-8") as text_file:
                    caption = text_file.read()
            elif item.endswith("jpg"):
                photo_path = f'{path}/{item}'
                photos.append(photo_path)
            elif item.endswith("mp4"):
                video_path = f'{path}/{item}'
                videos.append(video_path)
    return caption,videos,photos
    







