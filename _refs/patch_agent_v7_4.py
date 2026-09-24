# -*- coding: utf-8 -*-
# v7.4 贴脸版：①B3 注入 v5——样式随脚本进 iframe(头像条彩色圆底终于可见)+清除/恢复后重绘可见界面(消名界面上开着就重绘它,否则弹名单面板)
# ②版本 v7.4
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

NAMES = ["张三","李四","王五","赵六","钱七","孙八","周九","吴十","郑十一","冯十二","陈十三","林十四","黄十五","徐十六","马十七","高十八","罗十九","梁二十","宋甲一","唐乙二"]
JSN = "\\n".join(NAMES)
EMO = ["😀","😃","😄","😁","😆","😅","😂","🙂","🙃","😉","😊","😇","🥰","😍","🤩","😘","😗","😚","😙","🥳"]
COLS = ["#F59F23","#4A6FB5","#43A047","#EF6C00","#8E44AD","#00897B"]
PREV = "".join('<span style="background:%s">%s</span>' % (COLS[i % 6], EMO[i]) for i in range(8))

INJ = ('<style id="xyInj">'
       '.xyAvatars{position:fixed;left:14px;bottom:14px;z-index:9998;display:flex;flex-wrap:wrap;gap:5px;max-width:320px;align-items:center}'
       '.xyAvatars b{background:#0b1220;color:#ffe9a8;font-size:11px;padding:3px 9px;border-radius:999px;margin-right:2px;border:1px solid rgba(224,177,58,.5)}'
       '.xyAvatars span{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;color:#fff;border:1.5px solid rgba(255,255,255,.55);box-shadow:0 2px 6px rgba(0,0,0,.35);overflow:hidden}'
       '.xyAvatars span img{width:100%;height:100%;object-fit:cover}'
       '</style>'
       '<script>try{var __N="' + JSN + '";'
       'var __EM=["' + '","'.join(EMO) + '"];'
       'var __cl=["' + '","'.join(COLS) + '"];'
       'var __pp=document.getElementById("people");'
       'if(__pp){__pp.value=__N;var __sp=document.getElementById("saveP");if(__sp)__sp.click();}'
       'var __L=__N.split("\\n");'
       'var __map={};try{__map=JSON.parse(localStorage.getItem("xyAvFaces")||"{}")}catch(_e){}'
       'var __av=document.createElement("div");__av.className="xyAvatars";'
       'function __paintAv(){var st="";'
       'for(var i=0;i<__L.length;i++){var f=__map[__L[i]];'
       'st+= f?(\'<span title="\'+__L[i]+\'"><img src="\'+f+\'"></span>\'):(\'<span title="\'+__L[i]+\'" style="background:\'+__cl[i%6]+\'">\'+__EM[i%20]+\'</span>\');}'
       '__av.innerHTML=\'<b>虚拟名单</b>\'+st;}'
       '__paintAv();document.body.appendChild(__av);'
       'var __tip=document.createElement("div");'
       '__tip.innerHTML=\'<b>📄 虚拟示例名单（张三、李四…）</b><div style="margin:6px 0">' + PREV + '…</div>授课时用右下角按钮一键更换名单和头像，只存本机浏览器。\';'
       '__tip.style.cssText="position:fixed;right:14px;bottom:126px;z-index:9999;max-width:280px;background:rgba(13,20,38,.96);color:#ffe9a8;font-size:13px;line-height:1.6;padding:10px 13px;border-radius:12px;border:1px solid rgba(224,177,58,.55);box-shadow:0 8px 24px rgba(0,0,0,.4)";'
       'document.body.appendChild(__tip);'
       'setTimeout(function(){__tip.style.display="none"},12000);'
       'function __refresh(){try{if(document.getElementById("checkout")&&document.getElementById("checkout").classList.contains("on")&&window.renderCheckout)renderCheckout();}catch(_e){}'
       '  try{if(window.renderList)renderList();}catch(_e){}'
       '  try{if(window.paintIdle)paintIdle();}catch(_e){}}'
       'var __mk=function(bg){var lb=document.createElement("label");'
       'lb.style.cssText="position:fixed;right:14px;z-index:9999;background:"+bg+";color:#221a08;font-weight:800;padding:9px 13px;border-radius:12px;cursor:pointer;font-size:13.5px;box-shadow:0 6px 18px rgba(0,0,0,.45);white-space:nowrap";'
       'return lb};'
       'var __imp=__mk("#e0b13a");__imp.style.bottom="76px";'
       '__imp.innerHTML=\'📂 导入名单<input type="file" accept=".txt,.csv" style="display:none">\';'
       '__imp.querySelector("input").onchange=function(e){var f=e.target.files[0];if(!f)return;var r=new FileReader();'
       'r.onload=function(){var ns=String(r.result).split(/\\r?\\n/).map(function(x){return x.trim()}).filter(Boolean);'
       'if(ns.length){__pp.value=ns.join("\\n");var sp=document.getElementById("saveP");if(sp)sp.click();__L=ns;__paintAv();__av.style.display="flex";__refresh();alert("已导入 "+ns.length+" 人（只保存到本机浏览器）");}};'
       'r.readAsText(f,"utf-8");};'
       'document.body.appendChild(__imp);'
       'var __avB=__mk("#8FD3A7");__avB.style.bottom="14px";'
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
       '__tg.onclick=function(){'
       'if(__pp.value.trim().length>0&&__pp.value.indexOf("张三")<0){__pp.value=__N;var sp=document.getElementById("saveP");if(sp)sp.click();__L=__N.split("\\n");__paintAv();__av.style.display="flex";__tg.textContent="🧹 清除演示";__refresh();return;}'
       'if(__pp.value.trim().length){__pp.value="";var sp2=document.getElementById("saveP");if(sp2)sp2.click();__av.style.display="none";__tg.textContent="🔄 恢复虚拟演示";__refresh();}'
       'else{__pp.value=__N;var sp3=document.getElementById("saveP");if(sp3)sp3.click();__L=__N.split("\\n");__paintAv();__av.style.display="flex";__tg.textContent="🧹 清除演示";__refresh();}};'
       'document.body.appendChild(__tg);'
       '}catch(e){}</scr' + 'ipt>')

def rebuild(key):
    global s
    m = re.search(r'const %s="([^"]+)"' % key, s)
    b3 = base64.b64decode(m.group(1)).decode("utf-8")
    b3 = re.sub(r'<script>try\{var __N=[\s\S]*?</script>', '', b3)
    b3 = re.sub(r'<style id="xyInj">[\s\S]*?</style>', '', b3)
    assert "__N" not in b3 and "xyInj" not in b3
    b3 = b3.replace("</body>", INJ + "</body>")
    s = s[:m.start()] + 'const %s="' % key + base64.b64encode(b3.encode("utf-8")).decode() + '"' + s[m.end():]
rebuild("B3B64")
rebuild("B3XYL")

rep('v7.3 立体完成版', 'v7.4 贴脸版')

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.4 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
