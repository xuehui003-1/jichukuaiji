# -*- coding: utf-8 -*-
# v6.2：①上场模块(90-B3 v1.33 原版内嵌 iframe) ②灯箱关闭钮右上角 ③五步重排(看实况第4/验真第5)
# ④验真卡半开渐显 ⑤翻牌审账迁机器人车间+首页改静态"AI怎么被管住"三栏 ⑥置信度文案人话+shf音频重录
# ⑦图谱 kgstage 从零重写(svg满宽自撑,根治gwrap网格污染黑幕) ⑧nav sticky 修复 ⑨hero 删除+header 定位语
# ⑩训练场 rings+知识图谱/虚拟展厅 ⑪实录卡重写(去基础会计形象片+AI赋能注) ⑫VID 换 xfade 平滑版
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 VID 换 xfade 平滑版 ═══
VID = ",".join('"%s":"data:video/mp4;base64,%s"' % (k, b64("_refs/xy/%s.mp4" % k)) for k in ["xyintro", "tmap", "libtour"])
m = re.search(r"const VID=\{[\s\S]*?\};", s)
assert m
s = s[:m.start()] + "const VID={" + VID + "};" + s[m.end():]

# ═══ 2 shf 音频重录版替换 ═══
SHFB64 = b64("_refs/xy/shf.mp3")
s2, n = re.subn(r'shf:"data:audio/mpeg;base64,[^"]+"', 'shf:"data:audio/mpeg;base64,' + SHFB64 + '"', s, count=1)
assert n == 1, "shf 音频键未命中"
s = s2

# ═══ 3 置信度文案人话 ═══
rep("""'<div class="note">规则引擎置信度 '+(SHF.conf*100).toFixed(0)+'% → <b>低于阈值，已自动提交教师终审</b>（教师台可见）</div>'""",
    """'<div class="note">机器人复核：这条账它<b>自己也没把握</b>——按课堂规矩，<b>自动送老师终审</b>（教师台可见）</div>'""")
rep("""'<div class="confbar"><i style="width:'+(SHF.conf*100)+'%;background:#EF6C00"></i></div>'""",
    """'<div class="note" style="margin:6px 0 2px">机器人的把握（越短越拿不准）：</div><div class="confbar"><i style="width:'+(SHF.conf*100)+'%;background:#EF6C00"></i></div>'""")
rep('评环三步：你先判断 → 规则引擎复核并给置信度 → <b>低于 70% 自动进教师终审队列</b>。AI 只出意见，教师拍板——这就是「可信协同」。',
    '评环三步：<b>你先判断 → AI 复核并标明把握 → 拿不准的自动进教师终审队列</b>。AI 只出意见，教师拍板——这就是「可信协同」。')

# ═══ 4 结构手术（从后往前） ═══
# 4a 验真块(lead4..lead5)移到 secVid 卡之后，编号对调
A = s.find('<div class="secLead" id="lead4"')
B = s.find('<div class="secLead" id="lead5"')
assert 0 < A < B
blk = s[A:B]
s = s[:A] + s[B:]
blk = blk.replace('第四步 · 验真', '第五步 · 验真')
TAIL = '视频为外链在线播放；演示现场网络不稳时，可改播仓库内离线视频文件。</div>\n  </div>\n  </div>\n</section>'
assert s.count(TAIL) == 1
s = s.replace(TAIL, '视频为外链在线播放；演示现场网络不稳时，可改播仓库内离线视频文件。</div>\n  </div>\n  </div>\n' + blk + '</section>')
rep('第五步 · 看实况 —— 教师形象 30 秒导览', '第四步 · 看实况 —— 真实课堂实录两段（在线播放）')
rep('<div class="secLead" id="lead4">第五步 · 验真', '<div class="secLead" id="lead5">第五步 · 验真')
rep('<div class="secLead" id="lead5">第四步 · 看实况', '<div class="secLead" id="lead4">第四步 · 看实况')
# 4b secRule 翻牌卡 → 替换为静态"AI怎么被管住"三栏卡
C = s.find('<div class="card" id="secRule">')
D = s.find('<div class="secLead" id="lead3"')
assert 0 < C < D
NEWRULE = '''<div class="card" id="secRule"><h3>🛡 这门课怎么管住 AI<span class="pb">全站核心机制</span></h3>
    <div class="rule3">
      <div class="rcol"><b>① 学生先判断</b><span>每个任务先自己做、先动笔——AI 不代替你回答</span></div>
      <div class="rcol"><b>② AI 只给参考</b><span>机器人复核每条账并标明把握，拿不准的自动送审，不硬下结论</span></div>
      <div class="rcol"><b>③ 教师做终审</b><span>老师的裁定回执直达学生，AI 意见只作参考、不进成绩</span></div>
    </div>
    <div class="note">想亲手试？<button class="btn o" style="padding:3px 12px;margin:0 4px" onclick="showTab('bot')">去「机器人车间」翻牌审账 →</button>老师的裁定队列在「教师台 · 终审队列」。</div>
  </div>
  '''
