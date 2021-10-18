import ahocorasick

from record import Record


def aho_find_substrings(string, substring) -> list[Record]:
    automaton = ahocorasick.Automaton()

    automaton.add_word(substring, (0, substring))
    automaton.make_automaton()

    nlen = len(substring)
    for i, (_, _) in automaton.iter(string):
        yield Record(None, i, i + nlen, None, substring)

