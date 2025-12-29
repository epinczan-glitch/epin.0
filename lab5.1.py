import re  #正则表达式是用于处理文本的强大工具，可以进行模式匹配、查找、替换等操作
import csv   #csv 是Python的CSV文件处理模块,csv是逗号分隔值。它是一种纯文本格式，用来存储表格数据。
from bs4 import BeautifulSoup   #from bs4：指定从哪个模块导入，import BeautifulSoup：导入该模块中的BeautifulSoup类
#这三个库经常一起用于网络爬虫和数据提取项目

# ---------- 任务1：处理 task1_en.txt ----------
print("----------任务1----------")
with open(r'C:\Users\zyp92\OneDrive\桌面\task1-en.txt', 'r', encoding='utf-8') as f:#'r'：以只读模式打开文件,将打开的文件对象赋值给变量f
    #f.read()：读取文件的全部内容将整个文件内容作为一个字符串存储在text1变量中
    text1 = f.read()

# 1. 以 e 结尾的单词
words_ending_e = re.findall(r'\b\w*e\b', text1, flags=re.IGNORECASE)
# #\b单词边界,匹配单词的开始或结束位置   \w匹配任何单词字符
#text1：要搜索的文本,flags=re.IGNORECASE：忽略大小写,可以匹配 "e" 或 "E"
print("以 e 结尾的单词：", words_ending_e)

# 2. 圆括号中的数字
numbers_in_parens = re.findall(r'\((\d+)\)', text1)
#\(：匹配左圆括号 (,括号在正则中有特殊含义，需要转义     \d：匹配数字（0-9）,+：匹配1次或多次    ()：捕获组（capturing group）,表示要提取括号内的内容   匹配右圆括号 )
print("圆括号中的数字：", numbers_in_parens)

# ---------- 任务2：处理 task2.html ----------
print("----------任务2----------")
with open(r'C:\Users\zyp92\OneDrive\桌面\task2.html', 'r', encoding='utf-8') as f:
    html = f.read()
    #HTML 是 HyperText Markup Language 的缩写，中文意思是 超文本标记语言。它是创建网页和网络应用的标准标记语言
    soup = BeautifulSoup(html, 'html.parser')     #创建函数
    text2 = soup.get_text()    #提取HTML文档中的所有可见文本，忽略所有HTML标签     text2：纯文本字符串变量

# 同样提取以 e 结尾的单词和圆括号中的数字
words_ending_e_html = re.findall(r'\b\w*e\b', text2, flags=re.IGNORECASE)
numbers_in_parens_html = re.findall(r'\((\d+)\)', text2)

print("HTML中以 e 结尾的单词：", words_ending_e_html)
print("HTML中圆括号中的数字：", numbers_in_parens_html)

# ---------- 任务3：处理 task3.txt ----------
print("-----------任务3------------")
with open(r'C:\Users\zyp92\OneDrive\桌面\task3.txt', 'r', encoding='utf-8') as f:
    text3 = f.read()

# 正则提取各类数据
ids = re.findall(r'\b\d{1,3}\b', text3)      #{1,3}：匹配1到3次（1位、2位或3位数字）
names = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text3)
#功能：提取"名 姓"格式的英文全名
#[A-Z]：一个大写字母（名字首字母）  [a-z]+：一个或多个小写字母（名字剩余部分）  ：一个空格
emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text3)
#[a-zA-Z0-9._%+-]+：用户名部分，允许：字母、数字、点、下划线、百分号、加号、减号，+：至少一个字符
#[a-zA-Z0-9.-]+：域名部分（如：gmail、yahoo），\.：点（需要转义），[a-zA-Z]{2,}：顶级域名
dates = re.findall(r'\b\d{2}[\/\-.]\d{2}[\/\-.]\d{4}\b', text3)  #提取日期
websites = re.findall(r'https?:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text3)   #提取网址

# 确保数量一致（取前5个）
data_rows = list(zip(ids[:5], names[:5], emails[:5], dates[:5], websites[:5]))

# 写入CSV
print(data_rows)
with open('task3_output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)   #创建CSV写入器对象   writer：可以调用写入方法的对象
    writer.writerow(['ID', 'Name', 'Email', 'Date', 'Website'])  #writer.writerow()：写入一行数据,参数：一个列表，每个元素是一列的内容,这行创建了CSV文件的列标题
    writer.writerows(data_rows)#与writerow()的区别：一次写入多行

print("已生成 task3_output.csv")

# ---------- 附加任务：处理 task_add.txt ----------
#这段代码从文本中提取日期、邮箱和URL，并且要求这些模式前面必须有空格。然后各取前5个结果
print("---------------附加任务---------------")
with open(r'C:\Users\zyp92\OneDrive\桌面\task_add.txt', 'r', encoding='utf-8') as f:
    text_add = f.read()

# 提取日期、邮箱、URL（前面有空格）
dates_add = re.findall(r'\s(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})', text_add)
emails_add = re.findall(r'\s([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text_add)
urls_add = re.findall(r'\s(https?:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text_add)

# 各取前5个,切片操作[:5]
dates_add = dates_add[:5]
emails_add = emails_add[:5]
urls_add = urls_add[:5]
#提取列表的前5个元素   如果列表长度小于5，则返回全部    如果列表长度大于5，只取前5个，后面的丢弃

print("提取的日期：", dates_add)
print("提取的邮箱：", emails_add)
print("提取的网址：", urls_add)