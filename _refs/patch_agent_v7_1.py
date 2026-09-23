# -*- coding: utf-8 -*-
# v7.1 全员版：①页头小邮 2D SVG→3D 形象(圆角方图,hover 俏皮摆动) ②任务地图 8 段路线加方向箭头(贝塞尔 t=0.88 截短+marker)
# ③小邮全页布点第一梯队:任务地图卡角"跟着我走九站"+验真数据卡角"数据我盯着"(贴纸+气泡,悬浮动画)
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 页头 3D 化 ═══
a = s.find('<svg width="56" height="56" viewBox="0 0 64 64" aria-label="小邮（点我看亮相视频）"')
b = s.find("</svg>", a) + len("</svg>")
assert 0 < a < b
img = '<img class="hxy" src="data:image/png;base64,%s" width="56" height="56" aria-label="小邮（点我看亮相视频）" onclick="openVid(\'xyintro\',\'🎬 小邮亮相 · 小邮自我介绍\')">' % base64.b64encode(open("_refs/xy/xyfabA.png", "rb").read()).decode()
s = s[:a] + img + s[b:]

# ═══ 2 地图路线箭头 ═══
rep("""  path+='<path class="stp" d="M'+p1[0]+' '+p1[1]+' Q'+mx+' '+my+' '+p2[0]+' '+p2[1]+'"/>';}""",
    """  const nx=(0.0144*p1[0]+0.2112*mx+0.7744*p2[0]).toFixed(1),ny=(0.0144*p1[1]+0.2112*my+0.7744*p2[1]).toFixed(1);
  path+='<path class="stp" d="M'+p1[0]+' '+p1[1]+' Q'+mx+' '+my+' '+nx+' '+ny+'" marker-end="url(#mArr)"/>';}""")
rep("""box.innerHTML='<div class="mapwrap"><svg viewBox="0 -9 100 72"><text class="decor" x="2" y="-1">🚩</text>""",
    """box.innerHTML='<div class="mapwrap"><svg viewBox="0 -9 100 72"><defs><marker id="mArr" viewBox="0 0 8 8" refX="5.4" refY="4" markerWidth="3.6" markerHeight="3.6" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#E8590C"/></marker></defs><text class="decor" x="2" y="-1">🚩</text>""")

# ═══ 3 小邮全页布点（第一梯队两处） ═══
bA = base64.b64encode(open("_refs/xy/xyfabC.png", "rb").read()).decode()
bE = base64.b64encode(open("_refs/xy/xyfabE.png", "rb").read()).decode()
rep('<div class="card homeMap" id="secMap"><div class="hmHead">',
    '<div class="card homeMap" id="secMap"><div class="xySticker"><img src="data:image/png;base64,' + bA + '" alt=""><i>跟着我，九站走一遍</i></div><div class="hmHead">')
rep('<div class="card" id="secData"><div id="statsBox">',
    '<div class="card" id="secData"><div class="xySticker"><img src="data:image/png;base64,' + bE + '" alt=""><i>三次课的真实记录，我替你盯着</i></div><div id="statsBox">')

# ═══ 4 版本 ═══
rep('v7.0 同心版', 'v7.1 全员版')

# ═══ 5 CSS ═══
NEWCSS = '''
.hxy{object-fit:contain;border-radius:16px;transition:.2s;filter:drop-shadow(0 3px 8px rgba(191,54,12,.35));vertical-align:middle}
.hxy:hover{transform:scale(1.08) rotate(-4deg)}
.xySticker{position:absolute;top:-20px;right:14px;display:flex;align-items:flex-start;gap:4px;z-index:3;pointer-events:none}
.xySticker img{width:62px;animation:xyFloat 2.8s ease-in-out infinite;filter:drop-shadow(0 4px 10px rgba(90,50,10,.28))}
.xySticker i{font-style:normal;background:#FFFDF8;border:2px solid #E8CFA0;color:#8C1F28;font-weight:800;font-size:12.5px;border-radius:12px 12px 12px 3px;padding:5px 10px;margin-top:10px;box-shadow:0 4px 12px rgba(90,50,10,.15);white-space:nowrap}
#secMap{position:relative}
#secData{position:relative}
@media (max-width:760px){.xySticker i{display:none}}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.1 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
