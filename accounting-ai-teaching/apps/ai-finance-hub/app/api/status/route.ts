import {NextResponse} from 'next/server';
export const dynamic='force-dynamic';
async function probe(url:string){try{const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),1400);const res=await fetch(url,{cache:'no-store',signal:controller.signal});clearTimeout(timer);if(!res.ok)return false;const data=await res.json();return data?.ok===true}catch{return false}}
export async function GET(){const [appA,appB]=await Promise.all([probe('http://127.0.0.1:3000/api/health'),probe('http://127.0.0.1:3001/api/health')]);return NextResponse.json({ok:true,hub:true,appA,appB,checkedAt:new Date().toISOString()})}
