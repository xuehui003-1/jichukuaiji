# -*- coding: utf-8 -*-
# v6.5：①图谱=CSS 3D 知识大厦(四层楼板视差+跨层投影虚线+拖拽旋转+滚轮缩放+双击复位)
# ②卡牌质感增强(双线内框/角徽/呢绒牌桌/悬浮抬起/判定面花纹背) ③首页动线重组(懂规矩撤→机器人车间;特色升第二步;导览5钮)
# ④任务地图站→mapGo+右下「返回任务地图」浮标 ⑤名字消消乐=B3XYL(自动进消名全屏+h2改"完成任务后举手，老师消名字")
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 图谱辅助函数 ═══
rep("let kgView=\"graph\",kgV={x:0,y:0,s:1};", "let kgView=\"graph\",kgV={x:0,y:50,s:1};")
pass  # applyT/mapGo/mapBackGo 在 renderGraph 替换后插入(见下)
rep('''function kgZoomAt(f,ev){const svg=document.getElementById("kgSvg");const r=svg.getBoundingClientRect();
 const vx=(ev.clientX-r.left)/r.width*120,vy=(ev.clientY-r.top)/r.height*72;
 const ns=Math.min(4,Math.max(.6,kgV.s*f));kgV.x=vx-(vx-kgV.x)*(ns/kgV.s);kgV.y=vy-(vy-kgV.y)*(ns/kgV.s);kgV.s=ns;applyT()}''',
    'function kgZoomAt(f){kgV.s=Math.min(2.2,Math.max(.55,kgV.s*f));applyT()}')
rep('function kgReset(){kgV={x:0,y:0,s:1};applyT()}', 'function kgReset(){kgV={x:0,y:50,s:1};applyT()}')

