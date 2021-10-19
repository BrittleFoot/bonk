#! python
import argparse

from os import read
from sys import stdout

from typing import Iterable
from pathlib import Path
from itertools import chain

from record import Record
from algorithms import best_algorithm, installed


HEADER = [
    '#chr',
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


def write_table(table: Iterable[Record], output: str):
    def record_to_row(r): 
        return map(str, r)

    if output == '-':
        _write_table(table, stdout)
        return

    with output.open('w') as fd:
        _write_table(table, fd)
        

def _write_table(table, descriptor):
    def record_to_row(r): 
        return map(str, r)

    print(Bonkfig.separator.join(HEADER), file=descriptor)
    strings = map(Bonkfig.separator.join, map(record_to_row, table))
    print('\n'.join(strings), file=descriptor)    



def find_substrings(string, substring):
    length = len(substring)
    for i in range(len(string)):
        kmer = string[i:i+length]
        if kmer == substring:
            yield Record(None, i, i+length, None, substring)


def find_positive_strand(string, args, chr):
    algorithm = installed[args.algorithm]
    for record in algorithm(string, args.sequence):
        record.start += 1
        record.end += 1
        record.chr = chr
        record.strand = '+'
        yield record


def find_negative_strand(string, args, chr):
    algorithm = installed[args.algorithm]
    for record in algorithm(complement(reverse(string)), args.sequence):
        start = record.start
        end = record.end

        record.start = len(string) - end + 1
        record.end = len(string) - start + 1

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
        finds = find_positive_strand(record.sequence, args, record.chr)
        reverse_finds = find_negative_strand(record.sequence, args, record.chr)
        output = chain(output, finds, reverse_finds)

    write_table(output, args.output)


def parse_args(init=None):
    parser = argparse.ArgumentParser('bonk')
    parser.add_argument('-a', '--fasta', type=Path, required=True)
    parser.add_argument('-s', '--sequence', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('--separator', default='\t')
    parser.add_argument('--algorithm', choices=installed.keys(), default=best_algorithm())

    return parser.parse_args(init)


if __name__ == '__main__':
    args = parse_args()
    Bonkfig.postprocess_args(args)
    main(args)
