"""
Лаб-2  Вариант 9  (books.csv + currency.xml)
python lab2_v9.py
"""
import csv, random, os, locale
from xml.dom import minidom
from collections import Counter

CSV_FILE = r"C:\Users\zyp92\OneDrive\桌面\Python.py\books.csv"
XML_FILE = r"C:\Users\zyp92\OneDrive\桌面\Python.py\currency.xml"
REF_FILE = r"C:\Users\zyp92\OneDrive\桌面\Python.py\references.txt"
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

# ----------- ① 书名长度>30 的统计 -----------
def task1():
    cnt = 0
    with open(CSV_FILE, newline='', encoding='cp1251') as f:
        for row in csv.reader(f,delimiter=';'):
            if len(row) < 2:
                continue
            if len(row[1]) > 30:
                cnt += 1
    print('① The length of the book title > 30：', cnt)

# ----------- ② 按作者搜索（价格≤200 卢布） -----------
def task2():
    key = input('② Author Keywords: ').strip().lower()
    found = 0
    with open(CSV_FILE, newline='', encoding='cp1251') as f:
        for row in csv.reader(f,delimiter=';'):
            if len(row) < 4:
                continue
            if key in row[2].lower() and float(row[3]) <= 200:
                print(f'   {row[1]}  —  {row[3]} руб.')
                found += 1
    if not found:
        print('   The author does not have the book ≤200 руб.')

# ----------- ③ 生成 20 条随机参考文献 -----------
def task3():
    rows = list(csv.reader(open(CSV_FILE, newline='', encoding='cp1251')))
    sample = random.sample(rows, 20)
    with open(REF_FILE, 'w', encoding='utf-8') as ref:
        for idx, r in enumerate(sample, 1):
          if len(r) >=5:
             ref.write(f'{idx}. {r[2]}. {r[1]}. {r[4]}.\n')
    print(f'③ Generated {REF_FILE}')

# ----------- ④ 解析 XML：只保留 Value ≥200 卢布 -----------
def task4():
    from xml.dom import minidom

    doc = minidom.parse(XML_FILE)
    print('④ Currency with a value ≥200 руб ：')
    found = 0
    for node in doc.getElementsByTagName('Valute'):
        # 拿 Value 并转浮点
        v_txt = node.getElementsByTagName('Value')[0].firstChild.data
        v = float(v_txt.replace(',', '.'))   # 俄文逗号→小数点

        if v >= 200:
            char = node.getElementsByTagName('CharCode')[0].firstChild.data
            num  = node.getElementsByTagName('NumCode')[0].firstChild.data
            print(f'   {char} ({num})  —  {v} руб.')
            found += 1

    if found == 0:
        print('  Do not have records of any currency ≥200 руб')

# ----------- ⑤ 不重复“标签”列 -----------
def task5():
    tags = {row[5] for row in csv.reader(open(CSV_FILE, newline='', encoding='cp1251')) if len(row) >= 6}
    print('⑤ Do not repeat tags（tag）：')
    for t in sorted(tags):
        print(f'   {t}')

# ----------- ⑥ 最受欢迎 20 本书 -----------
def task6():
    cnt = Counter()
    for row in csv.reader(open(CSV_FILE, newline='', encoding='cp1251'),delimiter=';'):
        if len(row) >= 2:
          cnt[row[1]] += 1
    print('⑥ The 20 most popular books：')
    for title, c in cnt.most_common(20):
        print(f'   {title}  ({c} )')