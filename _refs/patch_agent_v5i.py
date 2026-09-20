#!/usr/bin/env python3
"""v5i：fab恢复圆形+聪明脸SVG(高光大眼/歪头浮动/hover兴奋)；面板300x640；关于页AI知识库+智慧课程对照；新增知识图谱标签(12节点/点击直达/掌握着色)；面板说话头像"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)

# ── 1 fab：圆形 64px ──
rep('.fab{position:fixed;right:20px;bottom:20px;z-index:60;width:48px;height:104px;border-radius:26px;',
    '.fab{position:fixed;right:20px;bottom:20px;z-index:60;width:64px;height:64px;border-radius:50%;')

# ── 2 新 SVG：聪明脸（渐变机身/大眼高光/微笑/侧耳） ──
import re
i=s.find('<svg class="xybot"');j=s.find('</svg>',i)+6
OLDSVG=s[i:j]
NEWSVG='''<svg class="xybot" viewBox="0 0 64 64" aria-hidden="true">
  <defs><linearGradient id="xgrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F59F23"/><stop offset="1" stop-color="#E8532F"/></linearGradient></defs>
  <line x1="32" y1="8" x2="32" y2="14" stroke="#FFE082" stroke-width="2.6"/>
  <circle class="xantb" cx="32" cy="6.5" r="3.6" fill="#FFE082"/>
  <rect x="4.5" y="25" width="5" height="11" rx="2.5" fill="#F59F23"/>
  <rect x="54.5" y="25" width="5" height="11" rx="2.5" fill="#F59F23"/>
  <rect x="10" y="14" width="44" height="31" rx="12" fill="url(#xgrad)"/>
  <rect x="15" y="19.5" width="34" height="20" rx="9" fill="#2A1D16"/>
  <g class="xeyes">
    <circle cx="26" cy="29" r="4.6" fill="#81D4FA"/><circle cx="38" cy="29" r="4.6" fill="#81D4FA"/>
    <circle cx="27.6" cy="27.3" r="1.5" fill="#fff"/><circle cx="39.6" cy="27.3" r="1.5" fill="#fff"/>
  </g>
  <path d="M27.5 34.5 q4.5 3.8 9 0" stroke="#FFE082" stroke-width="1.8" fill="none" stroke-linecap="round"/>
  <rect x="17" y="47" width="30" height="6.5" rx="3.2" fill="#FFE082"/>
  <circle cx="32" cy="57" r="5" fill="#BF360C"/>
</svg>'''
s=s[:i]+NEWSVG+s[j:]

# ── 3 动画升级（歪头浮动/hover兴奋/眼睛组眨+瞟） ──
rep('''.fab svg.xybot{width:100%;height:100%;display:block;animation:xbob 3.4s ease-in-out infinite}
.xantb{animation:xping 2.2s ease-in-out infinite;transform-origin:center}
.xeyeL,.xeyeR{animation:xblink 4.4s infinite;transform-origin:center;transform-box:fill-box}
.fab.nudge svg.xybot{animation:xjump .8s ease}
@keyframes xbob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
@keyframes xblink{0%,91%,100%{transform:scaleY(1)}94%{transform:scaleY(.12)}97%{transform:scaleY(1)}}
@keyframes xping{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes xjump{0%{transform:translateY(0)}30%{transform:translateY(-12px)}60%{transform:translateY(0)}78%{transform:translateY(-5px)}100%{transform:translateY(0)}}''',
'''.fab svg.xybot{width:100%;height:100%;display:block;animation:xbob 3.2s ease-in-out infinite}
.fab:hover svg.xybot{animation:xtickle .55s ease-in-out infinite}
.xantb{animation:xping 2s ease-in-out infinite}
.xeyes{animation:xblink 4.6s infinite, xglance 7s ease-in-out infinite;transform-origin:center;transform-box:fill-box}
.fab.nudge svg.xybot{animation:xjump .8s ease}
@keyframes xbob{0%,100%{transform:translateY(0) rotate(0deg)}30%{transform:translateY(-3px) rotate(-2.4deg)}65%{transform:translateY(-1px) rotate(2.4deg)}}
@keyframes xtickle{0%,100%{transform:rotate(0)}25%{transform:rotate(-7deg) translateY(-3px)}75%{transform:rotate(7deg) translateY(-3px)}}
@keyframes xblink{0%,91%,100%{transform:scaleY(1)}94%{transform:scaleY(.14)}97%{transform:scaleY(1)}}
@keyframes xglance{0%,72%,100%{transform:translateX(0)}78%,88%{transform:translateX(2.4px)}}
@keyframes xping{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes xjump{0%{transform:translateY(0)}30%{transform:translateY(-12px)}60%{transform:translateY(0)}78%{transform:translateY(-5px)}100%{transform:translateY(0)}}''')

# ── 4 面板更瘦长 ──
rep('width:min(320px,calc(100vw - 32px));height:min(600px,78vh);','width:min(300px,calc(100vw - 32px));height:min(640px,80vh);')

# ── 5 面板说话头像 ──
rep('<header2><b>🤖 小邮伴学 · 有问题问我</b>',
'''<header2><svg id="xyFace" viewBox="0 0 64 44" style="width:34px;vertical-align:middle" aria-hidden="true">
  <rect x="8" y="2" width="48" height="34" rx="12" fill="url(#xgrad)"/>
  <rect x="13" y="7" width="38" height="22" rx="8" fill="#2A1D16"/>
  <circle cx="25" cy="18" r="4.2" fill="#81D4FA"/><circle cx="39" cy="18" r="4.2" fill="#81D4FA"/>
  <circle cx="26.4" cy="16.6" r="1.3" fill="#fff"/><circle cx="40.4" cy="16.6" r="1.3" fill="#fff"/>
  <rect class="xm" x="28" y="23.5" width="8" height="3.4" rx="1.7" fill="#FFE082"/>
</svg> <b>小邮伴学 · 有问题问我</b>''')
rep('.gv figcaption{text-align:center;font-size:12.5px;margin-top:3px;color:#6b5d52;font-weight:700}',
'''.gv figcaption{text-align:center;font-size:12.5px;margin-top:3px;color:#6b5d52;font-weight:700}
#xyFace .xm{transform-origin:center;transform-box:fill-box}
#xyFace.talking .xm{animation:xmouth .32s ease-in-out infinite alternate}
@keyframes xmouth{from{transform:scaleY(.4)}to{transform:scaleY(1.5)}}''')
rep('function sayVoice(k){try{new Audio(VOICE[k]).play()}catch(e){}}',
'''function sayVoice(k){try{new Audio(VOICE[k]).play()}catch(e){}\n  const f=document.getElementById("xyFace");if(f){f.classList.add("talking");setTimeout(()=>f.classList.remove("talking"),2300)}}''')

# ── 6 知识图谱标签 ──
rep('<button id="tb-lib" onclick="showTab(\'lib\')">📚 课件馆</button>',
    '''<button id="tb-lib" onclick="showTab('lib')">📚 课件馆</button>
  <button id="tb-graph" onclick="showTab('graph')">🗺 图谱</button>''')
i=s.find('<section id="tab-bot">')
GRAPH='''<section id="tab-graph">
  <div class="eyebrow">🗺 课程知识图谱 · 这门课的骨架</div>
  <div class="note" style="margin:6px 0 10px">点任何节点直达课件原页或对应模块；<b style="color:#2E6B2E">亮绿</b>＝你已在智能体里练过、掌握了的知识点（着色随练习实时更新）。</div>
  <div class="card"><div id="kgBox"></div>
    <div class="note">图例：开场任务(变量/类型)→命令→流程图→判断/循环→三大任务(存钱罐/外卖/班费)→审账复核与铁律——和课件、课堂、上机完全同一条线。</div>
  </div>
</section>
'''
s=s[:i]+GRAPH+s[i:]
rep(''' bot:"跟着「第①②③步」走：选任务 → 改一个值 → 先猜再跑。每个变量旁边都写着它是什么",''',
''' bot:"跟着「第①②③步」走：选任务 → 改一个值 → 先猜再跑。每个变量旁边都写着它是什么",
 graph:"这张图就是这门课的骨架——点任何节点直达课件原页；你练过的地方会亮绿",''')
rep('if(t==="gest")sayVoiceOnce("gintro","vg");if(t==="teach")sayVoiceOnce("tintro","vt");',
    'if(t==="graph")renderKG();if(t==="gest")sayVoiceOnce("gintro","vg");if(t==="teach")sayVoiceOnce("tintro","vt");')
rep('function clsAsk(){',
'''const KG={nodes:[
 {id:"var",t:"变量",d:"贴标签的储物格",page:["08",26],x:32,y:11},
 {id:"type",t:"类型",d:"字符 / 数值",page:["08",26],x:12,y:28},
 {id:"cmd",t:"命令",d:"输入·打印·赋值",page:["08",32],x:52,y:28},
 {id:"flow",t:"流程图",d:"把步骤画出来",page:["17",7],x:32,y:45},
 {id:"if",t:"判断",d:"条件的岔路口",page:["17",6],x:13,y:63},
 {id:"loop",t:"循环",d:"重复交给机器人",page:["17",8],x:51,y:63},
 {id:"tank",t:"存钱罐",d:"判断＋循环",page:["17",8],x:32,y:80},
 {id:"waimai",t:"外卖满减",d:"顺序＋判断",page:["08",49],x:10,y:80},
 {id:"banfei",t:"班费记账",d:"顺序结构",page:["08",50],x:54,y:80},
 {id:"audit",t:"审账复核",d:"AI 复核·教师拍板",tab:"home",x:18,y:95},
 {id:"rule",t:"铁律",d:"先判断·只辅助·终审",tab:"gest",x:46,y:95}],
 edges:[["var","type"],["var","cmd"],["type","flow"],["cmd","flow"],["flow","if"],["flow","loop"],["if","tank"],["loop","tank"],["if","waimai"],["flow","banfei"],["tank","audit"],["tank","rule"],["waimai","audit"],["banfei","rule"]]};
function kgGot(n){
 if(n.tab==="gest")return g.score>=100;
 if(n.tab==="home")return state.class.shf.done;
 if(n.id==="var"||n.id==="type")return state.class.pv.done;
 if(typeof bot!=="undefined"&&bot.last&&bot.proj===n.id)return true;
 return false}
function kgClick(id){const n=KG.nodes.find(x=>x.id===id);
 if(n.page){showTab("lib");libDeck(n.page[0]);dkState.lib.cur=n.page[1]-1;libShow();document.getElementById("libStage").scrollIntoView({behavior:"smooth",block:"start"})}
 else showTab(n.tab)}
function renderKG(){const box=document.getElementById("kgBox");if(!box)return;
 let svg='<svg viewBox="0 0 64 103" style="width:100%;display:block">';
 KG.edges.forEach(e=>{const a=KG.nodes.find(n=>n.id===e[0]),b=KG.nodes.find(n=>n.id===e[1]);
  svg+='<line x1="'+a.x+'" y1="'+(a.y+5.2)+'" x2="'+b.x+'" y2="'+(b.y-5.2)+'" class="kge"/>'});
 KG.nodes.forEach(n=>{const got=kgGot(n);
  svg+='<g class="kg'+(got?" got":"")+'" onclick="kgClick(\\''+n.id+'\\')"><title>'+n.t+'：'+n.d+'（点'+(n.page?"开课件 p"+n.page[1]:"去 "+(n.tab==="home"?"首页体验":"手势闯关"))+'）</title><rect x="'+(n.x-12)+'" y="'+(n.y-5)+'" width="24" height="10.4" rx="5.2"/><text x="'+n.x+'" y="'+(n.y-0.4)+'">'+n.t+'</text><text class="kd" x="'+n.x+'" y="'+(n.y+3.4)+'">'+n.d+'</text></g>'});
 box.innerHTML=svg+'</svg>';}
function clsAsk(){''')
# KG CSS
rep('#xyFace .xm{transform-origin:center;transform-box:fill-box}',
'''#kgBox .kge{stroke:#D8C6AE;stroke-width:.7}
#kgBox .kg rect{fill:#fff;stroke:#C9AE8C;stroke-width:.55;cursor:pointer;transition:.15s}
#kgBox .kg:hover rect{stroke:#8C1F28;stroke-width:.9}
#kgBox .kg text{font-size:4.1px;font-weight:800;fill:#4a2c1e;text-anchor:middle}
#kgBox .kg text.kd{font-size:2.7px;font-weight:400;fill:#8a7a6a}
#kgBox .kg.got rect{fill:#E9F2E9;stroke:#2E6B2E}
#kgBox .kg.got text{fill:#2E6B2E}
#xyFace .xm{transform-origin:center;transform-box:fill-box}''')

# ── 7 关于页：AI 知识库亮牌＋智慧课程对照 ──
rep('<li><b>大模型可选接入</b>：OpenAI 兼容接口（DeepSeek、豆包等）；提示词约束「不替学生作答，只做结构化与启发式追问」；失败自动回退演示模式</li>',
'''<li><b>AI 知识库（本地优先）</b>：内置课程知识条目与高频问题库，关键词＋上下文追问即问即答，配合语音讲解；再经 OpenAI 兼容接口（DeepSeek、豆包等）可选接入大模型，升级为生成式问答——提示词约束「不替学生作答，只做结构化与启发式追问」，断网可用、数据不出浏览器</li>''')
rep('''  <div class="card"><h3>落地与声明</h3>''',
'''  <div class="card"><h3>🧭 与智慧课程建设的关系</h3>
    <table><tr><th>智慧课程要素</th><th>本作品的落地</th></tr>
    <tr><td>AI 助学智能体</td><td>小邮伴学：启发式问答＋语音讲解＋手势交互</td></tr>
    <tr><td>AI 知识库</td><td>本地课程知识库（即问即答），可选接入大模型升级生成式</td></tr>
    <tr><td>数字人讲解</td><td>动态形象＋语音合成的小邮（单文件轻量版，离线可跑）</td></tr>
    <tr><td>知识 / 问题 / 技能图谱</td><td>「🗺 图谱」页：点节点直达课件页，掌握度实时着色</td></tr>
    <tr><td>课程统计</td><td>教师台学情地图＋课堂快照（匿名聚合）</td></tr></table>
    <div class="note" style="margin-top:6px">本作品就是智慧课程建设的智能体底座：单文件即可独立开课使用，也可整体接入学校智慧课程平台。</div>
  </div>
  <div class="card"><h3>落地与声明</h3>''')

open(P,"w",encoding="utf-8").write(s)
import os
print("v5i OK; %.2f MB"%(os.path.getsize(P)/1048576))
