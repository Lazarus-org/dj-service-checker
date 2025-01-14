import requests
import time
from django.core.management.base import BaseCommand
import logging


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Django management command to check the availability of a given service URL.

    This command sends an HTTP GET request to the specified URL and reports its availability
    status along with the response time. It also supports configurable request timeouts and logs
    the process for debugging and auditing purposes.
    """

    help = "Check the availability of a service"

    def add_arguments(self, parser) -> None:
        """
        Add command-line arguments for the service checker command.

        Args:
            parser: An instance of argparse.ArgumentParser to define command-line arguments.
        """
        parser.add_argument(
            'url', 
            type=str, 
            help='The URL of the service to check'
        )
        parser.add_argument(
            '--timeout', 
            type=int, 
            default=10, 
            help='Timeout in seconds for the request (default: 10 seconds)'
        )

    def handle(self, *args, **options) -> None:
        """
        Handle the execution of the command.

        This method performs the following:
        1. Sends an HTTP GET request to the specified URL.
        2. Calculates the response time.
        3. Logs and displays the availability status of the service.

        Args:
            *args: Additional positional arguments.
            **options: Command-line options parsed as a dictionary.
        """
        url = options['url']
        timeout = options['timeout']

        try:
            # Track the start time
            start_time = time.time()

            logger.debug(f"start to send a get request to the url=[{url}]")

            # Send the request
            response = requests.get(url, timeout=timeout)

            # Calculate response time in milliseconds
            response_time = (time.time() - start_time) * 1000

            # Check the status code
            if response.status_code == 200:
                logger.debug(f"Service at {url} is available")
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Service at {url} is available! Response time: {response_time:.2f} ms"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Service at {url} responded with status: {response.status_code}. Response time: {response_time:.2f} ms"
                    )
                )

        except requests.RequestException as e:
            logger.error(f"Failed to check service at {url}: {e}")
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to check service at {url}: {e}"
                )
            )
