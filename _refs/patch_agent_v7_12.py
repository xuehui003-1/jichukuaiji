# -*- coding: utf-8 -*-
# v7.12 证据前置版：①课件馆三视频按逻辑链重排——V6占位卡(承诺)→正在上课条(声明+跳转)→录课实例两段(最硬证据,从页底上移)+V2卡→课件馆导览(用法)→全部课件主体；
#   解决"录课埋底不明显"(用户两次点名：首页底部+课件馆底部)
# ②第五步·成果推广全站一键直达：导航主栏加「📊 成果」按钮(XYGO_DATA=回首页+滚到数据看板+金色脉冲高亮)——内容不复制(防重复),入口全局化
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

# 1) clsLive 上移到 正在上课条(syncBan) 之后
if 'id="clsLive"' in s:
    i_live = s.find('<div id="clsLive">')
    live_end = walk_div_end(s, i_live)
    live = s[i_live:live_end]
    s = s[:i_live] + s[live_end:]
    b0 = s.find('<div class="syncBan"')
    assert b0 > 0
    b_end = walk_div_end(s, b0)
    s = s[:b_end] + "\n" + live + s[b_end:]
else:
    assert s.find('id="clsLive"') < s.find('<div class="syncBan"'), "clsLive 不在 syncBan 后"

# 2) note 方位词修正（课件主体现在其下方）
rep("实录里讲的，就是上方课件馆的课件 08（p26–44）；离线备份视频已随作品仓库提交。",
    "实录里讲的，就是下方课件馆的课件 08（p26–44）；离线备份视频已随作品仓库提交。")

# 3) 导航主栏加「📊 成果」
rep('<button id="tb-hall" onclick="showTab(\'hall\')">🏢 虚拟展厅</button>',
    '<button id="tb-hall" onclick="showTab(\'hall\')">🏢 虚拟展厅</button>\n  <button id="tb-data" onclick="XYGO_DATA()">📊 成果</button>')

# 4) xyV79 增补 XYGO_DATA + 脉冲样式
rep('window.XYVIDEO_URLS={V1:"",V2:"",V3:"",V6:"",V7:""};',
    'window.XYVIDEO_URLS={V1:"",V2:"",V3:"",V6:"",V7:""};\n'
    'window.XYGO_DATA=function(){try{showTab("home")}catch(e){}setTimeout(function(){var c=document.getElementById("secData");if(!c)return;'
    'try{c.scrollIntoView({behavior:"smooth"})}catch(e){}c.style.transition="box-shadow .4s";c.style.boxShadow="0 0 0 4px rgba(224,177,58,.85)";'
    'setTimeout(function(){c.style.boxShadow=""},1800)},120)};')

rep("v7.11 课件馆重排版", "v7.12 证据前置版")

# 校验
lib0 = s.find('<section id="tab-lib"')
assert 0 < s.find('<div class="syncBan"') and s.find('id="clsLive"') > s.find('<div class="syncBan"')
assert s.find('id="clsLive"', lib0) < s.find('id="libDeckRail"', lib0), "clsLive 应在课件主体之前"
assert 'id="tb-data"' in s and "XYGO_DATA" in s

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.12 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
