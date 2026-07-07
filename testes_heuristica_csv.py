import time
import csv

# ===================================================
# TESTES AUTOMÁTICOS DA HEURÍSTICA
# Problema do Conjunto Dominante aplicado à irrigação
# ===================================================
#
# Este arquivo deve ficar na mesma pasta dos arquivos:
# instancia_5.txt, instancia_10.txt, ..., instancia_35.txt
#
# Ele executa a heurística 5 vezes para cada instância e gera:
# 1) resultados_heuristica_execucoes.csv  -> todas as execuções
# 2) resultados_heuristica_resumo.csv     -> médias por instância


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

    # A própria região também é coberta por um irrigador instalado nela
    if regioes_cobertas[regiao] == False:
        ganho += 1
    else:
        sobreposicao += 1

    # Verifica as regiões vizinhas cobertas pelo irrigador
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


### HEURÍSTICA GULOSA COM DESEMPATE POR MENOR SOBREPOSIÇÃO ###
def heuristica_gulosa(matriz_adjacencia, quantidade_regioes):
    solucao = []
    regioes_cobertas = [False] * quantidade_regioes

    iteracoes = 0
    candidatos_avaliados = 0
    verificacoes_ganho = 0

    while todas_cobertas(regioes_cobertas, quantidade_regioes) == False:
        iteracoes += 1

        melhor_regiao = -1
        melhor_ganho = -1
        menor_sobreposicao = quantidade_regioes + 1

        for regiao in range(quantidade_regioes):
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


### REMOVER IRRIGADORES REDUNDANTES ###
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


### EXECUTAR UMA VEZ A HEURÍSTICA ###
def executar_heuristica(matriz_adjacencia, quantidade_regioes):
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

    resultado = {
        "espaco_busca_total": (1 << quantidade_regioes) - 1,
        "irrigadores_antes_remocao": estatisticas_guloso["irrigadores_antes_remocao"],
        "irrigadores_finais": len(solucao_final),
        "regioes_escolhidas": str(solucao_final),
        "solucao_valida": solucao_valida,
        "iteracoes_heuristica": estatisticas_guloso["iteracoes"],
        "candidatos_avaliados": estatisticas_guloso["candidatos_avaliados"],
        "verificacoes_ganho": estatisticas_guloso["verificacoes_ganho"],
        "verificacoes_pos_processamento": estatisticas_pos["verificacoes_pos_processamento"],
        "remocoes_realizadas": estatisticas_pos["remocoes_realizadas"],
        "tempo_guloso": tempo_guloso,
        "tempo_pos_processamento": tempo_pos_processamento,
        "tempo_total": tempo_total
    }

    return resultado


### CALCULAR MÉDIA ###
def media(lista):
    if len(lista) == 0:
        return 0

    soma = 0

    for valor in lista:
        soma += valor

    return soma / len(lista)


