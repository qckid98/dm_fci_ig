# -*- mode: python ; coding: utf-8 -*-

from kivymd import hooks_path as kivymd_hooks_path
from kivy_deps import sdl2, glew
import os
import sys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import shutil
import requests
import zipfile
import io

block_cipher = None

# Get the absolute path to the project root
project_root = os.path.abspath(os.getcwd())

# Create a directory for Chromium if it doesn't exist
chromium_dir = os.path.join(project_root, 'chromium')
if not os.path.exists(chromium_dir):
    os.makedirs(chromium_dir)

# Download specific version of ChromeDriver
chrome_driver_dir = os.path.join(chromium_dir, 'chromedriver')
if not os.path.exists(chrome_driver_dir):
    os.makedirs(chrome_driver_dir)

# Use a specific version of ChromeDriver that exists
chrome_driver_version = "114.0.5735.90"  # This version is known to exist
chrome_driver_url = f"https://chromedriver.storage.googleapis.com/{chrome_driver_version}/chromedriver_win32.zip"

try:
    # Download ChromeDriver
    response = requests.get(chrome_driver_url)
    response.raise_for_status()
    
    # Extract the zip file
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall(chrome_driver_dir)
    
    chrome_driver_path = os.path.join(chrome_driver_dir, "chromedriver.exe")
except Exception as e:
    print(f"Error downloading ChromeDriver: {e}")
    chrome_driver_path = None

a = Analysis(
    [os.path.join(project_root, 'src/main.py')],
    pathex=[project_root],
    binaries=[
        (chrome_driver_path, 'chromium/chromedriver') if chrome_driver_path else [],
    ],
    datas=[
        (os.path.join(project_root, "src/backend/*.py"), "backend"),
        (os.path.join(project_root, "src/ui/accountselectscreen/*.*"), "ui\\accountselectscreen"),
        (os.path.join(project_root, "src/ui/assets/*.png"), "ui\\assets"),
        (os.path.join(project_root, "src/ui/components/*.py"), "ui\\components"),
        (os.path.join(project_root, "src/ui/components/message_components/*.py"), "ui\\components\\message_components"),
        (os.path.join(project_root, "src/ui/messagescreen/*.*"), "ui\\messagescreen"),
        (os.path.join(project_root, "src/ui/welcomescreen/*.*"), "ui\\welcomescreen"),
        (os.path.join(project_root, "src/ui/progressscreen/*.*"), "ui\\progressscreen"),
        (os.path.join(project_root, "assets/*.*"), "assets"),
        (os.path.join(project_root, "chromium"), "chromium"),
    ],
    hiddenimports=[
        'selenium',
        'webdriver_manager',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.chrome.options',
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
        'webdriver_manager.chrome',
        'webdriver_manager.core.os_manager',
        'webdriver_manager.core.download_manager',
        'webdriver_manager.core.http',
        'webdriver_manager.core.utils',
        'kivy',
        'kivymd',
        'kivy.core.window',
        'kivy.core.text',
        'kivy.core.audio',
        'kivy.core.video',
        'kivy.core.image',
        'kivy.core.spelling',
        'kivy.core.clipboard',
        'kivy.core.camera',
        'kivy.core.touch',
        'kivy.core.window.window_sdl2',
        'kivy.core.audio.audio_sdl2',
        'kivy.core.video.video_ffpyplayer',
        'kivy.core.image.img_sdl2',
        'kivy.core.spelling.spelling_enchant',
        'kivy.core.clipboard.clipboard_sdl2',
        'kivy.core.camera.camera_opencv',
        'kivy.core.touch.touch_sdl2',
        'PIL',
        'PIL._imaging',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'PIL.ImageOps',
        'PIL.ImageTk',
        'PIL.ImageEnhance',
        'PIL.ImageFilter',
        'PIL.ImageGrab',
        'PIL.ImageMath',
        'PIL.ImageMorph',
        'PIL.ImagePalette',
        'PIL.ImagePath',
        'PIL.ImageSequence',
        'PIL.ImageStat',
        'PIL.ImageTransform',
        'PIL.ImageWin',
        'PIL.ImageCms',
        'PIL.ImageColor',
        'PIL.ImageFile',
        'PIL.ImageFileIO',
        'PIL.ImageGL',
        'PIL.ImageGrab',
        'PIL.ImageMath',
        'PIL.ImageMorph',
        'PIL.ImageOps',
        'PIL.ImagePalette',
        'PIL.ImagePath',
        'PIL.ImageQt',
        'PIL.ImageSequence',
        'PIL.ImageStat',
        'PIL.ImageTransform',
        'PIL.ImageWin',
        'PIL.PSDraw',
        'PIL.PixarImagePlugin',
        'PIL.PcdImagePlugin',
        'PIL.PcxImagePlugin',
        'PIL.PdfImagePlugin',
        'PIL.PixarImagePlugin',
        'PIL.PngImagePlugin',
        'PIL.PpmImagePlugin',
        'PIL.PsdImagePlugin',
        'PIL.PyAccess',
        'PIL.SunImagePlugin',
        'PIL.TarIO',
        'PIL.TgaImagePlugin',
        'PIL.TiffImagePlugin',
        'PIL.TiffTags',
        'PIL.WalImageFile',
        'PIL.WebPImagePlugin',
        'PIL.WmfImagePlugin',
        'PIL.XbmImagePlugin',
        'PIL.XpmImagePlugin',
        'PIL._binary',
        'PIL._imaging',
        'PIL._imagingagg',
        'PIL._imagingcms',
        'PIL._imagingft',
        'PIL._imaginggif',
        'PIL._imagingjpeg',
        'PIL._imagingmorph',
        'PIL._imagingpng',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'PIL._util',
        'PIL._webp',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'tkinter.colorchooser',
        'tkinter.commondialog',
        'tkinter.constants',
        'tkinter.dnd',
        'tkinter.font',
        'tkinter.scrolledtext',
        'tkinter.tix',
        'tkinter.tkinter',
        'tkinter.tkinter_filedialog',
        'tkinter.tkinter_messagebox',
        'tkinter.tkinter_simpledialog',
        'tkinter.tkinter_colorchooser',
        'tkinter.tkinter_commondialog',
        'tkinter.tkinter_constants',
        'tkinter.tkinter_dnd',
        'tkinter.tkinter_font',
        'tkinter.tkinter_scrolledtext',
        'tkinter.tkinter_tix',
    ],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'pandas', 'scipy',
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'IPython', 'notebook',
        'jupyter', 'qt5', 'qt6', 'PyQt4', 'PySide', 'wx', 'gtk',
        'PyGObject', 'PyGTK', 'PyQt', 'PySide', 'IPython', 'notebook',
        'jupyter', 'qt5', 'qt6', 'PyQt4', 'PySide', 'wx', 'gtk',
        'PyGObject', 'PyGTK', 'PyQt', 'PySide'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

splash = Splash(
    os.path.join(project_root, "src/ui/assets/Splash Screen.png"),
    binaries=a.binaries,
    datas=a.datas,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    splash.binaries,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='MR.DM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, "src/ui/assets/icon.png"),
    version='file_version_info.txt',
    uac_admin=True,
)