# Documentação do diálogo com a IA - Etapa 1: Escolha do domínio e modelagem do problema

**Disciplina:** Mineração de Dados  
**Atividade:** ATIVIDADE PRÁTICA 1 — Algoritmo Classificador Bayesiano  
**Responsável:** Mateus de Souza Arruda & Lorena Strobel Campos  
**Data:** 23/08/2026  

---

1. Qual é o rótulo alvo (o que será classificado como sim ou não)?
2. Quais são as 6 a 8 features mais relevantes para esse domínio?
3. Como cada feature pode ser discretizada em categorias significativas?
4. Qual é a lógica intuitiva por trás dos padrões de risco ou classificação?

## Prompts desenvolvidos para cada uma das perguntas e suas respectivas respostas:

### Prompt pergunta 1:

**Pergunta referente:** Qual é o rótulo alvo (o que será classificado como sim ou não)?

Olá! Estou desenvolvendo uma atividade para a disciplina de mineração de dados sobre o uso do algoritmo de Naive Bayes. O domínio escolhido é o de e-commerce (comércio eletrônico) com o contexto de prever antecipadamente se uma compra realizada em uma plataforma e-commerce será cancelada. O objetivo do sistema é identificar previamente a propensão de cancelamento permitindo assim que a plataforma adote medidas preventivas (como ofertas direcionadas, facilidades de frete ou suporte em tempo real). Com base nesse contexto, ajude-me a definir formalmente o problema de classificação para essa atividade. Responde especificamente cada uma dessas questões:

1. Qual deve ser o rótulo alvo da classificação?
2. Qual será o significado da classe "Sim"?
3. Qual será o significado da classe "Não"?
4. Qual unidade deve ser classificada: o cliente ou o pedido?
5. Qual definição seria mais adequada para uma atividade acadêmica utilizando Naive Bayes e dados discretizados?

Apresente uma proposta objetiva, evitando respostas genéricas. Explique também por que essa definição é adequada ao contexto de e-commerce e ao problema de classificação binária.

#### Resposta do Gemini:

**Definição do Problema de Classificação**
* **Rótulo alvo da classificação:** O rótulo alvo deve ser a Propensão de Cancelamento. Na sua base de dados de treinamento, essa coluna pode ser nomeada como `Risco_Cancelamento` ou simplesmente `Cancelou`.
* **Significado da classe "Sim":** A classe "Sim" indica que o pedido possui padrões históricos semelhantes aos de compras que foram abandonadas, não pagas (como boletos vencidos) ou ativamente canceladas pelo usuário. Esta é a classe crítica que servirá de gatilho para a plataforma acionar medidas preventivas.
* **Significado da classe "Não":** A classe "Não" indica que a transação apresenta um padrão seguro e seguirá o fluxo normal de processamento e faturamento, não exigindo nenhuma intervenção da equipe de retenção ou do sistema.
* **Unidade a ser classificada:** A unidade de análise deve ser o Pedido (a transação no momento do checkout), e não o cliente de forma isolada. Um usuário com ótimo histórico pode cancelar um pedido específico devido a um frete incompatível, uma compra duplicada acidental ou um erro na seleção de voltagem do produto.
* **Adequação para Naive Bayes com dados discretizados:** A melhor abordagem para este trabalho acadêmico é tratar o sistema como um Avaliador de Transações em Tempo Real. Ao focar no pedido, você consegue combinar features do histórico do cliente (ex: "Frequência de compras") com características exclusivas daquela transação (ex: "Meio de pagamento", "Período do dia"), facilitando a conversão de dados contínuos em categorias fechadas para o cálculo de probabilidade.

