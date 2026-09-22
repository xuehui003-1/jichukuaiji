# -*- coding: utf-8 -*-
# v6.4：①图谱分层重排(四层泳道+直线箭头边+近零交叉,关系/层次/顺序可读) ②翻牌面显示选项文字(先见内容再翻)
# ③首页IA梳理(删rings×8拼盘;第三步=四个训练入口;加映=图谱/展厅两卡;导览6钮对应标签)
# ④课堂点名/名字消消乐拆两标签 ⑤统计卡旧注归位
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 图谱分层重排 ═══
rep('''const GN=[
 {id:"var",t:"变量",c:0,x:45.3,y:38,z:1},{id:"type",t:"类型",c:0,x:74.7,y:38,z:1.05},{id:"cmd",t:"命令",c:0,x:60,y:26,z:.95},
 {id:"flow",t:"流程图",c:1,x:60,y:48,z:1.15},{id:"if",t:"判断",c:1,x:30,y:34,z:.95},{id:"loop",t:"循环",c:1,x:90,y:34,z:.95},
 {id:"tank",t:"存钱罐",c:2,x:85.2,y:49.6,z:1.2},{id:"waimai",t:"外卖满减",c:2,x:16.7,y:30.7,z:1.05},{id:"banfei",t:"班费记账",c:2,x:98.1,y:24.5,z:1.05},
 {id:"audit",t:"审账复核",c:3,x:12,y:24,z:.9},{id:"rule",t:"铁律",c:3,x:108,y:24,z:.9}];''',
    '''const GN=[
 {id:"var",t:"变量",c:0,x:25,y:11,z:1},{id:"type",t:"类型",c:0,x:60,y:11,z:1},{id:"cmd",t:"命令",c:0,x:95,y:11,z:1},
 {id:"flow",t:"流程图",c:1,x:50,y:30,z:1},{id:"if",t:"判断",c:1,x:80,y:36,z:1},{id:"loop",t:"循环",c:1,x:106,y:26,z:1},
 {id:"banfei",t:"班费记账",c:2,x:15,y:48,z:1},{id:"waimai",t:"外卖满减",c:2,x:45,y:48,z:1},{id:"tank",t:"存钱罐",c:2,x:88,y:48,z:1},
 {id:"audit",t:"审账复核",c:3,x:55,y:64,z:1},{id:"rule",t:"铁律",c:3,x:98,y:64,z:1}];''')
rep('''const GE=[["var","type"],["var","cmd"],["type","flow"],["cmd","flow"],["flow","if"],["flow","loop"],["if","tank"],["loop","tank"],["if","waimai"],["flow","banfei"],["tank","audit"],["tank","rule"],["waimai","audit"],["banfei","rule"]];''',
    '''const GE=[["var","flow"],["type","flow"],["cmd","flow"],["flow","if"],["flow","loop"],["if","waimai"],["if","tank"],["loop","tank"],["flow","banfei"],["tank","audit"],["waimai","audit"],["banfei","audit"],["audit","rule"]];''')
rep("const ORB='<ellipse class=\"gorb\" cx=\"60\" cy=\"34\" rx=\"17\" ry=\"8\"/><ellipse class=\"gorb\" cx=\"60\" cy=\"34\" rx=\"30\" ry=\"14\"/><ellipse class=\"gorb\" cx=\"60\" cy=\"34\" rx=\"44\" ry=\"19\"/><ellipse class=\"gorb\" cx=\"60\" cy=\"34\" rx=\"54\" ry=\"24\"/><g class=\"gcore\"><circle cx=\"60\" cy=\"34\" r=\"5.5\"/><text class=\"gce\" x=\"60\" y=\"35.4\">🤖</text><text class=\"gcl\" x=\"60\" y=\"43.5\">财务机器人</text></g>';",
    "const LANES='<rect x=\"1\" y=\"2\" width=\"118\" height=\"18\" rx=\"8\" fill=\"rgba(245,159,35,.06)\"/><rect x=\"1\" y=\"22\" width=\"118\" height=\"16\" rx=\"8\" fill=\"rgba(74,111,181,.06)\"/><rect x=\"1\" y=\"40\" width=\"118\" height=\"16\" rx=\"8\" fill=\"rgba(67,160,71,.06)\"/><rect x=\"1\" y=\"58\" width=\"118\" height=\"12\" rx=\"6\" fill=\"rgba(142,68,173,.06)\"/><text x=\"3.5\" y=\"8.5\" class=\"gln\">① 基础概念</text><text x=\"3.5\" y=\"28\" class=\"gln\">② 流程结构</text><text x=\"3.5\" y=\"46\" class=\"gln\">③ 任务应用</text><text x=\"3.5\" y=\"67.5\" class=\"gln\">④ 素养沉淀</text>';")
