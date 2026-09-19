/* 参赛智能体 v5.0 手术脚本：全课件入住＋全站协调改版。产物=唯一源，就地升级。 */
const fs=require("fs");
const R="/home/user/jichukuaiji/";
const SRC="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学五环智能体_v4.0_20260918.html";
const DST="参赛_2026_AI赋能教学创新展示/01_核心作品_小邮伴学课堂智能体_v5.0_20260918.html";
const IMG=JSON.parse(fs.readFileSync("/tmp/imgmap.json","utf8"));
let A=fs.readFileSync(R+SRC,"utf8");

/* ── 读课件 ── */
const DECKS={
 "04":{f:"RPA/04_项目一_第1讲_开学第一课_课件_v2.1_20260906.html",name:"04 开学第一课",scope:"lib04"},
 "08":{f:"RPA/08_项目二_第1-3讲_变量命令流程_纸上篇_课件_v1.4_参赛融合版_20260918.html",name:"08 纸上篇·变量命令流程",scope:"dk08"},
 "10":{f:"RPA/10_项目二_第4讲_机器人上岗_课件_v1.2_20260906.html",name:"10 机器人上岗",scope:"lib10"},
 "14":{f:"RPA/14_项目三_第1讲_图纸搬家_课件_v1.0_20260908.html",name:"14 图纸搬家",scope:"lib14"},
 "16":{f:"RPA/16_项目三_第2讲_循环_课件_v1.0_20260908.html",name:"16 循环",scope:"lib16"},
 "17":{f:"RPA/17_项目三_第3讲_判断加循环_课件_参赛精修版_v1.0_20260916.html",name:"17 判断＋循环·精修",scope:"dk17"}};
function slidesOf(s){const a=s.indexOf("const SLIDES"),b=s.indexOf("\n];",a);return eval(s.slice(a,b+3).replace("const SLIDES =",""))}
function deckCssOf(s){return [...s.matchAll(/<style>([\s\S]*?)<\/style>/g)].map(x=>x[1]).join("\n")}
function scopeCss(css,sc){
  css=css.replace(/\/\*[\s\S]*?\*\//g,"");
  let res="",i=0;const n=css.length;
  while(i<n){const b=css.indexOf("{",i);if(b<0){res+=css.slice(i);break}
    const sel=css.slice(i,b).trim();let d=1,j=b+1;
    while(j<n&&d>0){if(css[j]==="{")d++;else if(css[j]==="}")d--;j++}
    const body=css.slice(b+1,j-1);
    if(sel.startsWith("@media")||sel.startsWith("@supports"))res+=sel+"{"+scopeCss(body,sc)+"}";
    else if(sel.startsWith("@"))res+=sel+"{"+body+"}";
    else res+=sel.split(",").map(s0=>{s0=s0.trim();
      if(/^(:root|html|body)$/i.test(s0))return sc;
      if(s0==="*")return sc+" *";return sc+" "+s0;}).join(",")+"{"+body+"}";
    i=j;}
  return res;
}
function fixImg(h){return h.replace(/img\/[A-Za-z0-9_./-]+\.(?:png|jpe?g)/g,(m)=>{
  const key=m.split("/").pop().replace(/\.(png|jpg|jpeg)$/i,"");
  if(!IMG[key])throw new Error("缺图映射:"+m);
  return IMG[key];})}
function label(h,fallback){
  let m=h.match(/class="eyebrow"[^>]*>([^<]{1,60})</);
  if(!m)m=h.match(/<h1>([^<]{1,60})</);
  let t=m?m[1].replace(/\s+/g," ").trim():fallback;
  t=t.replace(/^⏸\s*/,"⏸");
  return t.length>15?t.slice(0,14)+"…":t;}

/* 旧产物 DKP 提取：只取 L08-26 的 PV 注入尾段（纯字符串，免 eval） */
function oldTail(){const k='"L08-26":';const a0=A.indexOf(k);if(a0<0)return"";
  const b0=A.indexOf(',"L08-27":',a0);if(b0<0)return"";
  const seg=A.slice(a0,b0);const ci=seg.indexOf('border-top:1.5px dashed');if(ci<0)return"";
  const di=seg.lastIndexOf('<div',ci);return seg.slice(di).replace(/},?$/,"");}
