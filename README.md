# Distribuição Ótima de Irrigadores em Áreas Agrícolas

Projeto desenvolvido para a disciplina **Projeto e Análise de Algoritmos** – Universidade Federal do Piauí (UFPI).

## 📌 Descrição

Este trabalho modela o problema de distribuição ótima de irrigadores utilizando **Teoria dos Grafos**, por meio do **Problema do Conjunto Dominante**.

O objetivo é encontrar a menor quantidade de irrigadores necessária para cobrir todas as regiões agrícolas da fazenda.

## 🧠 Modelagem

- Cada região agrícola é representada por um vértice.
- Relações de cobertura são representadas por arestas.
- Busca-se o menor conjunto de vértices capaz de cobrir todos os demais.

## ⚙️ Implementação

Foram implementadas duas abordagens para o problema:

### 1. Baseline por força bruta

Algoritmo exato que:

1. Gera subconjuntos possíveis de regiões usando bitmask.
2. Verifica quais subconjuntos cobrem toda a área.
3. Retorna a menor solução encontrada.

Esse algoritmo garante a solução ótima, mas possui alto custo computacional para instâncias maiores.

### 2. Heurística gulosa

Algoritmo heurístico que:

1. Avalia as regiões candidatas.
2. Escolhe a região com maior ganho de cobertura.
3. Em caso de empate, escolhe a região com menor sobreposição.
4. Aplica pós-processamento para tentar remover irrigadores redundantes.

A heurística não garante a solução ótima, mas busca encontrar soluções próximas ao ótimo em tempo reduzido.

## 📂 Estrutura dos Arquivos

- `irrigadores.py`
- `instancia_5.txt`
- `instancia_10.txt`
- `instancia_15.txt`
- `instancia_20.txt`
- `instancia_25.txt`
- `instancia_30.txt`
- `instancia_35.txt`
- `resultados_heuristica_execucoes.csv`
- `resultados_heuristica_resumo.csv`
- `README.md`

## ▶️ Como Executar

No terminal, execute:

```bash
python .\irrigadores.py
```

Ou:

```bash
python irrigadores.py
```

Depois, escolha uma das opções do menu:

```text
1 - Executar baseline com arquivo .txt
2 - Executar heurística com arquivo .txt
0 - Sair
```

Em seguida, informe o nome da instância desejada, por exemplo:

```text
instancia_5.txt
```

## 👨‍💻 Integrantes

- Bernan Rodrigues do Nascimento
- Danilo Rodrigues Barbosa
- Thiago Rafael Pereira de Carvalho