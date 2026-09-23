# -*- coding: utf-8 -*-
# v6.6 对标版：①导览五步名称紧扣《作品要求》(场景融合/创新理念/技术应用/实证课堂/成果推广+📑对应要求胶囊+步后总注)
# ②右下角小邮浮标换 3D 定妆照(内嵌 base64 圆形头图) ③课堂实录两段加电视机机框(木纹框+台标+REC)
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 导览五步对标 ═══
rep('<i class="tico">🗺️</i><span><u>第一步 · 首页地图</u>看路线</span>',
    '<i class="tico">🗺️</i><span><u>第一步 · 场景融合</u>九站任务地图</span>')
rep('<i class="tico">✨</i><span><u>第二步 · 看特色</u>两大镇店之宝</span>',
    '<i class="tico">✨</i><span><u>第二步 · 创新理念</u>两大特色视图</span>')
rep('<i class="tico">🎯</i><span><u>第三步 · 玩训练场</u>四个入口</span>',
    '<i class="tico">🎯</i><span><u>第三步 · 技术应用</u>AI 训练场</span>')
rep('<i class="tico">🎬</i><span><u>第四步 · 课堂同步</u>看实况</span>',
    '<i class="tico">🎬</i><span><u>第四步 · 实证课堂</u>教学实录</span>')
rep('<i class="tico">📊</i><span><u>第五步 · 真实数据</u>验真</span>',
    '<i class="tico">📊</i><span><u>第五步 · 成果推广</u>真实数据看板</span>')
i = s.find('id="tourBar"')
j = s.find("</div>", i)
assert 0 < i < j
s = s[:j] + '<span class="gsum">五步对照《作品要求》：场景融合 · 创新理念 · 技术应用 · 实证课堂 · 成果推广</span>' + s[j:]
rep('<div class="secLead" id="lead1">第一步 · 看路线 —— 九站任务地图，先看清这门课学什么<span class="tabChip">🏠 首页地图</span>',
    '<div class="secLead" id="lead1">第一步 · 场景融合 —— AI 智能体融入真实高校教学场景：九站任务地图，学到哪、走到哪<span class="tabChip">📑 对应要求：AI 与高校场景深度融合</span>')
rep('<div class="secLead" id="lead2">第二步 · 看特色 —— 两大镇店之宝：立体知识图谱 &amp; 虚拟展厅<span class="tabChip">🕸 知识图谱 · 🏢 虚拟展厅</span>',
    '<div class="secLead" id="lead2">第二步 · 创新理念 —— 让知识结构和课堂空间「看得见、转得动」，成果形式创新<span class="tabChip">📑 对应要求：创新理念 · 成果创新形式</span><span class="tabChip">🕸 知识图谱 · 🏢 虚拟展厅</span>')
rep('<div class="secLead" id="lead3">第三步 · 玩 AI 训练场 —— 四个动手入口，点了就进对应标签<span class="tabChip">🤖 机器人车间 · 🙌 手势闯关 · 🎯 课堂点名 · 🧹 名字消消乐</span>',
    '<div class="secLead" id="lead3">第三步 · 技术应用 —— 语音识别、图像识别、智能抽人，全部浏览器本地运行，课堂即用<span class="tabChip">📑 对应要求：技术创新应用 · 提升数字素养</span><span class="tabChip">🤖 车间 · 🙌 手势 · 🎯 点名 · 🧹 消消乐</span>')
rep('<div class="secLead" id="lead4">第四步 · 看实况 —— 真实课堂实录两段（在线播放）<span class="tabChip">🏫 课堂同步（录课实例同款）</span>',
    '<div class="secLead" id="lead4">第四步 · 实证课堂 —— 真实课堂实录两段：AI 生成的任务在投影上真跑，动线原样呈现<span class="tabChip">📑 对应要求：突破传统教学模式</span><span class="tabChip">🏫 课堂同步同款</span>')
rep('<div class="secLead" id="lead5">第五步 · 验真 —— 试点班级真实数据，点开看可视化<span class="tabChip">📊 数据由「课堂点名」计分导出</span>',
    '<div class="secLead" id="lead5">第五步 · 成果推广 —— 试点班级真实数据：三次课，发动学生 8→12→39 人，方法可复制<span class="tabChip">📑 对应要求：真实成果 · 示范推广作用</span>')

# ═══ 2 fab 换 3D 定妆照（静态 HTML，直接 data URI） ═══
b64 = base64.b64encode(open("_refs/xy/xyhead3d.png", "rb").read()).decode()
a = s.find('<svg class="xybot"')
b = s.find("</svg>", a) + len("</svg>")
assert 0 < a < b, "xybot svg 未找到"
s = s[:a] + '<img class="xybot" src="data:image/png;base64,' + b64 + '" alt="小邮伴学助手">' + s[b:]

# ═══ 3 电视机机框 ═══
rep('<figure><video controls preload="none" style="width:100%;border-radius:12px;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/8C9YvXdeGUCHhXiyjrqw6o.mp4"></video>',
    '<figure class="tvBezel"><div class="tvHead"><span class="rec"></span>课堂实录 · 片段① 开场任务 <u>LIVE</u></div><video controls preload="none" style="width:100%;border-radius:0 0 10px 10px;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/8C9YvXdeGUCHhXiyjrqw6o.mp4"></video>', n=2)
rep('<figure><video controls preload="none" style="width:100%;border-radius:12px;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/fUiT2T3KThx4xiSBQVGTdB.mp4"></video>',
    '<figure class="tvBezel"><div class="tvHead"><span class="rec"></span>课堂实录 · 片段② 暂停点⑨ <u>LIVE</u></div><video controls preload="none" style="width:100%;border-radius:0 0 10px 10px;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/fUiT2T3KThx4xiSBQVGTdB.mp4"></video>', n=2)

# ═══ 4 版本 ═══
rep('v6.5 立体版', 'v6.6 对标版')

# ═══ 5 CSS ═══
NEWCSS = '''
.gsum{font-size:11.5px;color:#8C1F28;background:#FBEDEA;border-radius:999px;padding:3px 12px;font-weight:700;margin-left:6px;white-space:nowrap}
.tvBezel{background:linear-gradient(160deg,#6B4A2B,#8A6238 55%,#5D3F22);border-radius:16px;padding:10px 10px 12px;box-shadow:0 10px 26px rgba(60,40,15,.28),inset 0 1.5px 0 rgba(255,235,200,.35)}
.tvHead{display:flex;align-items:center;gap:8px;color:#FFE8C4;font-size:12.5px;font-weight:800;letter-spacing:1px;padding:2px 4px 8px}
.tvHead u{text-decoration:none;background:rgba(0,0,0,.28);border-radius:6px;padding:1px 8px;font-size:10.5px;letter-spacing:2px}
.rec{width:9px;height:9px;border-radius:50%;background:#FF5252;box-shadow:0 0 8px #FF5252;animation:recBlink 1.2s infinite}
@keyframes recBlink{0%,55%{opacity:1}56%,100%{opacity:.25}}
.fab img.xybot{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;box-shadow:0 0 0 2.5px #fff inset}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v6.6 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
