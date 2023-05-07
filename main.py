import atexit
import os

import pygit2
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton


access_token = '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'


def git_pull(repo_path, remote_name='origin'):
    # Откройте локальный репозиторий
    repo = pygit2.Repository(repo_path)

    # Получите ссылку на удаленный репозиторий
    remote = repo.remotes[remote_name]

    # Создайте объект для аутентификации с помощью токена
    credentials = pygit2.UserPass(username=access_token, password='')

    # Настройте обратные вызовы аутентификации для удаленного репозитория
    remote_callbacks = pygit2.RemoteCallbacks(credentials=credentials)

    # Извлеките изменения из удаленного репозитория
    remote.fetch(callbacks=remote_callbacks)

    # Получите текущую ветку
    current_branch = repo.head.shorthand

    # Получите ссылку на ветку в удаленном репозитории
    remote_branch = f'refs/remotes/{remote_name}/{current_branch}'

    # Получите последний коммит в ветке удаленного репозитория
    remote_commit = repo.lookup_reference(remote_branch).target

    # Извлеките изменения из удаленного репозитория
    remote.fetch()

    # Выполните слияние изменений из удаленного репозитория
    merge_result, _ = repo.merge_analysis(remote_commit)
    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print('Already up to date from main')
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        print('Fast-forwarded from main')
        atexit.register(os.execl("updater.exe", "updater.exe"))
        exit(0)
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print('A normal merge is required. Please handle this case manually from main')
    else:
        print('Unknown merge result. Please handle this case manually from main')


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Пример программы PyQT')
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel(self)
        self.label.setText('v2')
        self.label.move(100, 50)

        self.button = QPushButton(self)
        self.button.setText('Нажми меня')
        self.button.move(100, 100)
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText('Кнопка нажата!')

if __name__ == '__main__':
    # Запустите функцию git_pull с путем к вашему репозиторию и именем удаленного репозитория
    git_pull(os.getcwd(), 'origin')
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
