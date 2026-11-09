import cv2
import time
import keyboard
from google import genai
from google.genai import types

# 1. 初始化 Gemini 客户端 (自动加载环境变量中的 GEMINI_API_KEY)
client = genai.Client()

# 2. 初始化采集卡视频流
# 如果电脑上有多个摄像头或采集卡，索引可能是 0, 1, 2 等。
CAP_INDEX = 2  
cap = cv2.VideoCapture(CAP_INDEX, cv2.CAP_DSHOW) # Windows系统推荐加 cv2.CAP_DSHOW 提升稳定性

if not cap.isOpened():
    print(f"[错误] 无法打开采集卡设备 (索引: {CAP_INDEX})！请检查 USB 连线或尝试将 CAP_INDEX 改为 1。")
    exit(1)

print(f"[系统] 采集卡连接成功！(Device Index: {CAP_INDEX})")
print("[提示] 程序运行后会弹出一个预览窗口，用于确认采集画面是否正常。")
print("[操作] 在任意界面按下快捷键: [Ctrl + Alt + S] 即可一键截图并让 Gemini 给出答案！")
print("[退出] 在预览窗口中按 [Esc] 键可安全退出程序。\n")

def capture_and_analyze():
    print("\n[捕获] 收到热键触发，正在从采集卡抓取画面...")
    
    # 连续读取几帧清空 OpenCV 缓冲区，确保拿到的是最新画面
    for _ in range(3):
        ret, frame = cap.read()
    
    if not ret or frame is None:
        print("[错误] 读取采集卡画面失败！")
        return

    # 图像编码为 JPEG 格式 (质量设为 90)
    success, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    if not success:
        print("[错误] 图像编码失败！")
        return
    
    image_bytes = buffer.tobytes()
    print("[传输] 正在发送画面至 Gemini 3.8 Flash 模型进行分析...")

    try:
        # 调用最新的 google-genai 视觉能力
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                "请仔细分析这张屏幕截图，找出其中的题目或核心内容，并提供准确、简洁的答案与详细解析："
            ]
        )
        
        print("\n" + "="*50)
        print(" 💡 Gemini 分析结果:")
        print("="*50)
        print(response.text)
        print("="*50 + "\n")

    except Exception as e:
        print(f"[错误] 调用 Gemini API 时发生异常: {e}")

# 3. 注册全局热键监听 (Ctrl + Alt + S)
keyboard.add_hotkey('ctrl+alt+s', capture_and_analyze)

# 4. 主循环：显示实时预览并保持程序运行
try:
    while True:
        ret, frame = cap.read()
        if ret:
            # 实时显示采集卡的画面，方便你随时对准答题笔记本的窗口
            cv2.imshow("Capture Card Live Feed (Press ESC to quit)", frame)
        
        # 检测键盘 ESC 键退出
        if cv2.waitKey(1) & 0xFF == 27:
            break
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("[系统] 程序已安全关闭。")