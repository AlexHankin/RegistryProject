# -*- mode: python -*-

block_cipher = None


a = Analysis(['OGRE.py'],
             #pathex=['C:\\Users\\sloane\\Documents\\RegistryProject'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          Tree('..\\RegistryProject\\img','prefix=img\\'),
          a.zipfiles,
          a.datas,
          [],
          name='OGRE',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='.\\img\\northland.ico')
