# -*- coding: utf-8 -*-
# v5q：①下探提示改白底药丸(红底红字修复) ②首页五步物理排序1→5+每步可返回导览+导览钮图标化
# ③地图半透明渐显+点击展开 ④图谱画布横版120×68重排(挤团/右空幕修复) ⑤快递六步→教学六步
# ⑥子任务阶段色全链化(胶囊左条+阶段名着色+页标题按阶段变色加粗) ⑦faqtask重录接线
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

# ═══ 1 首页物理排序：把「懂规矩」块(引导语+卡)移到「挑训练场」之前 ═══
i1 = s.find('<div class="secLead">第①步')
i2 = s.find('<div class="card" id="secData">')
assert 0 < i1 < i2, "锚点错序"
block = s[i1:i2]
s = s[:i1] + s[i2:]
j = s.find('<div class="secLead">第③步')
assert j > 0
s = s[:j] + block + s[j:]

# ═══ 2 五步引导语重编号（顺序校正在步骤8.5执行）＋id＋返回导览钮 ═══
rep('<div class="secLead">第①步 · 懂规矩 —— 30 秒翻一张牌，看 AI 怎么被管住</div>',
    '''<div class="secLead" id="lead2">第二步 · 懂规矩 —— 30 秒翻一张牌，看 AI 怎么被管住<button class="backTour" onclick="document.getElementById('tourBar').scrollIntoView({behavior:'smooth'})">▲ 返回导览</button></div>''')
rep('<div class="secLead">第②步 · 看路线 —— 九站任务地图，点站直达</div>',
    '''<div class="secLead" id="lead1">第一步 · 看路线 —— 九站任务地图，先看清这门课学什么<button class="backTour" onclick="document.getElementById('tourBar').scrollIntoView({behavior:'smooth'})">▲ 返回导览</button></div>''')
rep('<div class="secLead">第③步 · 挑训练场 —— 课件真页 / 机器人 / 手势 / 老师台</div>',
    '''<div class="secLead" id="lead3">第三步 · 挑训练场 —— 课件真页 / 机器人 / 手势 / 老师台<button class="backTour" onclick="document.getElementById('tourBar').scrollIntoView({behavior:'smooth'})">▲ 返回导览</button></div>''')
rep('<div class="secLead">第④步 · 验真 —— 试点班级真实数据，点开看可视化</div>',
    '''<div class="secLead" id="lead4">第四步 · 验真 —— 试点班级真实数据，点开看可视化<button class="backTour" onclick="document.getElementById('tourBar').scrollIntoView({behavior:'smooth'})">▲ 返回导览</button></div>''')
rep('<div class="secLead">第⑤步 · 看实况 —— 教师形象 30 秒导览</div>',
    '''<div class="secLead" id="lead5">第五步 · 看实况 —— 教师形象 30 秒导览<button class="backTour" onclick="document.getElementById('tourBar').scrollIntoView({behavior:'smooth'})">▲ 返回导览</button></div>''')

# ═══ 3 导览条：id＋图文钮（图标+步骤+名称），目标=步骤标题行 ═══
rep('''<div class="tour"><span class="tLead">本页 60 秒导览</span><button onclick="document.getElementById('secRule').scrollIntoView({behavior:'smooth'})">① 懂规矩</button><button onclick="document.getElementById('secMap').scrollIntoView({behavior:'smooth'})">② 看路线</button><button onclick="document.getElementById('secRing').scrollIntoView({behavior:'smooth'})">③ 挑训练场</button><button onclick="document.getElementById('secData').scrollIntoView({behavior:'smooth'})">④ 验真</button><button onclick="document.getElementById('secVid').scrollIntoView({behavior:'smooth'})">⑤ 看实况</button></div>''',
    '''<div class="tour" id="tourBar"><span class="tLead">本页 60 秒导览</span><button onclick="document.getElementById('lead1').scrollIntoView({behavior:'smooth'})"><i class="tico">🗺️</i><span><u>第一步</u>看路线</span></button><button onclick="document.getElementById('lead2').scrollIntoView({behavior:'smooth'})"><i class="tico">🃏</i><span><u>第二步</u>懂规矩</span></button><button onclick="document.getElementById('lead3').scrollIntoView({behavior:'smooth'})"><i class="tico">🎯</i><span><u>第三步</u>挑训练场</span></button><button onclick="document.getElementById('lead4').scrollIntoView({behavior:'smooth'})"><i class="tico">📊</i><span><u>第四步</u>验真</span></button><button onclick="document.getElementById('lead5').scrollIntoView({behavior:'smooth'})"><i class="tico">🎬</i><span><u>第五步</u>看实况</span></button></div>''')

