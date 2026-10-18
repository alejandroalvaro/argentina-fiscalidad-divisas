# 7. A opacidade como dado

Reconstruir os dois circuitos deu mais trabalho do que deveria. Este capítulo trata esse esforço como um resultado: o que foi preciso reunir, que séries não existem, que cifras mudam de uma publicação oficial para outra e que erros apareceram em arquivos oficiais. Nenhum desses problemas impede, sozinho, saber quanto o Estado deve. Juntos, eles tornam muito difícil saber em que moeda, a quem e com que recursos se paga.

::: {.destacado custom-style="Destacado"}
**O saldo da dívida é transparente; para reconstruir os seus movimentos, é preciso cruzar publicações que seguem critérios diferentes.**

Entre dezembro de 2023 e agosto de 2026, o esquema poupança-investimento-financiamento (AIF) da Secretaría de Hacienda registra 121.405 milhões de dólares de amortização de dívida "em moeda estrangeira". Desse total, 45.325 milhões eram dívida denominada em dólares que foi paga em pesos. Quem lesse toda essa amortização como pagamento efetivo em divisas superestimaria esses pagamentos, que foram de 76.080 milhões, em cerca de 60%.

*Alcance.* A porcentagem vale para a amortização dessa fonte nessa janela, com os pagamentos efetivos em divisas como denominador, e não se estende ao estoque da dívida. Ela decorre do critério de classificar pela moeda de denominação, que a estatística aplica de maneira coerente, e não supõe nenhuma intenção de ocultar.
:::

## 7.1 O tamanho do trabalho

Para chegar aos diagramas e tabelas deste relatório, foi preciso reunir:

- 1.291 fontes diferentes, em 50 lotes de busca, com 1.404 afirmações registradas;
- 1.214 documentos originais guardados, cada um identificado pela sua impressão digital sha256, e 1.540 downloads registrados;
- mais de 750 operações de dívida no SIGADE e os termos de emissão de 101 instrumentos, carregados à mão a partir de prospectos e resoluções;
- cerca de 640 perguntas que ficaram sem resposta nos registros do que não foi encontrado em cada lote.

O saldo da dívida é transparente: o SIGADE, a planilha trimestral e o perfil de vencimentos batem até o último dólar, uma virtude que nem todos os países têm. A opacidade está nos movimentos, na moeda em que se paga e em quem detém cada título.

## 7.2 Séries que não existem

- **Os depósitos do Tesouro em dólares**, em dólares. O BCRA publica os depósitos do Governo em moeda estrangeira convertidos em pesos. Para saber quantos dólares o Tesouro tem, é preciso reconvertê-los dia a dia.
- **Os depósitos do Tesouro em dólares no Banco Nación.** Não há série.
- **As compras de divisas do Tesouro** separadas por via (ao BCRA, no mercado, em operações em bloco). O BCRA informa em pesos as compras feitas a ele, e as do mercado aparecem em comunicados com cifras que depois mudam.
- **Com que pesos se compra cada dólar.** Não existe um comunicado, compra por compra, que diga se os pesos vieram do superávit, de dívida ou de depósitos.
- **O esquema poupança-investimento-financiamento aberto por instrumento ou por credor.** A amortização e a colocação de dívida saem como totais por moeda, sem dizer o que foi pago.
- **Uma nota metodológica** sobre como se classifica a dívida denominada em dólares que é paga em pesos (dólar linked, BONTE e Letras do Tesouro (LETES) que pagam em pesos, BONAR DUAL). O Manual de Classificações de 2026 não menciona esses instrumentos e traz duas regras escritas que se contradizem.
- **A dívida em pesos, em pesos.** A Secretaría de Finanzas publica a dívida em pesos convertida em dólares.
- **Quem detém cada título.** Não se publica quem tem cada instrumento, nem dentro nem fora do setor público. O FGS publica a sua carteira por categoria, nunca por papel.
- **As LEFI.** Não há série do total emitido nem da parte que ficou no BCRA. A fórmula de capitalização foi publicada como imagem no Boletín Oficial.
- **Os juros que o BCRA paga, mês a mês.** As demonstrações contábeis são anuais e passam por reexpressão.
- **A taxa média do estoque de depósitos a prazo** e o ranking oficial dos fundos de investimento por patrimônio.

## 7.3 Cifras que mudam de uma publicação para outra

