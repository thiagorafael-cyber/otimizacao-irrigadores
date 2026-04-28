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

Foi desenvolvido um algoritmo baseline exato por **força bruta**, que:

1. Gera todos os subconjuntos possíveis de regiões.
2. Verifica quais subconjuntos cobrem toda a área.
3. Retorna a menor solução encontrada.

## 📂 Estrutura dos Arquivos

- irrigadores.py
- instancia_5.txt
- instancia_10.txt
- instancia_25.txt
- instancia_30.txt
- instancia_31.txt
- README.md

## ▶️ Como Executar

    python irrigadores.py

Depois, informe o nome da instância desejada:

    instancia_5.txt

## 👨‍💻 Integrantes

- Bernan Rodrigues do Nascimento
- Danilo Rodrigues Barbosa
- Thiago Rafael Pereira de Carvalho
