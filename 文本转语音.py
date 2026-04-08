# -*- coding: utf-8 -*-
import subprocess
import sys

# ===================== 自动修复依赖 =====================
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
except:
    print("正在修复 tkinter...")

# 自动安装依赖
try:
    from qwen_tts import Qwen3TTSModel
except:
    print("正在安装依赖...")
    subprocess.run([
        r"D:\python1128\python.exe", "-m", "pip", "install",
        "qwen-tts", "torch", "soundfile", "torchaudio", "--upgrade",
        "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
    ])

# ===================== 正式导入 =====================
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import time
import soundfile as sf
from qwen_tts import Qwen3TTSModel

# ===================== 配置 =====================
MODEL_PATH = r"D:\Qwen3-TTS"
SAVE_DIR = "声音"

# ===================== 加载模型（修复版） =====================
print("正在加载模型，请稍候...")
model_ready = False
try:
    model = Qwen3TTSModel.from_pretrained(
        MODEL_PATH,
        device_map="auto",
        trust_remote_code=True
    )
    model_ready = True
    print("✅ 模型加载成功！")
except Exception as e:
    print(f"❌ 模型加载失败：{e}")

# ===================== 音色列表 =====================
VOICE_OPTIONS = [
    "tongtong (彤彤)",
    "chuichui (锤锤)",
    "xiaochen (小陈)",
    "jam (动物圈jam)",
    "kazi (动物圈kazi)",
    "douji (动物圈douji)",
    "luodo (动物圈luodo)",
    "male (男声)",
    "female (女声)"
]

def get_voice_code(s):
    return s.split()[0]

# ===================== 生成语音 =====================
def generate_voice():
    if not model_ready:
        messagebox.showerror("错误", "模型未加载成功")
        return

    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("提示", "请输入文本")
        return

    voice = get_voice_code(voice_combo.get())
    btn.config(state=tk.DISABLED, text="生成中...")
    root.update()

    try:
        wav, sr = model.generate(text=text, voice=voice, language="zh")
        os.makedirs(SAVE_DIR, exist_ok=True)
        filename = f"{SAVE_DIR}/语音_{time.strftime('%Y%m%d_%H%M%S')}.wav"
        sf.write(filename, wav, sr)
        messagebox.showinfo("成功", f"已保存：\n{filename}")
    except Exception as e:
        messagebox.showerror("失败", str(e))
    finally:
        btn.config(state=tk.NORMAL, text="🎧 生成语音")

# ===================== GUI界面 =====================
root = tk.Tk()
root.title("Qwen3-TTS 离线文本转语音")
root.geometry("620x460")

ttk.Label(root, text="选择音色：").place(x=20, y=20)
voice_combo = ttk.Combobox(root, values=VOICE_OPTIONS, state="readonly", width=35)
voice_combo.place(x=110, y=20)
voice_combo.current(0)

ttk.Label(root, text="输入文本：").place(x=20, y=60)
text_input = scrolledtext.ScrolledText(root, width=70, height=18)
text_input.place(x=20, y=90)
text_input.insert("1.0", "你好，欢迎使用离线版Qwen3-TTS！")

btn = tk.Button(root, text="🎧 生成语音", command=generate_voice,
                bg="#1E90FF", fg="white", font=("微软雅黑", 12, "bold"))
btn.place(x=230, y=400, width=180, height=40)

tk.Label(root, text=f"音频保存到：{SAVE_DIR} 文件夹", fg="gray").place(x=20, y=430)

root.mainloop()