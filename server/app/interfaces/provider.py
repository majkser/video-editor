from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @staticmethod
    @abstractmethod
    def get_repository():
        """Returns an instance of the repository associated with this provider."""
        raise NotImplementedError("Subclasses must implement get_repository method")
    
    @staticmethod
    @abstractmethod
    def get_service():
        """Returns an instance of the service associated with this provider."""
        raise NotImplementedError("Subclasses must implement get_service method")