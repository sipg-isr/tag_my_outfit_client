from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from typing import List, Union
    from outfit_tagging.client.frontend import FrontendInterface
    from outfit_tagging.client.result import PredictResult


class PredictParams(ABC):
    """
    Base class to define params for the server requests
    """

    def __init__(self, all_categories: bool = None, all_attributes: bool = None):
        """
        :param all_categories: True if the the server response should contain the values for all categories
                               and false for only the predicted one. Defaults to None if the frontend values
                               should be used.
        :param all_attributes: True if the the server response should contain the values for all attributes
                               and false for only the predicted ones. Defaults to None if the frontend values
                               should be used.
        """
        self.__all_categories = all_categories
        self.__all_attributes = all_attributes

    @property
    def all_categories(self) -> bool:
        return self.__all_categories

    @property
    def all_attributes(self) -> bool:
        return self.__all_attributes

    @abstractmethod
    def accept_frontend_interface(self, frontend: 'FrontendInterface') -> 'List[PredictResult]':
        """
        Accepts a frontend interface to send the request
        :param frontend: frontend to send the request
        :return: the response for the request
        """
        pass


class UnaryPredictParams(PredictParams, ABC):
    """
    Abstract class for params that only yield a single image to classify
    """

    @property
    @abstractmethod
    def bytes(self) -> bytes:
        """
        :return: Bytes of the image to classify
        """
        pass


class ImageBytesParams(UnaryPredictParams):
    """
    Class to define the params for a request with the image bytes
    """

    def __init__(self, image_bytes: bytes, all_categories: bool = None, all_attributes: bool = None):
        super().__init__(all_categories, all_attributes)
        if not isinstance(image_bytes, bytes):
            raise TypeError('Invalid type for image_bytes: bytes expected.')
        self.__bytes = bytes(image_bytes)

    @property
    def bytes(self) -> bytes:
        return self.__bytes

    def accept_frontend_interface(self, frontend: 'FrontendInterface') -> 'List[PredictResult]':
        return frontend.predict_image_bytes(self)


class ImagePathParams(UnaryPredictParams):

    def __init__(self, image_path: 'Union[str, Path]', all_categories: bool = None, all_attributes: bool = None):
        super().__init__(all_categories, all_attributes)
        if isinstance(image_path, str):
            self.__path = Path(image_path)
        elif isinstance(image_path, Path):
            self.__path = Path(image_path)
        else:
            raise TypeError('Invalid type for image_path: str or Path expected.')
        if not self.__path.exists() or not self.__path.is_file():
            raise ValueError(f'Invalid path \'{self.__path}\': File does not exists')
        self.__bytes = None

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def bytes(self) -> bytes:
        # Lazy init bytes in order to save space if never used
        if not self.__bytes:
            with open(self.__path, 'rb') as fp:
                self.__bytes = fp.read()
        return self.__bytes

    def accept_frontend_interface(self, frontend: 'FrontendInterface') -> 'List[PredictResult]':
        return frontend.predict_image_path(self)
