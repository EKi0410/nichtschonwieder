# -*- coding: utf-8 -*-
"""Erzeugt build/referenz.docx — die Stilvorlage für die Word-Ausgabe.

pandoc übernimmt aus dieser Datei Seitenformat, Ränder, Schrift und alle
Absatzstile. Wer die Word-Ausgabe umformatieren will, ändert hier etwas und
baut neu — nicht im 900-Seiten-Dokument selbst.

Maße in Twips (1 mm = 56,6929), Schriftgrößen in halben Punkten.
"""
import io, os, re, shutil, subprocess, zipfile
import pypandoc

# OOXML erzwingt die Reihenfolge der Kindelemente. Ein falsch einsortiertes
# <w:spacing> macht die Datei schemawidrig, und Word zeigt das nicht als
# Fehler, sondern ignoriert stillschweigend die Formatierung. Deshalb wird
# jedes pPr hier sortiert statt von Hand in die richtige Folge gebracht.
PPR_FOLGE = ['pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr',
             'widowControl', 'numPr', 'suppressLineNumbers', 'pBdr', 'shd',
             'tabs', 'suppressAutoHyphens', 'kinsoku', 'wordWrap',
             'overflowPunct', 'topLinePunct', 'autoSpaceDE', 'autoSpaceDN',
             'bidi', 'adjustRightInd', 'snapToGrid', 'spacing', 'ind',
             'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc',
             'textDirection', 'textAlignment', 'textboxTightWrap',
             'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange']

def sortiere(xml, folge=PPR_FOLGE):
    """Zerlegt eine Elementfolge in Elemente erster Ebene und sortiert sie."""
    teile, i = [], 0
    while i < len(xml):
        if xml[i] != '<':
            i += 1
            continue
        m = re.match(r'<w:([A-Za-z]+)', xml[i:])
        if not m:
            i += 1
            continue
        tag = m.group(1)
        leer = re.match(r'<w:%s\b[^>]*/>' % tag, xml[i:])
        if leer:
            teile.append((tag, leer.group(0))); i += leer.end(); continue
        voll = re.match(r'<w:%s\b[^>]*>.*?</w:%s>' % (tag, tag), xml[i:], re.S)
        assert voll, xml[i:i + 60]
        teile.append((tag, voll.group(0))); i += voll.end()
    unbekannt = [t for t, _ in teile if t not in folge]
    assert not unbekannt, unbekannt
    teile.sort(key=lambda x: folge.index(x[0]))
    return ''.join(x for _, x in teile)


MM = 56.6929
def mm(x): return str(int(round(x * MM)))
def pt(x): return str(int(round(x * 2)))
def zpt(x): return str(int(round(x * 20)))

ARB = 'build/.referenz-arbeit'
ZIEL = 'build/referenz.docx'

SEITE = dict(breite=155.96, hoehe=233.93, oben=18, unten=18,
             aussen=16, bund=22.3)
SCHRIFT = 'Georgia'
GRUND = 10.5
DURCHSCHUSS = 14.9
EINZUG = 4.5

shutil.rmtree(ARB, ignore_errors=True)
os.makedirs(ARB)
roh = os.path.join(ARB, 'roh.docx')
io.open(roh, 'wb').write(subprocess.run(
    [pypandoc.get_pandoc_path(), '--print-default-data-file', 'reference.docx'],
    capture_output=True, check=True).stdout)
with zipfile.ZipFile(roh) as z:
    z.extractall(ARB)
os.remove(roh)
W = os.path.join(ARB, 'word')

def lade(name): return io.open(os.path.join(W, name), encoding='utf-8').read()
def sichere(name, t): io.open(os.path.join(W, name), 'w', encoding='utf-8').write(t)

s = lade('styles.xml')

def stil(sid, pPr='', rPr=''):
    global s
    m = re.search(r'(<w:style [^>]*w:styleId="%s">)(.*?)(</w:style>)' % sid, s, re.S)
    assert m, sid
    kern = m.group(2)
    kern = re.sub(r'<w:pPr>.*?</w:pPr>', '', kern, flags=re.S)
    kern = re.sub(r'<w:rPr>.*?</w:rPr>', '', kern, flags=re.S)
    kern = kern.rstrip()
    if pPr: kern += '<w:pPr>%s</w:pPr>' % sortiere(pPr)
    if rPr: kern += '<w:rPr>%s</w:rPr>' % rPr
    s = s[:m.start()] + m.group(1) + kern + m.group(3) + s[m.end():]

FONT = '<w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s" />' % ((SCHRIFT,) * 3)
SPRACHE = '<w:lang w:val="de-DE" />'

stil('Normal',
     pPr=('<w:widowControl />'
          '<w:spacing w:before="0" w:after="0" w:line="%s" w:lineRule="exact" />'
          '<w:jc w:val="both" />' % zpt(DURCHSCHUSS)),
     rPr=FONT + '<w:sz w:val="%s" /><w:szCs w:val="%s" />%s'
         % (pt(GRUND), pt(GRUND), SPRACHE))
