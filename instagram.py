import os
from instaloader import Instaloader, Post, Profile, Story
import logging
logger = logging.getLogger()
from instaloader import Instaloader, Profile

L = Instaloader()
USERNAME = "atongjonathan"




def download_post(link):
    extract_code = lambda link,item: link.split(f"/{item}/")[1].split("/")[0]
    try:
        code = extract_code(link, "p")
    except:
        code = extract_code(link, "reel")
    post = Post.from_shortcode(L.context, code)
    path = f"{code}"
    try:
        L.download_post(post, path)
        is_successfull = True
    except Exception as e:
        print("Download failed. Reason", e)
        is_successfull = False
    return is_successfull,path


def get_caption(is_successfull,path):
    photos = []
    videos = []
    caption = ""
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
    
def download_story(username):
    L.load_session_from_file(USERNAME, "session-atongjonathan")
    profile = L.check_profile_id(username)
    path = f'{profile.username}'
    try:
        L.download_stories(userids=[profile.userid],filename_target=path)
        is_success = True
    except Exception as e:
        print("An error occurred", e)
        is_success = False
    return is_success, path












