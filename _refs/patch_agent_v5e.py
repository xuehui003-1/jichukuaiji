#!/usr/bin/env python3
"""v5e：气泡去冷却；灯箱全img；评环换审账题；手势五题覆盖四手势+去剧透；车间runOut重做+实时图纸+命名说明+互动指引；地图条视觉重做；课堂同步问小邮按钮"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)

# ── 1 气泡：删 15s 冷却（once 去重已防轰炸；显示中触发→直接换内容重置计时） ──
rep("let fabNudgeTimer=null,fabCool=0;const fabOnce=new Set();","let fabNudgeTimer=null;const fabOnce=new Set();")
rep("  const now=Date.now();if(now<fabCool)return;fabCool=now+15000;\n","")

# ── 2 灯箱：所有 img 可点放大（17 课页图无 .pic 类） ──
rep('stage.querySelectorAll(".pic").forEach(im=>{im.style.cursor="zoom-in";im.title="点击放大，再点关闭";',
    'stage.querySelectorAll("img").forEach(im=>{im.style.cursor="zoom-in";im.title="点击放大，再点关闭";')

# ── 3 评环：换成本课日常「审一条机器人记的账」 ──
i=s.find("const SHF={");j=s.find("};",i)+2
SHF='''const SHF={q:"检查一条机器人记的账：小王把「买早饭 6 元」和「坐公交 2 元」记成了一条——「早上出行共花 8 元」。这样记账对吗？",
 opts:["对，记了就行","不对，一件事记一条","说不准"],right:1,
 basis:["一件事记一条：早饭是「吃」、公交是「行」，混成一条，钱花在哪就看不清了","混账会让机器人复核卡住：AI 分不清哪笔该归哪类——这就是要治的「多事并记」","正确姿势：分成两条——「早餐 6 元」「公交 2 元」，月末每类花多少一目了然"],
 conf:0.58,low:true,ask:"追问：早饭和公交都是花钱，为什么必须分开记？用你自己的话说说。"};'''
s=s[:i]+SHF+s[j:]
rep('<div class="card"><h3>🙋 30 秒体验这个智能体的核心规矩<span class="pb">全站都围着它转</span></h3>',
    '<div class="card"><h3>🙋 30 秒体验：你判断，AI 复核，老师拍板<span class="pb">全站核心机制</span></h3>')
rep('<div class="note">爸妈转来的生活费，能直接记成收入吗？——这题出自你们在《基础会计》记过的生活账。规矩只有一条：<b>你先判断，AI 只给复核参考，最后由老师拍板。</b></div>',
    '<div class="note">这是这门课每天在发生的事：学生的账，机器人按规则复核一遍——但 AI 只给参考，<b>判断权在你，裁定权在老师</b>。用下面这道题亲手走一遍：</div>')

# ── 4 手势五题：覆盖四手势、题干说人话 ──
a=s.find("const GQ=[");b=s.find("];",a)
GQ='''const GQ=[
 {t:"学号要存进变量",q:"花名册上的学号 25010101，存的时候选「数值」类型——对吗？",opts:["对","不对"],exp:"Closed_Fist",know:"学号是编号不是数量",ans:"不对——学号要存「字符」：它不用来算术，存成数值还会弄丢前导零",back:["08",26]},
 {t:"给变量起名",q:"要建一个变量存「每次存 100」。哪个变量名符合课堂「见名知义」的规矩？",opts:["meiCi","abc123"],exp:"Pointing_Up",know:"变量名＝拼音、看名知义",ans:"meiCi——「每次」的拼音，一眼看懂；abc123 过一周连自己都忘了存了啥",back:["08",26]},
 {t:"「打印」会改值吗",q:"「打印」只是把变量的值显示到屏幕上。打印之后，变量里存的值会变吗？",opts:["会变","不会变"],exp:"Thumb_Up",know:"打印只显示、不改动",ans:"不会变——想让值变，要用赋值或累加",back:["08",31]},
 {t:"循环跑几次",q:"存钱罐里有 500，每次存 100，攒到 1000 就停。机器人要跑几次？",opts:["4 次","5 次"],exp:"Victory",know:"循环次数＝（目标−起点）÷ 每次",ans:"5 次——(1000−500)÷100＝5，第 5 次存完正好 1000",back:["17",8]},
 {t:"AI 的规矩",q:"「AI 一键把 67 份作业全改对，老师就不用检查了」——这句话对吗？",opts:["对","不对"],exp:"Closed_Fist",know:"学生先判断 · AI 只辅助 · 教师做终审",ans:"不对——AI 会「一声不吭替你做主」，它的每个决定都要摆上台面，拍板的永远是老师",back:["08",26]}];'''
s=s[:a]+GQ+s[b+2:]
rep("学号怎么存、打印干什么用、循环跑几圈、判断走哪边、AI 守不守规矩——正是这门课的主线",
    "学号怎么存、变量怎么起名、打印干什么、循环跑几圈、AI 守不守规矩——正是这门课的主线")

# ── 5 gMap 去剧透：静态图例 ──
rep('''document.getElementById("gMap").innerHTML=Object.entries(GLBL).map(([k,v])=>`<span class="gm${GQ[g.i]&&GQ[g.i].exp===k?" on":""}">${v}</span>`).join("");''',
'''document.getElementById("gMap").innerHTML='<span class="gm">☝ 选项一</span><span class="gm">✌ 选项二</span><span class="gm">👍 是 / 对</span><span class="gm">✊ 否 / 不对</span>';''')

# ── 6 车间：stepsBar 重写（做什么/看哪里/怎么互动）＋命名说明 ──
rep('''  <div class="stepsBar"><b>这一页是一条装配线，共四步：</b>① 选任务 → ② 给变量定值 → ③ 先猜，再让机器人跑 → ④ 对照课件原页。<br><b>为什么要你改数、先猜？</b>机器人跑之前，人先把数定好——这一步就是课件里讲的「赋值」；先猜再看结果，你才能亲眼看见「条件一变、结果就变」。改一个值就够，猜错不扣分。</div>''',
'''  <div class="stepsBar"><b>这一页你只做 3 个动作：</b>① 点一个任务 → ② 把一个变量的数改一改 → ③ 写下你猜的结果，点「▶ 让机器人跑」。<br><b>在哪看什么：</b>改数时，看「图纸」上的数<b>立刻跟着变</b>；跑完，看绿色横幅＋逐行日志（机器人一步步跑给你看）；拿不准，看第④步课件原页。<br><b>和小邮怎么互动：</b>跑完它会点评你的结果；卡住点右下角 🤖 直接问它；愿意就把成绩交给它，去「教师台」看 AI 与老师怎么接力。</div>''')
rep('+"</table>"+\n    `<div class="note">${p.hint}</div>`;',
    '+"</table>"+\n    `<div class="note">变量名＝拼音、见名知义（guanLi＝罐里、mubiao＝目标、meiCi＝每次）——课堂智多星同一个规矩。${p.hint}</div>`;')

# ── 7 车间：改数实时刷新图纸 ──
rep('''oninput="bot.vars['${v[0]}']=this.value"''',
    '''oninput="bot.vars['${v[0]}']=this.value;refreshFlow()"''')
rep("function runBot(){",
'''function refreshFlow(){const p=PROJS[bot.proj],c=botCfg();
  document.getElementById("flowBox").innerHTML=p.rows(c).map((r,i)=>`<div class="flowrow ${r.includes("判断")?"dia":""}"><span class="no">${i+1}</span>${r.replace(/</g,"&lt;")}</div>`).join("");
  document.getElementById("guessLabel").textContent=p.guessLabel;}
function runBot(){''')

# ── 8 runOut 重做：横幅＋逐行日志动画＋小邮点评（旧版日志挤成一段＋油滑话术） ──
rep('''  if(bot.last){const r=bot.last;
    let judge="";
    if(r.guess!==null&&r.guess!==""&&r.actual!==undefined&&!isNaN(parseFloat(r.actual))){
      const ok=Math.abs(parseFloat(r.guess)-parseFloat(r.actual))<1e-9;
      judge=ok?`<div class="verd ok">🎯 猜对了！图纸在你脑子里跑过一遍了——小邮的铃铛给你装上。</div>`
              :`<div class="verd no">🤔 你猜 ${r.guess}，机器人跑出 ${r.actual}。别急着改答案——回图纸「判断」行，把条件在脑子里再跑一圈。</div>`}
    out.innerHTML=`<div class="log">${r.logs.join("\\n")}</div>${judge}
      <button class="btn g" onclick="submitBot()">📮 把成绩交给小邮伴学（进教师台队列）</button>
      <span class="note">提交后到「教师台」看它走完评环闭环。</span>`;
  }else out.innerHTML=`<div class="note">填好你的猜想，再点「让机器人跑」。答案会在跑完之后出现。</div>`;''',
'''  if(bot.last){const r=bot.last;
    let judge="",comment="";
    if(r.guess!==null&&r.guess!==""&&r.actual!==undefined&&!isNaN(parseFloat(r.actual))){
      const ok=Math.abs(parseFloat(r.guess)-parseFloat(r.actual))<1e-9;
      judge=ok?`<div class="verd ok">🎯 你猜 ${r.guess}，机器人跑出 ${r.actual} —— 猜对了！</div>`
              :`<div class="verd no">你猜 ${r.guess}，机器人跑出 ${r.actual} —— 差在哪？到下面日志里找那一步</div>`;
      comment=ok?`条件什么时候停，你心里有数了。改一个数再跑一次试试？`
                :`看日志里「判断」那一行——条件是在哪一圈不成立的？想通了再猜一次。`;}
    out.innerHTML=`${judge}<div class="runlog">${r.logs.map((l,i)=>`<div class="rline" style="animation-delay:${(i*.16).toFixed(2)}s"><span class="rn">${i+1}</span><span>${l}</span></div>`).join("")}</div>`
      +(comment?`<div class="say">🤖 小邮：${comment}</div>`:"")
      +`<button class="btn g" onclick="submitBot()">📮 把成绩交给小邮（教师台可见）</button>`;
  }else out.innerHTML=`<div class="note">先在左边写你猜的数，再点「▶ 让机器人跑」——机器人会一步步跑给你看。</div>`;''')

# ── 9 课堂同步：「问小邮讲这页」＋clsAsk() ──
rep('''<button class="tbtn spot" id="clsSpotBtn" onclick="dkSpot('cls')">🔦 探照灯</button>''',
    '''<button class="tbtn spot" id="clsSpotBtn" onclick="dkSpot('cls')">🔦 探照灯</button>
      <button class="tbtn" onclick="clsAsk()">🤖 问小邮讲这页</button>''')
rep("function refreshFlow(){",
'''function clsAsk(){const a=document.getElementById("aip");if(!a.classList.contains("on"))toggleAip();
  const rail=dkRail("cls"),cur=rail[dkState.cls.cur];
  amsg("ai","这页是「"+cur[1]+"」。先自己读一遍——然后把你卡住的那一句打给我，我帮你拆。我<b>不直接给答案</b>，先让你判断。");}
function refreshFlow(){''')

# ── 10 地图条视觉重做（深红泳道） ──
rep('''.mapBar{background:#fff;border:1.6px solid var(--line);border-radius:16px;padding:12px 16px;margin:0 0 14px}
.mapBar .mt{font-weight:800;color:#8C1F28;margin-bottom:8px;font-size:15px}
.mrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:6px 0}
.mrole{flex:0 0 84px;text-align:center;border-radius:999px;padding:4px 0;font-size:12.5px;font-weight:800}
.mrole.s1{background:#FBEDEA;color:#8C1F28}.mrole.s2{background:#EAF3EA;color:#2E6B2E}.mrole.t1{background:#FDF3E0;color:#8C5A1E}
.mg{border:1.5px solid var(--line);background:#fff;border-radius:12px;padding:6px 12px;font-size:14.5px;font-weight:700;cursor:pointer;text-align:left;line-height:1.35}
.mg:hover{border-color:#8C1F28;background:#FFF7F3}
.mg em{font-style:normal;font-weight:400;font-size:12.5px;color:#6b5d52;display:block}
.mrow>i{color:#B08A6E;font-style:normal;font-weight:700}
.mchip{border:1.4px dashed #B5433A;color:#8C1F28;border-radius:999px;padding:6px 12px;font-size:13.5px;font-weight:700}''',
'''.mapBar{background:linear-gradient(135deg,#7A1B23,#A63A32);border-radius:18px;padding:16px 20px;color:#fff;margin:0 0 14px;box-shadow:0 6px 18px rgba(90,20,20,.16)}
.mapBar .mt{font-weight:800;margin-bottom:10px;font-size:15.5px;letter-spacing:.5px}
.mrow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:9px 0}
.mrole{flex:0 0 96px;text-align:center;border-radius:999px;padding:5px 0;font-size:12.5px;font-weight:800;letter-spacing:1px;border:1px solid rgba(255,255,255,.5)}
.mrole.s1{background:rgba(255,224,130,.28)}.mrole.s2{background:rgba(129,212,250,.24)}.mrole.t1{background:rgba(255,255,255,.26)}
.mg{background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.5);color:#fff;border-radius:12px;padding:8px 14px;font-size:14.5px;font-weight:700;cursor:pointer;text-align:left;line-height:1.35;transition:.15s}
.mg:hover{background:rgba(255,255,255,.26);transform:translateY(-1px)}
.mg em{font-style:normal;font-weight:400;font-size:12.5px;color:rgba(255,255,255,.85);display:block}
.mrow>i{color:rgba(255,255,255,.75);font-style:normal;font-weight:800}
.mchip{border:1.4px dashed rgba(255,255,255,.75);color:#fff;border-radius:999px;padding:8px 14px;font-size:13.5px;font-weight:700}''')

# ── 11 runlog 动画 CSS ──
rep('''.vdesc{color:#6b5d52;font-size:.92em}''',
'''.vdesc{color:#6b5d52;font-size:.92em}
.runlog{margin:10px 0}
.rline{display:flex;gap:9px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px 12px;margin:6px 0;font-size:14.5px;line-height:1.55;opacity:0;transform:translateY(6px);animation:rin .38s forwards}
.rn{flex:0 0 22px;height:22px;border-radius:50%;background:#8C1F28;color:#fff;font-size:12px;display:flex;align-items:center;justify-content:center;font-weight:700;margin-top:1px}
@keyframes rin{to{opacity:1;transform:none}}''')

open(P,"w",encoding="utf-8").write(s)
print("v5e 全部 OK")
