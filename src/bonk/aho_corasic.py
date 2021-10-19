import ahocorasick

from bonk.algorithms import IntGenerator


def aho_find_substrings(string, substring) -> IntGenerator:
    automaton = ahocorasick.Automaton()

    automaton.add_word(substring, (0, substring))
    automaton.make_automaton()

    for i, _ in automaton.iter(string):
        yield i
