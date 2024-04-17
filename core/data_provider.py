from abc import abstractmethod
from functools import singledispatchmethod
from typing import Protocol, runtime_checkable
from urllib import request, robotparser
from zipfile import ZipFile


@runtime_checkable
class DataProvider(Protocol):
    """
    Sketch of an abstraction over individual brick
    download/process pathways. The implementing classes
    provide definitions of `fetch` and `process_file`.
    """

    meta: dict  # this will contain file meta like compression (if any)
    files: list = []  # files being downloaded

    @abstractmethod
    def process_file(self, file_type):
        """Dispatches file handling logic on the type of `file_type`.
        Could provide some core functionality, like doing HTTP HEAD
        request to determine the type of resource to be loaded?

        Args:
            file_type: a file-like object
        """
        raise NotImplementedError

    def check_headers(self, url):
        req = request.Request(url=url, method="HEAD")
        with request.urlopen(req) as headers:
            return headers['Content-Type'] or None

    @abstractmethod
    def fetch(self, url) -> bool:
        """This abstract method provides a basic concrete implementation
        to check if the remote resource permits scraping by checking for the
        existence of a `robots.txt` file. All other functionality is deferred
        to subclasses.
        """
        robots = robotparser.RobotFileParser(url)
        robots.read()
        return robots.can_fetch("*", url)


class Deps(DataProvider):
    """
    This would be the Python class into which
    we would dump TOML config. Probably should extend
    the `DataProvider` protocol in order to provide
    the actual data-fetching functionality.
    """

    meta: dict
    files: list = []

    def __init__(self, **kwargs):
        self.meta = kwargs

    @singledispatchmethod
    def process_file(self, file_type):
        pass

    @process_file.register
    def _(self, file_type: ZipFile):
        pass

    def fetch(self, url) -> bool:
        can_scrape = super().fetch(url)
        return can_scrape


deps = Deps()

isinstance(deps, DataProvider)  # => True

# TypeError: Protocols with non-method members don't support issubclass()
issubclass(Deps, DataProvider)
