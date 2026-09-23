# -*- coding: utf-8 -*-
# v7.0 同心版：①fab 白圈根除(v6.6 遗留 inset 白描边覆盖为无) ②B3 两副本注入 v2：每次打开强制显示 20 虚拟名单+「📂 导入真实名单」按钮+提醒气泡
# ③外层说明同步 ④版本 v7.0
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

# ═══ 1 白圈根除 ═══
rep(".fab img.xybot{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;box-shadow:0 0 0 2.5px #fff inset}",
    ".fab img.xybot{object-fit:contain;display:block}")

# ═══ 2 B3 注入 v2 ═══
NAMES = ["张三","李四","王五","赵六","钱七","孙八","周九","吴十","郑十一","冯十二","陈十三","林十四","黄十五","徐十六","马十七","高十八","罗十九","梁二十","宋甲一","唐乙二"]
JSN = "\\n".join(NAMES)
INJ = ('<script>try{var __N="' + JSN + '";'
       'var __pp=document.getElementById("people");'
       'if(__pp){__pp.value=__N;var __sp=document.getElementById("saveP");if(__sp)__sp.click();}'
       'var __imp=document.createElement("label");'
       '__imp.innerHTML=\'📂 导入真实名单<input type="file" accept=".txt,.csv" style="display:none">\';'
       '__imp.style.cssText="position:fixed;right:14px;bottom:14px;z-index:9999;background:#e0b13a;color:#221a08;font-weight:800;padding:10px 14px;border-radius:12px;cursor:pointer;font-size:14px;box-shadow:0 6px 18px rgba(0,0,0,.45)";'
       '__imp.querySelector("input").onchange=function(e){var f=e.target.files[0];if(!f)return;var r=new FileReader();'
       'r.onload=function(){var ns=String(r.result).split(/\\r?\\n/).map(function(x){return x.trim()}).filter(Boolean);'
       'if(ns.length){__pp.value=ns.join("\\n");var sp=document.getElementById("saveP");if(sp)sp.click();alert("已导入 "+ns.length+" 人（只保存到本机浏览器）");}};'
       'r.readAsText(f,"utf-8");};'
       'document.body.appendChild(__imp);'
       'var __tip=document.createElement("div");'
       '__tip.innerHTML="<b>📄 当前是虚拟示例名单</b>（张三、李四…）——评奖演示随开随用；实际授课点右下角「导入真实名单」换成你的名单，只保存在本机浏览器。";'
       '__tip.style.cssText="position:fixed;right:14px;bottom:64px;z-index:9999;max-width:300px;background:rgba(13,20,38,.96);color:#ffe9a8;font-size:13px;line-height:1.6;padding:10px 13px;border-radius:12px;border:1px solid rgba(224,177,58,.55);box-shadow:0 8px 24px rgba(0,0,0,.4)";'
       'document.body.appendChild(__tip);'
       'setTimeout(function(){__tip.style.display="none"},15000);'
       '}catch(e){}</scr' + 'ipt>')

def rebuild(key):
    global s
    m = re.search(r'const %s="([^"]+)"' % key, s)
    b3 = base64.b64decode(m.group(1)).decode("utf-8")
    # 剥旧 __pp 注入（保留 __ck）
    b3 = re.sub(r'<script>try\{var __pp=[\s\S]*?</script>', '', b3)
    assert "__pp" not in b3
    b3 = b3.replace("</body>", INJ + "</body>")
    s = s[:m.start()] + 'const %s="' % key + base64.b64encode(b3.encode("utf-8")).decode() + '"' + s[m.end():]
rebuild("B3B64")
rebuild("B3XYL")

# ═══ 3 外层说明 ═══
rep("页内现显示的 20 个为虚拟示例名（张三、李四…），实际使用时清空重录即可。",
    "页内每次打开都自动显示 20 个虚拟示例名（张三、李四…，不读缓存）；实际授课点页面右下角「📂 导入真实名单」一键换成你的名单（只存本机浏览器）。", 2)

# ═══ 4 版本 ═══
rep('v6.9 声色版', 'v7.0 同心版')

# ═══ 5 CSS ═══
NEWCSS = '''
.fab img.xybot{box-shadow:none;border-radius:0}
'''
_i = s.rfind("</style>")
assert _i > 0
s = s[:_i] + NEWCSS + s[_i:]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v7.0 OK; %.2f MB" % (len(s.encode("utf-8")) / 1048576))