**Justificativa da Modelagem**
* **Alinhamento com o E-commerce:** Ações de mitigação (oferecer frete grátis, descontos ou abrir um chat de suporte) são aplicadas sobre um carrinho de compras sob risco iminente, e não sobre o perfil estático de um usuário. Focar na unidade "Pedido" torna a sua modelagem acionável para o negócio.
* **Aderência à Classificação Binária:** O problema se reduz a uma decisão mutuamente exclusiva ("Vai Cancelar" vs. "Não Vai Cancelar"). Isso simplifica bastante a implementação da Etapa 3 em SQL, especificamente no cálculo das probabilidades a priori e das log-probabilidades.
* **Maximização da Discretização:** A unidade de pedido oferece atributos mais ricos para serem categorizados (por exemplo, transformar um valor contínuo de carrinho de "R$ 450,00" para a categoria "Alto Valor"), o que é uma exigência fundamental para a criação das tabelas de verossimilhança no Naive Bayes.

---

### Prompt pergunta 2:

**Pergunta referente:** Quais são as 6 a 8 features mais relevantes para esse domínio?

Considerando a definição e o contexto do problema apresentado anteriormente, onde o objetivo é classificar se um pedido de e-commerce será cancelado ou não, preciso selecionar as variáveis de entrada (features) para o modelo Naive Bayes.
Escolha de 6 a 8 features que sejam relevantes, plausíveis e coerentes com o comportamento de cancelamento de pedidos em uma plataforma de comércio eletrônico.

Para cada uma das features, informe:
- nome da feature
- o que ela representa
- por que ela pode influenciar a probabilidade de cancelamento
- se a relação esperada com o cancelamento é direta, indireta ou depende do contexto
- qual a natureza da feature (numérica, categórica, etc.)

Priorize features que possam ser conhecidas antes da ocorrência do cancelamento e que possam contribuir para identificar antecipadamente pedidos com maior ou menor propensão ao cancelamento.
Evite escolher variáveis que sejam muito semelhantes entre si ou que representem praticamente a mesma informação, buscando um conjunto de features diversificado e relevante para o problema.
Ao final, por favor, apresente uma lista final com 6 a 8 features recomendadas e justifique por que esse conjunto é adequado para o problema.

#### Resposta da ia gemini:

Para construir um modelo preditivo robusto, precisamos de um conjunto de variáveis que capturem diferentes ângulos do comportamento de compra. O segredo é misturar dados transacionais, logísticos e comportamentais.

Abaixo, apresento uma proposta de 7 variáveis estratégicas.

**Features Selecionadas para o Modelo**

| Nome da Feature | O que representa | Influência na Probabilidade | Relação Esperada | Natureza Original |
| :--- | :--- | :--- | :--- | :--- |
| **Método de Pagamento** | A forma de pagamento (Boleto, Pix, Cartão de Crédito). | Compras no boleto têm historicamente altas taxas de não pagamento e abandono comparadas ao cartão. | Depende do contexto | Categórica |
| **Proporção do Frete** | O peso do valor do frete no custo total do pedido. | Fretes desproporcionalmente caros causam insatisfação imediata e arrependimento pós-compra. | Direta | Numérica |
| **Prazo de Entrega** | Quantidade de dias úteis até o recebimento. | Prazos muito longos abrem uma janela para o cliente encontrar o produto mais rápido no concorrente. | Direta | Numérica |
| **Histórico do Cliente** | Frequência de cancelamentos passados do usuário. | Identifica padrões comportamentais de clientes que habitualmente compram por impulso e desistem. | Direta | Numérica |
| **Dispositivo de Compra** | Origem do acesso no checkout (Mobile Web, App, Desktop). | Compras móveis tendem a ser mais impulsivas e suscetíveis a interrupções ou desistências. | Indireta | Categórica |
| **Horário da Compra** | Turno em que o pedido foi feito (Madrugada, Horário Comercial, Noite). | Compras de madrugada frequentemente refletem impulsividade ou falta de pesquisa adequada. | Contextual | Categórica |
| **Tipo de Autenticação** | Se a compra foi feita como "Visitante" ou "Logado". | Usuários sem conta criada (visitantes) possuem menor engajamento e compromisso com a loja. | Indireta | Categórica |

**Justificativa do Conjunto**
Este conjunto de 7 features é altamente adequado porque evita redundância ao cobrir quatro dimensões distintas da compra: a financeira (Pagamento e Frete), a logística (Prazo), a tecnológica (Dispositivo) e a comportamental (Histórico, Horário e Autenticação).

