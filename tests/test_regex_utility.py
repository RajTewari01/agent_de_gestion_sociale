from __future__ import annotations
import pytest   #type: ignore
from backend.core.regex_utility import RegexUtility #type: ignore

# ─── SENTENCES ────────────────────────────────────────────────────────────────

SENTENCES = [
    "  THE   QUICK   BROWN   FOX   JUMPS   OVER   THE   LAZY   DOG  ",
    "🔥🔥 Breaking News!!! 😱😱 You won't BELIEVE what happened today 🎉🎊🥳",
    "𠀋 Hello 𠀋𠀋 World 😊 This is a TEST 𠀋 string 🔥",
    "   @rajTewari01 just dropped the HOTTEST project 🔥🔥 #NeuralCitadel #AI #MachineLearning check it OUT!!!   ",
    "Follow us at https://neural-citadel.ai and check @NeuralCitadel on twitter #AI #LLM #OpenSource 🤖",
    "Héllo Wörld thïs ïs à tëst strïng wïth ünïcödë chäracters café naïve résumé",
    "THIS IS A VERY LONG SENTENCE THAT IS ALL IN CAPS AND HAS NO PUNCTUATION AND GOES ON AND ON",
    "hello    hello    hello    world    world    world    this    is    a    test",
    "  𠀋𠀋 @user123 HELLO   WORLD 😊🔥 https://example.com #hashtag café naïve   ",
    "Just launched my NEW AI project called Neural Citadel 🚀🚀🚀 It runs MULTIPLE models on a SINGLE consumer GPU with only 4GB VRAM!!! Check it out at https://github.com/RajTewari01 and give it a ⭐ if you like it!!! #AI #MachineLearning #OpenSource #NeuralCitadel @rajTewari01",
]

# ─── FIXTURES ─────────────────────────────────────────────────────────────────

@pytest.fixture
def basic() -> RegexUtility:
    return RegexUtility("Hello World")

@pytest.fixture
def spaced() -> RegexUtility:
    return RegexUtility("  hello   world  ")


# ─── CASE ─────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("input,expected", [
    ("HELLO WORLD",                     "hello world"),
    ("HELLO",                           "hello"),
    ("123ABC",                          "123abc"),
    ("THE QUICK BROWN FOX",             "the quick brown fox"),
    ("THIS IS ALL CAPS NO PUNCTUATION", "this is all caps no punctuation"),
])
def test_lower(input, expected):
    assert RegexUtility(input).lower().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("hello world",         "HELLO WORLD"),
    ("hello",               "HELLO"),
    ("123abc",              "123ABC"),
    ("the quick brown fox", "THE QUICK BROWN FOX"),
])
def test_upper(input, expected):
    assert RegexUtility(input).upper().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("hello world", "Hello world"),
    ("HELLO WORLD", "Hello world"),
    ("hELLO wORLD", "Hello world"),
])
def test_capitalize(input, expected):
    assert RegexUtility(input).capitalize().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("hello world",         "Hello World"),
    ("the quick brown fox", "The Quick Brown Fox"),
])
def test_title(input, expected):
    assert RegexUtility(input).title().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("Hello World", "hELLO wORLD"),
    ("hELLO wORLD", "Hello World"),
])
def test_swapcase(input, expected):
    assert RegexUtility(input).swapcase().build() == expected


# ─── STRIP ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("input,expected", [
    ("  hello  ",         "hello"),
    ("  hello   world  ", "hello   world"),
    ("\t hello \t",       "hello"),
])
def test_strip(input, expected):
    assert RegexUtility(input).strip().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("  hello  ", "hello  "),
    ("  hello",   "hello"),
])
def test_lstrip(input, expected):
    assert RegexUtility(input).lstrip().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("  hello  ", "  hello"),
    ("hello  ",   "hello"),
])
def test_rstrip(input, expected):
    assert RegexUtility(input).rstrip().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("hello   world",           "hello world"),
    ("hello      world   test", "hello world test"),
    ("  hello   world  ",       " hello world "),
])
def test_strip_extra_spaces(input, expected):
    assert RegexUtility(input).strip_extra_spaces().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("hello   world", "helloworld"),
    ("h e l l o",     "hello"),
    ("  hi  ",        "hi"),
])
def test_strip_spaces(input, expected):
    assert RegexUtility(input).strip_spaces().build() == expected


# ─── DEFAULT ──────────────────────────────────────────────────────────────────

