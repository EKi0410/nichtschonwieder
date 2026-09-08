## 7. Automatisierung, Softwarefrage, Skalierung — in der Praxis

Der Entscheidungsbaum vor jeder Softwareentwicklung steht in Teil I, Kapitel 7,
und er hat drei Bedingungen: Das Problem wurde in der eigenen Dienstleistung oft
genug selbst gelöst, der Vertriebsweg existiert, und die Software entlastet den
eigenen Betrieb so stark, dass sie sich auch ohne einen einzigen Fremdkunden
rechnet.

Dieses Kapitel setzt das voraus und behandelt, was danach kommt: **Wie man diese
Entscheidungen im Alltag trifft, wenn der Kalender voll ist und jemand eine
Lösung verspricht.** In den hundert Modellkapiteln wurde die Softwarefrage
hundertmal gestellt, und die Antwort lautete in gut zwei von drei Fällen nein.
Die Muster dahinter sind das, was übrig bleibt.

### Make or buy: die Frage, die falsch gestellt wird

Die Frage ist nie „selbst bauen oder kaufen". Sie lautet: **Welchen Teil kaufen
und welchen bauen?**

In den Modellen dieses Buches, in denen Software richtig war, ist die Antwort
fast immer geteilt. Sensorik und Portal gekauft, das prüffähige Protokoll
gebaut. Versandsoftware gekauft, der Stellenmarkt gebaut. Lernplattform
gekauft, nichts gebaut. Verwaltungssoftware gekauft, die Betreiberpflichten-Akte
gebaut.

**Das Muster ist überall dasselbe: Gekauft wird, was viele brauchen. Gebaut
wird, was nur dein Geschäft braucht — und was dein Unterschied ist.**

Daraus folgt eine unbequeme Regel: **Wenn du etwas bauen willst, das es zu
kaufen gibt, ist der Grund meistens Ungeduld oder Stolz.** Beides ist teuer. Ein
Buchhaltungssystem, ein Ticketsystem, eine Kursplattform, ein Bewerberportal,
eine Warenwirtschaft — das sind reife Märkte mit Anbietern, die zwanzig Jahre
Pflegearbeit hinter sich haben. Wer dort eigene Lösungen baut, pflegt
lebenslang Rechenkerne statt Kunden zu betreuen.

### Die drei Kosten, die in jeder Software-Rechnung fehlen

Vibecoding hat die Herstellungskosten von Software gegen null gedrückt. An drei
Dingen hat es nichts geändert, und sie sind der eigentliche Preis.

**Betrieb.** Server, Updates, Sicherheitslücken, Ausfälle, Datensicherung. Das
ist kein Aufwand von einmalig, sondern von immer — und er kommt am
Freitagabend.

**Support.** Wenn deine Software Kunden hat, hat sie Fragen. Zwanzig
Nutzer erzeugen mehrere Stunden im Monat, hundert Nutzer erzeugen eine
Teilzeitstelle. **Das ist die Kostenposition, die in jeder Kalkulation fehlt,
die ich gesehen habe.**

**Vertrieb.** Eine Software verkauft sich nicht, weil sie existiert. Sie
verkauft sich über denselben mühsamen Weg wie eine Dienstleistung — nur dass der
Ticketpreis meistens kleiner ist.

Deshalb steht in den Modellkapiteln, in denen Software abgelehnt wird, so oft
derselbe Satz: **Die Dienstleistung ist das bessere Geschäft.** Nicht weil
Software schlecht wäre, sondern weil dieselbe Zeit in der Dienstleistung
sofort Geld bringt und in der Software erst in zwei Jahren — wenn überhaupt.

### Interne Amortisation: die Bedingung, die zählt

Von den drei Bedingungen des Softwaretests ist die dritte die entscheidende, und
sie ist auch die, die man am leichtesten prüfen kann.

**Frage: Was würde diese Software mich einsparen, wenn niemand sie kauft?**

In H71 lautet die Antwort: eine Stelle. Bei zweihundert Objekten mit je acht
befristeten Nachweisen ist die Pflege von Hand nicht mehr fehlerfrei möglich —
also rechnet sich die Entwicklung, bevor der erste Fremdkunde existiert. In J95
lautet sie: jeder automatisierte Vorgang senkt direkt Personalkosten in einem
Geschäft, das nur aus Personalkosten besteht.

