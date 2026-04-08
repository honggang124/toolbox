# 全国区县天气查询 - 美化版·全中文显示·防闪退·稳定版
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import urllib.request
import urllib.parse
import json

# ==================== 【完整版】天气英文转中文词典（全覆盖wttr.in所有天气） ====================
weather_translate = {
    # 晴/云/阴
    "Sunny": "晴天",
    "Clear": "晴朗",
    "Cloudy": "多云",
    "Partly cloudy": "晴转多云",
    "Overcast": "阴天",
    "Cloudy with sunny intervals": "多云间晴",
    "Sunny intervals": "晴间多云",

    # 雾/霾/沙尘
    "Fog": "雾",
    "Mist": "薄雾",
    "Haze": "雾霾",
    "Smoke": "烟雾",
    "Dust": "浮尘",
    "Sand": "沙尘",
    "Dust storm": "沙尘暴",
    "Sand storm": "沙暴",
    "Blowing sand": "扬沙",

    # 雨类（全等级）
    "Rain": "雨",
    "Light rain": "小雨",
    "Moderate rain": "中雨",
    "Heavy rain": "大雨",
    "Very heavy rain": "暴雨",
    "Extreme rain": "特大暴雨",
    "Patchy rain nearby": "局部零星小雨",
    "Patchy light rain": "局部小雨",
    "Light drizzle": "毛毛雨",
    "Drizzle": "细雨",
    "Heavy drizzle": "大毛毛雨",
    "Rain shower": "阵雨",
    "Light rain shower": "小阵雨",
    "Moderate rain shower": "中阵雨",
    "Heavy rain shower": "大阵雨",
    "Torrential rain shower": "暴雨阵雨",

    # 雪类（全等级）
    "Snow": "雪",
    "Light snow": "小雪",
    "Moderate snow": "中雪",
    "Heavy snow": "大雪",
    "Very heavy snow": "暴雪",
    "Patchy snow nearby": "局部零星小雪",
    "Patchy light snow": "局部小雪",
    "Snow shower": "阵雪",
    "Light snow shower": "小阵雪",
    "Heavy snow shower": "大阵雪",
    "Blowing snow": "吹雪",
    "Blizzard": "暴风雪",

    # 雷暴/冻雨/冰雹
    "Thunderstorm": "雷阵雨",
    "Thundery outbreaks possible": "可能有雷暴",
    "Patchy light rain with thunder": "局部小雨伴雷暴",
    "Moderate or heavy rain with thunder": "中大雨伴雷暴",
    "Patchy light snow with thunder": "局部小雪伴雷暴",
    "Moderate or heavy snow with thunder": "中大雪伴雷暴",
    "Freezing rain": "冻雨",
    "Light freezing rain": "小冻雨",
    "Heavy freezing rain": "大冻雨",
    "Ice pellets": "冰粒",
    "Hail": "冰雹",
    "Sleet": "雨夹雪",
    "Light sleet": "小雨夹雪",
    "Heavy sleet": "大雨夹雪",

    # 霜/露/风
    "Frost": "霜冻",
    "Dew": "露水",
    "Windy": "大风",
    "Strong wind": "强风",
    "Gale": "大风",
    "Storm": "暴风雨",
    "Hurricane": "飓风"
}

# 防闪退装饰器
def safe_run(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            messagebox.showerror("提示", "网络异常或地名输入错误")
    return wrapper

# 查询天气
@safe_run
def query_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("提示", "请输入城市/区/县名称")
        return

    city_encoded = urllib.parse.quote(city)
    url = f"https://wttr.in/{city_encoded}?format=j1"
    
    headers = {"User-Agent": "curl/7.68.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    current = data["current_condition"][0]
    weather_en = current["weatherDesc"][0]["value"]
    weather_cn = weather_translate.get(weather_en, weather_en)

    result = (f"📍 位置：{city}\n"
              f"🌡️  温度：{current['temp_C']} °C\n"
              f"💨  风速：{current['windspeedKmph']} km/h\n"
              f"💧  湿度：{current['humidity']}%\n"
              f"🌥️  天气：{weather_cn}\n"
              f"✅ 数据源：wttr.in（全球稳定）")

    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, result)

# 清空内容
def clear_all():
    city_entry.delete(0, tk.END)
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, "✅ 支持全国省市区县镇\n✅ 天气状态全中文显示\n")
    city_entry.focus()

