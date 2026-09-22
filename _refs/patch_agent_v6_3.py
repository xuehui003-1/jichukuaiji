# -*- coding: utf-8 -*-
# v6.3：①真·翻牌(3D卡片翻转:牌背→点击rotateY180翻面揭晓) ②五步导览与标签对应(副行标对应标签+各步tabChip+看实况跳课堂同步)
# ③🎲上场→🎲课堂点名(含ring/实录注) ④内嵌点名页"下课消名字"→"下课检查·消名"(仅内嵌副本) ⑤懂规矩标题去"翻牌"表述
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 真·翻牌：pending 分支改为三张可翻卡片 ═══
rep("""  if(!a.done){
    h+=SHF.opts.map((o,i)=>'<button class="opt'+(a.pick===i?" sel":"")+'" onclick="shfFlip('+i+')">'+"ABC"[i]+'. '+o+' <u class="flipHint">🂠 点我翻牌 →</u></button>').join("");
    h+='<div class="note">想好再点——点击选项即翻牌揭晓（先判断，后揭晓）。</div>';
  }else{""",
    """  if(!a.done){
    h+='<div class="flipRow">'+SHF.opts.map((o,i)=>'<div class="fcW" id="fc'+i+'" onclick="shfFlip('+i+')"><div class="fcIn"><div class="fcF"><b>'+"ABC"[i]+'</b><span>🂠</span><u>点我翻牌</u></div><div class="fcB '+(i===SHF.right?"good":"bad")+'"><b>'+"ABC"[i]+'</b>'+o+'</div></div></div>').join("")+'</div>';
    h+='<div class="note">三张牌背朝上——先想好你选哪张，再点牌翻开（先判断，后揭晓）。</div>';
  }else{""")
rep('function shfFlip(i){const a=state.class.shf;a.pick=i;shfSubmit()}',
    '''function shfFlip(i){const a=state.class.shf;if(a.done||a.pick!==-1&&a.pick!==undefined&&a.pick!==null&&a.pick>=0)return;a.pick=i;
  const box=document.getElementById("shfBox");
  if(box&&box.querySelector(".fcW")){box.querySelectorAll(".fcW").forEach((c,k)=>{if(k===i)c.classList.add("flipped");else c.classList.add("dim")});setTimeout(()=>shfSubmit(),850)}else shfSubmit()}''')

# ═══ 2 五步导览 ↔ 标签对应 ═══
rep('<span><u>第一步</u>看路线</span>', '<span><u>第一步 · 首页地图</u>看路线</span>')
rep('<span><u>第二步</u>懂规矩</span>', '<span><u>第二步 · 机器人车间</u>懂规矩</span>')
rep('<span><u>第三步</u>挑训练场</span>', '<span><u>第三步 · 训练场入口</u>挑一个去</span>')
rep('<span><u>第四步</u>看实况</span>', '<span><u>第四步 · 课堂同步</u>看实况</span>')
rep('<span><u>第五步</u>验真</span>', '<span><u>第五步 · 真实数据</u>验真</span>')
rep('第二步 · 懂规矩 —— 30 秒翻一张牌，看 AI 怎么被管住<button class="backTour"',
    '第二步 · 懂规矩 —— 三条规矩，管住 AI（翻牌实操在机器人车间）<span class="tabChip">🤖 机器人车间</span><button class="backTour"')
rep('第一步 · 看路线 —— 九站任务地图，先看清这门课学什么<button class="backTour"',
    '第一步 · 看路线 —— 九站任务地图，先看清这门课学什么<span class="tabChip">🏠 首页地图</span><button class="backTour"')
rep('第三步 · 挑训练场 —— 课件真页 / 机器人 / 手势 / 老师台<button class="backTour"',
    '第三步 · 挑训练场 —— 下面每张卡直达一个标签<span class="tabChip">🎯 课件馆 / 车间 / 手势 / 教师 / 图谱 / 展厅 / 点名</span><button class="backTour"')
rep('第四步 · 看实况 —— 真实课堂实录两段（在线播放）<button class="backTour"',
    '第四步 · 看实况 —— 真实课堂实录两段（在线播放）<span class="tabChip">🏫 课堂同步（录课实例同款）</span><button class="backTour"')
rep('第五步 · 验真 —— 试点班级真实数据，点开看可视化<button class="backTour"',
    '第五步 · 验真 —— 试点班级真实数据，点开看可视化<span class="tabChip">📊 数据由「课堂点名」计分导出</span><button class="backTour"')
rep('演示现场断网可直接播仓库文件。</div>',
    '演示现场断网可直接播仓库文件。<button class="btn o" style="padding:3px 12px;margin-left:6px" onclick="showTab(\'class\')">进「课堂同步」对照课件逐页看 →</button></div>')

# ═══ 3 上场 → 课堂点名 ═══
rep('🎲 上场</button>', '🎲 课堂点名</button>')
rep('🎲 上场 · 真实课堂的抽人与名字消消乐（原版工具内嵌，风格原样）',
    '🎲 课堂点名 · 名字消消乐与随机抽人（原版工具内嵌，风格原样）')
rep('上场 · 抽人与名字消消乐', '课堂点名 · 消消乐与抽人', 2)  # ring 卡 + iframe title
rep('→「上场」随机抽人', '→「课堂点名」随机抽人')

# ═══ 4 内嵌点名页：下课消名字 → 下课检查·消名（仅内嵌副本，存档 v1.33 不动） ═══
m = re.search(r'const B3B64="([^"]+)"', s)
assert m, "B3B64 未找到"
raw = base64.b64decode(m.group(1)).decode("utf-8")
print("内嵌页 下课消名字 ×", raw.count("下课消名字"))
raw2 = raw.replace("下课消名字", "下课检查·消名")
s = s[:m.start()] + 'const B3B64="' + base64.b64encode(raw2.encode("utf-8")).decode() + '"' + s[m.end():]

# ═══ 5 版本 ═══
rep('v6.2 内嵌版', 'v6.3 翻牌版')

# ═══ 6 CSS ═══
NEWCSS = '''
.flipRow{display:flex;gap:12px;flex-wrap:wrap;margin:8px 0}
.fcW{width:158px;height:112px;perspective:750px;cursor:pointer}
.fcW.dim{opacity:.35;pointer-events:none}
.fcIn{position:relative;width:100%;height:100%;transform-style:preserve-3d;transition:transform .65s cubic-bezier(.4,1.4,.6,1)}
.fcW.flipped .fcIn{transform:rotateY(180deg)}
.fcF,.fcB{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:8px;text-align:center}
.fcF{background:linear-gradient(160deg,#8C1F28,#5D1520);color:#FFE082;border:2px solid #B3393F;box-shadow:0 4px 12px rgba(90,20,20,.25)}
.fcF b{font-size:1.5em}
.fcF span{font-size:2em;line-height:1}
.fcF u{text-decoration:none;font-size:.72em;color:#FFD9A0}
.fcB{transform:rotateY(180deg);font-size:.85em;background:#FFF8EE;border:2px solid #F2DFC0;color:#4a2c1e;line-height:1.4}
.fcB.good{border-color:#2E7D32;background:#E8F5E9}
.fcB.bad{border-color:#BF360C;background:#FBEDEA}
.fcB b{color:#8C1F28}
.tabChip{font-size:11.5px;background:#FBEDEA;color:#8C1F28;border-radius:999px;padding:2px 10px;font-weight:700;white-space:nowrap}
'''
_i = s.rfind('</style>')
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v6.3 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
