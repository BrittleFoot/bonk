#! python
import argparse

from pathlib import Path
from itertools import chain

from bonk import Record
from bonk import Bonkfig
from bonk.io import read_fasta, write_table
from bonk.bio import reverse, complement
from bonk.algorithms import best_algorithm
from bonk.algorithms import installed as installed_algorithms


def find_positive_strand(string, pattern, chr):
    algorithm = installed_algorithms[Bonkfig.algorithm]
    for i in algorithm(string, pattern):
        yield Record(
            chr=chr,
            start=i+1,
            end=i+len(pattern)+1,
            strand='+',
            sequence=pattern
        )


def find_negative_strand(string, pattern, chr):
    algorithm = installed_algorithms[Bonkfig.algorithm]
    for i in algorithm(complement(reverse(string)), pattern):
        start = i
        end = i + len(pattern)

        yield Record(
            chr=chr,
            start=len(string) - end + 1,
            end=len(string) - start + 1,
            strand='-',
            sequence=pattern
        )


def main(args):
    records = read_fasta(args.fasta)
    output = []
    for record in records:
        output = chain(output,
                       find_positive_strand(
                           record.sequence, args.sequence, record.chr),
                       find_negative_strand(
                           record.sequence, args.sequence, record.chr)
                       )

    write_table(output, args.output)


def parse_args(init=None):
    parser = argparse.ArgumentParser('bonk')
    parser.add_argument('-a', '--fasta', type=Path, required=True)
    parser.add_argument('-s', '--sequence', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('--separator', default='\t')
    parser.add_argument(
        '--algorithm', choices=installed_algorithms.keys(), default=best_algorithm())

    return parser.parse_args(init)


if __name__ == '__main__':
    args = parse_args()
    Bonkfig.postprocess_args(args)
    main(args)
