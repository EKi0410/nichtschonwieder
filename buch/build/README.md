# Vom Manuskript zur KDP-Datei

136 Markdown-Dateien, ein Befehl:

```bash
cd buch
bash build/bauen.sh          # ein Band, alle drei Ausgabeformate
bash build/bauen-baende.sh   # dasselbe als zwei Bände, mit Seitenmessung
```

Voraussetzung einmalig: `pip install pypandoc-binary weasyprint`. Für die
Sichtprüfung der Seiten zusätzlich `poppler-utils`.

## Was gebaut wird

| Datei | Wofür | Bei KDP |
|---|---|---|
| `out/100-geschaeftsideen-interior.pdf` | Buchblock | Taschenbuch, Feld „Manuskript" |
| `out/100-geschaeftsideen.epub` | E-Book | Kindle |
| `out/100-geschaeftsideen.docx` | Arbeitsdokument in Word | Taschenbuch, Feld „Manuskript" (KDP nimmt DOCX) |
| `out/band1.docx`, `out/band2.docx` | dasselbe als zwei Bände | dito |
| `out/gesamt-*.md` | zusammengefügtes Manuskript | Zwischenergebnis, prüfbar |

## Die Kette

```
manuskript/*.md
   → build/leseordnung.py      Leseordnung, einzige Quelle
   → build/zusammenfuegen.py   eine Datei je Ausgabe
   → pandoc + build/vorlage-print.html
   → build/kdp-print.css       Satz nach KDP-Vorgaben
   → build/nach-pdf.py         PDF und Seitenmessung

manuskript/*.md
   → build/zusammenfuegen.py docx
   → build/referenz-bauen.py    Stilvorlage referenz.docx
   → pandoc --reference-doc
```

## Die Word-Ausgabe

`referenz-bauen.py` erzeugt `referenz.docx` — die Stilvorlage. pandoc übernimmt
daraus Seitenformat, Ränder, Bundsteg, Schrift und alle Absatzstile. **Wer die
Word-Ausgabe umformatieren will, ändert dort etwas und baut neu, nicht im
900-Seiten-Dokument.** Enthalten sind: KDP-Trimformat mit gespiegelten Rändern
und 22,3 mm Bundsteg, Georgia 10,5 pt auf 14,9 pt, deutsche Silbentrennung,
Fußzeile mit Seitenzahl, Überschriften 1 bis 4 mit Seitenumbruch auf den
Ebenen 1 und 2, ein umrandeter Absatzstil `startbar` und ein linksbündiger
`sterne`.

Das Inhaltsverzeichnis ist ein Word-Feld: beim ersten Öffnen mit **F9**
aktualisieren, dann stehen die Seitenzahlen drin. Die Gliederung im
Navigationsbereich funktioniert sofort — bei 133 Kapiteln ist das der
eigentliche Grund, in Word zu arbeiten.

**Zwei Eingriffe nur für Word**, beide im Skript kommentiert:

- Das achtteilige Sternegitter wird eine Zeile. Als Tabelle mit vier Spalten à
  25 Prozent brechen die Zellen in Word auf drei bis fünf Zeilen um — aus zwei
  Zeilen wird eine halbe Seite. Im Druck bleibt das Gitter.
- Kästen und Sternezeile gehen als `custom-style` durch, nicht als Klasse. Der
  docx-Writer von pandoc ignoriert eine reine Div-Klasse stillschweigend; der
  Kasten war in der ersten Fassung ein Absatz ohne Rahmen.

**Die Seitenzahl in Word ist nicht die Seitenzahl des Buches.** Word und CSS
brechen unterschiedlich um, und die Zahl hängt an der installierten Schrift:
ohne Georgia setzt LibreOffice hier DejaVu Serif und braucht 21 Prozent mehr
Seiten — an einer Stichprobe von Teil I gemessen, 46 statt 38 Seiten. **Der
Druckstand ist das PDF, nicht das Word-Dokument.**

**Warum das Inhaltsverzeichnis selbst gebaut wird.** `--toc` setzt es immer an
den Dokumentanfang, also vor den Schmutztitel. Die Reihenfolge im Buch ist
Schmutztitel, Haupttitel, Impressum, Inhalt. `inhalt-einsetzen.py` liest daher
die Überschriften aus dem erzeugten HTML und setzt das Verzeichnis hinter das
Impressum; die Seitenzahlen trägt das Stylesheet über `target-counter` ein.
136 Einträge, aus dem Dokument selbst, nicht getippt.

**Warum eine eigene pandoc-Vorlage.** `--standalone` bettet ein eigenes
Stylesheet ein, das in der Kaskade vor dem übergebenen liegt. Ergebnis waren
1.472 statt 946 Seiten, ohne eine einzige Warnung. Die Vorlage in
`vorlage-print.html` verlinkt genau ein Stylesheet, sonst nichts.

## Was das Zusammenfügen am Manuskript ändert

