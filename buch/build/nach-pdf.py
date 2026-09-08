# -*- coding: utf-8 -*-
"""HTML -> PDF mit WeasyPrint und Bericht über die Seitenzahl.

Die Seitenzahl ist die Zahl, an der bei KDP alles hängt: Bundsteg,
Rückenstärke, Herstellungskosten und die Obergrenze von 828 Seiten. Sie wird
hier gemessen, nicht geschätzt.
"""
import io, os, sys, logging
from weasyprint import HTML, CSS

logging.getLogger('weasyprint').setLevel(logging.ERROR)
OUT = 'build/out'
html = os.path.join(OUT, 'gesamt-print.html')
pdf = os.path.join(OUT, '100-geschaeftsideen-interior.pdf')

# Kein stylesheets=-Argument: Das Stylesheet ist im HTML verlinkt und ist
# damit das einzige. Als Argument übergeben landete es in dieser
# WeasyPrint-Fassung VOR den eingebetteten pandoc-Standardstilen in der
# Kaskade — Ergebnis waren 1.472 statt 946 Seiten, ohne jede Fehlermeldung.
doc = HTML(filename=html, base_url=OUT).render()
doc.write_pdf(pdf)
n = len(doc.pages)

# KDP-Grenzwerte. Vor jedem Upload gegen die aktuellen KDP-Angaben prüfen —
# Amazon ändert sie ohne Ankündigung.
MAX_TB, MAX_HC = 828, 550
ruecken = n * 0.0572  # mm je Seite, weißes Papier 60 g
if n <= 150: bund = 9.53
elif n <= 300: bund = 12.7
elif n <= 500: bund = 15.88
elif n <= 700: bund = 19.05
else: bund = 22.23

print()
print('  PDF:            %s' % pdf)
print('  Seiten:         %d' % n)
print('  Taschenbuch:    %s (KDP-Grenze %d)'
      % ('passt' if n <= MAX_TB else 'ZU DICK', MAX_TB))
print('  Hardcover:      %s (KDP-Grenze %d)'
      % ('passt' if n <= MAX_HC else 'nicht möglich', MAX_HC))
print('  Rückenstärke:   %.1f mm  (für den Umschlagentwurf)' % ruecken)
print('  Bundsteg nötig: %.2f mm  (im CSS gesetzt: 22.30 mm)' % bund)
if bund > 22.3:
    print('  ACHTUNG: Bundsteg im CSS ist zu klein für diese Seitenzahl.')
if n > MAX_TB:
    print('  ACHTUNG: über der KDP-Obergrenze. Kürzen oder zwei Bände.')
