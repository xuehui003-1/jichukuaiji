#!/usr/bin/env python3
import base64
P="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html"
s=open(P,encoding="utf-8").read()
def b64(f):return "data:audio/mpeg;base64,"+base64.b64encode(open("_refs/"+f,"rb").read()).decode()
hello,done=b64("xy_hello.mp3"),b64("xy_done.mp3")
def rep(old,new):
    global s
    c=s.count(old);assert c==1,("count=%d"%c,old[:50])
    s=s.replace(old,new)
rep('function botSay(txt){return amsg("ai",txt)}',
    'function botSay(txt){return amsg("ai",txt)}\nconst VOICE={hello:"'+hello+'",done:"'+done+'"};\nfunction sayVoice(k){try{new Audio(VOICE[k]).play()}catch(e){}}')
rep('aOpened=true;\n','aOpened=true;\n    sayVoice("hello");\n')
rep('amsg("ai",`我是小邮 🤖 <b>什么时候找我：</b>',
    'amsg("ai",`🔊 <button class="btn o" style="padding:1px 8px" onclick="sayVoice(\'hello\')">▶ 再听一遍</button> 我是小邮，刚才那段就是我的声音。<br><b>什么时候找我：</b>')
rep('    sfx("done");fabNudge("五关全过！把「为什么」讲给同桌听——讲明白才算真会","gdone");',
    '    sfx("done");sayVoice("done");fabNudge("五关全过！把「为什么」讲给同桌听——讲明白才算真会","gdone");')
open(P,"w",encoding="utf-8").write(s)
print("语音嵌入 OK，新增",(len(hello)+len(done))//1024,"KB")