# ═══ 2 renderGraph 整体替换为 3D 构建器 ═══
a = s.find("function renderGraph(){")
b = s.find("\nfunction kgZoomAt", a)
assert 0 < a < b
NEW = '''function renderGraph(){const box=document.getElementById("kgBox");if(!box)return;kgProgText();
 const N=(id)=>GN.find(n=>n.id===id);
 const got={};GN.forEach(n=>{got[n.id]=n.c===3?(state.class.shf.done||g.score>=100):(n.id==="audit"?state.class.shf.done:(n.id==="var"||n.id==="type")?state.class.pv.done:(typeof bot!=="undefined"&&bot.last&&bot.proj===n.id))});
 got.audit=state.class.shf.done;got.rule=state.class.shf.done||g.score>=100;
 const P={var:[150,120],type:[320,148],cmd:[500,110],flow:[300,118],if:[470,170],loop:[578,76],banfei:[150,118],waimai:[330,160],tank:[500,103],audit:[350,130],rule:[520,152]};
 const FL=[{t:"① 基础概念层",ids:["var","type","cmd"]},{t:"② 流程结构层",ids:["flow","if","loop"]},{t:"③ 任务应用层",ids:["banfei","waimai","tank"]},{t:"④ 素养沉淀层",ids:["audit","rule"]}];
 const FI=(id)=>FL.findIndex(f=>f.ids.includes(id));
 let fls="";
 FL.forEach((f,fi)=>{
  let lines="",nds="";
  GE.forEach(e=>{const a2=N(e[0]),b2=N(e[1]);const pa=P[a2.id],pb=P[b2.id];const fa=FI(a2.id),fb=FI(b2.id);
   if(fa===fi&&fb===fi){
    const ang=Math.atan2(pb[1]-pa[1],pb[0]-pa[0]);const ex=pb[0]-Math.cos(ang)*17,ey=pb[1]-Math.sin(ang)*17;
    const sx1=(ex-Math.cos(ang-2.5)*7).toFixed(1),sy1=(ey-Math.sin(ang-2.5)*7).toFixed(1),sx2=(ex-Math.cos(ang+2.5)*7).toFixed(1),sy2=(ey-Math.sin(ang+2.5)*7).toFixed(1);
    lines+='<line class="kedge'+(got[b2.id]?" on":"")+'" data-a="'+a2.id+'" data-b="'+b2.id+'" x1="'+pa[0]+'" y1="'+pa[1]+'" x2="'+ex.toFixed(1)+'" y2="'+ey.toFixed(1)+'"/>';
    lines+='<polygon class="karr'+(got[b2.id]?" on":"")+'" data-a="'+a2.id+'" data-b="'+b2.id+'" points="'+pb[0]+','+pb[1]+' '+sx1+','+sy1+' '+sx2+','+sy2+'"/>';
   }else if(fb===fi){
    lines+='<line class="kedge kcross'+(got[b2.id]?" on":"")+'" data-a="'+a2.id+'" data-b="'+b2.id+'" x1="'+pa[0]+'" y1="'+pa[1]+'" x2="'+pb[0]+'" y2="'+pb[1]+'"/>';
    lines+='<circle class="kfoot'+(got[b2.id]?" on":"")+'" data-a="'+a2.id+'" data-b="'+b2.id+'" cx="'+pa[0]+'" cy="'+pa[1]+'" r="4.5"/>';
   }});
  f.ids.forEach(id=>{const n=N(id),p=P[id];
   nds+='<div class="kgN c'+n.c+(got[id]?" on":"")+'" data-id="'+id+'" style="left:'+p[0]+'px;top:'+p[1]+'px"><i>'+(got[id]?"✓":"")+'</i><b>'+n.t+'</b></div>';});
  fls+='<div class="kgFloor" style="transform:translateZ('+(fi*95)+'px)"><div class="kgPlate"><svg viewBox="0 0 640 240">'+lines+'</svg></div><div class="kgTag">'+f.t+'</div>'+nds+'</div>';
 });
 const CTL=document.getElementById("kgCtl");if(CTL)CTL.innerHTML='<span class="kchip kc0" data-c="0" onclick="kgToggleC(0)">基础</span><span class="kchip kc1" data-c="1" onclick="kgToggleC(1)">结构</span><span class="kchip kc2" data-c="2" onclick="kgToggleC(2)">任务</span><span class="kchip kc3" data-c="3" onclick="kgToggleC(3)">素养</span><button class="tbtn" onclick="kgZoom(1.25)">＋</button><button class="tbtn" onclick="kgZoom(.8)">－</button><button class="tbtn" onclick="kgReset()">⌂</button><span class="ghint2">立体知识大厦：底层是基础、顶层是素养，虚线跨层指向知识去向 · 拖拽旋转视角 · 滚轮缩放 · 双击复位 · 点胶囊收起一类</span>';
 box.innerHTML='<div class="kgstage kg3dStage"><div class="kg3d" id="kg3d">'+fls+'</div></div>';
 const stage=box.querySelector(".kg3dStage");let drag=null;
 stage.addEventListener("pointerdown",ev=>{if(ev.target.closest(".kgN"))return;drag={x:ev.clientX,y:ev.clientY,ox:kgV.x,oy:kgV.y};stage.setPointerCapture(ev.pointerId)});
 stage.addEventListener("pointermove",ev=>{if(!drag)return;kgV.x=Math.max(-70,Math.min(70,drag.ox+(ev.clientX-drag.x)*.35));kgV.y=Math.max(12,Math.min(82,drag.oy-(ev.clientY-drag.y)*.3));applyT()});
 stage.addEventListener("pointerup",()=>drag=null);
 stage.addEventListener("dblclick",()=>kgReset());
 box.querySelector(".kg3d").addEventListener("wheel",ev=>{ev.preventDefault();kgZoomAt(ev.deltaY<0?1.12:.89)},{passive:false});
 box.querySelectorAll(".kgN").forEach(el=>{
  el.addEventListener("mouseenter",()=>{const id=el.dataset.id;box.querySelectorAll(".kedge,.karr,.kfoot").forEach(p=>{if(p.dataset.a===id||p.dataset.b===id)p.classList.add("lit")});
   const nb=new Set([id]);GE.forEach(e=>{if(e[0]===id)nb.add(e[1]);if(e[1]===id)nb.add(e[0])});
   box.querySelectorAll(".kgN").forEach(x=>{if(nb.has(x.dataset.id))x.classList.add("lit")});});
  el.addEventListener("mouseleave",()=>{box.querySelectorAll(".lit").forEach(x=>x.classList.remove("lit"))});
  el.addEventListener("click",()=>{const n=N(el.dataset.id);
   const st=STOPS.find(q=>(n.id==="var"||n.id==="type")?q.id==="kai":q.id===(n.id==="cmd"?"kan":n.id==="flow"?"liu":n.id==="if"?"pan":n.id==="loop"?"xun":n.id==="tank"?"cun":n.id==="waimai"||n.id==="banfei"?"wai":n.id==="audit"?"shen":"shou"));
   if(st)stopGo(st);});});
 box.querySelectorAll(".kgN").forEach(x=>{const n=N(x.dataset.id);if(kgHide[n.c]){x.style.opacity=0;x.style.pointerEvents="none"}});
 box.querySelectorAll(".kedge,.karr,.kfoot").forEach(p=>{const a3=N(p.dataset.a||p.dataset.b),b3=N(p.dataset.b||p.dataset.a);if(kgHide[a3.c]||kgHide[b3.c])p.style.display="none";});
 applyT();}
'''
s = s[:a] + NEW + s[b + 1:]

