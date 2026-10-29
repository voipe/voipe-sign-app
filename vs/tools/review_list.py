#!/usr/bin/env python3
"""Print the client-facing he strings as a Markdown table (msgid | Hebrew | context path).
Usage: python3 vs/tools/review_list.py packages/lib/translations/he/web.po > list.md"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pofile  # noqa: E402
import scope  # noqa: E402


def cell(s):
    return s.replace('\\', '\\\\').replace('|', '\\|').replace('\n', '\\n').replace('<', '&lt;').replace('>', '&gt;')


_, entries = pofile.parse(sys.argv[1])
rows = [e for e in entries if scope.is_client(pofile.refs(e))]
print('| # | msgid | Hebrew | context |')
print('|---|---|---|---|')
for i, e in enumerate(rows, 1):
    refs = [r for r in pofile.refs(e) if scope.is_client([r])]
    ctx = ', '.join(refs[:3]) + (' (+%d)' % (len(refs) - 3) if len(refs) > 3 else '')
    if e['msgctxt']:
        ctx = '[%s] ' % e['msgctxt'] + ctx
    print('| %d | %s | %s | %s |' % (i, cell(e['msgid']), cell(e['msgstr']), cell(ctx)))