s = s[:C] + NEWRULE + s[D:]
# 4c bot 加翻牌壳
rep('演 · 造一台属于你的财务机器人</div>',
    '''演 · 造一台属于你的财务机器人</div>
  <div class="card"><h3>🃏 翻牌审账 · 亲手复核一条账</h3><div id="shfBox"></div><div class="note" style="margin-top:8px">翻完去「教师台」看终审队列——低置信的账都在那儿等老师拍板。</div></div>''')
rep('if(t==="home"){renderStats();renderSHF();renderMap("homeMapBox",homeScope)}',
    'if(t==="home"){renderStats();renderMap("homeMapBox",homeScope)}')
rep('if(t==="bot"){renderBot();dkMount("bot",DKRAIL[bot.proj])}',
    'if(t==="bot"){renderBot();renderSHF();dkMount("bot",DKRAIL[bot.proj])}')
# 4d hero 删除（intro 已在页头）
H = s.find('<div class="hero">')
T2 = s.find('<div class="tour"')
assert 0 < H < T2
s = s[:H] + s[T2:]
# 4e tour 钮 4/5 文本对调（顺序不变，指向不变）
rep('<i class="tico">📊</i><span><u>第四步</u>验真</span>', '<i class="tico">🎬</i><span><u>第四步</u>看实况</span>')
rep('<i class="tico">🎬</i><span><u>第五步</u>看实况</span>', '<i class="tico">📊</i><span><u>第五步</u>验真</span>')

