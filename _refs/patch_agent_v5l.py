#!/usr/bin/env python3
"""v5l：图谱悬浮工具条+真收缩+视觉升级(渐变球/光晕环/星点/双层边)；地图裁字修复+返回地图chip+本次课/全课程；教师台/关于右上角；课件馆书架卡；首页地图入口卡；3D展厅；小邮讲解按钮+知识库徽标"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)

rep("（公开页数据已匿名） ｜ v5.2 任务地图版`;","（公开页数据已匿名） ｜ v5.3 展厅版`;")
rep('''  <button id="tb-teach" onclick="showTab('teach')">📋 教师台</button>
  <button id="tb-about" onclick="showTab('about')">ℹ️ 关于小邮</button>
</div></nav>''',
'''  <button id="tb-hall" onclick="showTab('hall')">🏢 展厅</button>
</div><div class="corner">
  <button id="tb-teach" onclick="showTab('teach')">🧑‍🏫 教师台</button>
  <button id="tb-about" onclick="showTab('about')">ℹ️ 关于</button>
</div></nav>''')
rep('<div class="gctl"><button class="tbtn" onclick="kgZoom(1.25)">＋</button><button class="tbtn" onclick="kgZoom(.8)">－</button><button class="tbtn" onclick="kgReset()">重置</button><span class="kchip kc0" data-c="0" onclick="kgToggleC(0)">基础</span><span class="kchip kc1" data-c="1" onclick="kgToggleC(1)">结构</span><span class="kchip kc2" data-c="2" onclick="kgToggleC(2)">任务</span><span class="kchip kc3" data-c="3" onclick="kgToggleC(3)">素养</span><span class="gnote">滚轮缩放 · 拖拽平移 · 悬停看邻居</span></div>',
'<div class="gctl"><span class="kchip kc0" data-c="0" onclick="kgToggleC(0)">基础</span><span class="kchip kc1" data-c="1" onclick="kgToggleC(1)">结构</span><span class="kchip kc2" data-c="2" onclick="kgToggleC(2)">任务</span><span class="kchip kc3" data-c="3" onclick="kgToggleC(3)">素养</span><button class="tbtn" onclick="kgZoom(1.25)">＋</button><button class="tbtn" onclick="kgZoom(.8)">－</button><button class="tbtn" onclick="kgReset()">⌂</button></div><div class="ghint">滚轮缩放 · 拖拽平移 · 悬停看邻居 · 点胶囊收起一类</div>')
rep('const GCOLOR=["#FFB74D","#4FC3F7","#81C784","#FFD54F"];',
'''const GCOLOR=["#FFB74D","#4FC3F7","#81C784","#FFD54F"];
const GRAD='<defs><radialGradient id="gr0" cx="35%" cy="30%"><stop offset="0" stop-color="#FFE0B2"/><stop offset="1" stop-color="#FF9800"/></radialGradient><radialGradient id="gr1" cx="35%" cy="30%"><stop offset="0" stop-color="#B3E5FC"/><stop offset="1" stop-color="#039BE5"/></radialGradient><radialGradient id="gr2" cx="35%" cy="30%"><stop offset="0" stop-color="#C8E6C9"/><stop offset="1" stop-color="#43A047"/></radialGradient><radialGradient id="gr3" cx="35%" cy="30%"><stop offset="0" stop-color="#FFF3C0"/><stop offset="1" stop-color="#FFB300"/></radialGradient></defs>';
const STOPS_CLS=[
 {id:"c1",t:"开场任务",d:"建5个变量",icon:"🖊",page:["08",26]},
 {id:"c2",t:"命令三要素",d:"输入·赋值·打印",icon:"⌨",page:["08",28]},
 {id:"c3",t:"看图认命令",d:"三行命令对照",icon:"🖼",page:["08",32]},
 {id:"c4",t:"打印店案例",d:"打印的用场",icon:"🖨",page:["08",34]},
 {id:"c5",t:"下课挑战",d:"可选·不占分",icon:"🏁",page:["08",44]}];
const STXY_CLS=[[10,14],[33,8],[56,14],[78,8],[52,30]];
let kgScope="all";
function setKgScope(v){kgScope=v;document.getElementById("kgScCls").classList.toggle("on",v==="cls");document.getElementById("kgScAll").classList.toggle("on",v==="all");kgView="map";renderKG()}''')
rep('<button id="kgTabGraph" class="chip" onclick="setKgView(\'graph\')">🕸 知识图谱</button><span class="kprog"',
    '<button id="kgTabGraph" class="chip" onclick="setKgView(\'graph\')">🕸 知识图谱</button><button id="kgScCls" class="chip" onclick="setKgScope(\'cls\')">本次课</button><button id="kgScAll" class="chip on" onclick="setKgScope(\'all\')">全课程</button><span class="kprog"')
i=s.find("function renderMap(){");j=s.find("function renderGraph(){")
assert i>0 and j>i
NEW='''function renderMap(){const box=document.getElementById("kgBox");if(!box)return;
 const stops=kgScope==="cls"?STOPS_CLS:STOPS,XY=kgScope==="cls"?STXY_CLS:STXY;
 let cur=-1;stops.forEach((st,i)=>{if(cur<0&&!stopDone(st))cur=i});
 let n=0;stops.forEach(st=>{if(stopDone(st))n++});
 document.getElementById("kgProg").innerHTML="已点亮 <b>"+n+"</b> / "+stops.length+" 站"+(n===stops.length?" 🎉 全图通关！":"");
 let path="";
 for(let k=0;k<stops.length-1;k++){const p1=XY[k],p2=XY[k+1];
  const mx=(p1[0]+p2[0])/2,my=(p1[1]+p2[1])/2+(k%2?4:-4);
  path+='<path class="stp" d="M'+p1[0]+' '+p1[1]+' Q'+mx+' '+my+' '+p2[0]+' '+p2[1]+'"/>';}
 let stations="",labels="";
 stops.forEach((st,i)=>{const x=XY[i][0],y=XY[i][1],done=stopDone(st),isCur=(i===cur);
  let g='<g class="stG" data-i="'+i+'">';
  g+='<circle class="stc'+(done?" done":isCur?" cur":"")+'" cx="'+x+'" cy="'+y+'" r="5.6"/>';
  if(isCur)g+='<circle class="string" cx="'+x+'" cy="'+y+'" r="5.6"/>';
  g+='<text class="sti" x="'+x+'" y="'+(y+1.9)+'">'+st.icon+'</text>';
  if(done)g+='<circle class="stb" cx="'+(x+4.6)+'" cy="'+(y-4.2)+'" r="2.3"/><text class="stbt" x="'+(x+4.6)+'" y="'+(y-3.2)+'">✓</text>';
  if(isCur)g+='<rect class="stf" x="'+(x-8.5)+'" y="'+(y+8.2)+'" width="17" height="4.6" rx="2.3"/><text class="stft" x="'+x+'" y="'+(y+11.5)+'">下一站 ▶</text>';
  g+='</g>';stations+=g;
  labels+='<text class="stt'+(done?" d":"")+'" x="'+x+'" y="'+(y-8.8)+'">'+st.t+'</text>';});
 box.innerHTML='<div class="mapwrap"><svg viewBox="0 -9 100 72">'+path+stations+labels+'</svg></div>';
 box.querySelectorAll(".stG").forEach(g=>{g.style.cursor="pointer";g.onclick=()=>stopGo(stops[+g.dataset.i])});
}
'''
s=s[:i]+NEW+s[j:]
rep(''' GE.forEach(e=>{const a=N(e[0]),b=N(e[1]);const mx=(a.x+b.x)/2+(b.y-a.y)*.14,my=(a.y+b.y)/2-(b.x-a.x)*.14;
  edges+='<path class="ge'+(got[b.id]?" on":"")+'" data-a="'+a.id+'" data-b="'+b.id+'" d="M'+a.x+' '+(a.y+6)+' Q'+mx+' '+my+' '+b.x+' '+(b.y-6)+'"/>';});''',
''' GE.forEach(e=>{const a=N(e[0]),b=N(e[1]);const mx=(a.x+b.x)/2+(b.y-a.y)*.14,my=(a.y+b.y)/2-(b.x-a.x)*.14;
  const d='M'+a.x+' '+(a.y+6)+' Q'+mx+' '+my+' '+b.x+' '+(b.y-6);
  edges+='<path class="geu" data-a="'+a.id+'" data-b="'+b.id+'" d="'+d+'"/>';
  edges+='<path class="ge'+(got[b.id]?" on":"")+'" data-a="'+a.id+'" data-b="'+b.id+'" d="'+d+'"/>';});''')
rep('''nodes+='<g class="gn'+(got[n.id]?" on":"")+'" data-id="'+n.id+'" style="animation-delay:'+(i*55)+'ms" transform="translate('+n.x+','+n.y+')">'
  +'<circle class="gnc c'+n.c+'" r="6.2"/><text class="gnt" y="-8.6">'+n.t+'</text><text class="gnd" y="12.2">'+(n.c===3?"素养":(n.c===2?"任务":(n.c===1?"结构":"基础")))+'</text>'
  +(got[n.id]?'<text class="gk" x="4.6" y="-5.4">✓</text>':"")+'</g>';});''',
'''nodes+='<g class="gn'+(got[n.id]?" on":"")+'" data-id="'+n.id+'" style="animation-delay:'+(i*55)+'ms" transform="translate('+n.x+','+n.y+')">'
  +'<circle class="ghalo" r="9.5"/><circle class="gnc" fill="url(#gr'+n.c+')" stroke="'+GCOLOR[n.c]+'" stroke-width=".55" r="6.2"/><text class="gnt" y="-8.6">'+n.t+'</text><text class="gnd" y="12.2">'+(n.c===3?"素养":(n.c===2?"任务":(n.c===1?"结构":"基础")))+'</text>'
  +(got[n.id]?'<text class="gk" x="4.6" y="-5.4">✓</text>':"")+'</g>';});''')
rep(''''+edges+nodes+'</g></svg></div>';''',''''+GRAD+edges+nodes+'</g></svg></div>';''')
rep('''svg.querySelectorAll(".gn").forEach(x=>{const n=N(x.dataset.id);if(kgHide[n.c]){x.style.opacity=.14;const c=x.querySelector(".gnc");if(c)c.style.transform="scale(.55)"}});
 svg.querySelectorAll(".ge").forEach(p=>{const a=N(p.dataset.a),b=N(p.dataset.b);if(kgHide[a.c]||kgHide[b.c])p.style.opacity=.05;});''',
'''svg.querySelectorAll(".gn").forEach(x=>{const n=N(x.dataset.id);if(kgHide[n.c]){x.style.opacity=0;x.style.transform="scale(0)";x.style.pointerEvents="none"}});
 svg.querySelectorAll(".ge,.geu").forEach(p=>{const a=N(p.dataset.a||p.dataset.b),b=N(p.dataset.b||p.dataset.a);if(kgHide[a.c]||kgHide[b.c])p.style.display="none";});''')
rep('''  stage.onclick=()=>dkRevealCur(zone);''',
'''  if(window.__fromMap){window.__fromMap=0;const bm=document.createElement("button");bm.className="tbtn backmap";bm.textContent="↩ 回任务地图";bm.onclick=()=>showTab("graph");stage.appendChild(bm);}
  stage.onclick=()=>dkRevealCur(zone);''')
rep('''function stopGo(st){
 if(st.page){''','''function stopGo(st){
 window.__fromMap=1;
 if(st.page){''')
rep("const LIBRAILS=","const LDECKDESC={\"10\":\"机器人第一次跑起来\",\"14\":\"把纸上的图纸搬进电脑\",\"16\":\"让机器人重复干活\",\"17\":\"判断＋循环·参赛精修\",\"04\":\"开学第一课·认识课程\",\"08\":\"变量命令流程·本节课主课件\"};\nconst LIBRAILS=")
rep('''document.getElementById("libDeckRail").innerHTML=Object.keys(LIBDECKS).map(x=>'<button class="railBtn'+(x===d?" on":"")+'" onclick="libDeck(\\''+x+'\\')">'+LIBDECKS[x].name+"</button>").join("");''',
'''document.getElementById("libDeckRail").innerHTML=Object.keys(LIBDECKS).map(x=>'<button class="deckCard'+(x===d?" on":"")+'" onclick="libDeck(\\''+x+'\\')"><b>'+LIBDECKS[x].name+'</b><span>'+LDECKDESC[x]+' · '+LIBRAILS[x].length+' 页</span></button>').join("");''')
rep('''  <div class="card"><h3>🙋 30 秒体验：你判断，AI 复核，老师拍板''',
'''  <div class="card mapEntry"><div><h3 style="margin:0 0 4px">🗺 学习任务地图</h3><div class="note" style="margin:0">学到哪，走到哪——完成一站点亮一站，做完回地图领下一站。</div></div>
    <div class="meBtns"><button class="btn" onclick="setKgScope('cls');showTab('graph')">本次课 · 命令 5 站</button><button class="btn o" onclick="setKgScope('all');showTab('graph')">全课程 · 9 站</button></div></div>
  <div class="card"><h3>🙋 30 秒体验：你判断，AI 复核，老师拍板''')
rep('''<section id="tab-graph">''',
'''<section id="tab-hall">
  <div class="eyebrow">🏢 虚拟展厅 · 拖一拖，环视整个作品（每面墙都能点进去）</div>
  <div class="hallStage"><div class="room" id="hallRoom">
    <div class="wall w1"><div class="wT">📖 课件馆 · 6 份课件 154 页</div><div class="wD">全部课件真页整馆入住，评委翻的就是我课堂用的</div><button class="btn" onclick="showTab('lib')">进课件馆</button></div>
    <div class="wall w2"><div class="wT">🙋 核心机制 · 你判断 AI 复核老师拍板</div><div class="wD">30 秒亲手走一遍全站铁律；检查器选错翻脸、全对消名</div><button class="btn" onclick="showTab('home')">去体验</button></div>
    <div class="wall w3"><div class="wT">🙌 用手答 · 机器人真跑</div><div class="wD">本地手势识别＋真人示范；车间改参数先猜再跑</div><button class="btn" onclick="showTab('gest')">手势闯关</button></div>
    <div class="wall w4"><div class="wT">🗺 地图 · 语音 · 教师台</div><div class="wD">任务地图点亮进度；小邮 12 句语音；AI 备课预演</div><button class="btn" onclick="setKgScope('all');showTab('graph')">看任务地图</button></div>
  </div></div>
  <div class="hallCtl"><button class="tbtn" onclick="hallSpin(-38)">‹ 左转</button><button class="tbtn" onclick="hallSpin(38)">右转 ›</button><span class="note">按住拖动也可以转</span></div>
"</section>
<section id="tab-graph">''')
rep('if(t==="graph")renderKG();','if(t==="graph")renderKG();if(t==="hall")hallInit();')
rep('function clsAsk(){',
'''let hallA=0,hallDrag=null;
function hallInit(){const r=document.getElementById("hallRoom");if(!r||r.dataset.init)return;r.dataset.init="1";
 r.addEventListener("pointerdown",e=>{hallDrag={x:e.clientX,a:hallA};r.setPointerCapture(e.pointerId)});
 r.addEventListener("pointermove",e=>{if(!hallDrag)return;hallA=hallDrag.a+(e.clientX-hallDrag.x)*.25;applyHall()});
 r.addEventListener("pointerup",()=>hallDrag=null);}
function applyHall(){const r=document.getElementById("hallRoom");if(r)r.style.transform="translateZ(-30px) rotateY("+hallA+"deg)"}
function hallSpin(d){hallA+=d;applyHall()}
function clsAsk(){''')
rep('''<div class="heroBtns"><button class="hbtn" onclick="showTab('class')">🏫 进课堂同步（课件真页）</button><button class="hbtn o" onclick="showTab('bot')">🤖 机器人车间</button></div>''',
'''<div class="heroBtns"><button class="hbtn" onclick="showTab('class')">🏫 进课堂同步（课件真页）</button><button class="hbtn o" onclick="showTab('bot')">🤖 机器人车间</button><button class="hbtn o" onclick="sayVoice('hello');const c=document.getElementById('heroCap');if(c)c.style.display='block'">🔊 让小邮讲解</button></div><div class="say" id="heroCap" style="display:none;margin-top:8px">🔊 小邮：大家好，我是小邮——课件在我这儿原页重玩，机器人真能跑，卡住了随时问我！</div>''')
rep('<b>小邮伴学 · 有问题问我</b>','<b>小邮伴学 · 有问题问我</b><span class="aiKb">AI 知识库·本地优先</span>')
rep('.gv figcaption{text-align:center;font-size:12.5px;margin-top:3px;color:#6b5d52;font-weight:700}',
'''.gv figcaption{text-align:center;font-size:12.5px;margin-top:3px;color:#6b5d52;font-weight:700}
nav .nin{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
nav .corner{margin-left:auto;display:flex;gap:6px}
nav .corner button{font-size:13px;padding:7px 12px;opacity:.92}
.geu{fill:none;stroke:#4A6FB5;stroke-width:1.5;opacity:.1}
.ghalo{fill:none;stroke:rgba(160,200,255,.15);stroke-width:.45;stroke-dasharray:1.8 1.6;transform-box:fill-box;transform-origin:center;animation:gspin 16s linear infinite}
@keyframes gspin{to{transform:rotate(360deg)}}
.gstars{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1.5px),radial-gradient(rgba(140,180,255,.12) 1px,transparent 1.5px);background-size:46px 46px,29px 29px;background-position:0 0,14px 22px;pointer-events:none}
.gwrap{position:relative}
.gctl{position:absolute;top:12px;right:12px;display:flex;gap:5px;align-items:center;z-index:5;flex-wrap:wrap;max-width:60%;justify-content:flex-end}
.gctl .tbtn{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.25);padding:4px 10px;font-size:13px}
.ghint{position:absolute;left:12px;bottom:8px;font-size:11.5px;color:rgba(255,255,255,.4);z-index:5}
.deckCard{display:flex;flex-direction:column;gap:2px;align-items:flex-start;border:1.5px solid #E7D8C2;background:#fff;border-radius:12px;padding:8px 12px;cursor:pointer;transition:.15s}
.deckCard b{font-size:14px;color:#4a2c1e}
.deckCard span{font-size:12px;color:#8a7a6a}
.deckCard.on{border-color:#8C1F28;background:#FBEDEA}
.deckCard.on b{color:#8C1F28}
.deckCard:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(140,31,40,.12)}
#libDeckRail{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px;width:100%}
.mapEntry{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.meBtns{display:flex;gap:8px;flex-wrap:wrap}
.backmap{position:absolute;top:10px;right:10px;z-index:9;box-shadow:0 4px 14px rgba(80,20,20,.25)}
.stage{position:relative}
.hallStage{perspective:1150px;height:66vh;min-height:420px;overflow:hidden;background:radial-gradient(ellipse at center,#1C2438,#0B0F1A);border-radius:18px;border:1px solid #2A3550;position:relative}
.room{width:min(880px,90vw);height:52vh;min-height:360px;margin:7vh auto 0;position:relative;transform-style:preserve-3d;transition:transform .18s ease-out;cursor:grab}
.room:active{cursor:grabbing}
.wall{position:absolute;inset:0;border-radius:16px;padding:26px 30px;display:flex;flex-direction:column;gap:8px;justify-content:center;align-items:flex-start;backface-visibility:hidden;box-shadow:inset 0 0 60px rgba(0,0,0,.5)}
.wall .wT{font-size:22px;font-weight:800;color:#fff}
.wall .wD{font-size:14px;color:rgba(255,255,255,.75);margin-bottom:10px}
.w1{background:linear-gradient(135deg,#5D1A22,#8C2430);transform:rotateY(0deg) translateZ(-300px)}
.w2{background:linear-gradient(135deg,#153A2C,#1F5A41);transform:rotateY(90deg) translateZ(-300px)}
.w3{background:linear-gradient(135deg,#1E2C4E,#2E4478);transform:rotateY(180deg) translateZ(-300px)}
.w4{background:linear-gradient(135deg,#4A3510,#7A5A1E);transform:rotateY(270deg) translateZ(-300px)}
.hallCtl{display:flex;gap:8px;align-items:center;margin-top:10px}
.aiKb{margin-left:8px;font-size:10.5px;background:#EAF3EA;color:#2E6B2E;border-radius:999px;padding:2px 8px;font-weight:700;white-space:nowrap}''')
open(P,"w",encoding="utf-8").write(s)
import os
print("v5l OK; %.2f MB"%(os.path.getsize(P)/1048576))
