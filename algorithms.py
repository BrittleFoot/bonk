from record import Record



def find_substrings(string, substring) -> list[Record]:
    length = len(substring)
    for i in range(len(string)):
        kmer = string[i:i+length]
        if kmer == substring:
            yield Record(None, i, i+length, None, substring)



installed = dict(basic=find_substrings)


try:
    import ahocorasick
    from aho_corasic import aho_find_substrings
    installed['ahocorasic'] = aho_find_substrings

except ModuleNotFoundError:
    pass
    



__all__ = ['installed']