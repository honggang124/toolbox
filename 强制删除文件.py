import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

def force_delete():
    path = entry_path.get().strip()
    if not path:
        messagebox.showwarning("提示", "请先粘贴要删除的路径")
        return

    if not os.path.exists(path):
        messagebox.showerror("错误", "路径不存在")
        return

    try:
        # 1. 获取所有权
        subprocess.run(
            ["takeown", "/f", path, "/r", "/d", "y"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # 2. 赋予权限
        subprocess.run(
            ["icacls", path, "/grant", "*S-1-3-4:F", "/t"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        subprocess.run(
            ["icacls", path, "/grant", "Administrators:F", "/t"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # 3. 强制删除
        if os.path.isdir(path):
            subprocess.run(
                ["rmdir", "/s", "/q", path],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            subprocess.run(
                ["del", "/f", "/s", "/q", path],
                creationflags=subprocess.CREATE_NO_WINDOW
            )

        messagebox.showinfo("成功", "已强制删除！")
        entry_path.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("失败", f"删除出错：{str(e)}")

# ==================== GUI 界面 ====================
root = tk.Tk()
root.title("强制删除工具 - 无需权限")
root.geometry("550x160")
root.resizable(False, False)

frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="粘贴 文件/文件夹 完整路径：", font=("微软雅黑", 10)).grid(row=0, column=0, sticky="w")

entry_path = ttk.Entry(frame, font=("微软雅黑", 10))
entry_path.grid(row=1, column=0, pady=8, sticky="ew", columnspan=2)

btn_del = ttk.Button(frame, text="强制删除", command=force_delete)
btn_del.grid(row=2, column=0, pady=10, sticky="ew", columnspan=2)

frame.columnconfigure(0, weight=1)

root.mainloop()