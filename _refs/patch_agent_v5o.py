# -*- coding: utf-8 -*-
# v5o：①删首页孤儿按钮组(本次课残留) ②图谱页=纯知识图谱(控件移出画布+黑幕修复) ③首页地图全显示
# ④展厅平面导览修墙 ⑤翻牌模块场景化 ⑥任务范围措辞 ⑦课件子任务结构条 ⑧20句语音+6封面+问答接线
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()

# ═══ 1 首页孤儿按钮组（v5n 删卡残留：本次课·命令5站/全课程·9站 + 多余闭合） ═══
rep("""<div class="meBtns"><button class="btn" onclick="setKgScope('cls');showTab('graph')">本次课 · 命令 5 站</button><button class="btn o" onclick="setKgScope('all');showTab('graph')">全课程 · 9 站</button></div></div>""", "")

# ═══ 2 图谱页=纯知识图谱：删视图切换+课程下拉，控件行挂到画布外 ═══
rep("""<div class="kgTabs"><button id="kgTabMap" class="chip on" onclick="setKgView('map')">🎒 任务地图</button><button id="kgTabGraph" class="chip" onclick="setKgView('graph')">🕸 知识图谱</button><span id="kgScopeWrap"><select id="kgScopeSel" class="sel" onchange="setKgScope(this.value)"><option value="all">全课程 · 9 站</option><option value="cls">项目二 · 变量·命令·流程（本节课）</option><option value="p3">项目三 · 判断与循环</option><option value="" disabled>其余讲次 · 随课件入住建站</option></select></span><span class="kprog" id="kgProg"></span></div>""",
    """<div class="kgTabs"><span id="kgCtl" class="kgCtl"></span><span class="kprog" id="kgProg"></span></div>""")
rep('🗺 任务地图 · 学到哪，走到哪（右上角可切知识图谱）', '🕸 知识图谱 · 这门课的知识结构（🗺 任务地图在首页）')
rep("""<button id="tb-graph" onclick="showTab('graph')">🗺 任务地图</button>""", """<button id="tb-graph" onclick="showTab('graph')">🕸 知识图谱</button>""")

# ═══ 3 首页任务范围下拉改「任务」措辞（graph 侧下拉已删，此处仅剩 1 处） ═══
rep("""<option value="all">全课程 · 9 站</option><option value="cls">项目二 · 变量·命令·流程（本节课）</option><option value="p3">项目三 · 判断与循环</option><option value="" disabled>其余讲次 · 随课件入住建站</option>""",
    """<option value="all">全部任务 · 9 站</option><option value="cls">任务·变量命令流程（5 站）</option><option value="p3">任务·判断与循环（4 站）</option><option value="" disabled>其余任务 · 随课件入住建站</option>""")

# ═══ 4 kgView 默认图谱；setKgView 去除对已删元素的引用 ═══
rep('let kgView="map",kgV=', 'let kgView="graph",kgV=')
rep('document.getElementById("kgTabMap").classList.toggle("on",v==="map");', '')
rep('document.getElementById("kgTabGraph").classList.toggle("on",v==="graph");', '')
rep('const sw=document.getElementById("kgScopeWrap");if(sw)sw.style.display=(v==="map")?"inline-flex":"none";', '')

# ═══ 5 renderGraph：控件注入 #kgCtl（画布外），画布只留 svg ═══
rep("""box.innerHTML='<div class="gwrap"><div class="gctl"><span class="kchip kc0" data-c="0" onclick="kgToggleC(0)">基础</span><span class="kchip kc1" data-c="1" onclick="kgToggleC(1)">结构</span><span class="kchip kc2" data-c="2" onclick="kgToggleC(2)">任务</span><span class="kchip kc3" data-c="3" onclick="kgToggleC(3)">素养</span><button class="tbtn" onclick="kgZoom(1.25)">＋</button><button class="tbtn" onclick="kgZoom(.8)">－</button><button class="tbtn" onclick="kgReset()">⌂</button></div><div class="ghint">滚轮缩放 · 拖拽平移 · 悬停看邻居 · 点胶囊收起一类</div>'""",
    """const CTL=document.getElementById("kgCtl");if(CTL)CTL.innerHTML='<span class="kchip kc0" data-c="0" onclick="kgToggleC(0)">基础</span><span class="kchip kc1" data-c="1" onclick="kgToggleC(1)">结构</span><span class="kchip kc2" data-c="2" onclick="kgToggleC(2)">任务</span><span class="kchip kc3" data-c="3" onclick="kgToggleC(3)">素养</span><button class="tbtn" onclick="kgZoom(1.25)">＋</button><button class="tbtn" onclick="kgZoom(.8)">－</button><button class="tbtn" onclick="kgReset()">⌂</button><span class="ghint2">滚轮缩放 · 拖拽平移 · 点胶囊收起一类</span>';
 box.innerHTML='<div class="gwrap">'""")