# ═══ 5 验真卡半开渐显（statPeek） ═══
m = re.search(r"function renderStats\(\)\{[\s\S]*?function toggleStats\(\)\{[^}]*\}", s)
assert m
NEWSTAT = '''function renderStats(){const D=DATA3;const tot=D.pts.reduce((a,b)=>a+b,0);const pk=D.picks.reduce((a,b)=>a+b,0);
 const dots=Array.from({length:D.enrolled},(_,i)=>'<i class="dt'+(i<D.earned?" on":"")+'"></i>').join("");
 const bars=(label,arr,max,note)=>'<div class="vizRow"><div class="vizL">'+label+'</div><div class="bars3">'+arr.map((v,k)=>'<div class="b3"><i style="height:'+Math.round(v/max*100)+'%"></i><u>'+v+'</u><em>'+D.dates[k]+'</em></div>').join("")+'</div><div class="vizN">'+note+'</div></div>';
 document.getElementById("statsBox").innerHTML=
  '<div class="statFold"><div class="sfT"><b>🛰 三次课真实数据（已匿名聚合）</b><span class="sfSum">'+D.enrolled+' 人在册 · 累计加分 '+tot+' 分 · '+D.earned+' 人已得分 · 抽人 '+pk+' 次</span></div></div>'+
  '<div class="statPeek" id="statPeek">'+
  '<div class="statBody open" id="statBody">'+
  '<div class="vizRow"><div class="vizL">谁得过分</div><div class="dots">'+dots+'</div><div class="vizN">琥珀格 = 三次课里至少得过 1 分的 '+D.earned+' 人 / '+D.enrolled+' 人</div></div>'+
  bars("每次课得分人数",D.ppl,D.enrolled,"第 3 次课 41 人里 39 人发动——覆盖面一路涨")+
  bars("每次课班级总加分",D.pts,100,"加分总数三次翻倍，全部由课堂计分器当场记录")+
  bars("每次课抽人次数",D.picks,12,"随机抽人从 5 次涨到 11 次，记录册暂停点逐次变多")+
  '<div class="vizRow"><div class="vizL">加分场合（真实记录）</div><div class="occL">'+D.occ.map(o=>'<div class="occ"><i style="width:'+Math.round(o[1]/37*100)+'%"></i><u>'+o[0]+'　'+o[1]+' 次 · '+o[2]+' 分</u></div>').join("")+'</div></div>'+
  '<div class="note">数据来源：课堂计分器（随机点名与课堂计分器 v2.0）自动导出，三份原始表（2026-09-04 / 09-11 / 09-18）随作品仓库提交；「场合」为计分器当场记录的真实标签，未作修饰；姓名不出浏览器。</div>'+
  '</div><div class="statVeil" onclick="statOpen()"><button class="mapPeekBtn">⤢ 点击展开全部可视化</button></div></div>';}
function statOpen(){const p=document.getElementById("statPeek");if(p)p.classList.add("open");}'''
s = s[:m.start()] + NEWSTAT + s[m.end():]

# ═══ 6 mVid 关闭钮右上角 ═══
rep('''  <div class="mfoot" style="margin-top:10px;text-align:right"><button class="btn r" onclick="closeVid()">关闭</button></div>
</div></div>
<!-- 手势图解弹窗 -->''',
    '''  <button class="mvX" onclick="closeVid()" aria-label="关闭">✕</button>
</div></div>
<!-- 手势图解弹窗 -->''')

# ═══ 7 图谱从零重写：kgstage（svg 满宽自撑） ═══
rep("""box.innerHTML='<div class="gwrap">'
  +'<svg id="kgSvg" viewBox="0 0 120 68"><g id="kgT" transform="translate(0,0) scale(1)">'+GRAD+ORB+edges+nodes+'</g></svg></div>';""",
    """box.innerHTML='<div class="kgstage">'
  +'<svg id="kgSvg" viewBox="0 0 120 68" style="width:100%;height:auto;display:block;border-radius:14px"><g id="kgT" transform="translate(0,0) scale(1)"><rect x="0" y="0" width="120" height="68" fill="url(#kpaper)"/>'+GRAD+ORB+edges+nodes+'</g></svg></div>';""")
rep('</radialGradient></defs>', '''''' + '''</radialGradient><linearGradient id="kpaper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFDF7"/><stop offset="1" stop-color="#F6ECD9"/></linearGradient><pattern id="kdot" width="3" height="3" patternUnits="userSpaceOnUse"><circle cx=".5" cy=".5" r=".14" fill="rgba(140,31,40,.10)"/></pattern></defs>''')
rep('<rect x="0" y="0" width="120" height="68" fill="url(#kpaper)"/>', '<rect x="0" y="0" width="120" height="68" fill="url(#kpaper)"/><rect x="0" y="0" width="120" height="68" fill="url(#kdot)"/>')

# ═══ 8 nav sticky 修复 ═══
rep('nav{position:relative}', '')

# ═══ 9 header 定位语（AI 赋能导向）＋ header 小邮可点 ═══
rep('sub:"财务机器人课堂智能体 · 高职《财务机器人应用与开发》 ｜ 学生先判断 · AI 只辅助 · 教师做终审",',
    'sub:"高职《财务机器人应用与开发》的 AI 教学搭档：真课件原页入住 · 真机器人能跑 · 真课堂实录 · 真班级数据——AI 全程只辅助，教学全程教师做主",')
