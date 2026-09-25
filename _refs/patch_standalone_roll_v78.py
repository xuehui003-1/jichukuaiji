# -*- coding: utf-8 -*-
# 独立工具 90-B3_抽人抽组_上场_v1.32 同步 v7.7/v7.8 口令——评委开源码包看到的与页面内嵌版一致：
# 标题「抽到后做什么」/三组分类(动口·亮纸笔·上台)/新增默认「回答问题」/去行话(亮记录册·小组亮凭证)/播报「到你啦」/盘心开始可点击
import io
P = "参赛_2026_AI赋能教学创新展示/90-B3_抽人抽组_上场_v1.32_20260905.html"
s = io.open(P, encoding="utf-8").read()
if 'data-u="answer"' in s:
    print("已应用过，跳过"); raise SystemExit
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, "count=%d != %d : %s" % (c, n, old[:60])
    s = s.replace(old, new)

rep('s0: "要改 0"\n  }\n};\nlet useId = "book"',
    's0: "要改 0"\n  },\n  answer: {\n    label: "回答问题", suggest: "draw1", tip: "",\n    say: "请起立，回答问题", sub: "起立口答，答对加分；答不出可以请同桌帮忙。",\n    s2: "答对 2", s5: "答得好 5", s0: "再想想 0"\n  }\n};\nlet useId = "answer"')
rep('label: "举册子", suggest: "draw3", tip: "",', 'label: "亮记录册", suggest: "draw3", tip: "",')
rep('say: "这三位，册子举起来", sub: "写了就行。不用站起来，不用开口。",',
    'say: "请把记录册举起来给大家看", sub: "举起来给大家看一眼就行，先不用开口。",')
rep('label: "看凭证", suggest: "drawG",', 'label: "小组亮凭证", suggest: "drawG",')
rep('say: "这组，把写好的通用记账凭证举起来",', 'say: "请你们组把写好的记账凭证举起来",')
rep('抽一个人上场。', '抽一个人上来。')
rep('<h3>上场做什么（点一个）</h3>', '<h3>抽到后做什么（点一个）</h3>')
old_speak = 'if(useId==="book") text=who+"。举册子。";\n  else if(useId==="tianping") text=who+"。上来玩天平。";\n  else if(useId==="lianxian") text=who+"。上来连线。";\n  else if(useId==="shuiguang") text=who+"。上来看水管。";\n  else if(useId==="shisuan") text=who+"。上来找漏账。";\n  else if(useId==="mole") text=who+"。上来打地鼠。";\n  else if(useId==="dub") text=who+"。上来配音。";\n  else if(useId==="nitpick") text=who+"。举凭证。";\n  else if(useId==="voucher") text=who+"。举记账凭证。";\n  else text=who+"。"+((USES[useId]&&USES[useId].goBtn)||"上场")+"。";'
new_speak = 'const call=one?"，到你啦。":"，到你们啦。";\n  if(useId==="answer") text=who+call+"请起立，回答问题。";\n  else if(useId==="book") text=who+call+"请把记录册举起来，给大家看一眼。";\n  else if(useId==="tianping") text=who+call+"上来玩天平。";\n  else if(useId==="lianxian") text=who+call+"上来连一连。";\n  else if(useId==="shuiguang") text=who+call+"上来看水流。";\n  else if(useId==="shisuan") text=who+call+"上来找漏账。";\n  else if(useId==="mole") text=who+call+"上来打地鼠。";\n  else if(useId==="dub") text=who+call+"来给这一段配音。";\n  else if(useId==="nitpick") text=who+call+"把交换来的凭证举起来，帮它找找茬。";\n  else if(useId==="voucher") text=who+call+"请你们组把写好的记账凭证举起来。";\n  else text=who+call+"请做好准备。";'
rep(old_speak, new_speak)
old_btns = '<div class="uses" id="uses">\n    <button type="button" data-u="book" class="on">举册子</button>\n    <button type="button" data-u="tianping">天平</button>\n    <button type="button" data-u="lianxian">连线</button>\n    <button type="button" data-u="shuiguang">水管</button>\n    <button type="button" data-u="shisuan">试算表</button>\n    <button type="button" data-u="mole">打地鼠</button>\n    <button type="button" data-u="dub">配音</button>\n    <button type="button" data-u="nitpick">找茬</button>\n    <button type="button" data-u="voucher">看凭证</button>\n  </div>'
new_btns = '<div class="uses" id="uses">\n    <span style="flex:1 1 100%;font-size:11px;font-weight:800;color:#8fb3e8;padding:1px 2px;text-align:left">动口 · 答与说</span>\n    <button type="button" data-u="answer" class="on">回答问题</button>\n    <button type="button" data-u="dub">配音</button>\n    <span style="flex:1 1 100%;font-size:11px;font-weight:800;color:#8fb3e8;padding:1px 2px;text-align:left">亮纸笔 · 查落实</span>\n    <button type="button" data-u="book">亮记录册</button>\n    <button type="button" data-u="nitpick">找茬</button>\n    <button type="button" data-u="voucher">小组亮凭证</button>\n    <span style="flex:1 1 100%;font-size:11px;font-weight:800;color:#8fb3e8;padding:1px 2px;text-align:left">上台 · 玩课件</span>\n    <button type="button" data-u="tianping">天平</button>\n    <button type="button" data-u="lianxian">连线</button>\n    <button type="button" data-u="shuiguang">水管</button>\n    <button type="button" data-u="shisuan">试算表</button>\n    <button type="button" data-u="mole">打地鼠</button>\n  </div>'
rep(old_btns, new_btns)
HUB = '''<script>try{var h=document.getElementById("hubTxt");if(h&&h.parentNode){var b=h.parentNode;
b.style.cursor="pointer";b.title="点击「开始」直接抽人";
b.onclick=function(){var d=document.getElementById("draw1");if(d&&!d.disabled)d.click()};
var n=document.createElement("div");n.textContent="👆 点转盘中间的「开始」即可抽人（左侧按钮同样可用）";
n.style.cssText="text-align:center;font-size:12.5px;font-weight:800;color:#8a5a12;background:rgba(255,236,180,.8);border:1px solid #e0c27a;border-radius:999px;padding:4px 12px;margin:8px auto 0;max-width:300px";
b.parentNode.parentNode.insertBefore(n,b.parentNode.nextSibling)}}catch(e){}</script>
</body>'''
assert s.count("</body>") == 1
s = s.replace("</body>", HUB)
io.open(P, "w", encoding="utf-8").write(s)
print("standalone roll v7.8-aligned OK")
