#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py - Form Assistant (mode invisible, Windows)

Aucune fenetre visible. Tourne en arriere-plan.
  Ctrl+B  -> capture invisible + analyse + affiche la reponse au centre
  Ctrl+H  -> cacher la reponse affichee
  Ctrl+C  -> quitter (dans le terminal)

Installation :
    pip install -r requirements.txt

Configuration :
    Cree un fichier .env a cote de ce script avec :
        ANTHROPIC_API_KEY=sk-ant-...

Usage :
    python app.py
"""

import tkinter as tk
import threading
import time
import io
import json
import base64
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

try:
    from PIL import ImageGrab
except ImportError:
    print("[ERREUR] pip install pillow")
    sys.exit(1)

try:
    from pynput import keyboard as pynput_kb
except ImportError:
    print("[ERREUR] pip install pynput")
    sys.exit(1)


# ============================================================
#  CONFIG
# ============================================================

API_URL    = "https://api.anthropic.com/v1/messages"
MODEL      = "claude-sonnet-4-5"
MAX_TOKENS = 512

DISPLAY_DURATION = 8.0   # secondes d'affichage de la reponse
FONT_SIZE        = 120   # taille du chiffre/lettre affiche


# ============================================================
#  CLE API
# ============================================================

def load_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    for candidate in [
        Path(__file__).parent / ".env",
        Path(__file__).parent.parent / ".env",
    ]:
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


# ============================================================
#  CLAUDE API
# ============================================================

def _img_to_b64(img) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def screenshot_b64() -> str:
    img = ImageGrab.grab()
    return _img_to_b64(img)


def ask_claude(img_b64: str, api_key: str) -> str:
    """
    Envoie le screenshot a Claude.
    Retourne UNIQUEMENT la lettre (A/B/C/D...) ou le numero (1/2/3/4...) de la bonne reponse.
    Si question ouverte, retourne la reponse courte.
    """
    prompt = (
        "Tu vois un screenshot d'UNE seule question (quiz, formulaire, examen).\n\n"
        "Identifie la bonne reponse et retourne UNIQUEMENT :\n"
        "  - La LETTRE de la bonne reponse (A, B, C, D...) si choix multiples avec lettres\n"
        "  - Le NUMERO de la bonne reponse (1, 2, 3, 4...) si choix multiples numerotes\n"
        "  - Le TEXTE EXACT de la bonne reponse (max 5 mots) sinon\n\n"
        "Pas d'explication. Pas de phrase. Juste la reponse.\n"
        "Exemple de retour valide : B\n"
        "Exemple de retour valide : 3\n"
        "Exemple de retour valide : Vrai"
    )

    body = json.dumps({
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64", "media_type": "image/png", "data": img_b64
                }},
                {"type": "text", "text": prompt}
            ]
        }]
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL, data=body, method="POST",
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            return data["content"][0]["text"].strip().strip(".").strip()
        except urllib.error.HTTPError as e:
            if e.code == 529 and attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            raise


# ============================================================
#  OVERLAY CENTRE (gros texte au milieu de l'ecran)
# ============================================================

class CenterDisplay:
    def __init__(self, root: tk.Tk):
        self._root = root
        self._win: Optional[tk.Toplevel] = None
        self._label: Optional[tk.Label] = None
        self._hide_job = None

    def _build(self):
        if self._win is not None:
            return
        sw = self._root.winfo_screenwidth()
        sh = self._root.winfo_screenheight()

        win = tk.Toplevel(self._root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.85)
        win.config(bg="black")

        # Taille adaptee a la lettre/numero (grosse box centree)
        w, h = 320, 220
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        label = tk.Label(
            win, text="", font=("Segoe UI", FONT_SIZE, "bold"),
            fg="#00FF88", bg="black"
        )
        label.pack(expand=True, fill="both")

        win.withdraw()
        self._win = win
        self._label = label

    def show(self, text: str):
        self._build()
        # Si reponse longue (texte), reduire la police
        if len(text) > 4:
            self._label.config(font=("Segoe UI", 36, "bold"))
        else:
            self._label.config(font=("Segoe UI", FONT_SIZE, "bold"))
        self._label.config(text=text)
        self._win.deiconify()
        self._win.lift()

        if self._hide_job:
            self._root.after_cancel(self._hide_job)
        self._hide_job = self._root.after(int(DISPLAY_DURATION * 1000), self.hide)

    def hide(self):
        if self._win:
            self._win.withdraw()
        self._hide_job = None


# ============================================================
#  HOTKEY LISTENER (Ctrl+B / Ctrl+H)
# ============================================================

VK_B = 0x42
VK_H = 0x48


class HotkeyListener:
    def __init__(self, on_capture, on_hide):
        self._on_capture = on_capture
        self._on_hide    = on_hide
        self._ctrl       = False
        self._listener: Optional[pynput_kb.Listener] = None
        self._last_b = 0.0
        self._last_h = 0.0

    def start(self):
        self._listener = pynput_kb.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self._listener.start()

    def stop(self):
        if self._listener:
            self._listener.stop()

    def _on_press(self, key):
        if key in (pynput_kb.Key.ctrl_l, pynput_kb.Key.ctrl_r):
            self._ctrl = True
            return
        if not self._ctrl:
            return

        vk   = getattr(key, 'vk',   None)
        char = getattr(key, 'char', None)

        is_b = (vk == VK_B) or (char == '\x02')
        is_h = (vk == VK_H) or (char == '\x08')

        now = time.time()
        if is_b and now - self._last_b > 1.0:
            self._last_b = now
            self._on_capture()
        if is_h and now - self._last_h > 0.5:
            self._last_h = now
            self._on_hide()

    def _on_release(self, key):
        if key in (pynput_kb.Key.ctrl_l, pynput_kb.Key.ctrl_r):
            self._ctrl = False


# ============================================================
#  PIPELINE
# ============================================================

class Assistant:
    def __init__(self, root: tk.Tk, display: CenterDisplay, api_key: str):
        self._root    = root
        self._display = display
        self._api_key = api_key
        self._running = False

    def trigger(self):
        if self._running:
            print("[Assistant] Analyse deja en cours...")
            return
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        self._running = True
        t0 = time.time()
        try:
            print("\n[Assistant] Capture invisible...")
            img_b64 = screenshot_b64()

            print("[Assistant] Envoi a Claude...")
            answer = ask_claude(img_b64, self._api_key)

            dt = time.time() - t0
            print(f"[Assistant] Reponse : {answer}  ({dt:.1f}s)")

            self._root.after(0, lambda: self._display.show(answer))

        except urllib.error.HTTPError as e:
            print(f"[ERREUR] API HTTP {e.code} : {e.read().decode('utf-8', errors='replace')[:200]}")
        except Exception as e:
            print(f"[ERREUR] {type(e).__name__}: {e}")
        finally:
            self._running = False


# ============================================================
#  MAIN
# ============================================================

def main():
    api_key = load_api_key()
    if not api_key:
        print("[ERREUR] Cle API introuvable. Cree un fichier .env avec :")
        print("    ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    print("=" * 55)
    print("  Form Assistant - actif en arriere-plan")
    print(f"  Cle API : ...{api_key[-8:]}")
    print()
    print("  Ctrl+B  -> Capturer l'ecran et obtenir la reponse")
    print("  Ctrl+H  -> Cacher la reponse")
    print("  Ctrl+C  -> Quitter (dans ce terminal)")
    print("=" * 55)
    print()
    print("  Zoome bien sur UNE seule question avant Ctrl+B.")
    print()

    root = tk.Tk()
    root.withdraw()

    display = CenterDisplay(root)
    assistant = Assistant(root, display, api_key)

    hotkeys = HotkeyListener(
        on_capture=assistant.trigger,
        on_hide=lambda: root.after(0, display.hide),
    )
    hotkeys.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        hotkeys.stop()
        print("\n[Assistant] Ferme.")


if __name__ == "__main__":
    main()
