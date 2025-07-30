import os
import json
import hashlib

def calculate_file_hash(filepath):
    """Berechnet den SHA-256 Hash einer Datei"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Datei in Blöcken lesen für bessere Performance bei großen Dateien
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def is_optional(filename):
    """Prüft ob die Datei optional ist (enthält [O])"""
    return "[O]" in filename

def is_admin_only(filename):
    """Prüft ob die Datei nur für Admins ist (enthält [A])"""
    return "[A]" in filename

def scan_mods_folder():
    """Scannt den mods Ordner rekursiv und erstellt Mod-Einträge"""
    # Pfad relativ zum Script-Standort
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mods_folder = os.path.join(script_dir, "mods")
    mod_entries = []
    
    if not os.path.exists(mods_folder):
        print(f"Warnung: Ordner '{mods_folder}' existiert nicht.")
        return mod_entries
    
    # Rekursiv alle Dateien im mods Ordner und Unterordnern durchgehen
    for root, dirs, files in os.walk(mods_folder):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Relativen Pfad vom mods Ordner aus berechnen
            relative_path = os.path.relpath(root, mods_folder)
            
            # Wenn wir im Root-mods Ordner sind, ist der relative Pfad "."
            # In diesem Fall setzen wir folder auf leer
            if relative_path == ".":
                folder_path = ""
            else:
                # Backslashes durch Forward-Slashes ersetzen für konsistente Pfade
                folder_path = relative_path.replace("\\", "/")
            
            try:
                # Hash der Datei berechnen
                file_hash = calculate_file_hash(filepath)
                
                # Mod-Eintrag erstellen
                mod_entry = {
                    "filename": filename,
                    "hash": file_hash,
                    "optional": is_optional(filename),
                    "admin_only": is_admin_only(filename),
                    "folder": folder_path
                }
                
                mod_entries.append(mod_entry)
                if folder_path:
                    print(f"Mod hinzugefügt: {folder_path}/{filename}")
                else:
                    print(f"Mod hinzugefügt: {filename}")
                
            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei {filepath}: {e}")
    
    return mod_entries

def update_modlist():
    """Aktualisiert die modlist.json mit den gescannten Mods"""
    # Pfad relativ zum Script-Standort
    script_dir = os.path.dirname(os.path.abspath(__file__))
    modlist_file = os.path.join(script_dir, "modlist.json")
    
    # Bestehende modlist.json laden
    try:
        with open(modlist_file, 'r', encoding='utf-8') as f:
            modlist_data = json.load(f)
    except FileNotFoundError:
        print(f"Warnung: {modlist_file} nicht gefunden. Erstelle neue Datei.")
        modlist_data = {"mods": [], "devs": []}
    except json.JSONDecodeError as e:
        print(f"Fehler beim Lesen der JSON-Datei: {e}")
        return
    
    # Alle bestehenden Mod-Einträge löschen
    modlist_data["mods"] = []
    
    # Neue Mod-Einträge hinzufügen
    new_mods = scan_mods_folder()
    modlist_data["mods"] = new_mods
    
    # Aktualisierte modlist.json speichern
    try:
        with open(modlist_file, 'w', encoding='utf-8') as f:
            json.dump(modlist_data, f, indent=4, ensure_ascii=False)
        
        print(f"\nModlist erfolgreich aktualisiert!")
        print(f"Anzahl der Mods: {len(new_mods)}")
        
    except Exception as e:
        print(f"Fehler beim Speichern der modlist.json: {e}")

if __name__ == "__main__":
    print("Scanne mods Ordner und aktualisiere modlist.json...")
    update_modlist()