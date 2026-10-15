import csv,pickle,re
exec(open('mk_cap.py').read().split("# ---- tabla 1")[0])
res=pickle.load(open('/tmp/cap_months.pkl','rb'))
R={r['mes']:r for r in res}
# publicado
FP=[
 ['H1 2026 (acumulado enero-junio)','SPN base caja',7327029.2,5870835.1,1456194.1,'SRC-0610','Boletín Fiscal 2T26, cuadro I.2.3 (intereses netos = primario menos financiero; coincide con "Intereses Netos 5.870.835,1" del cuadro de la cuenta ahorro-inversión-financiamiento)'],
 ['Abril 2026','SPN base caja',632844.1,'',268102.9,'SRC-0610','Boletín Fiscal 2T26, evolución mensual (el título del cuadro dice "2025"; los totales coinciden con 2026)'],
 ['Mayo 2026','SPN base caja',1924366.9,1445753.7,478613.2,'SRC-0610','Boletín Fiscal 2T26, evolución mensual y cuadro SPN'],
 ['Junio 2026','SPN base caja',-696842.9,'',-1024891.4,'SRC-0610','Boletín Fiscal 2T26, evolución mensual'],
 ['Julio 2026','SPN base caja',2960333,2715436,244897,'SRC-0612','Hacienda, noticia de julio'],
 ['Agosto 2026','SPN base caja',1990322,1354793,635529,'SRC-0611','Hacienda, noticia de agosto'],
]
W(f'{OUT}/resultado_fiscal_publicado.csv',['periodo','perimetro_y_base','resultado_primario_millones_ars','intereses_netos_millones_ars','resultado_financiero_millones_ars','source_id','observacion'],FP)
# capitalización oficial
CO=[['2do trimestre 2026','Administración Central, deuda bruta (ajuste de valuación)',11996722.070,'SRC-0610','Boletín Fiscal 2T26, sección VII.2, flujos del trimestre, "Capitalización de Bonos, Letras y otros préstamos" (US$ 8.675.939 miles)'],
    ['1er semestre 2026','Administración Central, deuda bruta (ajuste de valuación)',24401605.165,'SRC-0610','Boletín Fiscal 2T26, flujos del semestre, misma línea (US$ 17.175.830 miles)']]
W(f'{OUT}/capitalizacion_oficial_flujos.csv',['periodo','perimetro','capitalizacion_millones_ars','source_id','observacion'],CO)
# escenario Jul/Ago
E=[]
pub={'2026-07':(2960333,2715436,244897),'2026-08':(1990322,1354793,635529)}
for mes,(pri,inte,fin) in pub.items():
    r=R[mes]
    for lab,grp in (('solo TEM fija (13 instrumentos, datos del nombre)',['fija']),('TEM fija más flotantes y duales con TEM implícita (supuesto)',['fija','flot'])):
        real=sum(r[f'{g}_interes_pagado_caja_real_al_vto'] for g in grp)/M
        esc=sum(r[f'{g}_interes_caja_escenario_mensual'] for g in grp)/M
        dev=sum(r[f'{g}_devengado_no_pagado'] for g in grp)/M
        E.append([mes,lab,pri,inte,fin,fm(dev),fm(real),fm(esc),fm(esc-real),fm(fin-(esc-real)),fm(inte-real+esc)])
W(f'{OUT}/escenario_interes_en_caja.csv',['mes','cobertura','primario_publicado_millones_ars','intereses_netos_publicados_millones_ars','financiero_publicado_millones_ars','devengado_no_pagado_derivado','interes_real_pagado_al_vto_derivado','interes_escenario_pago_mensual_derivado','diferencia_escenario_menos_real','financiero_ilustrativo_millones_ars','intereses_ilustrativos_millones_ars'],E)
for e in E: print(e)
# ilustración
I=[]
for tem in (0.02,0.025,0.03):
    for n in (6,12,24):
        cap=100*(1+tem)**n; sim=100+100*tem*n
        I.append([f'{tem*100:.1f}',n,fm(cap-100,2),fm(sim-100,2),fm(cap-sim,2),fm((cap-sim)/(sim-100)*100,1)])
