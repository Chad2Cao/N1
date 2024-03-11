# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['N0.py'],
    pathex=[],
    binaries=[],
    datas=[('ip_dva.txt','.'),('ip_mp9.txt','.'),('ip_tsp.txt','.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='N0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['light.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='N0',
)
app = BUNDLE(
    coll,
    name='N0.app',
    icon='light.ico',
    bundle_identifier=None,
)
