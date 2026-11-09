import cv2
import time
import keyboard
import io
from PIL import Image
import win32clipboard

# 你的 OBS 虚拟摄像头设备索引（根据刚才的成功经验，这里是 2）
CAP_INDEX = 2  
cap = cv2.VideoCapture(CAP_INDEX, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print(f"[错误] 无法打开设备 (索引: {CAP_INDEX})！")
    exit(1)

print(f"[系统] 虚拟摄像头连接成功！(Device Index: {CAP_INDEX})")
print("[操作] 在任意界面按下快捷键: [ F8 ] 即可一键截图并复制到剪贴板！")
print("[退出] 在预览窗口中按 [Esc] 键可安全退出程序。\n")

def image_to_clipboard(cv_img):
    """将 OpenCV 的 numpy 图像转换为位图并写入 Windows 剪贴板"""
    try:
        # 1. OpenCV 默认是 BGR，转换为 RGB 的 PIL 图像
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(rgb_image)
        
        # 2. 将 PIL 图像转换为 Windows DIB (Device Independent Bitmap) 格式
        output = io.BytesIO()
        pil_im.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]  # 去除 BMP 文件头部 14 字节
        output.close()
        
        # 3. 写入剪贴板
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print(f"[错误] 写入剪贴板失败: {e}")
        return false

def handle_screenshot():
    print("\n[捕获] 收到 F8 触发，正在截取当前帧并写入剪贴板...")
    
    # 连续读取几帧清空缓冲区，确保拿到最新画面
    for _ in range(3):
        ret, frame = cap.read()
    
    if not ret or frame is None:
        print("[错误] 抓取画面失败！")
        return

    # 复制到剪贴板
    if image_to_clipboard(frame):
        print("[成功] 截图已成功复制到剪贴板！")
        print("       (现在你只需直接在网页版 Gemini 输入框按 [Ctrl + V] 即可粘贴！)\n")

# 注册全局热键为 F8
keyboard.add_hotkey('F8', handle_screenshot)

# 主循环：保持预览窗口开启并监听热键
try:
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Capture Preview (Press ESC to quit)", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("[系统] 程序已安全关闭。")