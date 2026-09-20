#!/usr/bin/env python3
"""v5j：图谱页推倒重做=任务地图(蜿蜒路径9站/进度/下一站脉冲)+知识图谱(深色科技风:发光曲线边/分类霓虹节点/悬停高亮邻居/滚轮缩放/拖拽平移)；修着色(铁律节点)+完成事件实时刷新"""
import re
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

# ── 1 导航名 ──
rep("showTab('graph')\">🗺 图谱</button>","showTab('graph')\">🗺 任务地图</button>")
rep('graph:"这张图就是这门课的骨架——点任何节点直达课件原页；你练过的地方会亮绿"',
    'graph:"这就是这门课的寻宝路线：点亮一站是一站；右上角可切「知识图谱」看知识结构，点节点直达课件页"')

# ── 2 section HTML 重写 ──
i,j=cut('<section id="tab-graph">','</section>')
NEW='''<section id="tab-graph">
  <div class="eyebrow">🗺 任务地图 · 学到哪，走到哪（右上角可切知识图谱）</div>
  <div class="kgTabs"><button id="kgTabMap" class="chip on" onclick="setKgView('map')">🎒 任务地图</button><button id="kgTabGraph" class="chip" onclick="setKgView('graph')">🕸 知识图谱</button><span class="kprog" id="kgProg"></span></div>
  <div class="card" style="padding:0;overflow:hidden"><div id="kgBox"></div></div>
  <div class="note" style="margin-top:8px">站点全部出自课件与课堂任务：<b>完成检查器/跑过车间/提交审账/手势满分，对应站点自动点亮 ✓</b>；没点的站显示「下一站」脉冲引导。</div>
</section>'''
s=s[:i]+NEW+s[j+len('</section>'):]

