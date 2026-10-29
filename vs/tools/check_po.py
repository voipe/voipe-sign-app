#!/usr/bin/env python3
"""Validate a lingui .po catalog against its msgids (VoIPe fork, Track F).

Checks, for every non-empty msgstr:
  * the same multiset of simple placeholders  {name} / {0}
  * the same multiset of JSX tags            <0>  </0>  <0/>
  * the same ICU heads                       {count, plural, ...} / {x, select, ...}
  * '#' kept when the msgid uses it inside an ICU plural
  * balanced braces
  * no vendor name ("Documenso") in the translation
Also prints coverage (total and, with --scope, for the client-facing scope).

Usage: python3 vs/tools/check_po.py packages/lib/translations/he/web.po [--scope]
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pofile  # noqa: E402

TAG = re.compile(r'</?\d+\s*/?>')
ICU = re.compile(r'\{\s*([A-Za-z0-9_.]+)\s*,\s*(plural|select|selectordinal)\s*,')


def balanced(s):
    depth = 0
    for ch in s:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def simple_placeholders(s):
    """Return {name} placeholders, skipping ICU branch bodies such as `one {Day}`."""
    out = []

    def parse(i, in_icu):
        # parse until matching '}' (or end); in_icu: we are in the branches part of an ICU block
        while i < len(s):
            ch = s[i]
            if ch == '{':
                j = s.find('}', i)
                inner = s[i + 1:j] if j != -1 else ''
                m = re.match(r'\s*([A-Za-z0-9_.]+)\s*,\s*(plural|select|selectordinal)\s*,', s[i + 1:])
                if in_icu:
                    i = parse(i + 1, False)  # branch body
                elif m:
                    i = parse(i + 1 + m.end(), True)
                elif j != -1 and '{' not in inner and re.fullmatch(r'\s*[A-Za-z0-9_.]+\s*', inner):
                    out.append(inner.strip())
                    i = j + 1
                else:
                    i = parse(i + 1, False)
            elif ch == '}':
                return i + 1
            else:
                i += 1
        return i

    parse(0, False)
    return out


def ms(lst):
    return sorted(lst)


def check(src, dst):
    errs = []
    if not balanced(dst):
        errs.append('unbalanced braces')
    if set(simple_placeholders(src)) != set(simple_placeholders(dst)):
        errs.append('placeholders %s != %s' % (ms(simple_placeholders(src)), ms(simple_placeholders(dst))))
    if ms(TAG.findall(src)) != ms(TAG.findall(dst)):
        errs.append('tags %s != %s' % (ms(TAG.findall(src)), ms(TAG.findall(dst))))
    if ms(ICU.findall(src)) != ms(ICU.findall(dst)):
        errs.append('icu %s != %s' % (ICU.findall(src), ICU.findall(dst)))
    if ICU.search(src) and '#' in src and '#' not in dst:
        errs.append("'#' dropped")
    if 'documenso' in dst.lower():
        errs.append('vendor name in translation')
    return errs


def main():
    path = sys.argv[1]
    use_scope = '--scope' in sys.argv
    _, entries = pofile.parse(path)
    bad = 0
    done = 0
    scope_total = scope_done = 0
    if use_scope:
        import scope
    for e in entries:
        if use_scope and scope.is_client(pofile.refs(e)):
            scope_total += 1
            scope_done += bool(e['msgstr'])
        if not e['msgstr']:
            continue
        done += 1
        errs = check(e['msgid'], e['msgstr'])
        if errs:
            bad += 1
            print('ERROR %r -> %r: %s' % (e['msgid'], e['msgstr'], '; '.join(errs)))
    print('translated %d/%d (%.1f%%)' % (done, len(entries), 100.0 * done / len(entries)))
    if use_scope:
        print('client-facing %d/%d (%.1f%%)' % (scope_done, scope_total, 100.0 * scope_done / max(scope_total, 1)))
    print('errors: %d' % bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
