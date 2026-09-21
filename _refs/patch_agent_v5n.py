# -*- coding: utf-8 -*-
# v5n：①修 section 嵌套(5标签空白) ②页头并排教师台/关于 ③课堂同步并入课件馆+录课预留位
# ④首页单地图(删 mapEntry) ⑤30秒体验翻牌化 ⑥统计折叠可视化 ⑦展厅平面导览+点击修复 ⑧下拉建站中选项
import re, os
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:60])
    s = s.replace(old, new)

# ═══ 1 修复 section 嵌套（根因：tab-hall 缺 </section>） ═══
m = re.search(r'(<span class="note">拖动环视 · 点击展墙直达</span></div>)\s*(<section id="tab-graph">)', s)
assert m, "hall 未闭合处未找到"
s = s[:m.start(1)] + '<span class="note">拖动环视 · 点展墙直达 · 平面导览看全局</span></div>\n</section>\n\n<section id="tab-graph">' + s[m.end(2):]

# ═══ 2 页头并排：设置 | 教师台 | 关于 ═══
rep('<button class="gear" onclick="openSettings()">⚙ 设置</button>',
    '<button class="gear" onclick="openSettings()">⚙ 设置</button>\n  <button class="gear gear2" onclick="showTab(\'teach\')">🧑‍🏫 教师台</button>\n  <button class="gear gear2" onclick="showTab(\'about\')">ℹ️ 关于</button>')

# ═══ 3 导航：课堂同步移出主导航；隐藏 state-keeper ═══
rep('<button id="tb-class" onclick="showTab(\'class\')">🏫 课堂同步</button>\n  <button id="tb-lib"',
    '<button id="tb-lib"')
rep('''<div class="corner">
  <button id="tb-teach" onclick="showTab('teach')">🧑‍🏫 教师台</button>
  <button id="tb-about" onclick="showTab('about')">ℹ️ 关于</button>
</div>''',
    '''<div class="corner" style="display:none">
  <button id="tb-class" onclick="showTab('class')">🏫 课堂同步</button>
  <button id="tb-teach" onclick="showTab('teach')">🧑‍🏫 教师台</button>
  <button id="tb-about" onclick="showTab('about')">ℹ️ 关于</button>
</div>''')
rep('nav .nin{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding-right:200px}',
    'nav .nin{display:flex;flex-wrap:wrap;align-items:center;gap:6px}')
rep('''nav .corner{position:absolute;right:12px;top:50%;transform:translateY(-50%);display:flex;gap:6px}
nav .corner button{font-size:13px;padding:7px 12px;opacity:.92}''',
    'nav .corner{display:none}')

# ═══ 4 首页：删除旧 mapEntry 卡（只留一张任务地图） ═══
i = s.find('<div class="card mapEntry">')
assert i > 0
j = s.find('</div></div>', i)
assert 0 < j < i + 700
j += len('</div></div>')
while j < len(s) and s[j] == '\n':
    j += 1
s = s[:i] + s[j:]

# ═══ 5 下拉选项：加项目前缀 + 建站中亮牌（两处同串） ═══
rep('<option value="all">全课程 · 9 站</option><option value="cls">变量·命令·流程（本节课）</option><option value="p3">判断与循环（项目三）</option>',
    '<option value="all">全课程 · 9 站</option><option value="cls">项目二 · 变量·命令·流程（本节课）</option><option value="p3">项目三 · 判断与循环</option><option value="" disabled>其余讲次 · 随课件入住建站</option>', 2)

# ═══ 6 30 秒体验 → 翻牌审账（静态头） ═══
rep('''<h3>🙋 30 秒体验：你判断，AI 复核，老师拍板<span class="pb">全站核心机制</span></h3>
    <div class="note">这是这门课每天在发生的事：学生的账，机器人按规则复核一遍——但 AI 只给参考，<b>判断权在你，裁定权在老师</b>。用下面这道题亲手走一遍：</div>''',
    '''<h3>🙋 30 秒体验：翻牌审账<span class="pb">全站核心机制</span></h3>
    <div class="note">一张牌，三个角色：<b>① 你先判断 → ② 翻牌看 AI 复核 → ③ 等老师拍板</b>。这门课每天在发生的事，30 秒亲手走一遍——判断权在你，裁定权在老师：</div>''')

