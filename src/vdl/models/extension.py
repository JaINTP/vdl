"""
Module: vdl.models.extension
Defines the data model for an extension with validation and serialization capabilities.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class Extension(BaseModel):
    """
    Represents a downloadable extension with its metadata.

    Attributes:
        publisher (str): The publisher of the extension.
        domain (Optional[str]): The domain where the extension is hosted.
        name (str): The unique name of the extension.
        display_name (str): The human-readable name of the extension.
        last_updated (str): The last updated date of the extension in ISO format.
        description (Optional[str]): A short description of the extension.
        version (Optional[str]): The current version of the extension.
        download_url (Optional[str]): The URL for downloading the extension.
    """

    publisher: str = Field(..., description="The publisher of the extension")
    domain: Optional[str] = Field(None, description="The domain where the extension is hosted")
    name: str = Field(..., description="The unique name of the extension")
    display_name: str = Field(..., description="The display name of the extension")
    last_updated: str = Field(..., description="The last updated date of the extension")
    description: Optional[str] = Field(None, description="A short description of the extension")
    version: Optional[str] = Field(None, description="The current version of the extension")
    download_url: Optional[str] = Field(None, description="The URL to download the extension")

    def summary(self) -> str:
        """
        Returns a markdown-compatible, formatted summary of the extension.

        Returns:
            str: A formatted summary of the extension metadata.
        """
        try:
            # TODO: Add configurable datetime formatting.
            formatted_date = datetime.fromisoformat(self.last_updated).strftime("%B %d, %Y")
        except ValueError:
            formatted_date = "Not available"

        lines = [
            f"**{self.display_name} (v{self.version or 'N/A'})**",
            "",
            f"**Publisher:** {self.publisher}",
            f"**Domain:** {self.domain or 'Not specified'}",
            f"**Last Updated:** {formatted_date}",
            "",
            f"**Description:**",
            f"{self.description or 'No description available.'}",
        ]

        return "\n".join(lines)

    def to_dict(self) -> dict:
        """
        Converts the extension instance to a dictionary.

        Returns:
            dict: A dictionary representation of the extension.
        """
        return self.dict()

    def to_json(self) -> str:
        """
        Converts the extension instance to a JSON string.

        Returns:
            str: A JSON-formatted string representation of the extension.
        """
        return self.json(indent=4)

    class Config:
        """
        Pydantic configuration for the Extension model.

        Attributes:
            from_attributes (bool): Allows the model to populate fields from object attributes.
            populate_by_name (bool): Allows field names to be populated by alias names.
            arbitrary_types_allowed (bool): Enables support for arbitrary custom types.
            json_encoders (dict): Custom JSON encoders for specific types.
        """
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            # Add custom encoders if necessary
        }