# ── 3 JS 整块重写 ──
i,j=cut('const KG={nodes:[','function clsAsk(){')
JS='''const STOPS=[
 {id:"kai",t:"开场任务",d:"把你自己装进变量",icon:"🖊",page:["08",26]},
 {id:"kan",t:"看图认命令",d:"输入·打印·赋值",icon:"🖼",page:["08",32]},
 {id:"liu",t:"流程图",d:"把步骤画出来",icon:"📐",page:["17",7]},
 {id:"pan",t:"判断",d:"条件的岔路口",icon:"🔀",page:["17",6]},
 {id:"xun",t:"循环",d:"重复交给机器人",icon:"🔁",page:["17",8]},
 {id:"cun",t:"存钱罐",d:"车间·判断+循环",icon:"🐷",bot:"tank"},
 {id:"wai",t:"外卖·班费",d:"车间·顺序+判断",icon:"🍱",botAny:["waimai","banfei"]},
 {id:"shen",t:"审账复核",d:"AI复核·教师拍板",icon:"🧾",tab:"home"},
 {id:"shou",t:"手势五关",d:"全身答·课件判断题",icon:"🙌",tab:"gest"}];
const STXY=[[9,10],[30,6],[51,8],[72,6],[90,20],[70,30],[48,26],[26,38],[50,50]];
const GN=[
 {id:"var",t:"变量",c:0,x:32,y:11},{id:"type",t:"类型",c:0,x:12,y:28},{id:"cmd",t:"命令",c:0,x:52,y:28},
 {id:"flow",t:"流程图",c:1,x:32,y:45},{id:"if",t:"判断",c:1,x:13,y:63},{id:"loop",t:"循环",c:1,x:51,y:63},
 {id:"tank",t:"存钱罐",c:2,x:32,y:80},{id:"waimai",t:"外卖满减",c:2,x:10,y:80},{id:"banfei",t:"班费记账",c:2,x:54,y:80},
 {id:"audit",t:"审账复核",c:3,x:18,y:95},{id:"rule",t:"铁律",c:3,x:46,y:95}];
const GE=[["var","type"],["var","cmd"],["type","flow"],["cmd","flow"],["flow","if"],["flow","loop"],["if","tank"],["loop","tank"],["if","waimai"],["flow","banfei"],["tank","audit"],["tank","rule"],["waimai","audit"],["banfei","rule"]];
const GCOLOR=["#FFB74D","#4FC3F7","#81C784","#FFD54F"];
let kgView="map",kgV={x:0,y:0,s:1};
function stopDone(st){
 if(st.page)return !!(state.visited&&state.visited[st.page[0]+"-"+st.page[1]]);
 if(st.bot)return typeof bot!=="undefined"&&bot.last&&bot.proj===st.bot;
 if(st.botAny)return st.botAny.some(b=>typeof bot!=="undefined"&&bot.last&&bot.proj===b);
 if(st.tab==="home")return state.class.shf.done;
 if(st.tab==="gest")return g.score>=100;return false}
function stopGo(st){
 if(st.page){showTab("lib");libDeck(st.page[0]);dkState.lib.cur=st.page[1]-1;libShow();document.getElementById("libStage").scrollIntoView({behavior:"smooth",block:"start"})}
 else if(st.bot){showTab("bot");if(bot.proj!==st.bot){bot={proj:st.bot,vars:{},last:null};renderBot();dkMount("bot",DKRAIL[st.bot])}}
 else if(st.tab==="home"){showTab("home");const b=document.getElementById("shfBox");if(b)setTimeout(()=>b.scrollIntoView({behavior:"smooth",block:"center"}),80)}
 else if(st.tab==="gest")showTab("gest")}
function kgRefresh(){const t=document.getElementById("tab-graph");if(t&&t.classList.contains("on"))renderKG()}
function setKgView(v){kgView=v;
 document.getElementById("kgTabMap").classList.toggle("on",v==="map");
 document.getElementById("kgTabGraph").classList.toggle("on",v==="graph");
 kgV={x:0,y:0,s:1};renderKG()}
function kgProgText(){const n=STOPS.filter(stopDone).length;
 document.getElementById("kgProg").innerHTML="已点亮 <b>"+n+"</b> / "+STOPS.length+" 站"+(n===STOPS.length?" 🎉 全图通关！":"")}
function renderKG(){if(kgView==="map")renderMap();else renderGraph()}
function renderMap(){const box=document.getElementById("kgBox");if(!box)return;kgProgText();
 let doneCnt=0,path="",cur=-1;
 STOPS.forEach((st,i)=>{if(stopDone(st))doneCnt++;else if(cur<0)cur=i});
 let stations="",labels="";
 STOPS.forEach((st,i)=>{
  const [x,y]=STXY[i],done=stopDone(st),isCur=(i===cur);
  stations+='<circle class="stc'+(done?" done":isCur?" cur":"")+(isCur?" pulse":"")+'" cx="'+x+'" cy="'+y+'" r="5.6"/>';
  if(isCur)stations+='<circle class="string" cx="'+x+'" cy="'+y+'" r="5.6"/>';
  stations+='<text class="sti" x="'+x+'" y="'+(y+1.8)+'">'+st.icon+'</text>';
  if(done)stations+='<circle class="stb" cx="'+(x+4.6)+'" cy="'+(y-4.2)+'" r="2.3"/><text class="stbt" x="'+(x+4.6)+'" y="'+(y-3.1)+'">✓</text>';
  if(isCur){stations+='<rect class="stf" x="'+(x-8.5)+'" y="'+(y+8.2)+'" width="17" height="4.6" rx="2.3"/><text class="stft" x="'+x+'" y="'+(y+11.4)+'">下一站 ▶</text>'}
  labels+='<text class="stt'+(done?" d":"")+'" x="'+x+'" y="'+(y-8.2)+'">'+st.t+'</text>';});
 for(let k=0;k<STOPS.length-1;k++){const [x1,y1]=STXY[k],[x2,y2]=STOPS[k+1]&&STXY[k+1];
  const mx=(x1+x2)/2,my=(y1+y2)/2+(k%2?4:-4);
  path+='<path class="stp" d="M'+x1+' '+y1+' Q'+mx+' '+my+' '+x2+' '+y2+'"/>';}
 box.innerHTML='<div class="mapwrap"><svg viewBox="0 0 100 58">'+path+stations+labels+'</svg></div>';
 box.querySelectorAll(".stc,.sti").forEach(el=>{const idx=[...box.querySelectorAll(".stc")].indexOf(box.querySelector(".stc:not(.done)")) ;
  el.style.cursor="pointer";el.onclick=()=>stopGo(STOPS[[...box.querySelectorAll(".sti")].indexOf(el)>=0?[...box.querySelectorAll(".sti")].indexOf(el):0]||STOPS[0]);});
 const cs=[...box.querySelectorAll("svg g"===null?[]:[])];
 const circs=[...box.querySelectorAll(".stc,.sti,.stb,.string")];
 circs.forEach(el=>{el.style.cursor="pointer";el.addEventListener("click",ev=>{ev.stopPropagation();
   const idx=[...box.querySelectorAll(".stc")].indexOf(el.classList.contains("stc")?el:null);
   const iidx=[...box.querySelectorAll(".sti")].indexOf(el);
   const n=(idx>=0?idx:(iidx>=0?iidx:parseFloat((el.getAttribute&&el.getAttribute("cx"))||0)));});
 });
 box.querySelectorAll(".stc,.sti").forEach(el=>{el.onclick=()=>{const arr=[...box.querySelectorAll(".sti")];const i=el.classList&&el.classList.contains("sti")?arr.indexOf(el):arr.indexOf(el);stopGo(STOPS[Math.max(0,arr.indexOf(el)>=0?arr.indexOf(el):0)])}});
}
function renderGraph(){const box=document.getElementById("kgBox");if(!box)return;kgProgText();
 const N=(id)=>GN.find(n=>n.id===id);
 const got={};GN.forEach(n=>{got[n.id]=n.c===3?(state.class.shf.done||g.score>=100):(n.id==="audit"?state.class.shf.done:(n.id==="var"||n.id==="type")?state.class.pv.done:(typeof bot!=="undefined"&&bot.last&&bot.proj===n.id))});
 got.audit=state.class.shf.done;got.rule=state.class.shf.done||g.score>=100;
 let edges="",nodes="";
 GE.forEach(e=>{const a=N(e[0]),b=N(e[1]);const mx=(a.x+b.x)/2+(b.y-a.y)*.14,my=(a.y+b.y)/2-(b.x-a.x)*.14;
  edges+='<path class="ge'+(got[b.id]?" on":"")+'" data-a="'+a.id+'" data-b="'+b.id+'" d="M'+a.x+' '+(a.y+6)+' Q'+mx+' '+my+' '+b.x+' '+(b.y-6)+'"/>';});
 GN.forEach((n,i)=>{nodes+='<g class="gn'+(got[n.id]?" on":"")+'" data-id="'+n.id+'" style="animation-delay:'+(i*55)+'ms" transform="translate('+n.x+','+n.y+')">'
  +'<circle class="gnc c'+n.c+'" r="6.2"/><text class="gnt" y="-8.6">'+n.t+'</text><text class="gnd" y="12.2">'+(n.c===3?"素养":(n.c===2?"任务":(n.c===1?"结构":"基础")))+'</text>'
  +(got[n.id]?'<text class="gk" x="4.6" y="-5.4">✓</text>':"")+'</g>';});
 box.innerHTML='<div class="gwrap"><div class="gctl"><button class="tbtn" onclick="kgZoom(1.25)">＋</button><button class="tbtn" onclick="kgZoom(.8)">－</button><button class="tbtn" onclick="kgReset()">重置</button><span class="gnote">滚轮缩放 · 拖拽平移 · 悬停看邻居</span></div>'
  +'<svg id="kgSvg" viewBox="0 0 64 103"><g id="kgT" transform="translate(0,0) scale(1)">'+edges+nodes+'</g></svg></div>';
 const svg=document.getElementById("kgSvg");
 svg.addEventListener("wheel",ev=>{ev.preventDefault();const f=ev.deltaY<0?1.12:.89;kgZoomAt(f,ev);},{passive:false});
 let drag=null;
 svg.addEventListener("pointerdown",ev=>{drag={x:ev.clientX,y:ev.clientY,ox:kgV.x,oy:kgV.y};svg.setPointerCapture(ev.pointerId)});
 svg.addEventListener("pointermove",ev=>{if(!drag)return;const r=svg.getBoundingClientRect();
  kgV.x=drag.ox+(ev.clientX-drag.x)*64/r.width;kgV.y=drag.oy+(ev.clientY-drag.y)*103/r.height;applyT()});
 svg.addEventListener("pointerup",()=>drag=null);
 svg.querySelectorAll(".gn").forEach(g=>{
  g.addEventListener("mouseenter",()=>{svg.classList.add("dim");const id=g.dataset.id;
   svg.querySelectorAll(".ge").forEach(p=>{if(p.dataset.a===id||p.dataset.b===id)p.classList.add("lit")});
   const nb=new Set([id]);GE.forEach(e=>{if(e[0]===id)nb.add(e[1]);if(e[1]===id)nb.add(e[0])});
   svg.querySelectorAll(".gn").forEach(x=>{if(nb.has(x.dataset.id))x.classList.add("lit")});});
  g.addEventListener("mouseleave",()=>{svg.classList.remove("dim");svg.querySelectorAll(".lit").forEach(x=>x.classList.remove("lit"))});
  g.addEventListener("click",()=>{const n=N(g.dataset.id);
   const st=STOPS.find(s=>(n.id==="var"||n.id==="type")?s.id==="kai":s.id===(n.id==="cmd"?"kan":n.id==="flow"?"liu":n.id==="if"?"pan":n.id==="loop"?"xun":n.id==="tank"?"cun":n.id==="waimai"||n.id==="banfei"?"wai":n.id==="audit"?"shen":"shou"));
   if(st)stopGo(st);});});
 applyT();}
function applyT(){const g=document.getElementById("kgT");if(g)g.setAttribute("transform","translate("+kgV.x+","+kgV.y+") scale("+kgV.s+")")}
function kgZoom(f){kgV.s=Math.min(4,Math.max(.6,kgV.s*f));applyT()}
function kgZoomAt(f,ev){const svg=document.getElementById("kgSvg");const r=svg.getBoundingClientRect();
 const vx=(ev.clientX-r.left)/r.width*64,vy=(ev.clientY-r.top)/r.height*103;
 const ns=Math.min(4,Math.max(.6,kgV.s*f));kgV.x=vx-(vx-kgV.x)*(ns/kgV.s);kgV.y=vy-(vy-kgV.y)*(ns/kgV.s);kgV.s=ns;applyT()}
function kgReset(){kgV={x:0,y:0,s:1};applyT()}
'''
s=s[:i]+JS+s[j:]

