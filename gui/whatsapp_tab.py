from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QInputDialog, QMessageBox, QGraphicsBlurEffect
from PyQt6.QtCore import QUrl, Qt, QTimer
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
        self.profile = None
        self.is_loading = False
        self.web_view = None
        self.lock_screen = None
        
        try:
            self.setup_ui()
            self.setup_shortcuts()
            
            if not self.is_locked and self.web_view:
                QTimer.singleShot(200, self.load_whatsapp)
                
        except Exception as e:
            print(f"ERROR initializing tab {name}: {e}")
            raise
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.web_view = None
        self.lock_screen = None
        
        if self.is_locked:
            self.show_lock_screen()
        else:
            self.create_webview()
            if self.web_view:
                layout.addWidget(self.web_view)
                self.apply_zoom()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        QShortcut(QKeySequence("Ctrl++"), self).activated.connect(self.zoom_in)
        QShortcut(QKeySequence("Ctrl+="), self).activated.connect(self.zoom_in)
        QShortcut(QKeySequence("Ctrl+-"), self).activated.connect(self.zoom_out)
        QShortcut(QKeySequence("Ctrl+0"), self).activated.connect(self.reset_zoom)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.reload_whatsapp)
        QShortcut(QKeySequence("Ctrl+R"), self).activated.connect(self.reload_whatsapp)
    
    def create_webview(self):
        try:
            if self.profile:
                self.profile.deleteLater()
                self.profile = None
            
            import gc, time
            gc.collect()
            
            profile_name = f"profile_{self.account_id}_{int(time.time() * 1000)}"
            self.profile = QWebEngineProfile(profile_name, None)
            self.profile.setPersistentStoragePath(self.session_dir)
            self.profile.setCachePath(os.path.join(self.session_dir, "cache"))
            self.profile.setHttpCacheMaximumSize(100 * 1024 * 1024)
            
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            self.profile.setHttpUserAgent(user_agent)
            
            settings = self.profile.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.TouchIconsEnabled, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True)
            
            page = QWebEnginePage(self.profile, self)
            page.loadFinished.connect(self.on_page_loaded)
            page.renderProcessTerminated.connect(self.on_render_process_terminated)
            
            self.web_view = QWebEngineView(self)
            self.web_view.setPage(page)
            
            from PyQt6.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            
        except Exception as e:
            print(f"ERROR creating webview for {self.name}: {e}")
            self.web_view = None
    
    def on_page_loaded(self, ok):
        """Called when page finishes loading"""
        if ok and self.web_view:
            js_script = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """
            self.web_view.page().runJavaScript(js_script)
    
    def on_render_process_terminated(self, terminationStatus, exitCode):
        """Called when render process crashes"""
        from PyQt6.QtWebEngineCore import QWebEnginePage
        
        status_names = {
            QWebEnginePage.RenderProcessTerminationStatus.NormalTerminationStatus: "Normal",
            QWebEnginePage.RenderProcessTerminationStatus.AbnormalTerminationStatus: "Abnormal",
            QWebEnginePage.RenderProcessTerminationStatus.CrashedTerminationStatus: "Crashed",
            QWebEnginePage.RenderProcessTerminationStatus.KilledTerminationStatus: "Killed"
        }
        status_name = status_names.get(terminationStatus, "Unknown")
        
        if terminationStatus != QWebEnginePage.RenderProcessTerminationStatus.NormalTerminationStatus:
            QTimer.singleShot(2000, self.reload_whatsapp)
        else:
            QMessageBox.warning(
                self,
                "WhatsApp Web Crashed",
                f"WhatsApp Web for '{self.name}' has crashed.\n\n"
                f"Status: {status_name}\n"
                f"Exit Code: {exitCode}\n\n"
                "The page will reload automatically in 2 seconds."
            )
    
    def load_whatsapp(self):
        if self.web_view and not self.is_loading:
            try:
                self.is_loading = True
                self.web_view.setUrl(QUrl("https://web.whatsapp.com"))
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Loading Failed",
                    f"Failed to load WhatsApp Web for '{self.name}'.\n\n"
                    f"Error: {str(e)}\n\n"
                    "Try reloading or reducing the number of active accounts."
                )
            finally:
                QTimer.singleShot(3000, lambda: setattr(self, 'is_loading', False))
    
    def reload_whatsapp(self):
        if self.web_view:
            self.web_view.reload()
    
    def zoom_in(self):
        if self.web_view:
            self.zoom_level = min(self.zoom_level + 0.1, 3.0)
            self.apply_zoom()
    
    def zoom_out(self):
        if self.web_view:
            self.zoom_level = max(self.zoom_level - 0.1, 0.5)
            self.apply_zoom()
    
    def reset_zoom(self):
        if self.web_view:
            self.zoom_level = 1.0
            self.apply_zoom()
    
    def apply_zoom(self):
        if self.web_view:
            self.web_view.setZoomFactor(self.zoom_level)
            if self.db:
                self.db.update_zoom_level(self.account_id, self.zoom_level)
    
    def get_zoom_level(self):
        return self.zoom_level
    
    def show_lock_screen(self, parent_layout=None):
        if self.lock_screen:
            self.lock_screen.show()
            if self.web_view:
                self.apply_blur_effect(True)
            return
        
        from PyQt6.QtWidgets import QVBoxLayout
        
        self.lock_screen = QWidget(self)
        self.lock_screen.setObjectName("lockScreen")
        lock_layout = QVBoxLayout(self.lock_screen)
        lock_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock_layout.setContentsMargins(20, 20, 20, 20)
        
        # Lock icon with glow effect
        lock_icon = QLabel("🔒")
        lock_icon.setStyleSheet("""
            font-size: 72px;
            background: transparent;
            color: white;
        """)
        lock_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock_layout.addWidget(lock_icon)
        
        # Title
        lock_title = QLabel(f"{self.name}")
        lock_title.setStyleSheet("""
            font-size: 24px;
            color: white;
            font-weight: bold;
            margin-top: 20px;
            background: transparent;
        """)
        lock_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock_layout.addWidget(lock_title)
        
        # Subtitle
        lock_subtitle = QLabel("This tab is locked")
        lock_subtitle.setStyleSheet("""
            font-size: 14px;
            color: #aaa;
            margin-top: 10px;
            margin-bottom: 30px;
            background: transparent;
        """)
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
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
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
        
        self.lock_screen.setStyleSheet("""
            #lockScreen {
                background-color: rgba(11, 20, 26, 0.85);
            }
        """)
        
        self.lock_screen.setGeometry(0, 0, self.width(), self.height())
        self.lock_screen.show()
        self.lock_screen.raise_()
        
        if self.web_view:
            self.apply_blur_effect(True)
    
    def apply_blur_effect(self, enable=True):
        if self.web_view:
            if enable:
                blur_effect = QGraphicsBlurEffect()
                blur_effect.setBlurRadius(10)
                self.web_view.setGraphicsEffect(blur_effect)
            else:
                self.web_view.setGraphicsEffect(None)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.lock_screen and self.lock_screen.isVisible():
            self.lock_screen.setGeometry(0, 0, self.width(), self.height())
    
    def toggle_lock(self):
        if self.is_locked:
            self.unlock_with_password()
        else:
            self.lock_tab()
    
    def unlock_with_password(self):
        if not self.has_password:
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
                self.unlock_tab()
            else:
                QMessageBox.warning(self, "Wrong Password", "The password you entered is incorrect.")
    
    def lock_tab(self):
        self.is_locked = True
        
        if self.web_view:
            self.web_view.show()
        
        if not self.lock_screen:
            self.show_lock_screen()
        else:
            self.lock_screen.setGeometry(0, 0, self.width(), self.height())
            self.lock_screen.show()
            self.lock_screen.raise_()
            if self.web_view:
                self.apply_blur_effect(True)
    
    def unlock_tab(self):
        self.is_locked = False
        
        if self.web_view:
            self.apply_blur_effect(False)
        
        if self.lock_screen:
            self.lock_screen.hide()
        
        if self.web_view:
            self.web_view.show()
        else:
            self.create_webview()
            
            if self.web_view:
                self.layout().addWidget(self.web_view)
                self.web_view.show()
                self.apply_zoom()
                QTimer.singleShot(100, self.load_whatsapp)
            else:
                QMessageBox.critical(self, "Error", f"Failed to load WhatsApp Web for {self.name}.\nPlease try again.")
                self.lock_tab()
    
    def cleanup(self):
        if self.web_view:
            self.web_view.setUrl(QUrl("about:blank"))
            self.web_view.stop()
            
            from PyQt6.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            
            if self.web_view.page():
                page = self.web_view.page()
                self.web_view.setPage(None)
                page.deleteLater()
            
            self.web_view.deleteLater()
            self.web_view = None
        
        if self.profile:
            profile_to_delete = self.profile
            self.profile = None
            QTimer.singleShot(1000, lambda: profile_to_delete.deleteLater())