# ─── DEFAULT ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("input,expected", [
    ("HELLO   WORLD",     "hello world"),
    ("  HELLO   WORLD  ", " hello world "),
    ("FOO   BAR   BAZ",   "foo bar baz"),
])
def test_use_default(input, expected):
    result = RegexUtility(input).use_default().build()
    assert result == expected


# ─── APPEND / PREPEND ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("input,val,spaces,expected", [
    ("hello",  "world",   True,  "hello world"),
    ("hello",  "world",   False, "helloworld"),
    ("neural", "citadel", True,  "neural citadel"),
])
def test_append_str(input, val, spaces, expected):
    assert RegexUtility(input).append_str(val, spaces).build() == expected


@pytest.mark.parametrize("input,val,spaces,expected", [
    ("world",   "hello",  True,  "hello world"),
    ("world",   "hello",  False, "helloworld"),
    ("citadel", "neural", True,  "neural citadel"),
])
def test_prepend_str(input, val, spaces, expected):
    assert RegexUtility(input).prepend_str(val, spaces).build() == expected


@pytest.mark.parametrize("val", [123, None, 12.5, [], {}])
def test_append_str_type_error(val):
    with pytest.raises(TypeError):
        RegexUtility("hello").append_str(val)


def test_append_str_value_error():
    with pytest.raises(ValueError):
        RegexUtility("hello").append_str("")


@pytest.mark.parametrize("val", [123, None, 12.5, [], {}])
def test_prepend_str_type_error(val):
    with pytest.raises(TypeError):
        RegexUtility("hello").prepend_str(val)


def test_prepend_str_value_error():
    with pytest.raises(ValueError):
        RegexUtility("hello").prepend_str("")


# ─── UNICODE ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("input,form,expected", [
    ("café", "NFC",  "café"),
    ("café", "NFKC", "café"),
])
def test_normalize_unicode(input, form, expected):
    assert RegexUtility(input).normalize_unicode(form=form).build() == expected


@pytest.mark.parametrize("input,expected", [
    ("café",   "cafe"),
    ("naïve",  "naive"),
    ("résumé", "resume"),
])
def test_keep_ascii_only(input, expected):
    assert RegexUtility(input).keep_ascii_only().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("hello 𠀋 world", "hello  world"),
    ("𠀋𠀋 hello 𠀋",  " hello "),
])
def test_strip_high_unicode_chars(input, expected):
    assert RegexUtility(input).strip_high_unicode_chars().build() == expected


@pytest.mark.parametrize("input,expected", [
    ("hello 😊🔥 world", "hello  world"),
    ("🔥🔥 Breaking News", " Breaking News"),
])
def test_strip_emoji(input, expected):
    assert RegexUtility(input).strip_emoji().build() == expected


# ─── REPLACE ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("input,target,repl,count,expected", [
    ("aaa bbb aaa", "aaa", "ccc", 0, "ccc bbb ccc"),
    ("aaa bbb aaa", "aaa", "ccc", 1, "ccc bbb aaa"),
    ("hello world", "xyz", "abc", 0, "hello world"),
    ("aaa aaa aaa", "aaa", "bbb", 2, "bbb bbb aaa"),
])
def test_replace(input, target, repl, count, expected):
    assert RegexUtility(input).replace(target, repl, count=count).build() == expected


# ─── TRUNCATE ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("input,max_len,from_end,expected", [
    ("hello world", 5,  False, "hello"),
    ("hello world", 5,  True,  "world"),
    ("hello world", 11, False, "hello world"),
    ("hello world", 3,  True,  "rld"),
])
def test_truncate(input, max_len, from_end, expected):
    assert RegexUtility(input).truncate(max_len, from_end).build() == expected


@pytest.mark.parametrize("input,max_len,from_end,expected", [
    ("hello world", 5, False, "hello"),
    ("hello world", 5, True,  "world"),
])
def test_truncate_at_last(input, max_len, from_end, expected):
    assert RegexUtility(input).truncate_at_last(max_len, from_end).build() == expected


def test_truncate_at_last_runs_after_steps():
    result = RegexUtility("hello world").truncate_at_last(5).upper().build()
    assert result == "HELLO"


def test_truncate_cleared_after_build():
    ru = RegexUtility("hello world").truncate_at_last(5).build()
    assert ru._truncate is None


# ─── PROPERTY ─────────────────────────────────────────────────────────────────

def test_property_getter():
    ru = RegexUtility("hello world").lower().build()
    assert ru.text == "hello world"


