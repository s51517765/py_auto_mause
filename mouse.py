# pyinstaller mouse.py --onefile --hide-console hide-early
# exeファイル作成時はウィルス検知を一時的に無効

import pyautogui
import time
import random

posi = None
posi_max = 0
r = 0
flag = True


while True:
    # 現在地取得
    if posi == pyautogui.position():
        if flag:
            # (x, y)の位置にマウスカーソルを移動
            pyautogui.moveTo(100, posi.y)
        else:
            # (x, y)の位置にマウスカーソルを移動
            pyautogui.moveTo(posi_max - 100, posi.y)
        flag = not flag

        # クリック
        # pyautogui.click()
        pyautogui.press("shiftleft")
        time.sleep(0.1)
        pyautogui.keyUp("shiftleft")

        # 元の位置に戻る
        pyautogui.moveTo(posi.x, posi.y)
    else:
        posi = pyautogui.position()
        if posi != None:
            if posi_max < posi.x:
                posi_max = posi.x

    r = random.uniform(3.0, 10.0)
    time.sleep(r)
