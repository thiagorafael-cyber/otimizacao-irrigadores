# 💧 Otimização de Alocação de Irrigadores (Set Cover Problem)

Este repositório contém a solução algorítmica para um problema clássico de otimização combinatória: encontrar a alocação mínima de irrigadores numa fazenda subdividida em parcelas, garantindo cobertura total de água. O problema foi modelado utilizando os princípios da **Teoria dos Grafos**.

## 🧠 Abordagem Técnica

O problema de cobertura de parcelas é análogo ao problema do **Conjunto Dominante** (*Dominating Set*) ou **Cobertura de Conjuntos** (*Set Cover*). Para garantir a descoberta da solução matemática ótima (o número mínimo absoluto de equipamentos), foi implementado um algoritmo exaustivo (**Força-Bruta**).

### Principais Características da Implementação:
* **Matriz de Adjacência:** Estrutura de dados escolhida para representar o mapa físico da fazenda, permitindo consultas de vizinhança em tempo constante $O(1)$.
* **Operações Bit a Bit (Bitwise):** Geração de subconjuntos otimizada utilizando deslocamento de bits (`<<`) e operadores lógicos (`&`), dispensando o uso de bibliotecas de alto nível e reduzindo o *overhead* da CPU.
* **Poda de Busca:** O algoritmo descarta instantaneamente combinações de tamanho igual ou superior à melhor solução já encontrada, poupando milhões de ciclos de processamento.

## ⚙️ Como Executar o Projeto

**Pré-requisitos:**
* Python 3.x instalado na máquina.

**Passo a passo:**
1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
