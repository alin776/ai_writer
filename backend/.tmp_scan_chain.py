from pathlib import Path
import re

material = Path(r"D:\Java\ai_writer\docs\Agent\real-book\一夕千悟，从杂役弟子开始.txt")
text = material.read_text(encoding='utf-8')
lines = text.splitlines()
chapter_pattern = re.compile(r"^第\s*[0-9]+\s*章")

def norm(s):
    return s.replace('\u3000',' ').strip()

docs=[]
chapter_order=0
chapter_title='前言'
para=0
for raw in lines:
    line=norm(raw)
    if not line:
        continue
    if chapter_pattern.match(line):
        m=re.match(r"^第\s*([0-9]+)\s*章", line)
        if m:
            chapter_order=int(m.group(1))
        else:
            chapter_order += 1
        chapter_title=line
        para=0
        continue
    docs.append((chapter_order, para, chapter_title, line))
    para += 1

keywords = [
    '废刀','读取器灵','赵穆','好刀','兵刃用得越久','滋养','吞噬成功','吞噬','牛尾刀','器灵等阶','精神力','立即'
]

for kw in keywords:
    print(f"\n==== {kw} ====")
    count=0
    for ch,p,title,line in docs:
        if kw in line:
            print(f"{ch}:{p} {line[:120]}")
            count += 1
            if count>=25:
                break
    print('count_shown=',count)
