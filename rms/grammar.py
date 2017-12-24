"""RMS formal grammar.

AoC has a forgiving RMS parser. A variety of syntax errors are ignored.
This parser is somewhat stricter, but makes concessions for common syntax errors.

Errors fall into two categories:
    1) Behavior unchanged
    2) Unexpected behavior

Category (1) is handled by this parser. Some examples of handled syntax errors:
    - Missing closer at EOF or end of block (`endif`, `}`, etc)
    - Missing `{` at start of named block
    - Missing parameters of attribute
    - Unmatched comment closing
    - Unmatched block opening at EOF
    - Umatched `endif` at top level or in blocks
    - #define with more than one parameter

Category (2) is rejected. Some examples of rejected syntax errors:
    - `start random` instead of `start_random`
    - `)` instead of `}`
    - `elseif` instead of `if`
"""

# pylint: disable=expression-not-assigned, pointless-statement

from pyparsing import (Combine, FollowedBy, Forward, Group, LineEnd, Literal,
                       OneOrMore, Optional, ParseException, StringEnd,
                       StringStart, Suppress, Word, ZeroOrMore, alphanums,
                       alphas8bit, javaStyleComment, nums, oneOf)

TOKEN = alphanums + alphas8bit + '._#'
INTS = nums + '-'

SYN_IF = 'if'
SYN_ELSEIF = 'elseif'
SYN_ELSE = 'else'
SYN_ENDIF = 'endif'
SYN_CONST = '#const'
SYN_DEFINE = '#define'
SYN_INCLUDE = '#include_drs'
SYN_START_RANDOM = 'start_random'
SYN_END_RANDOM = 'end_random'
SYN_CHANCE = 'percent_chance'
SYN_OPEN_BRACE = '{'
SYN_CLOSE_BRACE = '}'
SYN_OPEN_BRACKET = '<'
SYN_CLOSE_BRACKET = '>'
SYN_OPEN_COMMENT = '/*'
SYN_CLOSE_COMMENT = '*/'
SYN_SET = 'set_'
SYN_SINGLETONS = oneOf(' '.join(['random_placement', 'nomad_resources', 'grouped_by_team']))
SYN_BLOCKS = oneOf(' '.join([
    'create_connect_all_lands', 'create_connect_all_players_land',
    'create_connect_teams_lands', 'create_connect_same_land_zones',
    'create_object', 'create_terrain', 'create_elevation',
    'create_land', 'create_player_lands'
]))


GRP_RANDOM = oneOf(' '.join([SYN_END_RANDOM, SYN_CHANCE]))

SYN_CLOSERS = oneOf(' '.join([
    SYN_ENDIF, SYN_END_RANDOM, SYN_CLOSE_BRACE, SYN_CLOSE_BRACKET,
    SYN_CLOSE_COMMENT]))
SYN_CLOSERS = oneOf(' '.join([SYN_ENDIF, SYN_CLOSE_COMMENT, SYN_END_RANDOM]))

SYN_KEYWORDS = oneOf(' '.join([
    SYN_IF, SYN_ELSEIF, SYN_ELSE, SYN_ENDIF, SYN_END_RANDOM,
    SYN_CHANCE, SYN_START_RANDOM, SYN_CONST, SYN_DEFINE, SYN_INCLUDE]))

TYPE_COMMENT = 'comment'
TYPE_DEFINE = 'define'
TYPE_CONST = 'const'
TYPE_ATTRIBUTE = 'attribute'
TYPE_SET = 'set'
TYPE_RANDOM = 'random'
TYPE_CHANCE = 'chance'
TYPE_CONDITIONAL = 'conditional'
TYPE_IF = 'if'
TYPE_ELSEIF = 'elseif'
TYPE_ELSE = 'else'
TYPE_ENDIF = 'endif'
TYPE_SECTION = 'section'
TYPE_INCLUDE = 'include'
TYPE_BLOCK = 'block'
TYPE_ANON_BLOCK = 'anon'
TYPE_EMPTY_BLOCK = 'empty'

PROP_BODY = 'body'
PROP_TYPE = 'type'
PROP_NAME = 'name'
PROP_VALUE = 'value'


STATEMENT = Forward()
ROOT = Forward()
SECTION = Forward()

COMMENT = Group(javaStyleComment(TYPE_COMMENT))

INCLUDE = Group(
    SYN_INCLUDE
    + Word(TOKEN)(TYPE_INCLUDE)
    + Optional(Word(nums)(PROP_VALUE))
)

