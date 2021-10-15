import pytest
import bonk

from pathlib import Path


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
    fasta = bonk.read_fasta(tmp_fasta)

    a, b = fasta

    assert a.chr == 'a'
    assert b.chr == 'b'

def test_write_fasta(tmp_file: Path):
    example = bonk.Record('a', 0, 1, '+', 'HELLO')

    bonk.write_table([example], tmp_file)

    with tmp_file.open('r') as fd:
        header = list(map(str.strip, next(fd).split(bonk.Bonkfig.separator)))
        rec = bonk.Record(*next(fd).split(bonk.Bonkfig.separator))

    assert header == bonk.HEADER
    assert rec == example
    
def test_find_substrings():
    find_result = list(bonk.find_substrings('AA', 'A'))
    r1, r2 = find_result
    assert r1.start == 0
    assert r2.start == 1

if __name__ == '__main__':
    pytest.main(['-s'])