stil('BodyText', pPr='<w:ind w:firstLine="%s" />' % mm(EINZUG))
stil('FirstParagraph', pPr='<w:ind w:firstLine="0" />')

def ueberschrift(sid, groesse, vor, nach, umbruch, lvl):
    stil(sid,
         pPr=(('<w:pageBreakBefore />' if umbruch else '')
              + '<w:keepNext /><w:keepLines />'
              + '<w:spacing w:before="%s" w:after="%s" w:line="%s" '
                'w:lineRule="auto" />' % (zpt(vor), zpt(nach), zpt(groesse * 1.18))
              + '<w:ind w:firstLine="0" /><w:jc w:val="left" />'
              + '<w:outlineLvl w:val="%d" />' % lvl),
         rPr=(FONT + '<w:b /><w:color w:val="000000" />'
              '<w:sz w:val="%s" /><w:szCs w:val="%s" />%s'
              % (pt(groesse), pt(groesse), SPRACHE)))

ueberschrift('Heading1', 19, 34, 10, True, 0)
ueberschrift('Heading2', 14, 20, 7, True, 1)
ueberschrift('Heading3', 11.5, 12, 4, False, 2)
ueberschrift('Heading4', GRUND, 9, 3, False, 3)

stil('Title', pPr='<w:jc w:val="center" /><w:spacing w:before="%s" w:after="%s" />'
                  % (zpt(120), zpt(12)),
     rPr=FONT + '<w:b /><w:sz w:val="%s" />%s' % (pt(26), SPRACHE))
stil('Subtitle', pPr='<w:jc w:val="center" /><w:spacing w:after="%s" />' % zpt(60),
     rPr=FONT + '<w:i /><w:sz w:val="%s" />%s' % (pt(13), SPRACHE))
stil('Author', pPr='<w:jc w:val="center" />',
     rPr=FONT + '<w:sz w:val="%s" />%s' % (pt(12), SPRACHE))
stil('BlockText',
     pPr=('<w:ind w:left="%s" w:right="%s" w:firstLine="0" />'
          '<w:spacing w:before="%s" w:after="%s" />'
          '<w:pBdr><w:left w:val="single" w:sz="6" w:space="8" '
          'w:color="999999" /></w:pBdr>'
          % (mm(6), mm(4), zpt(6), zpt(6))))
stil('Compact', pPr='<w:ind w:firstLine="0" /><w:spacing w:before="%s" w:after="%s" />'
                    % (zpt(2), zpt(2)))

RAHMEN = ('<w:pBdr>'
          '<w:top w:val="single" w:sz="4" w:space="4" w:color="000000" />'
          '<w:left w:val="single" w:sz="4" w:space="6" w:color="000000" />'
          '<w:bottom w:val="single" w:sz="4" w:space="4" w:color="000000" />'
          '<w:right w:val="single" w:sz="4" w:space="6" w:color="000000" />'
          '</w:pBdr>')
neu = ('<w:style w:type="paragraph" w:customStyle="1" w:styleId="startbar">'
       '<w:name w:val="startbar" /><w:basedOn w:val="BodyText" />'
       '<w:qFormat /><w:pPr>'
       + sortiere('<w:ind w:firstLine="0" />'
                  '<w:spacing w:before="%s" w:after="%s" />'
                  '<w:jc w:val="left" />' % (zpt(6), zpt(8)) + RAHMEN)
       + '</w:pPr><w:rPr>%s<w:sz w:val="%s" />%s</w:rPr></w:style>'
         % (FONT, pt(9.5), SPRACHE))
# Die achtteilige Sternezeile: linksbuendig, denn im Blocksatz reisst sie
# die Abstaende zwischen den Dimensionen auseinander.
sterne = ('<w:style w:type="paragraph" w:customStyle="1" w:styleId="sterne">'
          '<w:name w:val="sterne" /><w:basedOn w:val="BodyText" />'
          '<w:qFormat /><w:pPr>'
          + sortiere('<w:keepNext /><w:ind w:firstLine="0" />'
                     '<w:spacing w:before="%s" w:after="%s" />'
                     '<w:jc w:val="left" />' % (zpt(3), zpt(7)))
          + '</w:pPr><w:rPr>%s<w:sz w:val="%s" />%s</w:rPr></w:style>'
            % (FONT, pt(9.5), SPRACHE))
s = s.replace('</w:styles>', neu + sterne + '</w:styles>')

