from abc import ABC, abstractmethod


class AbstractModel(ABC):
    @property
    @abstractmethod
    def action(self):
        pass
