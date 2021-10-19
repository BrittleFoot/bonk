from typing import Generator


IntGenerator = Generator[int, None, None]


def find_substrings(string, substring) -> IntGenerator:
    """ Clasic naive algorithm """
    length = len(substring)
    for i in range(len(string)):
        kmer = string[i:i+length]
        if kmer == substring:
            yield i


installed = dict(basic=find_substrings)


try:
    import ahocorasick
    from bonk.aho_corasic import aho_find_substrings
    installed['ahocorasic'] = aho_find_substrings

except ModuleNotFoundError:
    pass


def best_algorithm():
    if 'ahocorasic' in installed:
        return 'ahocorasic'

    return 'basic'


__all__ = ['installed']
