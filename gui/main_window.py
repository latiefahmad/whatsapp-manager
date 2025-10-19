from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QTabWidget, QLabel, QInputDialog, QMessageBox, QLineEdit, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from core.database import Database
from gui.whatsapp_tab import WhatsAppTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("WhatsApp Manager - Multi Account")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        self.db = Database()
        self.tabs = {}
        self.welcome_tab = None
        
        self.setup_ui()
        self.apply_styles()
        self.setup_shortcuts()
        self.load_saved_accounts()
        self.show_welcome_if_empty()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Tab widget for multiple WhatsApp accounts (like browser tabs)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)  # Allow drag-drop tabs like browser
        self.tab_widget.setDocumentMode(True)  # Browser-style tabs
        self.tab_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_widget.customContextMenuRequested.connect(self.show_tab_context_menu)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Global controls bar (zoom, lock, reload, add) - all in tab bar
        controls_container = QWidget()
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setContentsMargins(5, 2, 5, 2)
        controls_layout.setSpacing(4)
        
        # Zoom Out button
        self.global_zoom_out_btn = QPushButton("−")
        self.global_zoom_out_btn.setFixedSize(26, 26)
        self.global_zoom_out_btn.setToolTip("Zoom Out (Ctrl+-)")
        self.global_zoom_out_btn.clicked.connect(self.zoom_out_active_tab)
        controls_layout.addWidget(self.global_zoom_out_btn)
        
        # Zoom label (styled like button)
        zoom_label_container = QWidget()
        zoom_label_container.setFixedSize(42, 26)
        zoom_label_container.setStyleSheet("""
            QWidget {
                background-color: #00a884;
                border-radius: 6px;
            }
            QWidget:hover {
                background-color: #06cf9c;
            }
        """)
        zoom_label_layout = QVBoxLayout(zoom_label_container)
        zoom_label_layout.setContentsMargins(0, 0, 0, 0)
        
        self.global_zoom_label = QLabel("100%")
        self.global_zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.global_zoom_label.setToolTip("Click to reset zoom")
        self.global_zoom_label.mousePressEvent = lambda e: self.reset_zoom_active_tab()
        self.global_zoom_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.global_zoom_label.setStyleSheet("color: white; font-size: 10px; font-weight: bold; background: transparent;")
        zoom_label_layout.addWidget(self.global_zoom_label)
        
        controls_layout.addWidget(zoom_label_container)
        
        # Zoom In button
        self.global_zoom_in_btn = QPushButton("+")
        self.global_zoom_in_btn.setFixedSize(26, 26)
        self.global_zoom_in_btn.setToolTip("Zoom In (Ctrl++)")
        self.global_zoom_in_btn.clicked.connect(self.zoom_in_active_tab)
        controls_layout.addWidget(self.global_zoom_in_btn)
        
        # Separator (invisible spacer)
        controls_layout.addSpacing(3)
        
        # Lock/Unlock button
        self.global_lock_btn = QPushButton("🔓")
        self.global_lock_btn.setFixedSize(28, 26)
        self.global_lock_btn.setToolTip("Lock/Unlock tab")
        self.global_lock_btn.clicked.connect(self.toggle_lock_active_tab)
        controls_layout.addWidget(self.global_lock_btn)
        
        # Reload button
        self.global_reload_btn = QPushButton("🔄")
        self.global_reload_btn.setFixedSize(28, 26)
        self.global_reload_btn.setToolTip("Reload (F5)")
        self.global_reload_btn.clicked.connect(self.reload_active_tab)
        controls_layout.addWidget(self.global_reload_btn)
        
        # Separator (invisible spacer)
        controls_layout.addSpacing(3)
        
        # Add account button
        self.add_tab_btn = QPushButton("+")
        self.add_tab_btn.setFixedSize(28, 26)
        self.add_tab_btn.setToolTip("Add New Account (Ctrl+T)")
        self.add_tab_btn.clicked.connect(self.add_account)
        controls_layout.addWidget(self.add_tab_btn)
        
        self.tab_widget.setCornerWidget(controls_container, Qt.Corner.TopRightCorner)
        
        # Update controls when tab changes
        self.tab_widget.currentChanged.connect(self.update_global_controls)
        
        main_layout.addWidget(self.tab_widget)
    
    def setup_shortcuts(self):
        """Setup global keyboard shortcuts"""
        from PyQt6.QtGui import QShortcut, QKeySequence
        
        # Add account: Ctrl+T (like browser new tab)
        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(self.add_account)
        
        # Close tab: Ctrl+W (like browser close tab)
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)
    
    def close_current_tab(self):
        """Close currently active tab"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.close_tab(current_index)
    
    def get_active_tab_widget(self):
        """Get currently active WhatsAppTab widget"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            widget = self.tab_widget.widget(current_index)
            # Check if it's a WhatsAppTab (not welcome tab)
            if hasattr(widget, 'zoom_in'):
                return widget
        return None
    
    def update_global_controls(self):
        """Update global control buttons based on active tab"""
        tab = self.get_active_tab_widget()
        
        if tab:
            # Update zoom label
            zoom_percent = int(tab.zoom_level * 100)
            self.global_zoom_label.setText(f"{zoom_percent}%")
            
            # Update lock button
            if tab.is_locked:
                self.global_lock_btn.setText("🔒")
                self.global_lock_btn.setToolTip("Unlock tab")
            else:
                self.global_lock_btn.setText("🔓")
                if tab.has_password:
                    self.global_lock_btn.setToolTip("Lock tab")
                else:
                    self.global_lock_btn.setToolTip("Set password to enable lock")
            
            # Enable all controls
            self.global_zoom_out_btn.setEnabled(True)
            self.global_zoom_in_btn.setEnabled(True)
            self.global_lock_btn.setEnabled(True)
            self.global_reload_btn.setEnabled(True)
        else:
            # No active tab, disable controls
            self.global_zoom_label.setText("100%")
            self.global_lock_btn.setText("🔓")
            self.global_zoom_out_btn.setEnabled(False)
            self.global_zoom_in_btn.setEnabled(False)
            self.global_lock_btn.setEnabled(False)
            self.global_reload_btn.setEnabled(False)
    
    def zoom_in_active_tab(self):
        """Zoom in active tab"""
        tab = self.get_active_tab_widget()
        if tab:
            tab.zoom_in()
            self.update_global_controls()
    
    def zoom_out_active_tab(self):
        """Zoom out active tab"""
        tab = self.get_active_tab_widget()
        if tab:
            tab.zoom_out()
            self.update_global_controls()
    
    def reset_zoom_active_tab(self):
        """Reset zoom on active tab"""
        tab = self.get_active_tab_widget()
        if tab:
            tab.reset_zoom()
            self.update_global_controls()
    
    def toggle_lock_active_tab(self):
        """Toggle lock on active tab"""
        tab = self.get_active_tab_widget()
        if tab:
            tab.toggle_lock()
            self.update_global_controls()
    
    def reload_active_tab(self):
        """Reload active tab"""
        tab = self.get_active_tab_widget()
        if tab:
            tab.reload_whatsapp()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0b141a;
            }
            
            /* Browser-style tabs - Fresh theme */
            QTabWidget {
                background-color: #1f2c34;
                border: none;
            }
            QTabWidget::pane {
                border: none;
                border-top: none;
                background-color: #0b141a;
                top: 0px;
                margin: 0px;
                padding: 0px;
            }
            QTabBar {
                background-color: #1f2c34;
                border: none;
            }
            QTabBar::tab {
                background-color: #00a884;
                color: white;
                padding: 8px 16px;
                margin-right: 3px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                min-width: 120px;
                max-width: 200px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #0b141a;
                color: white;
                border-bottom: 2px solid #00a884;
            }
            QTabBar::tab:hover:!selected {
                background-color: #06cf9c;
            }
            QTabBar::close-button {
                margin: 2px;
                padding: 0px;
            }
            
            /* Global controls in tab bar - Fresh theme */
            QWidget#controls_container {
                background-color: transparent;
            }
            QWidget#controls_container QPushButton {
                background-color: #00a884;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QWidget#controls_container QPushButton:hover {
                background-color: #06cf9c;
            }
            QWidget#controls_container QPushButton:pressed {
                background-color: #008f6d;
            }
            QWidget#controls_container QPushButton:disabled {
                background-color: #2a3942;
                color: #666;
            }
        """)
    
    def add_account(self):
        name, ok = QInputDialog.getText(
            self, 
            "Add WhatsApp Account",
            "Enter account name:",
            QLineEdit.EchoMode.Normal,
            f"Account {len(self.tabs) + 1}"  # Default name suggestion
        )
        
        if ok and name:
            # Hide welcome tab before adding first account
            self.show_welcome_if_empty()
            
            account_id, session_dir = self.db.add_account(name)
            self.create_account_tab(account_id, name, session_dir)
            
            # Remove welcome tab after adding account
            self.show_welcome_if_empty()
    
    def create_account_tab(self, account_id, name, session_dir, zoom_level=1.0, password_hash=None):
        has_password = password_hash is not None
        tab = WhatsAppTab(account_id, name, session_dir, zoom_level, has_password, self.db)
        # Use emoji only, shorter name for compact tabs
        lock_icon = "🔒 " if has_password else ""
        tab_title = f"{lock_icon}💬 {name}" if len(name) <= 10 else f"{lock_icon}💬 {name[:10]}..."
        index = self.tab_widget.addTab(tab, tab_title)
        self.tab_widget.setCurrentIndex(index)
        
        self.tabs[account_id] = {
            "name": name,
            "widget": tab,
            "index": index
        }
        
        # Update window title with account count
        self.update_window_title()
        
        # Update global controls
        self.update_global_controls()
    
    def close_tab(self, index):
        try:
            # Prevent closing welcome tab
            if self.tab_widget.widget(index) == self.welcome_tab:
                return
            
            if index < 0 or index >= self.tab_widget.count():
                return
            
            # Find account_id for this tab index
            account_id = None
            current_widget = self.tab_widget.widget(index)
            
            for aid, info in self.tabs.items():
                if info["widget"] == current_widget:
                    account_id = aid
                    break
            
            if account_id is None:
                print(f"Warning: No account found for tab index {index}")
                return
            
            name = self.tabs[account_id]["name"]
            
            # Confirmation dialog
            reply = QMessageBox.question(
                self,
                "Remove Account",
                f"Remove '{name}'?\n\n"
                "⚠️ This will:\n"
                "• Close this tab\n"
                "• Delete session data (need to scan QR again)\n"
                "• Remove account from database",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No  # Default to No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                print(f"Removing account: {name} (ID: {account_id})")
                
                # Step 1: Remove from tracking FIRST (prevent re-entry)
                tab_widget = self.tabs[account_id]["widget"]
                del self.tabs[account_id]
                
                # Step 2: Remove from database (deletes session files)
                try:
                    self.db.delete_account(account_id)
                    print(f"Database entry deleted for account {account_id}")
                except Exception as e:
                    print(f"Error deleting from database: {e}")
                
                # Step 3: Remove tab from UI (this triggers close event)
                # Block signals temporarily to prevent recursion
                self.tab_widget.blockSignals(True)
                self.tab_widget.removeTab(index)
                self.tab_widget.blockSignals(False)
                
                # Step 4: Cleanup webview (do this AFTER removing from UI)
                # Note: Zoom level already auto-saved on each zoom change
                try:
                    tab_widget.cleanup()
                    print(f"WebView cleanup completed")
                except Exception as e:
                    print(f"Error during cleanup: {e}")
                
                # Step 5: Update window title
                self.update_window_title()
                
                # Step 6: Show welcome tab if no accounts left
                self.show_welcome_if_empty()
                
                print(f"Account removed successfully. Remaining accounts: {len(self.tabs)}")
        
        except Exception as e:
            print(f"ERROR in close_tab: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to remove account: {str(e)}\n\nPlease restart the application."
            )
    
    def load_saved_accounts(self):
        accounts = self.db.get_all_accounts()
        for account_id, name, session_dir, zoom_level, password_hash in accounts:
            # Use saved zoom level, default to 1.0 if None
            zoom = zoom_level if zoom_level else 1.0
            self.create_account_tab(account_id, name, session_dir, zoom, password_hash)
        self.update_window_title()
    
    def show_welcome_if_empty(self):
        """Show welcome tab when no accounts exist"""
        if len(self.tabs) == 0:
            if self.welcome_tab is None:
                self.welcome_tab = self.create_welcome_tab()
            if self.tab_widget.indexOf(self.welcome_tab) == -1:
                self.tab_widget.addTab(self.welcome_tab, "Welcome")
        else:
            # Remove welcome tab if accounts exist
            if self.welcome_tab is not None:
                index = self.tab_widget.indexOf(self.welcome_tab)
                if index != -1:
                    self.tab_widget.removeTab(index)
    
    def create_welcome_tab(self):
        """Create welcome/empty state tab"""
        welcome = QWidget()
        layout = QVBoxLayout(welcome)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Icon
        icon_label = QLabel("💬")
        icon_label.setStyleSheet("font-size: 64px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title = QLabel("Welcome to WhatsApp Manager")
        title.setStyleSheet("font-size: 24px; color: white; font-weight: bold; margin-top: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Manage multiple WhatsApp accounts in one place")
        subtitle.setStyleSheet("font-size: 14px; color: #aaa; margin-top: 10px; margin-bottom: 30px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Add account button
        add_btn = QPushButton("➕ Add Your First Account")
        add_btn.setFixedSize(220, 45)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #00a884;
                color: white;
                border: none;
                border-radius: 8px;
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
        add_btn.clicked.connect(self.add_account)
        layout.addWidget(add_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Instructions
        instructions = QLabel(
            "📱 Click the button above or the '+' at the top\n"
            "🔐 Each account has its own secure session\n"
            "💾 Sessions are saved automatically"
        )
        instructions.setStyleSheet("font-size: 12px; color: #888; margin-top: 40px; line-height: 1.6;")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
        welcome.setStyleSheet("background-color: #0b141a;")
        return welcome
    
    def update_window_title(self):
        count = len(self.tabs)
        if count == 0:
            self.setWindowTitle("WhatsApp Manager")
        elif count == 1:
            self.setWindowTitle("WhatsApp Manager - 1 account")
        else:
            self.setWindowTitle(f"WhatsApp Manager - {count} accounts")
    
    def show_tab_context_menu(self, position):
        """Show right-click context menu on tab"""
        tab_bar = self.tab_widget.tabBar()
        index = tab_bar.tabAt(position)
        
        if index < 0:
            return
        
        # Get account for this tab
        widget = self.tab_widget.widget(index)
        if widget == self.welcome_tab:
            return
        
        account_id = None
        for aid, info in self.tabs.items():
            if info["widget"] == widget:
                account_id = aid
                break
        
        if not account_id:
            return
        
        # Create context menu
        menu = QMenu(self)
        
        # Set/Change Password
        password_action = QAction("🔑 Set/Change Password", self)
        password_action.triggered.connect(lambda: self.set_tab_password(account_id))
        menu.addAction(password_action)
        
        # Remove Password (if has password)
        if self.db.has_password(account_id):
            remove_password_action = QAction("🔓 Remove Password", self)
            remove_password_action.triggered.connect(lambda: self.remove_tab_password(account_id))
            menu.addAction(remove_password_action)
        
        menu.addSeparator()
        
        # Close tab
        close_action = QAction("❌ Close Tab", self)
        close_action.triggered.connect(lambda: self.close_tab(index))
        menu.addAction(close_action)
        
        # Show menu
        menu.exec(tab_bar.mapToGlobal(position))
    
    def set_tab_password(self, account_id):
        """Set or change password for tab"""
        if account_id not in self.tabs:
            return
        
        name = self.tabs[account_id]["name"]
        
        # Check if already has password
        if self.db.has_password(account_id):
            # Verify old password first
            old_password, ok = QInputDialog.getText(
                self,
                "Change Password",
                f"Enter current password for '{name}':",
                QLineEdit.EchoMode.Password
            )
            
            if not ok:
                return
            
            if not self.db.verify_password(account_id, old_password):
                QMessageBox.warning(
                    self,
                    "Wrong Password",
                    "The current password you entered is incorrect."
                )
                return
        
        # Get new password
        password, ok = QInputDialog.getText(
            self,
            "Set Password",
            f"Enter new password for '{name}':\n(Leave empty to remove password)",
            QLineEdit.EchoMode.Password
        )
        
        if not ok:
            return
        
        if password:
            # Confirm password
            confirm, ok = QInputDialog.getText(
                self,
                "Confirm Password",
                "Confirm password:",
                QLineEdit.EchoMode.Password
            )
            
            if not ok:
                return
            
            if password != confirm:
                QMessageBox.warning(
                    self,
                    "Password Mismatch",
                    "Passwords do not match. Please try again."
                )
                return
            
            # Set password
            self.db.set_password(account_id, password)
            
            # Update tab
            widget = self.tabs[account_id]["widget"]
            widget.has_password = True
            widget.is_locked = True
            widget.lock_tab()
            
            # Update global controls
            self.update_global_controls()
            
            # Update tab title with lock icon
            index = self.tabs[account_id]["index"]
            current_title = self.tab_widget.tabText(index)
            if not current_title.startswith("🔒"):
                self.tab_widget.setTabText(index, "🔒 " + current_title)
            
            QMessageBox.information(
                self,
                "Password Set",
                f"Password has been set for '{name}'.\nTab is now locked."
            )
        else:
            # Remove password
            self.remove_tab_password(account_id)
    
    def remove_tab_password(self, account_id):
        """Remove password from tab"""
        if account_id not in self.tabs:
            return
        
        name = self.tabs[account_id]["name"]
        
        # Confirm removal
        reply = QMessageBox.question(
            self,
            "Remove Password",
            f"Remove password protection from '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove password
            self.db.set_password(account_id, None)
            
            # Update tab
            widget = self.tabs[account_id]["widget"]
            widget.has_password = False
            widget.is_locked = False
            if widget.lock_screen:
                widget.lock_screen.hide()
            if widget.web_view:
                widget.web_view.show()
            
            # Update global controls
            self.update_global_controls()
            
            # Update tab title (remove lock icon)
            index = self.tabs[account_id]["index"]
            current_title = self.tab_widget.tabText(index)
            if current_title.startswith("🔒 "):
                self.tab_widget.setTabText(index, current_title.replace("🔒 ", ""))
            
            QMessageBox.information(
                self,
                "Password Removed",
                f"Password protection removed from '{name}'."
            )
