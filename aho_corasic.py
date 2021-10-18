import ahocorasick

from record import Record

def aho_find_substrings(string, substring) -> list[Record]:
    automaton = ahocorasick.Automaton()

    automaton.add_word(substring, (0, substring))
    automaton.make_automaton()

    nlen = len(substring)
    for end_index, (_, _) in automaton.iter(string):
        yield end_index

    return automaton.iter(string)




def main():

    res = list(aho_find_substrings('AAA', 'A'))
    print(res)

if __name__ == '__main__':
    main()