globalThis.OLDTAIL=oldTail();
const DKP={};const LIB={};
for(const [id,cfg] of Object.entries(DECKS)){
  const raw=fs.readFileSync(R+cfg.f,"utf8");
  const S=slidesOf(raw);
  const rail=[];
  if(id==="17"){
    /* 17 用它自己的 render 引擎 */
    const blocks=[...raw.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x=>x[1]);
    const main=blocks.sort((a,b)=>b.length-a.length)[0];
    function el(){return{innerHTML:"",className:"",style:{setProperty(){},zoom:""},value:"",classList:{add(){},remove(){},toggle(){}},
      addEventListener(){},removeEventListener(){},appendChild(){},querySelector:()=>el(),querySelectorAll:()=>[],
      getBoundingClientRect:()=>({width:800,height:500,top:0,left:0}),clientHeight:500}}
    const cardEl=el();
    const oldDoc=global.document;
    global.document={getElementById:(x)=>x==="card"?cardEl:el(),querySelectorAll:()=>[],querySelector:()=>el(),
      addEventListener(){},removeEventListener(){},createElement:()=>el(),body:el(),documentElement:el()};
    global.window={addEventListener(){},innerWidth:1280,innerHeight:800,location:{hash:""}};
    global.history={replaceState(){}};global.location={hash:""};
    global.localStorage={getItem:()=>null,setItem(){},removeItem(){}};
    const _st=global.setTimeout;global.setTimeout=()=>0;
    eval(main+`\n;globalThis.__D={render,setI:(v)=>{ i = v }};`);
    const D=globalThis.__D;
    S.forEach((s,i)=>{D.setI(i);D.render();
      const key=id+"-"+(i+1);
      DKP[key]={scope:"dk17",html:'<div class="'+(cardEl.className||"card")+'">'+fixImg(cardEl.innerHTML)+"</div>"};
      rail.push([key,(s.n||i+1)+" "+(s.title||"").slice(0,12)]);});
    global.setTimeout=_st;
    global.document=oldDoc;
  }else{
    S.forEach((s,i)=>{
      let h=s.html||"";
      if(id==="08"&&i===25){
        const c=h.indexOf('<div style="margin-top:12px;padding-top:8px;border-top:1.5px dashed');if(c>0)h=h.slice(0,c);
        h=h.replace(/（字符）/g,"（类型?你来选）").replace(/（数值）/g,"（类型?你来选）").replace(/＝「是」\/「否」/,"＝眼镜戴不戴");
        if(OLDTAIL)h+=OLDTAIL;}
      const key=id+"-"+(i+1);
      DKP[key]={scope:cfg.scope,html:fixImg(h)};
      rail.push([key,(i+1)+" "+label(h,"第"+(i+1)+"页")]);});
    if(id!=="08")LIB["css_"+id]=scopeCss(deckCssOf(raw),cfg.scope);
  }
  LIB["rail_"+id]=rail;
}
/* 用全量 DKP 替换产物旧定义 */
{const a0=A.indexOf("const DKP={");let d=0,b0=a0+9;
 for(;b0<A.length;b0++){if(A[b0]==="{")d++;else if(A[b0]==="}"){d--;if(d===0){b0++;break}}}
 A=A.slice(0,a0)+"const DKP="+JSON.stringify(DKP)+";"+A.slice(b0);}

/* 名单安全扫描 */
const ROSTER="李航宇,李一菲,林青,刘欣冉,牟秀梅,那吉亚,王艺佳,王紫钰,吾麦尔江,夏合娜扎尔,姚倩倩,依米拉尼,张笑妍,赵昊轩,赵若晴,阿力耶,侯苏齐,贾翔天,康琳旋,刘安然,刘清优,孟克巴图,席婧瑜,许子沄,杨晨彤,努尔艾力,艾尼斯江,比力克孜,李姝畅,李雯博,刘明轩,麦迪乃姆,苗权禄,吕子萱,孟甜,王兴哲,王禹凡,信璐璐,徐若冰,王妍茹".split(",");
for(const [k,p] of Object.entries(DKP)){for(const n of ROSTER){if(p.html.includes(n))throw new Error("名单泄漏:"+k+":"+n)}}
console.log("DKP:",Object.keys(DKP).length,"页 | 名单扫描: 0 ✓");

