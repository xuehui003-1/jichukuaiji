#!/usr/bin/env python3
"""v5c：关于页重写(去7连重复/去元文字)；footer怪句；气泡文案；评环卡短句；手势页结构重写；车间三步玩+变量说明列"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %s"%(c,old[:50]))
    s=s.replace(old,new)

# ── 1 关于页整节重写 ──
i=s.find('<section id="tab-about">');j=s.find('</section>',i)+len('</section>')
ABOUT='''<section id="tab-about">
  <div class="card"><h3>🧩 它是怎么设计的</h3>
    <table><tr><th>设计要素</th><th>本作品的做法</th></tr>
    <tr><td><b>给 AI 划边界</b></td><td>学生先自己判断，AI 只负责复核与追问；AI 拿不准的，交教师在「教师台」终审。敏感信息先脱敏——<b>AI 可以干活，不能拍板</b>。</td></tr>
    <tr><td><b>课件共生</b></td><td>和我的课件是同一套页面：本节课 19 页精编轨＋6 份课件 154 页整馆任翻。课上用课件讲，课后用智能体重玩订正。</td></tr>
    <tr><td><b>本地优先</b></td><td>规则引擎和手势识别都跑在本机，断网可用；大模型可选接入、失败自动回退；数据不出浏览器。</td></tr>
    <tr><td><b>双端协同</b></td><td>学生端（练习＋对话）与教师台（终审队列、备课预演、下节课建议）在同一个作品里闭环，裁定回执直达学生。</td></tr>
    <tr><td><b>小邮人设</b></td><td>校园快递站出身的助教机器人：「搬包裹按单子一件件来」正是循环的天赋；说话口语化，只启发、不代答。</td></tr></table>
    <div class="note" style="margin-top:8px">设计源头：本课程「先判断—AI 辅助—教师终审」的教学闭环，是辨·演·训·评·导教学模式中「评、导」两环的产品化。</div>
  </div>
  <div class="card"><h3>⚙ 技术亮点</h3>
    <ul style="margin-left:20px;font-size:.93em;line-height:1.9">
      <li><b>课件真页内嵌</b>：6 份课件 154 页原页整馆入住（课件自身引擎渲染，逐层揭晓、图片灯箱、🔦 探照灯原样保留）——不是仿制，是原页</li>
      <li><b>手势本地识别</b>：MediaPipe 手势识别，21 点手部骨架实时绘制；手势保持半秒防误触；视频只在本机处理、不上传；无摄像头自动按钮兜底</li>
      <li><b>规则引擎本地优先</b>：会计判断先走内置规则表——秒回、可解释、断网可用；8 类典型记账错误（多事并记、现金流等同收入、忽略债权债务等）本地分析</li>
      <li><b>大模型可选接入</b>：OpenAI 兼容接口（DeepSeek、豆包等）；提示词约束「不替学生作答，只做结构化与启发式追问」；失败自动回退演示模式</li>
      <li><b>可信协同</b>：学生先判断，AI 复核给参考，教师终审拍板；AI 替你做的每一个主都摆上台面，由教师采纳或驳回</li>
      <li><b>纯前端单文件</b>：零依赖、可离线、任何静态托管即可发布；数据不出浏览器，公开页不出现学生姓名</li>
    </ul>
  </div>
  <div class="card"><h3>落地与声明</h3>
    <div style="font-size:.93em" id="aboutLand"></div>
  </div>
</section>'''
s=s[:i]+ABOUT+s[j:]

# ── 2 footer 怪句 ──
rep('`学生先判断 → 规则复核 → 低置信度进教师终审 ｜ ${CONFIG.school} · ${CONFIG.cls}（公开页数据已匿名）`',
    '`学生先自己判断，AI 只做复核参考，拿不准的由老师终审 ｜ ${CONFIG.school} · ${CONFIG.cls}（公开页数据已匿名）`')

# ── 3 气泡欢迎语 ──
rep('我是右下角的小邮 🤖 任务卡住、答错想问为什么、想让我帮你查——随时点我',
    '我是小邮 🤖 任务卡住、答错想知道为什么、想让我帮你查——点右下角的我，随时说')

# ── 4 评环卡短句 ──
rep("题目出自同学们在先修课《基础会计》记过的 <b>67 份生活账</b>——旧账新用，正是这门课让 AI 复核的真实业务：你先判断，AI 只做规则复核给置信度，拿不准的自动等老师终审。",
    "爸妈转来的生活费，能直接记成收入吗？——这题出自你们在《基础会计》记过的生活账。规矩只有一条：<b>你先判断，AI 只给复核参考，最后由老师拍板。</b>")
rep("67 份生活记账作业来自先修课《基础会计》——旧账新用：它们是本课「让机器人干会计的活」的真实业务素材",
    "67 份生活记账作业，来自同学们的先修课《基础会计》——本课拿它当真实业务素材：让机器人来干会计的活")

# ── 5 手势页整节重写 ──
i=s.find('<section id="tab-gest">');j=s.find('</section>',i)+len('</section>')
GEST='''<section id="tab-gest">
  <div class="gestHero"><div class="gl"><b>🙌 用手答题</b><span>五道题全部出自课件 · 答对得 20 分 · 答错可回原页重学 · 摄像头视频只在本机处理，不上传不保存</span></div>
    <div class="gr"><i>☝<em>选项一</em></i><i>✌<em>选项二</em></i><i>👍<em>是 / 对</em></i><i>✊<em>否 / 不对</em></i></div></div>
  <div class="gwrap">
    <div class="card gmain">
      <div class="qhead"><span class="tag">课件判断 · 第 <span id="gIdx">1</span>/5 题</span><span class="gscore" id="gScore">得分 0</span></div>
      <h3 id="gTitle" style="margin:6px 0"></h3>
      <p id="gQ" style="font-size:17px;line-height:1.7"></p>
      <div id="gOpts"></div>
      <div id="gFeedback"></div>
      <div id="gNext"></div>
    </div>
    <div class="gside"><div class="card">
      <div class="gcam"><div class="off" id="gOff">摄像头未启用<br><span class="note">视频只在本机由浏览器识别，<br>不上传服务器、不写入任何记录</span></div>
        <video id="gVideo" muted playsinline></video><canvas id="gCanvas"></canvas>
        <span class="gbadge" id="gBadge" style="display:none">21点手部骨架 · 本地实时识别</span>
      </div>
      <button class="btn" id="gBtn" onclick="gToggle()">启用本地手势识别</button>
      <div class="note" id="gErr"></div>
      <div class="gcur">当前识别：<b id="gName">未启用</b><div class="gprog"><i id="gProg"></i></div></div>
      <div class="gmap" id="gMap"></div>
      <div class="note">没有摄像头？直接点左边题目下的大按钮，效果一样。</div>
    </div></div>
  </div>
</section>'''
s=s[:i]+GEST+s[j:]

# ── 6 renderGest 整函数重写 ──
i=s.find("function renderGest(){");j=s.find("function gSubmit(name){")
RENDER='''function renderGest(){
  document.getElementById("gScore").textContent="得分 "+g.score;
  document.getElementById("gMap").innerHTML=Object.entries(GLBL).map(([k,v])=>`<span class="gm${GQ[g.i]&&GQ[g.i].exp===k?" on":""}">${v}</span>`).join("");
  document.getElementById("gIdx").textContent=Math.min(g.i+1,5);
  if(g.i>=GQ.length){
    document.getElementById("gTitle").textContent="✓ 闯关完成！";
    document.getElementById("gQ").textContent=`最终得分 ${g.score} / 100`;
    document.getElementById("gOpts").innerHTML="";
    const bk=(Object.keys(g.errors).length)?`<li>答错的题：点「📖 回课件重学」看原页，再把「为什么」讲给同桌听——讲明白才算真会（费曼）</li>`:`<li>全对！挑一题把「为什么」讲给同桌听——讲明白才算真会（费曼）</li>`;
    document.getElementById("gFeedback").innerHTML=`<div class="basis"><b>这五题全部出自你的课件</b><ul><li>学号怎么存、打印干什么用、循环跑几圈、判断走哪边、AI 守不守规矩——正是这门课的主线</li>${bk}</ul></div><button class="btn o" onclick="gReset()">再闯一遍</button>`;
    document.getElementById("gNext").innerHTML="";
    return;
  }
  const q=GQ[g.i];
  document.getElementById("gTitle").textContent=q.t;
  document.getElementById("gQ").textContent=q.q;
  const yn=q.exp==="Thumb_Up"||q.exp==="Closed_Fist";
  document.getElementById("gOpts").innerHTML=yn
    ?`<button class="gans" onclick="gSubmit('Thumb_Up')">👍 ${q.opts[0]}</button><button class="gans" onclick="gSubmit('Closed_Fist')">✊ ${q.opts[1]}</button>`
    :`<button class="gans" onclick="gSubmit('Pointing_Up')">☝ ${q.opts[0]}</button><button class="gans" onclick="gSubmit('Victory')">✌ ${q.opts[1]}</button>`;
  document.getElementById("gFeedback").innerHTML="";
  document.getElementById("gNext").innerHTML="";
}
'''
s=s[:i]+RENDER+s[j:]

# ── 7 车间：三步玩＋变量说明列＋步骤标签 ──
rep('''  <div class="chips" id="projChips"></div>
  <div class="card"><h3>📦 变量面板（智多星同款：见名知义 · 选对类型）</h3>''',
'''  <div class="stepsBar"><b>三步玩：</b>① 下面选一个任务　② 在「变量面板」改一个值　③ 到「先猜再跑」写下你猜的结果 → 点 ▶ 让机器人跑 → 对照结果。<b>为什么改这些？</b>改不同的数、看结果怎么变——变量和循环在真实任务里就是这么用的。</div>
  <div class="stepTag">第 ① 步 · 选一个任务</div>
  <div class="chips" id="projChips"></div>
  <div class="card"><h3>📦 第 ② 步 · 变量面板——改一个值，机器人照你的改</h3>''')
rep('<h3>📐 图纸（机器人照着跑的那张单子）</h3>','<h3>📐 图纸——机器人照着跑的步骤单（跑的时候对照它看每一步）</h3>')
rep('<h3>🏃 先猜再跑（课堂规矩：先判断，后揭晓）</h3>','<h3>🏃 第 ③ 步 · 先猜再跑——写下你猜的，再看机器人真跑</h3>')
rep('<input id="nvName" placeholder="变量名（拼音，如 fanka）"','<input id="nvName" placeholder="给自己的新变量起名（拼音，如 fanka）"')
# vars 加说明列
rep('''  vars:[["guanLi","数值",0],["mubiao","数值",500],["meiCi","数值",50]],''',
'''  vars:[["guanLi","数值",0,"罐里现在有多少钱"],["mubiao","数值",500,"攒到多少就停"],["meiCi","数值",50,"每次存进去多少"]],''')
rep('''  vars:[["danJia","数值",13.3],["fenShu","数值",12],["manJian","数值",25],["jian","数值",4]],''',
'''  vars:[["danJia","数值",13.3,"一份多少钱"],["fenShu","数值",12,"买几份"],["manJian","数值",25,"满多少才减"],["jian","数值",4,"满了以后减多少"]],''')
rep('''  vars:[["banFei","数值",200],["maiHengFu","数值",50],["maiFeiZhi","数值",30]],''',
'''  vars:[["banFei","数值",200,"班里现在有多少钱"],["maiHengFu","数值",50,"买横幅花掉"],["maiFeiZhi","数值",30,"卖废纸收回"]],''')
rep('''document.getElementById("varTable").innerHTML="<table><tr><th>变量名</th><th>类型</th><th>值（可改，机器人用你改的跑）</th></tr>"+
    p.vars.map(v=>`<tr><td><code>${v[0]}</code></td><td>${v[1]}</td><td><input value="${c[v[0]]}" oninput="bot.vars['${v[0]}']=this.value"></td></tr>`).join("")+"</table>"+''',
'''document.getElementById("varTable").innerHTML="<table><tr><th>变量名</th><th>类型</th><th>这是什么</th><th>值（可改，机器人用你改的跑）</th></tr>"+
    p.vars.map(v=>`<tr><td><code>${v[0]}</code></td><td>${v[1]}</td><td class="vdesc">${v[3]}</td><td><input value="${c[v[0]]}" oninput="bot.vars['${v[0]}']=this.value"></td></tr>`).join("")+"</table>"+''')

# ── 8 CSS 补充 ──
rep('''#fabNudge:after{content:"";position:absolute;right:-9px;bottom:20px;border:8px solid transparent;border-left-color:#8C1F28}''',
'''#fabNudge:after{content:"";position:absolute;right:-9px;bottom:20px;border:8px solid transparent;border-left-color:#8C1F28}
.qhead{display:flex;justify-content:space-between;align-items:center}
.gscore{font-size:13px;background:#F7EFE8;border-radius:999px;padding:3px 10px;color:#8C1F28;font-weight:700}
#gOpts{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0 6px}
.gans{font-size:19px;font-weight:700;padding:16px 8px;border-radius:14px;border:1.6px solid var(--line);background:#fff;cursor:pointer;transition:.15s}
.gans:hover{border-color:#8C1F28;background:#FFF7F3;transform:translateY(-1px)}
.gm{display:inline-block;border:1.3px solid var(--line);border-radius:999px;padding:3px 10px;font-size:13px;margin:2px 4px 0 0;opacity:.55}
.gm.on{border-color:#8C1F28;background:#FBEDEA;opacity:1;font-weight:700}
.stepsBar{background:#FFF7E6;border:1.5px dashed #C8871E;border-radius:12px;padding:10px 14px;margin:0 0 10px;font-size:14.5px;line-height:1.7}
.stepTag{font-weight:700;margin:2px 0 6px}
.vdesc{color:#6b5d52;font-size:.92em}''')

open(P,"w",encoding="utf-8").write(s)
print("v5c 全部 OK")
