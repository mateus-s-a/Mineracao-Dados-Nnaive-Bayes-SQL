### O Pedido do Perfil 1:
* `metodo_pagamento` = **Síncrono (Cartão)**
* `proporcao_frete` = **Baixa**
* `prazo_entrega` = **Expresso**
* `historico_cliente` = **Impecável**
* `dispositivo_compra` = **Desktop**
* `horario_compra` = **Comercial**
* `tipo_autenticacao` = **Conta Antiga**

---

### PASSO 1: Probabilidades a Priori $P(\text{Classe})$

Na base de 120 pedidos:
* **Classe `Não` (68 pedidos):** $P(\text{Não}) = \frac{68}{120} = 0.5667 \implies \ln(0.5667) = \mathbf{-0.5680}$
* **Classe `Sim` (52 pedidos):** $P(\text{Sim}) = \frac{52}{120} = 0.4333 \implies \ln(0.4333) = \mathbf{-0.8362}$

---

### PASSO 2: Contagens na Base e Laplace $(\text{contagem} + 1) / (N + 3)$

O SQL conta quantas vezes cada uma das 7 características aparece nos pedidos de treino e aplica a Suavização de Laplace $+1.0$ no numerador e $+3$ no denominador (pois todas as features têm $V_i = 3$ categorias):

#### Para a classe `Sim` (Cancelou — Total $N = 52$):
1. **Cartão:** 8 vezes $\implies \frac{8+1}{52+3} = \frac{9}{55} = 0.1636 \implies \ln = \mathbf{-1.8101}$
2. **Frete Baixo:** 13 vezes $\implies \frac{13+1}{52+3} = \frac{14}{55} = 0.2545 \implies \ln = \mathbf{-1.3683}$
3. **Prazo Expresso:** 12 vezes $\implies \frac{12+1}{52+3} = \frac{13}{55} = 0.2364 \implies \ln = \mathbf{-1.4424}$
4. **Histórico Impecável:** 9 vezes $\implies \frac{9+1}{52+3} = \frac{10}{55} = 0.1818 \implies \ln = \mathbf{-1.7047}$
5. **Desktop:** 8 vezes $\implies \frac{8+1}{52+3} = \frac{9}{55} = 0.1636 \implies \ln = \mathbf{-1.8101}$
6. **Horário Comercial:** 9 vezes $\implies \frac{9+1}{52+3} = \frac{10}{55} = 0.1818 \implies \ln = \mathbf{-1.7047}$
7. **Conta Antiga:** 4 vezes $\implies \frac{4+1}{52+3} = \frac{5}{55} = 0.0909 \implies \ln = \mathbf{-2.3979}$

#### Para a classe `Não` (Não Cancelou — Total $N = 68$):
1. **Cartão:** 35 vezes $\implies \frac{35+1}{68+3} = \frac{36}{71} = 0.5070 \implies \ln = \mathbf{-0.6792}$
2. **Frete Baixo:** 37 vezes $\implies \frac{37+1}{68+3} = \frac{38}{71} = 0.5352 \implies \ln = \mathbf{-0.6251}$
3. **Prazo Expresso:** 31 vezes $\implies \frac{31+1}{68+3} = \frac{32}{71} = 0.4507 \implies \ln = \mathbf{-0.7969}$
4. **Histórico Impecável:** 32 vezes $\implies \frac{32+1}{68+3} = \frac{33}{71} = 0.4648 \implies \ln = \mathbf{-0.7662}$
5. **Desktop:** 26 vezes $\implies \frac{26+1}{68+3} = \frac{27}{71} = 0.3803 \implies \ln = \mathbf{-0.9668}$
6. **Horário Comercial:** 31 vezes $\implies \frac{31+1}{68+3} = \frac{32}{71} = 0.4507 \implies \ln = \mathbf{-0.7969}$
7. **Conta Antiga:** 30 vezes $\implies \frac{30+1}{68+3} = \frac{31}{71} = 0.4366 \implies \ln = \mathbf{-0.8287}$

---

### PASSO 3: Soma dos Logaritmos (Evitando Underflow)

A CTE `Soma_Logs` soma o log priori + os logs das 7 verossimilhanças:

* **Score `Sim`:** $(-0.8362) + (-1.8101) + (-1.3683) + (-1.4424) + (-1.7047) + (-1.8101) + (-1.7047) + (-2.3979) = \mathbf{-13.0745}$
* **Score `Não`:** $(-0.5680) + (-0.6792) + (-0.6251) + (-0.7969) + (-0.7662) + (-0.9668) + (-0.7969) + (-0.8287) = \mathbf{-6.0278}$

> *Note como o score da classe `Não` ($-6.0278$) é muito maior (menos negativo) que o da classe `Sim` ($-13.0745$).*

---

### PASSO 4: Exponenciação $\text{EXP}()$ e Normalização em Porcentagem

