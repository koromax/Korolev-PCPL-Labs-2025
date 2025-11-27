class Unique:
    def __init__(self, items, **kwargs):
        Unique._data = items
        Unique._used = set()
        Unique._index = 0
        Unique.ignore_case = kwargs["ignore_case"] if (len(kwargs) > 0 and "ignore_case" in kwargs.keys()) else False
    
    def __iter__(self):
        return self

    def __next__(self):
        while self._index < len(self._data):
            item = str(self._data[self._index])
            self._index += 1

            if self.ignore_case and item.lower() in [e.lower() for e in self._used]:
                continue
            if not self.ignore_case and item in self._used:
                continue

            self._used.add(item)
            return item
        
        raise StopIteration


if __name__ == "__main__":
    data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']

    print(list(Unique(data)))
    print(list(Unique(data, ignore_case=True)))
