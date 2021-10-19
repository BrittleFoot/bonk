import pytest

from pathlib import Path

from bonk import io as bonkio
from bonk import Bonkfig
from bonk import Record
from bonk.algorithms import installed as installed_algorithms


CONTENT = """> a
AAAAAAAAA
> b
TTTTTTTTT
"""


@pytest.fixture
def tmp_file(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    yield tmp_path / 'test_file'


@pytest.fixture
def tmp_fasta(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    tmp_file = tmp_path / 'genome.fa'

    with tmp_file.open('w') as fd:
        fd.write(CONTENT)

    yield tmp_file


def test_read_fasta(tmp_fasta: Path):
    fasta = bonkio.read_fasta(tmp_fasta)

    a, b = fasta

    assert a.chr == 'a'
    assert b.chr == 'b'


def test_write_fasta(tmp_file: Path):
    example = Record('a', 0, 1, '+', 'HELLO')

    bonkio.write_table([example], tmp_file)

    with tmp_file.open('r') as fd:
        header = list(map(str.strip, next(fd).split(Bonkfig.separator)))
        rec = Record(*map(str.strip, next(fd).split(Bonkfig.separator)))

    assert header == bonkio.HEADER
    assert rec == example


@pytest.mark.parametrize('algo', installed_algorithms.values())
def test_find_substrings(algo):
    find_result = list(algo('AA', 'A'))
    r1, r2 = find_result
    assert r1 == 0
    assert r2 == 1


if __name__ == '__main__':
    pytest.main(['-s'])
