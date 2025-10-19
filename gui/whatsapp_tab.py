from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QInputDialog, QMessageBox
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtGui import QKeySequence, QShortcut
import os

class WhatsAppTab(QWidget):
    def __init__(self, account_id, name, session_dir, zoom_level=1.0, has_password=False, db=None):
        super().__init__()
        self.account_id = account_id
        self.name = name
        self.session_dir = session_dir
        self.zoom_level = zoom_level  # Default 100%
        self.has_password = has_password
        self.is_locked = has_password  # Lock by default if password set
        self.db = db
        
        self.setup_ui()
        self.setup_shortcuts()
        self.load_whatsapp()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # No toolbar anymore - controls moved to global tab bar!
        
        # WebView or Lock Screen
        self.web_view = None
        self.lock_screen = None
        
        if self.is_locked:
            # Show lock screen instead of WebView
            self.show_lock_screen(layout)
        else:
            # Show WebView
            self.create_webview()
            if self.web_view:
                layout.addWidget(self.web_view)
                # Apply saved zoom level
                self.apply_zoom()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts for zoom and reload"""
        # Zoom in: Ctrl++ or Ctrl+=
        zoom_in_shortcut = QShortcut(QKeySequence("Ctrl++"), self)
        zoom_in_shortcut.activated.connect(self.zoom_in)
        zoom_in_shortcut2 = QShortcut(QKeySequence("Ctrl+="), self)
        zoom_in_shortcut2.activated.connect(self.zoom_in)
        
        # Zoom out: Ctrl+-
        zoom_out_shortcut = QShortcut(QKeySequence("Ctrl+-"), self)
        zoom_out_shortcut.activated.connect(self.zoom_out)
        
        # Reset zoom: Ctrl+0
        reset_zoom_shortcut = QShortcut(QKeySequence("Ctrl+0"), self)
        reset_zoom_shortcut.activated.connect(self.reset_zoom)
        
        # Reload: F5 or Ctrl+R
        reload_shortcut = QShortcut(QKeySequence("F5"), self)
        reload_shortcut.activated.connect(self.reload_whatsapp)
        reload_shortcut2 = QShortcut(QKeySequence("Ctrl+R"), self)
        reload_shortcut2.activated.connect(self.reload_whatsapp)
    
    def create_webview(self):
        try:
            print(f"Creating webview for {self.name}...")
            
            # Create profile with unique name
            profile = QWebEngineProfile(f"profile_{self.account_id}", self)
            profile.setPersistentStoragePath(self.session_dir)
            profile.setCachePath(os.path.join(self.session_dir, "cache"))
            
            # Set modern Chrome User Agent to bypass WhatsApp Web detection
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            profile.setHttpUserAgent(user_agent)
            
            # Enable all necessary features
            settings = profile.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
            
            # Create page
            page = QWebEnginePage(profile, self)
            
            # Create webview
            self.web_view = QWebEngineView(self)
            self.web_view.setPage(page)
            
            print(f"WebView created successfully for {self.name}")
            
        except Exception as e:
            print(f"ERROR creating webview for {self.name}: {e}")
            import traceback
            traceback.print_exc()
            self.web_view = None
    
    def load_whatsapp(self):
        if self.web_view:
            # Inject JavaScript to hide automation detection
            js_script = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """
            self.web_view.page().runJavaScript(js_script)
            self.web_view.setUrl(QUrl("https://web.whatsapp.com"))
    
    def reload_whatsapp(self):
        if self.web_view:
            self.web_view.reload()
    
    def zoom_in(self):
        """Increase zoom level"""
        if self.web_view:
            self.zoom_level = min(self.zoom_level + 0.1, 3.0)  # Max 300%
            self.apply_zoom()
    
    def zoom_out(self):
        """Decrease zoom level"""
        if self.web_view:
            self.zoom_level = max(self.zoom_level - 0.1, 0.5)  # Min 50%
            self.apply_zoom()
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        if self.web_view:
            self.zoom_level = 1.0
            self.apply_zoom()
    
    def apply_zoom(self):
        """Apply current zoom level to webview"""
        if self.web_view:
            self.web_view.setZoomFactor(self.zoom_level)
            zoom_percent = int(self.zoom_level * 100)
            print(f"Zoom set to {zoom_percent}% for {self.name}")
            
            # Auto-save zoom level to database
            if self.db:
                try:
                    self.db.update_zoom_level(self.account_id, self.zoom_level)
                    print(f"Zoom level saved: {zoom_percent}%")
                except Exception as e:
                    print(f"Error saving zoom level: {e}")
    
    def get_zoom_level(self):
        """Get current zoom level for saving"""
        return self.zoom_level
    
    def show_lock_screen(self, parent_layout):
        """Show lock screen overlay"""
        from PyQt6.QtWidgets import QVBoxLayout
        
        self.lock_screen = QWidget()
        lock_layout = QVBoxLayout(self.lock_screen)
        lock_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Lock icon
        lock_icon = QLabel("🔒")
        lock_icon.setStyleSheet("font-size: 72px;")
        lock_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock_layout.addWidget(lock_icon)
        
        # Title
        lock_title = QLabel(f"{self.name}")
        lock_title.setStyleSheet("font-size: 20px; color: white; font-weight: bold; margin-top: 20px;")
        lock_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock_layout.addWidget(lock_title)
        
        # Subtitle
        lock_subtitle = QLabel("This tab is locked")
        lock_subtitle.setStyleSheet("font-size: 14px; color: #aaa; margin-top: 10px; margin-bottom: 30px;")
        lock_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock_layout.addWidget(lock_subtitle)
        
        # Unlock button
        unlock_btn = QPushButton("🔓 Unlock")
        unlock_btn.setFixedSize(150, 40)
        unlock_btn.setStyleSheet("""
            QPushButton {
                background-color: #00a884;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #06cf9c;
            }
            QPushButton:pressed {
                background-color: #008f6d;
            }
        """)
        unlock_btn.clicked.connect(self.unlock_with_password)
        lock_layout.addWidget(unlock_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.lock_screen.setStyleSheet("background-color: #0b141a;")
        parent_layout.addWidget(self.lock_screen)
    
    def toggle_lock(self):
        """Toggle lock/unlock state"""
        if self.is_locked:
            # Try to unlock
            self.unlock_with_password()
        else:
            # Lock immediately
            self.lock_tab()
    
    def unlock_with_password(self):
        """Prompt for password and unlock if correct"""
        if not self.has_password:
            # No password set, just unlock
            self.unlock_tab()
            return
        
        password, ok = QInputDialog.getText(
            self,
            "Unlock Tab",
            f"Enter password for '{self.name}':",
            QLineEdit.EchoMode.Password
        )
        
        if ok:
            if self.db and self.db.verify_password(self.account_id, password):
                # Correct password
                self.unlock_tab()
            else:
                # Wrong password
                QMessageBox.warning(
                    self,
                    "Wrong Password",
                    "The password you entered is incorrect."
                )
    
    def lock_tab(self):
        """Lock the tab"""
        try:
            self.is_locked = True
            
            # Hide webview
            if self.web_view:
                self.web_view.hide()
            
            # Show or create lock screen
            if self.lock_screen:
                # Lock screen already exists, just show it
                self.lock_screen.show()
            else:
                # Create lock screen
                layout = self.layout()
                if layout:
                    self.show_lock_screen(layout)
                else:
                    print(f"WARNING: No layout found for {self.name}")
            
            print(f"Tab locked: {self.name}")
        except Exception as e:
            print(f"ERROR in lock_tab: {e}")
            import traceback
            traceback.print_exc()
    
    def unlock_tab(self):
        """Unlock the tab"""
        try:
            self.is_locked = False
            
            # Hide lock screen
            if self.lock_screen:
                self.lock_screen.hide()
            
            # Show or create webview
            if self.web_view:
                # Webview already exists, just show it
                self.web_view.show()
                print(f"Tab unlocked: {self.name} (webview shown)")
            else:
                # Webview doesn't exist, create it
                print(f"Creating webview for {self.name}...")
                self.create_webview()
                
                if self.web_view:
                    # Add to layout
                    self.layout().addWidget(self.web_view)
                    self.web_view.show()
                    
                    # Load WhatsApp
                    self.load_whatsapp()
                    
                    # Apply zoom
                    self.apply_zoom()
                    
                    print(f"Tab unlocked: {self.name} (webview created)")
                else:
                    print(f"ERROR: Failed to create webview for {self.name}")
                    # Show error and re-lock
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to load WhatsApp Web for {self.name}.\nPlease try again."
                    )
                    self.lock_tab()
        except Exception as e:
            print(f"ERROR in unlock_tab: {e}")
            import traceback
            traceback.print_exc()
            # Try to recover by locking again
            self.is_locked = True
            self.lock_btn.setText("🔒")
            self.update_lock_button_tooltip()
    
    def update_lock_button_tooltip(self):
        """Update lock button tooltip"""
        if self.has_password:
            if self.is_locked:
                self.lock_btn.setToolTip("Unlock (Enter password)")
            else:
                self.lock_btn.setToolTip("Lock this tab")
        else:
            self.lock_btn.setToolTip("Set password to enable lock")
    
    def cleanup(self):
        """Cleanup webview resources safely"""
        try:
            if self.web_view:
                # Load blank page first
                self.web_view.setUrl(QUrl("about:blank"))
                # Stop loading
                self.web_view.stop()
                # Clear page
                if self.web_view.page():
                    self.web_view.page().deleteLater()
                # Schedule deletion
                self.web_view.deleteLater()
                self.web_view = None
                print(f"WebView cleanup successful for {self.name}")
        except Exception as e:
            print(f"Error in cleanup for {self.name}: {e}")
