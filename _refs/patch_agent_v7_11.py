# -*- coding: utf-8 -*-
# v7.11 课件馆重排版（按用户框架意见）：
#   ①「课堂同步」横幅改造为一条精简「正在上课」条＋两个跳转按钮：▶ 看这节课实录(滚到录课实例并自动播第一段) /
#      📖 翻到这节课的课件↓(切课件馆到课件08并滚到课件主体)——用户建议的"跳转按钮直达"方案
#   ②删除 syncBlock 整块(19页同步工具栏+clsStage+note)——与课件馆"全部课件"完全同机制,纯重复
#   ③录课实例卡搬到课件馆主体之后(页面底部,包 id="clsLive")；V2 占位卡落位改 clsLive 尾(实证区聚在底部)
#   ④XYGO_SYNC 重定义=showTab lib+libDeck("08")+滚到课件工具栏；新增 XYGO_LIVE；showTab 移除 renderClass 挂钩；curZone 兜底 cls→lib
import os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

def walk_div_end(text, start):
    depth = 0
    for mt in re.finditer(r'<div\b|</div>', text[start:]):
        depth += 1 if mt.group(0) != "</div>" else -1
        if depth == 0:
            return start + mt.end()
    return -1

if 'id="syncBlock"' in s:
    # 1) 横幅改造
    rep('<div class="syncBan"><div><b>🏫 课堂同步 · 正在上的课</b><span>变量·命令·流程 19 页真页 + 教师录课实例——和教室大屏一字不差</span></div><button class="btn" onclick="XYGO_SYNC()">展开下方同步视图 ↓</button></div>',
        '<div class="syncBan"><div><b>🏫 正在上课：变量·命令·流程</b><span>课件 08 · p26–44 —— 实录两段在本页底部，真页就在下方「全部课件」</span></div>'
        '<div style="display:flex;gap:6px;flex-wrap:wrap"><button class="btn" onclick="XYGO_LIVE()">▶ 看这节课实录</button>'
        '<button class="btn" onclick="XYGO_SYNC()">📖 翻到这节课的课件 ↓</button></div></div>')
    # 2) 剪出录课实例卡
    b0 = s.find('<div id="syncBlock"')
    i_card = s.find('<div class="card" style="margin-top:12px"><h3>🎬 录课实例', b0)
    assert i_card > 0
    c_end = walk_div_end(s, i_card)
    live_card = s[i_card:c_end]
    live_card = live_card.replace('与上面同步视图对照看：上面是学生视角的课件真页，这里是教师视角的课堂全貌；离线备份视频已随作品仓库提交。',
                                  '实录里讲的，就是上方课件馆的课件 08（p26–44）；离线备份视频已随作品仓库提交。')
    # 3) 删除整个 syncBlock
    sb_end = walk_div_end(s, b0)
    s = s[:b0] + s[sb_end:]
    # 4) 录课实例卡包 clsLive 插到 tab-lib 末尾
    sec_end = s.find('</section>', s.find('<section id="tab-lib"'))
    assert sec_end > 0
    ins = '\n<div id="clsLive">\n' + live_card + '\n</div>\n'
    s = s[:sec_end] + ins + s[sec_end:]
else:
    assert 'id="clsLive"' in s, "syncBlock 与 clsLive 均未找到"

# 5) xyV79：V2 落位 + 两个跳转函数
rep('["V2","syncBlock",0]', '["V2","clsLive",1]')
rep('window.XYGO_SYNC=function(){try{showTab("lib")}catch(e){}setTimeout(function(){var b=document.getElementById("syncBlock");if(b)b.scrollIntoView({behavior:"smooth"})},80)};',
    'window.XYGO_SYNC=function(){try{showTab("lib");if(typeof libDeck==="function")libDeck("08")}catch(e){}setTimeout(function(){var b=document.querySelector("#tab-lib .dkToolbar");if(b)b.scrollIntoView({behavior:"smooth"})},120)};\nwindow.XYGO_LIVE=function(){try{showTab("lib")}catch(e){}setTimeout(function(){var c=document.getElementById("clsLive");if(!c)return;c.scrollIntoView({behavior:"smooth"});var v=c.querySelector("video");if(v){var p=v.play();if(p&&p.catch)p.catch(function(){})}},120)};')

# 6) showTab 移除 renderClass 挂钩；curZone 兜底 cls→lib
rep('if(t==="lib"){if(!dkState.lib.rail)libDeck("08");try{renderClass()}catch(e){}}',
    'if(t==="lib"){if(!dkState.lib.rail)libDeck("08");}')
rep('return t("tab-lib")?"lib":(t("tab-bot")?"bot":"cls")',
    'return t("tab-lib")?"lib":(t("tab-bot")?"bot":"lib")')


# 7) 课件馆口径句(幂等)
_anchor = '<div class="stage" id="libStage"></div>'
_note = '<div class="note" style="margin:8px 0 6px">全部 <b>6 份课件 154 页</b>，任你翻；正在上的课＝<b>课件 08 · p26–44</b>（上方「▶ 看这节课实录」可直达课堂实录）。</div>'
if _note not in s:
    assert s.count(_anchor) == 1
    s = s.replace(_anchor, _note + _anchor)

rep("v7.10 同步并入版", "v7.11 课件馆重排版")

assert 'id="syncBlock"' not in s and 'clsStage' not in s and 'clsRail' not in s
assert s.count('id="clsLive"') == 1
lib0 = s.find('<section id="tab-lib"')
assert lib0 < s.find('id="clsLive"') < s.find('</section>', lib0)

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.11 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