def test_property_setter():
    ru = RegexUtility("hello world").lower().build()
    ru.text = "RAJ TEWARI"
    assert ru.text == "RAJ TEWARI"


def test_property_setter_saves_temp():
    ru = RegexUtility("hello world").lower().build()
    ru.text = "RAJ TEWARI"
    assert ru.temp_text == "hello world"


def test_property_deleter_reverts():
    ru = RegexUtility("hello world").lower().build()
    ru.text = "RAJ TEWARI"
    del ru.text
    assert ru.text == "hello world"


def test_property_deleter_no_setter_no_crash():
    ru = RegexUtility("hello")
    del ru.text
    assert ru.text == "hello"


@pytest.mark.parametrize("val", [123, None, 12.5, [], {}])
def test_setter_type_error(val):
    with pytest.raises(TypeError):
        ru = RegexUtility("hello")
        ru.text = val


def test_setter_value_error():
    with pytest.raises(ValueError):
        ru = RegexUtility("hello")
        ru.text = ""


# ─── DUNDER ───────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("other,expected", [
    ("hello",               True),
    ("world",               False),
    (RegexUtility("hello"), True),
    (RegexUtility("world"), False),
])
def test_eq(other, expected):
    ru = RegexUtility("hello").build()
    assert (ru == other) == expected


def test_len():
    assert len(RegexUtility("hello").build()) == 5


def test_str():
    assert str(RegexUtility("hello").build()) == "hello"


def test_hash_dedup():
    seen = {
        RegexUtility("HELLO").lower().build(),
        RegexUtility("hello").build(),
    }
    assert len(seen) == 1


def test_hash_matches_str():
    assert hash(RegexUtility("hello").build()) == hash("hello")


# ─── RESET / CLEAR ────────────────────────────────────────────────────────────

def test_reset_reverts_text():
    ru = RegexUtility("HELLO").lower().build()
    ru.reset()
    assert ru == "HELLO"


def test_reset_clears_steps():
    ru = RegexUtility("HELLO")
    ru.lower().upper()
    ru.reset()
    assert len(ru.steps) == 0


def test_clear_steps():
    ru = RegexUtility("HELLO")
    ru.lower().upper()
    ru.clear_steps()
    assert len(ru.steps) == 0


def test_multi_build():
    ru = RegexUtility("HELLO WORLD").lower().build()
    ru.upper().build()
    assert ru == "HELLO WORLD"


# ─── CHAINING ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("input,expected", [
    ("  HELLO   WORLD  ", "hello world"),
    ("  FOO   BAR  ",     "foo bar"),
    ("  THE   QUICK  ",   "the quick"),
])
def test_chaining_lower_strip(input, expected):
    assert RegexUtility(input).lower().strip().strip_extra_spaces().build() == expected


# ─── REAL SENTENCES — NO CRASH ────────────────────────────────────────────────

@pytest.mark.parametrize("text", SENTENCES)
def test_lower_no_crash(text):
    result = RegexUtility(text).lower().build()
    assert result == text.lower()


@pytest.mark.parametrize("text", SENTENCES)
def test_strip_no_crash(text):
    result = RegexUtility(text).strip().build()
    assert result == text.strip()


@pytest.mark.parametrize("text", SENTENCES)
def test_full_pipeline_no_crash(text):
    result = (
        RegexUtility(text)
        .lower()
        .strip()
        .strip_emoji()
        .strip_high_unicode_chars()
        .strip_extra_spaces()
        .build()
    )
    assert isinstance(str(result), str)


@pytest.mark.parametrize("text", SENTENCES)
def test_truncate_no_crash(text):
    result = RegexUtility(text).truncate(50).build()
    assert len(result) <= 50


@pytest.mark.parametrize("text", SENTENCES)
def test_reset_after_pipeline(text):
    ru = RegexUtility(text).lower().strip().build()
    ru.reset()
    assert ru == text


# ─── CUSTOM STEP ──────────────────────────────────────────────────────────────

def test_add_custom_step():
    ru = RegexUtility("hello world").add(lambda x: x.replace("world", "RAJ")).build()
    assert ru == "hello RAJ"


def test_add_multiple_custom_steps():
    ru = (
        RegexUtility("hello world")
        .add(lambda x: x.upper())
        .add(lambda x: x.replace("WORLD", "RAJ"))
        .build()
    )
    assert ru == "HELLO RAJ"

