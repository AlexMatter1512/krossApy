from krossApy.data.Reservation import Reservation
from .custom_fields_handlers import CUSTOM_FIELDS_HANDLERS
from .custom_types_handlers import retype_fields

from ..scraper import scraper
from ..data import Fields, CustomFields, Field
from ..data.Reservations import Reservations
from ..data.Errors import KrossAPIError, LoginError, ConfigurationError

from typing import Dict, List, Optional, Union, Any
import requests
import logging
from dataclasses import dataclass
from http import HTTPStatus
import json
import base64

logger = logging.getLogger(__name__)

BASE_FIELDS = [
    Fields.CODE,
    Fields.LABEL,
    Fields.NIGHTS,
    Fields.ARRIVAL,
    Fields.DEPARTURE,
    Fields.N_ROOMS,
    Fields.ROOMS,
    Fields.N_BEDS,
    Fields.DATE_RESERVATION,
    Fields.LAST_UPDATE,
    Fields.CHANNEL,
    Fields.STATUS,
    Fields.TELEPHONE,
    Fields.GUEST_PORTAL_LINK,
]

@dataclass
class KrossConfig:
    """Configuration for KrossAPI"""

    base_url_template: str = "https://{}.krossbooking.com"
    login_path: str = "/login/v2"
    reservations_path: str = "/v2/reservations?lang=en"


class KrossAPI:
    def __init__(
        self, hotel_id: Optional[str] = None, config: Optional[KrossConfig] = None
    ):
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
            logger.debug(
                "Initial cookies received: %s", self.session.cookies.get_dict()
            )

            # Step 2: Actual Login
            payload = {"username": username, "password": password}
            response = self.session.post(login_url, data=payload)
            logger.debug("Login response: %s", response.text)

            if response.status_code != HTTPStatus.OK:
                raise LoginError(
                    f"Login failed with status code: {response.status_code}"
                )

            if err := response.json().get("login_error"):
                raise LoginError("Login failed: " + err)

            self.logged_in = True
            logger.debug(
                "Login successful, cookies: %s", self.session.cookies.get_dict()
            )

        except requests.RequestException as e:
            raise LoginError(f"Login request failed: {str(e)}") from e

    def _check_authentication(self) -> None:
        """Check if the client is authenticated."""
        if not self.logged_in:
            raise LoginError("You must login before making requests")
        
    def _direct_reservations_request(
        self, zt4_data: Dict[str, Any], name: str = ""
    ) -> requests.Response:
        """
        Make a direct request to get reservations data.

        Args:
            zt4_data: The data to send in the request

        Returns:
            Response from the server containing reservation data

        Raises:
            LoginError: If not logged in
            requests.RequestException: If the request fails
        """
        self._check_authentication()
        reservation_url = f"{self.base_url}{self.config.reservations_path}?"

        json_str = json.dumps(zt4_data)

        try:
            data = {"zt4_data": json_str}
            logger.debug(f"{name} Request data: {data}")

            request = requests.Request("POST", reservation_url, data=data)
            prepared_request = self.session.prepare_request(request)
            logger.debug(f"{name} Direct Request Body: %s", prepared_request.body)

            response = self.session.send(prepared_request)

            response.raise_for_status()
            return response

        except requests.RequestException as e:
            # logger.error("Failed to fetch reservations: %s", str(e))
            logger.error(f"Failed to fetch reservations ({name}): {str(e)}")
            raise

    def _csv_reservations_request(self) -> requests.Response:
        zt4b64_raw = json.dumps({"id": "reservations", "dwn": "csv"})
        queryString = {'zt4b64': base64.b64encode(zt4b64_raw.encode()).decode()}
        logger.debug(f"CSV Request data: {queryString}")
        response = self.session.get(f"{self.base_url}{self.config.reservations_path}", params=queryString)
        # logger.debug(f"CSV Response: {response.text}")
        return response

    def request_reservations(
        # self, filters: Dict[str, Any] = None, columns: List[str] = ["cod_reservation"]
        self,
        filters: List[str] = None,
        columns: List[str] = ["cod_reservation"],
        page: int = None,
        csv: bool = False,
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

        base_zt4_data = {
            "id": "reservations",
            "sort": ",arrival asc,",
            "text": "",
            "refresh_ajax": True,
        }

        if "cod_reservation" in columns:
            columns.remove("cod_reservation")
        columns.insert(0, "cod_reservation")

        # reset request to start from scratch
        reset_zt4_data = base_zt4_data.copy() | {"reset": True}
        self._direct_reservations_request(reset_zt4_data, "Reset")

        # remove base filters
        remove_filters_zt4_data = base_zt4_data.copy() | {"filters_remove": 0}
        self._direct_reservations_request(remove_filters_zt4_data, "Remove Filters")

        for filter in filters or []:
            filter_zt4_data = base_zt4_data.copy() | {"filters": filter}
            self._direct_reservations_request(filter_zt4_data, "Filter")

        # actual request
        zt4_data = (
            base_zt4_data.copy()
            | {"columns": columns}
            # | ({"filters": filters} if filters else {})
        )

        response = self._direct_reservations_request(zt4_data)

        # at this point, we have the first page of reservations with the desired columns and filters. 
        # csv is the chosen method to get the full data and we can return the response since we don't care about pagination
        if csv:
            return self._csv_reservations_request()

        if page:
            zt4_data_page = zt4_data.copy() | {"page": page - 1}
            response = self._direct_reservations_request(zt4_data_page)

        return response

    def get_reservations(
        self,
        filters: List[str] = None,
        fields: List[Field] = BASE_FIELDS,
        page: int = 1,
        full: bool = True,
    ) -> Reservations:
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
        # Split fields into custom and standard fields using set operations
        field_set = set(fields)
        logger.debug("Field set: %s", field_set)

        all_custom_field_values = {field.value for field in CustomFields}
        logger.debug("Custom field values: %s", all_custom_field_values)

        custom_fields = field_set.intersection(all_custom_field_values)
        logger.debug("Custom fields: %s", custom_fields)

        standard_fields = field_set - custom_fields

        # Map standard fields to their request values
        # request_fields = [field.value[_Field_Idx.REQUEST] for field in standard_fields]
        request_fields = [field.REQUEST for field in standard_fields]

        try:
            response = self.request_reservations(filters, request_fields, page, csv=full)
            data_tuple, total = scraper.getReservationsTuple(response, csv=full)
            data = tuple(Reservation(r) for r in data_tuple)

            reservations = Reservations(
                api=self,
                data=data,
                pages=None,
                current_page=None if full else page,
                total=total,
                filters=filters,
                fields=fields,
            )
            if custom_fields:
                logger.debug("Applying custom fields handlers")
                for field in custom_fields:
                    # get the handler for the custom field
                    handler = CUSTOM_FIELDS_HANDLERS.get(field)
                    logger.debug("Handler for %s: %s", field, handler)
                    if handler:
                        # apply the handler to the reservations
                        reservations = handler(reservations)

            reservations = retype_fields(reservations)

            return reservations

        except Exception as e:
            logger.error("Failed to get reservations: %s", str(e))
            logger.debug("response: %s", response.text)
            raise KrossAPIError(
                f"Failed to get reservations (see debug log): {str(e)}"
            ) from e

    def __enter__(self):
        """Support for context manager protocol"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when used as context manager"""
        self.session.close()