# ═══ 7 renderSHF 重写为翻牌 + shfFlip ═══
m = re.search(r'function renderSHF\(\)\{.*?document\.getElementById\("shfBox"\)\.innerHTML=h;\s*\}', s, re.S)
assert m, "renderSHF 未找到"
NEW_SHF = '''function renderSHF(){
  const a=state.class.shf;const vd=state.verdicts["case-shf"];
  const roles='<div class="roles"><span class="rc r1'+(a.done?"":" on")+'">① 你判断</span><span class="rc r2'+(a.done?" on":"")+'">② AI 复核</span><span class="rc r3'+(vd?" ok":a.done?" wait":"")+'">③ 老师拍板</span></div>';
  let h=roles+'<div style="font-size:.98em;margin:6px 0 2px">'+SHF.q+'</div>';
  if(!a.done){
    h+=SHF.opts.map((o,i)=>'<button class="opt'+(a.pick===i?" sel":"")+'" onclick="shfFlip('+i+')">'+"ABC"[i]+'. '+o+' <u class="flipHint">🂠 点我翻牌 →</u></button>').join("");
    h+='<div class="note">想好再点——点击选项即翻牌揭晓（先判断，后揭晓）。</div>';
  }else{
    h+='<div class="fcard">';
    h+='<div class="note">你的判断：'+SHF.opts[a.pick]+'</div>';
    h+=a.ok?'<div class="verd ok">✓ 判断正确</div>':'<div class="verd no">✗ 这题不对——看机器人怎么复核</div>';
    h+='<div class="basis"><b>📖 AI 复核（本地规则引擎，可解释）</b><ul>'+SHF.basis.map(b=>'<li>'+b+'</li>').join("")+'</ul></div>';
    h+='<div class="confbar"><i style="width:'+(SHF.conf*100)+'%;background:#EF6C00"></i></div>';
    h+='<div class="note">规则引擎置信度 '+(SHF.conf*100).toFixed(0)+'% → <b>低于阈值，已自动提交教师终审</b>（教师台可见）</div>';
    h+='<div class="badd">🧑‍🏫 教师裁定状态：'+(vd?'<b>'+(vd.pass?"通过 ✓":"退回重判")+'</b>'+(vd.cmt?'｜意见：'+vd.cmt:""):"待教师复核（稍后再来看）")+'</div>';
    h+='<div class="say">💬 '+SHF.ask+'</div>';
    h+=`<div style="margin-top:8px"><button class="btn o" onclick="state.class.shf={};state.queue=state.queue.filter(q=>q.caseId!=='shf'||q.status!=='待复核');delete state.verdicts['case-shf'];persist();renderSHF()">🂠 翻回重做</button></div></div>`;
  }
  document.getElementById("shfBox").innerHTML=h;
}'''
s = s[:m.start()] + NEW_SHF + s[m.end():]
rep('function shfPick(i){state.class.shf.pick=i;persist();renderSHF()}',
    'function shfPick(i){state.class.shf.pick=i;persist();renderSHF()}\nfunction shfFlip(i){const a=state.class.shf;a.pick=i;shfSubmit()}')

# ═══ 8 统计：折叠+点阵+条形 ═══
rep('<div class="stats" id="statsBox"></div>', '<div id="statsBox"></div>')
rep('''<h3>🛰 试点班级真实数据（已匿名聚合）</h3>
    ''', '')
m = re.search(r'function renderStats\(\)\{const s=CONFIG\.stats;.*?`\;}', s, re.S)
assert m, "renderStats 未找到"
NEW_STATS = '''function renderStats(){const s=CONFIG.stats;
  const dots=Array.from({length:s.students},(_,i)=>'<i class="dt'+(i<s.earners?" on":"")+'"></i>').join("");
  document.getElementById("statsBox").innerHTML=
   '<div class="statFold" onclick="toggleStats()"><div class="sfT"><b>🛰 试点班级真实数据（已匿名聚合）</b><span class="sfSum">'+s.students+' 人在册 · '+s.homework+' 份生活记账 · '+s.points+' 分课堂积分</span></div><span class="sfHint" id="sfHint">▾ 点击展开可视化</span></div>'+
   '<div class="statBody" id="statBody">'+
   '<div class="vizRow"><div class="vizL">在册 <b>'+s.students+'</b> 人</div><div class="dots">'+dots+'</div><div class="vizN">琥珀格 = 已获课堂积分的 '+s.earners+' 人（'+s.date+' 止）</div></div>'+
   '<div class="vizRow"><div class="vizL">生活记账 <b>'+s.homework+'</b> 份</div><div class="bar"><i style="width:100%"></i><u>'+s.homework+' 份 · 人均 '+(s.homework/s.students).toFixed(1)+' 份 · 先修《基础会计》真实作业</u></div></div>'+
   '<div class="vizRow"><div class="vizL">课堂积分 <b>'+s.points+'</b> 分</div><div class="bar"><i style="width:'+Math.round(s.points/60*100)+'%"></i><u>'+s.points+' 分（示意刻度 0–60）</u></div></div>'+
   '<div class="vizRow"><div class="vizL">随机抽签 <b>'+s.picks+'</b> 次</div><div class="bar"><i style="width:'+Math.round(s.picks/8*100)+'%"></i><u>'+s.picks+' 次 · 每次全员举册受检（示意刻度 0–8）</u></div></div>'+
   '<div class="note">条形为示意刻度，数字全部是真实聚合数；姓名不出浏览器。</div>'+
   '</div>';}
function toggleStats(){const b=document.getElementById("statBody");if(!b)return;const open=b.classList.toggle("open");const h=document.getElementById("sfHint");if(h)h.textContent=open?"▴ 点击收起":"▾ 点击展开可视化";}'''
s = s[:m.start()] + NEW_STATS + s[m.end():]

