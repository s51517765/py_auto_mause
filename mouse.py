# pyinstaller --onefile --noconsole --icon="img/ico.ico" mouse.py
import sys
import pyautogui
import time
import random
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QKeyEvent
import keyboard  # 使用するkeyboardライブラリ


# 現在位置情報
posi = pyautogui.position()
posi_max = posi.x if posi else 0
flag = True
interval = 3000  # ms

# 中止フラグ
should_stop = False

exit_keys = [
    "esc",
    "shift",
    "a",
    "i",
    "u",
    "e",
    "o",
]  # キーを追加


# PyQt5 アプリケーションの作成
class MyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

    # キー入力を定期的に監視
    def monitor_keyboard_input(self):
        global should_stop
        for key in exit_keys:
            if keyboard.is_pressed(key):  # 特定のキーが押されたら
                should_stop = True
                print("処理が中止されました")


# アプリケーションのインスタンスを作成
app = MyApp(sys.argv)

# アイコンのパスを絶対パスで設定（これを確認して正しいパスに変更してください）
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
    global posi, posi_max, flag, interval, should_stop

    # 特定のキーが押されていた場合、処理を中止
    if should_stop:
        should_stop = False
    else:
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
    print(f"次の実行まで: {interval / 1000:.2f} 秒")
    timer.start(int(interval))


# QTimer を設定
timer = QTimer()
timer.timeout.connect(check_mouse_position)
timer.start(3000)  # 最初のチェックを3秒後に開始

# もう1つのQTimerでキー入力の監視を定期的に行う
keyboard_timer = QTimer()
keyboard_timer.timeout.connect(app.monitor_keyboard_input)
keyboard_timer.start(100)  # 100msごとにキー入力を監視

# メッセージボックスを表示
msg_box.exec_()

# アプリケーションを実行（これがないとタスクトレイアイコンは表示されません）
app.exec_()