rep('<svg width="56" height="56" viewBox="0 0 64 64" aria-label="小邮">',
    '<svg width="56" height="56" viewBox="0 0 64 64" aria-label="小邮（点我看亮相视频）" style="cursor:pointer" onclick="openVid(\'xyintro\',\'🎬 小邮亮相 · 30 秒\')">')

# ═══ 10 训练场 rings 补两个特色入口 ═══
rep('''<u class="rb tch">老师</u><b>🧑‍🏫</b><div class="t">帮你评 · 教师台</div><div class="d">低置信自动进终审队列，裁定回执直达学生；备课预演＋导学建议</div></div>''',
    '''<u class="rb tch">老师</u><b>🧑‍🏫</b><div class="t">帮你评 · 教师台</div><div class="d">低置信自动进终审队列，裁定回执直达学生；备课预演＋导学建议</div></div>
    <div class="ring" onclick="showTab('graph')"><u class="rb">特色</u><b>🕸</b><div class="t">知识星图 · 知识图谱</div><div class="d">四轨道星图铺开全课知识结构，点亮会发光，点节点直达课件页</div></div>
    <div class="ring" onclick="showTab('hall')"><u class="rb">特色</u><b>🏢</b><div class="t">虚拟展厅</div><div class="d">3D 环视四面展墙，平面导览一键切换，点击展墙直达展区</div></div>
    <div class="ring" onclick="showTab('roll')"><u class="rb">特色</u><b>🎲</b><div class="t">上场 · 抽人与名字消消乐</div><div class="d">真实课堂同款工具原版内嵌：开场消名复习、随机抽人回答</div></div>''')

# ═══ 11 secVid 重写（去基础会计形象片 + AI 赋能注） ═══
rep('''<div class="note" style="margin-top:6px">两段均为真实课堂录像（外链在线播放）；离线备份已随作品仓库提交（26 页段 3′24″ / 38 页段 4′06″），演示现场断网可直接播仓库文件。下方为教师形象备选素材：</div>
    <video controls preload="metadata" style="width:100%;border-radius:12px;background:#000;max-height:300px" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/KWTHRZmRympu2GBMUdNjAg.mp4"></video>
    <div class="note" style="margin-top:6px">视频为外链在线播放；演示现场网络不稳时，可改播仓库内离线视频文件。</div>''',
    '''<div class="note" style="margin-top:6px">两段均为真实课堂原声录像：AI 生成的任务在投影上真跑，学生先动笔、AI 复核、老师抽人拍板——<b>AI 赋能下的课堂动线原样呈现</b>。外链在线播放；离线备份已随作品仓库提交（26 页段 3′24″ / 38 页段 4′06″），演示现场断网可直接播仓库文件。</div>''')
rep('<figcaption><b>片段① 开场任务（课件 26 页）</b>课堂导入＋智多星现场建命令，配合「名字消消乐」开场活动</figcaption>',
    '<figcaption><b>片段① 开场任务（课件 26 页）</b>课堂导入＋智多星现场建命令——开场活动用「名字消消乐」，全班 3 分钟把「你自己」装进变量面板</figcaption>')
rep('<figcaption><b>片段② 记录册暂停点⑨（课件 38 页）</b>讲完顺序·条件·循环，学生当堂写记录册，教师随机抽人回答生活实例</figcaption>',
    '<figcaption><b>片段② 记录册暂停点⑨（课件 38 页）</b>讲完顺序·条件·循环→学生当堂写记录册→「上场」随机抽人，用生活实例说清三类结构</figcaption>')

