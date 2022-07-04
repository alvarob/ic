# Projeto de Iniciação Científica

Projeto de iniciação científica pela UFU: Detecção de ataques em rede utilizando Machine Learning

---

Ver os [notebooks](./notebooks) para os resultados até o momento

---

## Changelog

### 04/07/2022

- Adicionado preprocessamento para descartar as linhas com dados "corrompidos"
- Cada um dos 3 modelos anteriores foi treinado com cada arquivo diferente (visto que cada arquivo do datset contém diferentes tipos de ataques)
- Código de avaliação alterado para dar métricas através da matriz de confusão (utilizando funções do `sklearn.metrics`)

Ver os [notebooks](./notebooks) para comentários.

PS: O notebook com resultados da semana anterior foi movido para [notebooks/archive](./notebooks/archive)


### 20/06/2022

Código inicial + resultados iniciais utilizando `Naive Bayes`, `Complement Naive Bayes` e `Hoeffding Tree` (ver notebook para discussão das estratégias de treino/teste)