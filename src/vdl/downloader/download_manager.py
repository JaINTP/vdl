import asyncio
import aiohttp
import os
import re
from typing import Callable

class DownloadManager:
    """
    Singleton class that manages asynchronous downloads dynamically.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._download_tasks = set()

    async def download_file(self, url: str, output_path: str,
                           progress_callback: Callable[[int, int], None],
                           completion_callback: Callable[[int, int], None]):
        """
        Downloads a file asynchronously with progress updates.

        Args:
            url (str): The URL of the file to download.
            output_path (str): Path to save the downloaded file.
            progress_callback (Callable[[int, int], None]): Function to report progress.
            progress_callback (Callable[[int, int], None]): Function to report completion.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get("Content-Length", 0))
                    downloaded = 0

                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    with open(output_path, "wb") as file:
                        async for chunk in response.content.iter_chunked(1024):
                            file.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback:
                                progress_callback(downloaded, total_size)

                    if completion_callback:
                        completion_callback(downloaded, total_size)

        except Exception as e:
            print(f"Error downloading {url}: {e}")
        finally:
            self._download_tasks.discard(asyncio.current_task())

    def start_download(self, url: str, output_path: str,
                       progress_callback: Callable[[int, int], None],
                       completion_callback: Callable[[int, int], None]
    ):
        """
        Start a download task immediately.

        Args:
            url (str): The URL of the file to download.
            output_path (str): Path to save the downloaded file.
            progress_callback (Callable[[int, int], None]): Function to report progress.
            progress_callback (Callable[[int, int], None]): Function to report completion.
        """
        task = asyncio.create_task(
            self.download_file(url, output_path, progress_callback, completion_callback)
        )
        self._download_tasks.add(task)

    def active_downloads(self):
        """
        Returns the number of active download tasks.
        """
        return len(self._download_tasks)