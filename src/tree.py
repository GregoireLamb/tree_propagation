class Tree:
    # rewrite with lower case
    def __init__(self, id, shape, grouppe, baumoehe, alterAb2023):
        self.id = id
        self._gps = shape
        self._grouppe = grouppe
        self._baumoehe = baumoehe
        self._alterAb2023 = alterAb2023

    def __repr__(self):
        return f"Tree({self.id}, position:{self._gps}, group:{self._grouppe}, height:{self._baumoehe}, age:{self._alterAb2023})"



