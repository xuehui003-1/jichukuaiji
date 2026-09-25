# -*- coding: utf-8 -*-
# v7.10b 并页收尾：curZone 摘除 tab-class 依赖(并页后 getElementById("tab-class")=null 会炸 dkNext/dkPrev)；
# dkPrev/dkNext 支持显式区参；syncBlock 工具栏按钮显式带 'cls'(与 lib 工具栏同屏防串台)；「全部课件→」改滚动到课件轨
import os
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

rep('if(t==="lib"){if(!dkState.lib.rail)libDeck("08");}','if(t==="lib"){if(!dkState.lib.rail)libDeck("08");try{renderClass()}catch(e){}}')
rep('return t("tab-class")?"cls":(t("tab-lib")?"lib":(t("tab-bot")?"bot":"cls"))',
    'return t("tab-lib")?"lib":(t("tab-bot")?"bot":"cls")')
rep('function dkNext(){const z=curZone()', 'function dkNext(z0){const z=z0||curZone()')
rep('function dkPrev(){const z=curZone()', 'function dkPrev(z0){const z=z0||curZone()')

# syncBlock 内工具栏：显式 'cls'
b0 = s.find('id="syncBlock"'); b1 = s.find("</div>", s.find("clsAsk()", b0))
assert 0 < b0 < b1
seg = s[b0:b1]
assert seg.count('onclick="dkPrev()"') == 1 and seg.count('onclick="dkNext()"') == 1
seg = seg.replace('onclick="dkPrev()"', "onclick=\"dkPrev('cls')\"").replace('onclick="dkNext()"', "onclick=\"dkNext('cls')\"")
seg = seg.replace("""<button class="tbtn" onclick="showTab('lib')">📚 全部课件 →</button>""",
                  """<button class="tbtn" onclick="document.getElementById('libRail').scrollIntoView({behavior:'smooth'})">📚 全部课件 ↑</button>""")
s = s[:b0] + seg + s[b1:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.10b OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
