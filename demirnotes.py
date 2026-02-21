#!/usr/bin/env python3
"""
DemirNotes — Encrypted Note-Taking Application
Multi-language (TR/EN/RU), AES encrypted, with drawing, attachments, and more.
MIT License (c) 2026 Demir
"""

import customtkinter as ctk
import os
import sys
import json
import uuid
import hashlib
import base64
import shutil
import io
import re
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tkinter import messagebox, filedialog, colorchooser
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# ══════════════════════════════════════════════════
# Translations
# ══════════════════════════════════════════════════
TRANSLATIONS = {
    "tr": {
        "app_title": "DemirNotes",
        "welcome": "Güvenli not uygulamanıza hoş geldiniz",
        "create_password": "Ana Şifre Oluşturun",
        "password_protect": "Bu şifre tüm notlarınızı koruyacaktır",
        "password": "Şifre",
        "password_again": "Şifreyi tekrar girin",
        "create_btn": "Şifre Oluştur",
        "login": "Giriş Yapın",
        "login_subtitle": "Notlarınıza erişmek için şifrenizi girin",
        "your_password": "Şifreniz",
        "login_btn": "Giriş",
        "wrong_password": "Yanlış şifre!",
        "pw_min_4": "Şifre en az 4 karakter olmalı",
        "pw_no_match": "Şifreler eşleşmiyor",
        "new_note": "＋ Yeni Not",
        "hidden": "👁 Gizli",
        "normal": "📋 Normal",
        "search": "Not ara...",
        "no_hidden": "Gizli not yok",
        "no_notes": "Henüz not yok",
        "no_results": "Sonuç bulunamadı",
        "untitled": "Başlıksız Not",
        "note_title_ph": "Not başlığı...",
        "hide": "🔒 Gizle",
        "show": "🔓 Göster",
        "delete": "🗑 Sil",
        "delete_confirm": "silinsin mi?",
        "chars": "karakter",
        "words": "kelime",
        "hidden_note": "🔒 Gizli not",
        "settings": "⚙  Ayarlar",
        "change_password": "Şifre Değiştir",
        "current_pw": "Mevcut şifre",
        "new_pw": "Yeni şifre",
        "new_pw_again": "Yeni şifre (tekrar)",
        "change_pw_btn": "Şifreyi Değiştir",
        "wrong_current_pw": "Mevcut şifre yanlış!",
        "pw_changed": "Şifre değiştirildi!",
        "success": "Başarılı",
        "select_note": "Bir not seçin veya yeni not oluşturun",
        "add_image": "🖼 Resim Ekle",
        "add_pdf": "📄 PDF Ekle",
        "whiteboard": "🎨 Çizim Tahtası",
        "export_pdf": "📤 PDF Dışa Aktar",
        "find_in_note": "🔍 Notta Ara",
        "find_placeholder": "Aranacak metin...",
        "find_next": "Sonraki",
        "find_prev": "Önceki",
        "close": "Kapat",
        "attachments": "Ekler",
        "no_attachments": "Ek yok",
        "open_file": "Aç",
        "remove": "Kaldır",
        "drawing_board": "Çizim Tahtası",
        "pen": "✏ Kalem",
        "eraser": "◻ Silgi",
        "color": "🎨 Renk",
        "thickness": "Kalınlık",
        "clear_canvas": "🗑 Temizle",
        "save_drawing": "💾 Kaydet",
        "cancel": "İptal",
        "language": "Dil",
        "lang_tr": "🇹🇷 Türkçe",
        "lang_en": "🇬🇧 English",
        "lang_ru": "🇷🇺 Русский",
        "undo": "↩ Geri Al",
        "redo": "↪ Yinele",
        "image_files": "Resim Dosyaları",
        "pdf_files": "PDF Dosyaları",
        "export_success": "Not PDF olarak dışa aktarıldı!",
        "error": "Hata",
        "confirm": "Onay",
        "new_note_title": "Yeni Not",
        "bold": "B",
        "italic": "I",
        "underline": "U",
        "categories": "Kategoriler",
        "all_notes": "Tüm Notlar",
        "add_category": "＋ Kategori Ekle",
        "category_name": "Kategori adı",
        "save_to_drawing": "Çizimi Nota Ekle",
    },
    "en": {
        "app_title": "DemirNotes",
        "welcome": "Welcome to your secure notes app",
        "create_password": "Create Master Password",
        "password_protect": "This password will protect all your notes",
        "password": "Password",
        "password_again": "Confirm password",
        "create_btn": "Create Password",
        "login": "Sign In",
        "login_subtitle": "Enter your password to access your notes",
        "your_password": "Your password",
        "login_btn": "Sign In",
        "wrong_password": "Wrong password!",
        "pw_min_4": "Password must be at least 4 characters",
        "pw_no_match": "Passwords don't match",
        "new_note": "＋ New Note",
        "hidden": "👁 Hidden",
        "normal": "📋 Normal",
        "search": "Search notes...",
        "no_hidden": "No hidden notes",
        "no_notes": "No notes yet",
        "no_results": "No results found",
        "untitled": "Untitled Note",
        "note_title_ph": "Note title...",
        "hide": "🔒 Hide",
        "show": "🔓 Show",
        "delete": "🗑 Delete",
        "delete_confirm": "will be deleted?",
        "chars": "characters",
        "words": "words",
        "hidden_note": "🔒 Hidden note",
        "settings": "⚙  Settings",
        "change_password": "Change Password",
        "current_pw": "Current password",
        "new_pw": "New password",
        "new_pw_again": "New password (again)",
        "change_pw_btn": "Change Password",
        "wrong_current_pw": "Current password is wrong!",
        "pw_changed": "Password changed!",
        "success": "Success",
        "select_note": "Select a note or create a new one",
        "add_image": "🖼 Add Image",
        "add_pdf": "📄 Add PDF",
        "whiteboard": "🎨 Whiteboard",
        "export_pdf": "📤 Export PDF",
        "find_in_note": "🔍 Find in Note",
        "find_placeholder": "Search text...",
        "find_next": "Next",
        "find_prev": "Previous",
        "close": "Close",
        "attachments": "Attachments",
        "no_attachments": "No attachments",
        "open_file": "Open",
        "remove": "Remove",
        "drawing_board": "Drawing Board",
        "pen": "✏ Pen",
        "eraser": "◻ Eraser",
        "color": "🎨 Color",
        "thickness": "Thickness",
        "clear_canvas": "🗑 Clear",
        "save_drawing": "💾 Save",
        "cancel": "Cancel",
        "language": "Language",
        "lang_tr": "🇹🇷 Türkçe",
        "lang_en": "🇬🇧 English",
        "lang_ru": "🇷🇺 Русский",
        "undo": "↩ Undo",
        "redo": "↪ Redo",
        "image_files": "Image Files",
        "pdf_files": "PDF Files",
        "export_success": "Note exported as PDF!",
        "error": "Error",
        "confirm": "Confirm",
        "new_note_title": "New Note",
        "bold": "B",
        "italic": "I",
        "underline": "U",
        "categories": "Categories",
        "all_notes": "All Notes",
        "add_category": "＋ Add Category",
        "category_name": "Category name",
        "save_to_drawing": "Add Drawing to Note",
    },
    "ru": {
        "app_title": "DemirNotes",
        "welcome": "Добро пожаловать в защищённое приложение заметок",
        "create_password": "Создайте мастер-пароль",
        "password_protect": "Этот пароль защитит все ваши заметки",
        "password": "Пароль",
        "password_again": "Подтвердите пароль",
        "create_btn": "Создать пароль",
        "login": "Вход",
        "login_subtitle": "Введите пароль для доступа к заметкам",
        "your_password": "Ваш пароль",
        "login_btn": "Войти",
        "wrong_password": "Неверный пароль!",
        "pw_min_4": "Пароль должен быть не менее 4 символов",
        "pw_no_match": "Пароли не совпадают",
        "new_note": "＋ Новая заметка",
        "hidden": "👁 Скрытые",
        "normal": "📋 Обычные",
        "search": "Поиск заметок...",
        "no_hidden": "Нет скрытых заметок",
        "no_notes": "Заметок пока нет",
        "no_results": "Ничего не найдено",
        "untitled": "Без названия",
        "note_title_ph": "Название заметки...",
        "hide": "🔒 Скрыть",
        "show": "🔓 Показать",
        "delete": "🗑 Удалить",
        "delete_confirm": "будет удалена?",
        "chars": "символов",
        "words": "слов",
        "hidden_note": "🔒 Скрытая заметка",
        "settings": "⚙  Настройки",
        "change_password": "Изменить пароль",
        "current_pw": "Текущий пароль",
        "new_pw": "Новый пароль",
        "new_pw_again": "Новый пароль (повтор)",
        "change_pw_btn": "Изменить пароль",
        "wrong_current_pw": "Текущий пароль неверен!",
        "pw_changed": "Пароль изменён!",
        "success": "Успешно",
        "select_note": "Выберите заметку или создайте новую",
        "add_image": "🖼 Добавить изображение",
        "add_pdf": "📄 Добавить PDF",
        "whiteboard": "🎨 Доска для рисования",
        "export_pdf": "📤 Экспорт PDF",
        "find_in_note": "🔍 Найти в заметке",
        "find_placeholder": "Искать текст...",
        "find_next": "Далее",
        "find_prev": "Назад",
        "close": "Закрыть",
        "attachments": "Вложения",
        "no_attachments": "Нет вложений",
        "open_file": "Открыть",
        "remove": "Удалить",
        "drawing_board": "Доска для рисования",
        "pen": "✏ Карандаш",
        "eraser": "◻ Ластик",
        "color": "🎨 Цвет",
        "thickness": "Толщина",
        "clear_canvas": "🗑 Очистить",
        "save_drawing": "💾 Сохранить",
        "cancel": "Отмена",
        "language": "Язык",
        "lang_tr": "🇹🇷 Türkçe",
        "lang_en": "🇬🇧 English",
        "lang_ru": "🇷🇺 Русский",
        "undo": "↩ Отменить",
        "redo": "↪ Повторить",
        "image_files": "Файлы изображений",
        "pdf_files": "Файлы PDF",
        "export_success": "Заметка экспортирована в PDF!",
        "error": "Ошибка",
        "confirm": "Подтверждение",
        "new_note_title": "Новая заметка",
        "bold": "Ж",
        "italic": "К",
        "underline": "Ч",
        "categories": "Категории",
        "all_notes": "Все заметки",
        "add_category": "＋ Добавить категорию",
        "category_name": "Имя категории",
        "save_to_drawing": "Добавить рисунок в заметку",
    },
}

