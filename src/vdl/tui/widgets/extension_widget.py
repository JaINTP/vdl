"""
Module: vdl.tui.widgets.extension_widget
Defines the widget for displaying an extension's details and a download button in the UI.
"""

from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal
from textual.geometry import Offset
from textual.widgets import Button, Collapsible, Markdown, Static

from vdl.models import Extension


class ExtensionWidget(Widget):
    """
    A widget for displaying extension details and providing a download button.

    Features:
    - Displays the extension's name and a button for initiating downloads.
    - Collapsible section for showing detailed information about the extension.

    Attributes:
        extension (Extension): The extension data model instance to display.
    """

    extension: Extension

    def __init__(self, extension: Extension, **kwargs) -> None:
        """
        Initializes the widget with the given extension.

        Args:
            extension (Extension): The extension whose details are displayed.
            **kwargs: Additional arguments passed to the parent Widget class.
        """
        self.extension = extension
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """
        Composes the UI components of the extension widget.

        Yields:
            ComposeResult: The composed UI components, including:
                - A horizontal layout for the name and download button.
                - A collapsible section for detailed extension information.
        """
        with Horizontal():
            yield Static("Name:", classes="static label")  # Label for the name
            yield Static(self.extension.name, classes="static name")  # Extension name
            yield Button("Download", id=f"{self.extension.name}_download_button")  # Download button

        with Collapsible(title="Information"):
            yield Markdown(markdown=self.extension.summary())  # Extension summary in Markdown format

    def on_mount(self) -> None:
        if self.first_of_type:
            self.query_one(Button).focus(True)