/* ══════════ 手术 1：标题/CONFIG ══════════ */
A=A.replace("<title>小邮伴学·五环财务机器人｜教育教学智能体</title>","<title>小邮伴学｜财务机器人课堂智能体</title>");
A=A.replace('name:"小邮伴学 · 财务机器人课堂智能体"','name:"小邮伴学"');
A=A.replace('sub:"高职会计课堂的伴学智能体 · 学生先判断 · AI 只辅助 · 教师做终审"','sub:"财务机器人课堂智能体 · 高职《财务机器人应用与开发》 ｜ 学生先判断 · AI 只辅助 · 教师做终审"');
A=A.replace('<h1 id="appName">小邮伴学 · 财务机器人课堂智能体</h1>','<h1 id="appName">小邮伴学</h1>');
A=A.replace('<div class="sub" id="appSub">高职会计课堂的伴学智能体 · 学生先判断 · AI 只辅助 · 教师做终审</div>',
            '<div class="sub" id="appSub">财务机器人课堂智能体 · 高职《财务机器人应用与开发》 ｜ 学生先判断 · AI 只辅助 · 教师做终审</div>');
A=A.split("小邮伴学 · 财务机器人课堂智能体</h2>").join("小邮伴学</h2>");
A=A.replace("<p>我是小邮——从校园快递站跑进课堂的助教机器人。","<p>我是小邮——从校园快递站跑进《财务机器人应用与开发》课堂的助教机器人。");

/* ══════════ 手术 2：导航 ══════════ */
A=A.replace(`<nav><div class="nin">
  <button id="tb-home" class="on" onclick="showTab('home')">🏠 首页</button>
  <button id="tb-class" onclick="showTab('class')">🏫 课堂同步</button>
  <button id="tb-bot" onclick="showTab('bot')">🤖 机器人车间</button>
  <button id="tb-gest" onclick="showTab('gest')">🙌 手势闯关</button>
  <button id="tb-teach" onclick="showTab('teach')">📋 教师台</button>
  <button id="tb-about" onclick="showTab('about')">ℹ️ 关于</button>
</div></nav>`,
`<nav><div class="nin">
  <button id="tb-home" class="on" onclick="showTab('home')">🏠 首页</button>
  <button id="tb-class" onclick="showTab('class')">🏫 课堂同步</button>
  <button id="tb-lib" onclick="showTab('lib')">📚 课件馆</button>
  <button id="tb-bot" onclick="showTab('bot')">🤖 机器人车间</button>
  <button id="tb-gest" onclick="showTab('gest')">🙌 手势闯关</button>
  <button id="tb-teach" onclick="showTab('teach')">📋 教师台</button>
  <button id="tb-about" onclick="showTab('about')">ℹ️ 关于小邮</button>
</div></nav>`);
if(!A.includes('tb-lib'))throw new Error("nav 替换失败");

/* ══════════ 手术 3：首页（副题/五卡/评环改名/关系链撤出） ══════════ */
A=A.replace('<div class="card"><h3>🧣 评环试一试 · 生活费判断<span class="pb">可信协同 · 30 秒体验</span></h3>\n    <div class="note">先自己判断 → 规则复核给置信度 → 低置信自动进教师终审——课堂名题「父母转生活费」。</div>',
            '<div class="card"><h3>🙋 先判断，AI 复核，教师拍板——30 秒试一试<span class="pb">本智能体的核心机制</span></h3>\n    <div class="note">这是课堂名题「父母转的生活费能不能直接记收入」：你先选判断，AI 只做规则复核并给出置信度，拿不准的自动等老师终审。</div>');
{ /* 关系链卡整体撤出首页 */
  const a=A.indexOf('<div class="card"><h3>🔗 数字支付关系链');
  if(a>=0){const b=A.indexOf("</div>\n</section>",a);A=A.slice(0,a)+A.slice(b);}
}
A=A.replace(`    <div class="ring" onclick="showTab('class')"><b>📖</b><div class="t">陪你练 · 课堂同步</div><div class="d">本节课 19 页课件真页原样入住，逐层揭晓和课堂一模一样</div></div>`,
`    <div class="ring" onclick="showTab('class')"><b>📖</b><div class="t">陪你练 · 课堂同步</div><div class="d">本节课 19 页课件真页原样入住，逐层揭晓和课堂一模一样</div></div>
    <div class="ring" onclick="showTab('lib')"><b>📚</b><div class="t">任你翻 · 课件馆</div><div class="d">全部 6 门课件 154 页整馆入住：想翻哪页翻哪页</div></div>`);