# ══════════════════════════════════════════════════
# Theme colors
# ══════════════════════════════════════════════════
COLORS = {
    "bg_dark": "#0f0f1a", "bg_sidebar": "#161625", "bg_card": "#1c1c30",
    "bg_input": "#232340", "bg_hover": "#2a2a4a", "accent": "#6c5ce7",
    "accent_hover": "#7f70f0", "accent_light": "#a29bfe", "danger": "#e74c3c",
    "danger_hover": "#ff6b6b", "warning": "#f39c12", "success": "#00b894",
    "text_primary": "#e8e8f0", "text_secondary": "#8888aa",
    "text_muted": "#555577", "border": "#2a2a45", "hidden_accent": "#fd79a8",
    "hidden_accent_hover": "#ff9fbd", "search_bg": "#1e1e35",
    "canvas_bg": "#1a1a2e", "toolbar_bg": "#12121f",
}

COLOR_TAGS = {
    "default": "#6c5ce7", "red": "#e74c3c", "orange": "#e67e22",
    "yellow": "#f1c40f", "green": "#00b894", "blue": "#0984e3",
    "purple": "#a29bfe", "pink": "#fd79a8",
}


# ══════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════
def get_data_dir():
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(base, "demirnotes")
    os.makedirs(d, exist_ok=True)
    os.makedirs(os.path.join(d, "notes"), exist_ok=True)
    os.makedirs(os.path.join(d, "attachments"), exist_ok=True)
    return d


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480_000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def encrypt_data(data: str, key: bytes) -> bytes:
    return Fernet(key).encrypt(data.encode("utf-8"))


def decrypt_data(token: bytes, key: bytes) -> str:
    return Fernet(key).decrypt(token).decode("utf-8")


def encrypt_bytes(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)


