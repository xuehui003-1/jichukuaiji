# -*- coding: utf-8 -*-
# v7.3 立体完成版：①图谱层标签立牌化 ②B3 注入v4(emoji虚拟头像+气泡内头像预览+三按钮:导入名单/导入头像/清除·恢复演示)
# ③车间hero横幅 ④小邮点击提示×2(验真展开按钮上方+课件馆页顶) ⑤手势页再平衡(删hero四符号块/删摄像头note/示范四宫格一排)
# ⑥语音最后6键换声(25/25 完成) ⑦版本v7.3
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 层标签立牌 ═══
rep('.kgTag{position:absolute;left:14px;bottom:-13px;',
    '.kgTag{position:absolute;left:14px;bottom:-14px;transform:rotateX(-50deg);transform-origin:0 100%;')

# ═══ 2 B3 注入 v4 ═══
NAMES = ["张三","李四","王五","赵六","钱七","孙八","周九","吴十","郑十一","冯十二","陈十三","林十四","黄十五","徐十六","马十七","高十八","罗十九","梁二十","宋甲一","唐乙二"]
JSN = "\\n".join(NAMES)
EMO = ["😀","😃","😄","😁","😆","😅","😂","🙂","🙃","😉","😊","😇","🥰","😍","🤩","😘","😗","😚","😙","🥳"]
COLS = ["#F59F23","#4A6FB5","#43A047","#EF6C00","#8E44AD","#00897B"]
AVJS = ('var __st="";'
        'for(var i=0;i<__L.length;i++){var f=__map[__L[i]];'
        '__st+= f?(\'<span title="\'+__L[i]+\'"><img src="\'+f+\'"></span>\'):(\'<span title="\'+__L[i]+\'" style="background:\'+__cl[i%6]+\'">\'+__EM[i%20]+\'</span>\');}'
        '__av.innerHTML=\'<b>虚拟名单</b>\'+__st;')