In den Fällen, in denen die Antwort „ein paar Stunden im Monat" lautet, ist die
Entwicklung falsch — auch wenn man sicher ist, dass andere sie kaufen würden.
**Denn wenn sie dir nur ein paar Stunden bringt, hast du keinen Grund, sie zu
pflegen, wenn der Verkauf schleppend läuft.** Und dann pflegst du sie nicht, und
dann ist sie nach einem Jahr wertlos.

### Was Skalierung im Alltag wirklich bedeutet

Skalierung klingt nach mehr Umsatz bei gleicher Arbeit. Im Alltag heißt sie
zunächst: **mehr Vorgänge, mehr Fehler, mehr Fragen, mehr Koordination.**

Was in diesem Buch immer wieder auffällt: Die Modelle mit fünf Sternen bei
Skalierbarkeit haben eines gemeinsam — sie haben etwas, das mit der Menge nicht
mitwächst. Ein Franchise wächst über Nehmer, die selbst zahlen und selbst
arbeiten. Ein Selfstorage wächst über Boxen, die niemand betreut. Eine
Videobibliothek wächst über Dateien, die niemand anfasst.

**Und die Modelle mit zwei Sternen haben ebenfalls eines gemeinsam: Jeder
zusätzliche Euro Umsatz bringt eine zusätzliche Stunde Arbeit mit.** Das ist
kein Fehler — die meisten guten Geschäfte funktionieren so —, aber es bestimmt
die Obergrenze, und man sollte sie kennen, bevor man Pläne macht.

Drei Dinge, die im Alltag tatsächlich skalieren und die nichts mit Software zu
tun haben:

**Ein Preis, der an einer Bezugsgröße beim Kunden hängt.** Je Objekt, je
Mitarbeiter, je Messstelle. Der Umsatz wächst, wenn der Kunde wächst — ohne
Verhandlung und ohne Mehrarbeit.

**Ein Vertriebsweg, der viele Einheiten je Gespräch bringt.** Eine Verwaltung
mit zweihundert Objekten. Ein Portfolio mit vierzig Gebäuden. Eine Flotte mit
sechzig Fahrzeugen. **Das ist die häufigste Eigenschaft der dreizehn besten
Modelle dieses Buches.**

**Ein Bestand, der von allein wiederkommt.** Prüffristen, Abos,
Wartungsverträge, Zertifikatsupdates.

### Der Fehler, der am teuersten ist

Er heißt Automatisierung vor Produktisierung, und er kommt in diesem Buch
mehrfach vor: **Wer einen Ablauf automatisiert, der noch nicht festgelegt ist,
gießt seine Unordnung in Beton.**

Konkret: Du hast fünfzehn Kunden mit fünfzehn Sonderregelungen. Statt die
Sonderregelungen abzubauen, baust du ein System, das fünfzehn Sonderregelungen
kann. Es funktioniert, es kostet drei Monate, und es macht jede weitere
Vereinheitlichung unmöglich, weil sie nun auch das System betrifft.

**Die Reihenfolge ist: gleich machen, dann beschreiben, dann automatisieren,
dann eventuell entwickeln.** Wer eine Stufe überspringt, zahlt sie später
doppelt.

### Und der Fall, in dem alles davon nicht gilt

Es gibt in diesem Buch Modelle, bei denen Automatisierung keine Option ist,
sondern Bedingung: die Nachweismodelle ab einer bestimmten Objektzahl, die
Fristenmodelle, das Selfstorage ohne Personal, die Kühlkettenüberwachung. Dort
ist der Satz „erst wachsen, dann automatisieren" falsch — **dort ist die
Automatisierung das Produkt.**

Wie man den Unterschied erkennt: **Frag, ob die Automatisierung deine Arbeit
billiger macht oder dein Angebot erst möglich.** Im ersten Fall hat sie eine
Amortisationszeit und kann warten. Im zweiten Fall ist sie der Anfang.

> **Was du aus diesem Kapitel mitnimmst:** Bei jeder Software zwei Fragen.
> **Welchen Teil kaufe ich, welchen baue ich?** Und: **Was spart sie mir, wenn
> sie niemand kauft?** Wenn die zweite Antwort „ein paar Stunden" lautet, baue
> sie nicht.