CONST = Group(
    SYN_CONST
    + Word(TOKEN)(TYPE_CONST)
    + Word(TOKEN)(PROP_VALUE)
)
DEFINE = Group(
    SYN_DEFINE
    + Word(TOKEN)(TYPE_DEFINE)
    # Invalid syntax, but accepted.
    + Optional(Word(nums))
)

ATTRIBUTE = (
    Group(
        ~SYN_KEYWORDS
        + Word(TOKEN)(TYPE_ATTRIBUTE)
        + OneOrMore(
            ~LineEnd()
            + ~SYN_KEYWORDS
            + Word(TOKEN)
        )(PROP_VALUE)
    ) | Group(~SYN_KEYWORDS + Word(TOKEN)(TYPE_ATTRIBUTE) + LineEnd())
)

SET = Group((
    SYN_SINGLETONS
    | Combine(
        SYN_SET
        + Word(TOKEN)
    )
)(TYPE_SET))

ONELINERS = (INCLUDE | CONST | DEFINE | SET | ATTRIBUTE)

CHANCE = Group(
    SYN_CHANCE
    + Optional(Word(INTS), default=0)(TYPE_CHANCE)
    + Optional(OneOrMore(
        ~GRP_RANDOM
        + STATEMENT
    ), default=None)(PROP_BODY)
)

RANDOM = Group(
    SYN_START_RANDOM
    + Group(
        Optional(OneOrMore(CHANCE), default=None)(PROP_BODY)
    )(TYPE_RANDOM)
    + SYN_END_RANDOM
)

IF = Group(
    Suppress(SYN_IF)
    + Word(TOKEN)(PROP_VALUE)
    + Optional(OneOrMore(STATEMENT), default=None)(PROP_BODY)
)

ELSEIF = Group(
    Suppress(SYN_ELSEIF)
    + Word(TOKEN)(PROP_VALUE)
    + Optional(OneOrMore(STATEMENT), default=None)(PROP_BODY)
)

ELSE = Group(
    Suppress(SYN_ELSE)
    + Optional(OneOrMore(STATEMENT), default=None)(PROP_BODY)
)

CONDITIONAL = Group(Group(Group(Group(
    IF(TYPE_IF)
    + ZeroOrMore(ELSEIF)(TYPE_ELSEIF)
    + Optional(ELSE(TYPE_ELSE))
    # StringEnd() is because EOF can end a conditional.
    # SYN_CLOSE_BRACE is because a closed block can end a conditional.
    + (Literal(SYN_ENDIF)(TYPE_ENDIF) | StringEnd() | FollowedBy(SYN_CLOSE_BRACE))
))(PROP_BODY))(TYPE_CONDITIONAL))

ANON_BLOCK = Group(
    Literal(SYN_OPEN_BRACE)(TYPE_ANON_BLOCK)
    + Optional(OneOrMore(ROOT), default=None)(PROP_BODY)
    # StringEnd() is because EOF can end a block.
    + (Suppress(SYN_CLOSE_BRACE) | StringEnd())
)

NAMED_BLOCK = Group(
    SYN_BLOCKS(TYPE_BLOCK)
    + ~SYN_KEYWORDS
    + Optional(Word(TOKEN)(PROP_VALUE))
    + Literal(SYN_OPEN_BRACE)
    + Optional(OneOrMore(STATEMENT), default=None)(PROP_BODY)
    + (Suppress(SYN_CLOSE_BRACE) | StringEnd())
)

EMPTY_BLOCK = Group(
    SYN_BLOCKS(TYPE_EMPTY_BLOCK)
    + Optional(
        ~SYN_KEYWORDS
        + Word(TOKEN)(PROP_VALUE)
    )
)

BLOCKS = (NAMED_BLOCK | ANON_BLOCK | EMPTY_BLOCK)

SECTION << Group(
    Suppress(SYN_OPEN_BRACKET)
    + Word(TOKEN)(TYPE_SECTION)
    + Suppress(SYN_CLOSE_BRACKET)
    + Suppress(LineEnd())
    + Group(Optional(OneOrMore(
        ~SECTION
        + STATEMENT
    )))(PROP_BODY)
)

STATEMENT << (
    SECTION | COMMENT | RANDOM | BLOCKS | ANON_BLOCK | CONDITIONAL
    | ONELINERS
)

# ENDIF is to catch unmatched `endif` statements.
ROOT << (STATEMENT | Group(SYN_CLOSERS))

