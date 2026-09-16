import { NextResponse } from 'next/server';
import { prisma } from '../../../../lib/prisma';
import { currentUser } from '../../../../lib/auth';
function extractJson(text:string){const clean=text.replace(/^```(?:json)?\s*/i,'').replace(/\s*```$/,'').trim();const a=clean.indexOf('{'),b=clean.lastIndexOf('}');if(a<0||b<a)throw new Error('NO_JSON');return JSON.parse(clean.slice(a,b+1))}
function valid(x:any){return x&&['type','summary','flow','question','feedback','variation'].every(k=>typeof x[k]==='string')}
export async function POST(request:Request){
 const user=await currentUser();if(!user||user.role!=='STUDENT')return NextResponse.json({ok:false,error:'仅登录学生可使用AI分析'},{status:403});
 const mode=process.env.AI_MODE||'mock',base=(process.env.AI_BASE_URL||'https://api.deepseek.com').replace(/\/$/,''),key=process.env.AI_API_KEY,model=process.env.AI_MODEL||'deepseek-v4-flash';
 if(mode!=='online'||!key)return NextResponse.json({ok:false,fallback:true,error:'当前使用离线Mock模式'},{status:503});
 const input=await request.json(),started=Date.now();let status='SUCCESS',errorCode:string|undefined;
 try{
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),30000);
  const response=await fetch(`${base}/chat/completions`,{method:'POST',headers:{'Content-Type':'application/json','Authorization':`Bearer ${key}`},signal:controller.signal,body:JSON.stringify({model,temperature:0.2,stream:false,max_tokens:1200,messages:[{role:'system',content:`你是高职《基础会计》AI伴学分析器。只做生活经济事项结构化和启发式追问，不替学生作答，不把个人生活机械等同企业账务。请只输出一个JSON对象，不要Markdown。字段：type事项类型；summary脱敏摘要；amount识别金额字符串；flow资金/资源/权利义务线索；question给学生的2个启发问题；feedback学生提交后可用的诊断方向，不给完整答案；variation一个变式任务；tag从VAGUE_EVENT、MULTIPLE_EVENTS_MERGED、CASH_EQUALS_INCOME、CASH_EQUALS_EXPENSE、IGNORE_LIABILITY、IGNORE_RECEIVABLE、ACCOUNT_TRANSFER_AS_EXPENSE、ACCOUNTING_ENTITY_CONFUSION或空字符串中选。若信息不足，type写“信息待补充”并在question中要求补充。`},{role:'user',content:JSON.stringify({participation:input.participation,category:input.category,eventDate:input.eventDate,amountMode:input.amountMode,amount:input.amount,payment:input.payment,fundFlow:input.fundFlow,description:input.description})}]})});clearTimeout(timer);
  if(!response.ok){errorCode=`HTTP_${response.status}`;throw new Error(errorCode)}const data=await response.json();const result=extractJson(data.choices?.[0]?.message?.content||'');if(!valid(result)){errorCode='INVALID_SCHEMA';throw new Error(errorCode)}
  await prisma.aIRequestLog.create({data:{userId:user.id,app:'LIFE_LEDGER',requestType:'ANALYZE_EVENT',provider:'DeepSeek',model,durationMs:Date.now()-started,status}});
  return NextResponse.json({ok:true,source:'online',model,result});
 }catch(e){status='FAILED';errorCode=errorCode||((e as Error).name==='AbortError'?'TIMEOUT':'PARSE_ERROR');await prisma.aIRequestLog.create({data:{userId:user.id,app:'LIFE_LEDGER',requestType:'ANALYZE_EVENT',provider:'DeepSeek',model,durationMs:Date.now()-started,status,errorCode}}).catch(()=>{});return NextResponse.json({ok:false,fallback:true,error:'真实AI暂时不可用，已切换本地规则',errorCode},{status:502})}
}
