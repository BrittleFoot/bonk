from dataclasses import astuple, dataclass


@dataclass
class Record:
    chr: str
    start: int
    end: int
    strand: str
    sequence: str

    def __post_init__(self):
        self.start = int(self.start)
        self.end = int(self.end)

    def __iter__(self):
        return iter(astuple(self))
