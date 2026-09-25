# -*- coding: utf-8 -*-
# v7.10 同步并入版：①「课堂同步」页(tab-class)整体并入课件馆页——移除孤岛 section，原内容包进 #syncBlock
#   放在课件馆「课堂同步·正在上的课」横幅正下方；原三处 showTab('class') 全部改为 XYGO_SYNC()=切到课件馆并平滑滚到同步区
#   （依据：用户既有决定「课堂同步并入课件馆」+ 本轮"没必要单独设课堂同步页"；孤岛页用户本人都找不到=评委更找不到）
# ②V2 占位卡落位改 #syncBlock 顶（随迁）；V6 占位卡标题改为「真实课堂实证 · 这页课件，教室里正在讲」与「课件馆导览」教程视频区分
# ③版本 v7.10
import os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# 1) 摘出 tab-class
m = re.search(r'<section id="tab-class">([\s\S]*?)</section>', s)
assert m, "tab-class 未找到"
assert "<section" not in m.group(1), "tab-class 内嵌套 section?"
inner = m.group(1)
s = s[:m.start()] + s[m.end():]

# 2) 找课件馆横幅(syncBan)，其后插入同步区
b0 = s.find('<div class="syncBan"')
assert b0 > 0, "syncBan 未找到"

def walk_div_end(text, start):
    depth = 0
    for mt in re.finditer(r'<div\b|</div>', text[start:]):
        depth += 1 if mt.group(0) != "</div>" else -1
        if depth == 0:
            return start + mt.end()
    return -1

b_end = walk_div_end(s, b0)
assert b_end > 0
block = '\n<div id="syncBlock" style="margin:10px 0">' + inner + '</div>\n'
s = s[:b_end] + block + s[b_end:]

# 3) 三处 showTab('class') → XYGO_SYNC()
assert s.count("showTab('class')") == 3
s = s.replace("showTab('class')", "XYGO_SYNC()")
# 横幅按钮文案
rep("进入同步视图 →", "展开下方同步视图 ↓")

# 4) xyV79：V2 落位改 syncBlock；V6 标题区分教程；补 XYGO_SYNC 定义
rep('["V2","tab-class",0]', '["V2","syncBlock",0]')
rep('V6:"真实课堂实证 · 实录重新组装"', 'V6:"真实课堂实证 · 这页课件，教室里正在讲"')
rep('window.XYVIDEO_URLS={V1:"",V2:"",V3:"",V6:"",V7:""};',
    'window.XYVIDEO_URLS={V1:"",V2:"",V3:"",V6:"",V7:""};\nwindow.XYGO_SYNC=function(){try{showTab("lib")}catch(e){}setTimeout(function(){var b=document.getElementById("syncBlock");if(b)b.scrollIntoView({behavior:"smooth"})},80)};')

rep("v7.9 占位点播版", "v7.10 同步并入版")

assert '<section id="tab-class"' not in s
assert s.count('id="syncBlock"') == 1
lib0, xyl0 = s.find('<section id="tab-lib"'), s.find('<section id="tab-xyl"')
assert lib0 < s.find('id="syncBlock"') < xyl0, "syncBlock 不在课件馆内"

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.10 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
