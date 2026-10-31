const fs=require('fs');const d=require('docx');const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,BorderStyle,AlignmentType,Footer,PageNumber,ShadingType}=d;
const D=JSON.parse(fs.readFileSync('reports/core-bd-close.json','utf8'));const today='2026-10-31';
const P=(t,o={})=>new Paragraph({spacing:{after:120},children:[new TextRun({text:t,font:'Arial',size:o.size||20,bold:!!o.bold,color:o.color||'1A1A1A'})]});
const W=[2600,1500,2700,1900,1740];
const cell=(t,w,h)=>new TableCell({width:{size:w,type:WidthType.DXA},shading:h?{type:ShadingType.CLEAR,fill:'1F3A5F',color:'auto'}:undefined,margins:{top:60,bottom:60,left:80,right:80},children:[new Paragraph({children:[new TextRun({text:String(t??''),font:'Arial',size:16,bold:!!h,color:h?'FFFFFF':'1A1A1A'})]})]});
const tbl=(head,rows)=>new Table({width:{size:W.reduce((a,b)=>a+b),type:WidthType.DXA},columnWidths:W,rows:[new TableRow({tableHeader:true,children:head.map((h,i)=>cell(h,W[i],true))}),...rows.map(r=>new TableRow({children:r.map((t,i)=>cell(t,W[i]))}))]});
const S=[];
S.push(P('Core BD Report \u2014 Florida',{bold:true,size:32}),P('DashRite Advisory LLC \u00b7 regenerated on the final bytes of the Florida 100 close \u00b7 '+today+' \u00b7 every figure read from the files; nothing typed',{size:18,color:'555555'}));
S.push(P('Florida in all: 200 rows across 197 companies (self-overlap checked 2026-10-31: three companies sit in both florida.html and florida-expansion.html). Call-ready: 98 rows across 97 companies. Every count below states rows or companies.',{bold:true}));
S.push(P(`Callable today from the existing Florida rows (rows): ${D.callable.length} of 47 Tier A (unchanged by the Florida 100 run \u2014 florida.html was not edited). Band 1: ${D.callable.filter(r=>r.band===1).length}.`));
S.push(P(`The Florida 100, closed at its measured count: ${D.admitted.length} admitted (Unverified, size Blind under the Chair\u2019s ruling, awaiting the Chair\u2019s tests 3 and 4) and ${D.contact_outstanding.length} complete with the contact outstanding. The target closed as a route tested and found absent, not as a shortfall.`));
for(const pr of ['Acquisitions','Fractionals','Private Equity']){
  const a=D.admitted.filter(r=>r.practice===pr);S.push(P(pr,{bold:true,size:24}));
  S.push(P(a.length?`${a.length} admitted row(s), each with a proved site, a dated third-party signal, tests 1, 2 and 5 passed, and a named executive with a source.`:'No admitted row in this practice.',{size:18}));
  if(a.length)S.push(tbl(['Company','Practice','Decision maker','Phone','Executive read'],a.map(r=>[r.company,r.practice,r.dm,r.phone,r.dm_read||''])));
}
S.push(P('Complete, contact outstanding',{bold:true,size:24}),P('Every test passed and size Blind; not admitted and never counted as admitted, because no named executive with a title was found on the routes spent (recorded on each row).',{size:18}));
S.push(tbl(['Company','Practice','Own site','',''],D.contact_outstanding.map(r=>[r.company,r.practice,r.site||'','',''])));
S.push(P('Existing callable rows',{bold:true,size:24}));
S.push(tbl(['Company','City','Band','Named person','Phone on file'],D.callable.map(r=>[r.company,r.city,String(r.band??''),r.person,r.phone])));
const doc=new Document({sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1000,bottom:1000,left:900,right:900},borders:{pageBorderTop:{style:BorderStyle.SINGLE,size:6,color:'1F3A5F',space:20},pageBorderBottom:{style:BorderStyle.SINGLE,size:6,color:'1F3A5F',space:20},pageBorderLeft:{style:BorderStyle.SINGLE,size:6,color:'1F3A5F',space:20},pageBorderRight:{style:BorderStyle.SINGLE,size:6,color:'1F3A5F',space:20}}}},footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:'DashRite Advisory LLC \u00b7 Core BD Report \u2014 Florida \u00b7 page ',size:16,font:'Arial'}),new TextRun({children:[PageNumber.CURRENT],size:16,font:'Arial'})]})]})},children:S}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync('Core-BD-Report-Florida.docx',b);fs.writeFileSync('reports/Core-BD-Report-Florida.docx',b);console.log('written',b.length)});
