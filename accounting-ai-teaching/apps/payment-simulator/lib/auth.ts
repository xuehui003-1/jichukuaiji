import { cookies } from 'next/headers';
import { prisma } from './prisma';
export const SESSION_COOKIE='acct_session';
export async function currentUser(){
 const jar=await cookies();const token=jar.get(SESSION_COOKIE)?.value;if(!token)return null;
 const session=await prisma.session.findUnique({where:{token},include:{user:true}});
 if(!session||session.expiresAt<new Date())return null;return session.user;
}
