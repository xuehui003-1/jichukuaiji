#!/usr/bin/env python3
"""v5.0 二轮审查补丁：手势换题+重设计；小邮气泡；揭晓层可见提示；6门→6份；生活记账挂基础会计来历"""
import sys
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old)
    assert c==1,("count=%d !=1: %s"%(c,old[:60]))
    s=s.replace(old,new)

# ── 1 手势页：删关系链卡，换 hero ──
rep('''  <div class="card"><h3>🔗 先看懂一笔花呗购物的关系链（下面五题的底座）</h3>
    <div class="chain" id="chainBox"></div>
    <div class="note">钱、货、权利、义务在四方之间流动——认清「谁欠谁、谁拥有什么」，再用四种手势回答五道认知题。</div>
  </div>
  <div class="say">🙌 四种手势答下面的五关：左边 <b>☝</b>｜右边 <b>✌</b>｜是 <b>👍</b>｜否 <b>✊</b>。手势保持约半秒提交；答对换题前请把手放下。<b>没有摄像头？下面的按钮完成一模一样的任务。</b></div>''',
'''  <div class="gestHero"><div class="gl"><b>🙌 用手答题</b><span>五道判断 · 全部出自课件 · 答错可回原页重学 · 摄像头视频只在本机处理，不上传不保存</span></div>
    <div class="gr"><i>☝<em>左</em></i><i>✌<em>右</em></i><i>👍<em>是</em></i><i>✊<em>否</em></i></div></div>
  <div class="say">手势保持约半秒提交；答对换题前请把手放下。<b>没有摄像头？用下面的按钮完成一模一样的任务。</b></div>''')
rep('<span class="tag">会计认知关联 · 闯关 <span id="gIdx">1</span>/5</span>','<span class="tag">课件判断 · 闯关 <span id="gIdx">1</span>/5</span>')

# ── 2 新题库（全部出自课件 · 是/否 · 带回跳页码） ──
a=s.find("const GQ=[");b=s.find("];",a)
GQ='''const GQ=[
 {t:"学号 25010101 存成数值——对吗？",q:"花名册上的学号只是一串编号，不参与算术。把它存成数值类型，对吗？",opts:["是","否"],exp:"Closed_Fist",know:"学号是编号不是数量",ans:"不对——学号要存字符；存成数值会弄丢前导零，还能被人拿去加减",back:["08",26]},
 {t:"「打印」执行后，变量里存的值会变吗？",q:"打印命令只是把变量的值显示到屏幕上。打印之后，变量里存的值会变吗？",opts:["会","不会"],exp:"Closed_Fist",know:"打印只显示、不改动",ans:"不会——打印只是把值抄到屏幕；想让值变，要用赋值或累加",back:["08",31]},
 {t:"500 起步、每次存 100、凑到 1000——要存 5 次？",q:"存钱罐里有 500，每次存入 100，想凑到 1000。机器人要执行存入动作 5 次，对吗？",opts:["对","不对"],exp:"Thumb_Up",know:"循环次数＝（目标−起始）÷每次",ans:"对——(1000−500)÷100＝5 次，第 5 次存完正好 1000",back:["17",8]},
 {t:"if 条件不满足，大括号里的命令也会执行一次？",q:"判断结构里，if 的条件不满足时，大括号里的命令也会执行一次，对吗？",opts:["对","不对"],exp:"Closed_Fist",know:"条件不满足就走「否则」分支",ans:"不对——条件不满足就跳过大括号；写了「否则」就走「否则」",back:["17",6]},
 {t:"AI 一键改完 67 份作业，老师就不用检查了？",q:"「AI 一键把 67 份作业全改对，老师就不用检查了」——这句话对吗？",opts:["对","不对"],exp:"Closed_Fist",know:"学生先判断 · AI 只辅助 · 教师做终审",ans:"不对——AI 会「一声不吭替你做主」；它的每个决定都要摆上台面，裁定权永远在老师",back:["08",26]}];'''
s=s[:a]+GQ+s[b+2:]

# ── 3 renderGest：选项提示改是/否；完成态文案换 ──
rep("""<div><b>${o}</b><em>${i===0?"☝ 左边":"✌ 右边"}</em></div>""",
    """<div><b>${o}</b><em>${i===0?"👍 是 · 举大拇指":"✊ 否 · 握拳头"}</em></div>""")