Nenhuma dessas variáveis diz a mesma coisa, o que é fundamental para o algoritmo Naive Bayes, que assume que as features são independentes entre si para calcular a probabilidade final.
Além disso, como a sua atividade exige que os dados sejam discretizados em categorias significativas, as variáveis numéricas listadas acima (como Prazo e Histórico) oferecem excelentes oportunidades para a criação de faixas ou "baldes" categóricos (ex: transformar prazos em "Curto", "Médio" e "Longo").

---

### Prompt pergunta 3:

**Pergunta referente:** Como cada feature pode ser discretizada em categorias significativas?

Agora considere as 6 a 8 features selecionadas anteriormente para prever o cancelamento de pedidos em um ambiente de e-commerce.
Preciso definir como cada uma dessas features pode ser dividida em categorias significativas para serem utilizadas posteriormente na construção da massa de dados e no classificador Naive Bayes.

Para cada feature:
1. apresente as categorias possíveis;
2. explique o significado de cada categoria;
3. justifique por que essa divisão é adequada para representar o comportamento relacionado ao cancelamento;
4. para variáveis numéricas, proponha faixas ou categorias qualitativas adequadas, como "baixo", "médio" e "alto", definindo claramente os limites de cada faixa;
5. evite criar categorias excessivamente específicas ou com diferenças pouco relevantes para o problema.

Organize a resposta em uma tabela contendo:
Feature | Tipo original | Categorias propostas | Critério de divisão | Justificativa

Ao final, faça uma breve análise verificando se as categorias propostas são claras, coerentes com o domínio de e-commerce e adequadas para serem utilizadas posteriormente na geração dos dados de treinamento.

#### Resposta da ia:

Para transformar as variáveis selecionadas em um modelo funcional de Naive Bayes, precisamos garantir que cada feature possua um espaço amostral fechado e bem definido. Como exigido na Etapa 1, a discretização em categorias significativas é um passo essencial para o cálculo das probabilidades.

Abaixo está o detalhamento de como organizar essas 7 variáveis em grupos estratégicos.

**Discretização das Features**

| Feature | Tipo original | Categorias propostas | Critério de divisão | Justificativa |
| :--- | :--- | :--- | :--- | :--- |
| **Método de Pagamento** | Categórica | 1. Síncrono<br>2. Assíncrono | Síncrono: Cartão, Pix (aprovação na hora).<br>Assíncrono: Boleto (aprovação futura). | O pagamento assíncrono dá ao cliente uma janela de dias para esquecer ou desistir de pagar o pedido, sendo o maior vetor de cancelamento passivo no e-commerce. |
| **Proporção do Frete** | Numérica | 1. Baixa<br>2. Média<br>3. Alta | Baixa: Frete é <= 10% do total.<br>Média: Frete entre 11% e 25%.<br>Alta: Frete > 25% do total. | Um frete que representa mais de um quarto do preço do produto gera forte dissonância cognitiva. O cliente frequentemente finaliza a compra no impulso, mas a cancela minutos depois ao avaliar o custo-benefício. |
| **Prazo de Entrega** | Numérica | 1. Expresso<br>2. Padrão<br>3. Longo | Expresso: Até 3 dias úteis.<br>Padrão: 4 a 10 dias úteis.<br>Longo: > 10 dias úteis. | Prazos longos de entrega abrem espaço para que o consumidor encontre o produto em uma loja física ou em um concorrente com logística mais ágil, motivando o cancelamento do pedido original. |
| **Histórico do Cliente** | Numérica | 1. Impecável<br>2. Aceitável<br>3. Risco | Impecável: 0% de cancelamentos anteriores.<br>Aceitável: 1% a 20% de cancelamentos.<br>Risco: > 20% de cancelamentos. | O comportamento passado é o melhor preditor do comportamento futuro. Usuários com o hábito frequente de cancelar possuem perfis de consumo voláteis. |
| **Dispositivo de Compra** | Categórica | 1. Desktop<br>2. Mobile App<br>3. Mobile Web | Plataforma usada no momento do checkout. | O Desktop indica um ambiente fixo e focado. O App indica um usuário engajado com a marca. Já o Mobile Web concentra usuários esporádicos, frequentemente suscetíveis a quedas de conexão de quem não possui um plano 4G ativo e depende da troca entre redes Wi-Fi, o que gera interrupções e desistências. |
| **Horário da Compra** | Categórica | 1. Comercial<br>2. Noturno<br>3. Madrugada | Comercial: 08h às 18h.<br>Noturno: 18h às 00h.<br>Madrugada: 00h às 08h. | As compras de madrugada possuem uma correlação direta com a impulsividade. É muito comum a loja registrar o pedido às 3h da manhã e receber o pedido de cancelamento por arrependimento às 9h. |
| **Tipo de Autenticação** | Categórica | 1. Visitante<br>2. Nova Conta<br>3. Conta Antiga | Visitante: Checkout sem login.<br>Nova Conta: Criada há <= 30 dias.<br>Conta Antiga: Criada há > 30 dias. | Clientes sem vínculo direto com a loja (visitantes) sentem menos "peso" ao abandonar ou cancelar uma transação, enquanto contas antigas refletem fidelidade. |

