from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Tuple
    from fashion_contract.service_pb2 import PredictResponse


class PredictResult(object):
    """
    Class to define responses from the server
    """

    def __init__(self, predict_response: 'PredictResponse'):
        self.__categories = list(map(lambda x: (x.label, x.value), predict_response.predicted_categories))
        self.__attributes = list(map(lambda x: (x.label, x.value), predict_response.predicted_attributes))

    @property
    def categories(self) -> 'List[Tuple[str, float]]':
        return self.__categories

    @property
    def attributes(self) -> 'List[Tuple[str, float]]':
        return self.__attributes

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"PredictResult" \
               f"{{categories: {self.__categories}," \
               f" attributes: {self.__attributes}}}"
