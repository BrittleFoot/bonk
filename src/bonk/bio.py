

COMPLEMENTARY_TABLE = str.maketrans({
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'
})


def reverse(seq: str) -> str:
    return seq[::-1]


def complement(seq: str) -> str:
    return seq.translate(COMPLEMENTARY_TABLE)