# ═══ 6 翻牌模块场景化 ═══
rep("""<h3>🙋 30 秒体验：翻牌审账<span class="pb">全站核心机制</span></h3>
    <div class="note">一张牌，三个角色：<b>① 你先判断 → ② 翻牌看 AI 复核 → ③ 等老师拍板</b>。这门课每天在发生的事，30 秒亲手走一遍——判断权在你，裁定权在老师：</div>""",
    """<h3>🃏 翻牌审账：这条账，你放行吗？<span class="pb">全站核心机制 · 30 秒</span></h3>
    <div class="note">场景：机器人刚替同学记了一条账（出自真实生活作业）。你是复核人——<b>①先自己判断 → ②翻牌看 AI 复核 → ③等老师拍板</b>。这三道关就是这门课管住 AI 的办法，每天在每条账上发生：</div>""")
rep('👉 想看老师那边怎么裁？去「教师台」的终审队列走一遍，全流程就通了。',
    '👉 这不是考你，是课堂日常的微缩。翻完牌去「教师台」看终审队列——低置信的账都在那儿等老师拍板。')

# ═══ 7 气泡文案跟进 ═══
rep('graph:"这就是这门课的寻宝路线：点亮一站是一站；右上角可切「知识图谱」看知识结构，点节点直达课件页"',
    'graph:"这就是这门课的知识结构：点亮的知识点是琥珀球，点节点直达课件页；寻宝路线（任务地图）在首页"')

# ═══ 8 课件子任务结构 ═══
rep('<div class="rail" id="clsRail"></div>', '<div class="subBar" id="clsSubBar"></div>\n    <div class="rail" id="clsRail"></div>')
rep('<div class="rail" id="libRail"></div>', '<div class="subBar" id="libSubBar"></div>\n    <div class="rail" id="libRail"></div>')
SUBT_JS = '''const SUBT={
 "08":[["开场·机器人收作业",0,5],["生活里找变量",6,11],["给格子起名字·五类对号",12,22],["命令三要素·案例①叫号",23,32],["案例②③·三种串法",33,43],["流程图·纸上调试",44,57]],
 "04":[["这门课学什么",0,4],["规矩实验室·拆洗衣机",5,18],["从机器到 AI·收官",19,25]],
 "10":[["开机第一跑",0,6],["把格子搬进电脑",7,10],["串命令·跑你的图纸",11,15],["读报错·类型转换",16,20]],
 "14":[["大任务验收·开工",0,4],["认识工作台",5,7],["搬家三步·对答案",8,10],["让流程会问·存档",11,14],["三件事收尾",15,17]],
 "16":[["回忆与揭晓",0,4],["你来拼循环",5,7],["次数听人的",8,10],["上架·收尾",11,14]],
 "17":[["作业对答案",0,3],["把判断装进循环",4,8],["你的存钱罐",9,10],["项目三收官",11,15]],
 "cls":[["开场·智多星建命令",0,2],["案例①·食堂叫号",3,6],["案例②·打印店",7,11],["案例③·正定行程",12,17],["课后任务",18,18]]};
function renderSubBar(elId,key,goPrefix,cur){const el=document.getElementById(elId);if(!el)return;const gs=SUBT[key]||[];
 if(!gs.length){el.innerHTML="";return}
 el.innerHTML='<span class="subLead">任务结构</span>'+gs.map((g,k)=>'<button class="subChip'+(cur>=g[1]&&cur<=g[2]?" on":"")+'" onclick="'+goPrefix+g[1]+')"><u>'+"①②③④⑤⑥"[k]+'</u>'+g[0]+'<i>'+(g[1]+1)+"–"+(g[2]+1)+' 页</i></button>').join("");}
'''
rep('function libShow(){', SUBT_JS + 'function libShow(){')
rep("""onclick="libGo('+i+')">'+x[1]+"</button>").join("");""",
    """onclick="libGo('+i+')">'+x[1]+"</button>").join("");renderSubBar("libSubBar",dkState.lib.mountedRail||"08","libGo(",dkState.lib.cur);""")
rep("function renderClass(){renderSHF();dkMount('cls',DKRAIL.cls)}",
    """function renderClass(){renderSHF();dkMount('cls',DKRAIL.cls);renderSubBar("clsSubBar","cls","dkGo('cls',",dkState.cls.cur)}""")
rep('function dkGo(zone,i){', """function dkGo(zone,i){if(zone==="cls")renderSubBar("clsSubBar","cls","dkGo('cls',",i);""")

# ═══ 9 课件馆封面 ═══
COV = ",".join('"%s":"data:image/jpeg;base64,%s"' % (k, b64("_refs/xy/cov%s.jpg" % k)) for k in ["04", "08", "10", "14", "16", "17"])
rep('const LDECKDESC={', 'const LIBCOV={' + COV + '};\nconst LDECKDESC={')
rep('\\\')"><b>\'+LIBDECKS[x].name+', '\\\')">\'+(LIBCOV[x]?\'<img class="dcover" src="\'+LIBCOV[x]+\'" alt="">\':\'\')+\'<b>\'+LIBDECKS[x].name+')