# ═══ 4 地图半透明渐显＋点击展开 ═══
rep('<div class="mapCall">▼ 九站任务路线全图 · 点任意一站直接去上课</div><div id="homeMapBox"></div>',
    '''<div class="mapCall">▼ 九站任务路线全图 · 展开后点任意一站直接去上课</div><div class="mapPeek" id="mapPeek"><div id="homeMapBox"></div><div class="mapVeil" onclick="mapPeekOpen()"><button class="mapPeekBtn">⤢ 点击展开全图（展开后点站点直达）</button></div></div>''')
rep('function renderStats(){', '''function mapPeekOpen(){const m=document.getElementById("mapPeek");if(m)m.classList.add("open")}
function renderStats(){''')

# ═══ 5 图谱横版重排 ═══
rep('viewBox="0 0 64 103"', 'viewBox="0 0 120 68"')
rep('const vx=(ev.clientX-r.left)/r.width*64,vy=(ev.clientY-r.top)/r.height*103;',
    'const vx=(ev.clientX-r.left)/r.width*120,vy=(ev.clientY-r.top)/r.height*68;')
rep('''const GN=[
 {id:"var",t:"变量",c:0,x:20.7,y:51.5,z:1},{id:"type",t:"类型",c:0,x:43.3,y:51.5,z:1.1},{id:"cmd",t:"命令",c:0,x:43.3,y:48.5,z:.95},
 {id:"flow",t:"流程图",c:1,x:32,y:58.5,z:1.15},{id:"if",t:"判断",c:1,x:11.3,y:47.1,z:.95},{id:"loop",t:"循环",c:1,x:52.7,y:47.1,z:.95},
 {id:"tank",t:"存钱罐",c:2,x:34.3,y:60,z:1.2},{id:"waimai",t:"外卖满减",c:2,x:10.7,y:55.7,z:1.05},{id:"banfei",t:"班费记账",c:2,x:54.5,y:55,z:1.05},
 {id:"audit",t:"审账复核",c:3,x:10.2,y:43.7,z:.9},{id:"rule",t:"铁律",c:3,x:53.8,y:43.7,z:.9}];''',
    '''const GN=[
 {id:"var",t:"变量",c:0,x:45.3,y:38,z:1},{id:"type",t:"类型",c:0,x:74.7,y:38,z:1.05},{id:"cmd",t:"命令",c:0,x:60,y:26,z:.95},
 {id:"flow",t:"流程图",c:1,x:60,y:48,z:1.15},{id:"if",t:"判断",c:1,x:30,y:34,z:.95},{id:"loop",t:"循环",c:1,x:90,y:34,z:.95},
 {id:"tank",t:"存钱罐",c:2,x:85.2,y:49.6,z:1.2},{id:"waimai",t:"外卖满减",c:2,x:16.7,y:30.7,z:1.05},{id:"banfei",t:"班费记账",c:2,x:98.1,y:24.5,z:1.05},
 {id:"audit",t:"审账复核",c:3,x:12,y:24,z:.9},{id:"rule",t:"铁律",c:3,x:108,y:24,z:.9}];''')
rep('''const ORB='<ellipse class="gorb" cx="32" cy="50" rx="12" ry="4.5"/><ellipse class="gorb" cx="32" cy="50" rx="22" ry="8.5"/><ellipse class="gorb" cx="32" cy="50" rx="26" ry="10"/><ellipse class="gorb" cx="32" cy="50" rx="24" ry="15"/><g class="gcore"><circle cx="32" cy="50" r="4.6"/><text class="gce" x="32" y="51.4">🤖</text><text class="gcl" x="32" y="59.5">财务机器人</text></g>';''',
    '''const ORB='<ellipse class="gorb" cx="60" cy="34" rx="17" ry="8"/><ellipse class="gorb" cx="60" cy="34" rx="30" ry="14"/><ellipse class="gorb" cx="60" cy="34" rx="44" ry="19"/><ellipse class="gorb" cx="60" cy="34" rx="54" ry="24"/><g class="gcore"><circle cx="60" cy="34" r="5.5"/><text class="gce" x="60" y="35.4">🤖</text><text class="gcl" x="60" y="43.5">财务机器人</text></g>';''')

