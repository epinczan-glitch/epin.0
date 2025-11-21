import tkinter as tk
import random
import pygame
import time

# 初始化pygame的音频模块
pygame.mixer.init()

# 预加载音乐文件
try:
    pygame.mixer.music.load(r"C:\CloudMusic\VipSongsDownload\AxR - Daydream.mp3")
    music_loaded = True
except Exception as e:
    print(f"背景音乐加载失败: {e}")
    music_loaded = False

def toggle_music(music_btn):
    """切换音乐播放状态"""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        music_btn.config(text="播放音乐")
    elif music_loaded:
        pygame.mixer.music.play(-1)
        music_btn.config(text="停止音乐")

def generate_key():
    """生成密钥并显示动画"""
    start = random.randint(1, 26)
    end = random.randint(1, 26)
    if start > end: start, end = end, start

    block1 = f"{start:02d}"
    block3 = f"{end:02d}"
    middle = ''.join(chr(ord('A') + random.randint(start, end) - 1) for _ in range(7))
    final_key = f"{block1} {middle} {block3}"

    # 显示动画
    animate_key(final_key)

def animate_key(key):
    """密钥逐字符显示动画"""
    key_label.config(text="")
    for i in range(len(key)):
        key_label.config(text=key[:i + 1])
        key_label.update()
        time.sleep(0.06)

# 创建主窗口
root = tk.Tk()
root.title("Terraria 密钥生成器")
root.geometry("500x350")
root.resizable(False, False)  # 禁止调整窗口大小

# 1. 创建画布（承载背景图，作为所有组件的底层）
canvas = tk.Canvas(root, width=500, height=350)
canvas.pack(fill="both", expand=True)  # 让画布占满窗口

# 2. 加载背景图（支持png/jpg格式）
try:
 # 替换原背景图加载代码中的路径
    bg_photo = tk.PhotoImage(file="C:\Users\zyp92\Desktop\PythonProject\terraria_bg.jpg")
    # 将图片绘制到画布上（从左上角0,0位置开始）
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    # 保留图片引用，防止被Python垃圾回收机制删除
    root.bg_photo = bg_photo
except Exception as e:
    print(f"背景图加载失败：{e}")



# 3. 界面组件（用 canvas.create_window 放在画布上，替代原来的 pack）
# 标题标签
title_label = tk.Label(
    root, text="Terraria 密钥生成系统",
    font=("Arial", 16, "bold"),
    fg="#ffeb3b", bg="#1a237e"
)
canvas.create_window(250, 30, window=title_label)  # (x=250, y=30) 是组件在画布上的位置

# 生成按钮
generate_btn = tk.Button(
    root, text="生成密钥", command=generate_key,
    font=("Arial", 12), bg="#3498db", fg="white",
    padx=20, pady=5
)
canvas.create_window(250, 80, window=generate_btn)

# 密钥显示标签
key_label = tk.Label(
    root, text="-- ------- --",
    font=("Courier New", 16, "bold"),
    fg="#e53935", bg="#000000",
    padx=15, pady=8
)
canvas.create_window(250, 140, window=key_label)

# 规则说明标签
rule_label = tk.Label(
    root, text="格式：XX XXXXXXX XX\n第1/3部分：字母位置(01-26) | 第2部分：区间内随机字母",
    font=("Arial", 9), fg="#e0f7fa", bg="#004d40",
    padx=10, pady=6, justify="center"
)
canvas.create_window(250, 210, window=rule_label)

root.mainloop()