# ═══ 2b 插入 applyT/mapGo/mapBackGo（在 kgZoomAt 前） ═══
i = s.find("function kgZoomAt")
assert i > 0
s = s[:i] + "function kgZoom(f){kgV.s=Math.min(2.2,Math.max(.55,kgV.s*f));applyT()}\nfunction applyT(){const el=document.getElementById(\"kg3d\");if(el)el.style.transform=\"rotateX(\"+kgV.y+\"deg) rotateZ(\"+kgV.x+\"deg) scale(\"+kgV.s+\")\"}\nfunction mapGo(t){showTab(t);const b=document.getElementById(\"mapBack\");if(b)b.classList.add(\"on\")}\nfunction mapBackGo(){showTab(\"home\");const b=document.getElementById(\"mapBack\");if(b)b.classList.remove(\"on\");const m=document.getElementById(\"lead1\");if(m)m.scrollIntoView({behavior:\"smooth\"})}\n" + s[i:]

# ═══ 2c stopGo 尾部挂返回地图浮标 ═══
rep(''' else if(st.tab==="gest")showTab("gest")}''',
    ''' else if(st.tab==="gest")showTab("gest");
 const mb=document.getElementById("mapBack");if(mb)mb.classList.add("on")}''')

# ═══ 3 首页动线重组 ═══
a2 = s.find('<div class="secLead" id="lead2">')
a3 = s.find('<div class="secLead" id="lead3"')
assert 0 < a2 < a3
seg = s[a2:a3]
r3a = seg.find('<div class="rule3">')
assert r3a > 0
rule3 = seg[r3a:].rstrip()
assert rule3.endswith("</div>")
s = s[:a2] + s[a3:]
a6 = s.find('<div class="secLead" id="lead6">')
aend = s.find("</section>", a6)
assert 0 < a6 < aend
seg6 = s[a6:aend].rstrip()
s = s[:a6] + s[aend:]
seg6 = seg6.replace('id="lead6"', 'id="lead2"')
seg6 = seg6.replace('加映 · 两大特色视图 —— 知识结构与虚拟展厅', '第二步 · 看特色 —— 两大镇店之宝：立体知识图谱 &amp; 虚拟展厅')
a3 = s.find('<div class="secLead" id="lead3"')
s = s[:a3] + seg6 + "\n  " + s[a3:]
re.sub(r"", "", "")
# tourBar 钮2 改 + 加映钮删
s = re.sub(r"<button onclick=\"document\.getElementById\('lead2'\)\.scrollIntoView\(\{behavior:'smooth'\}\)\"><i class=\"tico\">[^<]*</i><span><u>[^<]*</u>[^<]*</span></button>",
    "<button onclick=\"document.getElementById('lead2').scrollIntoView({behavior:'smooth'})\"><i class=\"tico\">✨</i><span><u>第二步 · 看特色</u>两大镇店之宝</span></button>", s, count=1)
s = re.sub(r"<button onclick=\"document\.getElementById\('lead6'\)\.scrollIntoView[^>]*><i class=\"tico\">[^<]*</i><span><u>[^<]*</u>[^<]*</span></button>", "", s, count=1)

# ═══ 4 规矩三栏搬机器人车间 ═══
ib = s.find('<section id="tab-bot">')
eoe = s.find("</div>", s.find('<div class="eyebrow">', ib)) + len("</div>")
s = s[:eoe] + '\n  <div class="card" style="margin:0 0 12px"><div class="eyebrow" style="margin-top:0">🛡 车间门口 · 这门课怎么管住 AI（三条规矩，翻牌实操见下）</div>' + rule3 + "</div>" + s[eoe:]

# ═══ 5 任务地图站 → mapGo + 返回浮标 ═══
a1 = s.find('id="lead1"')
a2 = s.find('id="lead2"')
assert 0 < a1 < a2
seg = s[a1:a2].replace("showTab(", "mapGo(")
s = s[:a1] + seg + s[a2:]
rep("</main>", '</main>\n<button id="mapBack" onclick="mapBackGo()">🗺 返回任务地图</button>')

# ═══ 6 名字消消乐 = B3XYL（自动进消名全屏 + h2 改） ═══
m = re.search(r'const B3B64="([^"]+)"', s)
b3 = base64.b64decode(m.group(1)).decode("utf-8")
assert b3.count("<h2>下课前\u3000检查册子</h2>") == 1
b3x = b3.replace("<h2>下课前\u3000检查册子</h2>", "<h2>完成任务后举手，老师消名字</h2>")
inject = '<script>try{var __ck=document.getElementById("checkout");if(__ck){__ck.classList.add("on");if(window.renderCheckout)renderCheckout();}}catch(e){}</scr' + "ipt>"
assert b3x.count("</body>") == 1
b3x = b3x.replace("</body>", inject + "</body>")
s = s[:m.end()] + '\nconst B3XYL="' + base64.b64encode(b3x.encode("utf-8")).decode() + '";' + s[m.end():]
rep('const xf=document.getElementById("xylFrame");if(xf)xf.srcdoc=decodeURIComponent(escape(atob(B3B64)));',
    'const xf=document.getElementById("xylFrame");if(xf)xf.srcdoc=decodeURIComponent(escape(atob(B3XYL)));')

