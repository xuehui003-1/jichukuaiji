# -*- coding: utf-8 -*-
# v5p：①展厅更名"虚拟展厅" ②平面导览点击修复(flat也记落点) ③图谱星图化(轨道环+核心+纵深感+影子)
# ④课件馆教学顺序+项目讲次徽章+封面92px ⑤子任务=快递六步前缀体系(色点+序号) ⑥首页五步导览动线
# ⑦地图卡醒目提示+下拉呼吸光圈 ⑧3句语音+问答接线
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

# ═══ 1 展厅更名 ═══
rep("""<button id="tb-hall" onclick="showTab('hall')">🏢 展厅</button>""",
    """<button id="tb-hall" onclick="showTab('hall')">🏢 虚拟展厅</button>""")

# ═══ 2 平面导览点击修复：flat 也记落点，pointermove 跳过 ═══
rep("""r.addEventListener("pointerdown",e=>{const stq=document.querySelector(".hallStage");if(stq&&stq.classList.contains("flat")){hallDrag=null;return}e.preventDefault();hallDrag={x:e.clientX,a:hallA,m:0,w:e.target.closest?e.target.closest(".wall"):null};try{r.setPointerCapture(e.pointerId)}catch(_){}});""",
    """r.addEventListener("pointerdown",e=>{e.preventDefault();const stq=document.querySelector(".hallStage");hallDrag={x:e.clientX,a:hallA,m:0,w:e.target.closest?e.target.closest(".wall"):null,f:!!(stq&&stq.classList.contains("flat"))};try{r.setPointerCapture(e.pointerId)}catch(_){}});""")
rep("""r.addEventListener("pointermove",e=>{if(!hallDrag)return;const dx=e.clientX-hallDrag.x;hallDrag.m=Math.max(hallDrag.m,Math.abs(dx));hallA=hallDrag.a+dx*.25;applyHall()});""",
    """r.addEventListener("pointermove",e=>{if(!hallDrag||hallDrag.f)return;const dx=e.clientX-hallDrag.x;hallDrag.m=Math.max(hallDrag.m,Math.abs(dx));hallA=hallDrag.a+dx*.25;applyHall()});""")

# ═══ 3 图谱星图化：GN 轨道坐标+z 纵深 ═══
rep('''const GN=[
 {id:"var",t:"变量",c:0,x:32,y:11},{id:"type",t:"类型",c:0,x:12,y:28},{id:"cmd",t:"命令",c:0,x:52,y:28},
 {id:"flow",t:"流程图",c:1,x:32,y:45},{id:"if",t:"判断",c:1,x:13,y:63},{id:"loop",t:"循环",c:1,x:51,y:63},
 {id:"tank",t:"存钱罐",c:2,x:32,y:80},{id:"waimai",t:"外卖满减",c:2,x:10,y:80},{id:"banfei",t:"班费记账",c:2,x:54,y:80},
 {id:"audit",t:"审账复核",c:3,x:18,y:95},{id:"rule",t:"铁律",c:3,x:46,y:95}];''',
    '''const GN=[
 {id:"var",t:"变量",c:0,x:20.7,y:51.5,z:1},{id:"type",t:"类型",c:0,x:43.3,y:51.5,z:1.1},{id:"cmd",t:"命令",c:0,x:43.3,y:48.5,z:.95},
 {id:"flow",t:"流程图",c:1,x:32,y:58.5,z:1.15},{id:"if",t:"判断",c:1,x:11.3,y:47.1,z:.95},{id:"loop",t:"循环",c:1,x:52.7,y:47.1,z:.95},
 {id:"tank",t:"存钱罐",c:2,x:34.3,y:60,z:1.2},{id:"waimai",t:"外卖满减",c:2,x:10.7,y:55.7,z:1.05},{id:"banfei",t:"班费记账",c:2,x:54.5,y:55,z:1.05},
 {id:"audit",t:"审账复核",c:3,x:10.2,y:43.7,z:.9},{id:"rule",t:"铁律",c:3,x:53.8,y:43.7,z:.9}];''')

