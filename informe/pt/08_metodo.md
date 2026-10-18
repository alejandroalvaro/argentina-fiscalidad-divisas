# 8. Método

Este capítulo descreve como o trabalho foi feito, para que qualquer pessoa possa refazer cada número e julgar os limites dele. O trabalho foi feito com agentes de inteligência artificial sob a direção do pesquisador, em quatro dias de outubro de 2026. O método importa tanto quanto os resultados, porque é ele que permite verificar um trabalho deste volume.

::: {.destacado custom-style="Destacado"}
**Cada número pode ser reconstruído da fonte até o resultado.**

Os mais de 1.200 documentos originais estão guardados com a sua impressão digital sha256, cada cálculo é código com testes automáticos, e o saldo das 753 operações do SIGADE coincide com a planilha oficial sem um dólar de diferença.

*Alcance.* Os fechamentos contábeis, os testes e as impressões digitais verificam coisas diferentes. A impressão digital prova que o documento é o mesmo que foi baixado; o teste automático, que o código faz o que diz; o fechamento contábil, que as contas batem. Nenhum deles garante sozinho que a interpretação econômica esteja correta.
:::

## 8.1 Papéis

- **O pesquisador** define a pergunta, toma as decisões de método e revisa. As decisões estão registradas, com data e fundamento, de D-001 a D-019 (`docs/DECISIONES.md`).
- **Um primeiro modelo (GPT)** desenhou o protocolo de pesquisa e de auditoria (`docs/protocolo/`): a pergunta, as hipóteses, as fontes prioritárias e dez controles pelos quais cada mudança tem que passar.
- **Um agente de busca (Grok)** encontra as fontes e monta lotes: a lista de fontes com a URL oficial, as afirmações com a citação textual e a página, as tabelas extraídas, uma síntese e um registro do que não encontrou. Entrega cada lote num branch do GitHub e não tem acesso ao armazenamento dos originais. Não faz pedidos de acesso à informação pública.
- **Um agente de código (Claude Code)** baixa cada documento da URL oficial, calcula a impressão digital sha256, guarda o arquivo, valida o lote, confere com o original os números que vão ser usados, escreve o código que calcula e só incorpora o lote se ele passar nos testes.

Os dois agentes se comunicaram por escrito, em 134 mensagens guardadas no repositório (`mensajes/`), sem intervenção do pesquisador, a não ser nas decisões de método.

## 8.2 Os originais

Cada documento que sustenta um número é guardado uma única vez, sem modificação, num armazenamento de objetos, com a impressão digital sha256 como nome. Se duas fontes entregam o mesmo arquivo, ele é guardado uma vez. Se uma fonte muda o arquivo, a impressão digital muda e a nova versão é guardada ao lado da antiga. Os manifestos do repositório registram, para cada fonte, a URL, a data do download, o código de resposta, o tamanho e a impressão digital, e se ela coincide com a que o agente de busca calculou.

No fechamento desta versão havia 1.214 originais guardados. Os 1.074 que são documentos oficiais podem ser baixados em https://datos.8kgm.com.br; os outros 140, de terceiros, aparecem com a URL de origem e a impressão digital. O anexo C, seção C.4, explica como verificar cada um. Algumas fontes não puderam ser guardadas porque o portal bloqueia o download automático (ANSES e FMI, capítulo 7); nesses casos se usou a leitura na web, e isso é indicado.

## 8.3 Validação e verificação

Cada lote passa por um validador que revisa os esquemas das tabelas, os identificadores, as referências cruzadas entre fontes, afirmações e instrumentos, e as duplicatas. Um lote que não passa não é incorporado.

A validação não garante que os números estejam corretos, e a rastreabilidade também não. Poder refazer um número a partir da fonte mostra que o cálculo é o que o relatório declara; não mostra que a fonte meça o que o relatório acha que ela mede, nem que a leitura econômica seja a correta. O erro nas compras de dólares do segundo rascunho, por exemplo, era rastreável de ponta a ponta e estava errado mesmo assim: misturava duas séries que medem quase a mesma coisa (capítulo 7). Por isso, além dos testes, cada rascunho passa por uma leitura externa. Para isso, o agente de código confere com o documento original cada número que vai usar num cálculo. Os resultados dessas verificações estão nas mensagens e em `docs/verificaciones/`. As 1.404 afirmações dos lotes continuam marcadas como "sin revisar" (não revisadas) nas suas tabelas, porque a verificação foi feita sobre as que são usadas, e não sobre todas.

## 8.4 Cálculo

Todo cálculo é código, com testes, e nunca texto de um modelo de linguagem. O modelo de linguagem escreve o relatório; ele não calcula.

