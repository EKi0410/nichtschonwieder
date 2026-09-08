# -*- coding: utf-8 -*-
"""Fügt die 136 Manuskriptdateien zu einer Satzvorlage zusammen.

    python3 build/zusammenfuegen.py print   -> build/out/gesamt-print.md
    python3 build/zusammenfuegen.py epub    -> build/out/gesamt-epub.md
    python3 build/zusammenfuegen.py docx    -> build/out/gesamt-docx.md

Drei Ziele, weil dieselbe Datei nicht für alle drei taugt. Der wichtigste
Unterschied: Das statische Inhaltsverzeichnis aus der Titelei fliegt in allen
drei Ausgaben heraus. Im Druck erzeugt pandoc es neu und der Satz trägt die
Seitenzahlen ein; im E-Book macht das Lesegerät die Navigation. Ein getipptes
Verzeichnis mit 133 Einträgen wäre in jeder Ausgabe die erste Fehlerquelle.
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leseordnung import leseordnung, TITEL, UNTERTITEL, AUTOR, SPRACHE

M = 'manuskript/'
ZIEL = (sys.argv[1] if len(sys.argv) > 1 else 'print')
assert ZIEL in ('print', 'epub', 'docx'), ZIEL
# Optional: nur ein Band. 1 = Denkweise und Kategorien A bis E,
# 2 = Kategorien F bis J, Teil III, Anhänge.
BAND = (sys.argv[2] if len(sys.argv) > 2 else '')
assert BAND in ('', '1', '2'), BAND

def im_band(datei):
    if not BAND: return True
    kat = datei[6:7] if datei.startswith('teil2-') else None
    if BAND == '1':
        if datei.startswith('teil3-'): return False
        if datei.startswith('nachwort'): return False
        if datei.startswith('anhang-') and 'anhang-a' not in datei: return False
        return kat is None or kat <= 'E'
    # Band 2: kein Teil I, keine Einleitung des ersten Bandes
    if datei.startswith('teil1-') and 'zwischenstueck' not in datei: return False
    if datei == 'einleitung.md': return False
    return kat is None or kat >= 'F'

# Was in welcher Ausgabe entfällt
WEG = {'print': {'titelei-03-inhaltsverzeichnis.md'},
       'docx':  {'titelei-03-inhaltsverzeichnis.md'},
       'epub':  {'titelei-01-titelblatt.md',
                 'titelei-03-inhaltsverzeichnis.md'}}[ZIEL]


def aufbereiten(text, bereich):
    # 1. Herstellungshinweise entfernen. Sie stehen als HTML-Kommentar im
    #    Manuskript und gehören in keine Ausgabe.
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)

    # 2. Startbarkeits-Marker: im Manuskript ein Codeblock, damit die
    #    Ausrichtung im Editor stimmt. Im Buch ist er ein Kasten, keine
    #    Schreibmaschinenschrift.
    text = re.sub(
        r'```\nSTARTBAR MIT(.*?)```',
        lambda m: '::: startbar\n**Startbar mit** — %s\n:::'
                  % ' '.join(m.group(1).split()),
        text, flags=re.S)

    # 3. Das Stufendiagramm bleibt vorformatiert, bekommt aber eine Klasse,
    #    damit es im Satz schmaler gesetzt und umbrochen werden kann.
    text = re.sub(r'```\n((?:[^\n]*→[^\n]*\n)+)```',
                  lambda m: '``` {.stufen}\n%s```' % m.group(1), text)

    # 4. Überschriftenebenen vereinheitlichen. Im Manuskript ist ein
    #    Modellkapitel `###`, weil es unter `## Kategorie` steht. Für Satz und
    #    Navigation muss ein Modellkapitel aber dieselbe Ebene haben wie ein
    #    Kapitel aus Teil I — sonst steht im Inhaltsverzeichnis entweder kein
    #    Modell oder jeder Unterabschnitt von Teil I mit drin. Also eine Ebene
    #    hoch, samt den Unterabschnitten darunter.
    # 3b. Titelblatt: Titel und Untertitel sind dort Schaubild, nicht
    #     Gliederung. Als Überschrift ausgezeichnet landen sie sonst im
    #     Inhaltsverzeichnis — der Untertitel des Buches als Kapitel.
    if bereich == 'titelblatt':
        zeilen = []
        for z in text.split('\n'):
            k = z.lstrip('#').strip()
            if not k: continue
            if z.startswith('# '):    zeilen.append('[%s]{.haupttitel}' % k)
            elif z.startswith('## '): zeilen.append('[%s]{.untertitel}' % k)
            else:                     zeilen.append('[%s]{.titelzeile}' % k)
        return '\n\n'.join(zeilen)

    if bereich == 'modell':
        # Reihenfolge zählt: erst die Dreier, dann die Vierer. `^### ` trifft
        # `#### ` nicht, weil das Leerzeichen im Muster steht — umgekehrt würde
        # der zweite Durchgang das Ergebnis des ersten noch einmal anheben.
        text = re.sub(r'^### ', '## ', text, flags=re.M)
        text = re.sub(r'^#### ', '### ', text, flags=re.M)

    # 5. Sternespalte der Modellmatrix verdichten. Im Manuskript steht sie als
    #    `4 3 4 3 · 3 5 4 3`, damit sie im Editor lesbar bleibt. Gesetzt braucht
    #    diese Form 28 mm Spaltenbreite, vorhanden sind 23 — die Spalte lief in
    #    die Modellspalte hinein. Die Legende von Anhang B beschreibt die
    #    Kurzform (`43454543`) ohnehin als das gemeinte Format, es ist also
    #    keine neue Entscheidung, sondern die dort erklärte Schreibweise.
    text = re.sub(r'`(\d) (\d) (\d) (\d) · (\d) (\d) (\d) (\d)`',
                  r'`\1\2\3\4\5\6\7\8`', text)

    text = re.sub(r'\n{4,}', '\n\n\n', text).strip()
    return text


teile, fehlt = [], []
for datei, bereich in leseordnung():
    if datei in WEG or not im_band(datei):
        continue
    p = M + datei
    if not os.path.exists(p):
        fehlt.append(datei); continue
    roh = io.open(p, encoding='utf-8').read()
    typ = ('matrix' if datei.startswith('anhang-b')
           else 'titelblatt' if datei.startswith('titelei-01')
           else 'modell' if re.match(r'teil2-[A-J]\d', datei)
                        and '00-einfuehrung' not in datei
           else 'kategorie' if '00-einfuehrung' in datei
           else 'kapitel')
    aufbereitet = aufbereiten(roh, typ)
    if not aufbereitet:
        fehlt.append(datei + ' (leer nach Aufbereitung)'); continue
    teile.append('::: {.abschnitt .%s .%s}\n\n%s\n\n:::'
                 % (bereich, typ, aufbereitet))

assert not fehlt, fehlt

kopf = [
    '---',
    'title: |', '  %s' % TITEL,
    'subtitle: |', '  %s' % UNTERTITEL,
    'author: |', '  %s' % AUTOR,
    'lang: %s' % SPRACHE,
    'toc-title: Inhalt',
    '---', '',
]
aus = 'build/out/gesamt-%s%s.md' % (ZIEL, '-band' + BAND if BAND else '')
io.open(aus, 'w', encoding='utf-8').write('\n'.join(kopf) + '\n\n'.join(teile) + '\n')

t = io.open(aus, encoding='utf-8').read()
print('%-22s %6d Wörter · %6d Zeilen · %s Dateien'
      % (aus, len(t.split()), t.count('\n'), len(teile)))
print('  Startbar-Kästen: %d · Codeblöcke übrig: %d · HTML-Kommentare: %d'
      % (t.count('::: startbar'), t.count('```') // 2, t.count('<!--')))
