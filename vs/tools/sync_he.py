#!/usr/bin/env python3
"""Sync packages/lib/translations/he/web.po from en/web.po.
Existing he translations are kept; extra JSON files (key = msgctxt\\x04msgid or msgid) override."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pofile  # noqa: E402
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'packages', 'lib', 'translations')
HEADER = [
    'POT-Creation-Date: 2024-07-24 13:01+1000', 'MIME-Version: 1.0', 'Content-Type: text/plain; charset=utf-8',
    'Content-Transfer-Encoding: 8bit', 'X-Generator: @lingui/cli', 'Language: he', 'Project-Id-Version: ',
    'Report-Msgid-Bugs-To: ', 'PO-Revision-Date: ', 'Last-Translator: ', 'Language-Team: ',
    'Plural-Forms: nplurals=2; plural=(n != 1);',
]
def main(jsons):
    _, en = pofile.parse(ROOT + '/en/web.po')
    he_path = ROOT + '/he/web.po'
    old = {}
    if os.path.exists(he_path):
        _, he = pofile.parse(he_path)
        old = {pofile.key(e): e['msgstr'] for e in he if e['msgstr']}
    for j in jsons:
        d = json.load(open(j, encoding='utf-8'))
        for k, v in d.items():
            if '\x04' not in k:
                k = '\x04' + k
            old[k] = v
    out = []
    used = 0
    for e in en:
        k = pofile.key(e)
        t = old.get(k, '')
        used += bool(t)
        out.append({'comments': e['comments'], 'msgctxt': e['msgctxt'], 'msgid': e['msgid'], 'msgstr': t})
    os.makedirs(os.path.dirname(he_path), exist_ok=True)
    pofile.write(he_path, HEADER, out)
    print('entries', len(out), 'translated', used)
if __name__ == '__main__':
    main(sys.argv[1:])