rep("""    document.getElementById("gFeedback").innerHTML=`<div class="basis"><b>主体决定会计结果</b><ul><li>你已经完成主体、债权、义务和收入边界五关</li><li>手势只是提交答案，核心仍是会计分析</li></ul></div>`;""",
"""    const bk=(Object.keys(g.errors).length)?`<li>答错的题：点「📖 回课件重学」看原页，再把「为什么」讲给同桌听——讲明白才算真会（费曼）</li>`:`<li>全对！挑一题把「为什么」讲给同桌听——讲明白才算真会（费曼）</li>`;
    document.getElementById("gFeedback").innerHTML=`<div class="basis"><b>这五题全部出自你的课件</b><ul><li>学号类型 → 打印命令 → 循环次数 → 判断结构 → AI 纪律，正是这门课的主线</li>${bk}</ul></div>`;""")

# ── 4 gSubmit 答错：回课件重学按钮＋气泡 ──
rep("""    fb.innerHTML=`<div class="verd no">✗ 这是${GLBL[name]}；本题需要「${GLBL[q.exp]}」。看懂知识含义再试——卡住了就问右下角 🤖 小邮。</div>`;return}""",
"""    fb.innerHTML=`<div class="verd no">✗ 这是${GLBL[name]}；本题需要「${GLBL[q.exp]}」。<button class="btn o gback" onclick="gBack('${q.back[0]}',${q.back[1]})">📖 回课件 p${q.back[1]} 重学</button></div>`;fabNudge("这道题卡住了？问我「为什么」——我只提示，不替你答");return}""")

# ── 5 gBack + fabNudge 组件（插在 function gSubmit 前） ──
rep("function gSubmit(name){",
"""function gBack(d,n){showTab("lib");libDeck(d);dkState.lib.cur=n-1;libShow();document.getElementById("libStage").scrollIntoView({behavior:"smooth",block:"start"});}
/* 小邮气泡：看到气泡→点右下角小邮；90 秒冷却，once 的本机只弹一次 */
let fabNudgeTimer=null,fabCool=0;
function fabNudge(txt,once){
  if(once){const k="nudge_"+once;try{if(localStorage.getItem(k))return;localStorage.setItem(k,"1")}catch(e){}}
  const now=Date.now();if(now<fabCool)return;fabCool=now+90000;
  let b=document.getElementById("fabNudge");
  if(!b){b=document.createElement("div");b.id="fabNudge";b.onclick=()=>{fabHide();toggleAip()};document.body.appendChild(b);}
  b.innerHTML='<button class="nx" onclick="event.stopPropagation();fabHide()">×</button>'+txt+'<div class="ngo">点这里找小邮 →</div>';
  b.classList.add("on");clearTimeout(fabNudgeTimer);fabNudgeTimer=setTimeout(fabHide,9000);}
function fabHide(){const b=document.getElementById("fabNudge");if(b)b.classList.remove("on");}
function gSubmit(name){""")

# ── 6 检查器答错→气泡 ──
rep("""+(ok?"":'<div class="note" style="margin-top:6px">卡住了？问右下角 🤖 小邮——比如「为什么学号不是数值」，它只提示，不替你答。</div>');""",
"""+(ok?"":'<div class="note" style="margin-top:6px">卡住了？问右下角 🤖 小邮——比如「为什么学号不是数值」，它只提示，不替你答。</div>');if(!ok)fabNudge("检查器里有不对的地方——问我「为什么错」？我只提示，不替你答");""")

# ── 7 教师台首次进入→气泡 ──
rep("""<button id="tb-teach" onclick="showTab('teach')">📋 教师台</button>""",
"""<button id="tb-teach" onclick="showTab('teach');fabNudge('老师的「下节课建议」就在这页——要我帮你预演一次 AI 备课也行','teach')">📋 教师台</button>""")

# ── 8 进站 12 秒欢迎气泡（挂在 libJumpGo 定义之后） ──
rep("""function libJumpGo(){const n=parseInt(document.getElementById("libJump").value,10);
  const rail=dkState.lib.rail;if(!n||n<1||n>rail.length)return;
  dkState.lib.cur=n-1;libShow();document.getElementById("libStage").scrollIntoView({behavior:"smooth",block:"start"});}""",
"""function libJumpGo(){const n=parseInt(document.getElementById("libJump").value,10);
  const rail=dkState.lib.rail;if(!n||n<1||n>rail.length)return;
  dkState.lib.cur=n-1;libShow();document.getElementById("libStage").scrollIntoView({behavior:"smooth",block:"start"});}
setTimeout(()=>fabNudge("我是右下角的小邮 🤖 任务卡住、答错想问为什么、想让我帮你查——随时点我","hi"),12000);""")

# ── 9 揭晓层可见提示（dkShow 注入占位提示＋点击揭晓） ──
rep("""  stage.querySelectorAll(".pic").forEach(im=>{""",
"""  stage.querySelectorAll(".rv:not(.rvshow)").forEach(el=>{const h=document.createElement("div");h.className="rvHint";h.innerHTML="👆 这页藏着一层答案——点这里揭晓";el.parentNode.insertBefore(h,el);el.__hint=h;
    h.onclick=ev=>{ev.stopPropagation();el.classList.add("rvshow");if(h.parentNode)h.remove();if(dkState[zone]&&dkState[zone].spot)dkSpotTo(zone,el);};});
  stage.querySelectorAll(".pic").forEach(im=>{""")