# ── 4 CSS 重写 ──
i2=s.find('#kgBox .kge{');j2=s.find('#xyFace .xm{',i2)
KG_CSS='''.kgTabs{display:flex;gap:8px;align-items:center;margin:0 0 10px;flex-wrap:wrap}
.kgTabs .chip.on{background:#8C1F28;color:#fff;border-color:#8C1F28}
.kprog{margin-left:auto;font-size:14.5px;color:#4a2c1e}
.kprog b{color:#2E6B2E;font-size:16px}
.mapwrap{background:linear-gradient(180deg,#FFF9EE,#FDEFD8);padding:8px}
.mapwrap svg{width:100%;display:block}
.stp{fill:none;stroke:#D8B888;stroke-width:1.1;stroke-dasharray:2.6 2.2;animation:dashf 1.6s linear infinite}
@keyframes dashf{to{stroke-dashoffset:-4.8}}
.stc{fill:#fff;stroke:#C9A87E;stroke-width:.6;transition:.2s}
.stc.done{fill:#DFF0DF;stroke:#2E6B2E;stroke-width:.9}
.stc.cur{stroke:#B5433A;stroke-width:1}
.string{fill:none;stroke:#B5433A;stroke-width:.7;transform-box:fill-box;transform-origin:center;animation:pulse 1.6s ease-out infinite}
@keyframes pulse{0%{transform:scale(1);opacity:.9}100%{transform:scale(2.1);opacity:0}}
.sti{font-size:5.6px;text-anchor:middle;pointer-events:none}
.stb{fill:#2E6B2E}
.stbt{font-size:2.6px;fill:#fff;text-anchor:middle;pointer-events:none}
.stf{fill:#B5433A;opacity:.94}
.stft{font-size:2.7px;fill:#fff;text-anchor:middle;font-weight:700}
.stt{font-size:3px;font-weight:800;fill:#4a2c1e;text-anchor:middle}
.stt.d{fill:#2E6B2E}
.gwrap{background:linear-gradient(160deg,#0E1424,#1A2338);padding:10px;position:relative}
.gctl{display:flex;gap:6px;align-items:center;margin-bottom:6px}
.gctl .tbtn{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.25)}
.gnote{font-size:12.5px;color:rgba(255,255,255,.55);margin-left:auto}
.gwrap svg{width:100%;display:block;touch-action:none;cursor:grab}
.gwrap svg:active{cursor:grabbing}
.ge{fill:none;stroke:url(#none);stroke:#3D5A8A;stroke-width:.5;opacity:.45;transition:.25s}
.ge.on{stroke:#5EC8F2;stroke-width:.62;opacity:.85;stroke-dasharray:2.4 2;animation:gflow 1.3s linear infinite}
@keyframes gflow{to{stroke-dashoffset:-4.4}}
.gn{cursor:pointer;transform-box:fill-box;transform-origin:center;animation:gpop .45s backwards}
@keyframes gpop{from{opacity:0;transform:scale(.3)}}
.gnc{transition:.25s;stroke-width:.7}
.c0{fill:#FFB74D;stroke:#A56A1C}.c1{fill:#4FC3F7;stroke:#1C74A5}.c2{fill:#81C784;stroke:#3D7A42}.c3{fill:#FFD54F;stroke:#A58A1C}
.gn.on .gnc{filter:drop-shadow(0 0 1.6px currentColor)}
.gn.on.c .gnc{}
.gn.on .c0{stroke:#FFE082}.gn.on .c1{stroke:#B3E5FC}.gn.on .c2{stroke:#C8E6C9}.gn.on .c3{stroke:#FFF3C0}
.gnt{font-size:3.4px;font-weight:800;fill:#EAF2FF;text-anchor:middle}
.gnd{font-size:2.2px;fill:#8FA3C8;text-anchor:middle}
.gk{font-size:3.2px;fill:#9CF2B0;font-weight:800}
svg.dim .gn{opacity:.13}svg.dim .ge{opacity:.07}
svg.dim .gn.lit,svg.dim .ge.lit{opacity:1}
'''
s=s[:i2]+KG_CSS+s[j2:]

# ── 5 访问记录 + 实时刷新钩子 ──
rep('  stage.onclick=()=>dkRevealCur(zone);',
'''  state.visited=state.visited||{};if(!state.visited[key]){state.visited[key]=1;persist();kgRefresh();}
  stage.onclick=()=>dkRevealCur(zone);''')
rep('persist();renderSHF();\n}','persist();renderSHF();kgRefresh();\n}')
rep('fabNudge("跑完了！对照上面「图纸」看每一步——再改一个数跑一次，看看结果怎么变","runbot");',
    'fabNudge("跑完了！对照上面「图纸」看每一步——再改一个数跑一次，看看结果怎么变","runbot");kgRefresh();')
rep('sfx("done");sayVoice("done");fabNudge("五关全过！把「为什么」讲给同桌听——讲明白才算真会","gdone");',
    'sfx("done");sayVoice("done");fabNudge("五关全过！把「为什么」讲给同桌听——讲明白才算真会","gdone");kgRefresh();')

open(P,"w",encoding="utf-8").write(s)
import os
print("v5j OK; %.2f MB"%(os.path.getsize(P)/1048576))