| Dado | O que diz cada fonte |
|---|---|
| Recompra de Letras Intransferibles de maio de 2026 | 21.700 milhões de USD (Ministério da Economia); 20.434 ou 22.284 (resoluções); 21.000 (BCRA); 13.225 efetivos (cálculo com a resolução). Pesos usados: $18,4 trilhões (resolução e comunicado) ou $12 trilhões (Informe de Política Monetária de junho de 2026) |
| Variação das reservas líquidas em 2025 | −12.100 milhões (relatório do corpo técnico do FMI) ou −9.600 (carta de intenção, mesmo documento) |
| Compras de divisas do Tesouro em 2025 | 2.727 ou 1.216 milhões, conforme a série do BCRA |
| Compras ao BCRA de janeiro e fevereiro de 2025 | 1.500 milhões que somem do acumulado no relatório de outubro de 2025 |
| Compras de abril de 2024 | 468 milhões no relatório do mês, 2.325 um ano depois |
| Acumulado de compras de 2026 | 6.088 milhões no relatório de julho e 3.335 no de agosto |
| Desembolsos do FMI | 10.729 milhões de DEG (comunicado) ou 10.689 (soma das parcelas do quadro) |
| Juros em moeda estrangeira de outubro de 2024 | 1.242 ou 1.265,7 milhões de USD, conforme a edição do boletim |
| Endividamento em 2025 | AIF mensal: $195,6 trilhões em moeda local e $35,2 trilhões em moeda estrangeira. Cuenta de Inversión: $67,2 e $3,8 trilhões |

Nenhuma dessas diferenças é, em si, um erro. Muitas têm explicação: valor nominal contra valor efetivo, data de contratação contra data de liquidação, critérios diferentes. O problema é que a explicação quase nunca vem publicada, e o leitor precisa reconstruí-la com os documentos originais.

## 7.4 O que se chama de "moeda estrangeira"

O caso mais importante para este relatório é a classificação da dívida por moeda no esquema poupança-investimento-financiamento da Secretaría de Hacienda. Entre dezembro de 2023 e agosto de 2026, a amortização de dívida "em moeda estrangeira" desse esquema soma 121.405 milhões de dólares. Desse total, 45.325 milhões eram dívida denominada em dólares que foi paga em pesos, de modo que o que se pagou em dólares foi 76.080 milhões. Do lado da colocação acontece o mesmo: de 83.563 milhões "em moeda estrangeira", 19.413 foram colocados por pesos e 64.150 entraram em dólares.

Além disso, o critério muda de uma publicação para outra:

- a Cuenta de Inversión 2024 conta o BONTE dólar linked como colocação em moeda estrangeira, e a de 2025 não;
- até 2025, a Oficina Nacional de Crédito Público classificava como moeda estrangeira os BONTE em dólares que pagam em pesos e como moeda nacional as letras atreladas ao dólar (LELINK); em 2026 passou a classificar pela moeda de pagamento e levou os BONTE para moeda nacional;
- o boletim da Secretaría de Finanzas conta a dívida dólar linked como moeda local no quadro A.3 e como moeda estrangeira no A.1;
- o quadro A.4 do boletim inclui trocas de títulos (canjes) sem movimento de caixa: a RC 16/2024 baixou BONAR DUAL e BONTE em dólares por 25.173 milhões que o esquema poupança-investimento-financiamento não mostra.

Um leitor que queira saber de quantos dólares o Tesouro precisou e leia toda a amortização "em moeda estrangeira" como pagamento em divisas vai superestimá-los em cerca de 60% (121.405 contra 76.080 milhões, entre dezembro de 2023 e agosto de 2026). Classificar pela moeda de denominação é um critério estatístico legítimo. O problema é que a classificação pela moeda de pagamento não sai publicada ao lado. Para corrigir isso, o relatório teve de reconstruir a dívida paga em pesos operação por operação, a partir dos leilões e das resoluções.

## 7.5 Erros em arquivos oficiais e operações sem explicação

