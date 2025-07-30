# GamesServer-System
Das hier ist das öfeentliche Repository zu dem GamesServer um alle wichtigen Informationen für Clients bereitzustellen. Die Infos werden von der Mod direkt von hier gedownloaded.

## AntiCheat - System
Das AntiCheat - System in der Mod implementiert sorgt dafür, dass es nicht mehr möglich ist, unerlaubte Mods o. Ä. zu nutzen. Dafür Werden Abfragen zu diesem Repository geschickt, um die erlaubten Dateien abzugleichen und unter Umständen ihren Stand auf den des Repositorys bringen. Alle Sachen die mit der AntiCheat zu tun haben finden sich im `./anticheat/`-Ordner.

### Modliste.json
Die Modliste.json ist eine Json Datei die Infos zur Abgleichung der aktuell erlaubten Mods für den Client enthält. 

_**Infos in der Modliste.json:**_

- Mods ("mods": [ {...} ]): 
	- <ins>Filename		("filename": String)</ins>\
  	Der genaue Filename, wie er im Ordner liegt
	- <ins>Filehash		("hash": String)</ins>\
	  Der SHA-256-Hash des gesamten Dateiinhalts
	- <ins>Optional - Attribut		("optional": Boolean)</ins>\
	  Ein Attribut, was angibt ob die Mod optional ist.
	- <ins>Admin-Only - Attribut		("admin_only": Boolean)</ins>\
	  Ein Attribut, was angibt ob die Mod nur von Admins verwendet werden darf.
	- <ins>Folden - Path ("folder": String)</ins>\
	  Der relative Path von dem Mods-Ordner zum File, um den Überblick besser zu behalten.

- Devs ("devs": [ Strings ]:\
	Die Usernames, die als Dev gelten sollen und somit die Admin-Only Mods nutzen dürfen.

### Modlist.py
Die Modlist.py ist ein File, der die Modlist.json mit Mods beschreibt. Dabei sind folgende Funktionen aktuell vorhanden:
- **Modfiles Suchen 📁:**\
  Hierbei wird der `./mods/` Ordner und alle Unterordner nach `.jar`- Dateien durchsucht.
- **Hashing #️⃣:**\
	Diese `.jar`-Dateien werden dann per SHA-256-Hashing vollständig ausgelsen und gehasht.
- **Prüfen auf Werte ✅:**\
  Im Anschluss wird der Filename nach Teilen durchsucht, der auf eine Optionalität oder Admin-Exklusivität hindeuten würde. 
- **Modliste updaten 📂:**\
  Für jeden Modfile wird ein eigenes Element unter `"mods": []` angelegt. Alle Werte werden wie [weiter oben](#Modliste.json) schon erklärt gespeichert.

### Verwendung
Um die Modlist.json zu schreiben oder zu aktuallisieren müssen alle Modfiles, die in der Liste ausfgeführt werden sollen, im `./mods`-Folder vorhanden sein. Wenn der Modlist.py-File ausgeführt wird, werden alle Funktionalitäten abgearbeitet und die Modliste vollständig umformatiert. 
> [!IMPORTANT]
> Beim Ausführen der Modlist.py werden alle Einträge unter `"mods"` gelöscht. Deshalb sollte man alle Modfiles, die in der Liste eingetragen sind, immer in dem Ordner `./mods` lassen, um an beiden Stellen immer Identische Ergebnisse zu haben, und nicht nur durch Ausführen des Codes alle Einträge zu löschen.

### Nutzen
Die Modliste soll beim Start des Client von diesem Repository gedownloaded werden und der Clint hasht die Modfiles, die in der aktuellen Instanz geladen sind. Im Anschluss werden diese Hashes mit denen aus der Modlist.json verglichen. Bei Unterschieden werden die Attribute geprüft. Sollte eine unerlaubte Mod auftreten, wird diese Mod entfernt, ein Logeintrag an Discord oder GitHub (Noch nicht genau klar) gesendet, eine Hinweis-Message angezeigt und nur noch die Option zum verlassen des Spiels gelassen. Sollten Mods fehlen werden die per GitHub-Pull gedownloaded.
