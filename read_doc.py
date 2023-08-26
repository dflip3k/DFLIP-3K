import tkinter as tk
from tkinter import filedialog
import fitz
import re

def preprocess(text):
    text = text.replace('\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text

def upload_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        try:
            doc = fitz.open(filepath)
            text_list = ""
            total_pages = doc.page_count
            end_page = total_pages
            for i in range(0, end_page):
                text = doc.load_page(i).get_text("text")
                text = preprocess(text)
                text_list += text
            text_area.delete('1.0', tk.END)
            text_area.insert('1.0', text_list)
        except Exception as e:
            text_area.delete('1.0', tk.END)
            text_area.insert('1.0', f"Error reading file: {e}")

def copy_to_clipboard():
    content = text_area.get('1.0', tk.END)  # 获取文本区域的内容
    root.clipboard_clear()  # 清空剪贴板
    root.clipboard_append(content)  # 将内容添加到剪贴板

root = tk.Tk()
root.geometry('500x500')
root.title("Change PDF to TEXT")

button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X)  # 将按钮放置在顶部

upload_button = tk.Button(button_frame, text="Upload File", command=upload_file)
upload_button.pack(side=tk.LEFT, padx=10)

copy_button = tk.Button(button_frame, text="Copy", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=10)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_area = tk.Text(root, yscrollcommand=scrollbar.set)
text_area.pack(side=tk.BOTTOM, fill='both', expand=True)  # 将文本区域和滚动条放置在底部

scrollbar.config(command=text_area.yview)

root.mainloop()