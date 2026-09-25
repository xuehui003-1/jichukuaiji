# -*- coding: utf-8 -*-
# v7.7 点盘即抽版：①课堂点名转盘中心「开始」可点击=直接抽人(模拟点#draw1)+盘下加注释 ②课件馆「上面输页码」贴纸从页顶右上挪到工具栏页码跳转旁 ③名单导入沿用 v7.6 姓名——
#   ①v7.5 迷你解析器正则未捕获 t="s"，把 xlsx 共享字符串的【索引号】当名字导入（用户实测全是数字 1..N）
#   ②旧逻辑"全表顺序抓值"，会把表头/其他列一并收进来
# v7.6 方案：弃用自造解析器，改调工具原生顶层 parseXlsx()/parseCsvText()（共享字符串/单元格坐标/多表全支持），
#   再做严格「姓名」列扫描：前 5 行内找含「姓名」的列名 → 只取该列之下 → 剔除纯数字与序号前缀 → 上限 200 人；
#   找不到「姓名」列名 → 明确报错指引（绝不回落到第 0 列，杜绝把学号/序号当姓名）。
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

INJ = '''<script>try{
var __N="张三\\n李四\\n王五\\n赵六\\n钱七\\n孙八\\n周九\\n吴十\\n郑十一\\n冯十二\\n陈十三\\n林十四\\n黄十五\\n徐十六\\n马十七\\n高十八\\n罗十九\\n梁二十\\n宋甲一\\n唐乙二";
var __pp=document.getElementById("people");
if(__pp&&__pp.value.trim().length===0){__pp.value=__N;var __sp=document.getElementById("saveP");if(__sp)__sp.click();}
var __L=__N.split("\\n");
function __genFace(i){var bg=["#F59F23","#4A6FB5","#43A047","#EF6C00","#8E44AD","#00897B"][i%6];
var skin=["#FFDFC4","#F0C8A0","#D4A574"][i%3];
var hair=["#2F2A26","#5B3A1E","#7B4B24","#1C1C1E","#4A4A4F"][i%5];
var hp=['M18 20 Q32 4 46 20 L46 26 Q32 14 18 26 Z','M18 20 Q32 6 46 20 L46 24 L52 22 L50 30 Q46 22 18 28 Z','M16 22 Q32 2 48 22 Q50 14 32 8 Q14 14 16 22 Z','M18 18 Q32 8 46 18 L46 30 L42 22 L22 22 L18 30 Z','M20 16 Q32 10 44 16 L44 22 Q32 18 20 22 Z'][i%5];
var girl=(i%2===1);
var svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
+'<rect width="64" height="64" rx="32" fill="'+bg+'"/>'
+(girl?'<path d="M14 30 Q32 10 50 30 L50 54 Q46 44 46 36 L18 36 Q18 44 14 54 Z" fill="'+hair+'"/>':'<path d="'+hp+'" fill="'+hair+'"/>')
+'<circle cx="32" cy="30" r="13" fill="'+skin+'"/>'
+(girl?'<path d="M19 26 Q32 14 45 26 L45 30 Q32 20 19 30 Z" fill="'+hair+'"/>':'')
+'<circle cx="27.5" cy="29" r="1.4" fill="#222"/><circle cx="36.5" cy="29" r="1.4" fill="#222"/>'
+'<path d="M28 34 Q32 37.5 36 34" stroke="#7a3b2e" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
+'<path d="M20 52 Q32 42 44 52 L44 64 L20 64 Z" fill="#FFFDF8" opacity=".92"/>'
+'<path d="M28 50 L32 54 L36 50" stroke="#8C1F28" stroke-width="2" fill="none"/>'
+'</svg>';
return 'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);}
function __redraw(){try{if(window.renderList)renderList()}catch(e){}
 try{if(window.renderCheckout&&document.getElementById("checkout")&&document.getElementById("checkout").classList.contains("on"))renderCheckout()}catch(e){}
 try{if(window.drawWheel)drawWheel((typeof items!=="undefined"&&items.length)?items:__L,(typeof rot!=="undefined")?rot:0,-1)}catch(e){}}
function __seed(){var need=[];__L.forEach(function(n){if(!window.photos||!window.photos[n])need.push(n)});
 var ps=need.map(function(n){return fetch(__genFace(__L.indexOf(n))).then(function(r){return r.blob()}).then(function(b){if(window.putPhoto)return putPhoto(n,b)})});
 Promise.all(ps).then(__redraw).catch(function(){});}
setTimeout(__seed,600);
var __tip=document.createElement("div");
__tip.innerHTML='<b>📄 演示名单与头像均为虚拟示例</b>；授课时用右下角按钮一键导入自己的名单和照片，只存本机浏览器。';
__tip.style.cssText="position:fixed;right:14px;bottom:126px;z-index:9999;max-width:270px;background:rgba(13,20,38,.96);color:#ffe9a8;font-size:13px;line-height:1.6;padding:10px 13px;border-radius:12px;border:1px solid rgba(224,177,58,.55);box-shadow:0 8px 24px rgba(0,0,0,.4)";
document.body.appendChild(__tip);
setTimeout(function(){__tip.style.display="none"},10000);
function __scanNameCol(rows){if(!rows||!rows.length)return null;
 for(var r=0;r<Math.min(rows.length,5);r++){var row=rows[r]||[];
  for(var c=0;c<row.length;c++){var h=String(row[c]==null?"":row[c]).trim();
   if(h.indexOf("姓名")>=0){var out=[];
    for(var rr=r+1;rr<rows.length;rr++){var cell=(rows[rr]||[])[c];
     var v=String(cell==null?"":cell).trim().replace(/^[0-9]+[.、:：)）\\s]+/,"");
     if(v&&!/^[0-9.]+$/.test(v)){out.push(v);if(out.length>=200)return out}}
    if(out.length)return out}}}
 return null}
async function __namesFromFile(f){var nm=(f.name||"").toLowerCase();
 if(/\\.xlsx$/i.test(nm)){
  if(typeof parseXlsx!=="function")throw 0;
  var sheets=await parseXlsx(await f.arrayBuffer());
  var keys=Object.keys(sheets||{}).filter(function(k){return k.charAt()!=="_"&&Array.isArray(sheets[k])});
  for(var i=0;i<keys.length;i++){var ns=__scanNameCol(sheets[keys[i]]);if(ns&&ns.length)return ns}
  return null}
 var text=await f.text();
 if(/\\.csv$/i.test(nm)||f.type==="text/csv")return __scanNameCol(parseCsvText(text));
 var ls=text.split(/\\r?\\n/).map(function(x){return x.replace(/^[0-9]+[.、:：)）\\s]+/,"").trim()}).filter(Boolean);
 if(ls.length&&ls[0].indexOf("姓名")>=0)ls=ls.slice(1);
 return ls.slice(0,200)}
function __afterList(ns){__pp.value=ns.join("\\n");var sp=document.getElementById("saveP");if(sp)sp.click();__L=ns.slice();__redraw();alert("已导入 "+ns.length+" 人（只保存到本机浏览器）");}
var __mk=function(bg){var lb=document.createElement("label");
 lb.style.cssText="position:fixed;right:14px;z-index:9999;background:"+bg+";color:#221a08;font-weight:800;padding:9px 13px;border-radius:12px;cursor:pointer;font-size:13.5px;box-shadow:0 6px 18px rgba(0,0,0,.45);white-space:nowrap";
 return lb};
var __imp=__mk("#e0b13a");__imp.style.bottom="76px";
__imp.innerHTML='📂 导入名单<input type="file" accept=".txt,.csv,.xlsx" style="display:none">';
__imp.querySelector("input").onchange=function(e){var f=e.target.files[0];if(!f)return;
 __namesFromFile(f).then(function(ns){
  if(ns&&ns.length)__afterList(ns);
  else alert("没找到「姓名」列：请让表格第一行有「姓名」这个列名，名字放在这一列之下（不要混入学号、序号、班级等其他数据）；也可另存为「CSV UTF-8」或 txt（一行一个名字）再导入。");
 }).catch(function(){alert("这份表格在浏览器里解析失败：老版 .xls 请先另存为 .xlsx；或在 Excel 里另存为「CSV UTF-8」；或直接用 txt（一行一个名字）。")});};
document.body.appendChild(__imp);
var __avB=__mk("#8FD3A7");__avB.style.bottom="14px";
__avB.innerHTML='🖼 导入头像<input type="file" accept="image/*" multiple style="display:none">';
__avB.querySelector("input").onchange=function(e){var fs=e.target.files;if(!fs||!fs.length)return;var done=0,idx=0;
 function nx(){if(idx>=fs.length){__redraw();alert("已导入 "+done+" 张头像：按文件名匹配名单（如 张三.jpg → 张三），对应同学的名字圆圈立即显示照片。");return;}
  var f=fs[idx++];var nm=f.name.replace(/\\.[^.]+$/,"").trim();
  if(window.putPhoto&&(__L.indexOf(nm)>=0||(__pp.value.split(/\\r?\\n/).indexOf(nm)>=0))){putPhoto(nm,f);done++;}
  nx();}
 nx();};
document.body.appendChild(__avB);
var __hub=document.getElementById("hubTxt");
if(__hub&&__hub.parentNode&&!__hub.parentNode.getAttribute("data-hubgo")){var __hb=__hub.parentNode;
 __hb.setAttribute("data-hubgo","1");__hb.style.cursor="pointer";__hb.title="点击「开始」直接抽人";
 __hb.onclick=function(){var b=document.getElementById("draw1");if(b&&!b.disabled)b.click();};
 var __wn=document.createElement("div");__wn.textContent="👆 点转盘中间的「开始」即可抽人（左侧按钮同样可用）";
 __wn.style.cssText="text-align:center;font-size:12.5px;font-weight:800;color:#8a5a12;background:rgba(255,236,180,.8);border:1px solid #e0c27a;border-radius:999px;padding:4px 12px;margin:8px auto 0;max-width:300px";
 if(__hb.parentNode&&__hb.parentNode.parentNode)__hb.parentNode.parentNode.insertBefore(__wn,__hb.parentNode.nextSibling);}
var __tg=document.createElement("button");__tg.textContent="🧹 清除演示";
__tg.style.cssText="position:fixed;right:14px;bottom:138px;z-index:9999;background:#F1E6CF;color:#5a3a18;font-weight:800;padding:9px 13px;border-radius:12px;cursor:pointer;font-size:13.5px;border:0;box-shadow:0 6px 18px rgba(0,0,0,.45)";
__tg.onclick=function(){
 var cur=__pp.value.trim();
 if(cur&&cur.indexOf("张三")<0){__pp.value=__N;var s1=document.getElementById("saveP");if(s1)s1.click();__L=__N.split("\\n");__tg.textContent="🧹 清除演示";__redraw();return;}
 if(cur){__pp.value="";var s2=document.getElementById("saveP");if(s2)s2.click();__tg.textContent="🔄 恢复虚拟演示";__redraw();}
 else{__pp.value=__N;var s3=document.getElementById("saveP");if(s3)s3.click();__L=__N.split("\\n");__tg.textContent="🧹 清除演示";__seed();__redraw();}};
document.body.appendChild(__tg);
}catch(e){}</scr''' + 'ipt>'


