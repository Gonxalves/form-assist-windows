**Objet :** Petite app pour t'aider — install en 5 min

Salut !

Je t'ai prepare une petite app qui tourne en arriere-plan sur ton PC. Tu appuies sur **Ctrl+B**, elle prend une photo invisible de ton ecran, l'envoie a Claude (l'IA), et la bonne reponse apparait au milieu de ton ecran pendant 8 secondes. Personne ne voit rien d'autre.

Suis les etapes une par une. Si tu bloques quelque part, screenshot et envoie-moi.

---

## ETAPE 1 — Installer Python (5 min)

1. Va sur : https://www.python.org/downloads/windows/
2. Clique sur le gros bouton jaune **"Download Python 3.12.x"** (ou plus recent).
3. Ouvre le fichier qui se telecharge.
4. **TRES IMPORTANT** : tout en bas de la fenetre d'install, coche la case **"Add python.exe to PATH"**. Sans ca, rien ne marchera.
5. Clique sur **"Install Now"** et attends que ce soit fini.
6. Clique **"Close"**.

---

## ETAPE 2 — Ouvrir le terminal (PowerShell)

1. Appuie sur la touche **Windows** de ton clavier.
2. Tape : `powershell`
3. Appuie sur **Entree**. Une fenetre bleue/noire s'ouvre. C'est le terminal.

Tu vas taper des commandes la-dedans. Tu copies/colles (clic droit pour coller dans PowerShell) puis tu appuies sur Entree.

---

## ETAPE 3 — Verifier que Python marche

Dans le terminal, tape :

```
python --version
```

Tu dois voir quelque chose comme `Python 3.12.5`. Si tu vois ca, parfait.

Si tu vois "n'est pas reconnu" ou rien : c'est que tu as oublie de cocher "Add to PATH" a l'etape 1. Reinstalle Python en cochant la case.

---

## ETAPE 4 — Telecharger l'app

Dans le terminal, copie-colle ces 2 commandes une par une :

```
cd Desktop
```

```
git clone https://github.com/Gonxalves/form-assist-windows.git
```

Si `git` n'est pas installe, telecharge-le ici : https://git-scm.com/download/win (clique-clique-clique, install par defaut), puis ferme le terminal, rouvre PowerShell, et refais les 2 commandes.

Ensuite :

```
cd form-assist-windows
```

---

## ETAPE 5 — Installer les dependances

Toujours dans le terminal (tu dois etre dans le dossier `form-assist-windows`) :

```
pip install -r requirements.txt
```

Attends que ca finisse (1-2 min). C'est normal qu'il y ait plein de texte qui defile.

---

## ETAPE 6 — Mettre la cle API

Je t'envoie la cle API par message prive (ne la mets jamais sur internet). Elle commence par `sk-ant-...`.

Dans le terminal, tape :

```
notepad .env
```

Notepad va te demander si tu veux creer le fichier. Reponds **Oui**.

Dans la fenetre Notepad qui s'ouvre, ecris cette ligne (remplace par la vraie cle que je t'envoie) :

```
ANTHROPIC_API_KEY=sk-ant-colle-ta-cle-ici
```

Sauvegarde (Ctrl+S) et ferme Notepad.

---

## ETAPE 7 — Lancer l'app

Dans le terminal :

```
python app.py
```

Tu dois voir :

```
=======================================================
  Form Assistant - actif en arriere-plan
  Ctrl+B  -> Capturer l'ecran et obtenir la reponse
  Ctrl+H  -> Cacher la reponse
  Ctrl+C  -> Quitter
=======================================================
```

**LAISSE CE TERMINAL OUVERT.** L'app tourne tant que ce terminal reste ouvert.

---

## ETAPE 8 — Utiliser l'app

1. Ouvre ton quiz / formulaire / examen dans ton navigateur.
2. **Zoome bien sur UNE seule question** (maintiens Ctrl et tourne la molette de ta souris).
3. Appuie sur **Ctrl+B**.
4. Attends 3 secondes.
5. La bonne reponse apparait en gros au centre de ton ecran (lettre A/B/C/D, chiffre, ou texte court).
6. Elle disparait toute seule apres 8 secondes. Tu peux aussi appuyer sur **Ctrl+H** pour la cacher tout de suite.

C'est tout.

---

## Pour relancer plus tard

Tu n'as PAS besoin de refaire toutes les etapes. Juste :

1. Ouvre PowerShell (touche Windows -> tape `powershell` -> Entree).
2. Tape :
   ```
   cd Desktop\form-assist-windows
   python app.py
   ```
3. Done.

---

## Si ca plante

Screenshot le message d'erreur du terminal et envoie-le moi. Je regarde.

Bisous,
Raph
