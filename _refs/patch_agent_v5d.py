#!/usr/bin/env python3
"""v5d：车间=四步装配线重写；首页使用地图+角色角标+评环卡定位；气泡=点哪提示哪(每标签一次)+事件触发；WebAudio音效"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)

# ── 1 fabNudge：内存 once（刷新即重置，方便反复录演示）＋冷却 15s＋TABNUDGE 表＋音效 ──
rep('''/* 小邮气泡：看到气泡→点右下角小邮；90 秒冷却，once 的本机只弹一次 */
let fabNudgeTimer=null,fabCool=0;
function fabNudge(txt,once){
  if(once){const k="nudge_"+once;try{if(localStorage.getItem(k))return;localStorage.setItem(k,"1")}catch(e){}}
  const now=Date.now();if(now<fabCool)return;fabCool=now+90000;''',
'''/* 小邮气泡：点哪提示哪＋事件触发；每来源一次（刷新重置）；冷却 15s */
let fabNudgeTimer=null,fabCool=0;const fabOnce=new Set();
function fabNudge(txt,once){
  if(once){if(fabOnce.has(once))return;fabOnce.add(once)}
  const now=Date.now();if(now<fabCool)return;fabCool=now+15000;''')
rep('''function fabHide(){const b=document.getElementById("fabNudge");if(b)b.classList.remove("on");}
''',
'''function fabHide(){const b=document.getElementById("fabNudge");if(b)b.classList.remove("on");}
const TABNUDGE={
 home:"先玩下面「30 秒体验核心规矩」的判断题——不知道去哪个标签，就照上面那张地图走",
 class:"这是今天的 19 页课件。先自己想，再点琥珀色提示条揭晓——答案不跟题目同屏",
 lib:"6 份课件 154 页都在这：左边换课件、上面输页码直达；答错的题也从这回原页",
 bot:"跟着「第①②③步」走：选任务 → 改一个值 → 先猜再跑。每个变量旁边都写着它是什么",
 gest:"开摄像头举手就答，没摄像头就点大按钮——答错能一键回课件原页重学",
 teach:"老师的主场：先跑「AI 备课预演」数数它替你做了几个主，再一键生成下节课建议",
 about:"设计思路和技术方案都在这页——想深聊哪一条，右下角问我"};
/* 极简音效（WebAudio 合成，零文件体积）：ok=叮咚 done=上行三音 no=低鸣 */
let _AC=null;
function sfx(k){try{_AC=_AC||new (window.AudioContext||window.webkitAudioContext)();const t=_AC.currentTime;
  const seq=k==="ok"?[[660,0],[990,.12]]:k==="done"?[[523,0],[659,.1],[784,.2]]:k==="no"?[[196,0]]:[[880,0]];
  seq.forEach(([f,d])=>{const o=_AC.createOscillator(),g=_AC.createGain();o.type="sine";o.frequency.value=f;
    g.gain.setValueAtTime(.001,t+d);g.gain.exponentialRampToValueAtTime(.07,t+d+.02);g.gain.exponentialRampToValueAtTime(.001,t+d+.28);
    o.connect(g);g.connect(_AC.destination);o.start(t+d);o.stop(t+d+.32);});}catch(e){}}
''')
# 导航教师台旧内联气泡撤（由 TABNUDGE 统一）
rep('''<button id="tb-teach" onclick="showTab('teach');fabNudge('老师的「下节课建议」就在这页——要我帮你预演一次 AI 备课也行','teach')">📋 教师台</button>''',
    '''<button id="tb-teach" onclick="showTab('teach')">📋 教师台</button>''')
# showTab 挂钩
rep('''if(t==="home"){renderStats();renderSHF()}''',
    '''if(t==="home"){renderStats();renderSHF()}
 if(TABNUDGE[t])fabNudge(TABNUDGE[t],"tab-"+t);''')

# ── 2 首页：使用地图 ──
rep('''  <div class="rings">
    <div class="ring" onclick="showTab('class')"><b>📖</b><div class="t">陪你练 · 课堂同步</div>''',
'''  <div class="mapBar">
    <div class="mt">⏱ 30 秒看懂怎么用（点哪个格子直接去哪）</div>
    <div class="mrow"><span class="mrole s1">学生 · 课上</span><button class="mg" onclick="showTab('class')">🏫 课堂同步<br><em>跟着课件学</em></button><i>→</i><button class="mg" onclick="showTab('gest')">🙌 手势闯关<br><em>全班用手答</em></button></div>
    <div class="mrow"><span class="mrole s2">学生 · 课后</span><button class="mg" onclick="showTab('lib')">📚 课件馆<br><em>忘了随时翻</em></button><i>→</i><button class="mg" onclick="showTab('bot')">🤖 机器人车间<br><em>纸上任务真跑</em></button><i>→</i><span class="mchip">💬 卡住问右下角小邮</span></div>
    <div class="mrow"><span class="mrole t1">老师</span><button class="mg" onclick="showTab('teach')">📋 教师台<br><em>备课预演 · 终审队列 · 下节课建议</em></button></div>
  </div>
  <div class="rings">
    <div class="ring" onclick="showTab('class')"><u class="rb">课上</u><b>📖</b><div class="t">陪你练 · 课堂同步</div>''')
rep('''<div class="ring" onclick="showTab('lib')"><b>📚</b>''','''<div class="ring" onclick="showTab('lib')"><u class="rb">课后</u><b>📚</b>''')
rep('''<div class="ring" onclick="showTab('bot')"><b>🤖</b>''','''<div class="ring" onclick="showTab('bot')"><u class="rb">课后</u><b>🤖</b>''')
rep('''<div class="ring" onclick="showTab('gest')"><b>🙌</b>''','''<div class="ring" onclick="showTab('gest')"><u class="rb">课上</u><b>🙌</b>''')
rep('''<div class="ring" onclick="showTab('teach')"><b>🧑‍🏫</b>''','''<div class="ring" onclick="showTab('teach')"><u class="rb tch">老师</u><b>🧑‍🏫</b>''')
# 评环卡定位句
rep('<div class="card"><h3>🙋 先判断，AI 复核，教师拍板——30 秒试一试<span class="pb">本智能体的核心机制</span></h3>',
    '<div class="card"><h3>🙋 30 秒体验这个智能体的核心规矩<span class="pb">全站都围着它转</span></h3>')
rep('<div id="shfBox"></div>\n  </div>\n  <div class="card"><h3>🛰 试点班级真实数据',
    '<div id="shfBox"></div>\n    <div class="note" style="margin-top:8px">👉 想看老师那边怎么裁？去「教师台」的终审队列走一遍，全流程就通了。</div>\n  </div>\n  <div class="card"><h3>🛰 试点班级真实数据')

# ── 3 机器人车间：整节重写为四步装配线（保留全部功能 ID） ──
i=s.find('<section id="tab-bot">');j=s.find('</section>',i)+len('</section>')
BOT='''<section id="tab-bot">
  <div class="eyebrow">演 · 造一台属于你的财务机器人</div>
  <div class="stepsBar"><b>这一页是一条装配线，共四步：</b>① 选任务 → ② 给变量定值 → ③ 先猜，再让机器人跑 → ④ 对照课件原页。<br><b>为什么要你改数、先猜？</b>机器人跑之前，人先把数定好——这一步就是课件里讲的「赋值」；先猜再看结果，你才能亲眼看见「条件一变、结果就变」。改一个值就够，猜错不扣分。</div>
  <div class="stepH">第 ① 步 · 选一个任务<span>三个任务都出自课件：存钱罐＝17 课 p6–9｜外卖满减＝08 课 p49｜班费记账＝08 课 p50</span></div>
  <div class="chips" id="projChips"></div>
  <div class="stepH">第 ② 步 · 给变量定值<span>看不懂变量名？「这是什么」一列写着；改一个值就行，机器人用你改的数跑</span></div>
  <div class="card"><div id="varTable"></div>
    <details style="margin-top:8px"><summary style="cursor:pointer;font-size:.9em;color:#8C5A1E">进阶（可选）：新建你自己的变量</summary>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
        <input id="nvName" placeholder="给自己的新变量起名（拼音，如 fanka）" style="flex:2;min-width:150px">
        <select id="nvType" style="flex:1;min-width:90px"><option>数值</option><option>字符</option></select>
        <input id="nvVal" placeholder="值" style="flex:1;min-width:80px">
        <button class="btn" onclick="addVar()">新建</button>
      </div>
      <div class="note" id="nvMsg" style="margin-top:6px"></div>
      <div class="note">为什么有这步？课堂智多星上机第一件事就是新建变量——变量名见名知义（fanka＝饭卡），和课堂一个规矩。</div>
    </details>
  </div>
  <div class="stepH">第 ③ 步 · 先猜，再让机器人跑<span>写什么：猜机器人跑完的结果（几圈／多少钱／剩多少）——先判断，后揭晓，课堂同款规矩</span></div>
  <div class="card">
    <div class="note" style="margin:0 0 6px">📐 图纸＝机器人照着跑的步骤单（跑的时候对照它，看清每一步怎么走）</div>
    <div id="flowBox"></div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:10px">
      <span id="guessLabel" style="font-size:.95em"></span>
      <input id="guessVal" class="sel" style="width:130px" inputmode="decimal" placeholder="写你猜的数">
      <button class="btn" onclick="runBot()">▶ 让机器人跑</button>
    </div>
    <div id="runOut" style="margin-top:10px"></div>
  </div>
  <div class="stepH">第 ④ 步 · 对照课件原页<span>下面就是课件里讲这个任务的那几页——课上课件、课后车间，同一套页面</span></div>
  <div class="dkToolbar">
    <div class="dkTitle">📐 课件原页（可直接照着讲）</div>
    <div class="rail" id="botRail"></div>
    <div class="dkBtns">
      <button class="tbtn" onclick="dkPrev()">‹ 上一页</button>
      <span class="pageNo" id="botPageNo"></span>
      <button class="tbtn" onclick="dkNext()">下一页 ›</button>
      <button class="tbtn amber" title="课件答案默认先藏：先自己想，再点逐层揭晓" onclick="dkRevealCur('bot')">✓ 揭晓下一层</button>
      <button class="tbtn spot" id="botSpotBtn" onclick="dkSpot('bot')">🔦 探照灯</button>
    </div>
  </div>
  <div class="stage" id="botStage"></div>
</section>'''
s=s[:i]+BOT+s[j:]

# ── 4 事件气泡＋音效挂点 ──
rep("function runBot(){const p=PROJS[bot.proj],c=botCfg();const r=p.run(c);bot.last={...r,guess:document.getElementById(\"guessVal\").value,actual:r[p.guessKey]};renderBot()}",
"function runBot(){const p=PROJS[bot.proj],c=botCfg();const r=p.run(c);bot.last={...r,guess:document.getElementById(\"guessVal\").value,actual:r[p.guessKey]};renderBot();sfx(\"ok\");fabNudge(\"跑完了！对照上面「图纸」看每一步——再改一个数跑一次，看看结果怎么变\",\"runbot\")}")
rep('''    document.getElementById("gFeedback").innerHTML=`<div class="basis"><b>这五题全部出自你的课件</b>''',
'''    sfx("done");fabNudge("五关全过！把「为什么」讲给同桌听——讲明白才算真会","gdone");
    document.getElementById("gFeedback").innerHTML=`<div class="basis"><b>这五题全部出自你的课件</b>''')
rep('''  g.lock=true;g.awaitRel=true;g.score+=20;''',
'''  g.lock=true;g.awaitRel=true;g.score+=20;sfx("ok");''')
rep('''    fb.innerHTML=`<div class="verd no">✗ 这是${GLBL[name]}''',
'''    sfx("no");
    fb.innerHTML=`<div class="verd no">✗ 这是${GLBL[name]}''')
rep('''  if(ok){const pv=state.class.pv;pv.done=true;pv.name=document.getElementById("pvV0").value;pv.date=new Date().toLocaleDateString("zh-CN");
    persist();pvRender(document.getElementById("pvWrap"));}''',
'''  if(ok){const pv=state.class.pv;pv.done=true;pv.name=document.getElementById("pvV0").value;pv.date=new Date().toLocaleDateString("zh-CN");
    persist();pvRender(document.getElementById("pvWrap"));sfx("done");fabNudge("全对，名字可以消了——「完成了才消」，课堂就是这么点名的","pvdone");}''')

# ── 5 CSS ──
rep('''.vdesc{color:#6b5d52;font-size:.92em}''',
'''.vdesc{color:#6b5d52;font-size:.92em}
.mapBar{background:#fff;border:1.6px solid var(--line);border-radius:16px;padding:12px 16px;margin:0 0 14px}
.mapBar .mt{font-weight:800;color:#8C1F28;margin-bottom:8px;font-size:15px}
.mrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:6px 0}
.mrole{flex:0 0 84px;text-align:center;border-radius:999px;padding:4px 0;font-size:12.5px;font-weight:800}
.mrole.s1{background:#FBEDEA;color:#8C1F28}.mrole.s2{background:#EAF3EA;color:#2E6B2E}.mrole.t1{background:#FDF3E0;color:#8C5A1E}
.mg{border:1.5px solid var(--line);background:#fff;border-radius:12px;padding:6px 12px;font-size:14.5px;font-weight:700;cursor:pointer;text-align:left;line-height:1.35}
.mg:hover{border-color:#8C1F28;background:#FFF7F3}
.mg em{font-style:normal;font-weight:400;font-size:12.5px;color:#6b5d52;display:block}
.mrow>i{color:#B08A6E;font-style:normal;font-weight:700}
.mchip{border:1.4px dashed #B5433A;color:#8C1F28;border-radius:999px;padding:6px 12px;font-size:13.5px;font-weight:700}
.rb{position:absolute;top:10px;right:12px;font-size:11.5px;font-style:normal;font-weight:800;background:#FBEDEA;color:#8C1F28;border-radius:999px;padding:2px 8px;text-decoration:none}
.rb.tch{background:#FDF3E0;color:#8C5A1E}
.stepH{font-weight:800;font-size:16.5px;margin:14px 0 6px;color:#4a2c1e}
.stepH span{font-weight:400;font-size:13px;color:#8a7a6a;margin-left:8px}
details>summary{list-style:none}details>summary:before{content:"▸ "}
details[open]>summary:before{content:"▾ "}''')

open(P,"w",encoding="utf-8").write(s)
print("v5d 全部 OK")
