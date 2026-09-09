# -*- coding: utf-8 -*-
"""Setzt das Inhaltsverzeichnis hinter das Impressum.

pandoc kann das nicht: --toc setzt das Verzeichnis immer an den Anfang des
Dokuments, also vor den Schmutztitel. Die Reihenfolge im Buch ist aber
Schmutztitel, Haupttitel, Impressum, Inhalt. Deshalb wird hier aus den
Überschriften des erzeugten HTML ein Verzeichnis gebaut und an der richtigen
Stelle eingesetzt. Die Seitenzahlen trägt das Stylesheet über target-counter
ein, wenn WeasyPrint umbricht — im HTML stehen sie nicht.
"""
import io, re, sys

datei = sys.argv[1]
t = io.open(datei, encoding='utf-8').read()

# Mit --section-divs trägt nicht die Überschrift die Kennung, sondern das
# umgebende <section>, und das Tag steht oft über zwei Zeilen. pandoc stellt
# seine eigenen Klassen ("level2") den Klassen aus dem Manuskript voran, die
# Reihenfolge im class-Attribut ist also nicht verlässlich.
# pandoc bricht lange Zeilen um, auch mitten im Tag ("<section\nid=..."),
# deshalb steht überall \s+ statt eines Leerzeichens.
ABSCHNITT = re.compile(r'<section\s+id="([^"]+)"\s+class="([^"]*)"\s*>'
                       r'\s*<h([1-6])>(.*?)</h\3>', re.S)

def entitaeten(s):
    for roh, klar in (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'),
                      ('&quot;', '"'), ('&#39;', "'")):
        s = s.replace(roh, klar)
    return s

# Das Verzeichnis kommt vor den ersten Abschnitt hinter der Titelei. Das ist
# im vollständigen Band die Einleitung ("vorspann"); in Band 2 gibt es keine,
# dort ist es der erste Hauptabschnitt.
m_vor = None
for klasse in ('vorspann', 'haupt', 'nachspann', 'anhang'):
    m_vor = re.search(r'<section\s[^>]*class="[^"]*\b%s\b[^"]*"' % klasse, t)
    if m_vor:
        break
assert m_vor, 'Kein Abschnitt hinter der Titelei gefunden'
anfang = m_vor.start()

# In den Anhängen sind die Zwischentitel Gliederung, keine Kapitel. Ihre
# Bereiche werden ausgenommen, sonst stehen dreißig Registerabschnitte im
# Inhaltsverzeichnis.
anhaenge = []
for m in re.finditer(r'<section\s+id="[^"]+"\s+class="[^"]*\banhang\b[^"]*"\s*>',
                     t):
    naechster = re.search(r'<section\s+id="[^"]+"\s+class="[^"]*'
                          r'\babschnitt\b[^"]*"\s*>', t[m.end():])
    anhaenge.append((m.start(),
                     m.end() + naechster.start() if naechster else len(t)))

def in_anhang(pos):
    return any(a < pos < b for a, b in anhaenge)

eintraege = []
for m in ABSCHNITT.finditer(t, anfang):
    ebene = int(m.group(3))
    if ebene > 2:
        continue
    if ebene == 2 and in_anhang(m.start()):
        continue
    titel = entitaeten(re.sub(r'<[^>]+>', '', m.group(4))).strip()
    # Eine Kategorie ist der Auftakt zu zehn Modellkapiteln und steht im
    # Verzeichnis eine Stufe über ihnen — sonst sind 110 Einträge in Teil II
    # eine Kette ohne Gliederung.
    art = 'kategorie' if 'kategorie' in m.group(2).split() else 'kapitel'
    eintraege.append((ebene, m.group(1), titel, art))

assert eintraege, 'keine Überschriften gefunden'
zeilen = ['<nav id="TOC" role="doc-toc">', '<h1>Inhalt</h1>']
offen = 0
for ebene, kennung, titel, art in eintraege:
    while offen < ebene:
        zeilen.append('<ul>'); offen += 1
    while offen > ebene:
        zeilen.append('</li></ul>'); offen -= 1
    if zeilen[-1].startswith('<li>'):
        zeilen.append('</li>')
    zeilen.append('<li%s><a href="#%s">%s</a>'
                  % (' class="kategorie"' if art == 'kategorie' else '',
                     kennung, titel))
while offen:
    zeilen.append('</li></ul>'); offen -= 1
zeilen.append('</nav>')
nav = '\n'.join(zeilen)

# Unmittelbar vor den Vorspann setzen, also hinter das Impressum.
i = anfang
t = t[:i] + nav + '\n' + t[i:]
io.open(datei, 'w', encoding='utf-8').write(t)

e1 = sum(1 for e, _, _, _ in eintraege if e == 1)
print('  Inhaltsverzeichnis: %d Einträge (%d Ebene 1, %d Ebene 2), '
      'hinter dem Impressum' % (len(eintraege), e1, len(eintraege) - e1))
