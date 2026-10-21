# Anexo C. Dados

## C.1 Fontes principais

| Fonte | O que traz | Identificador | Capítulos |
|---|---|---|---|
| SIGADE em 30-06-2026, Oficina Nacional de Crédito Público | Cada operação de dívida da Administração Central | SRC-0102 | 2 |
| Planilha trimestral da dívida, Secretaría de Finanzas | Saldos, fluxos e perfil de vencimentos oficiais | SRC-0103, SRC-1005 | 2, 8 |
| Boletim mensal da Secretaría de Finanzas, série 2019-2026 | Dívida por moeda (A.1, A.3), operações (A.4) e pagamentos por moeda de pagamento (A.5) | SRC-9002 | 2, 3, 5 |
| Dívida da Administração Central por detentor | Setor público, privados e organismos | SRC-1014, SRC-1706 a SRC-1715 | 2, 6 |
| Esquema poupança-investimento-financiamento (AIF), regime de caixa, Secretaría de Hacienda | Receitas, despesas, resultado e financiamento do setor público nacional | lotes AM e AN | 3, 5 |
| Balanço cambial, BCRA | Compras e vendas de divisas por conceito e por setor | SRC-1604 | 2 e 4 |
| Series.xlsm, BCRA | Fatores da base monetária e instrumentos do BCRA | SRC-1625 | 3 |
| Demonstrações contábeis do BCRA de 2023 a 2025 | Juros pagos e recebidos, lucros | SRC-1673 e seguintes | 3, 6 |
| Informe sobre Bancos, BCRA | Resultados do sistema financeiro | lote AJ | 6 |
| Relatórios do corpo técnico do FMI, acordo de 2025 e revisões | Metas e resultados de reservas líquidas, desembolsos | SRC-1263, SRC-1270, SRC-1271, SRC-1611 | 4 |
| Resoluções conjuntas de Finanzas e Hacienda | Recompras, trocas de títulos (canjes) e conversões | SRC-1257, SRC-2031, SRC-2042, SRC-2047, SRC-2063, SRC-2064 | 5, 6 |
| Compras de divisas do Tesouro (relatórios do BCRA e comunicados) | Compras ao BCRA e no mercado | lote AI | 5 |
| Leilões e dívida denominada em dólares paga em pesos | Colocações e pagamentos em pesos de dívida em dólares | lotes AQ e AR | 5, 7 |
| Zips mensais de exportações, ARCA | Valor FOB por posição | SRC-1375 a SRC-1491 | anexo A |
| Arrecadação dos direitos de exportação, datos.gob.ar | Direitos cobrados | lote D | anexo A |
| IPC nacional, INDEC | Deflator dos pesos | SRC-2028 | 3, 5 |
| Comunicación A 3500, BCRA | Taxa de câmbio de referência | `series/bcra_a3500.csv` | todos |

Um lote é uma entrega do agente de busca, guardada na pasta `inbox/lote-…` do repositório com a sua lista de fontes, as suas tabelas e as suas notas. A lista completa de fontes, com URL, data de download e impressão digital sha256, está em `manifests/downloads.csv` e no `sources.csv` de cada lote.

## C.2 Saídas que sustentam o relatório

| Saída | Comando | Arquivo |
|---|---|---|
| Calendário de pagamentos e necessidade de divisas | `argfx calendario` | `data/calendario/` |
| Conciliação, consolidação e posições | `argfx conciliacion` | `data/conciliacion/` |
| Juros capitalizados por trimestre | `argfx devengados` | `data/conciliacion/devengados_trimestral.csv` |
| Diagramas do mandato | `argfx flujos` | `data/informe/flujos_*.csv` e `.html` |
| Direitos estimados e cobrados | `argfx derechos` | `data/simulacion/derechos_*.csv` |
| Modelo da fase 4: o mandato com cobrança em dólares e a projeção até 2036 | `argfx simular` | `data/simulacion/mandato_*` e `proyeccion_*` |
| Gráficos de barras | `argfx graficos` | `data/informe/grafico_*.csv` e `.html` |
| A conta completa dos dólares (capítulo 2.6) | `argfx demanda` | `data/informe/demanda_divisas_observada.csv` e `cuenta_anual_divisas.csv` |
| Projeção do FMI para o saldo comercial | | `series/fmi_balanza_proyectada.csv` (SRC-1263) |
| Projeção do FMI para o balanço de pagamentos | | `series/fmi_cuenta_corriente_proyectada.csv` (SRC-1263) |

Todas as saídas desta versão foram regeneradas em 17 de outubro de 2026 a partir da versão `57a7c62` do repositório.

## C.3 Decisões de método

As decisões do pesquisador estão em `docs/DECISIONES.md`, com data e fundamento. As que mais pesam neste relatório são:

- **D-001.** Reservas líquidas pela definição do acordo com o FMI, sem subtrair os depósitos do Tesouro.
- **D-008.** A análise incorpora as operações posteriores ao corte do SIGADE.
- **D-009.** Os juros também são medidos em regime de competência.
- **D-011.** As letras em garantia do FODER são dívida contingente.
- **D-016.** O relatório trata da natureza bimonetária da dívida; a cobrança em dólares vai para um anexo.
- **D-017.** Cada moeda na sua unidade, gráficos por moeda e glossário.
- **D-018.** As hipóteses da rodada do modelo da fase 4.

## C.4 Como verificar um número

Tudo o que sustenta este relatório é público:

- **O repositório**, com o código, os testes, os manifestos, as tabelas de cada lote, as decisões de método e as mensagens entre os agentes, com todo o histórico: [github.com/alejandroalvaro/argentina-fiscalidad-divisas](https://github.com/alejandroalvaro/argentina-fiscalidad-divisas)
- **Os documentos originais oficiais**, do jeito que foram baixados, em [datos.8kgm.com.br](https://datos.8kgm.com.br). Cada original está em `objects/sha256/` seguido da sua impressão digital. A tabela `manifests/publicacion.csv` informa, para cada código SRC, o emissor, a URL de origem, a impressão digital e o endereço público.
- **Os documentos de terceiros** (notas de imprensa, trabalhos acadêmicos, relatórios de câmaras privadas e cópias de textos oficiais hospedadas em sites de terceiros), 140 de 1.214, não são reproduzidos porque os direitos pertencem aos seus autores. A mesma tabela informa a URL de origem e a impressão digital, para que quem os baixar possa conferir que se trata do mesmo arquivo.

Para conferir um original, basta baixá-lo e calcular a sua impressão digital (`shasum -a 256 archivo` no macOS ou no Linux, `certutil -hashfile archivo SHA256` no Windows): ela precisa coincidir com o nome do objeto. Para refazer um cálculo, o repositório explica como instalar o código e qual comando produz cada saída (seção C.2).

O código é distribuído sob a licença MIT, e os textos e as tabelas próprias, sob a licença Creative Commons Atribuição 4.0 (CC BY 4.0). Os documentos originais continuam pertencendo aos seus emissores.
