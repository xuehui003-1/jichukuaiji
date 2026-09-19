#!/usr/bin/env python3
"""v5f：首页评环卡修渲染；打印题矛盾修复+四手势全覆盖；规矩题点题；气泡欢迎防迟；问答引擎大升级(上下文追问+FAQ)；小邮主动进对话面板+未读红点；问小邮按钮提亮"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)

# ── 1 首页评环卡空白根因：init 漏调 renderSHF ──
rep("  renderStats();applyMode();\n}","  renderStats();renderSHF();applyMode();\n}")

# ── 2 打印题：矛盾修复（正确项与手势一致）＋补 👍 ──
rep(''' {t:"「打印」会改值吗",q:"「打印」只是把变量的值显示到屏幕上。打印之后，变量里存的值会变吗？",opts:["会变","不会变"],exp:"Thumb_Up",know:"打印只显示、不改动",ans:"不会变——想让值变，要用赋值或累加",back:["08",31]},''',
''' {t:"「打印」会改值吗",q:"「打印」只把变量的值显示到屏幕上，不改变变量里存的值——对吗？",opts:["对","不对"],exp:"Thumb_Up",know:"打印只显示、不改动",ans:"对——打印只是把值抄到屏幕上；想让值变，要用赋值或累加",back:["08",31]},''')

# ── 3 规矩题：点明考察什么 ──
rep(''' {t:"AI 的规矩",q:"「AI 一键把 67 份作业全改对，老师就不用检查了」——这句话对吗？",opts:["对","不对"],exp:"Closed_Fist",know:"学生先判断 · AI 只辅助 · 教师做终审",ans:"不对——AI 会「一声不吭替你做主」，它的每个决定都要摆上台面，拍板的永远是老师",back:["08",26]}];''',
''' {t:"规矩题 · 这门课的铁律",q:"有同学说：「AI 一键把 67 份作业全改对，老师就不用检查了。」按这门课的规矩，这个说法对吗？",opts:["对","不对"],exp:"Closed_Fist",know:"学生先判断 · AI 只辅助 · 教师做终审",ans:"不对——AI 会「一声不吭替你做主」，它的每个决定都要摆上台面，拍板的永远是老师",back:["08",26]}];''')

# ── 4 欢迎气泡：如果用户已在互动（见过任何提示），就不再补欢迎 ──
rep('setTimeout(()=>fabNudge("我是小邮 🤖 任务卡住、答错想知道为什么、想让我帮你查——点右下角的我，随时说","hi"),12000);',
    'setTimeout(()=>{if(fabOnce.size===0)fabNudge("我是小邮 🤖 任务卡住、答错想知道为什么、想让我帮你查——点右下角的我，随时说","hi")},12000);')

# ── 5 问小邮讲这页：提亮＋气泡里点名 ──
rep('''<button class="tbtn" onclick="clsAsk()">🤖 问小邮讲这页</button>''',
    '''<button class="tbtn amber" onclick="clsAsk()">🤖 问小邮讲这页</button>''')
rep('class:"这是今天的 19 页课件。先自己想，再点琥珀色提示条揭晓——答案不跟题目同屏"',
    'class:"这是今天的 19 页课件。先自己想，再点琥珀色提示条揭晓；要我讲这页，点工具条上的「🤖 问小邮讲这页」"')

# ── 6 fab 未读红点 ──
rep('<button class="fab" onclick="toggleAip()" title="小邮伴学助手">🤖</button>',
    '<button class="fab" onclick="toggleAip()" title="小邮伴学助手">🤖<i id="fabDot" style="display:none"></i></button>')
rep('''.fab{position:fixed;right:18px;bottom:18px;''','''.fab{position:fixed;right:18px;bottom:18px;overflow:visible;''')
rep('#fabNudge{position:fixed;',
    '''#fabDot{position:absolute;top:-3px;right:-3px;min-width:20px;height:20px;border-radius:999px;background:#D84315;color:#fff;font-size:12px;font-style:normal;display:flex;align-items:center;justify-content:center;padding:0 5px;border:2px solid #fff;z-index:70}
#fabNudge{position:fixed;''')

# ── 7 amsg 未读计数 + toggleAip 清零 + botSay 助手 ──
rep('function amsg(t,txt){const box=document.getElementById("aMsgs");const d=document.createElement("div");\n  d.className="m "+t;d.innerHTML=txt;box.appendChild(d);box.scrollTop=box.scrollHeight;return d}',
'''function amsg(t,txt){const box=document.getElementById("aMsgs");const d=document.createElement("div");
  d.className="m "+t;d.innerHTML=txt;box.appendChild(d);box.scrollTop=box.scrollHeight;
  const ip=document.getElementById("aip");
  if(t==="ai"&&!ip.classList.contains("on")){const dot=document.getElementById("fabDot");if(dot){dot.style.display="flex";dot.textContent=(parseInt(dot.textContent||"0",10)||0)+1}}
  return d}
function botSay(txt){return amsg("ai",txt)}''')
rep('function toggleAip(){const p=document.getElementById("aip");p.classList.toggle("on");',
    'function toggleAip(){const p=document.getElementById("aip");p.classList.toggle("on");\n  if(p.classList.contains("on")){const dot=document.getElementById("fabDot");if(dot){dot.style.display="none";dot.textContent=""}}')

# ── 8 车间跑完 → 小邮进对话面板（带追问按钮） ──
rep('function runBot(){const p=PROJS[bot.proj],c=botCfg();const r=p.run(c);bot.last={...r,guess:document.getElementById("guessVal").value,actual:r[p.guessKey]};renderBot();sfx("ok");fabNudge("跑完了！对照上面「图纸」看每一步——再改一个数跑一次，看看结果怎么变","runbot")}',
'''function runBot(){const p=PROJS[bot.proj],c=botCfg();const r=p.run(c);bot.last={...r,guess:document.getElementById("guessVal").value,actual:r[p.guessKey]};renderBot();sfx("ok");fabNudge("跑完了！对照上面「图纸」看每一步——再改一个数跑一次，看看结果怎么变","runbot");
  botSay(`我在「机器人车间」陪跑了一台：${p.name}，结果 ${r.result}。<button class="btn o" style="padding:2px 10px;margin-top:4px" onclick="aAsk('为什么是这个结果？')">为什么是这个结果？</button>`)}''')

# ── 9 评环提交 → 小邮进对话面板（首次） ──
rep('''    ai:`规则复核：${SHF.basis[0]}｜正确参考：${SHF.opts[SHF.right]}`,conf:SHF.conf,status:"待复核"});''',
'''    ai:`规则复核：${SHF.basis[0]}｜正确参考：${SHF.opts[SHF.right]}`,conf:SHF.conf,status:"待复核"});
  if(!globalThis.shfAsked){globalThis.shfAsked=true;
    botSay(`你刚在首页判断了「${SHF.opts[a.pick]}」，我复核只有 ${(SHF.conf*100).toFixed(0)}% 的把握。<button class="btn o" style="padding:2px 10px;margin-top:4px" onclick="aAsk('为什么拿不准？')">为什么拿不准？</button>`)}''')
rep('type:"课堂同步·生活费"','type:"课堂同步·审账复核"')

# ── 10 aBrain：上下文追问＋新 FAQ＋去过时指引 ──
rep('''function aBrain(q,short){
  const has=(...ws)=>ws.some(w=>q.includes(w));''',
'''function aBrain(q,short){
  const has=(...ws)=>ws.some(w=>q.includes(w));
  if(/为什么.*(结果|圈|元|剩)/.test(q)&&typeof bot!=="undefined"&&bot.last){const r=bot.last;
    return `你刚跑的是「${PROJS[bot.proj].name}」：${r.logs[0]}……最后停在 <b>${r.actual}</b>。关键看日志里「判断」那一行——条件在哪一圈从「继续」变成「停」，结果就定在哪。不信？改一个数再跑一次，规律自己撞出来。`;}
  if(has("拿不准","没把握")&&state.class.shf.done){return `你刚那题我只有 ${(SHF.conf*100).toFixed(0)}% 的把握：规则能确定「一件事记一条」，但真实账目花样多，我按规矩不硬撑——<b>低于 70% 就交老师终审</b>。这不叫没本事，叫守规矩。`;}
  if(has("怎么用手答","手答题","怎么答","没有摄像头","没摄像头"))return "「手势闯关」四种手势：☝＝选项一、✌＝选项二、👍＝是/对、✊＝否/不对，对着摄像头保持半秒就提交。没摄像头？点题目下面两张大按钮，效果一模一样。答错的题点「📖 回课件重学」直达原页。";
  if(has("讲这页","问小邮"))return "在「课堂同步」的工具条上点「🤖 问小邮讲这页」，我就会告诉你当前页讲什么——然后把卡住的那句打给我，我帮你拆（不直接给答案）。";
  if(has("车间","装配线","怎么玩","怎么操作"))return "「机器人车间」就 3 个动作：①点一个任务 ②把一个变量的数改一改（图纸上的数会立刻跟着变）③写下你猜的结果，点「▶ 让机器人跑」。跑完我会在对话里给你留话。";
  if(has("学号","字符","前导零"))return "学号是<b>编号</b>不是数量：不用来加减，就要存「字符」——存成数值会弄丢前面的 0，还可能被人拿去算。去课件 p26 亲手试试，选错我会翻脸。";
  if(has("打印","显示"))return "「打印」只是把值<b>抄到屏幕上</b>给人看，变量格子里存的值不动。想让值变：赋值（=）或累加（+=）。课件 p31 有三行命令对照，去翻翻。";''')
rep('if(has("生活费","收入"))return "好问题——但我<b>不直接给答案</b> 😤 去「课堂同步」的「评环·生活费判断」，先选一个你的判断，提交后规则复核会告诉你为什么。提示只给一句：钱到账 ≠ 你赚的。";',
    'if(has("生活费","收入"))return "好问题——但我<b>不直接给答案</b> 😤 去首页「30 秒体验」亲手判断一遍，规则复核会告诉你为什么。提示只给一句：钱到账 ≠ 你赚的，先分清来源。";')
rep('想练肌肉记忆？「手势闯关」第 2、3 关就是债权和义务的方向题。";','想练肌肉记忆？「手势闯关」五道题全出自课件，用手势答一遍就记住了。";')
rep('const AQUICK=["生活费是收入吗？","十二个货怎么分？","借贷方向怎么记？","存钱罐怎么改圈数？","分析：打车去吃饭一共58元记餐饮"];',
    'const AQUICK=["怎么用手答题？","生活费是收入吗？","存钱罐怎么改圈数？","学号为什么存字符？","分析：打车去吃饭一共58元记餐饮"];')

open(P,"w",encoding="utf-8").write(s)
print("v5f 全部 OK")
