# -*- coding: utf-8 -*-
"""Leseordnung des Buches — einzige Quelle für alle Bauschritte.

Wer ein Kapitel hinzufügt, ändert diese Datei und sonst nichts. Das
Inhaltsverzeichnis, die Anhänge B bis D und der Satz lesen alle hier.
"""

KATEGORIEN = [('A', 1, 10), ('B', 11, 20), ('C', 21, 30), ('D', 31, 40),
              ('E', 41, 50), ('F', 51, 60), ('G', 61, 70), ('H', 71, 80),
              ('I', 81, 90), ('J', 91, 100)]

# (Datei, Teilbereich). Teilbereich steuert Seitenzahlen, Umbrüche und
# was in welche Ausgabe kommt.
def leseordnung():
    o = [('titelei-01-titelblatt.md', 'titelei'),
         ('titelei-02-impressum.md', 'titelei'),
         ('titelei-03-inhaltsverzeichnis.md', 'inhalt')]
    o.append(('einleitung.md', 'vorspann'))
    o += [('teil1-kap%02d.md' % i, 'haupt') for i in range(1, 8)]
    o.append(('teil1-zwischenstueck.md', 'haupt'))
    for c, a, b in KATEGORIEN:
        o.append(('teil2-%s00-einfuehrung.md' % c, 'haupt'))
        o += [('teil2-%s%02d.md' % (c, n), 'haupt') for n in range(a, b + 1)]
    o += [('teil3-kap%02d.md' % i, 'haupt') for i in range(1, 9)]
    o += [('nachwort.md', 'nachspann'),
          ('nachwort-2-unterstuetzung.md', 'nachspann'),
          ('anhang-a-bewertungsbogen.md', 'anhang'),
          ('anhang-b-modellmatrix.md', 'anhang'),
          ('anhang-c-register.md', 'anhang'),
          ('anhang-d-quellen.md', 'anhang')]
    return o

TITEL = '100 Geschäftsideen'
UNTERTITEL = 'Und warum deine ständige Suche danach das Problem ist'
AUTOR = 'Jan-Erik Stern'
SPRACHE = 'de-DE'