alt_tbl = re.search(r'<w:tblPr>\s*<w:tblInd w:w="0" w:type="dxa" />', s)
assert alt_tbl, 'Tabellenstil nicht gefunden'
s = s[:alt_tbl.start()] + (
  '<w:tblPr><w:tblInd w:w="0" w:type="dxa" /><w:tblBorders>'
  '<w:top w:val="single" w:sz="4" w:color="666666" />'
  '<w:left w:val="single" w:sz="4" w:color="666666" />'
  '<w:bottom w:val="single" w:sz="4" w:color="666666" />'
  '<w:right w:val="single" w:sz="4" w:color="666666" />'
  '<w:insideH w:val="single" w:sz="4" w:color="666666" />'
  '<w:insideV w:val="single" w:sz="4" w:color="666666" />'
  '</w:tblBorders>'
  '<w:tblCellMar>'
  '<w:top w:w="%s" w:type="dxa" /><w:left w:w="%s" w:type="dxa" />'
  '<w:bottom w:w="%s" w:type="dxa" /><w:right w:w="%s" w:type="dxa" />'
  '</w:tblCellMar>' % (mm(0.6), mm(1.0), mm(0.6), mm(1.0))) + s[alt_tbl.end():]

# Absatzstil, den pandoc in Tabellenzellen setzt, kleiner stellen.
for tsid, groesse in [('Compact', 9.0)]:
    m = re.search(r'(<w:style [^>]*w:styleId="%s">)(.*?)(</w:style>)' % tsid,
                  s, re.S)
    kern = m.group(2)
    if '<w:rPr>' not in kern:
        kern += '<w:rPr>%s<w:sz w:val="%s" />%s</w:rPr>' % (
            FONT, pt(groesse), SPRACHE)
    s = s[:m.start()] + m.group(1) + kern + m.group(3) + s[m.end():]
s = re.sub(r'<w:tblCellMar>\s*<w:top w:w="0" w:type="dxa" />.*?</w:tblCellMar>',
           '', s, count=1, flags=re.S)
sichere('styles.xml', s)

d = lade('document.xml')
sect = ('<w:sectPr>'
        '<w:footerReference w:type="default" r:id="rIdFooter" />'
        '<w:footnotePr><w:numRestart w:val="eachSect" /></w:footnotePr>'
        '<w:pgSz w:w="%s" w:h="%s" />'
        '<w:pgMar w:top="%s" w:right="%s" w:bottom="%s" w:left="%s" '
        'w:header="%s" w:footer="%s" w:gutter="%s" />'
        '</w:sectPr>'
        % (mm(SEITE['breite']), mm(SEITE['hoehe']), mm(SEITE['oben']),
           mm(SEITE['aussen']), mm(SEITE['unten']), mm(SEITE['aussen']),
           mm(10), mm(10), mm(SEITE['bund'])))
d = re.sub(r'<w:sectPr>.*?</w:sectPr>', sect, d, flags=re.S)
sichere('document.xml', d)

sichere('footer1.xml',
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
  '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
  '<w:p><w:pPr><w:ind w:firstLine="0" /><w:jc w:val="center" />'
  '<w:rPr>%s<w:sz w:val="%s" /></w:rPr></w:pPr>'
  '<w:r><w:rPr>%s<w:sz w:val="%s" /></w:rPr>'
  '<w:fldChar w:fldCharType="begin" /></w:r>'
  '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
  '<w:r><w:fldChar w:fldCharType="end" /></w:r></w:p></w:ftr>'
  % (FONT, pt(9), FONT, pt(9)))

rp = os.path.join(W, '_rels', 'document.xml.rels')
r = io.open(rp, encoding='utf-8').read().replace('</Relationships>',
  '<Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/'
  'officeDocument/2006/relationships/footer" Target="footer1.xml" />'
  '</Relationships>')
io.open(rp, 'w', encoding='utf-8').write(r)

cp = os.path.join(ARB, '[Content_Types].xml')
ct = io.open(cp, encoding='utf-8').read().replace('</Types>',
  '<Override PartName="/word/footer1.xml" ContentType="application/'
  'vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" /></Types>')
io.open(cp, 'w', encoding='utf-8').write(ct)

st = lade('settings.xml').replace('<w:zoom w:percent="100" />',
  '<w:zoom w:percent="100" /><w:mirrorMargins />'
  '<w:autoHyphenation w:val="true" />'
  '<w:consecutiveHyphenLimit w:val="3" />'
  '<w:hyphenationZone w:val="%s" />' % mm(6))
sichere('settings.xml', st)

if os.path.exists(ZIEL): os.remove(ZIEL)
with zipfile.ZipFile(ZIEL, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(cp, '[Content_Types].xml')
    for wurzel, _, dateien in os.walk(ARB):
        for f in dateien:
            p = os.path.join(wurzel, f)
            rel = os.path.relpath(p, ARB)
            if rel == '[Content_Types].xml':
                continue
            z.write(p, rel)
shutil.rmtree(ARB, ignore_errors=True)
print('%s · Seitenformat %.2f x %.2f mm · Bundsteg %.1f mm · %s %.1f pt'
      % (ZIEL, SEITE['breite'], SEITE['hoehe'], SEITE['bund'], SCHRIFT, GRUND))
