#!/usr/bin/env python3
"""v5g：手势真人示范4连视频；fab瘦长+红点放大；10句语音接线(时刻+回复自动配音)；分析邀请新分支"""
import base64
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d: %r"%(c,old[:60]))
    s=s.replace(old,new)
def b64(f,mime):
    return "data:%s;base64,"%(mime,)+base64.b64encode(open("_refs/"+f,"rb").read()).decode()

# ── 1 视频：手势页真人示范 2×2 ──
LAB=[("☝","选项一"),("✌","选项二"),("👍","是 · 对"),("✊","否 · 不对")]
cells=[]
for i,(ic,lab) in enumerate(LAB,1):
    cells.append('<figure><video src="%s" poster="%s" controls muted loop playsinline preload="none"></video><figcaption>%s %s</figcaption></figure>'%(
        b64("g%d.mp4"%i,"video/mp4"),b64("g%d.jpg"%i,"image/jpeg"),ic,lab))
DEMO='<div class="gdemo"><div class="gdt">🙌 真人手势示范（点一下播放）</div><div class="gv">%s</div></div>'%("".join(cells))
rep('<div class="note">没有摄像头？直接点左边题目下的大按钮，效果一样。</div>',
    '<div class="note">没有摄像头？直接点左边题目下的大按钮，效果一样。</div>'+DEMO)

# ── 2 fab 瘦长 + 红点放大 + 气泡挪位 ──
rep('.fab{position:fixed;right:18px;bottom:18px;overflow:visible;z-index:60;width:60px;height:60px;border-radius:50%;',
    '.fab{position:fixed;right:20px;bottom:20px;z-index:60;width:48px;height:104px;border-radius:26px;')
rep('#fabDot{position:absolute;top:-3px;right:-3px;min-width:20px;height:20px;',
    '#fabDot{position:absolute;top:-6px;right:-6px;min-width:27px;height:27px;')
rep('font-size:12px;font-style:normal;display:flex;align-items:center;justify-content:center;padding:0 5px;border:2px solid #fff;z-index:70}',
    'font-size:14px;font-style:normal;font-weight:800;display:flex;align-items:center;justify-content:center;padding:0 6px;border:2.5px solid #fff;z-index:70;box-shadow:0 2px 8px rgba(160,40,20,.45)}')
rep('#fabNudge{position:fixed;right:88px;bottom:104px;','#fabNudge{position:fixed;right:82px;bottom:136px;}#fabNudgeX{position:fixed;')
# CSS 新增
rep('.vdesc{color:#6b5d52;font-size:.92em}',
'''.vdesc{color:#6b5d52;font-size:.92em}
.gdemo{margin-top:10px}
.gdt{font-weight:800;font-size:14px;margin-bottom:6px;color:#4a2c1e}
.gv{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.gv figure{margin:0}
.gv video{width:100%;aspect-ratio:9/14;object-fit:cover;border-radius:10px;background:#000;display:block}
.gv figcaption{text-align:center;font-size:12.5px;margin-top:3px;color:#6b5d52;font-weight:700}''')

# ── 3 语音接线 ──
V={k:b64("xy_%s.mp3"%k,"audio/mpeg") for k in ["pvall","shf","botrun","gintro","tintro","faqgest","faqtank","faqxh","faqfx","fallback"]}
rep('function sayVoice(k){try{new Audio(VOICE[k]).play()}catch(e){}}',
'''const VOICE2={pvall:"%(pvall)s",shf:"%(shf)s",botrun:"%(botrun)s",gintro:"%(gintro)s",tintro:"%(tintro)s",faqgest:"%(faqgest)s",faqtank:"%(faqtank)s",faqxh:"%(faqxh)s",faqfx:"%(faqfx)s",fallback:"%(fallback)s"};Object.assign(VOICE,VOICE2);
const RVOICE=[["「手势闯关」四种手势","faqgest"],["去「机器人车间」选「存钱罐","faqtank"],["学号是编号不是数量","faqxh"],["把那件事用「分析：」","faqfx"],["这个问题我卡壳了","fallback"],["我是小邮，财务机器人课堂的伴学智能体","hello"],["我在「机器人车间」陪跑了一台","botrun"],["你刚在首页判断了","shf"]];
function voiceForReply(t){if(!t)return null;t=String(t).replace(/<[^>]*>/g,"");for(const p of RVOICE)if(t.includes(p[0]))return p[1];return null}
function sayVoice(k){try{new Audio(VOICE[k]).play()}catch(e){}}
function sayVoiceOnce(k,f){if(f&&globalThis[f])return;globalThis[f]=1;sayVoice(k)}'''%V)
# 回复自动配音
rep('box.appendChild(d);box.scrollTop=box.scrollHeight;',
    'box.appendChild(d);box.scrollTop=box.scrollHeight;\n  if(t==="ai"){const vk=voiceForReply(txt);if(vk)sayVoice(vk)}')
# 消名时刻
rep('sfx("done");fabNudge("全对，名字可以消了——「完成了才消」，课堂就是这么点名的","pvdone");',
    'sfx("done");sayVoiceOnce("pvall","vpv");fabNudge("全对，名字可以消了——「完成了才消」，课堂就是这么点名的","pvdone");')
# 进手势/教师台时刻
rep('if(TABNUDGE[t])fabNudge(TABNUDGE[t],"tab-"+t);',
    'if(TABNUDGE[t])fabNudge(TABNUDGE[t],"tab-"+t);\n if(t==="gest")sayVoiceOnce("gintro","vg");if(t==="teach")sayVoiceOnce("tintro","vt");')
# 分析邀请新分支
rep('if(/为什么.*(结果|圈|元|剩)/.test(q)',
    'if(has("分析","找茬","帮我查"))return "把那件事用「分析：」开头发给我——比如「分析：打车去吃饭一共58元记餐饮」。我用 8 类错误标签帮你拆，但<b>不直接给答案</b>：自己改对了才算真的会。";\n  if(/为什么.*(结果|圈|元|剩)/.test(q)')

open(P,"w",encoding="utf-8").write(s)
import os
print("v5g OK；文件大小 %.2f MB"%(os.path.getsize(P)/1048576))
