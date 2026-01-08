from typing import Generic, TypeVar, List, Optional, ClassVar, Type
from xml.dom import NoDataAllowedErr

from pydantic import BaseModel, ConfigDict, PrivateAttr


T = TypeVar('T')

class Stack(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _things: List [T] = PrivateAttr(default_factory=list)
    _size: int = PrivateAttr()
    _stack_type: ClassVar[Optional[Type]] = None

    @classmethod
    def create(cls, item_type: Type[T]) -> 'Stack[T]':

        class StackStrict(Stack):
            _stack_type: ClassVar[Type] = item_type
            _size: int = 0

            def put(self, thing: T) -> None:
                if not isinstance(thing, self._stack_type):
                    raise TypeError(
                        f"This stack is of '{self._stack_type.__name__}' type, "
                        f"not '{type(thing).__name__}' what is attempted to be put!"
                    )
                self._things.append(thing)
                self._size += 1

        return StackStrict()

    def put (self, thing: T) -> None:
        raise NotImplementedError("Use create() factory method")

    def get_size (self) -> int:
        return self._size

    def is_empty (self) -> bool:
        return self._size == 0

    def take (self) -> Optional[T]:
        if self.is_empty():
            raise Exception('Stack is empty!')
        else:
            self._size -= 1
            return self._things.pop(self._size)

    def __iter__(self):
        self._itr = self._size
        return self

    def __next__(self):
        if self._itr > 0:
            self._itr -= 1
            return self._things[self._itr]
        else:
            raise StopIteration
