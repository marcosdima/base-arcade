# -*- mode: python ; coding: utf-8 -*-

import os

project_root = os.path.abspath(".")

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        (os.path.join(project_root, 'assets'), 'assets'),
    ],
    hiddenimports=["arcade"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name='main',
)