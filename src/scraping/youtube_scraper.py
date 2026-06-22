"""Scraping de comentarios desde YouTube Data API v3."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import pandas as pd

import config
from src.utils.helpers import extract_youtube_video_id, generate_comment_id, logger, safe_datetime


class YouTubeScraper:
    """Extractor de videos y comentarios de YouTube."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.YOUTUBE_API_KEY
        self.youtube = None
        if self.api_key:
            self._init_client()

    def _init_client(self) -> bool:
        try:
            from googleapiclient.discovery import build
            self.youtube = build("youtube", "v3", developerKey=self.api_key)
            return True
        except Exception as exc:
            logger.error("Error inicializando YouTube API: %s", exc)
            self.youtube = None
            return False

    @property
    def is_available(self) -> bool:
        return self.youtube is not None

    def search_videos(self, query: str, max_results: int = None) -> list[dict[str, Any]]:
        max_results = max_results or config.MAX_VIDEOS_PER_SEARCH
        if not self.is_available:
            logger.warning("YouTube API no disponible para búsqueda.")
            return []
        try:
            response = self.youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=max_results,
                relevanceLanguage="es",
                regionCode="PE",
            ).execute()
            videos = []
            for item in response.get("items", []):
                vid = item["id"]["videoId"]
                snippet = item["snippet"]
                videos.append({
                    "video_id": vid,
                    "video_title": snippet.get("title", ""),
                    "channel": snippet.get("channelTitle", ""),
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "published_at": snippet.get("publishedAt", ""),
                })
            return videos
        except Exception as exc:
            logger.error("Error buscando videos: %s", exc)
            return []

    def get_video_info(self, video_id: str) -> dict[str, Any]:
        if not self.is_available:
            return {"video_id": video_id, "video_title": "", "channel": ""}
        try:
            response = self.youtube.videos().list(part="snippet", id=video_id).execute()
            items = response.get("items", [])
            if not items:
                return {"video_id": video_id, "video_title": "", "channel": ""}
            snippet = items[0]["snippet"]
            return {
                "video_id": video_id,
                "video_title": snippet.get("title", ""),
                "channel": snippet.get("channelTitle", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }
        except Exception as exc:
            logger.error("Error obteniendo info de video: %s", exc)
            return {"video_id": video_id, "video_title": "", "channel": ""}

    def get_comments(self, video_id: str, max_comments: int = None) -> list[dict[str, Any]]:
        max_comments = max_comments or config.MAX_COMMENTS_PER_VIDEO
        if not self.is_available:
            return []
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=min(100, max_comments),
                textFormat="plainText",
            )
            while request and len(comments) < max_comments:
                response = request.execute()
                for item in response.get("items", []):
                    top = item["snippet"]["topLevelComment"]["snippet"]
                    comment_id = item["snippet"]["topLevelComment"]["id"]
                    dt = safe_datetime(top.get("publishedAt"))
                    comments.append({
                        "id": comment_id,
                        "source": "youtube",
                        "text": top.get("textDisplay", ""),
                        "author": top.get("authorDisplayName", "Anónimo"),
                        "date": dt.isoformat() if dt else None,
                        "likes": int(top.get("likeCount", 0)),
                        "replies": int(item["snippet"].get("totalReplyCount", 0)),
                        "video_id": video_id,
                        "url": f"https://www.youtube.com/watch?v={video_id}&lc={comment_id}",
                    })
                    if len(comments) >= max_comments:
                        break
                request = self.youtube.commentThreads().list_next(request, response)
            return comments
        except Exception as exc:
            logger.error("Error extrayendo comentarios de %s: %s", video_id, exc)
            return []

    def scrape_url(self, url: str) -> pd.DataFrame:
        video_id = extract_youtube_video_id(url)
        if not video_id:
            logger.error("URL de YouTube inválida: %s", url)
            return pd.DataFrame()
        info = self.get_video_info(video_id)
        comments = self.get_comments(video_id)
        for c in comments:
            c["video_title"] = info.get("video_title", "")
            c["channel"] = info.get("channel", "")
        return pd.DataFrame(comments)

    def scrape_search_queries(self, queries: list[str] = None) -> pd.DataFrame:
        queries = queries or config.DEFAULT_SEARCH_QUERIES
        all_comments = []
        seen_videos = set()
        for query in queries:
            videos = self.search_videos(query)
            for video in videos:
                vid = video["video_id"]
                if vid in seen_videos:
                    continue
                seen_videos.add(vid)
                comments = self.get_comments(vid)
                for c in comments:
                    c["video_title"] = video.get("video_title", "")
                    c["channel"] = video.get("channel", "")
                all_comments.extend(comments)
        return pd.DataFrame(all_comments)

    def scrape_keywords(self, keywords: list[str]) -> pd.DataFrame:
        return self.scrape_search_queries(keywords)


