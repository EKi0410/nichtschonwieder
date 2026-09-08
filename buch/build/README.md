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
| `out/100-geschaeftsideen.docx` | Satzvorlage | nur, wenn im Satzprogramm weitergearbeitet wird |
| `out/gesamt-*.md` | zusammengefügtes Manuskript | Zwischenergebnis, prüfbar |

## Die Kette

```
manuskript/*.md
   → build/leseordnung.py      Leseordnung, einzige Quelle
   → build/zusammenfuegen.py   eine Datei je Ausgabe
   → pandoc + build/vorlage-print.html
   → build/kdp-print.css       Satz nach KDP-Vorgaben
   → build/nach-pdf.py         PDF und Seitenmessung
```

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
| Grundschrift | 10,5 pt / 14,9 pt | Satzentscheidung |

Der Bundsteg richtet sich bei KDP nach der Seitenzahl. `nach-pdf.py` rechnet
das erforderliche Maß aus der gemessenen Seitenzahl und meldet, wenn der Wert
im Stylesheet zu klein ist. Für beide Bände liegt 22,3 mm über dem Minimum —
das ist zulässig und lässt Luft.

*Vor jedem Upload gegen die aktuellen KDP-Angaben prüfen. Amazon ändert
Seitengrenzen, Bundstegtabelle und Herstellungskosten ohne Ankündigung.*

## Zwei Dinge, die noch nicht Produktionsqualität sind

**Die Schrift.** Im Stylesheet steht Source Serif 4 mit Georgia als Rückfall.
Beide sind hier nicht installiert, gesetzt wird deshalb Liberation Serif. Die
Sterne, Pfeile und Mittelpunkte kommen aus einer CJK-Rückfallschrift. Das ist
für einen Andruck brauchbar und für die Auflage nicht. Eine Buchschrift ist
eine Entscheidung des Autors; sie ändert die Seitenzahl.

**Die Sternetabelle im Modellkapitel.** Bezeichnung und Sterne fallen je nach
Länge auf zwei Zeilen. Lesbar, aber uneinheitlich.
