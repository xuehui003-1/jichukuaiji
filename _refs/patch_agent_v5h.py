#!/usr/bin/env python3
"""v5h：修气泡(透明/关不掉根因=上轮选择器切错)；对话面板瘦长320x600；fab换动态SVG小邮(浮动+眨眼+天线脉冲+气泡时跳跃)；地图条浅色重做；AQUICK加语音演示"""
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)

rep('#fabNudge{position:fixed;right:82px;bottom:136px;}#fabNudgeX{position:fixed;max-width:280px;background:#fff;',
    '#fabNudge{position:fixed;right:82px;bottom:136px;max-width:280px;background:#fff;')
rep('width:min(370px,calc(100vw - 32px));height:min(490px,70vh);',
    'width:min(320px,calc(100vw - 32px));height:min(600px,78vh);')
rep('<button class="fab" onclick="toggleAip()" title="小邮伴学助手">🤖<i id="fabDot" style="display:none"></i></button>',
'''<button class="fab" onclick="toggleAip()" title="小邮伴学助手">
<svg class="xybot" viewBox="0 0 48 104" aria-hidden="true">
  <line x1="24" y1="12" x2="24" y2="22" stroke="#FFE082" stroke-width="3"/>
  <circle class="xantb" cx="24" cy="9" r="4.2" fill="#FFE082"/>
  <rect x="6" y="22" width="36" height="30" rx="10" fill="#F59F23"/>
  <rect x="11" y="28" width="26" height="17" rx="7" fill="#3B2B20"/>
  <rect class="xeyeL" x="17" y="33" width="4.6" height="6.2" rx="2.3" fill="#81D4FA"/>
  <rect class="xeyeR" x="26.4" y="33" width="4.6" height="6.2" rx="2.3" fill="#81D4FA"/>
  <rect x="13" y="56" width="22" height="8" rx="4" fill="#FFE082"/>
  <rect x="19" y="64" width="10" height="16" rx="5" fill="#FFE082"/>
  <circle cx="24" cy="84" r="7" fill="#BF360C"/>
  <rect x="10" y="93" width="28" height="6" rx="3" fill="#FFE082" opacity=".85"/>
</svg>
<i id="fabDot" style="display:none"></i></button>''')
rep('.gv figcaption{text-align:center;font-size:12.5px;margin-top:3px;color:#6b5d52;font-weight:700}',
'''.gv figcaption{text-align:center;font-size:12.5px;margin-top:3px;color:#6b5d52;font-weight:700}
.fab svg.xybot{width:100%;height:100%;display:block;animation:xbob 3.4s ease-in-out infinite}
.xantb{animation:xping 2.2s ease-in-out infinite;transform-origin:center}
.xeyeL,.xeyeR{animation:xblink 4.4s infinite;transform-origin:center;transform-box:fill-box}
.fab.nudge svg.xybot{animation:xjump .8s ease}
@keyframes xbob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
@keyframes xblink{0%,91%,100%{transform:scaleY(1)}94%{transform:scaleY(.12)}97%{transform:scaleY(1)}}
@keyframes xping{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes xjump{0%{transform:translateY(0)}30%{transform:translateY(-12px)}60%{transform:translateY(0)}78%{transform:translateY(-5px)}100%{transform:translateY(0)}}''')
rep('''.mapBar{background:linear-gradient(135deg,#7A1B23,#A63A32);border-radius:18px;padding:16px 20px;color:#fff;margin:0 0 14px;box-shadow:0 6px 18px rgba(90,20,20,.16)}
.mapBar .mt{font-weight:800;margin-bottom:10px;font-size:15.5px;letter-spacing:.5px}
.mrow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:9px 0}
.mrole{flex:0 0 96px;text-align:center;border-radius:999px;padding:5px 0;font-size:12.5px;font-weight:800;letter-spacing:1px;border:1px solid rgba(255,255,255,.5)}
.mrole.s1{background:rgba(255,224,130,.28)}.mrole.s2{background:rgba(129,212,250,.24)}.mrole.t1{background:rgba(255,255,255,.26)}
.mg{background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.5);color:#fff;border-radius:12px;padding:8px 14px;font-size:14.5px;font-weight:700;cursor:pointer;text-align:left;line-height:1.35;transition:.15s}
.mg:hover{background:rgba(255,255,255,.26);transform:translateY(-1px)}
.mg em{font-style:normal;font-weight:400;font-size:12.5px;color:rgba(255,255,255,.85);display:block}
.mrow>i{color:rgba(255,255,255,.75);font-style:normal;font-weight:800}
.mchip{border:1.4px dashed rgba(255,255,255,.75);color:#fff;border-radius:999px;padding:8px 14px;font-size:13.5px;font-weight:700}''',
'''.mapBar{background:#FFFBF4;border:1.5px solid #EADBC5;border-radius:20px;padding:15px 20px;margin:0 0 14px;box-shadow:0 3px 14px rgba(150,100,40,.08)}
.mapBar .mt{font-weight:800;margin-bottom:10px;font-size:15.5px;color:#8C5A1E}
.mrow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:9px 0}
.mrole{flex:0 0 96px;text-align:center;border-radius:999px;padding:5px 0;font-size:12.5px;font-weight:800;letter-spacing:1px}
.mrole.s1{background:#FBEDEA;color:#8C1F28}.mrole.s2{background:#E9F2E9;color:#2E6B2E}.mrole.t1{background:#FDF3E0;color:#8C5A1E}
.mg{background:#fff;border:1.5px solid #E7D8C2;color:#4a2c1e;border-radius:13px;padding:8px 14px;font-size:14.5px;font-weight:700;cursor:pointer;text-align:left;line-height:1.35;transition:.15s;box-shadow:0 1px 5px rgba(150,100,40,.08)}
.mg:hover{border-color:#B5433A;transform:translateY(-2px);box-shadow:0 5px 14px rgba(140,31,40,.14)}
.mg em{font-style:normal;font-weight:400;font-size:12.5px;color:#8a7a6a;display:block}
.mrow>i{color:#C9A87E;font-style:normal;font-weight:800}
.mchip{border:1.6px dashed #D8A64A;color:#8C5A1E;background:#FFF7E6;border-radius:999px;padding:8px 14px;font-size:13.5px;font-weight:700}''')
rep('b.classList.add("on");clearTimeout(fabNudgeTimer);fabNudgeTimer=setTimeout(fabHide,9000);}',
    'b.classList.add("on");clearTimeout(fabNudgeTimer);fabNudgeTimer=setTimeout(fabHide,9000);\n  const fb=document.querySelector(".fab");if(fb){fb.classList.add("nudge");setTimeout(()=>fb.classList.remove("nudge"),900)}}')
rep('const AQUICK=["怎么用手答题？",','const AQUICK=["小邮，开口说一句","怎么用手答题？",')
rep('  if(has("怎么用手答","手答题","怎么答","没有摄像头","没摄像头"))',
'''  if(has("开口","说一句","听听","声音","语音")){sayVoice("hello");return "听到没？这就是我的声音 😎 十二句台词都是我说的，回复里能对上台词的也会开口。";}
  if(has("怎么用手答","手答题","怎么答","没有摄像头","没摄像头"))''')
open(P,"w",encoding="utf-8").write(s)
import os
print("v5h OK; %.2f MB"%(os.path.getsize(P)/1048576))
