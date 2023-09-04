import unittest
from unittest.mock import patch, MagicMock

# Import the function you want to test and any other necessary modules
from main import get_arithmetic_result, get_cell_coordinates, set_cell_value, get_cell_value


class TestGetCellCoordinates(unittest.TestCase):

    def test_get_cell_coordinates_valid_input(self):
        # Test the function with a valid cellid
        cellid = "A1"
        result = get_cell_coordinates(cellid)
        # Assert that the result is a tuple with the correct coordinates
        self.assertEqual(result, ("A", "1"))

    def test_get_cell_coordinates_invalid_input(self):
        # Test the function with an invalid cellid
        invalid_cellid = "X"
        with self.assertRaises(Exception) as context:
            get_cell_coordinates(invalid_cellid)
        # Assert that an exception with the correct message has been raised
        self.assertEqual(str(context.exception), "Error - Invalid cellid")


class TestGetArithmeticResult(unittest.TestCase):

    @patch('main.get_cell_value')
    def test_get_arithmetic_result_valid_expression(self, mock_get_cell_value):
        # Mock the get_cell_value function
        mock_get_cell_value.side_effect = lambda cell: {"A1": "2", "B2": "3"}.get(cell, 0)

        # Test the function with a valid arithmetic expression
        expression = "A1 + B2"
        result = get_arithmetic_result(expression)

        # Assert that the result is as expected
        self.assertEqual(result, "5")

    @patch('main.get_cell_value')
    def test_get_arithmetic_result_invalid_expression(self, mock_get_cell_value):
        # Mock the get_cell_value function
        mock_get_cell_value.side_effect = lambda cell: {"A1": "2", "B2": 3}.get(cell, 0)

        # Test the function with an invalid arithmetic expression
        invalid_expression = "A1 + X"
        with self.assertRaises(Exception) as context:
            get_arithmetic_result(invalid_expression)

        # Assert that an exception with the correct message has been raised
        self.assertEqual(str(context.exception), "Invalid Arithmetic Expression")


class TestSetCellValue(unittest.TestCase):

    def setUp(self):
        # Create a mock for the updateSpreadSheetDict function
        self.mock_update_spreadsheet = MagicMock()
        self.patcher = patch('main.updateSpreadSheetDict', self.mock_update_spreadsheet)
        self.patcher.start()

    def tearDown(self):
        # Stop the patcher to clean up
        self.patcher.stop()

    def test_set_cell_value_arithmetic(self):
        # Test when the value starts with '=', it should call get_arithmetic_result
        mock_get_arithmetic_result = MagicMock(return_value='10')
        with patch('main.get_arithmetic_result', mock_get_arithmetic_result):
            set_cell_value('A1', '=A2+A3')
            mock_get_arithmetic_result.assert_called_once_with('A2+A3')
            self.mock_update_spreadsheet.assert_called_once_with('A1', '10')

    def test_set_cell_value_numeric(self):
        # Test when the value is a valid numeric string
        set_cell_value('A2', '42.42')
        self.mock_update_spreadsheet.assert_called_once_with('A2', '42.42')

    def test_set_cell_value_invalid_number(self):
        # Test when the value is not a valid numeric string
        with self.assertRaises(Exception):
            set_cell_value('A3', 'invalid')


class TestGetCellValue(unittest.TestCase):

    def setUp(self):
        # Create a mock for the get_cell_coordinates function
        self.mock_get_cell_coordinates = MagicMock(return_value=('A', '1'))
        self.patcher = patch('main.get_cell_coordinates', self.mock_get_cell_coordinates)
        self.patcher.start()

    def tearDown(self):
        # Stop the patcher to clean up
        self.patcher.stop()

    def test_get_cell_value_valid_cellid(self):
        # Test when a valid cellId is provided
        spreadSheetDict = {'A': {'1': '42'}}
        with patch('main.spreadSheetDict', spreadSheetDict):
            result = get_cell_value('A1')
            self.mock_get_cell_coordinates.assert_called_once_with('A1')
            self.assertEqual(result, '42')

    def test_get_cell_value_default_value(self):
        # Test when an invalid cellId is provided, it should return '0'
        with self.assertRaises(Exception):
            get_cell_value('invalid_cell')


if __name__ == '__main__':
    unittest.main()