# ═══ 4 轨道环+核心（画在 GRAD 之后） ═══
rep("""function renderGraph(){const box=document.getElementById("kgBox");if(!box)return;kgProgText();""",
    """const ORB='<ellipse class="gorb" cx="32" cy="50" rx="12" ry="4.5"/><ellipse class="gorb" cx="32" cy="50" rx="22" ry="8.5"/><ellipse class="gorb" cx="32" cy="50" rx="26" ry="10"/><ellipse class="gorb" cx="32" cy="50" rx="24" ry="15"/><g class="gcore"><circle cx="32" cy="50" r="4.6"/><text class="gce" x="32" y="51.4">🤖</text><text class="gcl" x="32" y="59.5">财务机器人</text></g>';
function renderGraph(){const box=document.getElementById("kgBox");if(!box)return;kgProgText();""")
rep("""+GRAD+edges+nodes+'</g></svg></div>';""",
    """+GRAD+ORB+edges+nodes+'</g></svg></div>';""")

# ═══ 5 节点渲染：按 y 排序(近景后画)+地面影子+z 缩放半径 ═══
rep("""GN.forEach((n,i)=>{nodes+='<g class="gn'+(got[n.id]?" on":"")+'" data-id="'+n.id+'" style="animation-delay:'+(i*55)+'ms" transform="translate('+n.x+','+n.y+')">'""",
    """GN.slice().sort((a,b)=>a.y-b.y).forEach((n,i)=>{const zz=n.z||1;nodes+='<g class="gn'+(got[n.id]?" on":"")+'" data-id="'+n.id+'" style="animation-delay:'+(i*45)+'ms" transform="translate('+n.x+','+n.y+')">'+'<ellipse class="gsh" cx="0" cy="'+(7.8*zz).toFixed(1)+'" rx="'+(7*zz).toFixed(1)+'" ry="2"/>'""")
rep("""+'<circle class="ghalo" r="9.5"/><circle class="gnc" fill="url(#gr'+n.c+')" stroke="'+GCOLOR[n.c]+'" stroke-width=".55" r="6.2"/>""",
    """+'<circle class="ghalo" r="'+(9.5*zz).toFixed(1)+'"/><circle class="gnc" fill="url(#gr'+n.c+')" stroke="'+GCOLOR[n.c]+'" stroke-width=".55" r="'+(6.2*zz).toFixed(1)+'"/>""")

# ═══ 6 LIBDECKS 教学顺序 + 项目讲次徽章 ═══
rep('''const LIBDECKS={"10":{"name":"机器人上岗（上机首秀）","scope":"lib10"},"14":{"name":"图纸搬家","scope":"lib14"},"16":{"name":"让机器人循环","scope":"lib16"},"17":{"name":"判断＋循环（精修版）","scope":"dk17"},"04":{"name":"开学第一课","scope":"lib04"},"08":{"name":"变量·命令·流程（本节课）","scope":"dk08"}};''',
    '''const LIBDECKS={"04":{"name":"开学第一课","scope":"lib04"},"08":{"name":"变量·命令·流程（本节课）","scope":"dk08"},"10":{"name":"机器人上岗（上机首秀）","scope":"lib10"},"14":{"name":"图纸搬家","scope":"lib14"},"16":{"name":"让机器人循环","scope":"lib16"},"17":{"name":"判断＋循环（精修版）","scope":"dk17"}};
const DBADGE={"04":"项目一 · 第1讲","08":"项目二 · 第1–3讲","10":"项目二 · 第4讲","14":"项目三 · 第1讲","16":"项目三 · 第2讲","17":"项目三 · 第3讲"};''')
rep('Object.keys(LIBDECKS).map', '["04","08","10","14","16","17"].map')
rep("""+'<b>'+LIBDECKS[x].name+'</b><span>'+LDECKDESC[x]""",
    """+'<div class="dcR"><u class="dbadge">'+(DBADGE[x]||"")+'</u><b>'+LIBDECKS[x].name+'</b><span>'+LDECKDESC[x]""")