**Análise de Adequação**
As categorias propostas atendem aos requisitos técnicos e de negócio para a construção do classificador:
1. **Clareza e Simplicidade:** Nenhuma variável possui mais do que 3 categorias. Isso evita o espalhamento excessivo dos dados e garante que o seu classificador Naive Bayes terá amostragem suficiente em cada cenário para calcular as verossimilhanças sem zerar probabilidades facilmente.
2. **Coerência com E-commerce:** As lógicas utilizadas (como a distinção vital entre pagamentos síncronos e assíncronos) refletem dinâmicas reais de plataformas de vendas, fugindo de variáveis genéricas e isolando os motivadores psicológicos e logísticos do cancelamento de pedidos.
3. **Vantagem Técnica para o Banco de Dados:** Esta divisão categórica facilitará muito a geração da massa de dados coerente para a Etapa 2. Além disso, como a Etapa 3 exige a implementação do classificador em linguagem SQL, as faixas sugeridas acima traduzem-se nativa e facilmente em estruturas de CASE WHEN para consultas no PostgreSQL, mantendo o seu código limpo e performático durante a extração das agregações.

---

### Prompt para pergunta 4:

**Pergunta referente:** Qual é a lógica intuitiva por trás dos padrões de risco ou classificação?

Considerando o problema de prever se um pedido de e-commerce será cancelado e considerando as features e categorias discretizadas definidas anteriormente, explique a lógica intuitiva por trás dos possíveis padrões de risco.

Quero entender quais combinações de características podem indicar:
* baixo risco de cancelamento;
* risco intermediário ou ambíguo;
* alto risco de cancelamento.

Para cada padrão, explique de forma intuitiva por que aquela combinação de características poderia estar associada ao cancelamento ou à conclusão da compra. Não faça afirmações como se fossem fatos universais ou estatisticamente comprovados. Diferencie claramente:
1. hipóteses intuitivas sobre o comportamento do consumidor;
2. relações que precisariam ser confirmadas pelos dados;
3. situações em que uma feature isoladamente não é suficiente para determinar a classe.

Considere, quando pertinente, que o Naive Bayes trabalha com a hipótese de independência condicional entre as features e explique como essa hipótese pode influenciar a interpretação dos padrões.

Apresente pelo menos três exemplos de perfis de pedido:
* um perfil de baixo risco;
* um perfil de alto risco;
* um perfil ambíguo.

#### Resposta da IA para a pergunta 4:

Abaixo, detalho a lógica dos padrões de risco para a previsão de cancelamentos de e-commerce.

