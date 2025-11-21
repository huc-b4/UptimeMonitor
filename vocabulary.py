import requests
import datetime
import json
import os

# 数据文件，用于积累历史单词
DATA_FILE = "data/vocabulary.json"

def load_history():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_daily_word():
    """抓取金山词霸每日一句 (包含英文、中文、图片)"""
    try:
        # 金山词霸免费 API
        url = "http://open.iciba.com/dsapi/"
        resp = requests.get(url, timeout=10).json()
        return {
            "date": resp["dateline"],
            "content": resp["content"],  # 英文
            "note": resp["note"],        # 中文
            "translation": resp["translation"], # 词霸小编讲解
            "picture": resp["picture2"]  # 配图
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_readme(word, history):
    # 生成历史列表 (最近 7 天)
    history_md = "| 日期 | 英文 | 中文 |\n| :--- | :--- | :--- |\n"
    # 将新词加到历史开头
    full_list = [word] + history
    
    # 取前 7 个展示在表格里
    for item in full_list[:7]:
        history_md += f"| {item['date']} | {item['content']} | {item['note']} |\n"

    # 生成主页内容
    content = f"""
# 📘 Daily English Learning

每天自动抓取每日一句，积累英语词汇。

### 📅 今日打卡 ({word['date']})

![Image]({word['picture']})

> **{word['content']}**
> 
> *{word['note']}*

---

### 🗂️ 最近一周记录
{history_md}

---
*Powered by GitHub Actions*
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    # 保存历史数据
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(full_list[:100], f, ensure_ascii=False, indent=2) # 只存最近100条

if __name__ == "__main__":
    word = get_daily_word()
    if word:
        history = load_history()
        update_readme(word, history)
        print("Vocabulary updated.")
    else:
        print("Failed to fetch word.")
