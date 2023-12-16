import json
from unittest.mock import ANY, Mock
import pytest
from youtube_api_lab.services.youtube import YoutubeService, YouTubeVideo


@pytest.fixture
def patch_youtube_playlist_response(requests_mock):
    fixture = "tests/services/fixtures/youtube_playlist_items_response.json"
    with open(fixture) as json_file:
        response = json.load(json_file)
    requests_mock.get(
        "https://youtube.googleapis.com/youtube/v3/playlistItems", json=response
    )
    yield


@pytest.fixture
def mock_youtube_service(patch_youtube_playlist_response) -> YoutubeService:
    mock_transcription_service = Mock()
    mock_transcription_service.get_transcripts_from_youtube.return_value = (
        "fake_transcript"
    )

    svc = YoutubeService(
        api_key="fake_api_key", transcription_service=mock_transcription_service
    )
    yield svc


def test_get_playlist_items_base(mock_youtube_service: YoutubeService):
    videos = mock_youtube_service.get_playlist_items("fake_playlist_id")
    expected_videos = [
        YouTubeVideo(
            video_id="qMeeEKrY02Q",
            thumbnail_url="https://i.ytimg.com/vi/qMeeEKrY02Q/default.jpg",
            title="CPI Data Release, Negative Divergences, Semiconductor Power Punch, Stock & Crypto Trades",
            published_at="2023-12-11T20:46:59Z",
            description=ANY,
            transcript="fake_transcript",
        ),
        YouTubeVideo(
            video_id="kRyJzm5nYJQ",
            thumbnail_url="https://i.ytimg.com/vi/kRyJzm5nYJQ/default.jpg",
            title="Weekly Trade Setups in Stocks, FED Decision, Negative Divergences in Crypto, Market Cycle Update",
            published_at="2023-12-10T16:31:48Z",
            description=ANY,
            transcript="fake_transcript",
        ),
    ]
    assert videos == expected_videos
