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
    
    total_podados = 0
    total_verificados = 0
    total_validos = 0

    for i in range(1, total_subconjuntos):
        regioes_com_irrigador = []

        for j in range(quantidade_regioes):
            if i & (1 << j):
                regioes_com_irrigador.append(j)

        if melhor_solucao != [] and len(regioes_com_irrigador) >= len(melhor_solucao):
            total_podados += 1
            continue

        total_verificados += 1

        if verifica_cobertura(matriz_adjacencia, regioes_com_irrigador, quantidade_regioes):
            total_validos += 1
            melhor_solucao = regioes_com_irrigador            

    estatisticas = {
        "total_podados": total_podados,
        "total_verificados": total_verificados,
        "total_validos": total_validos        
    }

    return melhor_solucao, estatisticas

print("===================================================")
print(" DISTRIBUIÇÃO ÓTIMA DE IRRIGADORES")
print(" Problema do Conjunto Dominante")
print("===================================================")

arquivo = input("Digite o nome do arquivo da instância: ").strip()

quantidade_regioes, matriz_adjacencia = ler_instancia(arquivo)

inicio = time.time()

solucao, estatisticas = conjunto_dominante_minimo(matriz_adjacencia, quantidade_regioes)

fim = time.time()

print("\n================ RESULTADO ================")
print("Quantidade de regiões agrícolas:", quantidade_regioes)
print("Número mínimo de irrigadores:", len(solucao))
print("Instalar irrigadores nas regiões:", solucao)
print("Tempo de execução: {:.6f} segundos".format(fim - inicio))

print("\n========== ESTATÍSTICAS ==========")
print("Espaço de busca total:", (1 << quantidade_regioes) - 1)
print("Subconjuntos descartados pela poda:", estatisticas["total_podados"])
print("Verificações de cobertura realizadas:", estatisticas["total_verificados"])
print("Subconjuntos válidos encontrados:", estatisticas["total_validos"])