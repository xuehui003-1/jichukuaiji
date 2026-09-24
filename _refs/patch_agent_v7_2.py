# -*- coding: utf-8 -*-
# v7.2 归位版：①任务地图箭头=流动箭头(animateMotion+mpath,每条线一枚,随1.6s虚线节奏全程巡游,置于站点上层)
# ②图谱节点立牌化(rotateX(-50deg)+底部锚点,侧面看文字立着) ③手势页左右平衡(gdemo移左列) ④B3注释瘦身+注入v3(强制虚拟名单+头像条+导入+短气泡)
# ⑤语音换声9键(xyintro/faqmap/faq12/faqjd/faqname/faqprint/faqbk/faqwm/faqtask) ⑥版本v7.2
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 流动箭头 ═══
rep("""  const nx=(0.0144*p1[0]+0.2112*mx+0.7744*p2[0]).toFixed(1),ny=(0.0144*p1[1]+0.2112*my+0.7744*p2[1]).toFixed(1);
  path+='<path class="stp" d="M'+p1[0]+' '+p1[1]+' Q'+mx+' '+my+' '+nx+' '+ny+'" marker-end="url(#mArr)"/>';}""",
    """  path+='<path class="stp" id="'+boxId+'L'+k+'" d="M'+p1[0]+' '+p1[1]+' Q'+mx+' '+my+' '+p2[0]+' '+p2[1]+'"/>';
  arrows+='<path class="stpa" d="M-2.2 -1.6 L1.8 0 L-2.2 1.6 z"><animateMotion dur="1.6s" repeatCount="indefinite" rotate="auto"><mpath href="#'+boxId+'L'+k+'"/></animateMotion></path>';}""")
rep(""" let path="";
 for(let k=0;k<stops.length-1;k++){const p1=XY[k],p2=XY[k+1];""",
    """ let path="",arrows="";
 for(let k=0;k<stops.length-1;k++){const p1=XY[k],p2=XY[k+1];""")
rep("""+path+stations+labels+'</svg></div>';""",
    """+path+stations+labels+arrows+'</svg></div>';""")
rep("""box.innerHTML='<div class="mapwrap"><svg viewBox="0 -9 100 72"><defs><marker id="mArr" viewBox="0 0 8 8" refX="5.4" refY="4" markerWidth="3.6" markerHeight="3.6" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="#E8590C"/></marker></defs><text class="decor" x="2" y="-1">🚩</text>""",
    """box.innerHTML='<div class="mapwrap"><svg viewBox="0 -9 100 72"><text class="decor" x="2" y="-1">🚩</text>""")

# ═══ 2 图谱立牌 ═══
# (CSS 在末尾统一覆盖)

# ═══ 3 手势页平衡：gdemo 移左列 ═══
gi = s.find('<div class="gdemo">')
assert gi > 0
# 平衡扫描找匹配 </div>
k = gi
depth = 0
while True:
    m = re.search(r'<div\b|</div>', s[k:])
    off = m.start()
    if m.group(0) == "</div>":
        depth -= 1
    else:
        depth += 1
    k += off
    if depth == 0:
        break
    k += len(m.group(0))
gdemo = s[gi:k + 6]
s = s[:gi] + s[k + 6:]
s = s.replace('<div class="gwrap">\n    <div class="card gmain">',
              '<div class="gwrap">\n    <div class="gleft">\n    <div class="card gmain">')
s = s.replace('      <div id="gNext"></div>\n    </div>\n    <div class="gside">',
              '      <div id="gNext"></div>\n    </div>\n' + gdemo + '\n    </div>\n    <div class="gside">')

# ═══ 4 B3 注释瘦身 ═══
rep("课堂开场：全体动手完成「把你自己装进变量面板」的全部操作，做完举手，老师检查、学委当场消名——<b>名字消消乐 v1.33</b>，正是实录片段①里用的那套（见首页第四步）。名单只存在使用者自己的浏览器本地，公开页不携带真实姓名——页内每次打开都自动显示 20 个虚拟示例名（张三、李四…，不读缓存）；实际授课点页面右下角「📂 导入真实名单」一键换成你的名单（只存本机浏览器）。",
    "开场复习工具：把「你自己」装进变量面板，做完举手、学委消名——实录片段①同款。名单为 20 个虚拟示例（评奖演示随开随用）；授课时点右下角「📂 导入真实名单」一键更换，只存本机浏览器。")
rep("记录册每个暂停点用「随机抽人」请同学回答；页内「下课检查·消名」用于放学前的举册检查——三次课的真实计分数据（首页第五步）正是这套工具导出的。开场用的「名字消消乐」在隔壁「🧹 名字消消乐」标签。名单只存在使用者自己的浏览器本地，公开页不携带真实姓名——页内每次打开都自动显示 20 个虚拟示例名（张三、李四…，不读缓存）；实际授课点页面右下角「📂 导入真实名单」一键换成你的名单（只存本机浏览器）。",
    "记录册暂停点随机抽人，「下课检查·消名」在页内。名单为 20 个虚拟示例（演示用，不读缓存）；授课时右下角一键导入真实名单（只存本机浏览器）。")

