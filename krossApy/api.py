from enum import StrEnum
from . import scraper

from typing import Dict, List, Optional, Union, Any
import requests
import logging
import urllib.parse
from dataclasses import dataclass
from http import HTTPStatus
import json

logger = logging.getLogger(__name__)

# TODO: Move errors to a separate module
class KrossAPIError(Exception):
    """Base exception for KrossAPI errors"""
    pass

class LoginError(KrossAPIError):
    """Raised when login fails"""
    pass

class ConfigurationError(KrossAPIError):
    """Raised when configuration is invalid"""
    pass

class Fields(StrEnum):
    """Enum for reservation fields"""
    CODE = "cod_reservation"
    LABEL = "label"
    ARRIVAL = "arrival"
    NIGHTS = "nights"
    DEPARTURE = "departure"
    N_ROOMS = "n_rooms"
    ROOMS = "rooms"
    N_BEDS = "n_beds"
    DATE_RESERVATION = "date_reservation"
    LAST_UPDATE = "last_update"
    CHANNEL = "channel"
    DATE_EXPIRATION = "date_expiration" 
    EMAIL = "email"
    TELEPHONE = "tel"
    GUEST_PORTAL_LINK = "guest_portal"
    STATUS = "name_reservation_status"

@dataclass
class KrossConfig:
    """Configuration for KrossAPI"""
    base_url_template: str = "https://{}.krossbooking.com"
    login_path: str = "/login/v2"
    reservations_path: str = "/v2/reservations"

class KrossAPI:
    def __init__(self, hotel_id: Optional[str] = None, config: Optional[KrossConfig] = None):
        """
        Initialize KrossAPI client.

        Args:
            hotel_id: The hotel identifier for the Krossbooking website
            config: Optional configuration object
        """
        self.session = requests.Session()
        self.config = config or KrossConfig()
        self.logged_in = False
        self._base_url: Optional[str] = None
        
        if hotel_id:
            self.set_hotel(hotel_id)

    def set_hotel(self, hotel_id: str) -> None:
        """
        Set the hotel_id for the Krossbooking website.

        Args:
            hotel_id: The hotel identifier
        
        Raises:
            ConfigurationError: If hotel_id is empty or invalid
        """
        if not hotel_id or not isinstance(hotel_id, str):
            raise ConfigurationError("Hotel ID must be a non-empty string")
        
        self._base_url = self.config.base_url_template.format(hotel_id)
        self.hotel_id = hotel_id
        # Reset login state when hotel changes
        self.logged_in = False

    @property
    def base_url(self) -> str:
        """
        Get the base URL for API requests.

        Raises:
            ConfigurationError: If hotel_id hasn't been set
        """
        if not self._base_url:
            raise ConfigurationError("Hotel ID must be set before making requests")
        return self._base_url

    def login(self, username: str, password: str) -> None:
        """
        Login to the Krossbooking website and store the session.

        Args:
            username: The username to login with
            password: The password to login with

        Raises:
            LoginError: If login fails
            ConfigurationError: If hotel_id isn't set
        """
        login_url = f"{self.base_url}{self.config.login_path}"
        
        # Step 1: Initial request to receive login cookies
        try:
            self.session.get(login_url)
            logger.debug("Initial cookies received: %s", self.session.cookies.get_dict())

            # Step 2: Actual Login
            payload = {"username": username, "password": password}
            response = self.session.post(login_url, data=payload)
            
            if response.status_code != HTTPStatus.OK:
                raise LoginError(f"Login failed with status code: {response.status_code}")
            
            self.logged_in = True
            logger.debug("Login successful, cookies: %s", self.session.cookies.get_dict())
            
        except requests.RequestException as e:
            raise LoginError(f"Login request failed: {str(e)}") from e

    def _check_authentication(self) -> None:
        """Check if the client is authenticated."""
        if not self.logged_in:
            raise LoginError("You must login before making requests")

    @staticmethod
    def build_filter_string(filters: Dict[str, Any]) -> str:
        """
        Convert a dictionary of filters to a URL-encoded string.

        Args:
            filters: Dictionary of filter parameters

        Returns:
            URL-encoded filter string
        """
        try:
            encoded_filters = urllib.parse.urlencode(filters)
            logger.debug("Encoded filters: %s", encoded_filters)
            return encoded_filters
        except Exception as e:
            raise ValueError(f"Invalid filter format: {str(e)}") from e

    def request_reservations(
        self, 
        filters: Dict[str, Any] = None,
        columns: List[str] = ["cod_reservation"]
    ) -> requests.Response:
        """
        Make an authenticated request to get reservations data.

        Args:
            filters: The filters to apply to the request
            columns: The columns to return in the response

        Returns:
            Response from the server containing reservation data

        Raises:
            LoginError: If not logged in
            requests.RequestException: If the request fails
        """
        self._check_authentication()
        
        if "cod_reservation" in columns:
            columns.remove("cod_reservation")
        columns.insert(0, "cod_reservation")
        
        reservation_url = f"{self.base_url}{self.config.reservations_path}?"

        zt4_data = {
            "id": "reservations",
            "sort": ",arrival asc,",
            "text": "",
            "refresh_ajax": True,
            "columns": columns,
        }
        if filters:
            filter_string = self.build_filter_string(filters)
            zt4_data["filters"] = filter_string
            
        json_str = json.dumps(zt4_data)

        try:
            data = {"zt4_data": json_str}
            logger.debug("Request data: %s", data)

            request = requests.Request("POST", reservation_url, data=data)
            prepared_request = self.session.prepare_request(request)
            logger.debug("Request Body: %s", prepared_request.body)

            response = self.session.send(prepared_request)
            
            response.raise_for_status()
            return response
            
        except requests.RequestException as e:
            logger.error("Failed to fetch reservations: %s", str(e))
            raise

    def get_reservations(
        self, 
        filters: Dict[str, Any] = None,
        fields: List[str] = ["cod_reservation"],
        simplified: bool = False
    ) -> Union[Dict, str]:
        """
        Get reservations data with optional simplification.

        Args:
            filters: The filters to apply to the request
            columns: The columns to return in the response
            simplified: If True, returns simplified format

        Returns:
            Reservations data in dictionary or JSON format

        Raises:
            KrossAPIError: If the request fails
        """
        try:
            response = self.request_reservations(filters, fields)
            return scraper.getReservationsDict(response, simplified)
        except Exception as e:
            logger.debug("response: %s", response.text)
            raise KrossAPIError(f"Failed to get reservations (see debug log): {str(e)}") from e

    def __enter__(self):
        """Support for context manager protocol"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when used as context manager"""
        self.session.close()