**A Hipótese do Naive Bayes e a Interpretação de Padrões**
O algoritmo Naive Bayes opera sob a hipótese da independência condicional. Isso significa que, matematicamente, ele assume que o impacto do "Horário da Compra" não tem relação direta com o "Dispositivo de Compra", desde que saibamos se o pedido foi cancelado ou não.

Na realidade, sabemos que características podem estar interligadas (ex: navegação na madrugada ocorre mais frequentemente via mobile). Contudo, essa simplificação é o que permite ao Naive Bayes ser rápido e eficiente. Consequentemente, uma feature isolada raramente é suficiente para determinar a classe. O algoritmo empilha (multiplica) as evidências probabilísticas de cada variável independentemente para chegar ao veredito final.

**Diferenciação Crítica**
Antes de definirmos os perfis, é preciso estabelecer que:
* **Hipóteses intuitivas:** Os padrões abaixo são baseados na psicologia do consumidor e na dinâmica padrão do comércio eletrônico. Eles representam o comportamento esperado, mas não são leis universais.
* **Confirmação pelos dados:** O modelo de Naive Bayes é "ingênuo" e só saberá o que você ensinar a ele. As lógicas abaixo precisarão ser confirmadas (ou seja, refletidas estatisticamente) na massa de 100+ registros que você gerará na Etapa 2. Se você criar uma base onde compras de madrugada nunca são canceladas, o modelo aprenderá exatamente isso, ignorando a nossa intuição.

**Exemplos de Perfis de Pedido (Casos de Teste)**

Estes três cenários atendem ao requisito da pergunta 4, fornecendo testes práticos para a sua implementação.

**1. Perfil de Baixo Risco de Cancelamento**
* **Características:** Pagamento Síncrono (Cartão) + Frete Baixo + Prazo Expresso + Conta Antiga + Histórico Impecável + Desktop + Horário Comercial.
* **A Lógica Intuitiva:** Este padrão aponta para uma compra extremamente pragmática, racional e utilitária. O cliente tem um longo relacionamento comercial com a marca (Conta Antiga, Histórico Impecável) e realizou a transação em um ambiente de foco (Desktop, Horário Comercial) – possivelmente comprando algo de que realmente precisa. A logística altamente favorável (Frete Baixo, Prazo Expresso) não gera dúvidas pós-compra, e o comprometimento financeiro imediato (Cartão) sela o pedido.

**2. Perfil de Alto Risco de Cancelamento**
* **Características:** Pagamento Assíncrono (Boleto) + Frete Alto + Prazo Longo + Visitante + Histórico de Risco + Mobile Web + Madrugada.
* **A Lógica Intuitiva:** Este é o cenário clássico de alto atrito e impulsividade. Um usuário sem laços com a loja (Visitante, Mobile Web) decide comprar algo às 3h da manhã. O custo do envio é desproporcional e a entrega vai demorar (Frete Alto, Prazo Longo). Por que ele finalizou o pedido? Porque a fricção era nula: ele escolheu gerar um Boleto. Horas depois, à luz do dia, o arrependimento ou a racionalidade tomam conta, e o cliente simplesmente deixa o boleto vencer, caracterizando um cancelamento passivo.

**3. Perfil de Risco Ambíguo (Intermediário)**
* **Características:** Pagamento Síncrono (Cartão) + Frete Alto + Prazo Padrão + Nova Conta + Histórico Aceitável + Mobile App + Madrugada.
* **A Lógica Intuitiva:** Este perfil emite fortes sinais conflitantes, exigindo que o algoritmo pese o poder discriminativo (log-odds) de cada variável. Por um lado, a compra de madrugada feita por uma conta recente sugere impulsividade. O frete alto também serve como gatilho para a dissonância cognitiva pós-compra. Por outro lado, o cliente instalou o aplicativo da loja (sinal de intenção) e, mais criticamente, comprometeu seu limite de crédito instantaneamente (Cartão). A ambiguidade reside no embate entre a facilidade logística do arrependimento versus o peso da transação financeira já aprovada. O Naive Bayes decidirá a classe com base em qual dessas forças teve maior peso estatístico nos dados de treinamento.