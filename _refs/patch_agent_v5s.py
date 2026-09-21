# -*- coding: utf-8 -*-
# v5s：①图谱画布透明+浅色纸感3D(黑幕终审:去max-height+透明底+全套浅色覆盖) ②三次课真实数据可视化
# ③第五步=课堂实录两片段(外链26/38页)+原教师形象片 ④音频单例打断+视频音频互斥 ⑤三段分镜动画视频替换
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 VID 重建（动态分镜版） ═══
VID = ",".join('"%s":"data:video/mp4;base64,%s"' % (k, b64("_refs/xy/%s.mp4" % k)) for k in ["xyintro", "tmap", "libtour"])
m = re.search(r"const VID=\{[\s\S]*?\};", s)
assert m and m.group(0).startswith('const VID={"xyintro"')
s = s[:m.start()] + "const VID={" + VID + "};" + s[m.end():]

# ═══ 2 renderStats 重写（真实三次课） ═══
m = re.search(r"function renderStats\(\)\{[\s\S]*?function toggleStats\(\)\{[^}]*\}", s)
assert m, "renderStats 未找到"
NEW = '''const DATA3={dates:["09-04","09-11","09-18"],enrolled:41,ppl:[8,12,39],pts:[37,47,96],picks:[5,6,11],earned:39,
 occ:[["下课检查册子",37,37],["表格·今天",20,84],["举册子",11,28],["改分",7,31]]};
function renderStats(){const D=DATA3;const tot=D.pts.reduce((a,b)=>a+b,0);const pk=D.picks.reduce((a,b)=>a+b,0);
 const dots=Array.from({length:D.enrolled},(_,i)=>'<i class="dt'+(i<D.earned?" on":"")+'"></i>').join("");
 const bars=(label,arr,max,note)=>'<div class="vizRow"><div class="vizL">'+label+'</div><div class="bars3">'+arr.map((v,k)=>'<div class="b3"><i style="height:'+Math.round(v/max*100)+'%"></i><u>'+v+'</u><em>'+D.dates[k]+'</em></div>').join("")+'</div><div class="vizN">'+note+'</div></div>';
 document.getElementById("statsBox").innerHTML=
  '<div class="statFold" onclick="toggleStats()"><div class="sfT"><b>🛰 三次课真实数据（已匿名聚合）</b><span class="sfSum">'+D.enrolled+' 人在册 · 累计加分 '+tot+' 分 · '+D.earned+' 人已得分 · 抽人 '+pk+' 次</span></div><span class="sfHint" id="sfHint">▾ 点击展开可视化</span></div>'+
  '<div class="statBody" id="statBody">'+
  '<div class="vizRow"><div class="vizL">谁得过分</div><div class="dots">'+dots+'</div><div class="vizN">琥珀格 = 三次课里至少得过 1 分的 '+D.earned+' 人 / '+D.enrolled+' 人</div></div>'+
  bars("每次课得分人数",D.ppl,D.enrolled,"第 3 次课 41 人里 39 人发动——覆盖面一路涨")+
  bars("每次课班级总加分",D.pts,100,"加分总数三次翻倍，全部由课堂计分器当场记录")+
  bars("每次课抽人次数",D.picks,12,"随机抽人从 5 次涨到 11 次，记录册暂停点逐次变多")+
  '<div class="vizRow"><div class="vizL">加分场合（真实记录）</div><div class="occL">'+D.occ.map(o=>'<div class="occ"><i style="width:'+Math.round(o[1]/37*100)+'%"></i><u>'+o[0]+'　'+o[1]+' 次 · '+o[2]+' 分</u></div>').join("")+'</div></div>'+
  '<div class="note">数据来源：课堂计分器（随机点名与课堂计分器 v2.0）自动导出，三份原始表（2026-09-04 / 09-11 / 09-18）随作品仓库提交；「场合」为计分器当场记录的真实标签，未作修饰；姓名不出浏览器。</div>'+
  '</div>';}
function toggleStats(){const b=document.getElementById("statBody");if(!b)return;const open=b.classList.toggle("open");const h=document.getElementById("sfHint");if(h)h.textContent=open?"▴ 点击收起":"▾ 点击展开可视化";}'''
s = s[:m.start()] + NEW + s[m.end():]