1. **Exponenciação para voltar à escala original:**
   * $E_{\text{Sim}} = e^{-13.0745} = \mathbf{0.000002098}$
   * $E_{\text{Não}} = e^{-6.0278} = \mathbf{0.002410710}$
   * **Soma Total:** $0.000002098 + 0.002410710 = \mathbf{0.002412808}$

2. **Normalização em %:**
   * **$P(\text{Não}) =$** $\frac{0.002410710}{0.002412808} \times 100\% = \mathbf{99.91\%}$
   * **$P(\text{Sim}) =$** $\frac{0.000002098}{0.002412808} \times 100\% = \mathbf{0.09\%}$

---

### Resultado Final e Veredito:
* **Classificação:** **`BAIXO RISCO`** ($99.91\%$ de probabilidade de Manter o Pedido).
* **Recomendação Operacional:** Manter o fluxo normal de faturamento do pedido.



<br>
<br>
<br>
⁂
<br>
<br>
<br>



### O Conceito do Log-Odds

O **Log-Odds** responde à seguinte pergunta:
*"Dado que o pedido tem a característica $X$, essa característica empurra o resultado para `Sim` (Cancelou) ou para `Não` (Manteve)?"*

#### A Fórmula do Log-Odds:

$$\text{Log-Odds}(F = v) = \ln \left( \frac{P(F = v \mid \text{Sim})}{P(F = v \mid \text{Não})} \right)$$

#### Como Interpretar o Resultado:
* **Log-Odds Positivo ($> 0$):** A característica **AUMENTA o risco de cancelamento** (`Sim`).
* **Log-Odds Negativo ($< 0$):** A característica **PROTEGE contra o cancelamento** (`Não`).
* **Log-Odds Próximo de Zero ($\approx 0$):** A característica é neutra e não ajuda a decidir.

---

### PASSO A PASSO — Exemplo 1: `tipo_autenticacao = 'Conta Antiga'` (Fator Protetor)

#### Passo 1: Pegar a verossimilhança com Laplace na classe `Sim`
* Na classe `Sim` ($N=52$), apenas 4 pedidos tinham `Conta Antiga`:
  $$P(\text{Conta Antiga} \mid \text{Sim}) = \frac{4 + 1}{52 + 3} = \frac{5}{55} = \mathbf{0.0909}$$

#### Passo 2: Pegar a verossimilhança com Laplace na classe `Não`
* Na classe `Não` ($N=68$), 30 pedidos tinham `Conta Antiga`:
  $$P(\text{Conta Antiga} \mid \text{Não}) = \frac{30 + 1}{68 + 3} = \frac{31}{71} = \mathbf{0.4366}$$

#### Passo 3: Dividir a verossimilhança `Sim` pela verossimilhança `Não` (Razão de Chances)
$$\text{Razão} = \frac{0.0909}{0.4366} = \mathbf{0.2082}$$

#### Passo 4: Aplicar o Logaritmo Natural ($\text{LN}$)
$$\text{Log-Odds} = \ln(0.2082) = \mathbf{-1.5692}$$

> **Conclusão:** Como deu **$-1.5692$ (muito negativo)**, a característica `Conta Antiga` é o **maior fator protetor contra cancelamento de todo o projeto**!

---

### PASSO A PASSO — Exemplo 2: `proporcao_frete = 'Alta'` (Fator de Risco)

#### Passo 1: Verossimilhança na classe `Sim`
* Na classe `Sim` ($N=52$), 29 pedidos tinham `Frete Alto`:
  $$P(\text{Frete Alto} \mid \text{Sim}) = \frac{29 + 1}{52 + 3} = \frac{30}{55} = \mathbf{0.5455}$$

#### Passo 2: Verossimilhança na classe `Não`
* Na classe `Não` ($N=68$), 11 pedidos tinham `Frete Alto`:
  $$P(\text{Frete Alto} \mid \text{Não}) = \frac{11 + 1}{68 + 3} = \frac{12}{71} = \mathbf{0.1690}$$

#### Passo 3: Dividir a verossimilhança `Sim` pela verossimilhança `Não`
$$\text{Razão} = \frac{0.5455}{0.1690} = \mathbf{3.2278}$$

#### Passo 4: Aplicar o Logaritmo Natural ($\text{LN}$)
$$\text{Log-Odds} = \ln(3.2278) = \mathbf{+1.1716}$$

> **Conclusão:** Como deu **$+1.1716$ (alto e positivo)**, ter `Frete Alto` é o **maior indutor de risco de cancelamento do e-commerce**!

---

### Dica para a Apresentação:
Se o professor perguntar por que calculamos os **Log-Odds**, você pode responder:
> *"Calculamos os Log-Odds para quantificar o poder discriminativo de cada variável. Descobrimos que `Conta Antiga` é o maior sinal protetor ($\text{Log-Odds} = -1.5692$) e que `Frete Alto` é o maior causador de desistência ($\text{Log-Odds} = +1.1716$), o que atesta a alta qualidade e explicabilidade do modelo."*