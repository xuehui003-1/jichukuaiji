# -*- coding: utf-8 -*-
# v5r：①init 补渲染首页地图(首开空地图bug) ②数据卡归位lead4之下 ③图谱画布aspect-ratio锁比例(黑边根治)
# ④3段卡通视频内嵌+灯箱(小邮亮相/看路线/课件馆导览) ⑤语音规律统一(graph/lib进门各播一次)
import base64, os
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()

# ═══ 1 首开地图 bug：init 补渲染 ═══
rep('renderStats();renderSHF();applyMode();\n})();',
    'renderStats();renderSHF();applyMode();renderMap("homeMapBox",homeScope);\n})();')

# ═══ 2 数据卡归位：secData 卡整段移到 lead4 之后（lead5 之前） ═══
iSD = s.find('<div class="card" id="secData">')
iL4 = s.find('<div class="secLead" id="lead4"')
iL5 = s.find('<div class="secLead" id="lead5"')
assert 0 < iSD < iL4 < iL5, (iSD, iL4, iL5)
seg = s[iSD:iL4]
s = s[:iSD] + s[iL4:iL5] + seg + s[iL5:]

# ═══ 3 图谱画布锁比例（黑边根治） ═══
rep('.gwrap{height:66vh;min-height:430px;background:linear-gradient(180deg,#0E1420,#0B0F1A);border-radius:14px}',
    '.gwrap{aspect-ratio:120/68;max-height:74vh;min-height:320px;background:linear-gradient(180deg,#0E1420,#0B0F1A);border-radius:14px}')

# ═══ 4 三段卡通视频内嵌 ═══
VID = ",".join('"%s":"data:video/mp4;base64,%s"' % (k, b64("_refs/xy/%s.mp4" % k)) for k in ["xyintro", "tmap", "libtour"])
rep('const RVOICE=[', 'const VID={' + VID + '};\nconst RVOICE=[')

# ═══ 5 视频灯箱 ═══
rep('<!-- 手势图解弹窗 -->',
    '''<!-- 视频灯箱 -->
<div class="modal" id="mVid"><div class="mcard" style="max-width:860px">
  <h3 id="mvT">小邮亮相</h3>
  <video id="mvPlayer" controls playsinline style="width:100%;border-radius:12px;background:#000"></video>
  <div class="mfoot" style="margin-top:10px;text-align:right"><button class="btn r" onclick="closeVid()">关闭</button></div>
</div></div>
<!-- 手势图解弹窗 -->''')
rep('function mapPeekOpen(){', '''function openVid(k,t){const m=document.getElementById("mVid");if(!m)return;
  document.getElementById("mvT").textContent=t||"小邮视频";
  const p=document.getElementById("mvPlayer");p.src=VID[k];m.classList.add("on");try{p.play()}catch(e){}}
function closeVid(){const m=document.getElementById("mVid");const p=document.getElementById("mvPlayer");
  if(p){try{p.pause()}catch(e){}p.removeAttribute("src");p.load()}
  if(m)m.classList.remove("on");}
function mapPeekOpen(){''')

# ═══ 6 入口挂视频 ═══
rep('<div class="heroBtns"><button class="hbtn" onclick="showTab(\'class\')">🏫 进课堂同步（课件真页）</button>',
    '<div class="heroBtns"><button class="hbtn" onclick="openVid(\'xyintro\',\'🎬 小邮亮相 · 30 秒\')">🎬 看小邮亮相</button><button class="hbtn" onclick="showTab(\'class\')">🏫 进课堂同步（课件真页）</button>')
rep('<svg width="86" height="86" viewBox="0 0 64 64" aria-label="小邮">',
    '<svg width="86" height="86" viewBox="0 0 64 64" aria-label="小邮（点我看亮相视频）" style="cursor:pointer" onclick="openVid(\'xyintro\',\'🎬 小邮亮相 · 30 秒\')">')
rep('<button onclick="document.getElementById(\'lead1\').scrollIntoView({behavior:\'smooth\'})"><i class="tico">🗺️</i><span><u>第一步</u>看路线</span></button>',
    '<button onclick="document.getElementById(\'lead1\').scrollIntoView({behavior:\'smooth\'});openVid(\'tmap\',\'🗺 第一步 · 看路线 · 10 秒过一遍\')"><i class="tico">🗺️</i><span><u>第一步</u>看路线</span></button>')
rep('''<section id="tab-lib">
  <div class="syncBan">''',
    '''<section id="tab-lib">
  <div class="card" style="margin:0 0 10px"><h3>🎬 课件馆导览 · 12 秒看完怎么用</h3>
    <video controls preload="none" src="''' + 'data:video/mp4;base64,' + b64("_refs/xy/libtour.mp4") + '''" style="width:100%;max-width:560px;border-radius:12px;background:#000"></video></div>
  <div class="syncBan">''')

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v5r OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
