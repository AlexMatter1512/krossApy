import json
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
def getReservationsDict(response, simplified=False):
    """Get reservations data from HTML response.
    
    Args:
        response: HTTP response containing HTML
        simplified (bool): If True, returns headers and data separately
            
    Returns:
        dict: Either {"headers": [...], "data": [...]} or list of header-value dictionaries
        
    Raises:
        ValueError: If reservations table is not found
    """
    soup = BeautifulSoup(response.text, "html.parser")
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
            logger.info("Skipping row with empty code")
            continue
        
        if simplified:
            row_data = cells
        else:
            row_data = dict(zip(headers, cells))
        data.append(row_data)
    
    return {"headers": headers, "data": data} if simplified else data