rep("""const mx=(a.x+b.x)/2+(b.y-a.y)*.14,my=(a.y+b.y)/2-(b.x-a.x)*.14;
  const d='M'+a.x+' '+(a.y+6)+' Q'+mx+' '+my+' '+b.x+' '+(b.y-6);""",
    """const d='M'+a.x+' '+(a.y+7)+' L'+b.x+' '+(b.y-7);""")
rep("""edges+='<path class="ge'+(got[b.id]?" on":"")+'" data-a="'+a.id+'" data-b="'+b.id+'" d="'+d+'"/>';""",
    """edges+='<path class="ge'+(got[b.id]?" on":"")+'" data-a="'+a.id+'" data-b="'+b.id+'" d="'+d+'" marker-end="url(#arr)"/>';""")
rep("""<text class="gnd" y="12.2">'+(n.c===3?"素养":(n.c===2?"任务":(n.c===1?"结构":"基础")))+'</text>'""",
    """'+(n.c===3?"":'<text class="gnd" y="12.2">'+(n.c===2?"任务":(n.c===1?"结构":"基础"))+'</text>')""")
rep("+GRAD+ORB+edges+nodes+", "+GRAD+LANES+edges+nodes+")
rep('<rect x="0" y="0" width="120" height="68" fill="url(#kpaper)"/><rect x="0" y="0" width="120" height="68" fill="url(#kdot)"/>',
    '<rect x="0" y="0" width="120" height="72" fill="url(#kpaper)"/><rect x="0" y="0" width="120" height="72" fill="url(#kdot)"/>')
rep('viewBox="0 0 120 68"', 'viewBox="0 0 120 72"')
rep('/r.height*68;', '/r.height*72;')
rep('</pattern></defs>', '</pattern><marker id="arr" viewBox="0 0 8 8" refX="6.6" refY="4" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#8a6a48"/></marker></defs>')
rep('滚轮缩放 · 拖拽平移 · 点胶囊收起一类', '自上而下四层：基础→结构→任务→素养，箭头指向知识去向 · 滚轮缩放 · 点胶囊收起一类')

# ═══ 2 翻牌面显示选项文字 ═══
rep("""h+='<div class="flipRow">'+SHF.opts.map((o,i)=>'<div class="fcW" id="fc'+i+'" onclick="shfFlip('+i+')"><div class="fcIn"><div class="fcF"><b>'+"ABC"[i]+'</b><span>🂠</span><u>点我翻牌</u></div><div class="fcB '+(i===SHF.right?"good":"bad")+'"><b>'+"ABC"[i]+'</b>'+o+'</div></div></div>').join("")+'</div>';
    h+='<div class="note">三张牌背朝上——先想好你选哪张，再点牌翻开（先判断，后揭晓）。</div>';""",
    """h+='<div class="flipRow">'+SHF.opts.map((o,i)=>'<div class="fcW" id="fc'+i+'" onclick="shfFlip('+i+')"><div class="fcIn"><div class="fcF"><b>'+"ABC"[i]+'</b><span>'+o+'</span><u>🂠 翻牌验证</u></div><div class="fcB '+(i===SHF.right?"good":"bad")+'"><b>'+(i===SHF.right?"✓":"✗")+'</b>'+(i===SHF.right?"判断正确！":"不是它——看下方复核")+'</div></div></div>').join("")+'</div>';
    h+='<div class="note">三个选项就写在牌面上——先想好你选哪张，再点牌翻开验证（先判断，后揭晓）。</div>';""")
