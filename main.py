import re

import numexpr

spreadSheetDict = {}


def updateSpreadSheetDict(cellid: str, value: str):
    """
    Update the spreadsheet dictionary with a new cell value.

    This function takes a cell ID (e.g., "A1") and a value and updates the content of the specified cell
    in the spreadsheet dictionary. If the column already exists in the dictionary, it updates the cell's
    value. If the column does not exist, it creates a new column and adds the cell with the specified value.

    Parameters:
    - cellid (str): The ID of the cell to update, in the format "A1" (column + row).
    - value (str): The new value to assign to the cell.

    Returns:
    None

    Example:
    >>> updateSpreadSheetDict('A1', '42')

    This example updates cell A1 in the spreadsheet dictionary with the value '42'.
    """
    coordinates = get_cell_coordinates(cellid)
    column = coordinates[0]
    row = coordinates[1]

    if column in spreadSheetDict:
        spreadSheetDict[column][row] = value
    else:
        cellDict = {row: value}
        spreadSheetDict[column] = cellDict


def get_cell_coordinates(cellid: str) -> tuple:
    """
    Extract and return the column and row coordinates from a cell ID.

    This function takes a cell ID (e.g., "A1") as input and uses a regular expression pattern to extract
    the column and row coordinates. It returns a tuple containing the column and row values.

    Parameters:
    - cellid (str): The ID of the cell in the format "A1" (column + row).

    Returns:
    tuple: A tuple containing two elements - the column (string) and row (string) coordinates.

    Raises:
    Exception: If the provided cell ID is invalid or does not match the expected format.

    Example:
    >>> get_cell_coordinates('A1')
    ('A', '1')

    This example extracts the column 'A' and row '1' from the cell ID 'A1'.
    """
    pattern = re.compile("([A-Z])([0-9]+)")
    cell = pattern.search(cellid)
    if cell:
        return cell.group(1), cell.group(2)
    else:
        raise Exception("Error - Invalid cellid")


def get_arithmetic_result(exp: str) -> str:
    """
    Evaluate an arithmetic expression with cell references and return the result as a string.

    This function takes an arithmetic expression as input, which may include cell references in the format
    "A1," "B2," etc. It replaces these cell references with their corresponding values from the spreadsheet
    and evaluates the resulting expression. The result is returned as a string.

    Parameters:
    - exp (str): The arithmetic expression to be evaluated.

    Returns:
    str: The result of the arithmetic expression as a string.

    Raises:
    Exception: If there is an error during evaluation or if the expression is invalid.

    Example:
    >>> get_arithmetic_result('2 * A1 + B2')
    '86.5'

    This example evaluates the expression '2 * A1 + B2' by substituting the values of cells A1 and B2
    from the spreadsheet and returns '86.5' as the result.
    """
    pattern = r"\b([A-Z]{1}\d+)\b"
    string_rep_expression = re.sub(pattern, lambda match: get_cell_value(match.group(1)), exp)
    try:
        result = numexpr.evaluate(string_rep_expression).item()
    except Exception:
        raise Exception("Invalid Arithmetic Expression")

    return str(result)


def set_cell_value(cellid: str, value: str):
    """
    Set the value of a cell in the spreadsheet based on the provided input.

    This function sets the value of a cell in the spreadsheet based on the provided `cellid` and `value`. If
    the `value` starts with '=', it is treated as an arithmetic expression and evaluated using the
    `get_arithmetic_result` function before updating the cell. If the `value` is a valid numeric string, it is
    directly assigned to the cell. Otherwise, an exception is raised.

    Parameters:
    - cellid (str): The ID of the cell to update in the format "A1" (column + row).
    - value (str): The new value to assign to the cell.

    Returns:
    None

    Raises:
    Exception: If the provided `value` is not a valid numeric string or if there is an error in evaluating
               an arithmetic expression.

    Example:
    >>> set_cell_value('A1', '42')
    >>> set_cell_value('B2', '=A1 + 10')
    >>> set_cell_value('C3', 'invalid_value')

    These examples set the values of cells A1, B2, and C3 based on the provided input. Cell A1 is directly set
    to '42', cell B2 is set to the result of the arithmetic expression '=A1 + 10' (e.g., '52'), and an exception
    is raised for cell C3 due to the 'invalid_value'.
    """
    if value.startswith('='):
        value = get_arithmetic_result(value[1:])
        updateSpreadSheetDict(cellid, value)

    else:
        if value.replace('.', '').isdigit():
            updateSpreadSheetDict(cellid, value)
        else:
            raise Exception("Invalid Number")


def get_cell_value(cellid: str):
    """
    Retrieve the value of a cell in the spreadsheet.

    This function retrieves the value of a cell in the spreadsheet based on the provided `cellid`. The `cellid`
    represents the location of the cell in the spreadsheet (e.g., "A1" for the cell in column A and row 1).
    If the specified cell exists in the spreadsheet, its value is returned. If the cell does not exist, the
    function returns the default value '0'.

    Parameters:
    - cellid (str): The ID of the cell to retrieve in the format "A1" (column + row).

    Returns:
    str: The value of the specified cell as a string.

    Raises:
    Exception: If the provided `cellid` is empty or if there is an issue with accessing the spreadsheet.

    Example:
    >>> get_cell_value('A1')
    '42'

    This example retrieves the value of cell A1 in the spreadsheet and returns '42'. If cell A1 does not exist,
    it returns the default value '0'.
    """
    if cellid:
        coordinates = get_cell_coordinates(cellid)
        column = coordinates[0]
        row = coordinates[1]
        return spreadSheetDict[column].get(row, '0')
    raise Exception("Invalid cellId")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    set_cell_value('A3', '19.10')
    set_cell_value('A1', '12')
    set_cell_value('A2', '14')
    set_cell_value('B1', '=A1+A3')
    print(get_cell_value('B1'))
