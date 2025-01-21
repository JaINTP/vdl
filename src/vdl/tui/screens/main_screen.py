"""
Module: vdl.tui.screens.main_screen
Defines the main screen for the VSIX Downloader application using Textual's framework.
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import VerticalScroll
from textual.widgets import Button, Footer, Header, Rule

from vdl.tui.widgets import DownloadProgressWidget, SearchWidget


class MainScreen(Screen):
    """
    The main screen for the VSIX Downloader application.

    Features:
    - A header for the application title.
    - A search widget for user queries.
    - A scrollable list for displaying download progress widgets.
    - A footer for navigation or key binding hints.
    """

    def __init__(self) -> None:
        """
        Initializes the main screen.
        """
        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Composes the UI components of the main screen.

        Yields:
            ComposeResult: The composed UI components, including:
                - Header
                - SearchWidget for user queries
                - Rule for visual separation
                - VerticalScroll for download progress widgets
                - Footer
        """
        yield Header()
        yield SearchWidget(id="url_input", classes="hatch")
        yield Rule(classes="hatch")
        yield VerticalScroll(id="progress_list", classes="hatch")
        yield Footer()

    def on_mount(self) -> None:
        """
        Called when the screen is mounted. Configures the progress list container.
        """
        progress_list = self.query_one("#progress_list", VerticalScroll)
        progress_list.show_vertical_scrollbar = True