rep("""+LIBRAILS[x].length+' 页</span></button>')""",
    """+LIBRAILS[x].length+' 页</span></div></button>')""")

# ═══ 7 子任务=快递六步前缀体系 ═══
rep('''"cls":[["开场·智多星建命令",0,2],["案例①·食堂叫号",3,6],["案例②·打印店",7,11],["案例③·正定行程",12,17],["课后任务",18,18]]};''',
    '''"cls":[["取件","开场·智多星建命令",0,2],["装车","命令三要素·案例①",3,6],["派送","案例②③·先猜再跑",7,17],["签收","三句话·课后任务",18,18]]};
const SUBSTAGE={"取件":"#F59F23","分拣":"#4A6FB5","贴单":"#43A047","装车":"#8E44AD","派送":"#EF6C00","签收":"#00897B"};''')
rep('''el.innerHTML='<span class="subLead">任务结构</span>'+gs.map((g,k)=>'<button class="subChip'+(cur>=g[1]&&cur<=g[2]?" on":"")+'" onclick="'+goPrefix+g[1]+')"><u>'+"①②③④⑤⑥"[k]+'</u>'+g[0]+'<i>'+(g[1]+1)+"–"+(g[2]+1)+' 页</i></button>').join("");''',
    '''el.innerHTML='<span class="subLead">任务结构</span><span class="subHint">（快递六步：取件→分拣→贴单→装车→派送→签收）</span>'+gs.map((g,k)=>'<button class="subChip'+(cur>=g[2]&&cur<=g[3]?" on":"")+'" onclick="'+goPrefix+g[2]+')"><u>'+"①②③④⑤⑥"[k]+'</u><i class="sdot" style="background:'+SUBSTAGE[g[0]]+'"></i>'+g[0]+' · '+g[1]+'<em>'+(g[2]+1)+"–"+(g[3]+1)+' 页</em></button>').join("");''')
rep('''"08":[["开场·机器人收作业",0,5],["生活里找变量",6,11],["给格子起名字·五类对号",12,22],["命令三要素·案例①叫号",23,32],["案例②③·三种串法",33,43],["流程图·纸上调试",44,57]],''',
    '''"08":[["取件","机器人收作业",0,5],["分拣","生活里找变量",6,11],["贴单","给格子起名字·五类对号",12,22],["装车","命令三要素·案例①",23,32],["派送","案例②③·三种串法",33,43],["签收","流程图·纸上调试",44,57]],''')
rep('''"04":[["这门课学什么",0,4],["规矩实验室·拆洗衣机",5,18],["从机器到 AI·收官",19,25]],''',
    '''"04":[["取件","这门课学什么",0,4],["分拣","规矩实验室·拆洗衣机",5,18],["签收","从机器到 AI·收官",19,25]],''')
rep('''"10":[["开机第一跑",0,6],["把格子搬进电脑",7,10],["串命令·跑你的图纸",11,15],["读报错·类型转换",16,20]],''',
    '''"10":[["取件","开机第一跑",0,6],["贴单","把格子搬进电脑",7,10],["派送","串命令·跑你的图纸",11,15],["签收","读报错·类型转换",16,20]],''')
rep('''"14":[["大任务验收·开工",0,4],["认识工作台",5,7],["搬家三步·对答案",8,10],["让流程会问·存档",11,14],["三件事收尾",15,17]],''',
    '''"14":[["取件","大任务验收·开工",0,4],["分拣","认识工作台",5,7],["装车","搬家三步·对答案",8,10],["派送","让流程会问·存档",11,14],["签收","三件事收尾",15,17]],''')
rep('''"16":[["回忆与揭晓",0,4],["你来拼循环",5,7],["次数听人的",8,10],["上架·收尾",11,14]],''',
    '''"16":[["取件","回忆与揭晓",0,4],["装车","你来拼循环",5,7],["派送","次数听人的",8,10],["签收","上架·收尾",11,14]],''')
