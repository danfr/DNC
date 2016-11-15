# -*- mode: python -*-

block_cipher = None


a = Analysis(['setup.py'],
             pathex=['C:\\Users\\DYNAMITE\\Documents\\Visual Studio 2015\\Projects\\DNC42\\client_old'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='setup',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='42.ico')