def decrypt_bytes(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


# ══════════════════════════════════════════════════
# Note Model
# ══════════════════════════════════════════════════
class Note:
    def __init__(self, note_id=None, title="", content="", hidden=False,
                 color_tag="default", created=None, modified=None,
                 category="", attachments=None, drawing_data=None):
        self.note_id = note_id or str(uuid.uuid4())[:8]
        self.title = title
        self.content = content
        self.hidden = hidden
        self.color_tag = color_tag
        self.created = created or datetime.now().isoformat()
        self.modified = modified or datetime.now().isoformat()
        self.category = category
        self.attachments = attachments or []
        self.drawing_data = drawing_data or []

    def to_meta(self):
        return {
            "id": self.note_id, "title": self.title, "hidden": self.hidden,
            "color_tag": self.color_tag, "created": self.created,
            "modified": self.modified, "category": self.category,
            "attachments": self.attachments, "drawing_data": self.drawing_data,
        }

    @staticmethod
    def from_meta(meta):
        return Note(
            note_id=meta["id"], title=meta.get("title", ""),
            hidden=meta.get("hidden", False), color_tag=meta.get("color_tag", "default"),
            created=meta.get("created"), modified=meta.get("modified"),
            category=meta.get("category", ""),
            attachments=meta.get("attachments", []),
            drawing_data=meta.get("drawing_data", []),
        )


# ══════════════════════════════════════════════════
# Note Manager
# ══════════════════════════════════════════════════
class NoteManager:
    def __init__(self, data_dir: str, key: bytes):
        self.data_dir = data_dir
        self.notes_dir = os.path.join(data_dir, "notes")
        self.attach_dir = os.path.join(data_dir, "attachments")
        self.key = key
        os.makedirs(self.notes_dir, exist_ok=True)
        os.makedirs(self.attach_dir, exist_ok=True)

    def _enc_path(self, nid): return os.path.join(self.notes_dir, f"{nid}.enc")
    def _meta_path(self, nid): return os.path.join(self.notes_dir, f"{nid}.meta")

    def save(self, note: Note):
        note.modified = datetime.now().isoformat()
        enc = encrypt_data(note.content, self.key)
        with open(self._enc_path(note.note_id), "wb") as f:
            f.write(enc)
        meta_json = json.dumps(note.to_meta(), ensure_ascii=False)
        enc_meta = encrypt_data(meta_json, self.key)
        with open(self._meta_path(note.note_id), "wb") as f:
            f.write(enc_meta)

    def load_content(self, nid: str) -> str:
        path = self._enc_path(nid)
        if not os.path.exists(path):
            return ""
        with open(path, "rb") as f:
            return decrypt_data(f.read(), self.key)

    def load_all_meta(self) -> list:
        notes = []
        for fname in os.listdir(self.notes_dir):
            if fname.endswith(".meta"):
                with open(os.path.join(self.notes_dir, fname), "rb") as f:
                    try:
                        meta_json = decrypt_data(f.read(), self.key)
                        notes.append(Note.from_meta(json.loads(meta_json)))
                    except Exception:
                        pass
        notes.sort(key=lambda n: n.modified, reverse=True)
        return notes

    def delete(self, nid: str):
        for p in (self._enc_path(nid), self._meta_path(nid)):
            if os.path.exists(p):
                os.remove(p)
        # Remove attachments
        for f in os.listdir(self.attach_dir):
            if f.startswith(nid + "_"):
                os.remove(os.path.join(self.attach_dir, f))

    def save_attachment(self, nid: str, filename: str, data: bytes) -> str:
        safe = re.sub(r'[^\w\-.]', '_', filename)
        enc = encrypt_bytes(data, self.key)
        path = os.path.join(self.attach_dir, f"{nid}_{safe}.enc")
        with open(path, "wb") as f:
            f.write(enc)
        return f"{nid}_{safe}"

    def load_attachment(self, att_id: str) -> bytes:
        path = os.path.join(self.attach_dir, f"{att_id}.enc")
        if not os.path.exists(path):
            return b""
        with open(path, "rb") as f:
            return decrypt_bytes(f.read(), self.key)

    def remove_attachment(self, att_id: str):
        path = os.path.join(self.attach_dir, f"{att_id}.enc")
        if os.path.exists(path):
            os.remove(path)

    def get_categories(self) -> list:
        cats = set()
        for n in self.load_all_meta():
            if n.category:
                cats.add(n.category)
        return sorted(cats)


# ══════════════════════════════════════════════════
# Whiteboard Dialog
# ══════════════════════════════════════════════════
class WhiteboardDialog(ctk.CTkToplevel):
    def __init__(self, parent, lang, existing_strokes=None, callback=None):
        super().__init__(parent)
        self.title(TRANSLATIONS[lang]["drawing_board"])
        self.geometry("900x650")
        self.configure(fg_color=COLORS["bg_dark"])
        self.transient(parent)
        self.grab_set()
        self.T = TRANSLATIONS[lang]
        self.callback = callback
        self.pen_color = "#ffffff"
        self.pen_size = 3
        self.tool = "pen"
        self.strokes = existing_strokes or []
        self.current_stroke = []
        self.undo_stack = list(self.strokes)
        self.redo_stack = []

        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color=COLORS["toolbar_bg"], height=50, corner_radius=0)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        self._pen_btn = ctk.CTkButton(toolbar, text=self.T["pen"], width=90, height=36,
            corner_radius=8, fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            font=ctk.CTkFont(size=13, weight="bold"), command=lambda: self._set_tool("pen"))
        self._pen_btn.pack(side="left", padx=(12, 4), pady=7)

        self._eraser_btn = ctk.CTkButton(toolbar, text=self.T["eraser"], width=90, height=36,
            corner_radius=8, fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            font=ctk.CTkFont(size=13), command=lambda: self._set_tool("eraser"))
        self._eraser_btn.pack(side="left", padx=4, pady=7)

        ctk.CTkButton(toolbar, text=self.T["color"], width=90, height=36,
            corner_radius=8, fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            font=ctk.CTkFont(size=13), command=self._pick_color).pack(side="left", padx=4, pady=7)

        self._color_preview = ctk.CTkFrame(toolbar, fg_color=self.pen_color, width=28, height=28, corner_radius=14)
        self._color_preview.pack(side="left", padx=(4, 8), pady=11)

        ctk.CTkLabel(toolbar, text=self.T["thickness"], font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]).pack(side="left", padx=(8, 4))
        self._size_slider = ctk.CTkSlider(toolbar, from_=1, to=20, number_of_steps=19,
            width=120, height=18, fg_color=COLORS["bg_input"], progress_color=COLORS["accent"],
            button_color=COLORS["accent_light"], command=self._on_size_change)
        self._size_slider.set(self.pen_size)
        self._size_slider.pack(side="left", padx=4, pady=7)

        ctk.CTkButton(toolbar, text=self.T["clear_canvas"], width=90, height=36,
            corner_radius=8, fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"],
            font=ctk.CTkFont(size=13), command=self._clear_canvas).pack(side="right", padx=(4, 12), pady=7)

        ctk.CTkButton(toolbar, text=self.T["save_drawing"], width=100, height=36,
            corner_radius=8, fg_color=COLORS["success"], hover_color="#00d9a7",
            font=ctk.CTkFont(size=13, weight="bold"), command=self._save).pack(side="right", padx=4, pady=7)

        ctk.CTkButton(toolbar, text=self.T["cancel"], width=70, height=36,
            corner_radius=8, fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            font=ctk.CTkFont(size=13), command=self.destroy).pack(side="right", padx=4, pady=7)

        # Canvas
        self.canvas = tk.Canvas(self, bg=COLORS["canvas_bg"], highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<B1-Motion>", self._on_draw)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        # Redraw existing strokes
        self._redraw_all()

    def _set_tool(self, tool):
        self.tool = tool
        if tool == "pen":
            self._pen_btn.configure(fg_color=COLORS["accent"])
            self._eraser_btn.configure(fg_color=COLORS["bg_card"])
            self.canvas.configure(cursor="crosshair")
        else:
            self._pen_btn.configure(fg_color=COLORS["bg_card"])
            self._eraser_btn.configure(fg_color=COLORS["accent"])
            self.canvas.configure(cursor="circle")

    def _pick_color(self):
        c = colorchooser.askcolor(initialcolor=self.pen_color, title="Color")
        if c and c[1]:
            self.pen_color = c[1]
            self._color_preview.configure(fg_color=self.pen_color)

    def _on_size_change(self, val):
        self.pen_size = int(val)

    def _on_press(self, event):
        color = COLORS["canvas_bg"] if self.tool == "eraser" else self.pen_color
        size = self.pen_size * 3 if self.tool == "eraser" else self.pen_size
        self.current_stroke = {"color": color, "size": size, "points": [(event.x, event.y)]}

    def _on_draw(self, event):
        if not self.current_stroke:
            return
        pts = self.current_stroke["points"]
        if len(pts) > 0:
            x0, y0 = pts[-1]
            self.canvas.create_line(x0, y0, event.x, event.y,
                fill=self.current_stroke["color"], width=self.current_stroke["size"],
                capstyle=tk.ROUND, joinstyle=tk.ROUND, smooth=True)
        pts.append((event.x, event.y))

    def _on_release(self, event):
        if self.current_stroke and len(self.current_stroke["points"]) > 1:
            self.strokes.append(self.current_stroke)
            self.redo_stack.clear()
        self.current_stroke = []

    def _clear_canvas(self):
        self.strokes.clear()
        self.canvas.delete("all")

    def _redraw_all(self):
        self.canvas.delete("all")
        for stroke in self.strokes:
            pts = stroke["points"]
            for i in range(1, len(pts)):
                self.canvas.create_line(pts[i-1][0], pts[i-1][1], pts[i][0], pts[i][1],
                    fill=stroke["color"], width=stroke["size"],
                    capstyle=tk.ROUND, joinstyle=tk.ROUND, smooth=True)

    def _save(self):
        if self.callback:
            self.callback(self.strokes)
        self.destroy()


# ══════════════════════════════════════════════════
# Main Application
# ══════════════════════════════════════════════════
class DemirNotesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.data_dir = get_data_dir()
        self.config_path = os.path.join(self.data_dir, "config.dat")
        self.key = None
        self.manager = None
        self.notes = []
        self.current_note = None
        self.show_hidden = False
        self.search_query = ""
        self.lang = "tr"
        self.T = TRANSLATIONS[self.lang]
        self.find_matches = []
        self.find_index = -1
        self.selected_category = ""
        self._undo_stack = []
        self._redo_stack = []
        self._image_refs = []

        self.title("DemirNotes")
        self.geometry("1200x750")
        self.minsize(950, 600)
        self.configure(fg_color=COLORS["bg_dark"])
        self._find_icon()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Load language from config if exists
        self._load_lang_pref()

        if os.path.exists(self.config_path):
            self._build_login_screen()
        else:
            self._build_setup_screen()

    def _find_icon(self):
        candidates = [
            os.path.join(os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)), "Demnote.ico"),
            os.path.join(os.path.expanduser("~"), "Downloads", "Demnote.ico"),
        ]
        for c in candidates:
            if os.path.exists(c):
                try:
                    self.iconbitmap(c)
                except Exception:
                    pass
                return

    def _load_lang_pref(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    cfg = json.load(f)
                    self.lang = cfg.get("lang", "tr")
                    self.T = TRANSLATIONS[self.lang]
        except Exception:
            pass

    def _save_lang_pref(self):
        try:
            cfg = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    cfg = json.load(f)
            cfg["lang"] = self.lang
            with open(self.config_path, "w") as f:
                json.dump(cfg, f)
        except Exception:
            pass

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ═══════════════════════════════════════
    # Setup Screen
    # ═══════════════════════════════════════
    def _build_setup_screen(self):
        self._clear()
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Language selector at top right
        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)
        for lcode, lname in [("tr", "🇹🇷"), ("en", "🇬🇧"), ("ru", "🇷🇺")]:
            ctk.CTkButton(lang_frame, text=lname, width=40, height=32,
                corner_radius=8, fg_color=COLORS["accent"] if self.lang == lcode else COLORS["bg_card"],
                hover_color=COLORS["accent_hover"],
                command=lambda lc=lcode: self._change_lang_setup(lc)
            ).pack(side="left", padx=2)

        ctk.CTkLabel(frame, text="🔐  DemirNotes", font=ctk.CTkFont(size=36, weight="bold"),
            text_color=COLORS["accent_light"]).pack(pady=(0, 5))
        ctk.CTkLabel(frame, text=self.T["welcome"], font=ctk.CTkFont(size=14),
            text_color=COLORS["text_secondary"]).pack(pady=(0, 30))

        card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=16, width=420)
        card.pack(padx=20, pady=10)
        card.pack_propagate(False)
        card.configure(height=330, width=420)

        ctk.CTkLabel(card, text=self.T["create_password"], font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"]).pack(pady=(25, 5))
        ctk.CTkLabel(card, text=self.T["password_protect"], font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]).pack(pady=(0, 20))

        self._setup_pw1 = ctk.CTkEntry(card, placeholder_text=self.T["password"], show="●",
            width=320, height=42, corner_radius=10, fg_color=COLORS["bg_input"],
            border_color=COLORS["border"], text_color=COLORS["text_primary"], font=ctk.CTkFont(size=14))
        self._setup_pw1.pack(pady=(0, 12))

        self._setup_pw2 = ctk.CTkEntry(card, placeholder_text=self.T["password_again"], show="●",
            width=320, height=42, corner_radius=10, fg_color=COLORS["bg_input"],
            border_color=COLORS["border"], text_color=COLORS["text_primary"], font=ctk.CTkFont(size=14))
        self._setup_pw2.pack(pady=(0, 8))

        self._setup_err = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12), text_color=COLORS["danger"])
        self._setup_err.pack(pady=(0, 8))

        ctk.CTkButton(card, text=self.T["create_btn"], width=320, height=44, corner_radius=10,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            font=ctk.CTkFont(size=15, weight="bold"), command=self._on_setup).pack(pady=(0, 20))

        self._setup_pw1.bind("<Return>", lambda e: self._setup_pw2.focus())
        self._setup_pw2.bind("<Return>", lambda e: self._on_setup())

    def _change_lang_setup(self, lcode):
        self.lang = lcode
        self.T = TRANSLATIONS[self.lang]
        if os.path.exists(self.config_path):
            self._save_lang_pref()
            self._build_login_screen()
        else:
            self._build_setup_screen()

    def _on_setup(self):
        pw1 = self._setup_pw1.get()
        pw2 = self._setup_pw2.get()
        if len(pw1) < 4:
            self._setup_err.configure(text=self.T["pw_min_4"])
            return
        if pw1 != pw2:
            self._setup_err.configure(text=self.T["pw_no_match"])
            return
        salt = os.urandom(16)
        pw_hash = hashlib.pbkdf2_hmac("sha256", pw1.encode(), salt, 480_000)
        config = {"salt": base64.b64encode(salt).decode(), "hash": base64.b64encode(pw_hash).decode(), "lang": self.lang}
        with open(self.config_path, "w") as f:
            json.dump(config, f)
        self.key = derive_key(pw1, salt)
        self.manager = NoteManager(self.data_dir, self.key)
        self._build_main_screen()

    # ═══════════════════════════════════════
    # Login Screen
    # ═══════════════════════════════════════
    def _build_login_screen(self):
        self._clear()
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Language selector
        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)
        for lcode, lname in [("tr", "🇹🇷"), ("en", "🇬🇧"), ("ru", "🇷🇺")]:
            ctk.CTkButton(lang_frame, text=lname, width=40, height=32,
                corner_radius=8, fg_color=COLORS["accent"] if self.lang == lcode else COLORS["bg_card"],
                hover_color=COLORS["accent_hover"],
                command=lambda lc=lcode: self._change_lang_setup(lc)
            ).pack(side="left", padx=2)

        ctk.CTkLabel(frame, text="🔐  DemirNotes", font=ctk.CTkFont(size=36, weight="bold"),
            text_color=COLORS["accent_light"]).pack(pady=(0, 5))
        ctk.CTkLabel(frame, text=self.T["login_subtitle"], font=ctk.CTkFont(size=14),
            text_color=COLORS["text_secondary"]).pack(pady=(0, 30))

        card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=16, width=420)
        card.pack(padx=20, pady=10)
        card.pack_propagate(False)
        card.configure(height=260, width=420)

        ctk.CTkLabel(card, text=self.T["login"], font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"]).pack(pady=(30, 20))

        self._login_pw = ctk.CTkEntry(card, placeholder_text=self.T["your_password"], show="●",
            width=320, height=42, corner_radius=10, fg_color=COLORS["bg_input"],
            border_color=COLORS["border"], text_color=COLORS["text_primary"], font=ctk.CTkFont(size=14))
        self._login_pw.pack(pady=(0, 8))
        self._login_pw.focus()

        self._login_err = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12), text_color=COLORS["danger"])
        self._login_err.pack(pady=(0, 8))

        ctk.CTkButton(card, text=self.T["login_btn"], width=320, height=44, corner_radius=10,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            font=ctk.CTkFont(size=15, weight="bold"), command=self._on_login).pack(pady=(0, 20))
        self._login_pw.bind("<Return>", lambda e: self._on_login())

    def _on_login(self):
        pw = self._login_pw.get()
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
            salt = base64.b64decode(config["salt"])
            stored_hash = base64.b64decode(config["hash"])
            pw_hash = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 480_000)
            if pw_hash != stored_hash:
                self._login_err.configure(text=self.T["wrong_password"])
                return
            self.key = derive_key(pw, salt)
            self.manager = NoteManager(self.data_dir, self.key)
            self._build_main_screen()
        except Exception as e:
            self._login_err.configure(text=f"{self.T['error']}: {e}")

    # ═══════════════════════════════════════
    # Main Screen
    # ═══════════════════════════════════════
    def _build_main_screen(self):
        self._clear()
        self.notes = self.manager.load_all_meta()

        main = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"])
        main.pack(fill="both", expand=True)
        self._main_frame = main

        # Sidebar
        self._sidebar = ctk.CTkFrame(main, fg_color=COLORS["bg_sidebar"], width=300, corner_radius=0)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # Sidebar top
        top_bar = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        top_bar.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(top_bar, text="📝 DemirNotes", font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["accent_light"]).pack(side="left")

        ctk.CTkButton(top_bar, text="⚙", width=32, height=32, corner_radius=8,
            fg_color="transparent", hover_color=COLORS["bg_hover"],
            text_color=COLORS["text_secondary"], font=ctk.CTkFont(size=16),
            command=self._show_settings).pack(side="right")

        # Buttons
        btn_bar = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        btn_bar.pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkButton(btn_bar, text=self.T["new_note"], height=36, corner_radius=8,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            font=ctk.CTkFont(size=13, weight="bold"), command=self._new_note
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))

        self._hidden_btn = ctk.CTkButton(btn_bar, text=self.T["hidden"], height=36, width=90,
            corner_radius=8, fg_color=COLORS["bg_card"], hover_color=COLORS["hidden_accent"],
            text_color=COLORS["text_secondary"], font=ctk.CTkFont(size=13),
            command=self._toggle_hidden)
        self._hidden_btn.pack(side="right")

        # Search
        search_frame = ctk.CTkFrame(self._sidebar, fg_color=COLORS["search_bg"], corner_radius=10, height=38)
        search_frame.pack(fill="x", padx=16, pady=(0, 10))
        search_frame.pack_propagate(False)
        ctk.CTkLabel(search_frame, text="🔍", font=ctk.CTkFont(size=14),
            text_color=COLORS["text_muted"]).pack(side="left", padx=(10, 4))
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", self._on_search)
        ctk.CTkEntry(search_frame, textvariable=self._search_var, placeholder_text=self.T["search"],
            fg_color="transparent", border_width=0, text_color=COLORS["text_primary"],
            font=ctk.CTkFont(size=13), height=34).pack(side="left", fill="x", expand=True, padx=(0, 8))

        # Category filter
        cat_frame = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        cat_frame.pack(fill="x", padx=16, pady=(0, 6))
        self._cat_menu_var = ctk.StringVar(value=self.T["all_notes"])
        cats = [self.T["all_notes"]] + self.manager.get_categories()
        self._cat_menu = ctk.CTkOptionMenu(cat_frame, values=cats, variable=self._cat_menu_var,
            width=200, height=30, corner_radius=8, fg_color=COLORS["bg_card"],
            button_color=COLORS["accent"], button_hover_color=COLORS["accent_hover"],
            dropdown_fg_color=COLORS["bg_card"], dropdown_hover_color=COLORS["bg_hover"],
            font=ctk.CTkFont(size=12), command=self._on_category_change)
        self._cat_menu.pack(side="left", fill="x", expand=True)

        # Note list
        self._note_list_frame = ctk.CTkScrollableFrame(self._sidebar, fg_color="transparent",
            scrollbar_button_color=COLORS["bg_hover"], scrollbar_button_hover_color=COLORS["accent"])
        self._note_list_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Editor area
        self._editor_frame = ctk.CTkFrame(main, fg_color=COLORS["bg_dark"], corner_radius=0)
        self._editor_frame.pack(side="right", fill="both", expand=True)

        self._build_editor_placeholder()
        self._refresh_note_list()

        # Keyboard shortcuts
        self.bind("<Control-n>", lambda e: self._new_note())
        self.bind("<Control-f>", lambda e: self._show_find_bar())
        self.bind("<Control-z>", lambda e: self._undo())
        self.bind("<Control-y>", lambda e: self._redo())
        self.bind("<Control-s>", lambda e: self._save_current_note())

    def _on_category_change(self, value):
        if value == self.T["all_notes"]:
            self.selected_category = ""
        else:
            self.selected_category = value
        self._refresh_note_list()

    # ═══════════════════════════════════════
    # Note List
    # ═══════════════════════════════════════
    def _refresh_note_list(self):
        for w in self._note_list_frame.winfo_children():
            w.destroy()
        query = self.search_query.lower().strip()
        visible = []
        for n in self.notes:
            if self.show_hidden and not n.hidden:
                continue
            if not self.show_hidden and n.hidden:
                continue
            if query:
                content = ""
                try:
                    content = self.manager.load_content(n.note_id).lower()
                except Exception:
                    pass
                if query not in n.title.lower() and query not in content:
                    continue
            if self.selected_category and n.category != self.selected_category:
                continue
            visible.append(n)

        if not visible:
            msg = self.T["no_hidden"] if self.show_hidden else self.T["no_notes"]
            if query:
                msg = self.T["no_results"]
            ctk.CTkLabel(self._note_list_frame, text=msg, text_color=COLORS["text_muted"],
                font=ctk.CTkFont(size=13)).pack(pady=40)
            return

        for note in visible:
            self._create_note_card(note)

    def _create_note_card(self, note):
        is_active = self.current_note and self.current_note.note_id == note.note_id
        card_color = COLORS["bg_hover"] if is_active else COLORS["bg_card"]
        card = ctk.CTkFrame(self._note_list_frame, fg_color=card_color, corner_radius=10, height=76, cursor="hand2")
        card.pack(fill="x", pady=3, padx=4)
        card.pack_propagate(False)

        tag_color = COLOR_TAGS.get(note.color_tag, COLOR_TAGS["default"])
        stripe = ctk.CTkFrame(card, fg_color=tag_color, width=4, corner_radius=2)
        stripe.pack(side="left", fill="y", padx=(6, 8), pady=8)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=8)

        title_text = note.title or self.T["untitled"]
        if note.hidden:
            title_text = "🔒 " + title_text
        if note.category:
            title_text += f" [{note.category}]"

        ctk.CTkLabel(info, text=title_text, font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_primary"], anchor="w").pack(fill="x")

        try:
            dt = datetime.fromisoformat(note.modified)
            date_str = dt.strftime("%d %b %Y  %H:%M")
        except Exception:
            date_str = ""

        att_count = len(note.attachments)
        extra = f"  📎{att_count}" if att_count > 0 else ""
        ctk.CTkLabel(info, text=date_str + extra, font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"], anchor="w").pack(fill="x")

        def on_click(e, nid=note.note_id):
            self._select_note(nid)
        card.bind("<Button-1>", on_click)
        for child in card.winfo_children():
            child.bind("<Button-1>", on_click)
            for gc in child.winfo_children():
                gc.bind("<Button-1>", on_click)

    def _select_note(self, note_id):
        self._save_current_note()
        for n in self.notes:
            if n.note_id == note_id:
                n.content = self.manager.load_content(n.note_id)
                self.current_note = n
                break
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._build_editor(self.current_note)
        self._refresh_note_list()

    # ═══════════════════════════════════════
    # Editor Placeholder
    # ═══════════════════════════════════════
    def _build_editor_placeholder(self):
        for w in self._editor_frame.winfo_children():
            w.destroy()
        ph = ctk.CTkFrame(self._editor_frame, fg_color="transparent")
        ph.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(ph, text="📝", font=ctk.CTkFont(size=48), text_color=COLORS["text_muted"]).pack(pady=(0, 8))
        ctk.CTkLabel(ph, text=self.T["select_note"], font=ctk.CTkFont(size=16),
            text_color=COLORS["text_muted"]).pack()

    # ═══════════════════════════════════════
    # Note Editor
    # ═══════════════════════════════════════
    def _build_editor(self, note):
        for w in self._editor_frame.winfo_children():
            w.destroy()
        self._image_refs.clear()

        # Top bar
        top = ctk.CTkFrame(self._editor_frame, fg_color=COLORS["bg_sidebar"], height=56, corner_radius=0)
        top.pack(fill="x")
        top.pack_propagate(False)

        self._title_var = ctk.StringVar(value=note.title)
        ctk.CTkEntry(top, textvariable=self._title_var, placeholder_text=self.T["note_title_ph"],
            fg_color="transparent", border_width=0, text_color=COLORS["text_primary"],
            font=ctk.CTkFont(size=18, weight="bold"), height=40
        ).pack(side="left", fill="x", expand=True, padx=16, pady=8)

        # Color tags
        color_frame = ctk.CTkFrame(top, fg_color="transparent")
        color_frame.pack(side="right", padx=(0, 8), pady=8)
        for tag_name, tag_color in COLOR_TAGS.items():
            ctk.CTkButton(color_frame, text="", width=18, height=18, corner_radius=9,
                fg_color=tag_color, hover_color=tag_color,
                command=lambda t=tag_name: self._set_color_tag(t)).pack(side="left", padx=2)

        # Action buttons
        action_frame = ctk.CTkFrame(top, fg_color="transparent")
        action_frame.pack(side="right", padx=(0, 8), pady=8)

        hide_text = self.T["show"] if note.hidden else self.T["hide"]
        ctk.CTkButton(action_frame, text=hide_text, width=80, height=32, corner_radius=8,
            fg_color=COLORS["bg_card"], hover_color=COLORS["hidden_accent"],
            text_color=COLORS["text_secondary"], font=ctk.CTkFont(size=12),
            command=self._toggle_note_hidden).pack(side="left", padx=(0, 6))

        ctk.CTkButton(action_frame, text=self.T["delete"], width=60, height=32, corner_radius=8,
            fg_color=COLORS["bg_card"], hover_color=COLORS["danger"],
            text_color=COLORS["danger"], font=ctk.CTkFont(size=12),
            command=self._delete_current).pack(side="left")

        # Toolbar
        toolbar = ctk.CTkFrame(self._editor_frame, fg_color=COLORS["toolbar_bg"], height=42, corner_radius=0)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        tool_btns = [
            (self.T["add_image"], self._add_image),
            (self.T["add_pdf"], self._add_pdf),
            (self.T["whiteboard"], self._open_whiteboard),
            (self.T["find_in_note"], self._show_find_bar),
            (self.T["export_pdf"], self._export_pdf),
            (self.T["undo"], self._undo),
            (self.T["redo"], self._redo),
        ]
        for txt, cmd in tool_btns:
            ctk.CTkButton(toolbar, text=txt, height=30, corner_radius=6,
                fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
                text_color=COLORS["text_secondary"], font=ctk.CTkFont(size=11),
                command=cmd).pack(side="left", padx=3, pady=6)

        # Category entry
        cat_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        cat_frame.pack(side="right", padx=8, pady=6)
        ctk.CTkLabel(cat_frame, text="📂", font=ctk.CTkFont(size=12)).pack(side="left")
        self._cat_var = ctk.StringVar(value=note.category)
        ctk.CTkEntry(cat_frame, textvariable=self._cat_var, placeholder_text=self.T["category_name"],
            width=120, height=28, corner_radius=6, fg_color=COLORS["bg_input"],
            border_width=0, text_color=COLORS["text_primary"],
            font=ctk.CTkFont(size=11)).pack(side="left", padx=4)

        # Find bar (hidden by default)
        self._find_frame = ctk.CTkFrame(self._editor_frame, fg_color=COLORS["search_bg"], height=40, corner_radius=0)
        self._find_var = ctk.StringVar()
        self._find_label = ctk.CTkLabel(self._find_frame, text="", font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"])

        # Content area
        self._content_text = ctk.CTkTextbox(self._editor_frame, fg_color=COLORS["bg_dark"],
            text_color=COLORS["text_primary"], font=ctk.CTkFont(family="Consolas", size=15),
            corner_radius=0, border_width=0, wrap="word",
            scrollbar_button_color=COLORS["bg_hover"], scrollbar_button_hover_color=COLORS["accent"],
            undo=True)
        self._content_text.pack(fill="both", expand=True, padx=20, pady=(12, 4))
        self._content_text.insert("1.0", note.content)
        self._content_text.bind("<KeyRelease>", self._on_content_change)

        # Attachments panel
        if note.attachments:
            self._build_attachments_panel(note)

        # Status bar
        status = ctk.CTkFrame(self._editor_frame, fg_color=COLORS["bg_sidebar"], height=28, corner_radius=0)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)

        char_count = len(note.content)
        word_count = len(note.content.split()) if note.content.strip() else 0
        status_text = f"  {char_count} {self.T['chars']}  •  {word_count} {self.T['words']}"
        if note.hidden:
            status_text += f"  •  {self.T['hidden_note']}"
        if note.category:
            status_text += f"  •  📂 {note.category}"

        self._status_label = ctk.CTkLabel(status, text=status_text, font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"], anchor="w")
        self._status_label.pack(side="left", padx=12)

    def _build_attachments_panel(self, note):
        att_frame = ctk.CTkFrame(self._editor_frame, fg_color=COLORS["bg_card"], corner_radius=8, height=80)
        att_frame.pack(fill="x", padx=20, pady=(4, 4))

        ctk.CTkLabel(att_frame, text=f"📎 {self.T['attachments']} ({len(note.attachments)})",
            font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=12, pady=(8, 4))

        att_list = ctk.CTkFrame(att_frame, fg_color="transparent")
        att_list.pack(fill="x", padx=12, pady=(0, 8))

        for att in note.attachments:
            att_item = ctk.CTkFrame(att_list, fg_color=COLORS["bg_input"], corner_radius=6, height=30)
            att_item.pack(side="left", padx=(0, 6), pady=2)

            fname = att.get("name", "file")
            ftype = att.get("type", "file")
            icon = "🖼" if ftype == "image" else "📄"

            ctk.CTkLabel(att_item, text=f"{icon} {fname}", font=ctk.CTkFont(size=11),
                text_color=COLORS["text_primary"]).pack(side="left", padx=(8, 4), pady=4)

            ctk.CTkButton(att_item, text=self.T["open_file"], width=40, height=22, corner_radius=4,
                fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                font=ctk.CTkFont(size=10),
                command=lambda a=att: self._open_attachment(a)).pack(side="left", padx=2, pady=4)

            ctk.CTkButton(att_item, text="✕", width=22, height=22, corner_radius=4,
                fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"],
                font=ctk.CTkFont(size=10),
                command=lambda a=att: self._remove_attachment(a)).pack(side="left", padx=(2, 6), pady=4)

    def _on_content_change(self, event=None):
        if not self.current_note:
            return
        content = self._content_text.get("1.0", "end-1c")
        char_count = len(content)
        word_count = len(content.split()) if content.strip() else 0
        status_text = f"  {char_count} {self.T['chars']}  •  {word_count} {self.T['words']}"
        if self.current_note.hidden:
            status_text += f"  •  {self.T['hidden_note']}"
        cat = self._cat_var.get() if hasattr(self, '_cat_var') else ""
        if cat:
            status_text += f"  •  📂 {cat}"
        self._status_label.configure(text=status_text)

    # ═══════════════════════════════════════
    # Actions
    # ═══════════════════════════════════════
    def _set_color_tag(self, tag):
        if self.current_note:
            self.current_note.color_tag = tag
            self._save_current_note()
            self._refresh_note_list()

    def _toggle_note_hidden(self):
        if self.current_note:
            self.current_note.hidden = not self.current_note.hidden
            self._save_current_note()
            self.current_note = None
            self._build_editor_placeholder()
            self._refresh_note_list()

    def _delete_current(self):
        if not self.current_note:
            return
        title = self.current_note.title or self.T["untitled"]
        if messagebox.askyesno(self.T["confirm"], f'"{title}" {self.T["delete_confirm"]}'):
            self.manager.delete(self.current_note.note_id)
            self.notes = [n for n in self.notes if n.note_id != self.current_note.note_id]
            self.current_note = None
            self._build_editor_placeholder()
            self._refresh_note_list()

    def _save_current_note(self):
        if not self.current_note:
            return
        try:
            self.current_note.title = self._title_var.get()
            self.current_note.content = self._content_text.get("1.0", "end-1c")
            if hasattr(self, '_cat_var'):
                self.current_note.category = self._cat_var.get()
        except Exception:
            pass
        self.manager.save(self.current_note)
        for i, n in enumerate(self.notes):
            if n.note_id == self.current_note.note_id:
                self.notes[i] = self.current_note
                return
        self.notes.insert(0, self.current_note)

    def _new_note(self):
        self._save_current_note()
        note = Note(title=self.T["new_note_title"], hidden=self.show_hidden)
        self.manager.save(note)
        self.notes.insert(0, note)
        self.current_note = note
        self._build_editor(note)
        self._refresh_note_list()

    def _toggle_hidden(self):
        self._save_current_note()
        self.show_hidden = not self.show_hidden
        self.current_note = None
        if self.show_hidden:
            self._hidden_btn.configure(text=self.T["normal"], fg_color=COLORS["hidden_accent"],
                hover_color=COLORS["hidden_accent_hover"], text_color="#fff")
        else:
            self._hidden_btn.configure(text=self.T["hidden"], fg_color=COLORS["bg_card"],
                hover_color=COLORS["hidden_accent"], text_color=COLORS["text_secondary"])
        self._build_editor_placeholder()
        self._refresh_note_list()

    def _on_search(self, *args):
        self.search_query = self._search_var.get()
        self._refresh_note_list()

    # ═══════════════════════════════════════
    # Undo / Redo
    # ═══════════════════════════════════════
    def _undo(self):
        try:
            self._content_text.edit_undo()
        except Exception:
            pass

    def _redo(self):
        try:
            self._content_text.edit_redo()
        except Exception:
            pass

    # ═══════════════════════════════════════
    # Find in Note
    # ═══════════════════════════════════════
    def _show_find_bar(self):
        if self._find_frame.winfo_ismapped():
            self._find_frame.pack_forget()
            self._content_text.tag_remove("find_highlight", "1.0", "end")
            return
        self._find_frame.pack(fill="x", before=self._content_text)
        self._find_frame.pack_propagate(False)

        for w in self._find_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(self._find_frame, text="🔍", font=ctk.CTkFont(size=13)).pack(side="left", padx=(12, 4))
        self._find_var = ctk.StringVar()
        find_entry = ctk.CTkEntry(self._find_frame, textvariable=self._find_var,
            placeholder_text=self.T["find_placeholder"], width=200, height=28,
            corner_radius=6, fg_color=COLORS["bg_input"], border_width=0,
            text_color=COLORS["text_primary"], font=ctk.CTkFont(size=12))
        find_entry.pack(side="left", padx=4)
        find_entry.focus()
        find_entry.bind("<Return>", lambda e: self._do_find_next())

        ctk.CTkButton(self._find_frame, text=self.T["find_prev"], width=60, height=26,
            corner_radius=6, fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            font=ctk.CTkFont(size=11), command=self._do_find_prev).pack(side="left", padx=2)
        ctk.CTkButton(self._find_frame, text=self.T["find_next"], width=60, height=26,
            corner_radius=6, fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            font=ctk.CTkFont(size=11), command=self._do_find_next).pack(side="left", padx=2)

        self._find_label = ctk.CTkLabel(self._find_frame, text="", font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"])
        self._find_label.pack(side="left", padx=8)

        ctk.CTkButton(self._find_frame, text="✕", width=26, height=26, corner_radius=6,
            fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"],
            font=ctk.CTkFont(size=11), command=self._show_find_bar).pack(side="right", padx=8)

    def _do_find_next(self):
        query = self._find_var.get()
        if not query:
            return
        self._content_text.tag_remove("find_highlight", "1.0", "end")
        self._content_text.tag_config("find_highlight", background=COLORS["warning"], foreground="#000")

        content = self._content_text.get("1.0", "end-1c")
        self.find_matches = []
        start = 0
        while True:
            idx = content.lower().find(query.lower(), start)
            if idx == -1:
                break
            self.find_matches.append(idx)
            start = idx + 1

        if not self.find_matches:
            self._find_label.configure(text=self.T["no_results"])
            return

        self.find_index = (self.find_index + 1) % len(self.find_matches)
        for m in self.find_matches:
            line = content[:m].count("\n") + 1
            col = m - content[:m].rfind("\n") - 1
            end_col = col + len(query)
            self._content_text.tag_add("find_highlight", f"{line}.{col}", f"{line}.{end_col}")

        # Scroll to current match
        m = self.find_matches[self.find_index]
        line = content[:m].count("\n") + 1
        col = m - content[:m].rfind("\n") - 1
        self._content_text.see(f"{line}.{col}")
        self._find_label.configure(text=f"{self.find_index + 1}/{len(self.find_matches)}")

    def _do_find_prev(self):
        if not self.find_matches:
            self._do_find_next()
            return
        self.find_index = (self.find_index - 2) % len(self.find_matches)
        self._do_find_next()

    # ═══════════════════════════════════════
    # Attachments
    # ═══════════════════════════════════════
    def _add_image(self):
        if not self.current_note:
            return
        path = filedialog.askopenfilename(
            title=self.T["add_image"],
            filetypes=[(self.T["image_files"], "*.png *.jpg *.jpeg *.gif *.bmp *.webp")])
        if not path:
            return
        try:
            with open(path, "rb") as f:
                data = f.read()
            fname = os.path.basename(path)
            att_id = self.manager.save_attachment(self.current_note.note_id, fname, data)
            self.current_note.attachments.append({"id": att_id, "name": fname, "type": "image"})
            self._save_current_note()
            self._build_editor(self.current_note)
        except Exception as e:
            messagebox.showerror(self.T["error"], str(e))

    def _add_pdf(self):
        if not self.current_note:
            return
        path = filedialog.askopenfilename(
            title=self.T["add_pdf"],
            filetypes=[(self.T["pdf_files"], "*.pdf")])
        if not path:
            return
        try:
            with open(path, "rb") as f:
                data = f.read()
            fname = os.path.basename(path)
            att_id = self.manager.save_attachment(self.current_note.note_id, fname, data)
            self.current_note.attachments.append({"id": att_id, "name": fname, "type": "pdf"})
            self._save_current_note()
            self._build_editor(self.current_note)
        except Exception as e:
            messagebox.showerror(self.T["error"], str(e))

    def _open_attachment(self, att):
        try:
            data = self.manager.load_attachment(att["id"])
            if not data:
                return
            tmp_dir = os.path.join(self.data_dir, "tmp")
            os.makedirs(tmp_dir, exist_ok=True)
            tmp_path = os.path.join(tmp_dir, att["name"])
            with open(tmp_path, "wb") as f:
                f.write(data)
            os.startfile(tmp_path)
        except Exception as e:
            messagebox.showerror(self.T["error"], str(e))

    def _remove_attachment(self, att):
        if not self.current_note:
            return
        self.manager.remove_attachment(att["id"])
        self.current_note.attachments = [a for a in self.current_note.attachments if a["id"] != att["id"]]
        self._save_current_note()
        self._build_editor(self.current_note)

    # ═══════════════════════════════════════
    # Whiteboard
    # ═══════════════════════════════════════
    def _open_whiteboard(self):
        if not self.current_note:
            return
        existing = list(self.current_note.drawing_data) if self.current_note.drawing_data else []
        WhiteboardDialog(self, self.lang, existing_strokes=existing, callback=self._on_drawing_saved)

    def _on_drawing_saved(self, strokes):
        if self.current_note:
            self.current_note.drawing_data = strokes
            self._save_current_note()

    # ═══════════════════════════════════════
    # Export PDF
    # ═══════════════════════════════════════
    def _export_pdf(self):
        if not self.current_note:
            return
        try:
            from fpdf import FPDF
        except ImportError:
            messagebox.showerror(self.T["error"], "fpdf2 not installed. Run: pip install fpdf2")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[(self.T["pdf_files"], "*.pdf")],
            initialfile=f"{self.current_note.title or 'note'}.pdf")
        if not path:
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            # Use a Unicode font
            font_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arial.ttf")
            if os.path.exists(font_path):
                pdf.add_font("ArialUni", "", font_path, uni=True)
                pdf.set_font("ArialUni", size=20)
            else:
                pdf.set_font("Helvetica", size=20)

            pdf.cell(0, 12, self.current_note.title or self.T["untitled"], new_x="LMARGIN", new_y="NEXT")

            if os.path.exists(font_path):
                pdf.set_font("ArialUni", size=12)
            else:
                pdf.set_font("Helvetica", size=12)

            content = self._content_text.get("1.0", "end-1c")
            pdf.multi_cell(0, 7, content)
            pdf.output(path)
            messagebox.showinfo(self.T["success"], self.T["export_success"])
        except Exception as e:
            messagebox.showerror(self.T["error"], str(e))

    # ═══════════════════════════════════════
    # Settings Dialog
    # ═══════════════════════════════════════
    def _show_settings(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.T["settings"])
        dialog.geometry("440x480")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS["bg_dark"])
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=self.T["settings"], font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["accent_light"]).pack(pady=(20, 16))

        # Language selection
        lang_card = ctk.CTkFrame(dialog, fg_color=COLORS["bg_card"], corner_radius=12)
        lang_card.pack(fill="x", padx=24, pady=(0, 12))

        ctk.CTkLabel(lang_card, text=self.T["language"], font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLORS["text_primary"]).pack(pady=(16, 8))

        lang_btns = ctk.CTkFrame(lang_card, fg_color="transparent")
        lang_btns.pack(pady=(0, 16))
        for lcode, lkey in [("tr", "lang_tr"), ("en", "lang_en"), ("ru", "lang_ru")]:
            ctk.CTkButton(lang_btns, text=self.T[lkey], width=120, height=36, corner_radius=8,
                fg_color=COLORS["accent"] if self.lang == lcode else COLORS["bg_input"],
                hover_color=COLORS["accent_hover"],
                font=ctk.CTkFont(size=13),
                command=lambda lc=lcode, d=dialog: self._change_language(lc, d)
            ).pack(side="left", padx=4)

        # Password change
        pw_card = ctk.CTkFrame(dialog, fg_color=COLORS["bg_card"], corner_radius=12)
        pw_card.pack(fill="x", padx=24, pady=(0, 16))

        ctk.CTkLabel(pw_card, text=self.T["change_password"], font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLORS["text_primary"]).pack(pady=(16, 12))

        old_pw = ctk.CTkEntry(pw_card, placeholder_text=self.T["current_pw"], show="●",
            width=300, height=38, corner_radius=8, fg_color=COLORS["bg_input"],
            border_color=COLORS["border"], text_color=COLORS["text_primary"])
        old_pw.pack(pady=(0, 8))

        new_pw = ctk.CTkEntry(pw_card, placeholder_text=self.T["new_pw"], show="●",
            width=300, height=38, corner_radius=8, fg_color=COLORS["bg_input"],
            border_color=COLORS["border"], text_color=COLORS["text_primary"])
        new_pw.pack(pady=(0, 8))

        new_pw2 = ctk.CTkEntry(pw_card, placeholder_text=self.T["new_pw_again"], show="●",
            width=300, height=38, corner_radius=8, fg_color=COLORS["bg_input"],
            border_color=COLORS["border"], text_color=COLORS["text_primary"])
        new_pw2.pack(pady=(0, 8))

        err_label = ctk.CTkLabel(pw_card, text="", font=ctk.CTkFont(size=11), text_color=COLORS["danger"])
        err_label.pack(pady=(0, 4))

        def do_change():
            old = old_pw.get()
            n1 = new_pw.get()
            n2 = new_pw2.get()
            with open(self.config_path, "r") as f:
                config = json.load(f)
            salt = base64.b64decode(config["salt"])
            stored = base64.b64decode(config["hash"])
            check = hashlib.pbkdf2_hmac("sha256", old.encode(), salt, 480_000)
            if check != stored:
                err_label.configure(text=self.T["wrong_current_pw"])
                return
            if len(n1) < 4:
                err_label.configure(text=self.T["pw_min_4"])
                return
            if n1 != n2:
                err_label.configure(text=self.T["pw_no_match"])
                return
            old_key = self.key
            new_salt = os.urandom(16)
            new_key = derive_key(n1, new_salt)
            all_notes = self.manager.load_all_meta()
            for note in all_notes:
                note.content = self.manager.load_content(note.note_id)
            self.key = new_key
            self.manager = NoteManager(self.data_dir, new_key)
            for note in all_notes:
                self.manager.save(note)
            new_hash = hashlib.pbkdf2_hmac("sha256", n1.encode(), new_salt, 480_000)
            config = {"salt": base64.b64encode(new_salt).decode(),
                      "hash": base64.b64encode(new_hash).decode(), "lang": self.lang}
            with open(self.config_path, "w") as f:
                json.dump(config, f)
            self.notes = self.manager.load_all_meta()
            dialog.destroy()
            messagebox.showinfo(self.T["success"], self.T["pw_changed"])

        ctk.CTkButton(pw_card, text=self.T["change_pw_btn"], width=300, height=38,
            corner_radius=8, fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            font=ctk.CTkFont(size=13, weight="bold"), command=do_change).pack(pady=(4, 16))

    def _change_language(self, lcode, dialog):
        self.lang = lcode
        self.T = TRANSLATIONS[self.lang]
        self._save_lang_pref()
        dialog.destroy()
        self._save_current_note()
        self._build_main_screen()

    # ═══════════════════════════════════════
    # Cleanup
    # ═══════════════════════════════════════
    def destroy(self):
        self._save_current_note()
        # Clean temp files
        tmp_dir = os.path.join(self.data_dir, "tmp")
        if os.path.exists(tmp_dir):
            try:
                shutil.rmtree(tmp_dir)
            except Exception:
                pass
        super().destroy()


# ══════════════════════════════════════════════════
# Entry Point
# ══════════════════════════════════════════════════
if __name__ == "__main__":
    app = DemirNotesApp()
    app.mainloop()