GRAMMAR = StringStart() + ZeroOrMore(ROOT)(PROP_BODY) + StringEnd()


# pylint: disable=too-many-branches
def structure_impl(result):
    """Recursive structure implementation."""
    body = []
    for statement in result[PROP_BODY]:
        if TYPE_IF in statement:
            body.append({
                PROP_TYPE: TYPE_IF,
                PROP_VALUE: statement[TYPE_IF][PROP_VALUE],
                PROP_BODY: structure_impl(statement.get(TYPE_IF))
            })
        if TYPE_ELSEIF in statement:
            for elseif in statement[TYPE_ELSEIF]:
                body.append({
                    PROP_TYPE: TYPE_ELSEIF,
                    PROP_VALUE: elseif[PROP_VALUE],
                    PROP_BODY: structure_impl(elseif)
                })
        if TYPE_ELSE in statement:
            body.append({
                PROP_TYPE: TYPE_ELSE,
                PROP_BODY: structure_impl(statement[TYPE_ELSE])
            })
        if TYPE_CONDITIONAL in statement:
            body.append({
                PROP_TYPE: TYPE_CONDITIONAL,
                PROP_BODY: structure_impl(statement[TYPE_CONDITIONAL])
            })
        elif TYPE_RANDOM in statement:
            body.append({
                PROP_TYPE: TYPE_RANDOM,
                PROP_BODY: structure_impl(statement[TYPE_RANDOM])
            })
        elif TYPE_CHANCE in statement:
            body.append({
                PROP_TYPE: TYPE_CHANCE,
                PROP_VALUE: int(statement[TYPE_CHANCE]),
                PROP_BODY: structure_impl(statement)
            })
        elif TYPE_SECTION in statement:
            body.append({
                PROP_TYPE: TYPE_SECTION,
                PROP_NAME: statement[TYPE_SECTION],
                PROP_BODY: structure_impl(statement)
            })
        elif TYPE_BLOCK in statement:
            body.append({
                PROP_TYPE: TYPE_BLOCK,
                PROP_NAME: statement.get(TYPE_BLOCK),
                PROP_VALUE: statement.get(PROP_VALUE),
                PROP_BODY: structure_impl(statement)
            })
        elif TYPE_EMPTY_BLOCK in statement:
            body.append({
                PROP_TYPE: TYPE_BLOCK,
                PROP_NAME: statement.get(TYPE_EMPTY_BLOCK),
                PROP_VALUE: statement.get(PROP_VALUE),
                PROP_BODY: []
            })
        elif TYPE_ANON_BLOCK in statement:
            body += structure_impl(statement)
        elif TYPE_DEFINE in statement:
            body.append({
                PROP_TYPE: TYPE_DEFINE,
                PROP_NAME: statement[TYPE_DEFINE]
            })
        elif TYPE_CONST in statement:
            body.append({
                PROP_TYPE: TYPE_CONST,
                PROP_NAME: statement[TYPE_CONST],
                PROP_VALUE: int(statement[PROP_VALUE])
            })
        elif TYPE_INCLUDE in statement:
            body.append({
                PROP_TYPE: TYPE_INCLUDE,
                PROP_NAME: statement[TYPE_INCLUDE],
                PROP_VALUE: statement.get(PROP_VALUE)
            })
        elif TYPE_ATTRIBUTE in statement:
            body.append({
                PROP_TYPE: TYPE_ATTRIBUTE,
                PROP_NAME: statement[TYPE_ATTRIBUTE],
                PROP_VALUE: statement.get(PROP_VALUE)
            })
        elif TYPE_SET in statement:
            body.append({
                PROP_TYPE: TYPE_SET,
                PROP_NAME: statement[TYPE_SET]
            })
        elif TYPE_COMMENT in statement:
            body.append({
                PROP_TYPE: TYPE_COMMENT,
                PROP_VALUE: statement[TYPE_COMMENT]
            })
    return body


def structure(result):
    """Wrapper around recursive structure function."""
    return {PROP_BODY: structure_impl(result)}


def parse(data):
    """Parse a data string."""
    try:
        result = GRAMMAR.parseString(data)
        return structure(result.asDict())
    except ParseException:
        raise ValueError('invalid RMS file')


def parse_file(path):
    """Parse a file."""
    with open(path, 'r', encoding='latin1') as handle:
        return parse(handle.read())


if __name__ == '__main__':
    import json
    import sys
    print(json.dumps(parse_file(sys.argv[1]), indent=2))
