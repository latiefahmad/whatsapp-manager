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
        # Limit processes and memory (increased for multiple accounts)
        "--renderer-process-limit=15 "
        "--js-flags=--max-old-space-size=768 "
        # Prevent shared worker crashes
        "--disable-shared-workers "
        # Enable process-per-site for better isolation
        "--process-per-site "
        # GPU and rendering stability (critical for QR code loading)
        "--disable-software-rasterizer "
        "--ignore-gpu-blocklist "
        "--enable-gpu-rasterization "
        # Prevent renderer crashes during heavy loads
        "--disable-hang-monitor "
        "--disable-prompt-on-repost "
        # Canvas and WebGL stability for QR codes
        "--enable-webgl "
        "--enable-accelerated-2d-canvas "
        # Process crash recovery
        "--disable-renderer-backgrounding "
        "--disable-background-timer-throttling "
        "--disable-backgrounding-occluded-windows"
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("WhatsApp Manager")
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
