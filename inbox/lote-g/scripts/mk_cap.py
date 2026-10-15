import csv,re,os,pickle,calendar,datetime as dt,sys
sys.argv=['x']
exec(open('cap_calc.py').read().split('# ---------- parte 2: modelo ----------')[0].replace('print(','(lambda *a,**k:None)('))
exec('# ---------- parte 2: modelo ----------'+open('cap_calc.py').read().split('# ---------- parte 2: modelo ----------')[1].replace('print(','(lambda *a,**k:None)('))
M=1e6  # a millones de pesos
OUT='lote_G/tablas'; os.makedirs(OUT,exist_ok=True)
def W(fn,h,rows):
    with open(fn,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(h); [w.writerow(r) for r in rows]
def fm(x,n=1): return '' if x is None else f'{x:.{n}f}'
# ---- tabla 1: instrumentos
ID={}
ins=list(csv.DictReader(open('lote_C/instruments.csv',encoding='utf-8')))
for i in ins: ID[i['operation_name_sigade']]=i['instrument_id']
rowsI=[]
for r in sorted(out,key=lambda r:(r['tipo'],r['venc'])):
    sn=r['sigade']['Nombre de la Operación']
    rowsI.append([ID.get(sn,''),sn,r['nombre'],r['tipo'],r['emision'],r['venc'],
        fm(r['tem']*100,4) if r['tem'] is not None else '', 'dato (nombre del instrumento)' if r['tipo']=='TEM fija' else ('derivado: coeficiente reportado^(1/meses)' if r['tem'] else 'sin dato'),
        fm(r['saldo_ars']/M),fm(r['vn_ars']/M),fm(r['cap_corte']/M),fm(r['ratio'],6),
        fm(r['B_corte_legal']/M) if r['B_corte_legal'] else '', fm((r['B_corte_legal']-r['saldo_ars'])/M) if r['B_corte_legal'] else '',
        fm(r['pago_venc']/M) if r['pago_venc'] else '', fm((r['pago_venc']-r['vn_ars'])/M) if r['pago_venc'] else '',
        fm((r['pago_venc']-r['B_corte_legal'])/M) if r['pago_venc'] else ''])
W(f'{OUT}/capitalizacion_instrumentos.csv',['instrument_id','operacion_sigade','denominacion_boletin','tipo','fecha_emision','vencimiento','tem_pct','origen_tem','saldo_sigade_corte_millones_ars','valor_nominal_residual_millones_ars','interes_capitalizado_en_saldo_al_corte_millones_ars','coeficiente_capitalizacion_reportado','saldo_formula_legal_al_corte_millones_ars','devengado_no_capitalizado_en_saldo_al_corte_millones_ars','pago_estimado_al_vencimiento_millones_ars','interes_total_estimado_al_vencimiento_millones_ars','interes_a_devengar_post_corte_millones_ars'],rowsI)
# ---- tabla 2: mensual
res=pickle.load(open('/tmp/cap_months.pkl','rb'))
hdr=['mes']
cols=['devengado_no_pagado','interes_pagado_caja_real_al_vto','capital_vn_pagado_al_vto','interes_caja_escenario_mensual']
rowsM=[];cum={}
for r in res:
    row=[r['mes']]
    for g in ('fija','flot'):
        for c in cols: row.append(fm(r[f'{g}_{c}']/M))
    rowsM.append(row)
H=['mes']+[f'{g}_{c}_millones_ars' for g in ('tem_fija','flotantes_y_duales_supuesto') for c in cols]
W(f'{OUT}/capitalizacion_mensual.csv',H,rowsM)
tot={ (g,c):sum(r[f'{g}_{c}'] for r in res) for g in ('fija','flot') for c in cols}
for k,v in tot.items(): print(k,round(v/M,1))
# ---- tabla 3: stock al corte por grupo
def grp_sum(sheet):
    ws=wb[sheet];L=[]
    for i,r in enumerate(ws.iter_rows(min_row=13,values_only=True),13):
        if r[2] is None or r[1] is None or not isinstance(r[7],(int,float)): continue
        L.append(dict(nombre=str(r[2]).strip(),vnr=r[6],vna=r[7]))
    return L
g=[]
def add(grupo,nombre,saldo,cap,nota): g.append([grupo,nombre,fm(saldo/M),fm(cap/M),nota])
for t,lab in (('TEM fija','BONCAP y LECAP a tasa efectiva mensual fija (13 instrumentos)'),('TAMAR','BONCAP y LECAP a TAMAR + margen (6 instrumentos)'),('dual','BONCAP Dual (2 instrumentos)')):
    add('A. Interés capitalizado (capitalización mensual, pago íntegro al vencimiento)',lab,sum(r['saldo_ars'] for r in out if r['tipo']==t),sum(r['cap_corte'] for r in out if r['tipo']==t),'derivado de SRC-0103 hoja A.1.7 (coeficiente) y SRC-0102 (saldo)')
cer=grp_sum('A.1.8')
FX=float([x for x in sig if x['Nombre de la Operación']=='BONCAP/$/15-01-2027'][0]['Saldo en Moneda de Origen'])/float([x for x in sig if x['Nombre de la Operación']=='BONCAP/$/15-01-2027'][0]['Saldo en Dólares'])
print('FX implícito',FX)
for r in cer: r['saldo_ars']=r['vna']*1000*FX; r['dev']=(r['vna']-r['vnr'])*1000*FX
def cls(n):
    if n.startswith('BONTE DUAL'): return 'BONTE Dual CER o TAMAR'
    if re.match(r'BONCER/\$\+CER/\d,',n): return 'BONCER con cupón (2%, 2,25%, 2,5%)'
    if n.startswith('BONCER/$+CER/') or n.startswith('LECER'): return 'BONCER cero cupón y LECER'
    return 'Par, Discount, Cuasipar CER, pagarés y préstamos garantizados (legados)'
for lab in ['BONCER cero cupón y LECER','BONTE Dual CER o TAMAR','BONCER con cupón (2%, 2,25%, 2,5%)','Par, Discount, Cuasipar CER, pagarés y préstamos garantizados (legados)']:
    s_=[r for r in cer if cls(r['nombre'])==lab]
    add('B. Ajuste por CER devengado y no pagado (indexación, distinto de capitalización de interés)',lab+f' ({len(s_)} filas)',sum(r['saldo_ars'] for r in s_),sum(r['dev'] for r in s_),'derivado de SRC-0103 hoja A.1.8; USD de la planilla convertidos a pesos con el tipo de cambio implícito de SIGADE al 30-06-2026 ('+f'{FX:.4f}'+' ARS/USD); el coeficiente combina CER y capitalización cuando existe')
W(f'{OUT}/capitalizacion_stock_corte.csv',['grupo','instrumentos','saldo_sigade_corte_millones_ars','devengado_en_saldo_al_corte_millones_ars','fuente_y_metodo'],g)
for x in g: print(x)
pickle.dump((tot,),open('/tmp/cap_tot.pkl','wb'))
