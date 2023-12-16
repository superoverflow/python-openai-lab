from dataclasses import dataclass
from typing import Any, Self
from youtube_transcript_api import YouTubeTranscriptApi
import logging
import requests

logger = logging.getLogger(__name__)


class YoutubePlaylistError(Exception):
    pass


class TranscriptionService:
    def join_transcript_text(transcripts):
        return " ".join((item["text"] for item in transcripts))

    def get_transcripts_from_youtube(self, video_id: str) -> str:
        try:
            transcripts, _ = YouTubeTranscriptApi.get_transcripts(
                [video_id], languages=["en"]
            )
        except Exception as e:
            logger.exception(f"Failed to get transcript for video {video_id}")
            raise e
        return TranscriptionService.join_transcript_text(transcripts[video_id])


@dataclass(frozen=True, kw_only=True)
class YouTubeVideo:
    video_id: str
    thumbnail_url: str
    title: str
    published_at: str
    description: str
    transcript: str = None

    def from_response(response: dict[str, Any], transcript: str | None = None) -> Self:
        return YouTubeVideo(
            video_id=response["snippet"]["resourceId"]["videoId"],
            thumbnail_url=response["snippet"]["thumbnails"]["default"]["url"],
            title=response["snippet"]["title"],
            published_at=response["snippet"]["publishedAt"],
            description=response["snippet"]["description"],
            transcript=transcript,
        )


class YoutubeService:
    def __init__(
        self,
        api_key: str,
        transcription_service: TranscriptionService = TranscriptionService(),
    ):
        self.api_key = api_key
        self.transcription_service = transcription_service

    def unpack_playlist_item(
        self, response_item: dict[str, Any]
    ) -> YouTubeVideo | None:
        video_id = response_item["snippet"]["resourceId"]["videoId"]
        transcript = self.transcription_service.get_transcripts_from_youtube(video_id)
        if transcript is None:
            return None
        return YouTubeVideo.from_response(
            response_item,
            transcript=transcript,
        )

    def get_playlist_items(self, playlistId: str) -> list[YouTubeVideo]:
        base_url = "https://youtube.googleapis.com/youtube/v3/playlistItems"
        params = {
            "part": "snippet",
            "playlistId": playlistId,
            "key": self.api_key,
        }
        resp = requests.get(base_url, params=params)
        if resp.status_code != 200:
            raise YoutubePlaylistError(
                f"Request failed with status code {resp.status_code}"
            )
        response = resp.json()

        return [
            self.unpack_playlist_item(item)
            for item in response["items"]
            if item is not None
        ]
