# -*- coding: utf-8 -*-
# v5r2：语音规律统一(graph/lib 进门各播一次)+VOICE5(faqlib/xyintro 音频入库)+版本 v5.9
# 注意：插入位置必须用行尾锚(不要 find(";")——base64 的 data:audio/mp3;base64 里有分号！)
import base64, os, re
P = "参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s = open(P, encoding="utf-8").read()
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:70])
    s = s.replace(old, new)

rep('if(t==="gest")sayVoiceOnce("gintro","vg");if(t==="teach")sayVoiceOnce("tintro","vt");',
    'if(t==="gest")sayVoiceOnce("gintro","vg");if(t==="teach")sayVoiceOnce("tintro","vt");if(t==="graph")sayVoiceOnce("faqkg","vkg");if(t==="lib")sayVoiceOnce("faqlib","vlib");')
rep('v5.8 循序版', 'v5.9 实况版')

m = re.search(r"const VOICE4=\{[\s\S]*?Object\.assign\(VOICE,VOICE4\);", s)
assert m, "VOICE4 未找到"
V5 = ",".join('"%s":"data:audio/mp3;base64,%s"' % (k, b64("_refs/xy/%s.mp3" % k)) for k in ["faqlib", "xyintro"])
NEW = m.group(0) + "\nconst VOICE5={" + V5 + "};Object.assign(VOICE,VOICE5);"
s = s[:m.start()] + NEW + s[m.end():]

tmp = P + ".tmp"
open(tmp, "w", encoding="utf-8").write(s)
os.replace(tmp, P)
print("v5r2 OK")
