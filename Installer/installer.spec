# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['installer.py'],
    pathex=[],
    binaries=[],

datas=[
    ('inky_banner.png', 'assets'),
    ('gghq.ico', 'assets'),
],
    hiddenimports=['PIL', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Inky500Installer',
    icon='gghq.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)
