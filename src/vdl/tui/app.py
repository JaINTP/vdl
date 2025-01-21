"""
Module: vdl.tui.app
Defines the main application for the VSIX Downloader using Textual's framework.
"""

import os
import re
from textual.app import App
from textual.css.query import NoMatches
from textual.widgets import Button, Input

from vdl.tui.screens import MainScreen, SearchScreen
from vdl.tui.widgets import DownloadProgressWidget
from vdl.models import Extension


class DownloadApp(App):
    """
    The main application class for the VSIX Downloader.

    Features:
    - Navigates between screens for searching and downloading VSIX extensions.
    - Manages download progress widgets dynamically.
    """

    CSS_PATH = "styles.tcss"

    def __init__(self) -> None:
        """
        Initializes the VSIX Downloader application.
        """
        super().__init__()
        self.title = "VSIX Downloader"

    def on_mount(self) -> None:
        """
        Called when the application is mounted. Pushes the main screen.
        """
        self.push_screen(MainScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles button press events. Triggers actions based on button IDs.

        Args:
            event (Button.Pressed): The button press event.
        """
        search_input: Input = self.query_one('#search_query') 
        if event.button.id == "search_button":
            # Retrieve the search query value
            search_query = search_input.value
            search_input.value = ''

            # Push the SearchScreen and pass the callback for downloading extensions
            self.push_screen(SearchScreen(search_query), self.download_extension)

    def download_extension(self, extension: Extension) -> None:
        """
        Initiates the download process for a given extension.

        Args:
            extension (Extension): The extension to download.
        """
        if extension:
            first_progress = None
            progress_list = self.query_one("#progress_list")

            try:
                # Check if a DownloadProgressWidget already exists
                first_progress = self.query_one(DownloadProgressWidget)
            except NoMatches:
                pass

            # Create a new download progress widget and mount it
            download_progress = DownloadProgressWidget(extension=extension)
            progress_list.mount(download_progress, before=first_progress)