# ═══ 12 上场模块（nav + section + init 注入） ═══
rep('''<button id="tb-gest" onclick="showTab('gest')">🙌 手势闯关</button>''',
    '''<button id="tb-gest" onclick="showTab('gest')">🙌 手势闯关</button>
  <button id="tb-roll" onclick="showTab('roll')">🎲 上场</button>''')
B3 = b64("参赛_2026_AI赋能教学创新展示/90-B3_名字消消乐_上场_v1.33_20260922.html")
rep('''<section id="tab-hall">''',
    '''<section id="tab-roll">
  <div class="eyebrow">🎲 上场 · 真实课堂的抽人与名字消消乐（原版工具内嵌，风格原样）</div>
  <div class="note" style="margin:0 0 8px">开场活动「名字消消乐」：3 分钟把「你自己」装进变量面板，完成举手，学委当场消名；记录册暂停点用「随机抽人」请同学回答——<b>本页就是课堂同款工具，名字消消乐 v1.33</b>；三次课的真实计分数据也由它导出（见首页第五步）。</div>
  <div class="card" style="padding:8px"><iframe id="rollFrame" style="width:100%;height:78vh;border:0;border-radius:10px;background:#FFF8EE" title="上场 · 抽人与名字消消乐"></iframe></div>
</section>
<section id="tab-hall">''')
rep('renderStats();renderSHF();applyMode();renderMap("homeMapBox",homeScope);',
    '''renderStats();renderSHF();applyMode();renderMap("homeMapBox",homeScope);
  const rf=document.getElementById("rollFrame");if(rf)rf.srcdoc=decodeURIComponent(escape(atob(B3B64)));''')
rep('const RVOICE=[', 'const B3B64="' + B3 + '";\nconst RVOICE=[')

# ═══ 13 文案跟进 ═══
rep('home:"先玩下面的「30 秒体验·翻牌审账」——不知道去哪个标签，就照上面那张地图走",',
    'home:"从第一步开始：先看任务地图，顺着五步往下滚，三分钟看懂这门课怎么转",')
rep('去首页「30 秒体验」亲手判断一遍，规则复核会告诉你为什么。',
    '去「机器人车间」翻牌审账亲手判断一遍，机器人复核会告诉你为什么。')
rep('bot:"跟着「第①②③步」走：选任务 → 改一个值 → 先猜再跑。每个变量旁边都写着它是什么",',
    'bot:"跟着「第①②③步」走：选任务 → 改一个值 → 先猜再跑；上方的「翻牌审账」也能亲手复核一条账",')
rep('const TABNUDGE={', 'const TABNUDGE={\n roll:"开场消名字、暂停点抽人——课堂里怎么用这里就怎么用，和教室里一字不差",')
# 30秒体验文字残留检查（翻牌审账在 home 的 h3 已被替换）

# ═══ 14 版本 ═══
rep('v6.1 录档版', 'v6.2 内嵌版')

# ═══ 15 CSS ═══
NEWCSS = '''
.kgstage{background:transparent}
.rule3{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:6px 0 8px}
.rcol{background:#FFF8EE;border:1.5px solid #F2DFC0;border-radius:12px;padding:12px}
.rcol b{display:block;color:#8C1F28;margin-bottom:4px}
.rcol span{font-size:.84em;color:#6b5d52;line-height:1.55}
.mvX{position:absolute;top:8px;right:10px;width:34px;height:34px;border-radius:50%;border:none;background:rgba(80,20,20,.55);color:#fff;font-size:17px;cursor:pointer;z-index:5}
.mvX:hover{background:#8C1F28}
.modal .mcard{position:relative}
.statPeek{position:relative;max-height:250px;overflow:hidden;margin-top:10px}
.statPeek.open{max-height:none}
.statVeil{position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:center;padding-bottom:10px;background:linear-gradient(180deg,rgba(255,252,246,0) 25%,rgba(255,252,246,.97) 82%);cursor:pointer}
.statPeek.open .statVeil{display:none}
'''
_i = s.rfind('</style>')
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v6.2 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
