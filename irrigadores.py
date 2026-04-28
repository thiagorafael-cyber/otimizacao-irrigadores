import time

def ler_instancia(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        quantidade_regioes = int(arquivo.readline())

        matriz_adjacencia = []

        for i in range(quantidade_regioes):
            linha = list(map(int, arquivo.readline().split()))
            matriz_adjacencia.append(linha)

    return quantidade_regioes, matriz_adjacencia

def verifica_cobertura(matriz_adjacencia, regioes_com_irrigador, quantidade_regioes):
    regioes_cobertas = [False] * quantidade_regioes

    for regiao in regioes_com_irrigador:
        regioes_cobertas[regiao] = True

        for vizinha in range(quantidade_regioes):
            if matriz_adjacencia[regiao][vizinha] == 1:
                regioes_cobertas[vizinha] = True

    for regiao in range(quantidade_regioes):
        if regioes_cobertas[regiao] == False:
            return False

    return True

def conjunto_dominante_minimo(matriz_adjacencia, quantidade_regioes):
    melhor_solucao = []
    total_subconjuntos = 1 << quantidade_regioes

    for i in range(1, total_subconjuntos):
        regioes_com_irrigador = []

        for j in range(quantidade_regioes):
            if i & (1 << j):
                regioes_com_irrigador.append(j)

        if melhor_solucao != [] and len(regioes_com_irrigador) >= len(melhor_solucao):
            continue

        if verifica_cobertura(matriz_adjacencia, regioes_com_irrigador, quantidade_regioes):
            melhor_solucao = regioes_com_irrigador

    return melhor_solucao

print("===================================================")
print(" DISTRIBUIÇÃO ÓTIMA DE IRRIGADORES")
print(" Problema do Conjunto Dominante")
print("===================================================")

arquivo = input("Digite o nome do arquivo da instância: ").strip()

quantidade_regioes, matriz_adjacencia = ler_instancia(arquivo)

inicio = time.time()

solucao = conjunto_dominante_minimo(matriz_adjacencia, quantidade_regioes)

fim = time.time()

print("\n================ RESULTADO ================")
print("Quantidade de regiões agrícolas:", quantidade_regioes)
print("Número mínimo de irrigadores:", len(solucao))
print("Instalar irrigadores nas regiões:", solucao)
print("Tempo de execução: {:.6f} segundos".format(fim - inicio))
