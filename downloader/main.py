import os
import pytube
from instaloader import Instaloader
import pinterest
from tqdm import tqdm

# Configuration
ACCESS_TOKEN = "AeR9TgRgWmzCX6vB2pGfC1D2eF3aA4bC5dE6fG7hI8jK9lM0"
OUTPUT_PATHS = {
    "youtube": "youtube_downloads",
    "instagram": "instagram_downloads",
    "pinterest": "pinterest_downloads"
}

# Error Handling
class DownloadError(Exception):
    pass

# Platform Downloader
def download_platform(url, platform):
    if platform == "youtube":
        return download_youtube_video(url)
    elif platform == "instagram":
        return download_instagram_media(url)
    elif platform == "pinterest":
        return download_pinterest_media(url)
    else:
        raise DownloadError("Invalid platform")

# YouTube Downloader
def download_youtube_video(url):
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(only_audio=False).first()
        stream.on_progress = lambda stream, chunk, bytes_remaining: tqdm.update(1)
        with tqdm(unit='B', unit_scale=True, leave=False) as t:
            stream.download(output_path=OUTPUT_PATHS["youtube"])
    except pytube.exceptions.VideoUnavailable:
        raise DownloadError("Video is unavailable")
    except pytube.exceptions.LiveStreamError:
        raise DownloadError("Live stream is not supported")
    except Exception as e:
        raise DownloadError("Error downloading YouTube video: {}".format(str(e)))

# Instagram Downloader
def download_instagram_media(url):
    try:
        ig = Instaloader()
        ig.download_post(url, target=OUTPUT_PATHS["instagram"], callback=lambda x: tqdm.update(1))
    except Exception as e:
        raise DownloadError("Error downloading Instagram media: {}".format(str(e)))

# Pinterest Downloader
def download_pinterest_media(url):
    try:
        pinterest_api = pinterest.PinterestAPI(access_token=ACCESS_TOKEN)
        pinterest_api.download_image(url, target=OUTPUT_PATHS["pinterest"], callback=lambda x: tqdm.update(1))
    except pinterest.exceptions.PinterestException as e:
        raise DownloadError("Error downloading Pinterest image: {}".format(str(e)))
    except Exception as e:
        raise DownloadError("Error downloading Pinterest image: {}".format(str(e)))

# Main function
def main():
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print the menu
    print("\033[91m" + " Media Downloader ".center(os.get_terminal_size().columns, "-") + "\033[0m")
    print("\033[91m" + "1. YouTube".center(os.get_terminal_size().columns) + "\033[0m")
    print("\033[91m" + "2. Instagram".center(os.get_terminal_size().columns) + "\033[0m")
    print("\033[91m" + "3. Pinterest".center(os.get_terminal_size().columns) + "\033[0m")

    choice = input("\033[91m" + "Enter your choice (1/2/3): ".center(os.get_terminal_size().columns) + "\033[0m")

    if choice == "1":
        url = input("\033[91m" + "Enter YouTube video URL: ".center(os.get_terminal_size().columns) + "\033[0m")
        try:
            download_platform(url, "youtube")
        except DownloadError as e:
            print("\033[91m" + str(e).center(os.get_terminal_size().columns) + "\033[0m")
    elif choice == "2":
        url = input("\033[91m" + "Enter Instagram post URL: ".center(os.get_terminal_size().columns) + "\033[0m")
        try:
            download_platform(url, "instagram")
        except DownloadError as e:
            print("\033[91m" + str(e).center(os.get_terminal_size().columns) + "\033[0m")
    elif choice == "3":
        url = input("\033[91m" + "Enter Pinterest image URL: ".center(os.get_terminal_size().columns) + "\033[0m")
        try:
            download_platform(url, "pinterest")
        except DownloadError as e:
            print("\033[91m" + str(e).center(os.get_terminal_size().columns) + "\033[0m")
    else:
        print("\033[91m" + "Invalid choice".center(os.get_terminal_size().columns) + "\033[0m")

if __name__ == "__main__":
    main()