PREV = "".join('<span style="background:%s">%s</span>' % (COLS[i % 6], EMO[i]) for i in range(8))
INJ = ('<script>try{var __N="' + JSN + '";'
       'var __EM=["' + '","'.join(EMO) + '"];'
       'var __cl=["' + '","'.join(COLS) + '"];'
       'var __pp=document.getElementById("people");'
       'if(__pp){__pp.value=__N;var __sp=document.getElementById("saveP");if(__sp)__sp.click();}'
       'var __L=__N.split("\\n");'
       'var __map={};try{__map=JSON.parse(localStorage.getItem("xyAvFaces")||"{}")}catch(_e){}'
       'var __av=document.createElement("div");__av.className="xyAvatars";'
       + AVJS +
       'document.body.appendChild(__av);'
       'function __paintAv(){var st="";'
       'for(var i=0;i<__L.length;i++){var f=__map[__L[i]];'
       'st+= f?(\'<span title="\'+__L[i]+\'"><img src="\'+f+\'"></span>\'):(\'<span title="\'+__L[i]+\'" style="background:\'+__cl[i%6]+\'">\'+__EM[i%20]+\'</span>\');}'
       '__av.innerHTML=\'<b>虚拟名单</b>\'+st;}'
       'var __tip=document.createElement("div");'
       '__tip.innerHTML=\'<b>📄 虚拟示例名单（张三、李四…）</b><div style="margin:6px 0">' + PREV + '…</div>授课时用右下角按钮一键更换名单和头像，只存本机浏览器。\';'
       '__tip.style.cssText="position:fixed;right:14px;bottom:126px;z-index:9999;max-width:280px;background:rgba(13,20,38,.96);color:#ffe9a8;font-size:13px;line-height:1.6;padding:10px 13px;border-radius:12px;border:1px solid rgba(224,177,58,.55);box-shadow:0 8px 24px rgba(0,0,0,.4)";'
       'document.body.appendChild(__tip);'
       'setTimeout(function(){__tip.style.display="none"},12000);'
       'var __mk=function(txt,bg){var lb=document.createElement("label");'
       'lb.style.cssText="position:fixed;right:14px;z-index:9999;background:"+bg+";color:#221a08;font-weight:800;padding:9px 13px;border-radius:12px;cursor:pointer;font-size:13.5px;box-shadow:0 6px 18px rgba(0,0,0,.45);white-space:nowrap";'
       'return lb};'
       'var __imp=__mk("","#e0b13a");__imp.style.bottom="76px";'
       '__imp.innerHTML=\'📂 导入名单<input type="file" accept=".txt,.csv" style="display:none">\';'
       '__imp.querySelector("input").onchange=function(e){var f=e.target.files[0];if(!f)return;var r=new FileReader();'
       'r.onload=function(){var ns=String(r.result).split(/\\r?\\n/).map(function(x){return x.trim()}).filter(Boolean);'
       'if(ns.length){__pp.value=ns.join("\\n");var sp=document.getElementById("saveP");if(sp)sp.click();__L=ns;__paintAv();alert("已导入 "+ns.length+" 人（只保存到本机浏览器）");}};'
       'r.readAsText(f,"utf-8");};'
       'document.body.appendChild(__imp);'
       'var __avB=__mk("","#8FD3A7");__avB.style.bottom="14px";'
       '__avB.innerHTML=\'🖼 导入头像<input type="file" accept="image/*" multiple style="display:none">\';'
       '__avB.querySelector("input").onchange=function(e){var fs=e.target.files;if(!fs||!fs.length)return;var done=0,idx=0;'
       'function nx(){if(idx>=fs.length){try{localStorage.setItem("xyAvFaces",JSON.stringify(__map))}catch(_e){}__paintAv();alert("已导入 "+done+" 张头像（按文件名匹配名单，未匹配的按顺序分配）");return;}'
       'var f=fs[idx++];var nm=f.name.replace(/\\.[^.]+$/,"");var r=new FileReader();'
       'r.onload=function(){var im=new Image();im.onload=function(){var c2=document.createElement("canvas");c2.width=c2.height=72;'
       'var g2=c2.getContext("2d");g2.drawImage(im,0,0,72,72);var du=c2.toDataURL("image/jpeg",.8);'
       'if(__L.indexOf(nm)>=0){__map[nm]=du}else{for(var k2=0;k2<__L.length;k2++){if(!__map[__L[k2]]){__map[__L[k2]]=du;break}}}'
       'done++;nx();};im.src=String(r.result);};r.readAsDataURL(f);}nx();};'
       'document.body.appendChild(__avB);'
       'var __tg=document.createElement("button");__tg.textContent="🧹 清除演示";'
       '__tg.style.cssText="position:fixed;right:14px;bottom:138px;z-index:9999;background:#F1E6CF;color:#5a3a18;font-weight:800;padding:9px 13px;border-radius:12px;cursor:pointer;font-size:13.5px;border:0;box-shadow:0 6px 18px rgba(0,0,0,.45)";'
       '__tg.onclick=function(){if(__pp.value.trim().length){__pp.value="";var sp=document.getElementById("saveP");if(sp)sp.click();__av.style.display="none";__tg.textContent="🔄 恢复虚拟演示";}else{__pp.value=__N;var sp2=document.getElementById("saveP");if(sp2)sp2.click();__L=__N.split("\\n");__paintAv();__av.style.display="flex";__tg.textContent="🧹 清除演示";}};'
       'document.body.appendChild(__tg);'
       '}catch(e){}</scr' + 'ipt>')

def rebuild(key):
    global s
    m = re.search(r'const %s="([^"]+)"' % key, s)
    b3 = base64.b64decode(m.group(1)).decode("utf-8")
    b3 = re.sub(r'<script>try\{var __N=[\s\S]*?</script>', '', b3)
    assert "__avB" not in b3
    b3 = b3.replace("</body>", INJ + "</body>")
    s = s[:m.start()] + 'const %s="' % key + base64.b64encode(b3.encode("utf-8")).decode() + '"' + s[m.end():]
rebuild("B3B64")
rebuild("B3XYL")