Nichts am Text. Fünf Eingriffe an der Form, alle im Skript kommentiert:

1. **Herstellungshinweise entfernt.** Die HTML-Kommentare im Titelblatt sind
   Anweisungen an den Satz und gehören in keine Ausgabe.
2. **Startbarkeits-Marker wird ein Kasten.** Im Manuskript ist er ein
   Codeblock, damit die Ausrichtung im Editor stimmt. Gesetzt ist er ein
   Kasten, keine Schreibmaschinenschrift.
3. **Titelblatt ohne Überschriftenauszeichnung.** Titel und Untertitel sind
   dort Schaubild. Als Überschrift ausgezeichnet stünde der Untertitel des
   Buches als Kapitel im Inhaltsverzeichnis.
4. **Modellkapitel eine Ebene höher.** Im Manuskript ist ein Modellkapitel
   `###` unter `## Kategorie`. Für Satz und Navigation muss es dieselbe Ebene
   haben wie ein Kapitel aus Teil I — sonst enthält das Inhaltsverzeichnis
   entweder kein einziges Modell oder jeden Unterabschnitt von Teil I.
5. **Sternespalte der Modellmatrix verdichtet.** `4 3 4 3 · 3 5 4 3` braucht
   28 mm Spaltenbreite, vorhanden sind 23 — die Spalte lief in die
   Modellspalte hinein. Die Legende von Anhang B beschreibt die Kurzform
   (`43454543`) ohnehin als das gemeinte Format.

**Das statische Inhaltsverzeichnis der Titelei fliegt in jeder Ausgabe
heraus.** Im Druck erzeugt pandoc es neu, und das Stylesheet trägt über
`target-counter` echte Seitenzahlen ein. Im E-Book macht das Lesegerät die
Navigation. `titelei-03-inhaltsverzeichnis.md` bleibt im Manuskript als
Prüfstück: Wenn die 133 Einträge dort und im PDF nicht übereinstimmen, fehlt
eine Datei in der Leseordnung.

## KDP-Werte, die im Stylesheet stehen

| Wert | Gesetzt | Grund |
|---|---|---|
| Trimformat | 155,96 × 233,93 mm | KDP 6,14 × 9,21 Zoll |
| Beschnitt | keiner | kein Bild läuft an den Rand |
| Bundsteg | 22,3 mm | KDP-Mindestmaß 601–828 Seiten |
| Außen, oben, unten | 16 / 18 / 18 mm | Satzentscheidung, KDP-Minimum 6,35 mm |
| Grundschrift | Linux Libertine O, 10,5 / 14,6 pt | Satzentscheidung |

Der Bundsteg richtet sich bei KDP nach der Seitenzahl. `nach-pdf.py` rechnet
das erforderliche Maß aus der gemessenen Seitenzahl und meldet, wenn der Wert
im Stylesheet zu klein ist. Für beide Bände liegt 22,3 mm über dem Minimum —
das ist zulässig und lässt Luft.

*Vor jedem Upload gegen die aktuellen KDP-Angaben prüfen. Amazon ändert
Seitengrenzen, Bundstegtabelle und Herstellungskosten ohne Ankündigung.*

## Die Schrift

**Linux Libertine O**, 10,5 pt auf 14,6 pt. Eine echte Buchschrift mit
brauchbarer Kursive, in Debian und Ubuntu als `fonts-linuxlibertine` verfügbar
und frei verwendbar. Gewählt nach einem Vergleich von sieben Serifenschriften
an einer Stichprobe von 26.700 Wörtern; bei gleicher optischer Größe lagen alle
sieben innerhalb von drei Prozent, die Wahl ist also keine Frage der Seitenzahl,
sondern des Aussehens.

**Die Sterne kommen aus FreeSerif**, weil keine Buchschrift den leeren Stern ☆
enthält. Ohne Auszeichnung holt sich der gefüllte ★ seine Form aus der
Buchschrift und der leere aus einer CJK-Rückfallschrift — das Paar passt dann
nicht zusammen. Deshalb fasst `zusammenfuegen.py` jede Sternefolge in eine
Auszeichnung `.sternfolge`, die als Ganzes aus FreeSerif kommt.

## Was der Produktionsapparat nicht mehr enthält

Die Klammern *(Vor Drucklegung prüfen: …)* richten sich an den Hersteller, nicht
an den Leser. Sie stehen im Manuskript und in keiner Ausgabe. Ebenso entfällt
die Aufzählung der 57 Prüfpunkte in Anhang D — mit den Klammern im Text ist sie
ohne Bezug; die drei leserseitigen Abschnitte des Anhangs bleiben. Im Impressum
entfallen die Zeilen für Druckerei, ISBN und Umschlag, solange die Angaben nicht
vorliegen. **Vollständig geführt werden alle offenen Punkte in
`05-recherche-backlog.md` und `06-kapitelregister.md`.**
