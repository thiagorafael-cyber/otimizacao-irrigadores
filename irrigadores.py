import time
### LER ARQUIVO TXT ###
def ler_instancia(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        quantidade_regioes = int(arquivo.readline())

        matriz_adjacencia = []

        for i in range(quantidade_regioes):
            linha = list(map(int, arquivo.readline().split()))
            matriz_adjacencia.append(linha)

    return quantidade_regioes, matriz_adjacencia

### VERIFICAR COBERTURA ###
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

### BASELINE - FORÇA BRUTA ###
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
########### FIM DA FORÇA-BRUTA ############

### FUNÇÕES AUXILIARES DA HEURÍSTICA ###

def todas_cobertas(regioes_cobertas, quantidade_regioes):
    for i in range(quantidade_regioes):
        if regioes_cobertas[i] == False:
            return False

    return True


def calcular_ganho_e_sobreposicao(matriz_adjacencia, regiao, regioes_cobertas, quantidade_regioes):
    ganho = 0
    sobreposicao = 0
    verificacoes = 0

    # Considera a própria região
    if regioes_cobertas[regiao] == False:
        ganho += 1
    else:
        sobreposicao += 1

    # Considera as regiões vizinhas cobertas pelo irrigador
    for vizinha in range(quantidade_regioes):
        verificacoes += 1

        if matriz_adjacencia[regiao][vizinha] == 1:
            if regioes_cobertas[vizinha] == False:
                ganho += 1
            else:
                sobreposicao += 1

    return ganho, sobreposicao, verificacoes


def marcar_cobertura(matriz_adjacencia, regiao, regioes_cobertas, quantidade_regioes):
    regioes_cobertas[regiao] = True

    for vizinha in range(quantidade_regioes):
        if matriz_adjacencia[regiao][vizinha] == 1:
            regioes_cobertas[vizinha] = True


def heuristica_gulosa(matriz_adjacencia, quantidade_regioes):
    solucao = []
    regioes_cobertas = [False] * quantidade_regioes

    iteracoes = 0
    candidatos_avaliados = 0
    verificacoes_ganho = 0

    while todas_cobertas(regioes_cobertas, quantidade_regioes) == False: # laço principal
        iteracoes += 1

        melhor_regiao = -1
        melhor_ganho = -1
        menor_sobreposicao = quantidade_regioes + 1

        for regiao in range(quantidade_regioes): # Avalia todas as candidatas
            candidatos_avaliados += 1

            ganho, sobreposicao, verificacoes = calcular_ganho_e_sobreposicao(
                matriz_adjacencia,
                regiao,
                regioes_cobertas,
                quantidade_regioes
            )

            verificacoes_ganho += verificacoes

            if ganho > melhor_ganho:
                melhor_ganho = ganho
                menor_sobreposicao = sobreposicao
                melhor_regiao = regiao

            elif ganho == melhor_ganho and sobreposicao < menor_sobreposicao:
                menor_sobreposicao = sobreposicao
                melhor_regiao = regiao

        solucao.append(melhor_regiao)
        marcar_cobertura(matriz_adjacencia, melhor_regiao, regioes_cobertas, quantidade_regioes)

    estatisticas = {
        "iteracoes": iteracoes,
        "candidatos_avaliados": candidatos_avaliados,
        "verificacoes_ganho": verificacoes_ganho,
        "irrigadores_antes_remocao": len(solucao)
    }

    return solucao, estatisticas


### REMOVE REDUNDANTES ###

def remover_redundantes(matriz_adjacencia, solucao, quantidade_regioes):
    solucao_final = solucao[:]

    verificacoes_pos_processamento = 0
    remocoes_realizadas = 0

    for regiao in solucao[:]:
        tentativa = []

        for r in solucao_final:
            if r != regiao:
                tentativa.append(r)

        verificacoes_pos_processamento += 1

        if verifica_cobertura(matriz_adjacencia, tentativa, quantidade_regioes):
            solucao_final = tentativa
            remocoes_realizadas += 1

    estatisticas_pos = {
        "verificacoes_pos_processamento": verificacoes_pos_processamento,
        "remocoes_realizadas": remocoes_realizadas
    }

    return solucao_final, estatisticas_pos

### MENUS DO SISTEMA ###

##### FUNCAO BASELINE #####

def executar_baseline_arquivo():
    arquivo = input("Digite o nome do arquivo da instância: ").strip()

    quantidade_regioes, matriz_adjacencia = ler_instancia(arquivo)

    inicio = time.time()

    solucao, estatisticas = conjunto_dominante_minimo(matriz_adjacencia, quantidade_regioes)

    fim = time.time()

    print("\n================ RESULTADO BASELINE ================")
    print("Quantidade de regiões agrícolas:", quantidade_regioes)
    print("Número mínimo de irrigadores:", len(solucao))
    print("Instalar irrigadores nas regiões:", solucao)
    print("Tempo de execução: {:.6f} segundos".format(fim - inicio))

    print("\n========== ESTATÍSTICAS ==========")
    print("Espaço de busca total:", (1 << quantidade_regioes) - 1)
    print("Subconjuntos descartados pela poda:", estatisticas["total_podados"])
    print("Verificações de cobertura realizadas:", estatisticas["total_verificados"])
    print("Subconjuntos válidos encontrados:", estatisticas["total_validos"])


##### FUNCAO HEURISTICA ARQUIVO .TXT  #####

def executar_heuristica_arquivo():
    arquivo = input("Digite o nome do arquivo da instância: ").strip()

    quantidade_regioes, matriz_adjacencia = ler_instancia(arquivo)

    inicio_guloso = time.perf_counter()
    solucao_inicial, estatisticas_guloso = heuristica_gulosa(matriz_adjacencia, quantidade_regioes)
    fim_guloso = time.perf_counter()

    inicio_pos = time.perf_counter()
    solucao_final, estatisticas_pos = remover_redundantes(
        matriz_adjacencia,
        solucao_inicial,
        quantidade_regioes
    )
    fim_pos = time.perf_counter()

    solucao_valida = verifica_cobertura(matriz_adjacencia, solucao_final, quantidade_regioes)

    tempo_guloso = fim_guloso - inicio_guloso
    tempo_pos_processamento = fim_pos - inicio_pos
    tempo_total = tempo_guloso + tempo_pos_processamento

    print("\n================ RESULTADO HEURÍSTICA ================")
    print("Quantidade de regiões agrícolas:", quantidade_regioes)
    print("Espaço de busca total:", (1 << quantidade_regioes) - 1)

    print("\n========== SOLUÇÃO ==========")
    print("Irrigadores antes da remoção:", estatisticas_guloso["irrigadores_antes_remocao"])
    print("Irrigadores finais:", len(solucao_final))
    print("Instalar irrigadores nas regiões:", solucao_final)
    print("Solução cobre todas as regiões:", solucao_valida)

    print("\n========== PROCESSAMENTO ==========")
    print("Iterações da heurística:", estatisticas_guloso["iteracoes"])
    print("Candidatos avaliados:", estatisticas_guloso["candidatos_avaliados"])
    print("Verificações de ganho:", estatisticas_guloso["verificacoes_ganho"])
    print("Verificações no pós-processamento:", estatisticas_pos["verificacoes_pos_processamento"])
    print("Remoções realizadas:", estatisticas_pos["remocoes_realizadas"])

    print("\n========== TEMPOS ==========")
    print("Tempo guloso: {:.6f} segundos".format(tempo_guloso))
    print("Tempo pós-processamento: {:.6f} segundos".format(tempo_pos_processamento))
    print("Tempo total: {:.6f} segundos".format(tempo_total))

#### MENU PRINCIPAL ###
def mostrar_menu():
    print("===================================================")
    print(" DISTRIBUIÇÃO ÓTIMA DE IRRIGADORES")
    print(" Problema do Conjunto Dominante")
    print("===================================================")
    print("1 - Executar baseline com arquivo .txt")
    print("2 - Executar heurística com arquivo .txt")    
    print("0 - Sair")


while True:
    mostrar_menu()

    opcao = input("\nEscolha uma opção: ").strip()

    if opcao == "1":
        executar_baseline_arquivo()

    elif opcao == "2":
        executar_heuristica_arquivo()

   # elif opcao == "3":
   #     print("\nOpção de geração automática será implementada na próxima etapa.")

    elif opcao == "0":
        print("\nEncerrando o sistema.")
        break

    else:
        print("\nOpção inválida. Tente novamente.")

    print()