# ═══ 7 版本 ═══
rep("v6.4 梳理版", "v6.5 立体版")

# ═══ 8 CSS ═══
NEWCSS = '''
.kg3dStage{aspect-ratio:auto;height:620px;perspective:1150px;overflow:hidden;position:relative;border-radius:14px;background:radial-gradient(ellipse at 50% 60%,#FDF6E8,#F0E2C8 68%,#E6D5B6)}
.kg3d{position:absolute;left:50%;top:53%;width:640px;height:240px;margin:-120px 0 0 -320px;transform-style:preserve-3d;transform:rotateX(50deg) rotateZ(0deg) scale(1)}
.kgFloor{position:absolute;inset:0;transform-style:preserve-3d}
.kgPlate{position:absolute;inset:0;background:rgba(255,252,244,.85);border:1.5px solid #E2D2B4;border-radius:18px;box-shadow:inset 0 0 0 4px rgba(255,255,255,.3),0 22px 44px rgba(120,90,40,.17)}
.kgPlate svg{width:100%;height:100%;display:block}
.kgTag{position:absolute;left:14px;bottom:-13px;background:#8C1F28;color:#FFE082;font-size:13px;font-weight:800;padding:4px 12px;border-radius:999px;letter-spacing:1px;box-shadow:0 4px 10px rgba(90,20,20,.25);white-space:nowrap}
.kgN{position:absolute;display:inline-flex;align-items:center;padding:5px 13px;border-radius:999px;background:linear-gradient(160deg,#5D1520,#8C1F28);color:#fff;font-size:13px;font-weight:800;letter-spacing:1px;transform:translateX(-50%);cursor:pointer;white-space:nowrap;border:2px solid rgba(255,255,255,.5);box-shadow:0 6px 14px rgba(90,20,20,.22);user-select:none}
.kgN i{position:absolute;right:-7px;top:-9px;width:19px;height:19px;background:#F59F23;color:#fff;border-radius:50%;font-style:normal;font-size:12px;display:none;align-items:center;justify-content:center;font-weight:900}
.kgN.on i{display:flex}
.kgN.on{border-color:#F59F23;box-shadow:0 0 0 3px rgba(245,159,35,.32),0 6px 16px rgba(245,159,35,.3)}
.kgN.c0{background:linear-gradient(160deg,#3D5FA8,#4A6FB5)}
.kgN.c1{background:linear-gradient(160deg,#2E7D32,#43A047)}
.kgN.c2{background:linear-gradient(160deg,#D9730D,#EF6C00)}
.kgN.c3{background:linear-gradient(160deg,#6C3BA8,#8E44AD)}
.kgN.lit{outline:2.5px solid #F59F23;outline-offset:2px}
.kedge{stroke:#C9B08A;stroke-width:2.4;fill:none}
.kedge.on{stroke:#F59F23;stroke-width:3}
.kedge.kcross{stroke-dasharray:7 5}
.kedge.lit{stroke:#E8590C}
.karr{fill:#C9B08A}.karr.on{fill:#F59F23}.karr.lit{fill:#E8590C}
.kfoot{fill:none;stroke:#C9B08A;stroke-width:2}.kfoot.on{stroke:#F59F23}.kfoot.lit{stroke:#E8590C}
#mapBack{position:fixed;right:18px;bottom:86px;z-index:57;display:none;background:#8C1F28;color:#fff;border:0;border-radius:999px;padding:9px 16px;font-weight:800;font-size:13.5px;box-shadow:0 6px 18px rgba(90,20,20,.35);cursor:pointer}
#mapBack.on{display:inline-flex;align-items:center;gap:6px}
.fcW{transition:transform .25s}
.fcW:hover{transform:translateY(-5px)}
.fcF{background:linear-gradient(165deg,#FFFDF7,#F6EBD6);border:2px solid #D8C39C;box-shadow:inset 0 0 0 4px #FFFDF7,inset 0 0 0 5.5px #CBB68C,0 6px 14px rgba(90,60,20,.14)}
.fcB{background:linear-gradient(45deg,#7A1B24,#5D1520,#7A1B24);border:2px solid #B3393F;box-shadow:inset 0 0 0 4px rgba(255,224,130,.12),inset 0 0 0 5.5px #D9A441}
.fcB b{font-size:2em;text-shadow:0 2px 8px rgba(0,0,0,.4)}
.fcF u{background:rgba(140,31,40,.07);border-radius:999px;padding:2px 10px}
.flipRow{background:radial-gradient(ellipse at center,#F1E6CF,#E2D2B2);padding:14px;border-radius:18px;border:1.5px solid #D8C39C}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v6.5 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
