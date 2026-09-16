'use client';
import {useEffect,useRef,useState} from 'react';
const questions=[
 {text:'银行卡向校园卡充值100元',answer:'账户转换'},
 {text:'使用花呗购买耳机，下月还款',answer:'偿还义务'},
 {text:'替三名同学先付聚餐费',answer:'收回权利'},
 {text:'网购退款已经确认但尚未到账',answer:'待收权利'},
 {text:'食堂购买并立即吃完午餐',answer:'资源消耗'},
 {text:'父母转入生活费',answer:'需明确主体'},
 {text:'把钱借给朋友，下周归还',answer:'收回权利'},
 {text:'支付可退还的共享设备押金',answer:'收回权利'}
];
const categories=['账户转换','偿还义务','收回权利','待收权利','资源消耗','需明确主体'];
const errors=[
 {statement:'校园卡充值100元，所以立即形成费用100元。',answer:'时点错误',reason:'充值后资源仍可使用，充值不等于实际消费。'},
 {statement:'收到同学归还的垫付款，所以确认收入。',answer:'性质错误',reason:'收回此前形成的权利，不形成新的收入。'},
 {statement:'花呗购买时银行卡没有减少，所以没有发生经济事项。',answer:'义务遗漏',reason:'商品已取得，同时形成未来偿还义务。'},
 {statement:'父母转生活费就是企业会计中的收入。',answer:'主体错误',reason:'个人生活与企业会计主体不能直接混用。'}
];
export default function LifeMiniGames(){
 const [mode,setMode]=useState<'classify'|'detect'>('classify'),[running,setRunning]=useState(false),[index,setIndex]=useState(0),[score,setScore]=useState(0),[streak,setStreak]=useState(0),[time,setTime]=useState(60),[feedback,setFeedback]=useState(''),[saveMessage,setSaveMessage]=useState('');
 const startRef=useRef(Date.now()),scoreRef=useRef(0),totalRef=useRef(0),correctRef=useRef(0),detailsRef=useRef<any[]>([]),savedRef=useRef(false);
 useEffect(()=>{if(!running||time<=0)return;const t=setInterval(()=>setTime(x=>x-1),1000);return()=>clearInterval(t)},[running,time]);
 useEffect(()=>{if(running&&time===0)finish()},[time,running]);
 function start(m:'classify'|'detect'){setMode(m);setRunning(true);setIndex(0);setScore(0);setStreak(0);setTime(60);setFeedback('');setSaveMessage('');startRef.current=Date.now();scoreRef.current=0;totalRef.current=0;correctRef.current=0;detailsRef.current=[];savedRef.current=false}
 function answer(x:string){const current=mode==='classify'?questions[index%questions.length]:errors[index%errors.length],ok=x===current.answer;totalRef.current++;if(ok)correctRef.current++;detailsRef.current.push({question:index+1,text:(current as any).text||(current as any).statement,answer:x,correctAnswer:current.answer,correct:ok});if(ok){const points=10+Math.min(5,streak);scoreRef.current+=points;setScore(scoreRef.current);setStreak(v=>v+1);setFeedback(`✓ 正确${mode==='detect'?`：${(current as any).reason}`:''}`)}else{setStreak(0);setFeedback(`✗ 正确答案：${current.answer}${mode==='detect'?`。${(current as any).reason}`:''}`)}setTimeout(()=>{setIndex(i=>i+1);setFeedback('')},700)}
 async function finish(){if(savedRef.current)return;savedRef.current=true;setRunning(false);setSaveMessage('正在保存游戏成绩…');try{const r=await fetch('/api/game-attempts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({gameType:mode==='classify'?'CLASSIFY':'DETECT',score:scoreRef.current,total:totalRef.current,correct:correctRef.current,durationMs:Date.now()-startRef.current,details:detailsRef.current})}),d=await r.json();setSaveMessage(d.ok?'✓ 游戏成绩已保存到SQLite':'保存失败')}catch{setSaveMessage('保存失败')}}
 const q=mode==='classify'?questions[index%questions.length]:errors[index%errors.length];
 return <section className="life-games"><div className="game-head"><div><span>练习游戏化</span><h2>生活会计小游戏</h2><p>分数来自判断、连续正确和订正，不与消费金额挂钩。</p></div>{running&&<div className="game-stats"><b>{score}<small>分</small></b><span>{time}s</span><em>连对{streak}</em></div>}</div>{!running?<div className="game-select"><button onClick={()=>start('classify')}><span>60秒</span><b>会计分类挑战</b><p>把生活事项归入资金、资源、权利或义务。</p><em>▶ 开始游戏</em></button><button onClick={()=>start('detect')}><span>AI找茬</span><b>生活账错误侦探</b><p>找出AI分析中的主体、时点和性质错误。</p><em>▶ 开始游戏</em></button></div>:<div className="game-board"><div className="game-progress"><i style={{width:`${time/60*100}%`}}/></div><span className="round">第{index+1}题 · {mode==='classify'?'选择经济关系':'找出错误类型'}</span><h3>{(q as any).text||(q as any).statement}</h3><div className="game-options">{(mode==='classify'?categories:['主体错误','时点错误','性质错误','义务遗漏']).map(x=><button onClick={()=>answer(x)} disabled={!!feedback} key={x}>{x}</button>)}</div>{feedback&&<p className={feedback.startsWith('✓')?'correct':'wrong'}>{feedback}</p>}<button className="quit-game" onClick={finish}>结束并保存成绩</button></div>}{saveMessage&&<p className="game-save-message">{saveMessage}</p>}</section>
}
