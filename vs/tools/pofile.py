"""Minimal PO parser/writer for lingui format-po catalogs."""
import re

def unquote(s):
    s = s.strip()
    assert s.startswith('"') and s.endswith('"'), s
    s = s[1:-1]
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\':
            n = s[i+1]
            out.append({'n': '\n', 't': '\t', '"': '"', '\\': '\\'}.get(n, '\\' + n))
            i += 2
        else:
            out.append(c); i += 1
    return ''.join(out)

def quote(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t') + '"'

def parse(path):
    text = open(path, encoding='utf-8').read()
    blocks = text.strip('\n').split('\n\n')
    header = None
    entries = []
    for b in blocks:
        lines = b.split('\n')
        e = {'comments': [], 'msgctxt': None, 'msgid': None, 'msgstr': None}
        cur = None
        for ln in lines:
            if ln.startswith('#'):
                e['comments'].append(ln)
            elif ln.startswith('msgctxt '):
                cur = 'msgctxt'; e[cur] = unquote(ln[8:])
            elif ln.startswith('msgid '):
                cur = 'msgid'; e[cur] = unquote(ln[6:])
            elif ln.startswith('msgstr '):
                cur = 'msgstr'; e[cur] = unquote(ln[7:])
            elif ln.startswith('"'):
                e[cur] += unquote(ln)
            elif ln.strip() == '':
                pass
            else:
                raise ValueError('bad line: ' + ln)
        if e['msgid'] == '' and header is None:
            header = e
        else:
            entries.append(e)
    return header, entries

def key(e):
    return (e['msgctxt'] or '') + '\x04' + e['msgid']

def refs(e):
    out = []
    for c in e['comments']:
        if c.startswith('#: '):
            out += c[3:].split()
    return out

def write(path, header_lines, entries):
    parts = ['msgid ""\nmsgstr ""\n' + ''.join(quote(h + '\n') + '\n' for h in header_lines).rstrip('\n')]
    for e in entries:
        s = '\n'.join(e['comments'])
        if s: s += '\n'
        if e['msgctxt'] is not None:
            s += 'msgctxt ' + quote(e['msgctxt']) + '\n'
        s += 'msgid ' + quote(e['msgid']) + '\n'
        s += 'msgstr ' + quote(e['msgstr'] or '')
        parts.append(s)
    open(path, 'w', encoding='utf-8').write('\n\n'.join(parts) + '\n')
