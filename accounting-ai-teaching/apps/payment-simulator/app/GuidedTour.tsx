'use client';
import {useCallback,useEffect,useState} from 'react';
export type TourStep={target:string;title:string;content:string};
export default function GuidedTour({steps,tourKey,restartSignal=0,intro}:{steps:TourStep[];tourKey:string;restartSignal?:number;intro?:{eyebrow?:string;title:string;content:string;button?:string}}){
 const [showIntro,setShowIntro]=useState(false),[active,setActive]=useState(false),[index,setIndex]=useState(0),[rect,setRect]=useState<DOMRect|null>(null);
 const measure=useCallback((i:number)=>{const el=document.querySelector(steps[i]?.target) as HTMLElement|null;setRect(el?el.getBoundingClientRect():null)},[steps]);
 const locate=useCallback((i:number)=>{const el=document.querySelector(steps[i]?.target) as HTMLElement|null;if(!el){setRect(null);return}el.scrollIntoView({behavior:'smooth',block:'center'});setTimeout(()=>measure(i),350)},[steps,measure]);
 useEffect(()=>{if(typeof window==='undefined')return;setIndex(0);const seen=sessionStorage.getItem(`tour-intro:${tourKey}`)==='1';if(intro&&!seen){setShowIntro(true);setActive(false)}else if(!intro){setActive(true);setTimeout(()=>locate(0),500)}},[tourKey]);
 useEffect(()=>{if(restartSignal>0){setActive(true);setIndex(0);setTimeout(()=>locate(0),100)}},[restartSignal]);
 useEffect(()=>{if(!active)return;const f=()=>measure(index);window.addEventListener('resize',f);window.addEventListener('scroll',f,{passive:true});return()=>{window.removeEventListener('resize',f);window.removeEventListener('scroll',f)}},[active,index,measure]);
 function go(i:number){if(i>=steps.length){finish();return}setIndex(i);locate(i)}
 function finish(){setActive(false);setRect(null)}
 if(showIntro)return <div className="tour-intro-backdrop"><div className="tour-intro-modal"><span>{intro?.eyebrow||'首次使用指引'}</span><h2>{intro?.title}</h2><p>{intro?.content}</p><div><button onClick={()=>{sessionStorage.setItem(`tour-intro:${tourKey}`,'1');setShowIntro(false)}}>暂时跳过</button><button className="primary" onClick={()=>{sessionStorage.setItem(`tour-intro:${tourKey}`,'1');setShowIntro(false);setActive(true);setIndex(0);setTimeout(()=>locate(0),180)}}>{intro?.button||'开始操作指引'}</button></div></div></div>;
 if(!active||!rect)return null;
 const gap=8,left=Math.max(8,rect.left-gap),top=Math.max(8,rect.top-gap),right=Math.min(innerWidth-8,rect.right+gap),bottom=Math.min(innerHeight-8,rect.bottom+gap),w=right-left,h=bottom-top,tipW=Math.min(350,innerWidth-24),placeBelow=bottom+190<innerHeight,tipTop=placeBelow?bottom+14:Math.max(12,top-175),tipLeft=Math.min(innerWidth-tipW-12,Math.max(12,left+w/2-tipW/2));
 const step=steps[index];
 return <div className="tour-root" aria-modal="true"><div className="tour-mask top" style={{height:top}}/><div className="tour-mask left" style={{top,height:h,width:left}}/><div className="tour-mask right" style={{top,height:h,left:right}}/><div className="tour-mask bottom" style={{top:bottom}}/><div className="tour-spot" style={{left,top,width:w,height:h}}/><div className="tour-tip" style={{left:tipLeft,top:tipTop,width:tipW}}><div className="tour-progress"><span>操作引导</span><b>{index+1} / {steps.length}</b></div><h3>{step.title}</h3><p>{step.content}</p><div className="tour-actions"><button className="skip" onClick={finish}>跳过本次引导</button>{index>0&&<button onClick={()=>go(index-1)}>上一步</button>}<button className="next" onClick={()=>go(index+1)}>{index===steps.length-1?'完成引导':'下一步'}</button></div></div></div>
}