- **A estrutura financeira da Oficina Nacional de Crédito Público** repete no Global 2035 a amortização do Global 2030.
- **O perfil oficial de vencimentos** subestima o principal a doze meses em 32.900 milhões de dólares, sobretudo porque deixa de fora o que foi emitido depois da data de corte (capítulo 2).
- **As letras em garantia do FODER** aparecem no SIGADE como dívida comum, com um cronograma mecânico de 266 milhões por ano, quando são dívida contingente.
- **Três letras em pesos** (TMF27, TMG27 e TZX27) têm o saldo reduzido sem nenhuma operação publicada que explique a queda.
- **A RC 60/2026** nunca publicou os seus valores.
- **A RC 30/2026** autorizou um pagamento de 1.040 milhões de dólares que não aparece nos depósitos do Tesouro.
- **Os arquivos de exportações da Agencia de Recaudación y Control Aduanero (ARCA)** trazem 81 registros com preços impossíveis. Em fevereiro de 2021, por exemplo, a soja em grão (1201.90.00) aparece com 6.508 milhões de dólares FOB para 37.325 toneladas, ou 174 dólares por quilo, contra uma mediana de 0,41. O relatório separa esses registros com um filtro de valor unitário e os lista.

## 7.6 Atrasos e portais

- **O SIGADE** de 30 de junho de 2026 foi publicado em 18 de setembro, uns 80 dias depois. Nesse intervalo, os leilões quinzenais mudam cerca de 36.000 milhões de dólares do principal a doze meses. O corte de 30 de setembro ainda não estava publicado em 17 de outubro.
- **A ANSES** bloqueia o download automático dos relatórios do FGS, e vários relatórios de 2023 e 2024 dão erro 404.
- **O FMI** bloqueia o download automático dos seus relatórios; foram usadas as cópias que o BCRA publica.
- **O BCRA** devolveu erros 502 seguidos para o Informe sobre Bancos de agosto de 2026, e alguns caminhos de arquivo mudam sem aviso.
- **A câmara dos fundos de investimento (CAFCI)** e o portal de dados do Ministério da Agricultura recusam o download automático.
- **A interface de séries do datos.gob.ar** perde observações ao acaso. É preciso usar os arquivos estáticos.

## 7.7 Os erros próprios

O método também detectou erros dos agentes que fizeram este trabalho, e vale contá-los porque mostram como é fácil errar com essas fontes:

- uma tabela de fatores da base monetária preparada num lote estava errada em 27 de 45 meses, porque somava o bloco anual da planilha ao mês de janeiro;
- uma cifra de juros que estava em bilhões de pesos foi lida como se fosse em dólares;
- supôs-se que duas recompras de Letras Intransferibles tinham sido pagas com pesos, quando foram pagas com dólares do FMI e com dólares que o BCRA entregou por BOPREAL;
- inferiu-se que a colocação de dívida em dólares por pesos era registrada como moeda local, e os dados dos leilões mostraram o contrário;
- no segundo rascunho, o total das compras de dólares do Tesouro vinha do relatório mensal do BCRA e a abertura por via, da série diária. As duas não somam o mesmo, porque o relatório mensal omite uma compra de 787 milhões ao BCRA em 5 de fevereiro de 2026. O terceiro rascunho usa uma série só, o relatório mensal, com essa compra acrescentada (capítulo 5);
- no mesmo rascunho, 16.703 milhões de dólares apareciam como valor nominal da dívida com o BCRA quitada com pesos. Esse é o equivalente em dólares do que se pagou; o valor nominal foi de 28.030 milhões.

Cada erro foi corrigido com base no documento original. À medida que as correções entraram, a diferença sem explicação do Tesouro em dólares caiu de −18.221 para −4.150 e depois para −3.522 milhões, e subiu para −4.309 quando se acrescentou a compra de fevereiro de 2026. Isso acontece porque essa compra fecha o mês em que ocorreu, e a soma de todos os meses, que compensa erros de sinal contrário, fica maior.

## 7.8 O que faltaria

A lista sai sozinha do que veio antes. Bastaria que a Secretaría de Finanzas publicasse a dívida em pesos em pesos e a posse dos títulos por setor e por instrumento; que a Secretaría de Hacienda abrisse a amortização e a colocação por instrumento e por moeda de pagamento, com uma nota de método; que o BCRA publicasse os depósitos do Tesouro em dólares em dólares e as compras do Tesouro por via; e que as operações entre o Tesouro e o BCRA fossem informadas com a sua contrapartida e o seu preço. Quase tudo isso já existe dentro da administração, porque sem esses dados não seria possível fazer os registros que de fato são publicados.
