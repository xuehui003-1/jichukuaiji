# -*- coding: utf-8 -*-
# v6.7 灵动版：①对标语委婉化(删总注+5枚"对应要求"胶囊,五步名称保留,lead文案改白话) ②实录机框改纪录片REC监视器风(炭黑机身+REC时间码用真实时长+四角取景框)
# ③右下角小邮=全身双帧透明PNG(常浮+周期挥手+hover挥手大笑) ④版本v6.7
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 对标语委婉化 ═══
rep('<span class="gsum">五步对照《作品要求》：场景融合 · 创新理念 · 技术应用 · 实证课堂 · 成果推广</span>', '')
rep('第一步 · 场景融合 —— AI 智能体融入真实高校教学场景：九站任务地图，学到哪、走到哪<span class="tabChip">📑 对应要求：AI 与高校场景深度融合</span>',
    '第一步 · 场景融合 —— 这门课的九站任务地图：学到哪，走到哪，走到哪都能点亮')
rep('第二步 · 创新理念 —— 让知识结构和课堂空间「看得见、转得动」，成果形式创新<span class="tabChip">📑 对应要求：创新理念 · 成果创新形式</span><span class="tabChip">🕸 知识图谱 · 🏢 虚拟展厅</span>',
    '第二步 · 创新理念 —— 知识结构变成会转的立体大厦，课程变成一座能逛的展厅<span class="tabChip">🕸 知识图谱 · 🏢 虚拟展厅</span>')
rep('第三步 · 技术应用 —— 语音识别、图像识别、智能抽人，全部浏览器本地运行，课堂即用<span class="tabChip">📑 对应要求：技术创新应用 · 提升数字素养</span><span class="tabChip">🤖 车间 · 🙌 手势 · 🎯 点名 · 🧹 消消乐</span>',
    '第三步 · 技术应用 —— 语音、图像、智能抽人，全在浏览器里真跑真答<span class="tabChip">🤖 车间 · 🙌 手势 · 🎯 点名 · 🧹 消消乐</span>')
rep('第四步 · 实证课堂 —— 真实课堂实录两段：AI 生成的任务在投影上真跑，动线原样呈现<span class="tabChip">📑 对应要求：突破传统教学模式</span><span class="tabChip">🏫 课堂同步同款</span>',
    '第四步 · 实证课堂 —— 真实课堂实录两段：AI 生成的任务在投影上真跑，动线原样呈现<span class="tabChip">🏫 课堂同步同款</span>')
rep('第五步 · 成果推广 —— 试点班级真实数据：三次课，发动学生 8→12→39 人，方法可复制<span class="tabChip">📑 对应要求：真实成果 · 示范推广作用</span>',
    '第五步 · 成果推广 —— 三次课的真实记录：发动起来的学生 8→12→39 人')

# ═══ 2 REC 监视器机框 ═══
rep('<figure class="tvBezel"><div class="tvHead"><span class="rec"></span>课堂实录 · 片段① 开场任务 <u>LIVE</u></div><video controls preload="none" style="width:100%;border-radius:0 0 10px 10px;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/8C9YvXdeGUCHhXiyjrqw6o.mp4"></video>',
    '<figure class="camBezel"><div class="camHud"><span class="recLive"><span class="recDot"></span>REC 00:03:24</span><span class="camId">CAM 01 · 1080p</span></div><div class="camClip"><video controls preload="none" style="width:100%;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/8C9YvXdeGUCHhXiyjrqw6o.mp4"></video></div>', n=2)
rep('<figure class="tvBezel"><div class="tvHead"><span class="rec"></span>课堂实录 · 片段② 暂停点⑨ <u>LIVE</u></div><video controls preload="none" style="width:100%;border-radius:0 0 10px 10px;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/fUiT2T3KThx4xiSBQVGTdB.mp4"></video>',
    '<figure class="camBezel"><div class="camHud"><span class="recLive"><span class="recDot"></span>REC 00:04:06</span><span class="camId">CAM 02 · 1080p</span></div><div class="camClip"><video controls preload="none" style="width:100%;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/fUiT2T3KThx4xiSBQVGTdB.mp4"></video></div>', n=2)

