#!/usr/bin/env python3
"""v5k：页脚版本标记v5.2；图谱分类图例(点击收缩/展开整类节点+边)；鼠标视差3D倾斜(拖拽自动回正)"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)

# 1 版本标记（肉眼可辨新旧文件）
rep("（公开页数据已匿名）`;","（公开页数据已匿名） ｜ v5.2 任务地图版`;")

# 2 收缩状态 + 图例 chips
rep('let kgView="map",kgV={x:0,y:0,s:1};',
    'let kgView="map",kgV={x:0,y:0,s:1};let kgHide={0:false,1:false,2:false,3:false};')
rep('''<button class="tbtn" onclick="kgReset()">重置</button><span class="gnote">''',
    '''<button class="tbtn" onclick="kgReset()">重置</button>
<span class="kchip kc0" data-c="0" onclick="kgToggleC(0)">基础</span><span class="kchip kc1" data-c="1" onclick="kgToggleC(1)">结构</span><span class="kchip kc2" data-c="2" onclick="kgToggleC(2)">任务</span><span class="kchip kc3" data-c="3" onclick="kgToggleC(3)">素养</span><span class="gnote">''')
rep('''function kgReset(){kgV={x:0,y:0,s:1};applyT()}''',
'''function kgReset(){kgV={x:0,y:0,s:1};applyT()}
function kgToggleC(c){kgHide[c]=!kgHide[c];document.querySelectorAll(".kchip").forEach(ch=>ch.classList.toggle("off",kgHide[+ch.dataset.c]));renderGraph()}''')

# 3 收缩应用 + 3D 倾斜（挂进 renderGraph 尾部）
rep('''   if(st)stopGo(st);});});
 applyT();}''',
'''   if(st)stopGo(st);});});
 svg.querySelectorAll(".gn").forEach(x=>{const n=N(x.dataset.id);if(kgHide[n.c]){x.style.opacity=.14;const c=x.querySelector(".gnc");if(c)c.style.transform="scale(.55)"}});
 svg.querySelectorAll(".ge").forEach(p=>{const a=N(p.dataset.a),b=N(p.dataset.b);if(kgHide[a.c]||kgHide[b.c])p.style.opacity=.05;});
 svg.addEventListener("mousemove",ev=>{if(drag)return;const r=svg.getBoundingClientRect();
   const px=(ev.clientX-r.left)/r.width-.5,py=(ev.clientY-r.top)/r.height-.5;
   svg.style.transform="perspective(950px) rotateX("+(-py*9).toFixed(1)+"deg) rotateY("+(px*11).toFixed(1)+"deg)";});
 svg.addEventListener("mouseleave",()=>svg.style.transform="");
 applyT();}''')
rep('svg.addEventListener("pointerdown",ev=>{drag={',
    'svg.addEventListener("pointerdown",ev=>{svg.style.transform="";drag={')

# 4 CSS
rep('.gnote{font-size:12.5px;color:rgba(255,255,255,.55);margin-left:auto}',
'''.gnote{font-size:12.5px;color:rgba(255,255,255,.55);margin-left:auto}
.kchip{cursor:pointer;font-size:12.5px;font-weight:800;border-radius:999px;padding:3px 11px;color:#102040;border:1px solid rgba(255,255,255,.3);transition:.15s}
.kchip.kc0{background:#FFB74D}.kchip.kc1{background:#4FC3F7}.kchip.kc2{background:#81C784}.kchip.kc3{background:#FFD54F}
.kchip.off{opacity:.32;text-decoration:line-through}
.gwrap svg{transition:transform .18s ease}''')

open(P,"w",encoding="utf-8").write(s)
import os
print("v5k OK; %.2f MB"%(os.path.getsize(P)/1048576))
