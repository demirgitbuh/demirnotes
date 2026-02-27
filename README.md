# DemirNotes 🔐

**Şifreli Not Uygulaması / Encrypted Note-Taking Application**

Modern arayüzlü, AES-256 şifrelemeli, çok dilli masaüstü not uygulaması.

## ✨ Özellikler / Features

| Özellik | Feature |
|---------|---------|
| 🔐 AES-256 Şifreleme | AES-256 Encryption |
| 🌍 3 Dil (TR/EN/RU) | 3 Languages (TR/EN/RU) |
| 🖼️ Resim Ekleme | Image Attachments |
| 📄 PDF Ekleme | PDF Attachments |
| 🎨 Çizim Tahtası | Whiteboard / Drawing |
| ✏️ Kalem, Silgi, Renk | Pen, Eraser, Color Picker |
| 🔍 Notta Ara (Ctrl+F) | Find in Note |
| 🏷️ Renk Etiketleri | Color Tags |
| 📂 Kategori Sistemi | Category System |
| 🔒 Gizli Notlar | Hidden / Secret Notes |
| ↩️ Geri Al / Yinele | Undo / Redo |
| 📤 PDF Dışa Aktarma | Export as PDF |
| 💾 Otomatik Kaydetme | Auto-Save |
| ⚙️ Şifre Değiştirme | Password Change |

## 🚀 Kurulum / Installation

### Gereksinimler / Requirements

```bash
pip install customtkinter cryptography Pillow fpdf2
```

### Çalıştırma / Run

```bash
python demirnotes.py
```

### EXE Oluşturma / Build EXE

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name demirnotes --icon=Demnote.ico demirnotes.py
```

## 📁 Veri Yapısı / Data Structure

```
demirnotes/           ← Encrypted data folder
├── config.dat        ← Password hash + language preference
├── notes/
│   ├── {id}.enc      ← Encrypted note content
│   └── {id}.meta     ← Encrypted metadata
└── attachments/
    └── {id}_{name}.enc  ← Encrypted attachments
```

## ⌨️ Kısayollar / Shortcuts

| Kısayol | Açıklama |
|---------|----------|
| Ctrl+N | Yeni Not / New Note |
| Ctrl+F | Notta Ara / Find in Note |
| Ctrl+Z | Geri Al / Undo |
| Ctrl+Y | Yinele / Redo |
| Ctrl+S | Kaydet / Save |

## 📜 License

MIT License (c) 2026 Demirarch
