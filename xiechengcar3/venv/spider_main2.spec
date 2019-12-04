# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

SETUP_DIR = 'C:\\Users\\admin\\PycharmProjects\\spider\\xiechengcar3\\venv\\Include\\xiechengcar_spider\\'
a = Analysis(['C:\\Users\\admin\\PycharmProjects\\spider\\xiechengcar3\\venv\\Include\\xiechengcar_spider\\core\\spider_main.py',
               'C:\\Users\\admin\\PycharmProjects\\spider\\xiechengcar3\\venv\\Include\\xiechengcar_spider\\utils\\excute_spider.py',
              'C:\\Users\\admin\\PycharmProjects\\spider\\xiechengcar3\\venv\\Include\\xiechengcar_spider\\utils\\ipool_utils.py',
              'C:\\Users\\admin\\PycharmProjects\\spider\\xiechengcar3\\venv\\Include\\xiechengcar_spider\\logs\\spider_log.py'],
             pathex=['C:\\Users\\admin\\PycharmProjects\\spider\\xiechengcar3\\venv'],
             binaries=[],
             datas=[(SETUP_DIR+'logs','logs'),(SETUP_DIR+'docs','docs'),('C:\\Users\\admin\\PycharmProjects\\spider\\xiechengcar3\\venv\\Lib\\site-packages','lib\\site-packages')],
             hiddenimports=['requests','json','time','execjs','random','os','csv',
             'threading','datetime','bs4','logging'],
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
          [],
          exclude_binaries=True,
          name='spider_main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='spider_main')