/* ══════════ 手术 4：课堂同步工具条加「去课件馆」 ══════════ */
A=A.replace(`<button class="tbtn spot" id="clsSpotBtn" onclick="dkSpot('cls')">🔦 探照灯</button>
    </div>
  </div>
  <div class="stage" id="clsStage"></div>`,
`<button class="tbtn spot" id="clsSpotBtn" onclick="dkSpot('cls')">🔦 探照灯</button>
      <button class="tbtn" onclick="showTab('lib')">📚 全部课件 →</button>
    </div>
  </div>
  <div class="stage" id="clsStage"></div>`);

/* ══════════ 手术 5：课件馆 section（插在 class 之后） ══════════ */
const libSection=`
<section id="tab-lib">
  <div class="dkToolbar">
    <div class="dkTitle">📚 课件馆 · <b>全部课件，任你翻</b></div>
    <div class="rail" id="libDeckRail"></div>
    <div class="rail" id="libRail"></div>
    <div class="dkBtns">
      <button class="tbtn" onclick="dkPrev()">‹ 上一页</button>
      <span class="pageNo" id="libPageNo"></span>
      <button class="tbtn" onclick="dkNext()">下一页 ›</button>
      <button class="tbtn amber" onclick="dkRevealCur('lib')">✓ 揭晓下一层</button>
      <button class="tbtn spot" id="libSpotBtn" onclick="dkSpot('lib')">🔦 探照灯</button>
      <input id="libJump" class="sel" style="width:86px" inputmode="numeric" placeholder="页码" onkeydown="if(event.key==='Enter')libJumpGo()">
      <button class="tbtn" onclick="libJumpGo()">跳转</button>
    </div>
  </div>
  <div class="stage" id="libStage"></div>
</section>
`;
{const a=A.indexOf('</section>',A.indexOf('id="tab-class"'));
 A=A.slice(0,a)+"</section>\n"+libSection+A.slice(a+10);}

/* ══════════ 手术 6：手势页——关系链入住＋框定说明 ══════════ */
A=A.replace('<div class="eyebrow">演＋ · 本地手势识别（MediaPipe · 21点手部骨架）· 摄像头视频只在本机处理，不上传不保存</div>',
`<div class="eyebrow">用手答 · 本地手势识别（MediaPipe · 21点手部骨架）· 摄像头视频只在本机处理，不上传不保存</div>
  <div class="card"><h3>🔗 先看懂一笔花呗购物的关系链（下面五题的底座）</h3>
    <div class="chain" id="chainBox"></div>
    <div class="note">钱、货、权利、义务在四方之间流动——认清「谁欠谁、谁拥有什么」，再用四种手势回答五道认知题。</div>
  </div>`);
A=A.replace('<div class="say">🙌 四种手势答五关','<div class="say">🙌 四种手势答下面的五关');