# ═══ 3 第五步 = 课堂实录两片段 + 原教师形象片 ═══
rep('''<h3>🎬 30 秒案例导览（教师形象 · 在线播放）</h3>
    <video controls preload="metadata" style="width:100%;border-radius:12px;background:#000;max-height:320px" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/KWTHRZmRympu2GBMUdNjAg.mp4"></video>''',
    '''<h3>🎬 看实况 · 真实课堂实录两段（在线播放）</h3>
    <div class="vidRow">
      <figure><video controls preload="none" style="width:100%;border-radius:12px;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/8C9YvXdeGUCHhXiyjrqw6o.mp4"></video><figcaption><b>片段① 开场任务（课件 26 页）</b>课堂导入＋智多星现场建命令，配合「名字消消乐」开场活动</figcaption></figure>
      <figure><video controls preload="none" style="width:100%;border-radius:12px;background:#000;aspect-ratio:16/9" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/fUiT2T3KThx4xiSBQVGTdB.mp4"></video><figcaption><b>片段② 记录册暂停点⑨（课件 38 页）</b>讲完顺序·条件·循环，学生当堂写记录册，教师随机抽人回答生活实例</figcaption></figure>
    </div>
    <div class="note" style="margin-top:6px">两段均为真实课堂录像（外链在线播放，演示现场不稳时可换仓库离线文件）。下方为教师形象备选素材：</div>
    <video controls preload="metadata" style="width:100%;border-radius:12px;background:#000;max-height:300px" src="https://musk-online.fbcontent.cn/pub-musk-ai-studio/user/upload/repo/KWTHRZmRympu2GBMUdNjAg.mp4"></video>''')

# ═══ 4 图谱画布透明+浅色（黑幕终审） ═══
rep('.gwrap{aspect-ratio:120/68;max-height:74vh;min-height:320px;background:linear-gradient(180deg,#0E1420,#0B0F1A);border-radius:14px}',
    '.gwrap{aspect-ratio:120/68;min-height:320px;background:transparent;border-radius:14px}')

# ═══ 5 音频单例（播新停旧）+ 视频/音频互斥 ═══
rep('''function sayVoice(k){try{new Audio(VOICE[k]).play()}catch(e){}''',
    '''let _xyA=null;
function sayVoice(k){try{if(_xyA){_xyA.pause();_xyA=null}
  const _vp=document.getElementById("mvPlayer");if(_vp&&!_vp.paused){try{_vp.pause()}catch(_e){}}
  _xyA=new Audio(VOICE[k]);_xyA.play()}catch(e){}''')
rep('function openVid(k,t){const m=document.getElementById("mVid");if(!m)return;',
    '''function openVid(k,t){const m=document.getElementById("mVid");if(!m)return;
  try{if(_xyA){_xyA.pause();_xyA=null}}catch(e){}''')

# ═══ 6 版本 ═══
rep('v5.9 实况版', 'v6.0 实据版')

# ═══ 7 CSS：图谱浅色覆盖 + 新组件 ═══
NEWCSS = '''
.gwrap{background:transparent;max-height:none}
.gstars{background-image:radial-gradient(560px 300px at 70% 12%,rgba(191,54,12,.07),transparent 70%),radial-gradient(520px 300px at 10% 88%,rgba(74,111,181,.08),transparent 70%),radial-gradient(rgba(140,31,40,.11) 1px,transparent 1.4px),radial-gradient(rgba(74,111,181,.09) 1px,transparent 1.4px);background-size:100% 100%,100% 100%,46px 46px,29px 29px;background-position:0 0,0 0,0 0,14px 22px}
.gwrap:after{content:"";position:absolute;left:6%;right:6%;bottom:4%;height:30%;background:radial-gradient(ellipse at center bottom,rgba(191,54,12,.06),transparent 70%);pointer-events:none}
.ghalo{stroke:rgba(191,54,12,.10)}
.gorb{stroke:rgba(140,31,40,.16)}
.gsh{fill:rgba(90,60,30,.22)}
.geu{stroke:#8a6a48;opacity:.3}
.ge{stroke:#4A6FB5;opacity:.5}
.ge.on{stroke:#BF360C}
.gnp{fill:#fff;stroke:#E7D8C2}
.gnt{fill:#4a2c1e}
.gnd{fill:#8a7a6a}
.gk{fill:#2E7D32}
.gcl{fill:#8C1F28}
.gcore circle{stroke:#8C1F28}
.vidRow{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:760px){.vidRow{grid-template-columns:1fr}}
.vidRow figcaption{font-size:12.5px;color:#6b5d52;margin-top:4px;line-height:1.5}
.vidRow figcaption b{color:#8C1F28}
.bars3{display:flex;gap:16px;align-items:flex-end;height:78px}
.b3{display:flex;flex-direction:column;align-items:center;gap:3px;height:100%;justify-content:flex-end}
.b3 i{width:36px;background:linear-gradient(180deg,#F59F23,#EF6C00);border-radius:6px 6px 0 0;display:block}
.b3 u{text-decoration:none;font-size:12.5px;font-weight:800;color:#BF360C}
.b3 em{font-style:normal;font-size:10.5px;color:#8a7a6a}
.occL{flex:1;min-width:240px;display:grid;gap:6px}
.occ{position:relative;background:#F6E7CC;border-radius:6px;height:22px;overflow:hidden}
.occ i{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#F59F23,#EF6C00);opacity:.7}
.occ u{position:absolute;left:8px;line-height:22px;font-size:.74em;color:#4a2c1e;text-decoration:none;font-weight:700;white-space:nowrap;text-shadow:0 1px 0 rgba(255,255,255,.7)}
'''
_i = s.rfind('</style>')
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v5s OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
