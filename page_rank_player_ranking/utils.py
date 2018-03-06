def generated(ParentClass):
    class GeneratingWrapper(ParentClass):
        __identifier = 0

        def __init__(self, *args, **kwargs):
            super(*args, **kwargs)
            self.__id = self.__next_identifier()

        @classmethod
        def __next_identifier(cls):
            to_return = cls.__identifier
            cls.__identifier += 1
            return to_return

        def _get_generated_id(self):
            return self.__id

    return GeneratingWrapper


def retained(ParentClass):
    class RetentionWrapper(ParentClass):
        retained = {}

        def __init__(self, *args, **kwargs):
            super(*args, **kwargs)
            self.retained[self._get_generated_id()] = self

        @classmethod
        def get_instance(cls, key):
            return cls.retained.get(key, None)

        @classmethod
        def remove_instance(cls, key):
            cls.retained.pop(key)

    return RetentionWrapper
