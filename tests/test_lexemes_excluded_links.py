# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pytest


# lexemes are divided by blank lines;
# lines that starts with "#" are comments;
# lines that starts with "XFAIL" excludes lexeme from testing.

def parse_lexemes(lexemes_txt):
    lexemes_txt = "".join(
        line for line in lexemes_txt.strip().splitlines(True)
        if not line.startswith("#")
    )
    return lexemes_txt.split("\n\n")


def get_lexeme_words(lexeme):
    lexeme_words = tuple(lexeme.split())
    if lexeme_words[0].startswith('XFAIL'):
        pytest.xfail()
    return lexeme_words


def parse_full_lexeme(lexeme):
    forms = lexeme.strip().splitlines()
    return [form.split(None, 1) for form in forms]


LEXEMES_NOT_LINKED = parse_lexemes("""
# =========== noun
# век века

в век

век в

страница стр

строение стр
""")


# ============ Tests:

@pytest.mark.parametrize("lexeme", LEXEMES_NOT_LINKED)
def test_not_linked_lexemes(lexeme, morph):
    """
    Check if the lexeme of the first word in the lexeme is the same lexeme.
    """
    lexeme_words = get_lexeme_words(lexeme)

    variants = _lexemes_for_word_ar_array(lexeme_words[0], morph)
    if lexeme_words[1] in variants:
        variants_repr = "\n".join([" ".join(v) for v in variants])
        assert False, "%s in \n%s" % (lexeme_words[1], variants_repr)

LEXEMES_LINKED = parse_lexemes("""
# =========== noun
кг килограмм

килограмм кг

км километр

километр км
""")

@pytest.mark.parametrize("lexeme", LEXEMES_LINKED)
def test_linked_lexemes(lexeme, morph):
    """
    Check if the lexeme of the first word in the lexeme is the same lexeme.
    """
    lexeme_words = get_lexeme_words(lexeme)

    variants = _lexemes_for_word_ar_array(lexeme_words[0], morph)
    if lexeme_words[1] not in variants:
        variants_repr = "\n".join([" ".join(v) for v in variants])
        assert False, "%s in \n%s" % (lexeme_words[1], variants_repr)


def assert_has_full_lexeme(word, forms, morph):
    for p in morph.parse(word):
        lexeme_forms = [(f.word, str(f.tag)) for f in p.lexeme]
        if lexeme_forms == forms:
            return
    raise AssertionError("Word %s doesn't have lexeme %s" % (word, forms))


def _lexemes_for_word_ar_array(word, morph):
    res = []
    for p in morph.parse(word):
        for f in p.lexeme:
            res.append(f.word)
    return res
