---
title: "Blanchard Cap 11: Poupança, acumulação de capital e produto"
author: "Mariano Laplane"
date: "11/03/2020"
tags:
- "Notas de Aula"
- "Macroeconomia"
categories:
- "PED"
- "Macroeconomia III"

---

# Introdução

Blanchard abre o capítulo questionando se existe uma relação entre taxa de poupança e **taxa de crescimento**. Argumenta que é só um efeito nível, mas que isso altera o **padrão de vida**.

# Interações entre produto e capital

Em linhas gerais as interações são:

- Capital determina o produto

$$
K \Rightarrow Y
$$

- Produto determina a poupança que determina o capital acumulado

$$
Y \Rightarrow S \Rightarrow K 
$$

## Efeitos do capital sobre o produto

Retomando a função de produção agregada do capítulo anterior, bem como a hipótese de rendimentos decrescentes dos fatores e normalizando pelos trabalhadores:
$$
\frac{Y}{N} = F\left(\frac{K}{N}, 1\right) \sim \frac{Y_t}{N} = f\left(\frac{K_t}{N}\right)
$$
Em seguida, explicita mais duas hipóteses:

- Tamanho da população, a taxa de atividade e de desemprego são constantes

$$
N = \overline N
$$

​	**Consequência:** O estoque de capital é o único fator de produção que varia no tempo

- Não há **progresso tecnológico**

## Efeitos do produto sobre a acumulação de capital

### Produto e investimento

Nesta seção, adiciona outras hipóteses:

- Economia fechada
- Com governo, mas o orçamento é equilibrado ($G = T$)

Com essas hipóteses em mãos,
$$
I \equiv S_p
$$
A seguir, assume que a poupança (privada) é proporcional à renda
$$
S = \overline s\cdot Y
$$
Combinando com a identidade anterior:
$$
I_t = s\cdot Y_t
$$

### Investimento e acumulação de capital

