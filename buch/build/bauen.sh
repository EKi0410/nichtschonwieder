#!/usr/bin/env bash
# Baut aus den 136 Manuskriptdateien die Dateien, die bei KDP hochgeladen
# werden. Aufruf aus dem Verzeichnis buch/:  bash build/bauen.sh
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=build/out
mkdir -p "$OUT"
PANDOC=$(python3 -c "import pypandoc,os;print(pypandoc.get_pandoc_path())")
MD_EIN="markdown+fenced_divs+bracketed_spans+pipe_tables+smart"

echo "== 1. Zusammenfügen =="
for z in print epub docx; do python3 build/zusammenfuegen.py "$z"; done

echo "== 2. Druckausgabe (PDF für KDP Paperback) =="
"$PANDOC" "$OUT/gesamt-print.md" -f "$MD_EIN" -t html5 \
  --template=build/vorlage-print.html --toc --toc-depth=2 --section-divs \
  --metadata lang=de-DE --metadata title="100 Geschäftsideen" \
  -o "$OUT/gesamt-print.html"
python3 build/nach-pdf.py

echo "== 3. E-Book (EPUB für Kindle) =="
"$PANDOC" "$OUT/gesamt-epub.md" -f "$MD_EIN" -t epub3 \
  --toc --toc-depth=2 --epub-chapter-level=2 \
  --metadata lang=de-DE \
  -o "$OUT/100-geschaeftsideen.epub"

echo "== 4. Word-Ausgabe (DOCX, das Arbeitsdokument) =="
python3 build/referenz-bauen.py
"$PANDOC" "$OUT/gesamt-docx.md" -f "$MD_EIN" -t docx \
  --reference-doc=build/referenz.docx --toc --toc-depth=2 \
  --metadata lang=de-DE \
  -o "$OUT/100-geschaeftsideen.docx"

echo
ls -lh "$OUT" | awk 'NR>1 {printf "  %-40s %s\n", $9, $5}'