def xy_edits(b3):
    # v7.8 点名口令：默认"回答问题"、播报口语化("×××，到你啦。请起立，回答问题。")、九活动按学生动作分组、去行话
    if 'data-u="answer"' in b3:
        return b3  # 幂等：已应用
    def rep3(old, new):
        nonlocal b3
        c = b3.count(old)
        assert c == 1, "XYL count=%d: %s" % (c, old[:60])
        b3 = b3.replace(old, new)
    # ① USES 新增 answer 并设为默认
    rep3('s0: "要改 0"\n  }\n};\nlet useId = "book";',
         's0: "要改 0"\n  },\n  answer: {\n    label: "回答问题", suggest: "draw1", tip: "",\n    say: "请起立，回答问题", sub: "起立口答，答对加分；答不出可以请同桌帮忙。",\n    s2: "答对 2", s5: "答得好 5", s0: "再想想 0"\n  }\n};\nlet useId = "answer";')
    # ② 去行话：举册子→亮记录册；看凭证→小组亮凭证；台词同步
    rep3('label: "举册子", suggest: "draw3", tip: "",', 'label: "亮记录册", suggest: "draw3", tip: "",')
    rep3('say: "这三位，册子举起来", sub: "写了就行。不用站起来，不用开口。",',
         'say: "请把记录册举起来给大家看", sub: "举起来给大家看一眼就行，先不用开口。",')
    rep3('label: "看凭证", suggest: "drawG",', 'label: "小组亮凭证", suggest: "drawG",')
    rep3('say: "这组，把写好的通用记账凭证举起来",', 'say: "请你们组把写好的记账凭证举起来",')
    rep3('抽一个人上场。', '抽一个人上来。')
    rep3('<h3>上场做什么（点一个）</h3>', '<h3>抽到后做什么（点一个）</h3>')
    # ③ speakLine 播报词重写（评委也听得懂）
    old_speak = 'if(useId==="book") text=who+"。举册子。";\n  else if(useId==="tianping") text=who+"。上来玩天平。";\n  else if(useId==="lianxian") text=who+"。上来连线。";\n  else if(useId==="shuiguang") text=who+"。上来看水管。";\n  else if(useId==="shisuan") text=who+"。上来找漏账。";\n  else if(useId==="mole") text=who+"。上来打地鼠。";\n  else if(useId==="dub") text=who+"。上来配音。";\n  else if(useId==="nitpick") text=who+"。举凭证。";\n  else if(useId==="voucher") text=who+"。举记账凭证。";\n  else text=who+"。"+((USES[useId]&&USES[useId].goBtn)||"上场")+"。";'
    new_speak = 'const call=one?"，到你啦。":"，到你们啦。";\n  if(useId==="answer") text=who+call+"请起立，回答问题。";\n  else if(useId==="book") text=who+call+"请把记录册举起来，给大家看一眼。";\n  else if(useId==="tianping") text=who+call+"上来玩天平。";\n  else if(useId==="lianxian") text=who+call+"上来连一连。";\n  else if(useId==="shuiguang") text=who+call+"上来看水流。";\n  else if(useId==="shisuan") text=who+call+"上来找漏账。";\n  else if(useId==="mole") text=who+call+"上来打地鼠。";\n  else if(useId==="dub") text=who+call+"来给这一段配音。";\n  else if(useId==="nitpick") text=who+call+"把交换来的凭证举起来，帮它找找茬。";\n  else if(useId==="voucher") text=who+call+"请你们组把写好的记账凭证举起来。";\n  else text=who+call+"请做好准备。";'
    rep3(old_speak, new_speak)
    # ④ 按钮重排：动口/亮纸笔/上台 三组
    old_btns = '<div class="uses" id="uses">\n    <button type="button" data-u="book" class="on">举册子</button>\n    <button type="button" data-u="tianping">天平</button>\n    <button type="button" data-u="lianxian">连线</button>\n    <button type="button" data-u="shuiguang">水管</button>\n    <button type="button" data-u="shisuan">试算表</button>\n    <button type="button" data-u="mole">打地鼠</button>\n    <button type="button" data-u="dub">配音</button>\n    <button type="button" data-u="nitpick">找茬</button>\n    <button type="button" data-u="voucher">看凭证</button>\n  </div>'
    new_btns = '<div class="uses" id="uses">\n    <span style="flex:1 1 100%;font-size:11px;font-weight:800;color:#8fb3e8;padding:1px 2px;text-align:left">动口 · 答与说</span>\n    <button type="button" data-u="answer" class="on">回答问题</button>\n    <button type="button" data-u="dub">配音</button>\n    <span style="flex:1 1 100%;font-size:11px;font-weight:800;color:#8fb3e8;padding:1px 2px;text-align:left">亮纸笔 · 查落实</span>\n    <button type="button" data-u="book">亮记录册</button>\n    <button type="button" data-u="nitpick">找茬</button>\n    <button type="button" data-u="voucher">小组亮凭证</button>\n    <span style="flex:1 1 100%;font-size:11px;font-weight:800;color:#8fb3e8;padding:1px 2px;text-align:left">上台 · 玩课件</span>\n    <button type="button" data-u="tianping">天平</button>\n    <button type="button" data-u="lianxian">连线</button>\n    <button type="button" data-u="shuiguang">水管</button>\n    <button type="button" data-u="shisuan">试算表</button>\n    <button type="button" data-u="mole">打地鼠</button>\n  </div>'
    rep3(old_btns, new_btns)
    return b3