/* ══════════ 手术 7：教师台说人话改版 ══════════ */
A=A.replace('<div class="card"><h3>🗂 可信评价 · 教师终审队列</h3>\n    <div class="note">规则复核置信度不足的判断，自动进这里；AI 只给意见，<b>裁定权在教师</b>。裁定后学生端立刻收到回执。</div>',
'<div class="card"><h3>⏳ 等老师拍板（AI 拿不准的都排在这儿）</h3>\n    <div class="note">学生先判断、AI 只复核；AI 没把握的判断自动排进本队列，<b>老师点「通过 / 退回」，学生那边立刻收到回执</b>。<br><b>什么时候用：</b>课前 2 分钟清空队列即可，不用盯屏。</div>');
A=A.replace('<div class="card"><h3>🧮 AI 备课预演（辨 ·「它一声不吭替你做了主」软件版）</h3>\n    <div class="note">把企业微信导出的记账作业喂给 AI，它会替你做很多「方便的小决定」——这里把每一个「主」都摆上台面，教师逐条把关。</div>',
'<div class="card"><h3>🧮 AI 备课预演——它替你做的主，你来把关</h3>\n    <div class="note">把企业微信导出的记账作业喂给 AI，它会一声不吭替你做几个「方便的小决定」（合并重名、拆事件、照单记收入）。这里把每个「主」摆上台面，逐条采纳或驳回。<br><b>什么时候用：</b>备新课、导入新一周期作业数据时。</div>');
A=A.replace('<div class="card"><h3>🗺 班级认知地图（辨 · 演示基线）</h3>\n    <div id="knowBox"></div>\n    <div class="note">接入真实作业数据后自动更新；此处为 67 份生活记账作业 + 课堂记分的演示基线。</div>',
'<div class="card"><h3>🗺 全班学情地图 ＋ 📸 课堂快照</h3>\n    <div id="knowBox"></div>\n    <div class="note" id="snapBox" style="margin-top:6px"></div>\n    <div class="note">接入真实作业数据后自动更新；此处为 67 份生活记账作业 + 课堂记分的演示基线。</div>');
A=A.replace('<div class="card"><h3>🧭 导学建议（导 · 一键生成）</h3>\n    <button class="btn" onclick="genAdvice()">生成下节课建议</button>',
'<div class="card"><h3>📌 下节课建议（老师看这里；学生用右下角 🤖 问小邮）</h3>\n    <button class="btn" onclick="genAdvice()">生成下节课建议</button>');
{ /* 旧课堂快照卡整卡撤（并入上学情卡） */
  const a=A.indexOf('<div class="card"><h3>📸 课堂快照（2026-09-11 · 匿名聚合）</h3>');
  if(a>=0){const b=A.indexOf('</div>',A.indexOf('id="snapBox"',a));const e=A.indexOf('</div>',b+6)+6;A=A.slice(0,a)+A.slice(e);}
}
A=A.replace('document.getElementById("snapBox").textContent=','{const e=document.getElementById("snapBox");if(e)e.textContent=');
A=A.replace('姓名已匿名。`;','姓名已匿名。`;}');

/* ══════════ 手术 8：助手开场语分工 ══════════ */
A=A.replace('我是小邮 🤖 三个用法：<br>① 不懂就问（我不直接给答案，先让你猜）<br>② 输入「<b>分析：＋一件事</b>」，我用 8 类错误标签帮你找记账的茬<br>③ 老师在投影上打开我，也是这节课的演示环节 😉',
'我是小邮 🤖 <b>学生</b>不懂就问我（我不直接给答案，先让你猜）；<b>老师</b>请看「教师台」的下节课建议。<br>还可以输入「<b>分析：＋一件事</b>」，我帮你找记账的茬。');

