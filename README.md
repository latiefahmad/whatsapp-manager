# WhatsApp Manager - Multi Account Desktop App

Aplikasi desktop Windows untuk mengelola multiple WhatsApp accounts sekaligus dengan UI modern dan fresh.

## 🆕 Latest Update (v1.2.3)
# WhatsApp Manager - Multi Account Desktop App

> Aplikasi desktop Windows untuk mengelola multiple WhatsApp accounts dalam satu window dengan UI modern

![Version](https://img.shields.io/badge/version-1.2.3-green) ![Platform](https://img.shields.io/badge/platform-Windows-blue) ![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Key Features

### 🎯 Core Features
- 📱 **Multi-Account** - Jalankan beberapa WhatsApp sekaligus dalam satu aplikasi
- 💾 **Session Persistence** - Auto-login setelah scan QR pertama kali
- 🔍 **Zoom Controls** - Sesuaikan ukuran tampilan (50%-300%) dengan auto-save
- 🪟 **Browser-Style Tabs** - Interface seperti browser dengan drag-drop support
- ⚡ **Lightweight** - Optimized untuk performa dan memori

### 🔐 Security & Privacy
- 🔒 **Password Lock** - Proteksi per tab dengan enkripsi SHA256
- ✨ **Blur Effect** - Modern glassmorphism ketika tab locked
- 🏠 **Local Storage** - Semua data tersimpan lokal, tidak ada cloud sync
- 🔐 **Encrypted Passwords** - SHA256 hashing untuk keamanan maksimal

### 🎨 Modern UI
- 🎨 Fresh WhatsApp green theme (#00a884)
- 🖼️ Glassmorphism blur effect on lock screen
- 🎯 Unified control bar (all controls in one place)
- ⌨️ Full keyboard shortcuts support

## Previous Updates
**v1.2.2** - Standard browser tab behavior (rightmost insertion)
**v1.2.1-hotfix** - Fixed second account crash regression
**v1.2.0** - Fixed QR code crash on 4th+ account ([details](FIX_QR_CRASH_V2.md))
**v1.1.0** - Fixed force close when adding second account ([details](FIX_FORCE_CLOSE.md))

## ✨ Features
- 📱 Multiple WhatsApp accounts dalam satu aplikasi
- 🔐 Password lock per tab dengan **blur effect** yang modern
- 🔍 Zoom controls (50%-300%) dengan auto-save
- 💾 Session persistence (auto-login setelah scan QR pertama)
- 🎨 Fresh green theme dengan unified controls
- 🪟 Browser-style tab interface
- ⚡ Lightweight & efficient
- ⌨️ Keyboard shortcuts (Ctrl+T, Ctrl+W, Ctrl+±, F5)
- ✨ Glassmorphism lock screen dengan blur effect

## 🚀 Quick Start

### 1️⃣ Run from Source
```bash
# Install dependencies
pip install -r requirements.txt
# atau: install_dependencies.bat

# Run application
python main.py
# atau: run.bat
```

### 2️⃣ Build Executable
```bash
# Build EXE
REBUILD_EXE.bat

# Build Installer (requires Inno Setup)
QUICK_BUILD.bat
```

**Output**: `dist\WhatsAppManager\WhatsAppManager.exe`

## � Usage Guide

### ➕ Tambah Akun
1. Klik tombol **`+`** atau tekan `Ctrl+T`
2. Masukkan nama akun (misal: "Pribadi", "Bisnis")
3. Scan QR code dengan WhatsApp di HP
4. Session tersimpan otomatis

### 🔐 Password Lock
1. Right-click tab → **Set Password**
2. Masukkan password (akan di-hash SHA256)
3. Klik **🔓** untuk lock/unlock tab
4. Tab locked menampilkan **blur effect** yang modern

### 🔍 Zoom Control
| Action | Shortcut | Button |
|--------|----------|--------|
| Zoom In | `Ctrl++` | Click `+` |
| Zoom Out | `Ctrl+-` | Click `−` |
| Reset | `Ctrl+0` | Click `%` |

### ⌨️ Keyboard Shortcuts
- `Ctrl+T` - Tambah akun baru
- `Ctrl+W` - Tutup tab aktif
- `Ctrl++/-/0` - Zoom in/out/reset
- `F5` atau `Ctrl+R` - Reload tab

### 📋 Right-Click Menu
- Set Password - Buat password untuk tab
- Change Password - Ubah password existing
- Remove Password - Hapus password protection

## 💻 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 64-bit | Windows 11 64-bit |
| **RAM** | 4GB (3-4 accounts) | 8GB+ (6-8 accounts) |
| **GPU** | Integrated | Dedicated GPU |
| **Disk** | 500MB | 1GB |
| **Internet** | Required | Stable connection |

> 💡 **Note**: Setiap account menggunakan ~400MB RAM

## 🛠️ Tech Stack

- **PyQt6** - GUI framework
- **PyQt6-WebEngine** - Embedded Chromium
- **SQLite** - Database lokal
- **PyInstaller** - Build executable
- **Inno Setup** - Windows installer

## 📂 Project Structure

```
whatsapp-manager/
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── build.spec                  # PyInstaller config
├── installer.iss               # Inno Setup script
│
├── core/
│   └── database.py             # SQLite (accounts, zoom, passwords)
│
├── gui/
│   ├── main_window.py          # Main window + tabs
│   └── whatsapp_tab.py         # WhatsApp Web tab + lock screen
│
└── *.bat                       # Build & run scripts
```

### Build Scripts
- `run.bat` - Run dari source
- `install_dependencies.bat` - Install requirements
- `REBUILD_EXE.bat` - Build executable
- `QUICK_BUILD.bat` - Build installer

## 🐛 Troubleshooting

### WhatsApp tidak load / blank page
```bash
# Check internet connection
# Click 🔄 Reload button
# Restart aplikasi
```

### QR code tidak muncul
```bash
# Update GPU drivers
# Test WebGL: https://get.webgl.org/
# Reduce account count
# Click 🔄 Reload atau tunggu auto-reload
```

### Error: "No module named PyQt6"
```bash
pip install -r requirements.txt
```

### Error: "missing vcruntime140.dll"
Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Windows SmartScreen warning
Normal untuk unsigned EXE. Klik **"More info"** → **"Run anyway"**

### Lupa password tab
- Right-click tab → **Remove Password**
- Atau hapus database: `%USERPROFILE%\.whatsapp-manager\accounts.db`

### High RAM usage
Setiap tab = 1 Chromium instance (~400MB). Trade-off untuk 100% WhatsApp Web compatibility.

## 📝 Changelog

### v1.2.3 (Latest)
- ✨ **NEW**: Blur effect on lock screen (glassmorphism)
- 🎨 Modern semi-transparent overlay
- 🔐 Content visible but blurred when locked

### v1.2.2
- 🪟 Standard browser tab behavior (rightmost insertion)
- 🎯 Simplified tab management logic

### v1.2.0
- 🐛 **FIX**: QR code crash on 4th+ account
- ⚡ GPU acceleration enabled (WebGL + 2D Canvas)
- 💾 Increased cache to 100MB
- 🚀 Renderer limit increased to 15

### v1.1.0
- 🐛 **FIX**: Force close when adding second account
- 🔧 Unique profile names with timestamp
- 🎯 Better memory management

## ❓ FAQ

**Q: Apakah ini bot automation?**  
A: Tidak. Ini multi-account client seperti WhatsApp Desktop official.

**Q: Melanggar ToS WhatsApp?**  
A: Tidak. Hanya load web.whatsapp.com resmi.

**Q: Data disimpan dimana?**  
A: Lokal di `%USERPROFILE%\.whatsapp-manager\` (tidak ada cloud sync)

**Q: Bisa export chat?**  
A: Ya, gunakan fitur export bawaan WhatsApp Web.

## 🔐 Security & Privacy

- 🔒 Password di-hash SHA256
- 🏠 Semua data tersimpan lokal
- 🌐 Hanya load web.whatsapp.com official
- 📖 Open source (bisa diaudit)

## 📜 License

MIT License - Free for personal and commercial use

---

**Made with ❤️ for WhatsApp power users**

## 🐛 Troubleshooting

### Force close when loading QR code (4th+ account)
**✅ FIXED in v1.2.0** - If you still experience this issue:
1. Check available RAM: `Task Manager → Performance`
2. Close other applications to free memory
3. Reduce account count to 6 or less
4. Update GPU drivers
5. See [FIX_QR_CRASH_V2.md](FIX_QR_CRASH_V2.md) for detailed solutions

### Force close when adding second account
**✅ FIXED in v1.1.0** - If you still experience this issue:
1. Rebuild the app: `REBUILD_EXE.bat`
2. Test with: `TEST_MULTI_ACCOUNT.bat`
3. See [FIX_FORCE_CLOSE.md](FIX_FORCE_CLOSE.md) for details

### WhatsApp tidak load / blank page
- Check internet connection
- Click **🔄 Reload** button
- Restart aplikasi

### QR code tidak muncul
- **Check GPU**: Update graphics drivers
- **Test WebGL**: Visit https://get.webgl.org/ in Chrome
- **Reduce accounts**: Try with fewer accounts
- Click **🔄 Reload** button (or wait for auto-reload)
- See [FIX_QR_CRASH_V2.md](FIX_QR_CRASH_V2.md) for GPU troubleshooting

### Error: "No module named PyQt6"
```bash
pip install -r requirements.txt
```

### Error: "DLL load failed" atau "missing vcruntime140.dll"
Install Visual C++ Redistributable:  
https://aka.ms/vs/17/release/vc_redist.x64.exe

### Build error: "PyInstaller command not found"
```bash
pip install pyinstaller
```

### Lupa password tab
- Right-click tab → Remove Password (akan reset ulang tab)
- Atau hapus database: `%APPDATA%\WhatsAppManager\accounts.db`

### QR code tidak muncul
- Buka Developer Tools (F12 di webview)
- Check console untuk error
- Coba update Chrome User Agent di `whatsapp_tab.py`

---

## 🔐 Security & Privacy

- **Passwords**: SHA256 hashed, stored in local SQLite database
- **Sessions**: Stored locally di `%APPDATA%\WhatsAppManager\`
- **No Cloud**: Semua data tersimpan lokal, tidak ada sync ke cloud
- **WhatsApp Web**: Menggunakan web.whatsapp.com official
- **Open Source**: Source code dapat diaudit

## 🛣️ Roadmap

- [ ] Multi-language support (EN, ID)
- [ ] Custom themes
- [ ] Notification badges per tab
- [ ] Tab grouping
- [ ] Auto-update mechanism
- [ ] MacOS & Linux support

## 📜 License
MIT License - Free for personal and commercial use

## 🤝 Contributing

Pull requests are welcome! Untuk perubahan besar:
1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support

Jika ada issues atau pertanyaan:
- Open an issue di GitHub
- Describe masalah dengan detail (OS, Python version, error message)
- Attach screenshot jika perlu

---

**Made with ❤️ for WhatsApp power users**
