from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from fashion_frontend.frontend import FrontendInterface
    from fashion_frontend.result import PredictResult


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


class ImageBytesParams(PredictParams):
    """
    Class to define the params for a request with the image bytes
    """

    def __init__(self, image_bytes: bytes, all_categories: bool = None, all_attributes: bool = None):
        super().__init__(all_categories, all_attributes)
        self.__image_bytes = image_bytes

    @property
    def image_bytes(self) -> bytes:
        return self.__image_bytes

    def accept_frontend_interface(self, frontend: 'FrontendInterface') -> 'List[PredictResult]':
        return frontend.predict_image_bytes(self)
