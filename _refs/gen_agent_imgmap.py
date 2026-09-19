#!/usr/bin/env python3
"""参赛智能体·课件真页图片库生成器：扫描全部课件引用图→压缩→base64→/tmp/imgmap.json"""
from PIL import Image
import base64,io,json,os,re
RPA=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"RPA")
DECKS=["04_项目一_第1讲_开学第一课_课件_v2.1_20260906.html",
"08_项目二_第1-3讲_变量命令流程_纸上篇_课件_v1.4_参赛融合版_20260918.html",
"10_项目二_第4讲_机器人上岗_课件_v1.2_20260906.html",
"14_项目三_第1讲_图纸搬家_课件_v1.0_20260908.html",
"16_项目三_第2讲_循环_课件_v1.0_20260908.html",
"17_项目三_第3讲_判断加循环_课件_参赛精修版_v1.0_20260916.html"]
refs=set()
for f in DECKS:
    s=open(os.path.join(RPA,f),encoding="utf-8").read()
    refs.update(re.findall(r'(img/[A-Za-z0-9_./-]+[.](?:png|jpe?g))',s))
out={}
for r in sorted(refs):
    p=os.path.join(RPA,r)
    if not os.path.exists(p):
        print("缺图!",r);continue
    im=Image.open(p).convert("RGB")
    w,h=im.size
    if w>640:im=im.resize((640,int(h*640/w)),Image.LANCZOS)
    buf=io.BytesIO();im.save(buf,"JPEG",quality=72,optimize=True)
    out[os.path.basename(r).rsplit(".",1)[0]]="data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()
json.dump(out,open("/tmp/imgmap.json","w"))
print("图库:",len(out),"张, 总",sum(len(v) for v in out.values())//1024,"KB")
