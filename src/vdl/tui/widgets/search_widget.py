"""
Module: vdl.tui.widgets.SearchWidget
Provides a search input widget with a query field and a search button.
"""

from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, Input, Static


class SearchWidget(Widget):
    """
    A widget that provides a search interface with an input field and a search button.

    Features:
    - A labeled query input field.
    - A "Search" button for triggering search actions.
    """

    BINDINGS = [
        ('enter', 'enter_pressed'),
    ]

    def compose(self) -> ComposeResult:
        """
        Composes the UI components for the search widget.

        Yields:
            ComposeResult: The composed UI components, including:
                - A static label for the query.
                - An input field for entering the search query.
                - A button to trigger the search action.
        """
        with Horizontal():
            # Label for the input field
            yield Static('Query:', classes='hatch')
            # Input field for the query
            yield Input(placeholder='Publisher or Extension Name...',
                        id='search_query')
            # Search button
            yield Button('Search',
                         disabled=True,
                         id='search_button',
                         variant='success')

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Handles input change events. Triggers actions based on input IDs.

        Args:
            event (Input.Changed): The input change event.
        """
        if event.input.id == "search_query":
            # Retrieve the search query value
            search_query = event.input.value

            # Enable the search button if the search query is not empty
            search_button: Button = self.query_one("#search_button")
            search_button.disabled = not bool(search_query != '')

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter" and self.query_one("#search_query").has_focus:
            search_button: Button = self.query_one('#search_button')
            search_button.press()
            self.post_message(Button.Pressed(search_button))