rep('''"17":[["作业对答案",0,3],["把判断装进循环",4,8],["你的存钱罐",9,10],["项目三收官",11,15]],''',
    '''"17":[["取件","作业对答案",0,3],["装车","把判断装进循环",4,8],["派送","你的存钱罐",9,10],["签收","项目三收官",11,15]],''')

# ═══ 8 首页五步动线：锚点 id ═══
rep('<div class="card"><h3>🃏 翻牌审账', '<div class="card" id="secRule"><h3>🃏 翻牌审账')
rep('<div class="card homeMap">', '<div class="card homeMap" id="secMap">')
rep('<div class="rings">', '<div class="rings" id="secRing">')
rep('<div class="card"><div id="statsBox"></div>', '<div class="card" id="secData"><div id="statsBox"></div>')
rep('<div class="card"><h3>🎬 30 秒案例导览', '<div class="card" id="secVid"><h3>🎬 30 秒案例导览')

# ═══ 9 导览条+五步引导语+英雄区下探提示 ═══
rep('''<div class="card" id="secRule">''',
    '''<div class="secLead">第①步 · 懂规矩 —— 30 秒翻一张牌，看 AI 怎么被管住</div>
  <div class="card" id="secRule">''')
rep('''<div class="card homeMap" id="secMap">''',
    '''<div class="tour"><span class="tLead">本页 60 秒导览</span><button onclick="document.getElementById('secRule').scrollIntoView({behavior:'smooth'})">① 懂规矩</button><button onclick="document.getElementById('secMap').scrollIntoView({behavior:'smooth'})">② 看路线</button><button onclick="document.getElementById('secRing').scrollIntoView({behavior:'smooth'})">③ 挑训练场</button><button onclick="document.getElementById('secData').scrollIntoView({behavior:'smooth'})">④ 验真</button><button onclick="document.getElementById('secVid').scrollIntoView({behavior:'smooth'})">⑤ 看实况</button></div>
  <div class="secLead">第②步 · 看路线 —— 九站任务地图，点站直达</div>
  <div class="card homeMap" id="secMap">''')
rep('''<div class="rings" id="secRing">''',
    '''<div class="secLead">第③步 · 挑训练场 —— 课件真页 / 机器人 / 手势 / 老师台</div>
  <div class="rings" id="secRing">''')
rep('''<div class="card" id="secData">''',
    '''<div class="secLead">第④步 · 验真 —— 试点班级真实数据，点开看可视化</div>
  <div class="card" id="secData">''')
rep('''<div class="card" id="secVid">''',
    '''<div class="secLead">第⑤步 · 看实况 —— 教师形象 30 秒导览</div>
  <div class="card" id="secVid">''')
rep('''</div><div class="say" id="heroCap"''',
    '''</div><div class="downHint">▼ 往下 60 秒，看懂这门课怎么玩</div><div class="say" id="heroCap"''')
rep('''<div id="homeMapBox"></div>''',
    '''<div class="mapCall">▼ 九站任务路线全图 · 点任意一站直接去上课</div><div id="homeMapBox"></div>''')

# ═══ 10 3 句语音 + 问答接线 + 图谱页讲解按钮 ═══
V4 = ",".join('"%s":"data:audio/mp3;base64,%s"' % (k, b64("_refs/xy/%s.mp3" % k)) for k in ["faqkg", "faqmap", "faqtask"])
rep(';Object.assign(VOICE,VOICE3);', ';Object.assign(VOICE,VOICE3);\nconst VOICE4={' + V4 + '};Object.assign(VOICE,VOICE4);')
rep('''["外卖满减的门道","faqwm"],[''',
    '''["外卖满减的门道","faqwm"],["像一片星座","faqkg"],["九个站点","faqmap"],["快递六步","faqtask"],[''')
