from abc import ABC


class BaseService(ABC):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            if cls.__name__ == "BaseService":
                raise NotImplementedError("BaseService is an abstract class and cannot be instantiated")
            cls._instance = super(BaseService, cls).__new__(cls)
        return cls._instance
