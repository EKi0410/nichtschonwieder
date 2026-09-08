# -*- coding: utf-8 -*-
"""Wo gehen die Seiten hin? Nutzt den Lesezeichenbaum des PDF."""
import logging
from weasyprint import HTML, CSS
logging.getLogger('weasyprint').setLevel(logging.ERROR)
doc = HTML(filename='build/out/gesamt-print.html', base_url='build/out').render(
    stylesheets=[CSS(filename='build/kdp-print.css')])
N = len(doc.pages)
flat = []
def lauf(knoten, tiefe=0):
    for k in knoten:
        label, (seite, _x, _y), kinder, _state = k
        flat.append((tiefe, label, seite + 1))
        lauf(kinder, tiefe + 1)
lauf(doc.make_bookmark_tree())
top = [(l, p) for t, l, p in flat if t == 0]
print('Seiten gesamt: %d' % N)
print('%-52s %5s %5s' % ('Abschnitt (Ebene 1)', 'ab S.', 'Seiten'))
for i, (l, p) in enumerate(top):
    ende = top[i + 1][1] if i + 1 < len(top) else N + 1
    print('%-52s %5d %5d' % (l[:52], p, ende - p))
# Kategorien einzeln
print()
kats = [(l, p) for t, l, p in flat if l.startswith('Kategorie ')]
for i, (l, p) in enumerate(kats):
    ende = kats[i + 1][1] if i + 1 < len(kats) else None
    if ende: print('  %-50s %5d %5d' % (l[:50], p, ende - p))
