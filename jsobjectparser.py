import re

ID_RE = re.compile(r'[a-zA-Z_\$][\w\d_\$]*')
DIGIT_RE = re.compile(r'[1-9]\d*(\.\d+)?')
BOOLEAN_RE = re.compile(r'(true|false|null)[\$\W]')
BOOLEAN_DIC = {
    'true': True,
    'false': False,
    'null': None
}

class ParseError(BaseException):
    pass

def parse_obj(s):
    items = []
    s = s[1:].strip()
    while s and not s.startswith('}'):
        key, s = parse_identifier(s)
        if not s.startswith(':'):
            raise ParseError('expect ":"')
        s = s[1:].strip()
        parser = PARSER_MAP.get(s[0], parse_other)
        value, s = parser(s)
        items.append((key, value))
        if s.startswith('}'):
            break
        if not s.startswith(','):
            raise ParseError('expect ",": %s', s)
        s = s[1:].strip()
    if not s:
        raise ParseError('expect "}"')
    s = s[1:].strip()
    return dict(items), s

def parse_str(s):
    quote = s[0]
    s = s[1:]
    parsed = ''
    while s:
        parts = s.split(quote, 1)
        if len(parts) == 1:
            raise ParseError('EOL while parse string')
        t, s = parts
        if t.endswith('\\') and not t.endswith('\\\\'):
            parsed += t + quote
            continue
        return (parsed + t), s.strip()
    raise ParseError('EOL while parse string')

def parse_array(s):
    items = []
    s = s[1:].strip()
    while s and not s.startswith(']'):
        parser = PARSER_MAP.get(s[0], parse_other)
        value, s = parser(s)
        items.append(value)
        if s.startswith(']'):
            break
        if not s.startswith(','):
            raise ParseError('expect ",": %s', s)
        s = s[1:].strip()
    if not s:
        raise ParseError('expect "]"')
    return items, s[1:].strip()

def parse_identifier(s):
    m = ID_RE.match(s)
    if not m:
        raise ParseError('expect an identifier: %s', s)
    return m.group(), s[m.end():].strip()

def parse_other(s):  #int, bool, null
    m = BOOLEAN_RE.match(s)
    if m:
        b = m.group().strip()
        obj = BOOLEAN_DIC[b]
    else:
        m = DIGIT_RE.match(s)
        if not m:
            raise ParseError('syntax error: %s', s)
        num = m.group()
        obj = int(num) if '.' not in num else float(num)
    return obj, s[m.end():].strip()


def parse(s):
    s = s.strip()
    if not s:
        return None
    parser = PARSER_MAP.get(s[0], parse_other)
    obj, remain = parser(s)
    if remain:
        raise ParseError('there is some character remain after parse')
    return obj

PARSER_MAP = {
    '{': parse_obj,
    '[': parse_array,
    '"': parse_str,
    '\'': parse_str
}

if __name__ == '__main__':
    s = """
{
    a: 'b',
    c: {
        d: 4.5,
        e: [
            {
                f: 4,
                g: true
            },
            {
                $f: "4",
                g: '5',
                h: false
            }
        ]
    }
}
    """
    from time import time
    t = time()
    for _ in range(100000):
        obj = parse(s)
    print((time()-t)/100000)
    print(obj)
    print(type(obj))