# ═══ 9 课堂同步并入课件馆 ═══
rep('🏫 课堂同步 · <b>本节课（命令）19 页</b>', '🏫 课堂同步 · <b>正在上：变量·命令·流程（19 页）</b>')
rep('<div class="note" style="margin:6px 0 0">这里只放这节课正在讲的 19 页',
    '<div class="note" style="margin:6px 0 0">这里只放正在上的课的 19 页')
rep('''  <div class="stage" id="clsStage"></div>
</section>''',
    '''  <div class="stage" id="clsStage"></div>
  <div class="card" style="margin-top:12px"><h3>🎬 录课实例（预留位）</h3>
    <div class="recSlot"><div><b>这里将播放真实课堂录课画面</b><span>薛辉老师的授课实况 · 供课后回看与评审查看 · 素材整理中，上传后在此展示</span></div></div>
    <div class="note" style="margin-top:6px">与上面同步视图对照看：上面是学生视角的课件真页，这里是教师视角的课堂全貌。</div>
  </div>
</section>''')
rep('''<section id="tab-lib">
  <div class="dkToolbar">''',
    '''<section id="tab-lib">
  <div class="syncBan"><div><b>🏫 课堂同步 · 正在上的课</b><span>变量·命令·流程 19 页真页 + 教师录课实例——和教室大屏一字不差</span></div><button class="btn" onclick="showTab('class')">进入同步视图 →</button></div>
  <div class="dkToolbar">''')

# ═══ 10 展厅：点击修复 + 平面导览 ═══
rep('r.addEventListener("pointerdown",e=>{e.preventDefault();hallDrag={x:e.clientX,a:hallA,m:0};try{r.setPointerCapture(e.pointerId)}catch(_){}});',
    'r.addEventListener("pointerdown",e=>{const stq=document.querySelector(".hallStage");if(stq&&stq.classList.contains("flat")){hallDrag=null;return}e.preventDefault();hallDrag={x:e.clientX,a:hallA,m:0,w:e.target.closest?e.target.closest(".wall"):null};try{r.setPointerCapture(e.pointerId)}catch(_){}});')
rep('r.addEventListener("pointerup",e=>{if(hallDrag&&hallDrag.m<6){const w=e.target.closest&&e.target.closest(".wall");if(w&&w.dataset.go)showTab(w.dataset.go)}hallDrag=null});',
    'r.addEventListener("pointerup",e=>{if(hallDrag&&hallDrag.m<6&&hallDrag.w&&hallDrag.w.dataset.go)showTab(hallDrag.w.dataset.go);hallDrag=null});')
rep('<div class="hallCtl"><button class="tbtn" onclick="hallSpin(-38)">‹ 左转</button>',
    '<div class="hallCtl"><button class="tbtn" id="hallFlatBtn" onclick="hallFlat()">🗺 平面导览</button><button class="tbtn" onclick="hallSpin(-38)">‹ 左转</button>')
rep('function hallSpin(d){hallA+=d;applyHall()}',
    'function hallSpin(d){hallA+=d;applyHall()}\nfunction hallFlat(){const st=document.querySelector(".hallStage");if(!st)return;const on=st.classList.toggle("flat");const b=document.getElementById("hallFlatBtn");if(b)b.textContent=on?"🏚 返回环视":"🗺 平面导览";if(!on)applyHall();else{const r=document.getElementById("hallRoom");if(r)r.style.transform="none"}}')
