from typing import Optional, List, TypeVar, Generic

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self.__container: List[T] = list()

    def append(self, item: T) -> None:
        self.__container.append(item)

    def pop(self) -> Optional[T]:
        return self.__container.pop()

    def empty(self) -> bool:
        return len(self.__container) == 0


if __name__ == "__main__":
    s = Stack()
    s.append("a")
    s.append("b")
    s.append(1.0)
    print(s.pop())
    print(s.empty())
    print(s.pop())
    print(s.pop())
    print(s.empty())
    print(s.pop())
