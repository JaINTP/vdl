"""
Module: vdl.downloader.vsix_api_handler
Provides an asynchronous handler for interacting with the Visual Studio Marketplace API.


TODO: Add query result cacheing with expiration mechanic to save on unneeded queries.
"""

import httpx
import asyncio
from asyncio import Event
from vdl.models import Extension


class VsixApiHandler:
    """
    A handler for interacting with the Visual Studio Marketplace API asynchronously.

    Features:
    - Asynchronous API calls to fetch extensions.
    - Ability to cancel ongoing API requests.
    """

    API_URL = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json;api-version=3.0-preview.1",
    }

    def __init__(self):
        """
        Initializes the VsixApiHandler with a stop event for canceling requests.
        """
        self._stop_event = Event()

    def stop(self):
        """
        Cancels any ongoing requests by setting the stop event.
        """
        self._stop_event.set()

    async def _call_api(self, payload, timeout=10):
        """
        Makes an asynchronous POST request to the Visual Studio Marketplace API.

        Args:
            payload (dict): The payload for the POST request.
            timeout (int): Timeout in seconds for the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            Exception: If the request fails or is canceled.
        """
        self._stop_event.clear()  # Reset the stop event before starting
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(self.API_URL, json=payload, headers=self.HEADERS)

                if self._stop_event.is_set():
                    raise asyncio.CancelledError("Request was canceled by user.")

                response.raise_for_status()
                return response.json()
            except httpx.RequestError as exc:
                raise Exception(f"An HTTP request error occurred: {exc}") from exc
            except httpx.TimeoutException:
                raise Exception("The request timed out.")
            except asyncio.CancelledError:
                print("Request was canceled.")
                return None

    @staticmethod
    def _build_query(filter_type, value, page_number=1, page_size=10):
        """
        Constructs the payload for the API query.

        Args:
            filter_type (int): The filter type (e.g., 4 for publisher, 10 for extension name).
            value (str): The value to filter by.
            page_number (int): The page number to fetch.
            page_size (int): The number of results per page.

        Returns:
            dict: The constructed query payload.
        """
        return {
            "filters": [
                {
                    "criteria": [
                        {"filterType": filter_type, "value": value}
                    ],
                    "pageNumber": page_number,
                    "pageSize": page_size,
                    "sortBy": 0,
                    "sortOrder": 0,
                }
            ],
            "assetTypes": [],
            "flags": 514,
        }

    @staticmethod
    def _parse_results(data):
        """
        Parses the API results into a list of Extension objects.

        Args:
            data (dict): The API response JSON.

        Returns:
            list[Extension]: A list of parsed Extension objects.

        Raises:
            ValueError: If the response data is invalid or incomplete.
        """
        extensions = []
        try:
            results = data["results"][0]["extensions"]
            for ext in results:
                publisher_name = ext["publisher"]["publisherName"]
                domain = ext["publisher"].get("domain", "marketplace.visualstudio.com")
                last_updated = ext.get("lastUpdated", "Unknown")
                extension_name = ext["extensionName"]
                display_name = ext.get("displayName", "N/A")
                description = ext.get("shortDescription", "No description available.")
                version_data = ext["versions"][0]
                version = version_data["version"]
                download_url = next(
                    (file["source"] for file in version_data["files"] if file["assetType"] == "Microsoft.VisualStudio.Services.VSIXPackage"),
                    None
                )

                extensions.append(Extension(
                    publisher=publisher_name,
                    domain=domain,
                    name=extension_name,
                    display_name=display_name,
                    last_updated=last_updated,
                    description=description,
                    version=version,
                    download_url=download_url,
                ))
        except (KeyError, IndexError):
            raise ValueError("Failed to extract extension information from the API response.")
        return extensions

    async def search_extensions(self, query, by_publisher=False, page_size=10, page_number=1):
        """
        Asynchronously searches for extensions by publisher or extension name.

        Args:
            query (str): The search query (publisher or extension name).
            by_publisher (bool): Whether to search by publisher name. Defaults to False.
            page_size (int): Number of results per page. Defaults to 10.
            page_number (int): Page number to fetch. Defaults to 1.

        Returns:
            list[Extension]: A list of matching extensions.
        """
        filter_type = 4 if by_publisher else 10
        payload = self._build_query(filter_type, query, page_number, page_size)
        data = await self._call_api(payload)
        return self._parse_results(data) if data else []