rep('if(has("起名","命名"))',
    '''if(has("知识图谱","图谱","星座"))return "这是这门课的<b>知识图谱</b>，像一片星座：中心是财务机器人，四类颜色就是四类知识点，点亮过的会发光。像一片星座——我念给你听。";
  if(has("任务地图","路线图"))return "任务地图：<b>九个站点就是九个任务</b>，学完一个点亮一个；右上角切换任务范围，点任何一站直接去上课。九个站点——我念给你听。";
  if(has("子任务","任务结构"))return "每份课件是一个任务，子任务按<b>快递六步</b>走：取件接任务、分拣认类型、贴单起名字、装车学命令、派送跑案例、签收做验收。快递六步——我念给你听。";
  if(has("起名","命名"))''')
rep('"你的隐私三原则？"];', '"你的隐私三原则？","知识图谱怎么看？","任务地图怎么用？","子任务是什么？"];')
rep('🕸 知识图谱 · 这门课的知识结构（🗺 任务地图在首页）',
    '🕸 知识图谱 · 这门课的知识结构（🗺 任务地图在首页）<button class="tbtn gvo" onclick="sayVoice(\'faqkg\')">🔊 听小邮讲图谱</button>')

# ═══ 11 版本 ═══
rep('v5.6 结构版', 'v5.7 动线版')

# ═══ 12 CSS ═══
NEWCSS = '''
.gorb{fill:none;stroke:rgba(140,180,255,.13);stroke-dasharray:2 1.7;animation:gspin 22s linear infinite;transform-box:fill-box;transform-origin:center}
.gorb:nth-of-type(2){animation-duration:30s;animation-direction:reverse}
.gorb:nth-of-type(3){animation-duration:38s}
.gorb:nth-of-type(4){animation-duration:46s;animation-direction:reverse}
.gsh{fill:rgba(0,0,0,.42)}
.gcore circle{fill:url(#gr3);stroke:#CE93D8;stroke-width:.4;opacity:.95;animation:gpulse 3s ease-in-out infinite}
@keyframes gpulse{50%{opacity:.55}}
.gce{font-size:3.2px;text-anchor:middle}
.gcl{fill:#CE93D8;font-size:2.4px;text-anchor:middle;font-weight:700;letter-spacing:.2px}
.tour{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:12px 0 4px}
.tour button{border:1.5px solid #E7D8C2;background:#fff;border-radius:999px;padding:7px 14px;font-size:.86em;cursor:pointer;color:#4a2c1e;font-family:inherit}
.tour button:hover{border-color:#BF360C;color:#BF360C}
.tLead{font-weight:800;color:#8C1F28;font-size:.9em}
.secLead{margin:18px 0 8px;font-weight:800;color:#6b4a24;font-size:.98em}
.secLead:before{content:"◈ ";color:#BF360C}
.downHint{text-align:center;margin-top:14px;color:#BF360C;font-weight:700;font-size:.95em;animation:bob 1.6s ease-in-out infinite}
@keyframes bob{50%{transform:translateY(4px)}}
.mapCall{font-size:.88em;color:#BF360C;font-weight:700;margin:0 0 6px}
.homeMap select{animation:selGlow 2.4s ease-in-out infinite}
@keyframes selGlow{0%,100%{box-shadow:0 0 0 0 rgba(245,159,35,0)}50%{box-shadow:0 0 0 6px rgba(245,159,35,.28)}}
.sdot{width:9px;height:9px;border-radius:50%;display:inline-block;flex:0 0 auto}
.subChip em{font-style:normal;font-size:11px;color:#8a7a6a;margin-left:2px}
.subChip.on em{color:#FFD9A0}
.subHint{font-size:11.5px;color:#a08a70;font-weight:400;margin-left:4px}
.dbadge{font-size:11px;color:#8C1F28;background:#FBEDEA;border-radius:999px;padding:2px 8px;font-weight:700;text-decoration:none;white-space:nowrap}
.dcR{display:flex;flex-direction:column;gap:2px;align-items:flex-start;min-width:0}
.deckCard{gap:12px;padding:10px}
.dcover{width:92px;height:92px}
#libDeckRail{grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.eyebrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.gvo{background:#8C1F28;color:#fff;border-color:#8C1F28}
'''
_i = s.rfind('</style>')
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v5p OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
