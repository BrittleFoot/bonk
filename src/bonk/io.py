from pathlib import Path
from typing import Iterable
from sys import stdout

from bonk import Record
from bonk import Bonkfig


HEADER = [
    '#chr',
    '#start_position',
    '#end_position',
    '#strand',
    '#substring_seq',
]


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
    if output == '-':
        _write_table(table, stdout)
        return

    with open(output, 'w') as fd:
        _write_table(table, fd)


def _write_table(table, descriptor):
    def record_to_row(r):
        return map(str, r)

    print(Bonkfig.separator.join(HEADER), file=descriptor)
    strings = map(Bonkfig.separator.join, map(record_to_row, table))
    print('\n'.join(strings), file=descriptor)