class RedditScraper:
    """Importador opcional desde Reddit (PRAW)."""

    def __init__(self, client_id: str = "", client_secret: str = "", user_agent: str = "sentiment_platform"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.reddit = None

    def _init(self) -> bool:
        if not self.client_id or not self.client_secret:
            return False
        try:
            import praw
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
            )
            return True
        except Exception as exc:
            logger.warning("Reddit no disponible: %s", exc)
            return False

    def search(self, query: str, subreddit: str = "Peru", limit: int = 100) -> pd.DataFrame:
        if not self._init():
            return pd.DataFrame()
        rows = []
        try:
            for submission in self.reddit.subreddit(subreddit).search(query, limit=limit):
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list()[:limit]:
                    dt = datetime.fromtimestamp(comment.created_utc)
                    rows.append({
                        "id": generate_comment_id(comment.body, str(comment.author), submission.id),
                        "source": "reddit",
                        "text": comment.body,
                        "author": str(comment.author),
                        "date": dt.isoformat(),
                        "likes": comment.score,
                        "replies": 0,
                        "video_id": submission.id,
                        "video_title": submission.title,
                        "channel": subreddit,
                        "url": f"https://reddit.com{comment.permalink}",
                    })
        except Exception as exc:
            logger.error("Error scraping Reddit: %s", exc)
        return pd.DataFrame(rows)


class DataImporter:
    """Importador unificado CSV/Excel."""

    @staticmethod
    def from_csv(path: str, source: str = "csv") -> pd.DataFrame:
        try:
            df = pd.read_csv(path)
            if df.empty:
                logger.warning("CSV vacío: %s", path)
                return pd.DataFrame()
            df["source"] = source
            column_map = {
                "comment": "text",
                "comentario": "text",
                "usuario": "author",
                "fecha": "date",
                "me_gusta": "likes",
            }
            df = df.rename(columns=column_map)
            if "id" not in df.columns:
                df["id"] = df.apply(
                    lambda r: generate_comment_id(
                        str(r.get("text", "")),
                        str(r.get("author", "")),
                        str(r.get("video_id", "csv")),
                    ),
                    axis=1,
                )
            return df
        except Exception as exc:
            logger.error("Error leyendo CSV: %s", exc)
            return pd.DataFrame()

    @staticmethod
    def from_excel(path: str, source: str = "excel") -> pd.DataFrame:
        try:
            df = pd.read_excel(path)
            if df.empty:
                logger.warning("Excel vacío: %s", path)
                return pd.DataFrame()
            df["source"] = source
            column_map = {
                "comment": "text",
                "comentario": "text",
                "usuario": "author",
                "fecha": "date",
                "me_gusta": "likes",
            }
            df = df.rename(columns=column_map)
            if "id" not in df.columns:
                df["id"] = df.apply(
                    lambda r: generate_comment_id(
                        str(r.get("text", "")),
                        str(r.get("author", "")),
                        str(r.get("video_id", "excel")),
                    ),
                    axis=1,
                )
            return df
        except Exception as exc:
            logger.error("Error leyendo Excel: %s", exc)
            return pd.DataFrame()
