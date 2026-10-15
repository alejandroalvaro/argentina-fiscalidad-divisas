import openpyxl,csv,re,calendar,datetime as dt,json,collections
D=dt.date
CUT=D(2026,6,30)
wb=openpyxl.load_workbook('lote_C/docs/deuda_publica_30-06-2026_0.xlsx',data_only=True)
ws=wb['A.1.7']
rows=[]
for i,r in enumerate(ws.iter_rows(min_row=13,values_only=True),13):
    if r[2] is None or r[0] is not None and False or not isinstance(r[7],(int,float)) or r[1] is None: continue
    rows.append(dict(fila=i,emision=r[1].date(),nombre=str(r[2]).strip(),tasa=r[3],venc_anio=r[4],vno=r[5],vnr=r[6],vna=r[7]))
sig=list(csv.DictReader(open('lote_C/data/sigade_2026-06-30_saldo_de_deuda_en_situacion_de_pago_normal.csv',encoding='utf-8')))
def match(r):
    c=[s for s in sig if abs(float(s['Saldo en Dólares'])-r['vna']*1000)<=max(1.0,r['vna']*1000*1e-9) and s['Moneda del Prestamo']=='ARP']
    return c
def maturity(name):
    m=re.search(r'(\d{2})-(\d{2})-(\d{4})',name)
    if m: return D(int(m.group(3)),int(m.group(2)),int(m.group(1)))
    m=re.search(r'(\d{1,2})-(\d{1,2})-(\d{2})(?!\d)',name)
    return None
def d360(a,b): return (b.year-a.year)*360+(b.month-a.month)*30+(min(b.day,30)-min(a.day,30))
def addm(d,k):
    y=d.year+(d.month-1+k)//12; m=(d.month-1+k)%12+1
    return D(y,m,min(d.day,calendar.monthrange(y,m)[1]))
def kmonths(a,t):
    k=(t.year-a.year)*12+t.month-a.month
    while k>0 and addm(a,k)>t: k-=1
    return k
out=[]
for r in rows:
    n=r['nombre']
    if not (n.startswith('BONCAP') or n.startswith('LECAP')): continue
    r['tipo']='TEM fija' if re.search(r'/\$/\d,\d\d%/',n) else ('dual' if 'DUAL' in n else 'TAMAR')
    m=re.search(r'/(\d{2})-(\d{2})-(\d{4})(?: \(\d\))?$',n)
    r['venc']=D(int(m.group(3)),int(m.group(2)),int(m.group(1)))
    r['ratio']=r['vna']/r['vnr']
    mm=match(r); r['sigade']=mm[0] if len(mm)==1 else None; r['nmatch']=len(mm)
    r['k']=kmonths(r['emision'],CUT)
    out.append(r)
for r in out:
    s=r['sigade']; 
    print(r['tipo'],r['nombre'][:42],r['emision'],r['venc'],'ratio=%.5f'%r['ratio'],'k=',r['k'],'match',r['nmatch'],s['Nombre de la Operación'] if s else None)
import pickle; pickle.dump(out,open('/tmp/cap_rows.pkl','wb'))

# ---------- parte 2: modelo ----------
import math
def tem_of(r):
    if r['tipo']=='TEM fija': return float(r['tasa'])
    if r['k']>0: return r['ratio']**(1.0/r['k'])-1
    return None
for r in out:
    r['tem']=tem_of(r)
    r['saldo_ars']=float(r['sigade']['Saldo en Moneda de Origen'])
    r['vn_ars']=r['saldo_ars']/r['ratio']
    r['cap_corte']=r['saldo_ars']-r['vn_ars']
    r['ratio_modelo_step']=(1+r['tem'])**r['k'] if r['tem'] else None
    f=lambda t: r['vn_ars']*(1+r['tem'])**(d360(r['emision'],t)/30.0) if r['tem'] else None
    r['B']=f
    r['B_corte_legal']=f(CUT) if r['tem'] else None
    r['pago_venc']=f(r['venc']) if r['tem'] else None
print('check ratio step vs reported (TEM fija):')
for r in out:
    if r['tipo']=='TEM fija': print(r['nombre'][:30],'%.6f %.6f'%(r['ratio'],r['ratio_modelo_step']))
tot=lambda g,k: sum(r[k] for r in out if r['tipo'] in g)
print('cap al corte (ARS bn):', {t:round(sum(r['cap_corte'] for r in out if r['tipo']==t)/1e12,3) for t in ['TEM fija','TAMAR','dual']})
print('saldo corte (ARS bn):', {t:round(sum(r['saldo_ars'] for r in out if r['tipo']==t)/1e12,3) for t in ['TEM fija','TAMAR','dual']})
pickle.dump([{k:v for k,v in r.items() if k not in('B','sigade')}|{'sig_name':r['sigade']['Nombre de la Operación']} for r in out],open('/tmp/cap_rows2.pkl','wb'))
# meses
def eom(y,m): return D(y,m,calendar.monthrange(y,m)[1])
months=[]
y,m=2026,7
while (y,m)<=(2028,8):
    months.append((y,m)); m+=1
    if m==13: y+=1;m=1
res=[]
for (y,m) in months:
    E=eom(y,m); P=CUT if (y,m)==(2026,7) else eom(*( (y,m-1) if m>1 else (y-1,12)))
    row={'mes':f'{y}-{m:02d}'}
    for grp,tipos in (('fija',['TEM fija']),('flot',['TAMAR','dual'])):
        acc=pay_int=pay_pr=sc=0.0
        for r in out:
            if r['tipo'] not in tipos or not r['tem']: continue
            if r['venc']<=P: continue
            e=min(E,r['venc']); 
            acc+=r['B'](e)-r['B'](P)
            B0=r['B_corte_legal']
            dd=d360(P,e)/30.0
            sc+=B0*((1+r['tem'])**dd-1)
            if P<r['venc']<=E:
                pay_int+=r['B'](r['venc'])-r['vn_ars']; pay_pr+=r['vn_ars']
        row[f'{grp}_devengado_no_pagado']=acc; row[f'{grp}_interes_pagado_caja_real_al_vto']=pay_int
        row[f'{grp}_capital_vn_pagado_al_vto']=pay_pr; row[f'{grp}_interes_caja_escenario_mensual']=sc
    res.append(row)
pickle.dump(res,open('/tmp/cap_months.pkl','wb'))
for r in res[:14]: print(r['mes'],*['%.1f'%(r[k]/1e9) for k in r if k!='mes'])