rep('.fcF{background:linear-gradient(160deg,#8C1F28,#5D1520);color:#FFE082;border:2px solid #B3393F;box-shadow:0 4px 12px rgba(90,20,20,.25)}\n.fcF b{font-size:1.5em}\n.fcF span{font-size:2em;line-height:1}',
    '.fcF{background:#FFF8EE;border:2px solid #E7D8C2;color:#4a2c1e;box-shadow:0 4px 12px rgba(90,20,20,.12)}\n.fcF b{display:inline-block;width:28px;height:28px;line-height:28px;border-radius:50%;background:#8C1F28;color:#fff;font-size:.95em}\n.fcF span{font-size:.95em;line-height:1.35;font-weight:700}')

# ═══ 3 首页 IA 梳理 ═══
A = s.find('<div class="secLead" id="lead3"')
B = s.find('<div class="secLead" id="lead4"')
assert 0 < A < B
NEWL3 = '''<div class="secLead" id="lead3">第三步 · 玩 AI 训练场 —— 四个动手入口，点了就进对应标签<span class="tabChip">🤖 机器人车间 · 🙌 手势闯关 · 🎯 课堂点名 · 🧹 名字消消乐</span><button class="backTour" onclick="document.getElementById('tourBar').scrollIntoView({behavior:'smooth'})">▲ 返回导览</button></div>
  <div class="rings" id="secRing">
    <div class="ring" onclick="showTab('bot')"><u class="rb">真跑</u><b>🤖</b><div class="t">机器人车间</div><div class="d">改一个数先猜再跑；翻牌审账亲手复核一条账</div></div>
    <div class="ring" onclick="showTab('gest')"><u class="rb">用手答</u><b>🙌</b><div class="t">手势闯关</div><div class="d">☝✌👍✊ 摄像头本地识别答题，五题全出自课件</div></div>
    <div class="ring" onclick="showTab('roll')"><u class="rb">抽人</u><b>🎯</b><div class="t">课堂点名</div><div class="d">记录册暂停点随机抽人回答；下课检查·消名也在这页</div></div>
    <div class="ring" onclick="showTab('xyl')"><u class="rb">开场</u><b>🧹</b><div class="t">名字消消乐</div><div class="d">3 分钟把「你自己」装进变量面板——开场复习同款</div></div>
  </div>
  '''
s = s[:A] + NEWL3 + s[B:]
rep('<span><u>第三步 · 训练场入口</u>挑一个去</span>', '<span><u>第三步 · 玩训练场</u>四个入口</span>')
rep('</button><button onclick="document.getElementById(\'lead5\').scrollIntoView({behavior:\'smooth\'})"><i class="tico">📊</i><span><u>第五步 · 真实数据</u>验真</span></button></div>',
    '''</button><button onclick="document.getElementById('lead5').scrollIntoView({behavior:'smooth'})"><i class="tico">📊</i><span><u>第五步 · 真实数据</u>验真</span></button><button onclick="document.getElementById('lead6').scrollIntoView({behavior:'smooth'})"><i class="tico">✨</i><span><u>加映</u>特色视图</span></button></div>''')
rep('''数据来源：《财务机器人应用与开发》2501 班教学试点——67 份生活记账作业，来自同学们的先修课《基础会计》——本课拿它当真实业务素材：让机器人来干会计的活；姓名不出浏览器，公开页仅展示聚合数。</div>
  </div>
  </section>''',
    '''数据来源：课堂计分器自动导出（三次课 2026-09-04 / 09-11 / 09-18），三份原始表随作品仓库提交；姓名不出浏览器，公开页仅展示聚合数。另：67 份《基础会计》生活记账作业仍是本课真实业务素材——机器人干的活就从这些账里来。</div>
  </div>
  <div class="secLead" id="lead6">加映 · 两大特色视图 —— 知识结构与虚拟展厅<span class="tabChip">🕸 知识图谱 · 🏢 虚拟展厅</span><button class="backTour" onclick="document.getElementById('tourBar').scrollIntoView({behavior:'smooth'})">▲ 返回导览</button></div>
  <div class="rings">
    <div class="ring" onclick="showTab('graph')"><u class="rb">特色</u><b>🕸</b><div class="t">知识星图 · 知识图谱</div><div class="d">基础→结构→任务→素养四层知识地图，点亮会发光，点节点直达课件页</div></div>
    <div class="ring" onclick="showTab('hall')"><u class="rb">特色</u><b>🏢</b><div class="t">虚拟展厅</div><div class="d">3D 环视四面展墙，平面导览一键切换，点击展墙直达展区</div></div>
  </div>
  </section>''')

