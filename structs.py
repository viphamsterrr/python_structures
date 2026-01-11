from typing import Generic, TypeVar, List, Optional, ClassVar, Type
from xml.dom import NoDataAllowedErr

import pydantic
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
        raise NotImplementedError("Use Stack.create(type) method instaed of Stack()")

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

    def __cmp__(self, other: T):
        if not isinstance(other, type(self)):
            return NotImplemented
        if self.get_size() == other.get_size():
            return 0
        if self.get_size() > other.get_size():
            return 1
        return -1

    def __eq__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() == other.get_size()

    def __lt__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() < other.get_size()

    def __gt__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() > other.get_size()

    def __le__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() <= other.get_size()

    def __ge__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() >= other.get_size()

    def __str__(self):
        return "Stack of " + self._stack_type.__name__

    def __contains__(self, thing):
        if not isinstance(thing, self._stack_type):
            return False
        else:
            for i in range(self.get_size()):
                if self._things[i] == thing:
                    return True
        return False


class Queue(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _things: List [T] = PrivateAttr(default_factory=list)
    _size: int = PrivateAttr()
    _first: int = PrivateAttr()
    _last: int = PrivateAttr()
    _queue_type: ClassVar[Optional[Type]] = None

    @classmethod
    def create(cls, item_type: Type[T]) -> 'Queue[T]':

        class QueueStrict(Queue):
            _queue_type: ClassVar[Type] = item_type
            _size: int = 0
            _first: int = 0
            _last: int = 0

            def put(self, thing: T) -> None:
                if not isinstance(thing, self._queue_type):
                    raise TypeError(
                        f"This queue is of '{self._queue_type.__name__}' type, "
                        f"not '{type(thing).__name__}' what is attempted to be put!"
                    )
                self._things.append(thing)
                self._size += 1
                if self._size > 1:
                    self._last += 1
        return QueueStrict()

    def put (self, thing: T) -> None:
        raise NotImplementedError("Use Queue.create(type) instead of Queue()")

    def get_size (self) -> int:
        return self._size

    def is_empty (self) -> bool:
        return self._size == 0

    def take (self) -> Optional[T]:
        if self.is_empty():
            raise Exception('Stack is empty!')
        else:
            rslt = self._things[self._first]
            self._size -= 1
            self._first += 1
            if (len(self._things) > 1000) and (self._size < self._first - 30):
                self._rebase()
            if self._size == 0:
                while len(self._things) != 0:
                    self._things.pop()
                self._first = 0
                self._last = 0
            return rslt

    def _rebase(self):
        for i in range(self._size):
            self._things[self._size - i - 1] = self._things.pop()
        while len(self._things) > self._size:
            self._things.pop()
        self._first = 0
        self._last = self._size - 1

    def __iter__(self):
        self._itr = self._first
        return self

    def __next__(self):
        if self.is_empty():
            raise StopIteration
        if self._itr <= self._last:
            rslt = self._things[self._itr]
            self._itr += 1
            return rslt
        else:
            raise StopIteration

    def __cmp__(self, other: T):
        if not isinstance(other, type(self)):
            return NotImplemented
        if self.get_size() == other.get_size():
            return 0
        if self.get_size() > other.get_size():
            return 1
        return -1

    def __eq__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() == other.get_size()

    def __lt__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() < other.get_size()

    def __gt__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() > other.get_size()

    def __le__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() <= other.get_size()

    def __ge__(self, other: T) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.get_size() >= other.get_size()

    def __str__(self):
        return "Queue of " + self._queue_type.__name__

    def __contains__(self, thing):
        if not isinstance(thing, self._queue_type):
            return False
        else:
            for i in range(self._first, self._last + 1):
                if self._things[i] == thing:
                    return True
        return False
