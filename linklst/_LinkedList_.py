from typing import Iterable, Iterator, Any


class LinkedList(Iterable):

    class Element:

        value = None

        following = None
        follows = None

        def __init__(self, val, follows, following):
            self.value = val
            self.follows = follows
            self.following = following

        def truncate(self) -> Any:
            if self.follows is not None:
                self.follows.following = self.following
            if self.following is not None:
                self.following.follows = self.follows
            return self.value

        def insert_following(self, value):
            new = LinkedList.Element(value, self, self.following)
            self.following.follows = new
            self.following = new

        def insert_follows(self, value):
            new = LinkedList.Element(value, self.follows, self)
            self.follows.following = new
            self.follows = new

        def __eq__(self, other):
            return isinstance(other, self.__class__) and self.value == other.value

        def __hash__(self):
            return hash(self.value)

    head: Element = None
    tail: Element = None

    def __init__(self, iterable: Iterable = None, *, head: Element = None, tail: Element = None):
        if iterable is not None:
            for element in iterable:
                self.append(element)
        else:
            self.head = head
            self.tail = tail

    def __len__(self):
        counter = 0
        current = self.head
        while current is not None:
            counter += 1
            current = current.follows
        return counter

    def get(self, index: int):
        if self.isEmpty():
            raise IndexError()

        elif index == 0:
            return self.head

        elif index > 0:

            count = 0
            current = self.head

            while count < index:
                count += 1
                current = current.follows
                if current is None:
                    raise IndexError()

            return current

        else:

            count = -1
            current = self.tail

            while count > index:
                count -= 1
                current = current.following
                if current is None:
                    raise IndexError()

            return current

    def __getitem__(self, item):
        if not type(item) is int:
            raise IndexError()
        return self.get(item).value

    def __setitem__(self, key, value):
        if not type(key) is int or self.head is None:
            raise IndexError()
        self.get(key).value = value

    def __iter__(self) -> Iterator:
        return self.iterate()

    def iterate(self, *, unwrap=True) -> Iterator[Element]:
        if not self.isEmpty():
            current = self.head
            while current is not None:
                yield current.value if unwrap else current
                current = current.follows

    def __str__(self):
        string = self.__class__.__name__ + '(['

        for element in self:
            string += repr(element) + ','

        if string[-1] == ',':
            string = string[:-1]

        string += '])'

        return string

    def appendleft(self, item):
        if self.isEmpty():
            self.head = self.Element(item, None, None)
            self.tail = self.head

        else:
            new = self.Element(item, self.head, None)
            self.head.following = new
            self.head = new
            self.head = self.Element(item, self.head, None)
            if self.tail.following is None:
                self.tail.following = self.head

    def append(self, item):
        if self.isEmpty():
            self.tail = self.Element(item, None, None)
            self.head = self.tail

        else:
            new = self.Element(item, None, self.tail)
            self.tail.follows = new
            self.tail = new
            if self.head.follows is None:
                self.head.follows = new

    def isEmpty(self):
        return self.head is None

    # noinspection DuplicatedCode
    def popleft(self):
        buffer = self.head

        if buffer is None:
            raise ValueError()

        if buffer.follows is None:
            self.head = None
            self.tail = None
            return buffer.value()

        self.head = buffer.follows
        return buffer.value()

    # noinspection DuplicatedCode
    def pop(self):
        buffer = self.tail

        if buffer is None:
            raise ValueError()

        if buffer.following is None:
            self.head = None
            self.tail = None
            return buffer.value()

        self.tail = buffer.following
        return buffer.value()

    def first(self):
        if self.isEmpty():
            raise ValueError()
        return self.head.value

    def last(self):
        if self.isEmpty():
            raise ValueError()
        return self.tail.value