# ═══ 10 语音 8 句 + 问答接线 ═══
V3 = ",".join('"%s":"data:audio/mp3;base64,%s"' % (k, b64("_refs/xy/%s.mp3" % k)) for k in ["faqname", "faqprint", "faq12", "faqjd", "faqzx", "faqbk", "faqys", "faqwm"])
rep(';Object.assign(VOICE,VOICE2);', ';Object.assign(VOICE,VOICE2);\nconst VOICE3={' + V3 + '};Object.assign(VOICE,VOICE3);')
rep('const RVOICE=[[',
    'const RVOICE=[["起名窍门","faqname"],["print 的用处","faqprint"],["十二类货的口诀","faq12"],["借贷口诀","faqjd"],["置信度低交老师","faqzx"],["备课预演怎么用","faqbk"],["隐私三原则","faqys"],["外卖满减的门道","faqwm"],[')
rep('const AQUICK=["小邮，开口说一句","怎么用手答题？","生活费是收入吗？","存钱罐怎么改圈数？","学号为什么存字符？","分析：打车去吃饭一共58元记餐饮"];',
    'const AQUICK=["小邮，开口说一句","怎么用手答题？","生活费是收入吗？","存钱罐怎么改圈数？","学号为什么存字符？","分析：打车去吃饭一共58元记餐饮","变量名怎么起？","print 是干嘛的？","十二类货怎么分？","借贷方向怎么记？","你的隐私三原则？"];')
rep('if(has("生活费","收入"))',
    '''if(has("起名","命名"))return "给变量起名的窍门：<b>拼音或英文＋见名知意</b>——guanLi 就是「管理」。别用中文、别拿数字开头。起名窍门，我念给你听。";
  if(has("打印","print"))return "<code>print</code> 就像把格子里的东西<b>抄到黑板上</b>：干完活亮结果给你看。print 的用处，我念给你听。";
  if(has("隐私"))return "三句话：<b>姓名不出浏览器、页面只留聚合数、语音只在本机处理</b>。隐私三原则，我念给你听。";
  if(has("备课","预演"))return "老师在我这里把课先走一遍：<b>哪页停、问什么、答案何时揭晓</b>。备课预演怎么用，我念给你听。";
  if(has("置信","把握"))return "我的复核把握不足（置信度低）时<b>不硬下结论</b>，账目自动进教师台终审队列——置信度低交老师，我把这条规矩念给你听。";
  if(has("满减","外卖"))return "先看满减线、再算单价差——满减线是商家设好的<b>常量</b>。外卖满减的门道，我念给你听。";
  if(has("生活费","收入"))''')
rep('去「课堂同步」翻课件 15–18 真页，点屏逐类对答案。";', '去「课件馆」翻课件 15–18 真页，点屏逐类对答案。十二类货的口诀，我念给你听。";')
rep('用手势答一遍就记住了。";', '用手势答一遍就记住了。借贷口诀，我念给你听。";')

# ═══ 11 版本 ═══
rep('v5.5 聚合版', 'v5.6 结构版')

# ═══ 12 CSS ═══
NEWCSS = '''
.gwrap{height:66vh;min-height:430px;background:linear-gradient(180deg,#0E1420,#0B0F1A);border-radius:14px}
#kgSvg{width:100%;height:100%;display:block}
.kgCtl{display:flex;gap:6px;align-items:center;flex-wrap:wrap;flex:1}
.ghint2{font-size:11.5px;color:#8A6A48;margin-left:4px}
.homeMap #homeMapBox .mapwrap{height:auto!important;max-height:none!important;overflow:visible!important}
.homeMap #homeMapBox .mapwrap svg{width:100%;height:auto;display:block}
.hallStage.flat .wall{transform:none!important}
.subBar{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 8px;align-items:center}
.subLead{font-size:12px;color:#8a7a6a;font-weight:700}
.subChip{display:inline-flex;align-items:center;gap:6px;border:1.5px solid #E7D8C2;background:#fff;border-radius:999px;padding:5px 12px;font-size:12.5px;cursor:pointer;color:#4a2c1e;transition:.15s}
.subChip u{text-decoration:none;font-weight:800;color:#BF360C}
.subChip i{font-style:normal;font-size:11px;color:#8a7a6a}
.subChip:hover{border-color:#BF360C}
.subChip.on{background:#8C1F28;color:#fff;border-color:#8C1F28}
.subChip.on u{color:#FFE082}
.subChip.on i{color:#FFD9A0}
.deckCard{flex-direction:row;align-items:center;gap:10px}
.deckCard b{font-size:13.5px}
.dcover{width:64px;height:64px;object-fit:cover;border-radius:10px;flex:0 0 auto;border:1.5px solid #EFD9B8}
'''
_i = s.rfind('</style>')
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v5o OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
