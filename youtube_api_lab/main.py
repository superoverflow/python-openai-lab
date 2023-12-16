import os
import dotenv
from openai import OpenAI
from youtube_api_lab.services.chatgpt import ChatGPTService
from youtube_api_lab.services.youtube import YoutubeService
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--playlist", type=str, required=True)
    return parser.parse_args()


def get_openai_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)


def main(playlist_id: str):
    open_api_key = os.getenv("OPENAI_API_KEY")
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    chatgpt_service = ChatGPTService(get_openai_client(api_key=open_api_key))
    youtube_service = YoutubeService(api_key=youtube_api_key)
    videos = youtube_service.get_playlist_items(playlist_id)

    for item in videos:
        print(f"Video: [{item.video_id}] [{item.published_at}], title: [{item.title}]")
        sentiments = chatgpt_service.summarize_transcript(item.transcript)
        for sentiment in sentiments:
            print(sentiment)
        print("-------------------")


if __name__ == "__main__":
    dotenv.load_dotenv()
    args = parse_args()
    playlist_id = args.playlist
    main(playlist_id)
