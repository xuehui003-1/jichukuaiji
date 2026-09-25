# -*- coding: utf-8 -*-
# v7.9 占位点播版：①五张「📺 真实课堂实证」点播占位卡装进页——点击即播(外链就绪后),未就绪点击提示"视频制作中"；
#   V1=课堂点名页顶 / V2=课堂同步页顶 / V3=知识图谱页顶 / V6=课件馆页顶 / V7=首页第五步数据看板卡内(V4=替换小邮亮相弹窗视频)
#   布局先定→再截图→再做视频→外链回填,不进循环；外链不占页面体积
# ②手势闯关"真人手势示范"内嵌视频(4 段 data:video)原本无 controls 点不动(须走⋮菜单)——加▶悬浮播放按钮+点击切换播放/暂停
# ③版本 v7.9
import os
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

SCRIPT = '''<script id="xyV79">
(function(){
var CSS=document.createElement("style");
CSS.textContent=".xyVidPill{display:flex;align-items:center;gap:8px;width:calc(100% - 16px);max-width:760px;margin:2px auto 10px;padding:9px 14px;background:linear-gradient(90deg,#101b36,#1a2744);color:#ffe9a8;border:1px solid rgba(224,177,58,.5);border-radius:999px;cursor:pointer;font-size:13px;box-shadow:0 4px 14px rgba(0,0,0,.35);text-align:left}"
+".xyVidPill b{font-weight:800}"
+".xyVidPill i{margin-left:auto;font-style:normal;font-size:12px;background:#e0b13a;color:#221a08;font-weight:800;padding:3px 10px;border-radius:999px;white-space:nowrap}"
+".xyVidPill.wait i{background:#5a6b8f;color:#fff}"
+".xyGvWrap{position:relative;display:block}"
+".xyGvPlay{position:absolute;left:0;top:0;right:0;bottom:0;display:flex;align-items:center;justify-content:center;cursor:pointer;background:rgba(10,16,34,.28);border-radius:10px}"
+".xyGvPlay span{width:52px;height:52px;border-radius:50%;background:rgba(224,177,58,.95);color:#221a08;font-size:24px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(0,0,0,.45)}";
document.head.appendChild(CSS);
window.XYVIDEO_URLS={V1:"",V2:"",V3:"",V6:"",V7:""};
var TITLES={V1:"真实课堂实证 · 消名与点名",V2:"真实课堂实证 · 任务与记录册",V3:"真实课堂实证 · 图谱与数据",V6:"真实课堂实证 · 实录重新组装",V7:"真实成果 · 从原始表到课堂"};
function pill(k){var b=document.createElement("button");b.type="button";b.className="xyVidPill";b.setAttribute("data-vid",k);
 b.innerHTML="📺 <b>"+TITLES[k]+"</b><i>点击观看</i>";
 b.onclick=function(){var u=(window.XYVIDEO_URLS||{})[k];
  if(!u){b.classList.add("wait");b.querySelector("i").textContent="视频制作中 · 外链就绪后一键替换";
   setTimeout(function(){b.classList.remove("wait");b.querySelector("i").textContent="点击观看";},2400);return;}
  var v=document.createElement("video");v.controls=true;v.setAttribute("playsinline","");v.preload="metadata";
  v.src=u;v.style.cssText="width:100%;max-width:760px;display:block;margin:2px auto 10px;aspect-ratio:16/9;background:#000;border-radius:12px";
  b.replaceWith(v);var pr=v.play();if(pr&&pr.catch)pr.catch(function(){});};
 return b;}
[["V1","tab-roll",0],["V2","tab-class",0],["V3","tab-graph",0],["V6","tab-lib",0],["V7","secData",1]].forEach(function(it){
 var k=it[0],host=document.getElementById(it[1]);if(!host||host.querySelector('[data-vid="'+k+'"]'))return;
 var p=pill(k);
 if(it[2]){host.appendChild(p);}else{host.insertBefore(p,host.querySelector(".card"));}
});
document.querySelectorAll(".gv video").forEach(function(v){
 if(v.parentNode&&v.parentNode.className==="xyGvWrap")return;
 v.removeAttribute("controls");
 v.setAttribute("playsinline","");v.setAttribute("preload","metadata");
 var w=document.createElement("span");w.className="xyGvWrap";
 v.parentNode.insertBefore(w,v);w.appendChild(v);
 var o=document.createElement("div");o.className="xyGvPlay";o.innerHTML="<span>\\u25B6</span>";
 w.appendChild(o);
 var show=function(){o.style.display="flex";};
 v.addEventListener("play",function(){o.style.display="none";});
 v.addEventListener("pause",show);v.addEventListener("ended",show);
 function go(e){e.preventDefault();e.stopPropagation();
  if(v.paused){var pr=v.play();if(pr&&pr.catch)pr.catch(function(){});}else{v.pause();}}
 o.addEventListener("click",go);v.addEventListener("click",go);
});
})();
</script>'''

assert 'id="xyV79"' not in s
rep("v7.8 到你啦版", "v7.9 占位点播版")
assert s.count("</body>") == 1
s = s.replace("</body>", SCRIPT + "</body>")

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.9 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
