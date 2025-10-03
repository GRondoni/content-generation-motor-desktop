# -*- mode: python ; coding: utf-8 -*-
import os
project_root = os.path.abspath(os.path.dirname(__file__))
block_cipher = None

a = Analysis(
    ['desktop_app.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        # include the entire app/ folder
        (os.path.join(project_root, 'app'), 'app'),
        # include .env if present
        (os.path.join(project_root, '.env'), '.')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ContentGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True
)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name='ContentGenerator')