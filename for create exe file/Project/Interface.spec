# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Interface.py'],
    pathex=[],
    binaries=[],
    datas=[('.\\PoseModule.py', '.'), ('.\\Hand_Detecter.py', '.'), ('.\\Global_Use.py', '.'), ('.\\Jumping_Jacks.py', '.'), ('.\\Leg_Raises.py', '.'), ('.\\Push_Up.py', '.'), ('.\\Sit_Ups.py', '.'), ('.\\Squat.py', '.'), ('C:/Users/daniel/AppData/Local/Programs/Python/Python310/Lib/site-packages/mediapipe/modules', './mediapipe/modules')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Interface',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
