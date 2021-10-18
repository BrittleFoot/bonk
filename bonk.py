import argparse
from os import read

from typing import Iterable
from pathlib import Path
from itertools import chain
from dataclasses import astuple
from dataclasses import dataclass


HEADER = [
    '#chd',
    '#start_position',
    '#end_position',
    '#strand',
    '#substring_seq',
]

COMPLEMENTARY_TABLE = str.maketrans({
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'
})


class Bonkfig:
    separator = '\t'

    @staticmethod
    def postprocess_args(args):
        Bonkfig.separator = args.separator


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


def reverse(seq: str) -> str:
    return seq[::-1]


def complement(seq: str) -> str:
    return seq.translate(COMPLEMENTARY_TABLE)


def _create_record(header, buffer):
    seq = ''.join(buffer)
    return Record(header, 0, len(seq), '+', seq)


def read_fasta(file_path: Path) -> Iterable[Record]:
    HEAD_SYMBOL = '>'
    def is_header(s): return s.startswith(HEAD_SYMBOL)

    with file_path.open('r') as fd:
        buffer = []
        header = ''

        while 'my guitar gently weeps':
            line = fd.readline().strip()

            if is_header(line) or not line:
                if buffer:
                    yield _create_record(header, buffer)

                if not line:
                    break

                buffer = []
                header = line.removeprefix(HEAD_SYMBOL).strip()
                continue

            buffer.append(line)


def write_table(table: Iterable[Record], output: Path):
    def record_to_row(r): 
        return map(str, r)

    with output.open('w') as fd:
        print(Bonkfig.separator.join(HEADER), file=fd)
        strings = map(Bonkfig.separator.join, map(record_to_row, table))
        print('\n'.join(strings), file=fd)


def find_substrings(string, substring):
    length = len(substring)
    for i in range(len(string)):
        kmer = string[i:i+length]
        if kmer == substring:
            yield Record(None, i+1, i+length, None, substring)


def find_positive_strand(string, substring, chr):
    for record in find_substrings(string, substring):
        record.chr = chr
        record.strand = '+'
        yield record


def find_negative_strand(string, substring, chr):
    for record in find_substrings(complement(reverse(string)), substring):
        record.chr = chr
        record.strand = '-'
        yield record


def main(args):
    """
    read_fasta
    find_substrings
    reverse
    find_substrings
    write_table
    """
    records = read_fasta(args.fasta)
    output = []
    for record in records:
        finds = find_positive_strand(record.sequence, args.sequence, record.chr)
        reverse_finds = find_negative_strand(record.sequence, args.sequence, record.chr)
        output = chain(output, finds, reverse_finds)
    write_table(output, args.output)


def parse_args(init=None):
    parser = argparse.ArgumentParser('bonk')
    parser.add_argument('-s', '--sequence')
    parser.add_argument('-o', '--output', type=Path)
    parser.add_argument('-v', '--verboose', action='store_true')
    parser.add_argument('-a', '--fasta', type=Path)
    parser.add_argument('--separator', default='\t')

    return parser.parse_args(init)


if __name__ == '__main__':
    args = parse_args()
    Bonkfig.postprocess_args(args)
    main(args)