def rebuild(key):
    global s
    m = re.search(r'const %s="([^"]+)"' % key, s)
    b3 = base64.b64decode(m.group(1)).decode("utf-8")
    b3 = re.sub(r'<style id="xyInj">[\s\S]*?</style>', "", b3)
    b3 = re.sub(r'<script>try\{\s*var __N=[\s\S]*?</script>', "", b3)
    assert "__genFace" not in b3 and "xyInj" not in b3
    if key == "B3XYL":
        b3 = xy_edits(b3)
    b3 = b3.replace("</body>", INJ + "</body>")
    s = s[:m.start()] + 'const %s="' % key + base64.b64encode(b3.encode("utf-8")).decode() + '"' + s[m.end():]
rebuild("B3B64")
rebuild("B3XYL")

# 课件馆贴纸：从 section 顶部右上角挪到工具栏页码跳转旁(幂等：已挪过则跳过)
if 'style="width:34px;animation:none"' in s:
    m2 = None
else:
    m2 = re.search(r'(<section id="tab-lib">\s*)<div class="xySticker"><img src="(data:image/png;base64,[^"]+)"[^>]*>\s*<i>([^<]*)</i></div>', s)
assert m2 is not None or 'style="width:34px;animation:none"' in s, "tab-lib 贴纸未找到"
if m2 is None:
    m2 = type("X",(),{"start":0,"end":0,"group":lambda self,i:""})()
    _skip = True
else:
    _skip = False
img, tip = m2.group(2), m2.group(3)
if not _skip:
    s = s[:m2.start()] + m2.group(1) + s[m2.end():]
stkr = ('<div class="xySticker" style="position:static;align-items:center;pointer-events:auto;margin:0 4px 0 0;flex:0">'
        '<img src="' + img + '" style="width:34px;animation:none" alt="">'
        '<i style="margin-top:0;max-width:180px;white-space:normal;line-height:1.45">' + tip + '</i></div>\n      ')
if not _skip:
    assert s.count('<input id="libJump"') == 1
    s = s.replace('<input id="libJump"', stkr + '<input id="libJump"')

if "v7.8 到你啦版" not in s:
    rep("v7.7 点盘即抽版", "v7.8 到你啦版")

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.7 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
