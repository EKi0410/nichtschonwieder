# -*- coding: utf-8 -*-
import logging
from weasyprint import HTML
logging.getLogger('weasyprint').setLevel(logging.ERROR)
ges = 0
for b in ('1', '2'):
    d = HTML(filename='build/out/gesamt-print-band%s.html' % b,
             base_url='build/out').render()
    d.write_pdf('build/out/band%s-interior.pdf' % b)
    n = len(d.pages); ges += n
    print('Band %s: %4d Seiten · Rücken %4.1f mm · Taschenbuch %s · Hardcover %s'
          % (b, n, n * 0.0572, 'passt   ' if n <= 828 else 'ZU DICK ',
             'passt' if n <= 550 else 'zu dick'))
print('Summe:   %4d Seiten' % ges)
