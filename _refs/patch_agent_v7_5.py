# -*- coding: utf-8 -*-
# v7.5 头像进圈版：①删除左下角"虚拟名单+emoji"横条(用户否定) ②20 个虚拟学生=程序生成 SVG 卡通头像,经工具自带 putPhoto 灌入
#    →名单面板圆圈/消名界面圆圈/抽人转盘 全部显示虚拟照片(IndexedDB 持久化,不覆盖用户自定义)
# ③🖼导入头像改走 putPhoto(修 v7.4 写错存储致圆圈不显示) ④📂导入名单支持 .xlsx(DecompressionStream 最小解析器)+csv+txt
# ⑤清除/恢复 refresh 增加重绘转盘 ⑥气泡改短无头像预览 ⑦版本 v7.5
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
async function __readXlsx(f){
 var buf=new Uint8Array(await f.arrayBuffer());var dv=new DataView(buf.buffer);
 var eocd=-1;for(var i=buf.length-22;i>=Math.max(0,buf.length-66000);i--){if(dv.getUint32(i,true)===0x06054b50){eocd=i;break}}
 if(eocd<0)throw 0;
 var cnt=dv.getUint16(eocd+10,true),off=dv.getUint32(eocd+16,true),entries={},p=off;
 for(var k=0;k<cnt;k++){if(dv.getUint32(p,true)!==0x02014b50)break;
  var method=dv.getUint16(p+10,true),csize=dv.getUint32(p+20,true),nlen=dv.getUint16(p+28,true),elen=dv.getUint16(p+30,true),clen=dv.getUint16(p+32,true),lho=dv.getUint32(p+42,true);
  var name=new TextDecoder().decode(buf.slice(p+46,p+46+nlen));entries[name]={method:method,csize:csize,lho:lho};p+=46+nlen+elen+clen;}
 async function unz(name){var e=entries[name];if(!e)return null;
  var lp=e.lho,nl=dv.getUint16(lp+26,true),el=dv.getUint16(lp+28,true);
  var data=buf.slice(lp+30+nl+el,lp+30+nl+el+e.csize);
  if(e.method===0)return new TextDecoder().decode(data);
  var stream=new Blob([data]).stream().pipeThrough(new DecompressionStream("deflate-raw"));
  return await new Response(stream).text();}
 var ss=[];var sst=await unz("xl/sharedStrings.xml");
 if(sst){var m0,sre=/<t[^>]*>([\\s\\S]*?)<\\/t>/g;while((m0=sre.exec(sst)))ss.push(m0[1].replace(/&amp;/g,"&").replace(/&lt;/g,"<").replace(/&gt;/g,">"));}
 var sheet=await unz("xl/worksheets/sheet1.xml");if(!sheet)throw 0;
 var names=[],seen={},cre=/<c[^>]*?(?: t="(\\w+)")?[^>]*>(?:<v>([\\s\\S]*?)<\\/v>)?(?:<is><t[^>]*>([\\s\\S]*?)<\\/t><\\/is>)?/g,cm;
 while((cm=cre.exec(sheet))){var typ=cm[1],v=cm[2],isv=cm[3],val="";
  if(typ==="s"&&v!==undefined)val=ss[+v]||"";else if(isv!==undefined)val=isv;else if(v!==undefined)val=v;
  val=String(val).trim().replace(/&amp;/g,"&");if(val&&!seen[val]){seen[val]=1;names.push(val)}}
 if(!names.length)throw 0;return names.slice(0,200);}
function __afterList(ns){__pp.value=ns.join("\\n");var sp=document.getElementById("saveP");if(sp)sp.click();__L=ns.slice();__redraw();alert("已导入 "+ns.length+" 人（只保存到本机浏览器）");}
var __mk=function(bg){var lb=document.createElement("label");
 lb.style.cssText="position:fixed;right:14px;z-index:9999;background:"+bg+";color:#221a08;font-weight:800;padding:9px 13px;border-radius:12px;cursor:pointer;font-size:13.5px;box-shadow:0 6px 18px rgba(0,0,0,.45);white-space:nowrap";
 return lb};
var __imp=__mk("#e0b13a");__imp.style.bottom="76px";
__imp.innerHTML='📂 导入名单<input type="file" accept=".txt,.csv,.xlsx" style="display:none">';
__imp.querySelector("input").onchange=function(e){var f=e.target.files[0];if(!f)return;
 if(/\\.xlsx$/i.test(f.name)){__readXlsx(f).then(function(ns){__afterList(ns)}).catch(function(){alert("此 Excel 无法在浏览器直接解析，请在 Excel 中另存为「CSV UTF-8」后再导入，或直接用 txt（一行一个名字）")});return;}
 var r=new FileReader();
 r.onload=function(){var ns=String(r.result).split(/\\r?\\n/).map(function(x){return x.trim()}).filter(Boolean);
  if(ns.length)__afterList(ns);else alert("没读到名字：请确保一行一个名字。");};
 r.readAsText(f,"utf-8");};
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
var __tg=document.createElement("button");__tg.textContent="🧹 清除演示";
__tg.style.cssText="position:fixed;right:14px;bottom:138px;z-index:9999;background:#F1E6CF;color:#5a3a18;font-weight:800;padding:9px 13px;border-radius:12px;cursor:pointer;font-size:13.5px;border:0;box-shadow:0 6px 18px rgba(0,0,0,.45)";
__tg.onclick=function(){
 var cur=__pp.value.trim();
 if(cur&&cur.indexOf("张三")<0){__pp.value=__N;var s1=document.getElementById("saveP");if(s1)s1.click();__L=__N.split("\\n");__tg.textContent="🧹 清除演示";__redraw();return;}
 if(cur){__pp.value="";var s2=document.getElementById("saveP");if(s2)s2.click();__tg.textContent="🔄 恢复虚拟演示";__redraw();}
 else{__pp.value=__N;var s3=document.getElementById("saveP");if(s3)s3.click();__L=__N.split("\\n");__tg.textContent="🧹 清除演示";__seed();__redraw();}};
document.body.appendChild(__tg);
}catch(e){}</scr''' + 'ipt>'

def rebuild(key):
    global s
    m = re.search(r'const %s="([^"]+)"' % key, s)
    b3 = base64.b64decode(m.group(1)).decode("utf-8")
    b3 = re.sub(r'<style id="xyInj">[\s\S]*?</style>', "", b3)
    b3 = re.sub(r'<script>try\{var __N=[\s\S]*?</script>', "", b3)
    assert "__genFace" not in b3 and "xyInj" not in b3
    b3 = b3.replace("</body>", INJ + "</body>")
    s = s[:m.start()] + 'const %s="' % key + base64.b64encode(b3.encode("utf-8")).decode() + '"' + s[m.end():]
rebuild("B3B64")
rebuild("B3XYL")

rep("v7.4 贴脸版", "v7.5 头像进圈版")

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.5 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