# ═══ 6 快递六步→教学六步 ═══
rep('''const SUBSTAGE={"取件":"#F59F23","分拣":"#4A6FB5","贴单":"#43A047","装车":"#8E44AD","派送":"#EF6C00","签收":"#00897B"};''',
    '''const STAGE6={"热身":["#F59F23","#FFF3E0"],"新知":["#4A6FB5","#E8F0FE"],"实操":["#43A047","#E8F5E9"],"案例":["#EF6C00","#FFF0E0"],"精进":["#8E44AD","#F3E5F5"],"收官":["#00897B","#E0F2F1"]};
function stColor(key,i){const gs=SUBT[key]||[];for(const g of gs){if(i>=g[2]&&i<=g[3])return STAGE6[g[0]]?STAGE6[g[0]][0]:"#8a7a6a"}return "#8a7a6a"}''')
rep('''"08":[["取件","机器人收作业",0,5],["分拣","生活里找变量",6,11],["贴单","给格子起名字·五类对号",12,22],["装车","命令三要素·案例①",23,32],["派送","案例②③·三种串法",33,43],["签收","流程图·纸上调试",44,57]],''',
    '''"08":[["热身","机器人收作业",0,5],["新知","生活里找变量",6,11],["实操","给格子起名字·五类对号",12,22],["案例","命令三要素·案例①",23,32],["精进","案例②③·三种串法",33,43],["收官","流程图·纸上调试",44,57]],''')
rep('''"04":[["取件","这门课学什么",0,4],["分拣","规矩实验室·拆洗衣机",5,18],["签收","从机器到 AI·收官",19,25]],''',
    '''"04":[["热身","这门课学什么",0,4],["实操","规矩实验室·拆洗衣机",5,18],["收官","从机器到 AI·收官",19,25]],''')
rep('''"10":[["取件","开机第一跑",0,6],["贴单","把格子搬进电脑",7,10],["派送","串命令·跑你的图纸",11,15],["签收","读报错·类型转换",16,20]],''',
    '''"10":[["热身","开机第一跑",0,6],["实操","把格子搬进电脑",7,10],["案例","串命令·跑你的图纸",11,15],["精进","读报错·类型转换",16,20]],''')
rep('''"14":[["取件","大任务验收·开工",0,4],["分拣","认识工作台",5,7],["装车","搬家三步·对答案",8,10],["派送","让流程会问·存档",11,14],["签收","三件事收尾",15,17]],''',
    '''"14":[["热身","大任务验收·开工",0,4],["新知","认识工作台",5,7],["实操","搬家三步·对答案",8,10],["案例","让流程会问·存档",11,14],["收官","三件事收尾",15,17]],''')
rep('''"16":[["取件","回忆与揭晓",0,4],["装车","你来拼循环",5,7],["派送","次数听人的",8,10],["签收","上架·收尾",11,14]],''',
    '''"16":[["热身","回忆与揭晓",0,4],["实操","你来拼循环",5,7],["案例","次数听人的",8,10],["收官","上架·收尾",11,14]],''')
rep('''"17":[["取件","作业对答案",0,3],["装车","把判断装进循环",4,8],["派送","你的存钱罐",9,10],["签收","项目三收官",11,15]],''',
    '''"17":[["热身","作业对答案",0,3],["实操","把判断装进循环",4,8],["案例","你的存钱罐",9,10],["收官","项目三收官",11,15]],''')
rep('''"cls":[["取件","开场·智多星建命令",0,2],["装车","命令三要素·案例①",3,6],["派送","案例②③·先猜再跑",7,17],["签收","三句话·课后任务",18,18]]};''',
    '''"cls":[["热身","开场·智多星建命令",0,2],["新知","命令三要素·案例①",3,6],["案例","案例②③·先猜再跑",7,17],["收官","三句话·课后任务",18,18]]};''')
rep("""el.innerHTML='<span class="subLead">任务结构</span><span class="subHint">（快递六步：取件→分拣→贴单→装车→派送→签收）</span>'+gs.map((g,k)=>'<button class="subChip'+(cur>=g[2]&&cur<=g[3]?" on":"")+'" onclick="'+goPrefix+g[2]+')"><u>'+"①②③④⑤⑥"[k]+'</u><i class="sdot" style="background:'+SUBSTAGE[g[0]]+'"></i>'+g[0]+' · '+g[1]+'<em>'+(g[2]+1)+"–"+(g[3]+1)+' 页</em></button>').join("");""",
    """el.innerHTML='<span class="subLead">任务结构</span><span class="subHint">（教学六步：热身→新知→实操→案例→精进→收官）</span>'+gs.map((g,k)=>'<button class="subChip'+(cur>=g[2]&&cur<=g[3]?" on":"")+'" style="--sc:'+STAGE6[g[0]][0]+';--sb:'+STAGE6[g[0]][1]+'" onclick="'+goPrefix+g[2]+')"><u>'+"①②③④⑤⑥"[k]+'</u><b class="sname">'+g[0]+'</b>'+g[1]+'<em>'+(g[2]+1)+"–"+(g[3]+1)+' 页</em></button>').join("");""")
