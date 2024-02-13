###
Warum JSON:

Einfach und Lesbar:
JSON bietet eine einfache und leicht lesbare Struktur.

Leichte Implementierung:
Einfache Integration ohne zusätzlichen Overhead.

Geringer Overhead:
Wenig Ressourcenbedarf, ideal für Mikrocontroller wie ESP32.

Flexibel:
Anpassungsfähige Struktur für einfache Modifikationen.

Schnelles Prototyping:
Unkompliziertes Speichern und Laden für schnelle Entwicklungszyklen.


Vergleich mit SQLite und LittleFS:

SQLite:
Höherer Ressourcenbedarf und Komplexität.
Bietet leistungsstarke SQL-Abfragen und Transaktionen für komplexe Anwendungen.

LittleFS:
Effizientes Dateisystem, jedoch weniger Query-Funktionen.
Optimiert für Flash-Speicher, geeignet für einfache Dateispeicherung.
###
mfrc522 library von -> 
###
Zur leichten Eingabe zwecks Kontrolle, ob der Webserver auch das richtige Passwort akzeptiert.
Funktioniert:           weiße Karte : "uid: 0xa4d6b15b"
Funktioniert nicht:     blauer Chip : "uid: 0x79307de2"
###
Nur die id des physischen rfid-Objekts wird gespeichert, nicht die falschen Eingaben beim Webserver, da es zu viele Eingabemöglichkeiten gibt.
###