# ═══ 5 B3 注入 v3（强制名单+头像条+导入+短气泡） ═══
NAMES = ["张三","李四","王五","赵六","钱七","孙八","周九","吴十","郑十一","冯十二","陈十三","林十四","黄十五","徐十六","马十七","高十八","罗十九","梁二十","宋甲一","唐乙二"]
JSN = "\\n".join(NAMES)
COLS = ["#F59F23","#4A6FB5","#43A047","#EF6C00","#8E44AD","#00897B"]
# 生成头像 span 的 JS（在注入脚本里循环）
AVJS = ('var __cl=["%s"];var __st="";'
        'for(var i=0;i<__L.length;i++){__st+=\'<span title="\'+__L[i]+\'" style="background:\'+__cl[i%%6]+\'">\'+__L[i].slice(0,2)+\'</span>\'}'
        '__av.innerHTML=\'<b>虚拟名单</b>\'+__st;') % '","'.join(COLS)
INJ = ('<script>try{var __N="' + JSN + '";'
       'var __pp=document.getElementById("people");'
       'if(__pp){__pp.value=__N;var __sp=document.getElementById("saveP");if(__sp)__sp.click();}'
       'var __L=__N.split("\\n");'
       'var __av=document.createElement("div");__av.className="xyAvatars";'
       + AVJS +
       'document.body.appendChild(__av);'
       'var __imp=document.createElement("label");'
       '__imp.innerHTML=\'📂 导入真实名单<input type="file" accept=".txt,.csv" style="display:none">\';'
       '__imp.style.cssText="position:fixed;right:14px;bottom:14px;z-index:9999;background:#e0b13a;color:#221a08;font-weight:800;padding:10px 14px;border-radius:12px;cursor:pointer;font-size:14px;box-shadow:0 6px 18px rgba(0,0,0,.45)";'
       '__imp.querySelector("input").onchange=function(e){var f=e.target.files[0];if(!f)return;var r=new FileReader();'
       'r.onload=function(){var ns=String(r.result).split(/\\r?\\n/).map(function(x){return x.trim()}).filter(Boolean);'
       'if(ns.length){__pp.value=ns.join("\\n");var sp=document.getElementById("saveP");if(sp)sp.click();__av.style.display="none";alert("已导入 "+ns.length+" 人（只保存到本机浏览器）");}};'
       'r.readAsText(f,"utf-8");};'
       'document.body.appendChild(__imp);'
       'var __tip=document.createElement("div");'
       '__tip.innerHTML="<b>📄 虚拟示例名单</b>（张三、李四…）；授课时点右下角「📂 导入真实名单」一键更换，只存本机浏览器。";'
       '__tip.style.cssText="position:fixed;right:14px;bottom:64px;z-index:9999;max-width:280px;background:rgba(13,20,38,.96);color:#ffe9a8;font-size:13px;line-height:1.6;padding:10px 13px;border-radius:12px;border:1px solid rgba(224,177,58,.55);box-shadow:0 8px 24px rgba(0,0,0,.4)";'
       'document.body.appendChild(__tip);'
       'setTimeout(function(){__tip.style.display="none"},12000);'
       '}catch(e){}</scr' + 'ipt>')

def rebuild(key):
    global s
    m = re.search(r'const %s="([^"]+)"' % key, s)
    b3 = base64.b64decode(m.group(1)).decode("utf-8")
    b3 = re.sub(r'<script>try\{var __N=[\s\S]*?</script>', '', b3)
    assert "__N" not in b3 and "__av" not in b3
    b3 = b3.replace("</body>", INJ + "</body>")
    s = s[:m.start()] + 'const %s="' % key + base64.b64encode(b3.encode("utf-8")).decode() + '"' + s[m.end():]
rebuild("B3B64")
rebuild("B3XYL")

# ═══ 6 语音换声 9 键 ═══
for k2 in ["xyintro","faqmap","faq12","faqjd","faqname","faqprint","faqbk","faqwm","faqtask"]:
    b = base64.b64encode(open("_refs/xy/%s.mp3" % k2, "rb").read()).decode()
    pat = re.compile(r'("?%s"?\s*:\s*")data:audio/[a-z0-9]+;base64,[A-Za-z0-9+/=]+"' % k2)
    m = pat.search(s)
    assert m, "voice key 未命中: " + k2
    s = s[:m.start()] + m.group(1) + "data:audio/mpeg;base64," + b + '"' + s[m.end():]
print("语音 9 键已换声（累计 19/25）")

# ═══ 7 版本 ═══
rep('v7.1 全员版', 'v7.2 归位版')

# ═══ 8 CSS ═══
NEWCSS = '''
.stpa{fill:#E8590C;opacity:.95}
.gleft{display:flex;flex-direction:column;gap:10px;min-width:0}
.gleft .gdemo{margin-top:0}
.kgN{transform:translate(-50%,-100%) rotateX(-50deg);transform-origin:bottom center}
.xyAvatars{position:fixed;left:14px;bottom:14px;z-index:9998;display:flex;flex-wrap:wrap;gap:5px;max-width:320px;align-items:center}
.xyAvatars b{background:#0b1220;color:#ffe9a8;font-size:11px;padding:3px 9px;border-radius:999px;margin-right:2px;border:1px solid rgba(224,177,58,.5)}
.xyAvatars span{width:32px;height:32px;border-radius:50%;color:#fff;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,.35);border:1.5px solid rgba(255,255,255,.55)}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.2 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
