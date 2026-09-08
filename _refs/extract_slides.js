#!/usr/bin/env node
/* 课件 SLIDES 权威提取器：node eval 解析（绕开文本 split 的丢头/假 ]; 坑）
   用法: node _refs/extract_slides.js <课件.html> <输出.json> */
const fs = require('fs');
const [, , inFile, outFile] = process.argv;
const s = fs.readFileSync(inFile, 'utf8');
const a = s.indexOf('const SLIDES');
if (a < 0) throw new Error('未找到 const SLIDES: ' + inFile);
const b = s.indexOf('\n];', a);
if (b < 0) throw new Error('未找到 SLIDES 结尾: ' + inFile);
const code = s.slice(a, b + 3);
const SLIDES = eval(code.replace('const SLIDES =', ''));
if (SLIDES.includes(undefined)) throw new Error('SLIDES 有稀疏洞(双逗号), 浏览器会出空白页: ' + inFile);
const bad = SLIDES.map((x, i) => [x, i]).filter(([x]) => !('cls' in x) || !x.html);
if (bad.length) throw new Error('异常条目(0基): ' + bad.map(([, i]) => i).join(','));
const out = SLIDES.map((x, i) => ({ no: i + 1, cls: String(x.cls || ''), html: String(x.html || ''), notes: String(x.notes || ''), badges: x.badges || [] }));
fs.writeFileSync(outFile, JSON.stringify(out));
console.log(inFile.split('/').pop().slice(0, 2), '->', out.length, '页 ->', outFile);