rep("""document.getElementById(zone+"Rail").innerHTML=rail.map((x,i)=>'<button class="railBtn'+(i===st.cur?" on":"")+'" onclick="dkGo(\\''+zone+'\\','+i+')">'+x[1]+"</button>").join("");""",
    """document.getElementById(zone+"Rail").innerHTML=rail.map((x,i)=>'<button class="railBtn'+(i===st.cur?" on":"")+'" style="color:'+stColor({cls:"cls",tank:"17",waimai:"08",banfei:"08"}[zone]||"08",i)+'" onclick="dkGo(\\''+zone+'\\','+i+')">'+x[1]+"</button>").join("");""")
rep("""document.getElementById("libRail").innerHTML=rail.map((x,i)=>'<button class="railBtn'+(i===dkState.lib.cur?" on":"")+'" onclick="libGo('+i+')">'+x[1]+"</button>").join("");""",
    """document.getElementById("libRail").innerHTML=rail.map((x,i)=>'<button class="railBtn'+(i===dkState.lib.cur?" on":"")+'" style="color:'+stColor(dkState.lib.mountedRail||"08",i)+'" onclick="libGo('+i+')">'+x[1]+"</button>").join("");""")

# ═══ 7 faqtask 重录＋文案换教学六步 ═══
V4 = ",".join('"%s":"data:audio/mp3;base64,%s"' % (k, b64("_refs/xy/%s.mp3" % k)) for k in ["faqkg", "faqmap", "faqtask"])
s = re.sub(r"const VOICE4=\{[^}]+\};", "const VOICE4={" + V4 + "};", s, count=1)
rep('["快递六步","faqtask"]', '["教学六步","faqtask"]')
rep('if(has("子任务","任务结构"))return "每份课件是一个任务，子任务按<b>快递六步</b>走：取件接任务、分拣认类型、贴单起名字、装车学命令、派送跑案例、签收做验收。快递六步——我念给你听。";',
    'if(has("子任务","任务结构"))return "每份课件是一个大任务，子任务按<b>教学六步</b>走：热身回忆、新知讲解、实操上机、案例拆解、精进排错、收官验收。教学六步——我念给你听。";')


# ═══ 1b 顺序校正：验真块移到训练场块之后 ═══
_i4=s.find('<div class="secLead" id="lead4"')
_i3=s.find('<div class="secLead" id="lead3"')
_i5=s.find('<div class="secLead" id="lead5"')
if 0<_i4<_i3<_i5:
    s=s[:_i4]+s[_i3:_i5]+s[_i4:_i3]+s[_i5:]

# ═══ 8 版本 ═══
rep('v5.7 动线版', 'v5.8 循序版')

# ═══ 9 CSS ═══
NEWCSS = '''
.downHint{display:inline-block;background:rgba(255,255,255,.94);color:#8C1F28;margin-top:14px;padding:8px 20px;border-radius:999px;font-weight:800;font-size:.95em;box-shadow:0 3px 10px rgba(80,20,20,.28);animation:bob 1.6s ease-in-out infinite}
.tour button{display:inline-flex;align-items:center;gap:9px;padding:8px 15px}
.tico{font-style:normal;font-size:21px;line-height:1}
.tour button span{display:flex;flex-direction:column;align-items:flex-start;line-height:1.25}
.tour button u{text-decoration:none;font-size:11px;color:#BF360C;font-weight:800}
.secLead{scroll-margin-top:84px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.backTour{border:1.5px solid #E7D8C2;background:#fff;border-radius:999px;padding:3px 12px;font-size:12px;cursor:pointer;color:#6b4a24;font-family:inherit}
.backTour:hover{border-color:#BF360C;color:#BF360C}
.mapPeek{position:relative;max-height:330px;overflow:hidden}
.mapPeek.open{max-height:none}
.mapVeil{position:absolute;inset:0;z-index:3;display:flex;align-items:flex-end;justify-content:center;padding-bottom:14px;background:linear-gradient(180deg,rgba(255,252,246,0) 30%,rgba(255,252,246,.96) 86%);cursor:pointer}
.mapPeek.open .mapVeil{display:none}
.mapPeekBtn{background:#8C1F28;color:#fff;border:none;border-radius:999px;padding:10px 22px;font-size:14.5px;font-weight:800;cursor:pointer;box-shadow:0 4px 14px rgba(80,20,20,.35);font-family:inherit}
.subChip{border-left:4px solid var(--sc,#BF360C);background:var(--sb,#FFF8EE)}
.subChip .sname{color:var(--sc,#BF360C);font-weight:800}
.subChip.on{background:var(--sc,#8C1F28);border-color:var(--sc,#8C1F28)}
.subChip.on .sname{color:#FFE082}
.railBtn{font-weight:700}
.railBtn.on{color:#fff!important}
'''
_i = s.rfind('</style>')
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v5q OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
