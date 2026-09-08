#!/usr/bin/env bash
# Messvariante: dieselbe Pipeline, aber als zwei Bände.
set -euo pipefail
cd "$(dirname "$0")/.."
PANDOC=$(python3 -c "import pypandoc;print(pypandoc.get_pandoc_path())")
MD="markdown+fenced_divs+bracketed_spans+pipe_tables+smart"
for b in 1 2; do
  python3 build/zusammenfuegen.py print $b
  "$PANDOC" build/out/gesamt-print-band$b.md -f "$MD" -t html5 \
    --template=build/vorlage-print.html --toc --toc-depth=2 --section-divs \
    --metadata lang=de-DE --metadata title="100 Geschäftsideen, Band $b" \
    -o build/out/gesamt-print-band$b.html
done
python3 build/baende-messen.py
