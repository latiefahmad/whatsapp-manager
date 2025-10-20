import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    # Set Chromium flags for stability AND balanced memory optimization
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
        "--disable-gpu-process-crash-limit "
        "--disable-features=RendererCodeIntegrity "
        "--no-sandbox "
        "--disable-setuid-sandbox "
        "--disable-dev-shm-usage "
        # Memory optimization flags (balanced)
        "--disable-extensions "
        "--disable-breakpad "
        "--disable-component-extensions-with-background-pages "
        "--disable-features=TranslateUI "
        "--no-first-run "
        "--no-default-browser-check "
        "--disable-sync "
        # Limit processes and memory (512MB per renderer)
        "--renderer-process-limit=3 "
        "--js-flags=--max-old-space-size=512"
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("WhatsApp Manager")
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