# ═══ 3 fab 全身双帧 ═══
bA = base64.b64encode(open("_refs/xy/xyfabA.png", "rb").read()).decode()
bB = base64.b64encode(open("_refs/xy/xyfabB.png", "rb").read()).decode()
m = re.search(r'<img class="xybot" src="data:image/png;base64,[^"]+" alt="小邮伴学助手">', s)
assert m, "fab img 未找到"
s = s[:m.start()] + '<img class="xybot xyA" src="data:image/png;base64,' + bA + '" alt="小邮伴学助手"><img class="xybot xyB" src="data:image/png;base64,' + bB + '" alt="">' + s[m.end():]

# ═══ 3b 视频标题秒数清理（历史错标） ═══
rep("openVid('xyintro','🎬 小邮亮相 · 30 秒')",
    "openVid('xyintro','🎬 小邮亮相 · 小邮自我介绍')")
rep("openVid('tmap','🗺 第一步 · 看路线 · 10 秒过一遍')",
    "openVid('tmap','🗺 第一步 · 看路线 · 小邮带飞一遍')")
rep('<h3>🎬 课件馆导览 · 12 秒看完怎么用</h3>',
    '<h3>🎬 课件馆导览 · 一段看完就会用</h3>')

# ═══ 4 版本 ═══
rep('v6.6 对标版', 'v6.7 灵动版')

# ═══ 5 CSS ═══
NEWCSS = '''
.camBezel{background:linear-gradient(160deg,#23272B,#3A4046 55%,#1E2226);border-radius:14px;padding:8px 8px 10px;box-shadow:0 10px 26px rgba(20,25,30,.35),inset 0 1.5px 0 rgba(255,255,255,.12)}
.camHud{display:flex;align-items:center;justify-content:space-between;color:#E8ECEF;font-family:ui-monospace,Consolas,monospace;font-size:12px;letter-spacing:1.5px;padding:2px 4px 8px;font-weight:700}
.recLive{display:inline-flex;align-items:center;gap:6px}
.recDot{width:9px;height:9px;border-radius:50%;background:#FF3B30;box-shadow:0 0 8px #FF3B30;animation:recBlink 1.2s infinite}
.camId{opacity:.75}
.camClip{position:relative;border-radius:0 0 10px 10px;overflow:hidden}
.camClip::before,.camClip::after{content:"";position:absolute;width:22px;height:22px;z-index:2;pointer-events:none}
.camClip::before{left:8px;top:8px;border-left:2.5px solid rgba(255,255,255,.85);border-top:2.5px solid rgba(255,255,255,.85)}
.camClip::after{right:8px;bottom:8px;border-right:2.5px solid rgba(255,255,255,.85);border-bottom:2.5px solid rgba(255,255,255,.85)}
.fab{background:transparent;box-shadow:none;width:76px;height:76px;right:14px;bottom:14px}
.fab:hover{transform:translateY(-3px) scale(1.04)}
.fab::after{content:"";position:absolute;left:50%;bottom:2px;width:34px;height:8px;margin-left:-17px;border-radius:50%;background:rgba(70,45,20,.22);filter:blur(1.5px)}
.fab .xyA,.fab .xyB{position:absolute;inset:4px;width:68px;height:68px;object-fit:contain;object-position:center bottom;box-shadow:none;border-radius:0;animation:xyFloat 2.8s ease-in-out infinite}
.fab .xyB{opacity:0;animation:xyFloat 2.8s ease-in-out infinite,xyWave 5.5s steps(1,end) infinite}
.fab:hover .xyA{opacity:0}
.fab:hover .xyB{opacity:1;animation:xyFloat 2.8s ease-in-out infinite}
@keyframes xyFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes xyWave{0%,72%,100%{opacity:0}74%,86%{opacity:1}}
.aip{bottom:100px}
#fabNudge{bottom:100px}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v6.7 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
