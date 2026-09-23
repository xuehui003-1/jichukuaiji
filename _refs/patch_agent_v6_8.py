# -*- coding: utf-8 -*-
# v6.8 亮点版：①fab 放大(76→108px,帧图 96px) ②六帧状态动效库(待机挥手轮播+开助手欢呼+发消息抱包裹+回答完点赞+翻牌思考+进点名抱包裹+进消消乐欢呼+图谱通关欢呼+hover大笑)
# ③B3 两页 note 加"名单只存评委本地浏览器"说明 ④版本 v6.8
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 fab 加四帧(点赞C/思考D/抱包裹E/欢呼F) ═══
imgs = "".join('<img class="xybot xy%s" src="data:image/png;base64,%s" alt="">' % (f, base64.b64encode(open("_refs/xy/xyfab%s.png" % f, "rb").read()).decode()) for f in "CDEF")
m = re.search(r'<img class="xybot xyB" src="data:image/png;base64,[^"]+" alt="">', s)
assert m, "xyB 未找到"
s = s[:m.end()] + imgs + s[m.end():]

# ═══ 2 xyPose 函数 + 触发点 ═══
rep('function toggleAip(){const p=document.getElementById("aip");p.classList.toggle("on");',
    'function xyPose(f,ms){document.querySelectorAll(".fab .xybot").forEach(function(im){im.classList.remove("pose")});var el=document.querySelector(".fab .xy"+f);if(el){el.classList.add("pose");if(ms)setTimeout(function(){el.classList.remove("pose")},ms)}}\n'
    'function toggleAip(){const p=document.getElementById("aip");p.classList.toggle("on");\n'
    '  if(p.classList.contains("on"))setTimeout(function(){xyPose("F",1600)},80);')
rep('d.className="m "+t;d.innerHTML=txt;box.appendChild(d);box.scrollTop=box.scrollHeight;\n  if(t==="ai"){const vk=voiceForReply(txt);if(vk)sayVoice(vk)}',
    'd.className="m "+t;d.innerHTML=txt;box.appendChild(d);box.scrollTop=box.scrollHeight;\n  if(t==="me")xyPose("E",2000);else xyPose("C",1800);\n  if(t==="ai"){const vk=voiceForReply(txt);if(vk)sayVoice(vk)}')
rep(' if(TABNUDGE[t])fabNudge(TABNUDGE[t],"tab-"+t);',
    ' if(TABNUDGE[t])fabNudge(TABNUDGE[t],"tab-"+t);\n if(t==="roll")xyPose("E",1800);if(t==="xyl")xyPose("F",1800);if(t==="bot")xyPose("D",1600);')
rep('a.pick=i;shfSubmit()' if False else 'function shfFlip(i){const a=state.class.shf;if(a.done||a.pick!==-1&&a.pick!==undefined&&a.pick!==null&&a.pick>=0)return;a.pick=i;',
    'function shfFlip(i){const a=state.class.shf;if(a.done||a.pick!==-1&&a.pick!==undefined&&a.pick!==null&&a.pick>=0)return;a.pick=i;xyPose("D",1500);')
rep('+(n===STOPS.length?" 🎉 全图通关！":"")}',
    '+(n===STOPS.length?" 🎉 全图通关！":"");if(n===STOPS.length)xyPose("F",2200)}')

# ═══ 3 B3 名单本地说明 ═══
rep("开场用的「名字消消乐」在隔壁「🧹 名字消消乐」标签。",
    "开场用的「名字消消乐」在隔壁「🧹 名字消消乐」标签。名单只存在使用者自己的浏览器本地，公开页不携带任何真实姓名。")
rep("正是实录片段①里用的那套（见首页第四步）。",
    "正是实录片段①里用的那套（见首页第四步）。名单只存在使用者自己的浏览器本地，公开页不携带任何真实姓名。")

# ═══ 4 版本 ═══
rep('v6.7 灵动版', 'v6.8 亮点版')

# ═══ 5 CSS ═══
NEWCSS = '''
.fab{background:transparent;box-shadow:none;width:108px;height:108px;right:8px;bottom:8px}
.fab::after{left:50%;bottom:4px;width:52px;height:10px;margin-left:-26px}
.fab .xyA,.fab .xyB,.fab .xyC,.fab .xyD,.fab .xyE,.fab .xyF{inset:6px;width:96px;height:96px;opacity:0;object-fit:contain;object-position:center bottom;animation:xyFloat 2.8s ease-in-out infinite}
.fab .xyA{opacity:1}
.fab .xybot.pose{opacity:1 !important}
.fab .xyB{animation:xyFloat 2.8s ease-in-out infinite,xyWave 5.5s steps(1,end) infinite}
.fab:hover .xyA{opacity:0}
.fab:hover .xyB{opacity:1;animation:xyFloat 2.8s ease-in-out infinite}
.aip{bottom:130px}
#fabNudge{bottom:130px}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v6.8 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
