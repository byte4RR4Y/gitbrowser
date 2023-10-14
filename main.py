import xbmcgui
import requests
import json
import git
import os

# Ihr persönlicher GitHub-Zugriffstoken
access_token = "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"

# Funktion zum Suchen von Kodi-Addons auf GitHub mit paginierter Abfrage
def search_github_addons():
    addon_list = []

    page = 1
    per_page = 100  # Anzahl der Addons pro Seite
    total_results = per_page

    while total_results == per_page:
        url = f"https://api.github.com/search/repositories?q=kodi+addon&page={page}&per_page={per_page}"
        headers = {"Authorization": f"token {access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            results = data.get("items", [])
            addon_list.extend(results)
            total_results = len(results)
            page += 1
        else:
            xbmcgui.Dialog().notification('Fehler', 'Fehler beim Abrufen der Daten von GitHub.', xbmcgui.NOTIFICATION_ERROR, 5000)
            break

    # Sortieren Sie die Addons alphabetisch nach dem Namen
    addon_list.sort(key=lambda addon: addon["name"])
    
    return addon_list

# Funktion zum Klonen eines Git-Repositorys in das Kodi-Addon-Verzeichnis
def clone_git_repository(url, addon_name):
    try:
        # Zielverzeichnis für das Addon (Verzeichnisname entspricht dem Repositorynamen)
        addon_dir = os.path.expanduser('~/.kodi/addons/') + addon_name

        # Überprüfen, ob das Verzeichnis bereits existiert, und es gegebenenfalls löschen
        if os.path.exists(addon_dir):
            xbmcgui.Dialog().notification('Hinweis', 'Addon-Verzeichnis existiert bereits. Lösche es.', xbmcgui.NOTIFICATION_INFO, 5000)
            os.rmdir(addon_dir)

        # Klonen des GitHub-Repositorys in das Addon-Verzeichnis
        git.Repo.clone_from(url, addon_dir)
        xbmcgui.Dialog().notification('Erfolg', 'Repository wurde geklont.', xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception as e:
        xbmcgui.Dialog().notification('Fehler', str(e), xbmcgui.NOTIFICATION_ERROR, 5000)

# Hauptfunktion zum Starten des Addons.
def run():
    addon_list = search_github_addons()
    
    if addon_list:
        addon_names = [addon["name"] for addon in addon_list]
        addon_names.sort()  # Sortieren Sie die Addon-Namen alphabetisch
        selected_items = xbmcgui.Dialog().multiselect('GitHub Kodi Addons', addon_names)

        if selected_items:
            selected_addons = [addon_list[index] for index in selected_items]
            for addon in selected_addons:
                clone_git_repository(addon["html_url"], addon["name"])

if __name__ == '__main__':
    run()
