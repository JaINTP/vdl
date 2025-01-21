"""
Module: vdl.tui.widgets.download_progress_widget
Provides a widget for displaying download progress using Textual's framework.
"""

from pathlib import Path

from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, ProgressBar, Static

from vdl.downloader import DownloadManager
from vdl.models import Extension


class DownloadProgressWidget(Static):
    """
    A widget for managing and displaying the download progress of an extension.

    Attributes:
        extension (Extension): The extension being downloaded.
    """

    def __init__(self, extension: Extension) -> None:
        """
        Initializes the widget with the given extension.

        Args:
            extension (Extension): The extension for which the download progress is tracked.
        """
        self.extension = extension
        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Composes the UI components of the widget.

        Yields:
            ComposeResult: The composed UI components, including:
                - A label showing the extension details.
                - A horizontal container with a progress bar and log.
        """
        yield Label(f'Extension: {self.extension.publisher} - {self.extension.name} - v{self.extension.version}')
        with Horizontal():
            yield Static("Progress:")
            yield ProgressBar(id="progress", )
            yield Label(id="log")

    async def on_mount(self) -> None:
        """
        Called when the widget is mounted. Initiates the download process.
        """
        self.start_download()

    @work
    async def start_download(self) -> None:
        """
        Starts the download process and updates the progress bar and log.

        Handles callbacks for download progress and completion.
        """
        try:
            # Prepare output file path
            output_file = Path.home() / 'Downloads' / f'{self.extension.name}-{self.extension.version}.vsix'

            # Cache widget references
            progress_bar: ProgressBar = self.query_one("#progress", ProgressBar)
            log_label: Label = self.query_one("#log", Label)

            def progress_callback(downloaded: int, total_size: int) -> None:
                """
                Updates the progress bar and log with the current download status.

                Args:
                    downloaded (int): The number of bytes downloaded so far.
                    total_size (int): The total size of the file in bytes.
                """
                progress_bar.update(total=total_size, progress=downloaded)
                log_label.update(f"{self.format_size(downloaded)}/{self.format_size(total_size)}")

            def completion_callback(downloaded: int, total_size: int) -> None:
                """
                Notifies the user and updates the log when the download is complete.

                Args:
                    downloaded (int): The total bytes downloaded.
                    total_size (int): The total size of the file.
                """
                self.notify(f'Download complete: {output_file}')
                log_label.update(f"✓ Done {self.format_size(downloaded)}/{self.format_size(total_size)}")

            # Initiate download with callbacks
            manager = DownloadManager()
            manager.start_download(
                url=self.extension.download_url,
                output_path=output_file,
                progress_callback=progress_callback,
                completion_callback=completion_callback,
            )

        except Exception as e:
            log_label.update("Error!")
            self.notify(f"Error downloading {self.extension.name}: {e}")
            raise

    @staticmethod
    def format_size(size_in_bytes: int) -> str:
        """
        Converts bytes to a human-readable format (e.g., KB, MB, GB).

        Args:
            size_in_bytes (int): The size in bytes.

        Returns:
            str: The size with the appropriate unit.
        """
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = size_in_bytes
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.2f} {units[unit_index]}"