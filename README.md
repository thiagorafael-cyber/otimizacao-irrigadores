# Otimização de Alocação de Irrigadores

Este repositório contém a solução algorítmica para um problema clássico de otimização combinatória: encontrar a alocação mínima de irrigadores numa fazenda subdividida em parcelas, garantindo cobertura total de água. O problema foi modelado utilizando os princípios da **Teoria dos Grafos**.

## Abordagem Técnica

O problema de cobertura de parcelas é análogo ao problema do **Conjunto Dominante** (*Dominating Set*). Para garantir a descoberta da solução matemática ótima (o número mínimo absoluto de equipamentos), foi implementado um algoritmo exaustivo (**Força-Bruta**).

### Principais Características da Implementação:
* **Matriz de Adjacência:** Estrutura de dados escolhida para representar o mapa físico da fazenda, permitindo consultas de vizinhança em tempo constante O(1).
* **Operações Bit a Bit (Bitwise):** Geração de subconjuntos otimizada utilizando deslocamento de bits (`<<`) e operadores lógicos (`&`), dispensando o uso de bibliotecas de alto nível e reduzindo o *overhead* da CPU.
* **Poda de Busca:** O algoritmo descarta instantaneamente combinações de tamanho igual ou superior à melhor solução já encontrada, poupando milhões de ciclos de processamento.

## Como Executar o Projeto

**Pré-requisitos:**
* Python 3.x instalado na máquina.

**Passo a passo:**
1. Clone este repositório:
   ```bash
   [git clone https://github.com/thiagorafael-cyber/otimizacao-irrigadores.git](https://github.com/thiagorafael-cyber/otimizacao-irrigadores.git)
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd NOME_DO_REPOSITORIO
   ```
3. Execute o script principal:
   ```bash
   python irrigadores.py
   ```

## 📁 Estrutura dos Ficheiros de Instância (.txt)

O programa consome ficheiros de texto simples como *input*. A primeira linha define o número total de parcelas (N) e as linhas seguintes representam a matriz de adjacência (conexões/alcance da água).

Exemplo (`instancia_5.txt`):
```text
5
0 1 1 1 0
1 0 0 0 0
1 0 0 0 0
1 0 0 0 1
0 0 0 1 0
```
*Para testar cenários maiores, basta alterar a variável `arquivo_teste` no ficheiro `irrigadores.py` para apontar para `instancia_10.txt`, `instancia_20.txt`, etc.*

## ⏱️ Complexidade e Benchmarking

Por se tratar de uma solução exaustiva para um problema NP-Completo, a complexidade de tempo é **O(2^n)**. 
Durante os testes de *benchmarking*, o algoritmo resolveu instâncias de N=10 instantaneamente (menos de 1 milissegundo). Para instâncias de N=25 (mais de 33 milhões de combinações), o tempo de execução foi de aproximadamente 27 segundos. O limite prático computacional da máquina de testes foi atingido em instâncias próximas a N=30.

---
*Projeto desenvolvido para fins académicos.*