# ═══ 4 课堂点名/名字消消乐 拆分 ═══
rep('''  <button id="tb-roll" onclick="showTab('roll')">🎲 课堂点名</button>''',
    '''  <button id="tb-xyl" onclick="showTab('xyl')">🧹 名字消消乐</button>
  <button id="tb-roll" onclick="showTab('roll')">🎯 课堂点名</button>''')
rep('''<section id="tab-roll">
  <div class="eyebrow">🎲 课堂点名 · 名字消消乐与随机抽人（原版工具内嵌，风格原样）</div>
  <div class="note" style="margin:0 0 8px">开场活动「名字消消乐」：3 分钟把「你自己」装进变量面板，完成举手，学委当场消名；记录册暂停点用「随机抽人」请同学回答——<b>本页就是课堂同款工具，名字消消乐 v1.33</b>；三次课的真实计分数据也由它导出（见首页第五步）。</div>
  <div class="card" style="padding:8px"><iframe id="rollFrame" style="width:100%;height:78vh;border:0;border-radius:10px;background:#FFF8EE" title="课堂点名 · 消消乐与抽人"></iframe></div>
</section>''',
    '''<section id="tab-xyl">
  <div class="eyebrow">🧹 名字消消乐 · 开场复习：3 分钟把「你自己」装进变量面板（原版工具内嵌，风格原样）</div>
  <div class="note" style="margin:0 0 8px">课堂开场：全体动手完成「把你自己装进变量面板」的全部操作，做完举手，老师检查、学委当场消名——<b>名字消消乐 v1.33</b>，正是实录片段①里用的那套（见首页第四步）。</div>
  <div class="card" style="padding:8px"><iframe id="xylFrame" style="width:100%;height:78vh;border:0;border-radius:10px;background:#FFF8EE" title="名字消消乐"></iframe></div>
</section>
<section id="tab-roll">
  <div class="eyebrow">🎯 课堂点名 · 随机抽人（记录册暂停点专用 · 原版工具内嵌）</div>
  <div class="note" style="margin:0 0 8px">记录册每个暂停点用「随机抽人」请同学回答；页内「下课检查·消名」用于放学前的举册检查——三次课的真实计分数据（首页第五步）正是这套工具导出的。开场用的「名字消消乐」在隔壁「🧹 名字消消乐」标签。</div>
  <div class="card" style="padding:8px"><iframe id="rollFrame" style="width:100%;height:78vh;border:0;border-radius:10px;background:#FFF8EE" title="课堂点名 · 随机抽人"></iframe></div>
</section>''')
rep('''  const rf=document.getElementById("rollFrame");if(rf)rf.srcdoc=decodeURIComponent(escape(atob(B3B64)));''',
    '''  const rf=document.getElementById("rollFrame");if(rf)rf.srcdoc=decodeURIComponent(escape(atob(B3B64)));
  const xf=document.getElementById("xylFrame");if(xf)xf.srcdoc=decodeURIComponent(escape(atob(B3B64)));''')
rep('roll:"开场消名字、暂停点抽人——课堂里怎么用这里就怎么用，和教室里一字不差",',
    'xyl:"开场复习就用我：3 分钟把「你自己」装进变量面板，做完举手，学委消名",\n roll:"记录册暂停点随机抽人；下课检查·消名也在这一页",')

# ═══ 5 版本 ═══
rep('v6.3 翻牌版', 'v6.4 梳理版')

# ═══ 6 CSS ═══
NEWCSS = '''
.gln{font-size:2.6px;fill:#8a7a6a;font-weight:700;letter-spacing:.15px}
.fcW{width:172px;height:126px}
.fcF u{text-decoration:none;font-size:.74em;color:#BF360C;font-weight:700}
.fcB b{font-size:1.8em;line-height:1}
'''
_i = s.rfind('</style>')
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v6.4 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
