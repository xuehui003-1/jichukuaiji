# -*- coding: utf-8 -*-
# v6.9 声色版：①语音第一批10句换 voice-01 音色(旧base64随之删除) ②B3两副本注入20个虚拟示例名单(张三李四式,评委可玩)
# ③fab 放大120px+AI呼吸光环(旋转conic渐变描边+呼吸波) ④新增G介绍/H惊讶/I提示/J胜利4帧+触发(课件馆展厅介绍/数据展开惊讶/提示气泡眨眼/手势闯关胜利)
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 语音换声（10句） ═══
VO = ["hello","gintro","tintro","faqkg","faqlib","shf","done","botrun","fallback","pvall"]
for k in VO:
    b = base64.b64encode(open("_refs/xy/%s.mp3" % k, "rb").read()).decode()
    pat = re.compile(r'("?%s"?\s*:\s*")data:audio/[a-z0-9]+;base64,[A-Za-z0-9+/=]+"' % k)
    m = pat.search(s)
    assert m, "voice key 未命中: " + k
    s = s[:m.start()] + m.group(1) + "data:audio/mpeg;base64," + b + '"' + s[m.end():]
print("语音10句已换声")

# ═══ 2 B3 虚拟名单（重建 B3B64 → 派生 B3XYL） ═══
m2 = re.search(r'const B3B64="([^"]+)"', s)
b3 = base64.b64decode(m2.group(1)).decode("utf-8")
assert "虚拟示例名单" not in b3
NAMES = "张三\n李四\n王五\n赵六\n钱七\n孙八\n周九\n吴十\n郑十一\n冯十二\n陈十三\n林十四\n黄十五\n徐十六\n马十七\n高十八\n罗十九\n梁二十\n宋甲一\n唐乙二"
inject = ('<script>try{var __pp=document.getElementById("people");'
          'if(__pp&&!__pp.value.trim()){__pp.value="' + NAMES.replace("\n", "\\n") + '";}}catch(e){}</scr' + "ipt>")
assert b3.count("</body>") == 1
b3new = b3.replace("</body>", inject + "</body>")
s = s[:m2.start()] + 'const B3B64="' + base64.b64encode(b3new.encode("utf-8")).decode() + '"' + s[m2.end():]
# 派生 B3XYL
b3x = b3new.replace("<h2>下课前\u3000检查册子</h2>", "<h2>完成任务后举手，老师消名字</h2>")
inject2 = ('<script>try{var __ck=document.getElementById("checkout");if(__ck){__ck.classList.add("on");'
           'if(window.renderCheckout)renderCheckout();}}catch(e){}</scr' + "ipt>")
assert b3x.count("</body>") == 1
b3x = b3x.replace("</body>", inject2 + "</body>")
m3 = re.search(r'const B3XYL="([^"]+)"', s)
s = s[:m3.start()] + 'const B3XYL="' + base64.b64encode(b3x.encode("utf-8")).decode() + '"' + s[m3.end():]
# 外层 note 补句
rep("开场用的「名字消消乐」在隔壁「🧹 名字消消乐」标签。名单只存在使用者自己的浏览器本地，公开页不携带任何真实姓名。",
    "开场用的「名字消消乐」在隔壁「🧹 名字消消乐」标签。名单只存在使用者自己的浏览器本地，公开页不携带真实姓名——页内现显示的 20 个为虚拟示例名（张三、李四…），实际使用时清空重录即可。")
rep("正是实录片段①里用的那套（见首页第四步）。名单只存在使用者自己的浏览器本地，公开页不携带任何真实姓名。",
    "正是实录片段①里用的那套（见首页第四步）。名单只存在使用者自己的浏览器本地，公开页不携带真实姓名——页内现显示的 20 个为虚拟示例名（张三、李四…），实际使用时清空重录即可。")

# ═══ 3 fab 呼吸光环 + 放大 + 四新帧 ═══
imgs = "".join('<img class="xybot xy%s" src="data:image/png;base64,%s" alt="">' % (f, base64.b64encode(open("_refs/xy/xyfab%s.png" % f, "rb").read()).decode()) for f in "GHIJ")
m4 = re.search(r'<img class="xybot xyF" src="data:image/png;base64,[^"]+" alt="">', s)
assert m4, "xyF 未找到"
s = s[:m4.end()] + imgs + s[m4.end():]
rep('function statOpen(){const p=document.getElementById("statPeek");if(p)p.classList.add("open");}',
    'function statOpen(){const p=document.getElementById("statPeek");if(p)p.classList.add("open");xyPose("H",1800);}')
rep('  b.classList.add("on");clearTimeout(fabNudgeTimer);',
    '  b.classList.add("on");xyPose("I",1500);clearTimeout(fabNudgeTimer);')
rep('if(t==="gest")renderGest();',
    'if(t==="gest"){renderGest();xyPose("J",1800)}if(t==="lib"||t==="hall")xyPose("G",1800);')

# ═══ 4 版本 ═══
rep('v6.8 亮点版', 'v6.9 声色版')

# ═══ 5 CSS ═══
NEWCSS = '''
@property --xya{syntax:"<angle>";inherits:false;initial-value:0deg}
.fab{width:120px;height:120px;right:6px;bottom:6px;animation:xyBreath 2.4s ease-in-out infinite}
.fab::before{content:"";position:absolute;inset:-7px;border-radius:50%;padding:3px;background:conic-gradient(from var(--xya),#F59F23,#81D4FA,#E8590C,#81D4FA,#F59F23);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);mask-composite:exclude;animation:xySpin 3.6s linear infinite;filter:drop-shadow(0 0 7px rgba(245,159,35,.6));z-index:1;pointer-events:none}
@keyframes xySpin{to{--xya:360deg}}
@keyframes xyBreath{0%,100%{filter:drop-shadow(0 0 2px rgba(245,159,35,.25))}50%{filter:drop-shadow(0 0 12px rgba(245,159,35,.55))}}
.fab .xyA,.fab .xyB,.fab .xyC,.fab .xyD,.fab .xyE,.fab .xyF,.fab .xyG,.fab .xyH,.fab .xyI,.fab .xyJ{inset:6px;width:108px;height:108px}
.fab .xybot{z-index:2}
.aip{bottom:142px}
#fabNudge{bottom:142px}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v6.9 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
