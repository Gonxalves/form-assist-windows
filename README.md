# Form Assistant (Windows)

App invisible qui tourne en arriere-plan. Quand tu appuies sur **Ctrl+B**, elle prend un screenshot de ton ecran, l'envoie a Claude, et affiche la bonne reponse au centre de l'ecran.

## Raccourcis

| Touche | Action |
|--------|--------|
| `Ctrl+B` | Capturer l'ecran + obtenir la reponse |
| `Ctrl+X` | Cacher la reponse affichee |
| `Ctrl+C` | Quitter (dans le terminal) |

## Installation rapide

1. Installer Python 3.10+ depuis https://www.python.org/downloads/windows/
   - **Important** : cocher "Add Python to PATH" pendant l'install.

2. Cloner ce repo :
   ```
   git clone https://github.com/Gonxalves/form-assist-windows.git
   cd form-assist-windows
   ```

3. Installer les dependances :
   ```
   pip install -r requirements.txt
   ```

4. Creer un fichier `.env` a cote de `app.py` avec ta cle API Anthropic :
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

5. Lancer :
   ```
   python app.py
   ```

## Utilisation

1. Lance `python app.py` dans un terminal et laisse-le tourner.
2. Ouvre ton quiz / formulaire / examen dans le navigateur.
3. Zoome bien sur **UNE seule question** (Ctrl+molette).
4. Appuie sur **Ctrl+B**.
5. Apres ~3 secondes, la reponse s'affiche au centre de l'ecran.
6. `Ctrl+X` pour la cacher immediatement.
