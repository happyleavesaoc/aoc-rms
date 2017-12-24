import unittest
from rms.grammar import parse


class TestGrammar(unittest.TestCase):

    def test_include(self):
        data = "#include_drs random_map.def"
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'random_map.def', 'value': None, 'type': 'include'}
            ]
        })

    def test_const(self):
        data = "#const TEST 1"
        self.assertEqual(parse(data), {
            'body': [
                {'value': 1, 'name': 'TEST', 'type': 'const'}
            ]
        })

    def test_define(self):
        data = "#define LABEL"
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'LABEL', 'type': 'define'}
            ]
        })

    def test_attribute(self):
        data = "some_attr 1 2"
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'some_attr', 'value': ['1', '2'], 'type': 'attribute'}
            ]
        })

    def test_set(self):
        data = "set_option"
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'set_option', 'type': 'set'}
            ]
        })

    def test_comment(self):
        data = "/* hello */"
        self.assertEqual(parse(data), {
            'body': [
                {'value': '/* hello */', 'type': 'comment'}
            ]
        })

    def test_comment_unopened(self):
        data = "some_attr 1 */"
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'some_attr', 'value': ['1'], 'type': 'attribute'}
            ]
        })

    def test_section(self):
        data = "<test_section>"
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'test_section', 'type': 'section', 'body': []}
            ]
        })

    def test_block(self):
        data = "create_object arg { }"
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'create_object', 'value': 'arg', 'type': 'block', 'body': []}
            ]
        })

    def test_anon_block(self):
        data = "{ set_option }"
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'set_option', 'type': 'set'}
            ]
        })

    def test_empty_block(self):
        data = "create_object arg"
        print(parse(data))
        self.assertEqual(parse(data), {
            'body': [
                {'name': 'create_object', 'value': 'arg', 'type': 'block', 'body': []}
            ]
        })

    def test_random(self):
        data = "start_random percent_chance 10 end_random"
        self.assertEqual(parse(data), {
            'body': [
                {'type': 'random', 'body': [
                    {'type': 'chance', 'value': 10, 'body': []}
                ]}
            ]
        })

    def test_conditional(self):
        data = "if TEST elseif OTHER else endif"
        self.assertEqual(parse(data), {
            'body': [
                {'type': 'conditional', 'body': [
                    {'type': 'if', 'body': [], 'value': 'TEST'},
                    {'type': 'elseif', 'body': [], 'value': 'OTHER'},
                    {'type': 'else', 'body': []}
                ]}
            ]
        })

    def test_conditional_eof(self):
        data = "if TEST"
        self.assertEqual(parse(data), {
            'body': [
                {'type': 'conditional', 'body': [
                    {'type': 'if', 'body': [], 'value': 'TEST'}
                ]}
            ]
        })

    def test_conditional_block_eof(self):
        data = "{if TEST}"
        self.assertEqual(parse(data), {
            'body': [
                {'type': 'conditional', 'body': [
                    {'type': 'if', 'body': [], 'value': 'TEST'}
                ]}
            ]
        })

    def test_conditional_orphan(self):
        data = "if TEST endif endif"
        self.assertEqual(parse(data), {
            'body': [
                {'type': 'conditional', 'body': [
                    {'type': 'if', 'body': [], 'value': 'TEST'}
                ]}
            ]
        })

    def test_unmatched_closer(self):
        data = "endif"
        self.assertEqual(parse(data), {
            'body': []
        })

    def test_invalid(self):
        data = "elseif X"
        with self.assertRaises(ValueError):
            parse(data)