# ═══ 3 车间 hero ═══
bG = base64.b64encode(open("_refs/xy/xyfabG.png", "rb").read()).decode()
ib = s.find('<section id="tab-bot">')
e2 = s.find('<div class="eyebrow">', ib)
eoe = s.find("</div>", e2) + len("</div>")
hero = ('\n  <div class="botHero"><img src="data:image/png;base64,' + bG + '" alt=""><div><b>带你看机器人真跑</b>'
        '<span>① 选任务 → ② 改一个数 → ③ 先猜再跑——猜对了算你赢，猜错了算我教</span>'
        '<div class="bhChips"><u>🤖 真任务</u><u>⚙️ 真运行</u><u>✅ 真验证</u></div></div></div>')
s = s[:eoe] + hero + s[eoe:]

# ═══ 4 小邮点击提示 ×2 ═══
bI = base64.b64encode(open("_refs/xy/xyfabI.png", "rb").read()).decode()
bC = base64.b64encode(open("_refs/xy/xyfabC.png", "rb").read()).decode()
rep('</div><div class="statVeil" onclick="statOpen()"><button class="mapPeekBtn">⤢ 点击展开全部可视化</button></div></div>\';}',
    '</div><img class="xyHint" src="data:image/png;base64,' + bI + '" alt="点这里展开"><div class="statVeil" onclick="statOpen()"><button class="mapPeekBtn">⤢ 点击展开全部可视化</button></div></div>\';}')
rep('<section id="tab-lib">\n  <div class="card" style="margin:0 0 10px"><h3>🎬 课件馆导览 · 一段看完就会用</h3>',
    '<section id="tab-lib">\n  <div class="xySticker"><img src="data:image/png;base64,' + bC + '" alt=""><i>上面输页码，直达任何一页</i></div>\n  <div class="card" style="margin:0 0 10px"><h3>🎬 课件馆导览 · 一段看完就会用</h3>')

# ═══ 5 手势页再平衡 ═══
rep('<div class="gr"><i>☝<em>选项一</em></i><i>✌<em>选项二</em></i><i>👍<em>是 / 对</em></i><i>✊<em>否 / 不对</em></i></div>', '')
rep('<div class="note">没有摄像头？直接点左边题目下的大按钮，效果一样。</div>', '')

# ═══ 6 语音 6 键 ═══
for k2 in ["faqgest","faqys","faqzx","faqxh","faqfx","faqtank"]:
    b = base64.b64encode(open("_refs/xy/%s.mp3" % k2, "rb").read()).decode()
    pat = re.compile(r'("?%s"?\s*:\s*")data:audio/[a-z0-9]+;base64,[A-Za-z0-9+/=]+"' % k2)
    m = pat.search(s)
    assert m, "voice key 未命中: " + k2
    s = s[:m.start()] + m.group(1) + "data:audio/mpeg;base64," + b + '"' + s[m.end():]
print("语音最后 6 键已换声——25/25 全部完成")

# ═══ 7 版本 ═══
rep('v7.2 归位版', 'v7.3 立体完成版')

# ═══ 8 CSS ═══
NEWCSS = '''
.gv{grid-template-columns:repeat(4,1fr)}
.gv figure{margin:0}
.botHero{display:flex;align-items:center;gap:14px;background:linear-gradient(135deg,#8C1F28,#B5433A);border-radius:16px;padding:14px 20px;color:#fff;margin:0 0 12px;flex-wrap:wrap}
.botHero img{width:72px;animation:xyFloat 2.8s ease-in-out infinite;filter:drop-shadow(0 4px 10px rgba(60,10,10,.4))}
.botHero b{font-size:21px;display:block;letter-spacing:1px}
.botHero span{font-size:14px;opacity:.95}
.bhChips{margin-top:6px;display:flex;gap:8px;flex-wrap:wrap}
.bhChips u{text-decoration:none;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:3px 12px;font-size:12.5px;font-weight:800}
.xyHint{position:absolute;right:150px;bottom:70px;width:54px;z-index:6;pointer-events:none;animation:xyFloat 2.8s ease-in-out infinite;filter:drop-shadow(0 4px 10px rgba(90,50,10,.3))}
#statPeek{position:relative}
.xyAvatars span img{width:100%;height:100%;border-radius:50%;object-fit:cover}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.3 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
