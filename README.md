
# Simple Spreadsheet Backend in Python

This is a simple Python-based spreadsheet backend that allows you to set and retrieve values for cells identified by their IDs. It supports two main operations:

1. `set_cell_value(cellid: str, value: str)`: Sets the value of a cell identified by `cellid` to the provided `value`. The `value` can be a numeric value or an arithmetic expression (starting with '=').

2. `get_cell_value(cellid: str) -> str`: Retrieves the value of a cell identified by `cellid`. If the cell contains an arithmetic expression, it evaluates the expression and returns the result as a string.

## Example

Here's how you can use this simple spreadsheet backend in Python:

```python
# Create a new spreadsheet backend
spreadsheet = {}

# Set cell values
set_cell_value('A1', '13')
set_cell_value('A2', '14')

# Retrieve cell values
cell_value_1 = get_cell_value('A1')  # Returns '13'
cell_value_2 = get_cell_value('A2')  # Returns '14'

# Set cell A3 with an arithmetic expression "=A1+A2"
set_cell_value('A3', '=A1+A2')

# Retrieve the value of cell A3 (evaluates the expression)
cell_value_3 = get_cell_value('A3')  # Returns '27'

# Set cell A4 with a more complex expression "=A1+A2+A3"
set_cell_value('A4', '=A1+A2+A3')

# Retrieve the value of cell A4 (evaluates the expression)
cell_value_4 = get_cell_value('A4')  # Returns '54'
```

## Usage

You can integrate this simple spreadsheet backend into your Python project by using the `set_cell_value` and `get_cell_value` functions as shown in the example above.

```python
# Create a new spreadsheet backend (a dictionary)
spreadsheet = {}

# Set cell values
set_cell_value('A1', '13')
set_cell_value('A2', '14')

# Retrieve cell values
cell_value_1 = get_cell_value('A1')
cell_value_2 = get_cell_value('A2')

# ... continue using the spreadsheet ...
```

## Testing

To validate the code and ensure it works as expected, you can write unit tests using Python's built-in `unittest` framework or any other testing framework of your choice.

Here's an example of using Python's `unittest`:

```python
import unittest

class TestSpreadsheetBackend(unittest.TestCase):

    def test_set_and_get_cell_value(self):
        # Create a new spreadsheet backend (a dictionary)
        spreadsheet = {}

        # Set cell values
        set_cell_value('A1', '13')
        set_cell_value('A2', '14')

        # Retrieve cell values and assert
        self.assertEqual(get_cell_value('A1'), '13')
        self.assertEqual(get_cell_value('A2'), '14')

    def test_arithmetic_expression(self):
        # Create a new spreadsheet backend (a dictionary)
        spreadsheet = {}

        # Set cell values and an arithmetic expression
        set_cell_value('A1', '13')
        set_cell_value('A2', '14')
        set_cell_value('A3', '=A1+A2')

        # Retrieve the value of cell A3 (evaluates the expression)
        self.assertEqual(get_cell_value('A3'), '27')

if __name__ == '__main__':
    unittest.main()
```

In this example, two test cases are defined to test setting and retrieving cell values as well as evaluating arithmetic expressions.

## License

This spreadsheet backend is available under the [MIT License](LICENSE).

Feel free to adapt and extend this code as needed for your specific use case.