rep('🏢 虚拟展厅 · 按住拖动环视，点击展墙进入', '🏢 虚拟展厅 · 拖动环视 · 点展墙直达 · 可切平面导览')

# ═══ 11 版本 + 气泡文案 ═══
rep('v5.4 精修版', 'v5.5 聚合版')
rep('先玩下面「30 秒体验核心规矩」的判断题——不知道去哪个标签，就照上面那张地图走',
    '先玩下面的「30 秒体验·翻牌审账」——不知道去哪个标签，就照上面那张地图走')

# ═══ 12 新增 CSS ═══
NEWCSS='''
.roles{display:flex;gap:8px;flex-wrap:wrap;margin:2px 0 8px}
.rc{font-size:.78em;font-weight:700;padding:4px 12px;border-radius:999px;background:#F1E7D8;color:#9A8A76;border:1.5px solid #E7D8C2;transition:.25s}
.rc.on{background:#FFF3E0;color:#BF360C;border-color:#F59F23}
.rc.ok{background:#E8F5E9;color:var(--ok);border-color:#C8E6C9}
.rc.wait{background:#FFF8E1;color:var(--warn);border-color:var(--amber)}
.fcard{animation:flipIn .55s ease}
@keyframes flipIn{0%{transform:rotateY(90deg);opacity:0}100%{transform:rotateY(0);opacity:1}}
.flipHint{float:right;font-size:.78em;color:#BF360C;text-decoration:none;font-weight:700}
.statFold{display:flex;justify-content:space-between;align-items:center;gap:10px;cursor:pointer;background:linear-gradient(160deg,#FFF8EE,#FDEAD3);border:1.5px solid #F2DFC0;border-radius:14px;padding:12px 16px;transition:.15s}
.statFold:hover{border-color:#F59F23;box-shadow:0 4px 14px rgba(191,54,12,.12)}
.sfT b{color:#4A2C12;font-size:1.02em}
.sfSum{display:block;font-size:.78em;color:#8A6A48;margin-top:2px}
.sfHint{font-size:.8em;color:#BF360C;font-weight:700;white-space:nowrap}
.statBody{display:none;margin-top:10px}
.statBody.open{display:grid;gap:12px}
.vizRow{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.vizL{flex:0 0 148px;font-size:.86em;color:#6b4a24}
.vizL b{color:#BF360C;font-size:1.15em}
.dots{display:flex;flex-wrap:wrap;max-width:380px;gap:2px}
.dt{width:12px;height:12px;border-radius:3px;background:#EAD9BC;display:inline-block}
.dt.on{background:linear-gradient(160deg,#F59F23,#EF6C00);box-shadow:0 0 0 2px #FFE0B2}
.bar{position:relative;flex:1;min-width:220px;background:#F6E7CC;border-radius:8px;height:24px;overflow:hidden}
.bar i{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#F59F23,#EF6C00);border-radius:8px}
.bar u{position:absolute;right:8px;top:0;line-height:24px;font-size:.72em;color:#5D4037;text-decoration:none;font-weight:600;white-space:nowrap}
.vizN{width:100%;font-size:.74em;color:#8A6A48}
.syncBan{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;background:linear-gradient(135deg,#FFF3E0,#FFE3BF);border:1.5px solid #F2DFC0;border-radius:14px;padding:10px 14px;margin:0 0 10px}
.syncBan b{color:#4A2C12}
.syncBan span{display:block;font-size:.78em;color:#8A6A48;margin-top:2px}
.recSlot{display:flex;gap:14px;align-items:center;border:2px dashed #EFD9B8;border-radius:14px;padding:18px 16px;background:#FFFDF7;font-size:.95em}
.recSlot:before{content:"🎥";font-size:1.9em}
.recSlot b{display:block;color:#4A2C12}
.recSlot span{font-size:.85em;color:#8A6A48;display:block;margin-top:3px}
.hallStage.flat{perspective:none;height:auto;min-height:0;padding:12px}
.hallStage.flat .floor{display:none}
.hallStage.flat .room{position:static;transform:none!important;transform-style:flat;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;width:100%;height:auto;margin:0;cursor:default}
.hallStage.flat .wall{position:static;inset:auto;width:100%;height:230px;opacity:1;display:flex}
'''
_i=s.rfind('</style>');assert _i>0;s=s[:_i]+NEWCSS+s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v5n OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