- **O motor contratual** (fase 2) monta o calendário de pagamentos instrumento por instrumento, com as condições de emissão: cupons, amortizações, capitalização, ajuste por CER com a sua defasagem, taxas TAMAR e BADLAR (a dos depósitos a prazo de mais de um milhão de pesos), duais que pagam o maior de dois ramos. Cada fluxo guarda separadamente a moeda em que está denominado, a indexação, a moeda em que é pago e o detentor.
- **A conciliação** (fase 3) confronta o inventário com a planilha oficial, desconta os pagamentos a órgãos do próprio setor público e reconstrói os juros que são apropriados e não são pagos.
- **Os diagramas de fluxos** do mandato combinam o esquema poupança-investimento-financiamento, o boletim de Finanzas, o balanço cambial e os fatores da base monetária. Cada linha é tomada em termos líquidos na janela, e cada diagrama tem que fechar: o que entra é igual ao que sai, e a diferença que sobra aparece com nome próprio.

Os testes automáticos (88 no fechamento) fixam as propriedades que não podem ser quebradas: que os diagramas fechem, que a dívida dólar linked não conte como necessidade de dólares, que um dado ausente fique vazio. O código só é incorporado se todos passarem.

## 8.5 Regras inegociáveis

- Um dado ausente fica vazio. Nunca é preenchido com zero.
- A moeda em que uma dívida está denominada, a indexação dela, a moeda em que é paga e o detentor ficam em campos separados.
- Os dados observados, os termos contratuais, os cenários e as hipóteses ficam em tabelas separadas.
- As reservas líquidas seguem a definição do acordo com o FMI (D-001).
- O Tesouro, o BCRA e o setor público consolidado são apresentados separadamente, sem contar duas vezes o que uma parte do Estado deve a outra.
- Os pesos são informados em pesos e os dólares em dólares (D-017).
- Cada saída informa a data de corte, a fonte e a versão.

## 8.6 Conciliações que fecham

| Controle | Resultado |
|---|---|
| Saldo do SIGADE contra a planilha de Finanzas em 30-06-2026 | 471.690 milhões de USD nas duas, sem diferença |
| Identidades de fluxos do segundo trimestre de 2026 | Fecham no dólar |
| Perfil oficial de vencimentos em doze meses | Reproduzido nas suas 24 células |
| Calendário do motor contra o perfil oficial | Diferença de 32.913 milhões de principal explicada sem resíduo |
| Mercado de câmbio do mandato | 493.513 milhões de USD de cada lado |
| Tesouro em dólares | Fecha; diferença entre moedas de 4.309 milhões à vista |
| Setor público nacional em pesos | Fecha com $214.000 milhões de arredondamento |
| BCRA em pesos | Fecha exatamente contra a variação da base |
| Lucros do BCRA | Iguais na planilha do BCRA e na de Hacienda ($42,9 trilhões) |

## 8.7 Como reproduzir

O repositório contém o código, os testes, os manifestos e as tabelas pequenas. Os originais estão no armazenamento, identificados pela impressão digital.

```
make install && make check
uv run argfx fetch <sha256> <destino>   # qualquer original pela impressão digital
uv run argfx calendario                 # calendário de pagamentos (capítulo 2)
uv run argfx conciliacion               # consolidação e controles (capítulo 2)
uv run argfx devengados                 # juros capitalizados (capítulo 3)
uv run argfx flujos                     # os quatro diagramas do mandato
uv run argfx derechos                   # direitos de exportação (anexo A)
uv run argfx simular                    # o modelo da fase 4 (anexo A)
uv run argfx graficos                   # os gráficos de barras
python scripts/build_informe.py --docx  # este relatório em HTML e em Word
```

## 8.8 Limites

- A verificação contra o original foi feita sobre os números usados, e não sobre todas as afirmações reunidas.
- Algumas fontes são leituras na web sem impressão digital guardada.
- Há estimativas nossas, identificadas em cada caso: os juros apropriados das LEFI, a parte do TDE25 que o BCRA converteu sem pagamento, a distribuição proporcional da carteira do setor público e as conversões de taxa de câmbio.
- A diferença sem explicação do Tesouro em dólares, 4.309 milhões, é atribuída a descompassos de calendário e de registro, sem que se possa prová-lo mês a mês.
- O estoque é medido em 30 de junho de 2026, com as operações posteriores até 16 de outubro; os fluxos vão até agosto de 2026.
- Os agentes erram. O capítulo 7 lista os erros que a verificação encontrou. Os que ela não encontrou são o principal limite deste trabalho, e a razão para que tudo seja reproduzível.
