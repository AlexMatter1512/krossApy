# Mapping of comparison operators to their string representations
OPERATOR_MAP = {
    '<': 'mi',
    '>': 'ma',
    '<=': 'miu',
    '>=': 'mau',
    '=': 'e',
    '==': 'e',
    '!=': 'd'
}

def get_operator_string(operator: str) -> str:
    """
    Convert comparison operator to its string representation
    
    Args:
        operator (str): The comparison operator (<, >, <=, >=, =, ==)
        
    Returns:
        str: The string representation of the operator
        
    Raises:
        KeyError: If the operator is not supported
    """
    return OPERATOR_MAP[operator]

def get_operator_from_string(operator_string: str) -> str:
    """
    Convert string representation back to comparison operator
    
    Args:
        operator_string (str): The string representation (mau, wau, mau_e, wau_e, e)
        
    Returns:
        str: The comparison operator
        
    Raises:
        ValueError: If the string representation is not recognized
    """
    for op, string in OPERATOR_MAP.items():
        if string == operator_string:
            return op
    raise ValueError(f"Unknown operator string: {operator_string}")