W(f'{OUT}/ilustracion_posponer_interes.csv',['tem_pct','meses','interes_acumulado_si_capitaliza_por_100','interes_total_si_se_paga_cada_mes_por_100','interes_sobre_interes_por_100','interes_sobre_interes_pct_del_pago_mensual'],I)
w=sum(r['saldo_ars']*r['tem'] for r in out if r['tipo']=='TEM fija' and r['tem'])/sum(r['saldo_ars'] for r in out if r['tipo']=='TEM fija' and r['tem']); print('TEM ponderada fija',w)
# meses resumen
tot=pickle.load(open('/tmp/cap_tot.pkl','rb'))[0]
print({k:round(v/1e6,1) for k,v in tot.items()})
# top 3 months
for mes in ['2026-07','2026-08','2026-09','2026-12','2027-03']: print(mes,{k:round(v/1e6,1) for k,v in R[mes].items() if k!='mes'})
# fechas explicitas
ev=[]
def dates(txt_year_blocks):
    return txt_year_blocks
L1=[(2026,[(3,31),(4,30),(5,29),(6,30),(7,31),(8,31),(9,30),(10,30),(11,30),(12,30)]),(2027,[(1,29),(2,26),(3,31),(4,30),(5,31),(6,30),(7,30),(8,31),(9,30),(10,29)])]
L2=[(2026,[(4,30),(5,29),(6,30),(7,31),(8,31),(9,30),(10,30),(11,30),(12,30)]),(2027,[(1,29),(2,26),(3,31),(4,30),(5,31),(6,30),(7,30),(8,31),(9,30),(10,29),(11,30),(12,30)]),(2028,[(1,31),(2,29),(3,31),(4,28),(5,31),(6,30),(7,31),(8,31),(9,29),(10,31)])]
rows=[]
for iid,nom,L,src,ref,venc in (('INS-C-0359','BONAR/U$S/6%/29-10-2027',L1,'SRC-0601','Res. Conj. 11/2026 art. 4 (intereses 6% nominal anual, pago mensual vencido, 30/360)',(2027,10,29)),('INS-C-0360','BONAR/U$S/6%/31-10-2028',L2,'SRC-0609','Res. Conj. 16/2026 art. 5 (intereses 6% nominal anual, pago mensual vencido, 30/360)',(2028,10,31))):
    for y,ms in L:
        for m,d in ms:
            fin=(y,m,d)==venc
            rows.append([iid,nom,f'{y}-{m:02d}-{d:02d}','interes',1.0 if fin else '', 'false','1' if fin else '',src,ref])
# columnas: instrument_id,nombre,fecha,tipo_flujo,fraccion_capital(solo amort),... simplificar
rows2=[]
for r in rows:
    rows2.append([r[0],r[1],r[2],'interes_y_capital' if r[4]==1.0 else 'interes',r[4] if r[4]!='' else '',r[7],r[8]])
W('lote_G/contratos/fechas_explicitas.csv',['instrument_id','nombre','fecha','tipo_flujo','fraccion_capital','source_id','referencia'],rows2)
print(len(rows2))
# topes
T=[('INS-C-0443','maximo','SOFR_TERM_1A',0.71513,-1.0,'SRC-0106','hoja D'),('INS-C-0440','maximo','SOFR_TERM_1A',0.71513,-1.0,'SRC-0106','hoja D'),('INS-C-0441','maximo','SOFR_TERM_1A',0.71513,-1.0,'SRC-0106','hoja D'),
('INS-C-0444','maximo','LIBOR_1A','',-1.0,'SRC-0106','hoja D'),('INS-C-0445','maximo','LIBOR_1A','',-1.0,'SRC-0106','hoja D'),
('INS-C-0442','sin_tope_en_la_fuente','','','','SRC-0106','hoja D (solo tasa de reservas, sin tope en la descripción)'),('INS-C-0447','sin_tope_en_la_fuente','','','','SRC-0106','hoja D (solo tasa de reservas, sin tope en la descripción)')]
W('lote_G/contratos/topes_propuesta.csv',['instrument_id','tipo_tope','indice_tope','margen_ajuste_pp','diferencial_pp','source_id','referencia'],T)
