from typing import List, Tuple
import json
from krossApy.data.Reservation import Reservation


class Reservations:
    data: Tuple[Reservation, ...]  # list of reservations
    total: int  # total number of reservations matching the filters
    total_pages: int  # total number of pages
    current_page: int  # current page number
    current_page_total: int  # number of reservations on the current page (may be less than per_page e.g. on the last page)

    _api = None  # KrossAPI instance
    _applied_filters: str  # filters applied to the request (cannot be changed, a new request must be made)
    _fields: List[
        str
    ]  # columns to return in the response (cannot be changed, a new request must be made)
    _original_zt4_data: dict  # original zt4 data used to make the request

    def __init__(
        self,
        api,
        data: tuple,
        pages: int,
        current_page: int,
        total: int,
        filters: str,
        fields: List[str],
    ):
        self.data = data
        self.total = total
        self.total_pages = pages
        self.current_page = current_page
        self.current_page_total = len(data)
        self._api = api
        self._applied_filters = filters
        self._fields = fields

    def __getitem__(self, item):
        """
        Get a reservation by index

        Args:
            item (int): The index of the reservation to get

        Returns:
            dict: The reservation data
        """
        try:
            return self.data[item]
        except IndexError:
            raise IndexError(f"Reservation at index {item} does not exist.")
        except Exception as e:
            raise ValueError(f"Failed to get reservation at index {item}: {str(e)}") from e

    def __iter__(self):
        """
        Iterate over the reservations

        Returns:
            iterator: An iterator over the reservations
        """
        return iter(self.data)

    @property
    def _plain_data(self):
        """
        Get the plain data of the reservations

        Returns:
            list: The plain data of the reservations
        """
        return [reservation.data for reservation in self.data]

    def page(self, page_number: int):
        """
        Move to a different page of reservations

        Args:
            page_number (int): The page number to move to
        """
        try:
            new_res = self._api.get_reservations(
                filters=self._applied_filters, fields=self._fields, page=page_number
            )
            for attr in [
                "data",
                "total",
                "total_pages",
                "current_page",
                "current_page_total",
            ]:
                setattr(self, attr, getattr(new_res, attr))
        except Exception as e:
            raise ValueError(f"Failed to move to page {page_number}: {str(e)}") from e

    def all(self):
        """
        Return all reservations in a single dictionary
        """
        pass

    def json(self):
        """
        Return reservations data in JSON format
        """
        return json.dumps(self._plain_data, indent=2)

    def next(self):
        """
        Move to the next page of reservations
        """
        if self.current_page:
            self.page(self.current_page + 1)

    def __str__(self):  # this can be used like: print(reservations)
        """
        Print reservations data
        """
        return self.json()

    @property  # this can be used like: print(reservations.info)
    def info(self):
        """
        Print reservations metadata
        """
        return json.dumps(
            {
                "api": str(self._api),
                "total": self.total,
                "total_pages": self.total_pages,
                "current_page": self.current_page,
                "current_page_total": self.current_page_total,
                "applied_filters": self._applied_filters,
                "columns": self._fields,
            },
            indent=2,
        )

    @property
    def simple_data(self):
        # turn a [{key: value, key: value, ...}, ...] list into a {keys: [key, key, ...], values: [[value, value, ...], ...]} dict
        headers = list(self.data[0].data.keys())
        data = [[row[header] for header in headers] for row in self.data]
        return {"keys": headers, "values": data}
