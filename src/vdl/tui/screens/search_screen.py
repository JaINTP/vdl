"""
Module: vdl.tui.screens.search_screen
Provides a screen for displaying search results for extensions using Textual's framework.
"""

from typing import Dict

from textual import work
from textual._node_list import DuplicateIds
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Rule, Static

from vdl.downloader import VsixApiHandler
from vdl.tui.widgets import ExtensionWidget
from vdl.models import Extension


class SearchScreen(Screen):
    """
    A screen for displaying search results for extensions.

    Attributes:
        BINDINGS (list): Key bindings for the screen.
        api_handler (VsixApiHandler): Handles API interactions for fetching extensions.
        search_query (str): The query string used for searching extensions.
        extensions (Dict[str, Extension]): A dictionary of fetched extensions.
    """

    BINDINGS = [
        ('ctrl+b', 'back', 'Return to main screen.')
    ]

    api_handler: VsixApiHandler = None
    search_query: str
    extensions: Dict[str, Extension] = {}

    def __init__(self, search_query: str = None) -> None:
        """
        Initializes the search screen.

        Args:
            search_query (str): The search query for finding extensions. Defaults to None.
        """
        super().__init__()
        self.search_query = search_query
        self.api_handler = VsixApiHandler()

    def compose(self) -> ComposeResult:
        """
        Composes the UI components for the search screen.

        Yields:
            ComposeResult: The composed UI components, including:
                - Header
                - Query static display
                - A vertical scroll container for search results
                - Footer
        """
        yield Header()
        yield Static('Search results for extension:', classes='title hatch')
        yield Static(f'Query: {self.search_query}', classes='hatch')
        yield Rule()
        yield VerticalScroll(id='extension_container')
        yield Footer()

    async def on_mount(self) -> None:
        """
        Called when the screen is mounted. Starts fetching and displaying extensions.
        """
        self.query_one('#extension_container', VerticalScroll).loading = True
        self.populate_extensions()

    def action_back(self) -> None:
        """
        Handles the 'back' action. Stops API calls and dismisses the screen.
        """
        self.api_handler.stop()
        self.dismiss(None)

    @work
    async def populate_extensions(self) -> None:
        """
        Populates the vertical scroll container with extensions matching the search query.

        Fetches search results using the API handler and dynamically mounts widgets
        for each extension.
        """
        vertical = self.query_one('#extension_container', VerticalScroll)
        search_results = []

        if self.search_query:
            try:
                search_results = await self.api_handler.search_extensions(self.search_query)
            except Exception as e:
                self.notify(f'Exception searching for extensions: {e}')
                await asyncio.sleep(4)  # Allow the user to read the error
                self.dismiss(None)

        for extension in search_results:
            self.extensions[extension.name] = extension

            try:
                vertical.mount(ExtensionWidget(extension, id=extension.name))
            except DuplicateIds:
                pass

        vertical.loading = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles button press events. Detects if a download button is pressed and dismisses
        the screen with the corresponding extension.

        Args:
            event (Button.Pressed): The button press event.
        """
        if '_download_button' in event.button.id:
            extension_name = event.button.id.replace('_download_button', '')
            self.dismiss(self.extensions[extension_name])
