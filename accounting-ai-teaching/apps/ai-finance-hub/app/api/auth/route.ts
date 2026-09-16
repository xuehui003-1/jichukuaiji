import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import crypto from 'node:crypto';
import { prisma } from '../../../lib/prisma';
import { SESSION_COOKIE } from '../../../lib/auth';
export async function POST(request:Request){
 try{const {username,password}=await request.json();const user=await prisma.user.findUnique({where:{username}});const hash=crypto.createHash('sha256').update(String(password||'')).digest('hex');if(!user||user.passwordHash!==hash)return NextResponse.json({ok:false,error:'用户名或密码错误'},{status:401});await prisma.user.update({where:{id:user.id},data:{lastLoginAt:new Date()}});const token=crypto.randomBytes(32).toString('hex');const expiresAt=new Date(Date.now()+8*60*60*1000);await prisma.session.create({data:{token,userId:user.id,expiresAt}});const jar=await cookies();jar.set(SESSION_COOKIE,token,{httpOnly:true,sameSite:'lax',path:'/',expires:expiresAt});return NextResponse.json({ok:true,user:{id:user.id,username:user.username,displayName:user.displayName,role:user.role,forcePasswordChange:user.forcePasswordChange}})}catch{return NextResponse.json({ok:false,error:'登录失败，请确认数据库已初始化'},{status:500})}
}
export async function DELETE(){const jar=await cookies();const token=jar.get(SESSION_COOKIE)?.value;if(token)await prisma.session.deleteMany({where:{token}});jar.delete(SESSION_COOKIE);return NextResponse.json({ok:true})}