### PROGRAMA PRINCIPAL ###
def main():
    instancias = [
        "instancia_5.txt",
        "instancia_10.txt",
        "instancia_15.txt",
        "instancia_20.txt",
        "instancia_25.txt",
        "instancia_30.txt",
        "instancia_35.txt"
    ]

    repeticoes = 5

    arquivo_execucoes = "resultados_heuristica_execucoes.csv"
    arquivo_resumo = "resultados_heuristica_resumo.csv"

    campos_execucoes = [
        "instancia",
        "execucao",
        "quantidade_regioes",
        "espaco_busca_total",
        "irrigadores_antes_remocao",
        "irrigadores_finais",
        "regioes_escolhidas",
        "solucao_valida",
        "iteracoes_heuristica",
        "candidatos_avaliados",
        "verificacoes_ganho",
        "verificacoes_pos_processamento",
        "remocoes_realizadas",
        "tempo_guloso",
        "tempo_pos_processamento",
        "tempo_total"
    ]

    campos_resumo = [
        "instancia",
        "quantidade_regioes",
        "espaco_busca_total",
        "irrigadores_finais",
        "regioes_escolhidas",
        "solucao_valida",
        "iteracoes_heuristica",
        "candidatos_avaliados",
        "verificacoes_ganho",
        "verificacoes_pos_processamento",
        "remocoes_realizadas",
        "tempo_guloso_medio",
        "tempo_pos_processamento_medio",
        "tempo_total_medio"
    ]

    resultados_resumo = []

    with open(arquivo_execucoes, "w", newline="", encoding="utf-8") as csv_execucoes:
        escritor_execucoes = csv.DictWriter(csv_execucoes, fieldnames=campos_execucoes, delimiter=";")
        escritor_execucoes.writeheader()

        for nome_instancia in instancias:
            try:
                quantidade_regioes, matriz_adjacencia = ler_instancia(nome_instancia)
            except FileNotFoundError:
                print("Arquivo não encontrado:", nome_instancia)
                print("Pulando esta instância.\n")
                continue

            print("Executando testes para:", nome_instancia)

            tempos_guloso = []
            tempos_pos = []
            tempos_total = []

            ultimo_resultado = None

            for execucao in range(1, repeticoes + 1):
                resultado = executar_heuristica(matriz_adjacencia, quantidade_regioes)

                linha = {
                    "instancia": nome_instancia,
                    "execucao": execucao,
                    "quantidade_regioes": quantidade_regioes,
                    "espaco_busca_total": resultado["espaco_busca_total"],
                    "irrigadores_antes_remocao": resultado["irrigadores_antes_remocao"],
                    "irrigadores_finais": resultado["irrigadores_finais"],
                    "regioes_escolhidas": resultado["regioes_escolhidas"],
                    "solucao_valida": resultado["solucao_valida"],
                    "iteracoes_heuristica": resultado["iteracoes_heuristica"],
                    "candidatos_avaliados": resultado["candidatos_avaliados"],
                    "verificacoes_ganho": resultado["verificacoes_ganho"],
                    "verificacoes_pos_processamento": resultado["verificacoes_pos_processamento"],
                    "remocoes_realizadas": resultado["remocoes_realizadas"],
                    "tempo_guloso": "{:.9f}".format(resultado["tempo_guloso"]),
                    "tempo_pos_processamento": "{:.9f}".format(resultado["tempo_pos_processamento"]),
                    "tempo_total": "{:.9f}".format(resultado["tempo_total"])
                }

                escritor_execucoes.writerow(linha)

                tempos_guloso.append(resultado["tempo_guloso"])
                tempos_pos.append(resultado["tempo_pos_processamento"])
                tempos_total.append(resultado["tempo_total"])

                ultimo_resultado = resultado

                print(
                    "  Execução", execucao,
                    "- irrigadores:", resultado["irrigadores_finais"],
                    "- tempo total: {:.9f}s".format(resultado["tempo_total"])
                )

            linha_resumo = {
                "instancia": nome_instancia,
                "quantidade_regioes": quantidade_regioes,
                "espaco_busca_total": ultimo_resultado["espaco_busca_total"],
                "irrigadores_finais": ultimo_resultado["irrigadores_finais"],
                "regioes_escolhidas": ultimo_resultado["regioes_escolhidas"],
                "solucao_valida": ultimo_resultado["solucao_valida"],
                "iteracoes_heuristica": ultimo_resultado["iteracoes_heuristica"],
                "candidatos_avaliados": ultimo_resultado["candidatos_avaliados"],
                "verificacoes_ganho": ultimo_resultado["verificacoes_ganho"],
                "verificacoes_pos_processamento": ultimo_resultado["verificacoes_pos_processamento"],
                "remocoes_realizadas": ultimo_resultado["remocoes_realizadas"],
                "tempo_guloso_medio": "{:.9f}".format(media(tempos_guloso)),
                "tempo_pos_processamento_medio": "{:.9f}".format(media(tempos_pos)),
                "tempo_total_medio": "{:.9f}".format(media(tempos_total))
            }

            resultados_resumo.append(linha_resumo)
            print()

    with open(arquivo_resumo, "w", newline="", encoding="utf-8") as csv_resumo:
        escritor_resumo = csv.DictWriter(csv_resumo, fieldnames=campos_resumo, delimiter=";")
        escritor_resumo.writeheader()

        for linha in resultados_resumo:
            escritor_resumo.writerow(linha)

    print("Testes finalizados.")
    print("Arquivo gerado:", arquivo_execucoes)
    print("Arquivo gerado:", arquivo_resumo)


if __name__ == "__main__":
    main()
