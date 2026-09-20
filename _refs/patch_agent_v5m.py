#!/usr/bin/env python3
"""v5m：图谱工具条紧凑透明+真收缩样式强化+素养改紫+去视差防糊+节点标签药丸+边发光；地图=视图切换+课程下拉(修跳转bug)+标签描边+起终点旗；首页mapBar→图文任务地图(带下拉)；展厅重做(画框/射灯/地板/整墙可点/防拖出新页)；教师台关于=导航栏右上角(绝对定位)；fab说话动画；知识库徽标→面板底注；课件馆去数字前缀"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)
def cut(a,b):
    global s
    i=s.find(a);assert i>=0,a[:40]
    j=s.find(b,i);assert j>=0,b[:40]
    return i,j

rep("v5.3 展厅版`;","v5.4 精修版`;")

# ═══ 1 图谱 ═══
rep('const GCOLOR=["#FFB74D","#4FC3F7","#81C784","#FFD54F"];','const GCOLOR=["#FFB74D","#4FC3F7","#81C784","#CE93D8"];')
i,j=cut("const GRAD='<defs>","</defs>';")
s=s[:i]+"const GRAD='<defs><filter id=\"gglow\" x=\"-80%\" y=\"-80%\" width=\"260%\" height=\"260%\"><feGaussianBlur stdDeviation=\"1.1\" result=\"b\"/><feMerge><feMergeNode in=\"b\"/><feMergeNode in=\"SourceGraphic\"/></feMerge></filter><radialGradient id=\"gr0\" cx=\"35%\" cy=\"30%\"><stop offset=\"0\" stop-color=\"#FFE0B2\"/><stop offset=\"1\" stop-color=\"#FF9800\"/></radialGradient><radialGradient id=\"gr1\" cx=\"35%\" cy=\"30%\"><stop offset=\"0\" stop-color=\"#B3E5FC\"/><stop offset=\"1\" stop-color=\"#039BE5\"/></radialGradient><radialGradient id=\"gr2\" cx=\"35%\" cy=\"30%\"><stop offset=\"0\" stop-color=\"#C8E6C9\"/><stop offset=\"1\" stop-color=\"#43A047\"/></radialGradient><radialGradient id=\"gr3\" cx=\"35%\" cy=\"30%\"><stop offset=\"0\" stop-color=\"#F3D9FF\"/><stop offset=\"1\" stop-color=\"#8E44AD\"/></radialGradient></defs>';" +s[j+len("</defs>';"):]
rep(".kchip{cursor:pointer;font-size:12.5px;font-weight:800;border-radius:999px;padding:3px 11px;color:#102040;border:1px solid rgba(255,255,255,.3);transition:.15s}",
    ".kchip{cursor:pointer;font-size:12px;font-weight:800;border-radius:999px;padding:2px 9px;color:#102040;border:1px solid rgba(255,255,255,.3);transition:.15s}")
rep(".kchip.kc3{background:#FFD54F}",".kchip.kc3{background:#CE93D8}")
rep(".kchip.off{opacity:.32;text-decoration:line-through}",
    ".kchip.off{opacity:.28;filter:grayscale(1);text-decoration:line-through;text-decoration-thickness:2px}")
rep(".gctl{position:absolute;top:12px;right:12px;display:flex;gap:5px;align-items:center;z-index:5;flex-wrap:wrap;max-width:60%;justify-content:flex-end}",
    ".gctl{position:absolute;top:10px;right:10px;display:flex;gap:4px;align-items:center;z-index:5;background:transparent}")
rep(".gctl .tbtn{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.25);padding:4px 10px;font-size:13px}",
    ".gctl .tbtn{background:rgba(255,255,255,.12);color:#fff;border-color:rgba(255,255,255,.25);padding:2px 8px;font-size:12.5px;line-height:1.4}")
rep(".ge.on{stroke:#5EC8F2;stroke-width:.62;opacity:.85;",".ge.on{filter:url(#gglow);stroke:#5EC8F2;stroke-width:.62;opacity:.9;")
rep("+'<circle class=\"ghalo\" r=\"9.5\"/><circle class=\"gnc\" fill=\"url(#gr'+n.c+')\" stroke=\"'+GCOLOR[n.c]+'\" stroke-width=\".55\" r=\"6.2\"/><text class=\"gnt\" y=\"-8.6\">'",
    "+'<circle class=\"ghalo\" r=\"9.5\"/><circle class=\"gnc\" fill=\"url(#gr'+n.c+')\" stroke=\"'+GCOLOR[n.c]+'\" stroke-width=\".55\" r=\"6.2\"/><rect class=\"gnp\" x=\"-9\" y=\"-11.7\" width=\"18\" height=\"4.8\" rx=\"2.4\"/><text class=\"gnt\" y=\"-8.3\">'")
rep(".gnt{font-size:3.4px;font-weight:800;fill:#EAF2FF;text-anchor:middle}",
    ".gnt{font-size:3.2px;font-weight:800;fill:#EAF2FF;text-anchor:middle}\n.gnp{fill:rgba(13,22,44,.78);stroke:rgba(130,170,230,.3);stroke-width:.22}")
rep(".gstars{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1.5px),radial-gradient(rgba(140,180,255,.12) 1px,transparent 1.5px);background-size:46px 46px,29px 29px;background-position:0 0,14px 22px;pointer-events:none}",
    ".gstars{position:absolute;inset:0;background-image:radial-gradient(600px 320px at 72% 14%,rgba(96,70,200,.32),transparent 70%),radial-gradient(520px 300px at 12% 85%,rgba(20,120,160,.25),transparent 70%),radial-gradient(rgba(255,255,255,.16) 1px,transparent 1.5px),radial-gradient(rgba(140,180,255,.12) 1px,transparent 1.5px);background-size:100% 100%,100% 100%,46px 46px,29px 29px;background-position:0 0,0 0,0 0,14px 22px;pointer-events:none}")
rep('''svg.addEventListener("mousemove",ev=>{if(drag)return;const r=svg.getBoundingClientRect();
   const px=(ev.clientX-r.left)/r.width-.5,py=(ev.clientY-r.top)/r.height-.5;
   svg.style.transform="perspective(950px) rotateX("+(-py*9).toFixed(1)+"deg) rotateY("+(px*11).toFixed(1)+"deg)";});
 svg.addEventListener("mouseleave",()=>svg.style.transform="");''','')
rep('svg.addEventListener("pointerdown",ev=>{svg.style.transform="";drag={','svg.addEventListener("pointerdown",ev=>{drag={')
rep(".gwrap svg{transition:transform .18s ease}",".stt{paint-order:stroke;stroke:#FBF3E2;stroke-width:1.2px;stroke-linejoin:round}")

# ═══ 2 地图页 ═══
rep('''<button id="kgScCls" class="chip" onclick="setKgScope('cls')">本次课</button><button id="kgScAll" class="chip on" onclick="setKgScope('all')">全课程</button>''',
    '''<span id="kgScopeWrap"><select id="kgScopeSel" class="sel" onchange="setKgScope(this.value)"><option value="all">全课程 · 9 站</option><option value="cls">变量·命令·流程（本节课）</option><option value="p3">判断与循环（项目三）</option></select></span>''')
rep('''const STXY_CLS=[[10,14],[33,8],[56,14],[78,8],[52,30]];
let kgScope="all";
function setKgScope(v){kgScope=v;document.getElementById("kgScCls").classList.toggle("on",v==="cls");document.getElementById("kgScAll").classList.toggle("on",v==="all");kgView="map";renderKG()}''',
'''const STXY_CLS=[[10,14],[33,8],[56,14],[78,8],[52,30]];
const STOPS_P3=[
 {id:"p1",t:"流程图",d:"把步骤画出来",icon:"📐",page:["17",7]},
 {id:"p2",t:"判断",d:"条件的岔路口",icon:"🔀",page:["17",6]},
 {id:"p3",t:"循环",d:"重复交给机器人",icon:"🔁",page:["17",8]},
 {id:"p4",t:"存钱罐",d:"车间·判断+循环",icon:"🐷",bot:"tank"}];
const STXY_P3=[[12,12],[40,8],[68,14],[44,32]];
let kgScope="all",homeScope="all";
function setKgScope(v){kgScope=v;renderKG()}''')
rep('''function setKgView(v){kgView=v;
 document.getElementById("kgTabMap").classList.toggle("on",v==="map");
 document.getElementById("kgTabGraph").classList.toggle("on",v==="graph");
 kgV={x:0,y:0,s:1};renderKG()}''',
'''function setKgView(v){kgView=v;
 document.getElementById("kgTabMap").classList.toggle("on",v==="map");
 document.getElementById("kgTabGraph").classList.toggle("on",v==="graph");
 const sw=document.getElementById("kgScopeWrap");if(sw)sw.style.display=(v==="map")?"inline-flex":"none";
 kgV={x:0,y:0,s:1};renderKG()}''')
rep('''function renderMap(){const box=document.getElementById("kgBox");if(!box)return;
 const stops=kgScope==="cls"?STOPS_CLS:STOPS,XY=kgScope==="cls"?STXY_CLS:STXY;''',
'''function renderMap(boxId,scope){boxId=boxId||"kgBox";scope=scope||kgScope;
 const box=document.getElementById(boxId);if(!box)return;
 const stops=scope==="cls"?STOPS_CLS:scope==="p3"?STOPS_P3:STOPS,XY=scope==="cls"?STXY_CLS:scope==="p3"?STXY_P3:STXY;''')
rep(''' document.getElementById("kgProg").innerHTML="已点亮 <b>"+n+"</b> / "+stops.length+" 站"+(n===stops.length?" 🎉 全图通关！":"");''',
''' const pe=document.getElementById("kgProg");if(pe)pe.innerHTML="已点亮 <b>"+n+"</b> / "+stops.length+" 站"+(n===stops.length?" 🎉 全图通关！":"");''')
rep('''box.innerHTML='<div class="mapwrap"><svg viewBox="0 -9 100 72">'+path+stations+labels+'</svg></div>';
 box.querySelectorAll(".stG").forEach(g=>{g.style.cursor="pointer";g.onclick=()=>stopGo(stops[+g.dataset.i])});''',
'''box.innerHTML='<div class="mapwrap"><svg viewBox="0 -9 100 72"><text class="decor" x="2" y="-1">🚩</text><text class="decor" x="92" y="56">🏁</text>'+path+stations+labels+'</svg></div>';
 box.querySelectorAll(".stG").forEach(g=>{g.style.cursor="pointer";g.onclick=()=>{window.__fromMapTab=(boxId==="homeMapBox")?"home":"graph";stopGo(stops[+g.dataset.i])}});''')
rep('''bm.textContent="↩ 回任务地图";bm.onclick=()=>showTab("graph");''',
'''const bt=window.__fromMapTab||"graph";bm.textContent=bt==="home"?"↩ 回首页地图":"↩ 回任务地图";bm.onclick=()=>showTab(bt);''')
rep('.stt{font-size:3px;font-weight:800;fill:#4a2c1e;text-anchor:middle}','.stt{font-size:3px;font-weight:800;fill:#4a2c1e;text-anchor:middle;paint-order:stroke;stroke:#FBF3E2;stroke-width:1.1px;stroke-linejoin:round}')
rep('.stp{fill:none;stroke:#D8B888;stroke-width:1.1;stroke-dasharray:2.6 2.2;animation:dashf 1.6s linear infinite}',
    '.stp{fill:none;stroke:#C99B5F;stroke-width:1.25;stroke-dasharray:2.6 2.2;animation:dashf 1.6s linear infinite;stroke-linecap:round}\n.decor{font-size:4.2px;opacity:.95}')

# ═══ 3 首页 mapBar → 图文任务地图 ═══
i,j=cut('<div class="mapBar">','<div class="rings">')
HOME='''<div class="card homeMap"><div class="hmHead"><h3 style="margin:0">🗺 学习任务地图 <span class="hmSub">学到哪，走到哪——完成一站点亮一站</span></h3>
    <select id="homeScopeSel" class="sel" onchange="homeScope=this.value;renderMap('homeMapBox',homeScope)"><option value="all">全课程 · 9 站</option><option value="cls">变量·命令·流程（本节课）</option><option value="p3">判断与循环（项目三）</option></select></div>
    <div id="homeMapBox"></div>
    <div class="note" style="margin-top:4px">点任何站点直达任务；老师备课用右上角「🧑‍🏫 教师台」。</div></div>
  '''
s=s[:i]+HOME+s[j:]
rep('if(t==="home"){renderStats();renderSHF()}','if(t==="home"){renderStats();renderSHF();renderMap("homeMapBox",homeScope)}')

# ═══ 4 教师台/关于 = 导航栏右上角绝对定位 ═══
rep('nav .corner{margin-left:auto;display:flex;gap:6px}',
    'nav{position:relative}\nnav .corner{position:absolute;right:12px;top:50%;transform:translateY(-50%);display:flex;gap:6px}')
rep('nav .nin{display:flex;flex-wrap:wrap;align-items:center;gap:6px}',
    'nav .nin{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding-right:200px}')

# ═══ 5 fab 说话动画 ═══
rep('''function sayVoice(k){try{new Audio(VOICE[k]).play()}catch(e){}
  const f=document.getElementById("xyFace");if(f){f.classList.add("talking");setTimeout(()=>f.classList.remove("talking"),2300)}}''',
'''function sayVoice(k){try{new Audio(VOICE[k]).play()}catch(e){}
  const fb2=document.querySelector(".fab");if(fb2){fb2.classList.add("talking");setTimeout(()=>fb2.classList.remove("talking"),2400)}
  const f=document.getElementById("xyFace");if(f){f.classList.add("talking");setTimeout(()=>f.classList.remove("talking"),2300)}}''')
rep('.aiKb{margin-left:8px;font-size:10.5px;background:#EAF3EA;color:#2E6B2E;border-radius:999px;padding:2px 8px;font-weight:700;white-space:nowrap}',
'''.fab.talking svg.xybot{animation:xsay .5s ease-in-out infinite}
.fab.talking:after{content:"🔈";position:absolute;top:-16px;right:-4px;font-size:17px;animation:xping 1s ease-in-out infinite}
@keyframes xsay{0%,100%{transform:translateY(0) rotate(0)}25%{transform:translateY(-5px) rotate(-6deg)}75%{transform:translateY(-5px) rotate(6deg)}}
.afoot{font-size:11px;color:#8a7a6a;padding:5px 10px;border-top:1px dashed var(--line);background:#FFFDF8}''')

# ═══ 6 知识库徽标 → 面板底注 ═══
rep('<b>小邮伴学 · 有问题问我</b><span class="aiKb">AI 知识库·本地优先</span>','<b>小邮伴学 · 有问题问我</b>')
rep('''<button onclick="aSend()">发</button></div>''',
'''<button onclick="aSend()">发</button></div><div class="afoot">💡 回答来自小邮本地 AI 知识库 · 可在设置接入大模型</div>''')

# ═══ 7 课件馆去数字前缀 ═══
i,j=cut("const LIBDECKS={",";\nconst LDECKDESC")
s=s[:i]+'const LIBDECKS={"10":{"name":"机器人上岗（上机首秀）","scope":"lib10"},"14":{"name":"图纸搬家","scope":"lib14"},"16":{"name":"让机器人循环","scope":"lib16"},"17":{"name":"判断＋循环（精修版）","scope":"dk17"},"04":{"name":"开学第一课","scope":"lib04"},"08":{"name":"变量·命令·流程（本节课）","scope":"dk08"}}'+s[j+len(";\nconst LDECKDESC"):]
rep('"17":"判断＋循环·参赛精修"','"17":"参赛精修版课件"')

# ═══ 8 展厅重做 ═══
i,j=cut('<section id="tab-hall">','</section>')
HALL='''<section id="tab-hall">
  <div class="eyebrow">🏢 虚拟展厅 · 按住拖动环视，点击展墙进入</div>
  <div class="hallStage"><div class="floor"></div><div class="room" id="hallRoom">
    <div class="wall w1" data-go="lib"><div class="frame"><div class="fIc">📚</div><div class="wT">课件馆</div><div class="wD">6 份课件 · 154 页真页</div><div class="go">点击进入 →</div></div></div>
    <div class="wall w2" data-go="home"><div class="frame"><div class="fIc">🙋</div><div class="wT">核心机制</div><div class="wD">你判断 · AI 复核 · 老师拍板</div><div class="go">点击进入 →</div></div></div>
    <div class="wall w3" data-go="gest"><div class="frame"><div class="fIc">🙌</div><div class="wT">用手答 · 机器人真跑</div><div class="wD">本地手势识别 · 车间先猜再跑</div><div class="go">点击进入 →</div></div></div>
    <div class="wall w4" data-go="graph"><div class="frame"><div class="fIc">🗺</div><div class="wT">地图 · 语音 · 智能服务</div><div class="wD">任务地图 · 12 句语音 · 备课预演</div><div class="go">点击进入 →</div></div></div>
  </div></div>
  <div class="hallCtl"><button class="tbtn" onclick="hallSpin(-38)">‹ 左转</button><button class="tbtn" onclick="hallSpin(38)">右转 ›</button><span class="note">拖动环视 · 点击展墙直达</span></div>
'''
s=s[:i]+HALL+s[j+len('</section>'):]
i,j=cut('let hallA=0,hallDrag=null;','function clsAsk(){')
JS='''let hallA=0,hallDrag=null;
function hallInit(){const r=document.getElementById("hallRoom");if(!r||r.dataset.init)return;r.dataset.init="1";
 r.addEventListener("dragstart",e=>e.preventDefault());
 r.addEventListener("pointerdown",e=>{e.preventDefault();hallDrag={x:e.clientX,a:hallA,m:0};try{r.setPointerCapture(e.pointerId)}catch(_){}});
 r.addEventListener("pointermove",e=>{if(!hallDrag)return;const dx=e.clientX-hallDrag.x;hallDrag.m=Math.max(hallDrag.m,Math.abs(dx));hallA=hallDrag.a+dx*.25;applyHall()});
 r.addEventListener("pointerup",e=>{if(hallDrag&&hallDrag.m<6){const w=e.target.closest&&e.target.closest(".wall");if(w&&w.dataset.go)showTab(w.dataset.go)}hallDrag=null});
 r.addEventListener("pointercancel",()=>hallDrag=null);}
function applyHall(){const r=document.getElementById("hallRoom");if(r)r.style.transform="translateZ(-30px) rotateY("+hallA+"deg)"}
function hallSpin(d){hallA+=d;applyHall()}
'''
s=s[:i]+JS+s[j:]
rep('.wall{position:absolute;inset:0;border-radius:16px;padding:26px 30px;display:flex;flex-direction:column;gap:8px;justify-content:center;align-items:flex-start;backface-visibility:hidden;box-shadow:inset 0 0 60px rgba(0,0,0,.5)}',
'''.wall{position:absolute;inset:8% 6%;border-radius:14px;padding:20px;display:flex;align-items:center;justify-content:center;backface-visibility:hidden;box-shadow:inset 0 0 60px rgba(0,0,0,.5);cursor:pointer;user-select:none;-webkit-user-drag:none}
.wall:before{content:"";position:absolute;top:-8%;left:18%;right:18%;height:55%;background:radial-gradient(ellipse at top,rgba(255,240,200,.16),transparent 72%);pointer-events:none}
.frame{background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.4);border-radius:12px;padding:20px 30px;box-shadow:0 12px 34px rgba(0,0,0,.45),inset 0 0 0 7px rgba(255,255,255,.05);display:flex;flex-direction:column;gap:5px;align-items:center;text-align:center;transition:.2s;max-width:78%}
.wall:hover .frame{border-color:#FFE082;box-shadow:0 16px 44px rgba(0,0,0,.5),0 0 26px rgba(255,224,130,.3);transform:translateY(-3px)}
.fIc{font-size:46px;line-height:1.1}
.go{font-size:12.5px;color:#FFE082;font-weight:800;margin-top:2px}
.floor{position:absolute;left:-25%;right:-25%;bottom:-2%;height:22%;background:linear-gradient(#232E4A,#0B0F1A);transform:perspective(420px) rotateX(58deg);transform-origin:bottom;pointer-events:none}''')
rep('.wall .wT{font-size:22px;font-weight:800;color:#fff}','.wall .wT{font-size:21px;font-weight:800;color:#fff}')
rep('.wall .wD{font-size:14px;color:rgba(255,255,255,.75);margin-bottom:10px}','.wall .wD{font-size:13.5px;color:rgba(255,255,255,.78)}')
rep('.room{width:min(880px,90vw);height:52vh;min-height:360px;margin:7vh auto 0;position:relative;transform-style:preserve-3d;transition:transform .18s ease-out;cursor:grab}',
    '.room{width:min(880px,90vw);height:52vh;min-height:360px;margin:7vh auto 0;position:relative;transform-style:preserve-3d;transition:transform .18s ease-out;cursor:grab;user-select:none;-webkit-user-drag:none}')

# ═══ 9 首页地图卡 CSS ═══
rep('.mapEntry{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}',
'''.homeMap .hmHead{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:4px}
.hmSub{font-size:13.5px;font-weight:400;color:#8a7a6a}
.homeMap #homeMapBox .mapwrap{border-radius:12px}''')

open(P,"w",encoding="utf-8").write(s)
import os
print("v5m OK; %.2f MB"%(os.path.getsize(P)/1048576))