rep("""  if(h.length){h[0].classList.add("rvshow");""",
"""  if(h.length){h[0].classList.add("rvshow");if(h[0].__hint&&h[0].__hint.parentNode)h[0].__hint.remove();""")

# ── 10 CSS（hero/提示条/气泡/回学钮） ──
rep(""".lib04 img,.lib10 img,.lib14 img,.lib16 img{border-radius:12px;max-width:100%}
</style>""",
""".lib04 img,.lib10 img,.lib14 img,.lib16 img{border-radius:12px;max-width:100%}
.gestHero{display:flex;justify-content:space-between;align-items:center;gap:14px;background:linear-gradient(135deg,#8C1F28,#B5433A);border-radius:16px;padding:16px 22px;color:#fff;margin:0 0 12px;flex-wrap:wrap}
.gestHero .gl b{font-size:23px;display:block;letter-spacing:1px}
.gestHero .gl span{opacity:.92;font-size:14px}
.gestHero .gr{display:flex;gap:10px}
.gestHero .gr i{display:flex;flex-direction:column;align-items:center;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);border-radius:12px;padding:6px 12px;font-style:normal;font-size:26px;line-height:1.2}
.gestHero .gr em{font-style:normal;font-size:12px;margin-top:2px;opacity:.95}
.rvHint{margin:10px 0;padding:10px 14px;border:1.6px dashed #C8871E;background:#FFF7E6;border-radius:12px;color:#7A5200;font-size:15px;cursor:pointer;user-select:none}
.rvHint:hover{background:#FFEFC9}
#fabNudge{position:fixed;right:88px;bottom:104px;max-width:280px;background:#fff;border:1.5px solid #8C1F28;border-radius:14px;box-shadow:0 8px 28px rgba(80,20,20,.28);padding:12px 26px 10px 14px;font-size:14px;line-height:1.55;color:#4a1418;opacity:0;transform:translateY(12px);pointer-events:none;transition:.25s;z-index:999}
#fabNudge.on{opacity:1;transform:none;pointer-events:auto}
#fabNudge .ngo{margin-top:6px;font-size:12.5px;color:#B5433A;font-weight:700}
#fabNudge .nx{position:absolute;top:2px;right:7px;border:0;background:none;font-size:17px;color:#999;cursor:pointer;padding:2px}
#fabNudge:after{content:"";position:absolute;right:-9px;bottom:20px;border:8px solid transparent;border-left-color:#8C1F28}
.gback{margin-top:6px}
</style>""")

# ── 11 「6 门」→「6 份课件」 ──
rep('<div class="d">全部 6 门课件 154 页整馆入住：想翻哪页翻哪页</div>','<div class="d">全部 6 份课件 154 页整馆入住：想翻哪页翻哪页</div>')
rep("全部 6 门 154 页去「课件馆」","全部 6 份课件 154 页去「课件馆」")
rep("本节课 19 页精编轨＋全部 6 门课件 154 页任翻（课件馆）","本节课 19 页精编轨＋全部 6 份课件 154 页任翻（课件馆）")

# ── 12 生活记账挂《基础会计》来历 ──
rep("题目出自本班 <b>67 份生活记账作业</b>——「父母转的生活费能不能直接记收入」是 AI 复核拿不准的真实高频场景：你先判断，AI 只做规则复核给置信度，拿不准的自动等老师终审。",
    "题目出自同学们在先修课《基础会计》记过的 <b>67 份生活账</b>——旧账新用，正是这门课让 AI 复核的真实业务：你先判断，AI 只做规则复核给置信度，拿不准的自动等老师终审。")
rep("67 份生活记账作业是本课「让机器人干会计的活」的真实业务素材",
    "67 份生活记账作业来自先修课《基础会计》——旧账新用：它们是本课「让机器人干会计的活」的真实业务素材")
rep("此处为 67 份生活记账作业 + 课堂记分的演示基线。","此处为 67 份生活记账作业（源自先修课《基础会计》）＋课堂记分的演示基线。")
rep("围绕「生活记账」真实作业运转","围绕《基础会计》生活记账作业（旧账新用）运转")
rep("<b>${s.homework}</b><span>生活记账作业（份）</span>","<b>${s.homework}</b><span>生活记账作业（份·源自基础会计）</span>")

open(P,"w",encoding="utf-8").write(s)
print("v5b 补丁 12 组全部 OK")
