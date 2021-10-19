from dataclasses import astuple, dataclass

from bonk.algorithms import best_algorithm


class Bonkfig:
    separator = '\t'
    algorithm = best_algorithm()

    @staticmethod
    def postprocess_args(args):
        Bonkfig.separator = args.separator
        Bonkfig.algorithm = args.algorithm


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
