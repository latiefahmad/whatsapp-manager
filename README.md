# WhatsApp Manager - Multi Account Desktop App

Aplikasi desktop Windows untuk mengelola multiple akun WhatsApp sekaligus dengan UI modern dan fresh.

## ✨ Features
- 📱 Multiple WhatsApp accounts dalam satu aplikasi
- 🔐 Password lock per tab untuk keamanan extra
- 🔍 Zoom controls (50%-300%) dengan auto-save
- 💾 Session persistence (auto-login setelah scan QR pertama)
- 🎨 Fresh green theme dengan unified controls
- 🪟 Browser-style tab interface
- ⚡ Lightweight & efficient
- ⌨️ Keyboard shortcuts (Ctrl+T, Ctrl+W, Ctrl+±, F5)

---

## 🚀 Quick Start

### Option 1: Run from Source (Recommended for Development)
```bash
# 1. Clone repository
git clone <your-repo-url>
cd whatsapp-manager

# 2. Install dependencies
pip install -r requirements.txt
# or use the batch file:
install_dependencies.bat

# 3. Run application
python main.py
# or use:
run.bat
```

### Option 2: Build Executable
```bash
# Build standalone EXE
REBUILD_EXE.bat

# Build installer (requires Inno Setup)
QUICK_BUILD.bat
```

---

## 🏗️ Building

### Build Executable (EXE)
```bash
# Quick rebuild (cleans and builds)
REBUILD_EXE.bat

# Or manually:
pyinstaller build.spec
```

**Output:** `dist\WhatsAppManager\WhatsAppManager.exe`

### Build Installer (requires Inno Setup)
1. Install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Run `QUICK_BUILD.bat`
3. Installer akan tersimpan di `installer_output\`

### PyInstaller Spec
File `build.spec` sudah dikonfigurasi dengan:
- Hidden imports untuk PyQt6 modules
- Excluded packages (matplotlib, numpy, pandas)
- Optimized untuk ukuran file minimal

---

## 📱 Usage Guide

### Adding Account
1. Click **`+`** button (atau tekan `Ctrl+T`)
2. Masukkan nama account (e.g., "Pribadi", "Bisnis")
3. Scan QR code dengan WhatsApp di HP
4. Session tersimpan otomatis

### Zoom Controls
- **Zoom In**: Click `+` atau `Ctrl++`
- **Zoom Out**: Click `−` atau `Ctrl+-`
- **Reset**: Click percentage label atau `Ctrl+0`
- Zoom level auto-save per account

### Password Lock
1. Right-click tab → **Set Password**
2. Enter password (SHA256 encrypted)
3. Click **🔓** untuk lock tab
4. Enter password untuk unlock

### Keyboard Shortcuts
- `Ctrl+T` - Add new account
- `Ctrl+W` - Close current tab
- `Ctrl++` - Zoom in
- `Ctrl+-` - Zoom out
- `Ctrl+0` - Reset zoom
- `F5` / `Ctrl+R` - Reload tab

### Managing Accounts
- **Close tab**: Click X di tab atau `Ctrl+W`
- **Switch tabs**: Click tab atau drag-drop untuk reorder
- **Right-click menu**: Set password, change password, remove password

---

## 💻 System Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 2GB minimum (4GB recommended untuk 3+ accounts)
- **Disk**: 500MB untuk aplikasi + session data
- **Internet**: Diperlukan untuk WhatsApp Web

---

## 🛠️ Tech Stack
- **PyQt6** - Modern cross-platform GUI framework
- **PyQt6-WebEngine** - Embedded Chromium for WhatsApp Web
- **SQLite** - Local database untuk account & session management
- **PyInstaller** - Package Python app menjadi standalone EXE
- **Inno Setup** - Create professional Windows installer

---

## 📂 Project Structure
```
whatsapp-manager/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies (PyQt6, PyQt6-WebEngine)
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
│
├── core/                            # Core functionality
│   ├── __init__.py
│   └── database.py                  # SQLite database (accounts, zoom, passwords)
│
├── gui/                             # GUI components
│   ├── __init__.py
│   ├── main_window.py               # Main window with tabs & global controls
│   └── whatsapp_tab.py              # WhatsApp Web tab (zoom, lock, reload)
│
├── build.spec                       # PyInstaller configuration
├── installer.iss                    # Inno Setup installer script
│
├── run.bat                          # Quick run from source
├── install_dependencies.bat         # Install requirements
├── build_exe.bat                    # Build EXE
├── REBUILD_EXE.bat                  # Clean + rebuild EXE
└── QUICK_BUILD.bat                  # Build installer
```

### Generated Folders (gitignored)
```
dist/                                # PyInstaller output
build/                               # PyInstaller temp files
__pycache__/                         # Python cache
sessions/                            # WhatsApp session data
*.db                                 # SQLite database files
```

---

## 🎨 UI Features

### Fresh Green Theme
- WhatsApp green (#00a884) sebagai primary color
- Unified color scheme untuk tabs dan controls
- Hover states dengan lighter green (#06cf9c)
- Selected tab dengan dark background + green border

### Unified Control Bar
All controls dalam satu baris dengan tabs:
```
[Tab 1] [Tab 2]     [−] [80%] [+] [🔒] [🔄] [+]
                     ↑    ↑    ↑   ↑    ↑   ↑
                  Zoom Current Zoom Lock Reload Add
                  Out  Level   In
```

### Space Efficient
- No redundant toolbars
- No visible separators (clean spacing)
- Maximum vertical space untuk WhatsApp Web content
- Seamless tab appearance

---

## ❓ FAQ

**Q: Apakah ini WhatsApp automation bot?**  
A: Tidak. Ini hanya multi-account client seperti WhatsApp.exe official.

**Q: Apakah melanggar Terms of Service WhatsApp?**  
A: Tidak. Aplikasi hanya load WhatsApp Web resmi (web.whatsapp.com).

**Q: Kenapa RAM usage tinggi?**  
A: Setiap tab = 1 Chromium instance. Trade-off untuk 100% WhatsApp Web compatibility.

**Q: Bisa export chat?**  
A: Gunakan fitur export bawaan WhatsApp Web.

**Q: Windows SmartScreen warning?**  
A: Normal untuk unsigned EXE. Click "More info" → "Run anyway".

---

## 🐛 Troubleshooting

### WhatsApp tidak load / blank page
- Check internet connection
- Click **🔄 Reload** button
- Restart aplikasi

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
