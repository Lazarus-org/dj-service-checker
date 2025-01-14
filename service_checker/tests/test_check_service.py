import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch, MagicMock
from service_checker.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
import sys
import requests

pytestmark = [
    pytest.mark.check_service,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]

class TestCheckServiceCommand:
    """
    Test suite for the `check_service` management command, ensuring it correctly checks service availability
    and handles various scenarios.
    """

    @patch('requests.get')
    def test_service_available(self, mock_get):
        """
        Test that the command correctly identifies an available service.

        Asserts:
        -------
        - The success message is displayed when the service responds with status code 200.
        - The response time is measured and included in the output.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch('sys.stdout.write') as mock_stdout:
            call_command('check_service', 'https://example.com')
            mock_stdout.assert_any_call("Service at https://example.com is available! Response time: 0.00 ms\n")


    @patch('requests.get')
    def test_service_unavailable(self, mock_get):
        """
        Test that the command handles services responding with non-200 status codes.

        Asserts:
        -------
        - A warning message is displayed with the status code.
        """
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_get.return_value = mock_response

        with patch('sys.stdout.write') as mock_stdout:
            call_command('check_service', 'https://example.com')
            mock_stdout.assert_any_call("Service at https://example.com responded with status: 503. Response time: 0.00 ms\n")


    def test_missing_url_argument(self):
        """
        Test that the command raises a CommandError if the required URL argument is missing.

        Asserts:
        -------
        - A CommandError is raised when the `url` argument is not provided.
        """
        with pytest.raises(CommandError, match="Error: the following arguments are required: url"):
            call_command('check_service')

    @patch('requests.get')
    def test_request_exception_handling(self, mock_get):
        """
        Test that the command handles request exceptions gracefully.

        Asserts:
        -------
        - An error message is displayed when a RequestException occurs.
        """
        # Simulate a requests.RequestException being raised
        mock_get.side_effect = requests.RequestException("Connection error")

        with patch('sys.stdout.write') as mock_stdout:
            call_command('check_service', 'https://example.com')
            mock_stdout.assert_called_with('Failed to check service at https://example.com: Connection error\n')


    @patch('requests.get')
    def test_custom_timeout(self, mock_get):
        """
        Test that the command correctly uses a custom timeout value.

        Asserts:
        -------
        - The request is made with the specified timeout.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        call_command('check_service', 'https://example.com', '--timeout', 5)
        mock_get.assert_called_with('https://example.com', timeout=5)

    @patch('requests.get')
    def test_response_time_calculation(self, mock_get):
        """
        Test that the command calculates and includes response time in the output.

        Asserts:
        -------
        - The response time is included in the success or warning messages.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch('time.time', side_effect=[1, 1.5]):  # Simulate response time of 0.5 seconds
            with patch('sys.stdout.write') as mock_stdout:
                call_command('check_service', 'https://example.com')
                mock_stdout.assert_any_call("Service at https://example.com is available! Response time: 500.00 ms\n")

