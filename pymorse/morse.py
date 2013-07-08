from itertools import chain

MORSE_ALPHABET = {
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '...-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..'
}

MORSE_REVERSE_MAP = {v: k for k, v in MORSE_ALPHABET.items()}


def decompose_char(char):
    """ Given a string of 4 morse code characters, return possible matches
        in the alphabet.

        >>> decompose_char(".--.")
        ('e', 'a', 'w', 'p')
        >>> decompose_char('....')
        ('e', 'i', 's', 'h')
        >>> decompose_char('.-00')
        ('e', 'a', None, None)
        >>> decompose_char('..')
        Traceback (most recent call last):
            ...
        AssertionError
    """
    assert len(char) == 4
    return (
        MORSE_REVERSE_MAP.get(char[:1]),
        MORSE_REVERSE_MAP.get(char[:2]),
        MORSE_REVERSE_MAP.get(char[:3]),
        MORSE_REVERSE_MAP.get(char[:4]),
    )


def iter_morse_code(morse_string):
    """ Iterate over a morse code string returning 4 char length pieces.

        >>> [n for n in iter_morse_code(".--.--..")]
        ['.--.', '--.-', '-.--', '.--.', '--..']

    """
    for index in range(len(morse_string) - 3):
        yield morse_string[index:index + 4]


def match_alphabet(morse_string):
    """ Given a morse code string, return series of 4 tuples for each 4
        character combination.

        >>> [n for n in match_alphabet(".-")]
        ['e', 'a', None, None, 't', None, None, None]
        >>> [n for n in match_alphabet(".-.")]
        ['e', 'a', 'r', None, 't', 'n', None, None, 'e', None, None, None]
        >>> [n for n in match_alphabet(".--.-")]
        ['e', 'a', 'w', 'p', 't', 'm', 'g', 'q', 't', 'n', 'k', None, 'e', 'a', None, None, 't', None, None, None]
    """
    morse_string += "000"  # Append junk at the end to iterate to the last char
    return reduce(chain, [decompose_char(char)
                          for char in iter_morse_code(morse_string)])


def recompose_words(letters, offset=0):
    """ Given a series of letters (as returned from `match_alphabet`), return
        every combination of words.

        >>> recompose_words(['e', 'a', 'r', None, 't', 'n', None, None, 'e', None, None, None])
        ['e', 'a', 'r', 'et', 'ete', 'en', 'ae']
    """
    words = []
    for i, index in enumerate(range(offset, offset + 4)):
        if not letters[index]:
            continue
        if len(words) <= 4:
            words.append(letters[index])
        for word in words:
            words.append(
                [
                    word + letter
                    for letter in recompose_words(
                        letters,
                        offset=(len(word) + i) * 4
                    )
                ]
            )
    return words


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #letters = [n for n in match_alphabet(".-.")]
    #print recompose_words(letters)
