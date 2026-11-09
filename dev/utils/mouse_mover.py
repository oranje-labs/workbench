import time
import math
import pyautogui

# 防灾安全机制：将鼠标快速甩到屏幕任意四角可强制中断脚本
pyautogui.FAILSAFE = True

print("鼠标【持续连续移动】脚本已启动！")
print("提示：按下 Ctrl+C 或将鼠标迅速甩至屏幕角落可停止脚本。")

# 记录当前鼠标位置作为轨迹中心
center_x, center_y = pyautogui.position()
radius = 40  # 移动轨迹半径（像素）
angle = 0.0

try:
    while True:
        # 使用三角函数计算连续圆周运动轨迹
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # 持续平滑移动至新坐标
        pyautogui.moveTo(x, y, duration=0.01)
        
        # 递增角度控制旋转速度
        angle += 0.1
        if angle >= math.pi * 2:
            angle = 0.0
            
except KeyboardInterrupt:
    print("\n脚本已手动停止。")