/* ══════════ 手术 9：课件馆引擎（数据＋逻辑＋CSS） ══════════ */
const deckCssExtra=Object.entries(LIB).filter(([k])=>k.startsWith("css_")).map(([k,v])=>v).join("\n");
const extraBase=`
.lib04,.lib10,.lib14,.lib16{font-size:19px}
.lib04 .slide,.lib10 .slide,.lib14 .slide,.lib16 .slide{position:relative;inset:auto;padding:26px 34px 40px;display:none;flex-direction:column;overflow:visible;height:auto}
.lib04 .slide.on,.lib10 .slide.on,.lib14 .slide.on,.lib16 .slide.on{display:flex}
.lib04 img,.lib10 img,.lib14 img,.lib16 img{border-radius:12px;max-width:100%}
`;
const libJs=`
const LIBDECKS=${JSON.stringify(Object.fromEntries(Object.entries(DECKS).map(([id,c])=>[id,{name:c.name,scope:c.scope}])))};
const LIBRAILS=${JSON.stringify(Object.fromEntries(Object.entries(LIB).filter(([k])=>k.startsWith("rail_")).map(([k,v])=>[k.slice(5),v])))};
dkState.lib={cur:0,spot:false,rail:null};
function libDeck(d){
  dkState.lib.cur=0;dkState.lib.rail=LIBRAILS[d];
  document.getElementById("libDeckRail").innerHTML=Object.keys(LIBDECKS).map(x=>'<button class="railBtn'+(x===d?" on":"")+'" onclick="libDeck(\\''+x+'\\')">'+LIBDECKS[x].name+"</button>").join("");
  dkState.lib.mountedRail=d;
  libShow();
}
function libShow(){
  const rail=dkState.lib.rail;const key=rail[dkState.lib.cur][0];
  dkShow("lib",key);
  document.getElementById("libRail").innerHTML=rail.map((x,i)=>'<button class="railBtn'+(i===dkState.lib.cur?" on":"")+'" onclick="libGo('+i+')">'+x[1]+"</button>").join("");
}
function libGo(i){dkState.lib.cur=i;libShow()}
function libJumpGo(){const n=parseInt(document.getElementById("libJump").value,10);
  const rail=dkState.lib.rail;if(!n||n<1||n>rail.length)return;
  dkState.lib.cur=n-1;libShow();document.getElementById("libStage").scrollIntoView({behavior:"smooth",block:"start"});}
`;
/* curZone 扩 lib + 键盘 */
A=A.replace('function curZone(){return document.getElementById("tab-class").classList.contains("on")?"cls":(document.getElementById("tab-bot").classList.contains("on")?"bot":"cls")}',
'function curZone(){const t=id=>document.getElementById(id).classList.contains("on");return t("tab-class")?"cls":(t("tab-lib")?"lib":(t("tab-bot")?"bot":"cls"))}');
A=A.replace('if(e.key==="ArrowRight")dkNext();if(e.key==="ArrowLeft")dkPrev();',
'if(e.key==="ArrowRight"&&!document.getElementById("libJump").__hasFocus)dkNext();if(e.key==="ArrowLeft")dkPrev();');
/* showTab 挂 lib */
A=A.replace('if(t==="class")renderClass();','if(t==="lib"){if(!dkState.lib.rail)libDeck("08");}if(t==="class")renderClass();');
/* dkRail 兼容数组轨（lib） */
A=A.replace('function dkRail(zone){return JSON.parse(dkState[zone].rail||"null")||DKRAIL[zone]}',
            'function dkRail(zone){return Array.isArray(dkState[zone].rail)?dkState[zone].rail:(JSON.parse(dkState[zone].rail||"null")||DKRAIL[zone])}');
/* CSS 注入 dkLb 前；JS 追加到 deck 引擎块（含 const dkState）末尾 */
A=A.replace('<div id="dkLb"',`<style>${deckCssExtra}\n${extraBase}</style>\n<div id="dkLb"`);
{const i0=A.indexOf("const dkState=");if(i0<0)throw new Error("找不到 dkState");
 const iEnd=A.indexOf("</script>",i0);if(iEnd<0)throw new Error("找不到引擎块尾");
 A=A.slice(0,iEnd)+libJs+"\n"+A.slice(iEnd);}

/* ══════════ 手术 10：about 口径补课件馆 ══════════ */
A=A.replace("与自研课件同一套页面（19 页真页内嵌），课上课件、课后智能体，互为镜像","与自研课件同一套页面：本节课 19 页精编轨＋全部 6 门课件 154 页任翻（课件馆），课上课件、课后智能体，互为镜像");

fs.writeFileSync(R+DST,A);
console.log("写出:",DST,(fs.statSync(R+DST).size/1024/1024).toFixed(2)+"MB");
console.log("DKP总数:",Object.keys(DKP).length,"| 库轨道:",Object.entries(LIB).filter(([k])=>k.startsWith("rail_")).map(([k,v])=>k.slice(5)+":"+v.length).join(" "));