Seja $\delta$ a parcela do capital que deprecia,
$$
K_{t+1} = \underbrace{(1-\delta)K_t}_{\text{N. Deprecia}} + \underbrace{I_t}_{\text{Novo}}
$$
Rearranjando,
$$
\Delta K = I_t - \delta\cdot K_{t-1}
$$
normalizando pelo trabalho e substituindo a relação obtida na seção anterior
$$
\frac{\Delta K}{N} = s\cdot \frac{Y}{N} - \delta\cdot \frac{K_{t-1}}{N}
$$
Outra forma de visualizar é dividindo ambos os lados da equação pelo estoque de capital no período anterior para obter a taxa de acumulação ($g_K$), bem como a taxa de acumulação líquida de depreciação ($g'_k$):
$$
\frac{\Delta K}{K_{t-1}} = \frac{I}{K_{t-1}} - \delta
\label{Solow}
$$

$$
g'_k = g_k - \delta
$$

Haverá acumulação líquida de capital sempre que
$$
g_k > \delta
$$

## Implicações de taxas de poupança diferentes

### Dinâmica do capital e do produto

Nesta seção, Blanchard investiga o significado e a dinâmica da equação $\ref{solow}$. Pode ser resumido nos seguintes termos:

- O capital por trabalhador determina o produto por trabalhador. Este último, por sua vez, determina a poupança por trabalhador e, consequentemente, o investimento
- Haverá uma mudança positiva no capital por trabalhador se o investimento por trabalhador superar a depreciação por trabalhador
  - Esta depreciação aumenta proporcionalmente com o capital por trabalhador
- A função do investimento por trabalhador possui o mesmo formato que o produto por trabalhador
- O *steady state* é aquele que mantém o capital por trabalhador constante

![image-20200310153307504](/dados/PhD/Materias/1S2020/PED_CE572A/Aulas/Aula_03/image-20200310153307504.png)

### Capital e produto no estado estacionário

Como destacado anteriormente, estado estacionário é definido como aquele momento econômico em que o capital por trabalhador se mantém constante:
$$
s\cdot f\left(\frac{K^*}{N}\right) = \delta\cdot \left(\frac{K^*}{N}\right)
$$

## Taxa de poupança e produto

Ao longo desta seção, Blanchard argumenta que a taxa de produto por trabalhador não possui nenhum efeito **taxa** sobre o produto no estado estacionário

- Isso significa que possui apenas um efeito nível, ou seja, o nível do produto por trabalhador é menor, mas a taxa de acumulação se mantém a mesma
- **Memo:** Rendimentos decrescentes dos fatores. Seria necessário poupar a uma taxa cada vez maior (ano a ano!) para afetar persistentemente a acumulação. Sendo assim, é impossível manter uma taxa de capital por trabalhador crescendo a uma taxa constante ao longo do tempo.

Dito isso, avança em direção para explicar qual seria o determinante do crescimento no longo prazo: **progresso tecnológico**. Resumidamente, afirma que uma economia que possui progresso tecnológico apresenta uma taxa de crescimento do produto por trabalhador constante (inclusive no longo prazo).

<img src="/dados/PhD/Materias/1S2020/PED_CE572A/Aulas/Aula_03/image-20200310173130988.png" alt="image-20200310173130988" style="zoom:50%;" />

## Taxa de poupança e consumo

Blanchard inicia a seção discutindo como o governo pode impactar a taxa de poupança e questiona se um aumento nesta taxa implica **necessariamente** em um aumento no consumo. A resposta pode ser vista em dois casos extremos:

- $s=1$: Significa **consumo** igual à zero no longo prazo
- $s=0$: Significa **produto** igual à zero no longo prazo, logo, consumo também é nulo.
  - Montante excessivo de capital

Dito isso, apresenta o conceito de **regra de ouro**: taxa de poupança ($s_g$) que maximiza o consumo por trabalhador no <u>estado estacionário</u>:

- $s < s_g$: um aumento na taxa de poupança significa um **aumento** no consumo por trabalhador até se alcançar $s_g$
- $s > s_g$: um aumento na taxa de poupança significa uma **diminuição** no consumo por trabalhador

<img src="/dados/PhD/Materias/1S2020/PED_CE572A/Aulas/Aula_03/image-20200310173814305.png" alt="image-20200310173814305" style="zoom:50%;" />

#  Uma ideia das grandezas

## ANPEC 2004 (Ex 15, adaptado)

Considere uma economia cuja função de produção é dada por $Y = K^{\alpha}\cdot(NA)^{1-{\alpha}}$, em que $Y$, $K$, $N$ e $A$ representam respectivamente o produto, o estoque de capital, o número de trabalhadores e o estado da tecnologia. Por sua vez, a taxa de poupança é igual a 20%, a taxa de depreciação é igual a 5%, a taxa de crescimento do número de trabalhadores é igual a 2.5% e a taxa de crescimento tecnológico é igual a 2.5%. Calcule o valor do capital por trabalhador efetivo no estado estacionário

**Modificações:**

- $g_N = 0$
- $A=1$ e $g_A = 0$
- $\alpha = \frac{1}{2}$

**Do enunciado:**

- $s = 0.2$
- $\delta = 0.05$

## Resolução

==**Dica:** Substituir valores por último.==

Reescrevendo a função de produção em termos do número de trabalhadores
$$
Y = K^{\alpha}\cdot N^{1-\alpha} \hspace{4cm} \div N
$$

$$
\frac{Y}{N} = K^{\alpha}\cdot \frac{N^{1-\alpha}}{N}
$$

$$
\frac{Y}{N} = K^{\alpha}\cdot (N^{1-\alpha}\cdot N^{-1})
$$

$$
\frac{Y}{N} = K^{\alpha}\cdot (N^{-\alpha})
$$

$$
\frac{Y}{N} = \frac{K^{\alpha}}{N^{\alpha}} = \left(\frac{K}{N}\right)^{\alpha}
$$

Retomando a identidade entre poupança e investimento, temos
$$
I = s\cdot Y
$$
Lembrando que o estado estacionário é definido por:
$$
I = \delta K
$$
normalizado pelos trabalhadores
$$
\frac{I}{N} = \delta\cdot \frac{K}{N}
$$
Substituindo,
$$
s\cdot\frac{Y}{N} = \delta\cdot \frac{K}{N}
$$
Por fim, substituindo pela função de produção encontrada anteriormente:
$$
s\cdot\left(\frac{K}{N}\right)^{\alpha} = \delta\cdot \frac{K}{N}
$$
reescrevendo
$$
\frac{K}{N} = \frac{s}{\delta}\left(\frac{K}{N}\right)^{\alpha}
$$
resolvendo para $K/N$
$$
\frac{\frac{K}{N}}{\left(\frac{K}{N}\right)^{\alpha}} = \frac{s}{\delta}
$$

$$
\left(\frac{K}{N}\right)^{1-\alpha} = \left(\frac{s}{\delta}\right)^{1}
$$

$$
\left(\frac{K}{N}\right)^{\frac{1-\alpha}{1-\alpha}} = \left(\frac{s}{\delta}\right)^{\frac{1}{1-\alpha}}
$$

$$
\left(\frac{K}{N}\right)^{*} = \left(\frac{s}{\delta}\right)^{\frac{1}{1-\alpha}}
$$

Finalmente, substituindo os valores
$$
\left(\frac{K}{N}\right)^* = \left(\frac{0.20}{0.05}\right)^{\frac{1}{1/2}}
$$

$$
\left(\frac{K}{N}\right)^* = \left(\frac{1/5}{1/20}\right)^{2}
$$

$$
\left(\frac{K}{N}\right)^* = \left(\frac{20}{5}\right)^{2}
$$

$$
\left(\frac{K}{N}\right)^* = \left(4\right)^{2}
$$

$$
\left(\frac{K}{N}\right)^* = 16
$$

### Qual seria o valor do produto por trabalhador?

Da função de produção, temos
$$
\frac{Y^*}{N} = \left(\frac{K^*}{N}\right)^{\alpha}
$$
basta substituir o resultado anterior
$$
\frac{Y^*}{N} = (16)^{1/2} = \sqrt{16} = 4
$$

### E qual seria a taxa de poupança equivalente à regra de ouro?

No estado estacionário, o consumo por trabalhador é dado pela renda líquida da depreciação. Em outras palavras, ao valor que é superior para manter um nível de capital constante:
$$
\frac{C}{N} = \frac{Y}{N} - s\cdot \frac{Y}{N}
$$

$$
\frac{C}{N} = \frac{Y}{N} - \delta\cdot \frac{K}{N}
$$

$$
\frac{C}{N} = (1-s)\cdot \frac{Y}{N}
$$

$$
\frac{C}{N} = (1-s)\cdot \left(\frac{K}{N}\right)^{\alpha}
$$

$$
\frac{C}{N} = (1-s)\cdot \left(\frac{s}{\delta}\right)^{\frac{\alpha}{1-\alpha}}
$$

Para $\alpha = 1/2$
$$
\frac{C}{N} = \frac{(1-s)\cdot s}{\delta}
$$
qual seria a taxa de poupança compatível com a regra de ouro?
$$
s_g = \frac{\partial C/N}{\partial s} = 0
$$
pela regra da cadeia
$$
\frac{\partial C/N}{\partial s} = \frac{1}{\delta}\left(-1\cdot s + (1-s)\right)
$$

$$
\frac{1}{\delta}\left(1-2\cdot s\right) = 0
$$

como o valor de $\delta$ não faz com que essa equação seja igual à zero (apenas que tenda à zero quando tende ao infinito), basta avaliar o valor de $s$
$$
1 - 2\cdot s = 0
$$

$$
\therefore s_g = \frac{1}{2} > s
$$

Logo, a taxa de poupança desta economia hipotética não é igual à regra de ouro e, portanto, não maximiza o consumo por trabalhador.

### O que aconteceria com um aumento de $s$ para além de $s_g$?

$$
\frac{\partial^2 C/N}{\partial s^2} = \frac{1}{\delta}\frac{\partial (1-2\cdot s)}{\partial s}
$$

$$
\frac{\partial^2 C/N}{\partial s^2} = -\frac{2}{\delta} < 0
$$

Portanto, o consumo irá diminuir.

# Capital físico versus capital humano

## Ampliando a função de produção

Resumidamente, amplia-se a função de produção da seguinte forma
$$
\frac{Y}{N} = f\left(\frac{K}{N}, \frac{H}{N}\right)
$$
em que $H/N$ é o nível de qualificação médio.

## Capital humano, capital físico e produto

Em linhas gerais, nessa seção Blanchard destaca que os resultados sobre a acumulação do capital físico não só se preservam, mas se estendem para o caso com capital humano.

## Crescimento endógeno

Reposiciona a conclusão anterior. Resumidamente, afirma que mudanças na taxa de poupança alteram o **nível** e não a taxa de crescimento do produto por trabalhador. No entanto, nos modelos de **crescimento endógeno** a taxa de poupança e a taxa de gastos em educação afetam a taxa de crescimento de *steady state* mesmo **sem** progresso tecnológico.

# Observações e comentários

- [ ] **Provocação:** Seguindo o PDE (*à la* Possas), o consumo ou a poupança é residual?

- [ ] Enfatizar a diferença entre efeito nível e efeito taxa

  - Destacar que o efeito nível altera a taxa **em média**

- [ ] Destacar a igualdade entre propensão marginal e média a poupar

  - Propensão marginal é um parâmetro (e exógena)
  - Propensão média só é idêntica na ausência de $Z$
  - Havendo tempo, relacionar com distribuição de renda. Supondo uma economia fechada, sem governo, sem gastos autônomos não criadores de capacidade produtiva ao setor privado. Além disso, separando entre trabalhadores e capitalistas e considerando que os primeiros gastam o que ganham enquanto os segundos ganham o que gastam

  $$
  Y = C + I
  $$

  $$
  S = Y - C
  $$

  $$
  C = C_w + C_k
  $$

  $$
  C_w = W \hspace{3cm} \omega = \overline \omega
  $$

  Supondo que todo o consumo é induzido pela renda,
  $$
  C = \overline \omega\cdot c_w\cdot Y + (1-\overline \omega)\cdot c_k\cdot Y
  $$
  mas que a propensão marginal a consumir dos capitalistas a partir da renda é zero ($c_k = 0$) enquanto a dos trabalhadores é igual a um ($c_w = 1$), temos
  $$
  C = \overline\omega\cdot Y
  $$
  logo, 
  $$
  S = Y - C \Rightarrow S = Y - \overline \omega\cdot Y \Rightarrow S = (1-\overline \omega)\cdot Y
  $$

  $$
  \therefore \frac{S}{Y} = (1-\omega)
  $$

  A relação acima pode ser apresentada de outra maneira. Se $\omega$ é a participação dos salários na renda, a poupança da economia é feita pelos capitalistas a partir dos lucros totais ($FT$):
  $$
  Y = W + FT
  $$

  $$
  (1-\omega) = \frac{FT}{Y}
  $$

  $$
  \therefore FT = (1-\omega)\cdot Y
  $$

  Assim como o consumo total da economia, a poupança é dada pela média ponderada pela propensão marginal a poupar de cada uma das classes.
  $$
  s = s_w\cdot \omega + s_k\cdot (1-\omega)
  $$

  $$
  s_w = 1 - c_w = 0
  $$

  $$
  s_k = 1 - c_k = 1
  $$

  $$
  \therefore S = s\cdot Y \Leftrightarrow S = (1-\omega)\cdot Y
  $$

  

## PIB privado e PIB público

Retomando aos princípios **básicos** de contabilidade social. O PIB pela ótica da demanda é dado por:
$$
Y = C + I + G + (X-M)
$$
Desmembrando um pouco
$$
I = I_p + I_g
$$
A “definição” de “PIB” público:
$$
Y_g = I_g + G
$$
enquanto o PIB privado é dado por
$$
Y_p = Y - Y_g
$$
Desmembrando mais ainda:
$$
G = \text{saúde } + \text{educação } + \text{previdência } + \ldots
$$

- Uma epidemia aumenta os gastos com serviços de saúde e, portanto, aumenta o “PIB público”. Isso é uma boa notícia?
- Onde são contabilizados os gastos com transferência de renda? Na renda disponível/consumo das famílias e não nos gastos do governo!
- Outro problema: essa divisão não possui um equivalente na ótica da oferta
  - Quem produz o bem de capital contabilizado como investimento público é o setor privado

### Saldos financeiros

Vamos partir do caso de uma economia fechada com governo:
$$
Y \equiv C + I + G
$$
Descontando os impostos de ambos os lados da equação preserva a identidade
$$
\underbrace{Y - T}_{YD} \equiv C + I + G - T
$$
Desagregando o investimento
$$
I = I_p + I_g
$$
e agrupando
$$
YD = (\overbrace{C + I_p}^{Y_p}) + (\overbrace{G + I_g}^{Y_g} - T)
$$
Passando tudo para o lado esquerdo
$$
(YD - C - I_p) + (T - G - I_g) \equiv 0
$$
Seja $S_p$ a poupança privada e $S_g$ a poupança do setor público 
$$
S_p = YD - C
$$

$$
S_g = T - G
$$

rearranjando:
$$
(S_p - I_p) + (S_g - I_g) \equiv 0
$$
Este é o conceito de saldo financeiro líquido tão comum na metodologia SFC:
$$
SFL_p + SFL_g \equiv 0
$$
Podemos estender esta relação para o caso de uma economia aberta também, mas isto é o suficiente para nossos propósitos. O que acontece se o setor privado investe menos do que poupa?
$$
S_p > I_p
$$

$$
SFL_p >0
$$

logo, o setor privado possui uma posição financeira positiva e, portanto, acumulará riqueza (financeira.) Mas e o governo? Para manter a identidade, o setor público necessariamente está em uma posição negativa:
$$
NFL_g \equiv - NFL_p
$$
ou seja, o governo está investindo um valor maior que seu saldo primário
$$
I_g > S_g
$$
Em resumo, não faz sentido distinguir PIB em privado e público se ambos são necessariamente relacionados.

