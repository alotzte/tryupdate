import PyInstaller.__main__

PyInstaller.__main__.run([
    'updater.py',
    '--onefile',
    '--collect-all=pygit2'
])

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--collect-all=pygit2'
])