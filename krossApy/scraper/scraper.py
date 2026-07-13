from typing import List
from bs4 import BeautifulSoup
import logging

#csv parsing
import csv

logger = logging.getLogger(__name__)
def getReservationsTuple(response, simplified=False, csv=False) -> tuple[dict, int]:
    """Get reservations data from HTML response.
    
    Args:
        response: HTTP response containing HTML
        simplified (bool): If True, returns headers and data separately
            
    Returns:
        tuple: Reservations data and total number of reservations
        
    Raises:
        ValueError: If reservations table is not found
    """
    if csv:
        return scrapeCsv(response)
    return scrapeHtml(response)
    
def scrapeCsv(csv_response) -> tuple[list[dict], int]:
    """Scrape CSV response for reservations data."""
    reader = csv.DictReader(csv_response.text.splitlines())
    headers = reader.fieldnames

    data = []
    for row in reader:
        cleaned_row = {}
        for k, v in row.items():
            if isinstance(v, list):
                cleaned_row[k] = ', '.join(x.strip() for x in v if x)
            elif isinstance(v, str):
                cleaned_row[k] = v.strip()
            else:
                cleaned_row[k] = v
        data.append(cleaned_row)

    return data, len(data)
    
def scrapeHtml(response) -> tuple[dict, int]:
    """Scrape HTML response for reservations data.
    
    Args:
        response: HTTP response containing HTML
        
    Returns:
        dict: Reservations data
    """
    soup = BeautifulSoup(response.text, "html.parser")

    # try to find the span with class "t" 
    total = soup.find("span", class_="t")
    if total is None:
        logger.error("No total reservations found in response")
    else:
        total = int(total.text.strip())

    table = soup.find("table", id="reservations")
    
    if table is None:
        logger.error("No reservations table found in response")
        raise ValueError("No reservations table found")

    # Try both th and td for headers
    header_row = table.find("tr")
    headers = [h.text.strip() for h in header_row.find_all(["th", "td"])]
    
    # Find indices of non-empty headers
    valid_indices = [i for i, h in enumerate(headers) if h]
    headers = [headers[i] for i in valid_indices]
    
    if not headers:
        raise ValueError("No headers found in table")

    data = []
    for row in table.find_all("tr")[1:]:
        cells = [cell.text.strip() for cell in row.find_all("td")]
        
        # Skip rows with wrong number of cells
        if len(cells) < max(valid_indices, default=0) + 1:
            logger.warning(f"Skipping row with {len(cells)} cells (expected {len(headers)})")
            continue
            
        # Only keep cells corresponding to non-empty headers
        cells = [cells[i] for i in valid_indices]

        # the first cell is the code, if it is empty, skip the row
        if not cells[0]:
            logger.debug("Skipping row with empty code")
            continue
        
        row_data = dict(zip(headers, cells))
        data.append(row_data)
    
    return data, total