# ==================== 美化后的UI界面 ====================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("天气查询工具 🎈")
    root.geometry("580x480")
    root.resizable(False, False)
    # 设置全局背景色（柔和浅蓝）
    root.configure(bg="#f0f8ff")

    # 配置ttk样式（美化组件）
    style = ttk.Style(root)
    style.theme_use("clam")  # 启用clam主题以支持更多样式自定义
    
    # 自定义按钮样式
    style.configure("Query.TButton", 
                    font=("微软雅黑", 11),
                    foreground="white",
                    background="#409eff",
                    padding=8)
    style.map("Query.TButton",
              background=[("active", "#66b1ff")],
              foreground=[("active", "white")])
    
    style.configure("Clear.TButton", 
                    font=("微软雅黑", 11),
                    foreground="white",
                    background="#909399",
                    padding=8)
    style.map("Clear.TButton",
              background=[("active", "#a8abb2")],
              foreground=[("active", "white")])
    
    # 自定义输入框样式
    style.configure("City.TEntry",
                    font=("微软雅黑", 12),
                    padding=6)

    # 标题容器
    title_frame = tk.Frame(root, bg="#f0f8ff")
    title_frame.pack(pady=25)
    # 标题标签（渐变配色+加粗）
    title_label = tk.Label(title_frame, 
                           text="📅 全国天气查询工具", 
                           font=("微软雅黑", 20, "bold"), 
                           fg="#1967d2",
                           bg="#f0f8ff")
    title_label.pack()
    # 副标题
    sub_label = tk.Label(title_frame,
                         text="支持精准到区县的天气查询",
                         font=("微软雅黑", 10),
                         fg="#666666",
                         bg="#f0f8ff")
    sub_label.pack(pady=3)

    # 输入区域容器
    input_frame = tk.Frame(root, bg="#f0f8ff")
    input_frame.pack(pady=10)
    # 输入框（圆角+边框美化）
    city_entry = ttk.Entry(input_frame, 
                           style="City.TEntry",
                           width=35)
    city_entry.pack(side=tk.LEFT, padx=5)
    city_entry.focus()
    city_entry.bind("<Return>", lambda e: query_weather())

    # 按钮区域容器
    btn_frame = tk.Frame(root, bg="#f0f8ff")
    btn_frame.pack(pady=12)
    # 查询按钮
    query_btn = ttk.Button(btn_frame, 
                           text="查询天气", 
                           command=query_weather,
                           style="Query.TButton",
                           width=15)
    query_btn.pack(side=tk.LEFT, padx=8)
    # 清空按钮
    clear_btn = ttk.Button(btn_frame, 
                           text="清空内容", 
                           command=clear_all,
                           style="Clear.TButton",
                           width=15)
    clear_btn.pack(side=tk.LEFT, padx=8)

    # 结果显示区域
    result_frame = tk.Frame(root, bg="#f0f8ff", bd=1, relief=tk.RIDGE)
    result_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    # 结果文本框（美化样式）
    result_box = scrolledtext.ScrolledText(result_frame, 
                                           font=("微软雅黑", 11), 
                                           width=65, 
                                           height=16,
                                           bg="white",
                                           bd=0,
                                           relief=tk.FLAT,
                                           wrap=tk.WORD)
    result_box.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
    # 初始提示文本
    result_box.insert(tk.END, "✅ 支持全国省市区县镇\n✅ 天气状态全中文显示\n✅ 输入名称后按回车也可查询\n")
    # 设置文本框选中颜色
    result_box.tag_configure("sel", background="#e6f7ff", foreground="black")

    root.mainloop()