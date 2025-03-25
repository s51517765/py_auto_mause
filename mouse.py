# pyinstaller --onefile --noconsole --icon="img/ico.ico" mouse.py
import sys
import pyautogui
import time
import random
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

# 現在位置情報
posi = pyautogui.position()
posi_max = posi.x if posi else 0
flag = True

# PyQt5 アプリケーションの作成
app = QApplication(sys.argv)

# システムトレイアイコンを作成
icon_path = "img/ico.jpg"  # アイコンのパス
tray_icon = QSystemTrayIcon(QIcon(icon_path), parent=app)

# コンテキストメニューを作成
menu = QMenu()
exit_action = QAction("終了", app)
exit_action.triggered.connect(app.quit)
menu.addAction(exit_action)

tray_icon.setContextMenu(menu)
tray_icon.show()

# メッセージボックス（アプリケーションが動作していることを通知）
msg_box = QMessageBox()
msg_box.setWindowTitle("マウス監視")
msg_box.setText(
    "スクリプトはバックグラウンドで動作しています。\n終了するには「終了」ボタンをクリックしてください。"
)

# アイコンを設定（カスタムアイコンを指定）
msg_box.setIconPixmap(QIcon(icon_path).pixmap(64, 64))  # カスタムアイコンを設定
msg_box.setStandardButtons(QMessageBox.Ok)


def check_mouse_position():
    global posi, posi_max, flag

    current_pos = pyautogui.position()

    if posi == current_pos:
        if flag:
            pyautogui.moveTo(100, posi.y)
        else:
            pyautogui.moveTo(posi_max - 100, posi.y)
        flag = not flag

        # Shiftキーを押す
        pyautogui.keyDown("shift")
        time.sleep(0.1)
        pyautogui.keyUp("shift")

        # 元の位置に戻る
        pyautogui.moveTo(posi.x, posi.y)
    else:
        posi = current_pos
        posi_max = max(posi_max, posi.x)

    # 次回のチェックをランダムな時間後に実行
    interval = random.uniform(3.0, 10.0) * 1000  # ミリ秒単位
    timer.start(int(interval))


# QTimer を設定
timer = QTimer()
timer.timeout.connect(check_mouse_position)
timer.start(3000)  # 最初のチェックを3秒後に開始

# システムトレイアイコンを表示
# tray_icon.show()

# メッセージボックスを表示
msg_box.exec_()
