import tkinter as tk
from tkinter import font as tkfont
import math

class SmartCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("智能中学生计算器")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)
        
        # 创建自定义字体
        self.display_font = tkfont.Font(family="Arial", size=18, weight="bold")
        self.button_font = tkfont.Font(family="Arial", size=12, weight="bold")
        
        # 创建显示区域
        self.create_display()
        
        # 创建按钮区域
        self.create_buttons()
        
        # 初始化表达式
        self.expression = ""
        
    def create_display(self):
        # 创建显示框
        self.display_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.display_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
        
        self.display = tk.Entry(
            self.display_frame, 
            width=25, 
            borderwidth=5, 
            font=self.display_font,
            justify="right",
            bg="#e6f7ff",
            fg="#000000",
            relief=tk.SUNKEN
        )
        self.display.pack(fill=tk.X, padx=5, pady=5)
        
        # 添加说明标签
        self.info_label = tk.Label(
            self.display_frame, 
            text="支持基本运算和科学计算 (如: sin(30), log(100), sqrt(9))", 
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#555555"
        )
        self.info_label.pack(side=tk.BOTTOM, anchor=tk.E, padx=5)
    
    def create_buttons(self):
        # 按钮配置
        buttons = [
            ['sin', 'cos', 'tan', 'log', 'C'],
            ['7', '8', '9', '+', 'sqrt'],
            ['4', '5', '6', '-', '^'],
            ['1', '2', '3', '*', '('],
            ['0', '.', '=', '/', ')']
        ]
        
        # 创建按钮网格
        for i, row in enumerate(buttons):
            for j, char in enumerate(row):
                if char == 'C':
                    btn = tk.Button(
                        self.root, 
                        text=char, 
                        padx=20, 
                        pady=10, 
                        font=self.button_font,
                        bg="#ff9999",
                        activebackground="#ff6666",
                        command=self.clear
                    )
                elif char == '=':
                    btn = tk.Button(
                        self.root, 
                        text=char, 
                        padx=20, 
                        pady=10, 
                        font=self.button_font,
                        bg="#4CAF50",
                        activebackground="#45a049",
                        command=self.calculate
                    )
                elif char in ['sin', 'cos', 'tan', 'log', 'sqrt']:
                    btn = tk.Button(
                        self.root, 
                        text=char, 
                        padx=15, 
                        pady=10, 
                        font=self.button_font,
                        bg="#e6e6fa",
                        activebackground="#d8bfd8",
                        command=lambda c=char: self.button_click(f"{c}(")
                    )
                elif char in ['+', '-', '*', '/', '(', ')', '.', '^']:
                    btn = tk.Button(
                        self.root, 
                        text=char, 
                        padx=20, 
                        pady=10, 
                        font=self.button_font,
                        bg="#e6e6e6",
                        activebackground="#d9d9d9",
                        command=lambda c=char: self.button_click(c)
                    )
                else:
                    btn = tk.Button(
                        self.root, 
                        text=char, 
                        padx=20, 
                        pady=10, 
                        font=self.button_font,
                        bg="#ffffff",
                        activebackground="#f0f0f0",
                        command=lambda c=char: self.button_click(c)
                    )
                
                btn.grid(row=i+1, column=j, padx=2, pady=2, sticky="nsew")
        
        # 配置网格权重
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
    
    def button_click(self, char):
        """处理按钮点击事件"""
        self.expression += char
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
    
    def clear(self):
        """清除显示内容"""
        self.expression = ""
        self.display.delete(0, tk.END)
    
    def calculate(self):
        """计算表达式结果"""
        try:
            # 预处理表达式
            expr = self.expression
            
            # 替换科学函数
            expr = expr.replace('sin(', 'math.sin(math.radians(')
            expr = expr.replace('cos(', 'math.cos(math.radians(')
            expr = expr.replace('tan(', 'math.tan(math.radians(')
            expr = expr.replace('log(', 'math.log10(')
            expr = expr.replace('sqrt(', 'math.sqrt(')
            expr = expr.replace('^', '**')
            
            # 添加闭合括号（简单处理）
            open_parens = expr.count('(')
            close_parens = expr.count(')')
            expr += ')' * (open_parens - close_parens)
            
            # 计算结果
            result = eval(expr, {"__builtins__": None}, {"math": math})
            
            # 格式化结果
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 8)
            
            # 显示结果
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.expression = str(result)
            
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, f"错误: {str(e)}")
            self.expression = ""

# 创建主窗口
root = tk.Tk()
root.geometry("350x400")

# 创建计算器实例
calculator = SmartCalculator(root)

# 运行主循环
root.mainloop()
