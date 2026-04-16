# ====================================================================
# PROJETO: Distribuição de Irrigadores por Aspersão (Conjunto Dominante)
# DISCIPLINA: Projeto e Análise de Algoritmos
# ====================================================================

# ---------------------------------------------------------
# ATIVIDADE 3: Estrutura de Dados e Instância do Problema
# ---------------------------------------------------------
import time

def ler_matriz_do_arquivo(nome_arquivo):
    """
    Lê a matriz de adjacência a partir de um arquivo de texto.
    """
    # Abre o arquivo de texto em modo de leitura ('r' = read)
    with open(nome_arquivo, 'r') as arquivo:
        # Lê todas as linhas do arquivo e guarda numa lista
        linhas = arquivo.readlines()
        
        # Pega a primeira linha, remove espaços invisíveis (strip) e converte para número inteiro.
        # Este é o 'n', ou seja, o número total de parcelas (ex: 5)
        n = int(linhas[0].strip())
        
        # Cria uma lista vazia que vai guardar a nossa matriz final
        matriz = []
        
        # Faz um loop da segunda linha do arquivo (índice 1) até a última (n)
        for i in range(1, n + 1):
            # Pega a linha atual (ex: "0 1 1 1 0"), tira espaços extras, separa os números 
            # onde tem espaço e transforma cada um deles num número inteiro.
            linha_matriz = list(map(int, linhas[i].strip().split()))
            
            # Adiciona essa lista (linha) dentro da nossa matriz principal
            matriz.append(linha_matriz)
            
    # Retorna o tamanho (n) e a matriz montada para quem chamou a função
    return n, matriz


# ---------------------------------------------------------
# ATIVIDADE 4: Algoritmo Baseline (Força-Bruta)
# ---------------------------------------------------------

def verifica_cobertura(matriz, subconjunto, n):
    """
    Verifica se a combinação que estamos testando no momento molha TODAS as parcelas.
    """
    # Percorre todas as parcelas da fazenda (de 0 até n-1)
    for parcela in range(n):
        
        # Se a parcela atual já tem um irrigador instalado nela mesma (está no subconjunto),
        # ela já está molhada. O 'continue' faz pular para analisar a próxima parcela.
        if parcela in subconjunto:
            continue
            
        # Variável para anotar se a parcela atual recebeu água de algum vizinho
        esta_coberta = False
        
        # Verifica um por um os irrigadores que decidimos ligar nesta tentativa
        for aspersor in subconjunto:
            # Olha na matriz: o aspersor alcança a parcela atual? (1 = alcança)
            if matriz[parcela][aspersor] == 1:
                esta_coberta = True # Opa, recebeu água!
                break # Como já está molhada, não precisamos checar os outros aspersores para ela
                
        # Se terminou de olhar todos os aspersores ligados e a parcela continuou seca (False)
        if not esta_coberta:
            # Significa que essa tentativa não serve, falhou em cobrir a fazenda toda
            return False
            
    # Se o loop terminou de rodar e não retornou False para nenhuma parcela, 
    # significa que a fazenda inteira foi regada. Retorna True (Sucesso!).
    return True

def forca_bruta_irrigadores(matriz, n):
    """
    Gera todos os subconjuntos possíveis usando lógica binária (O(2^n)).
    """
    # Começamos dizendo que o "melhor tamanho" é maior que o máximo possível (n + 1).
    # Assim, qualquer solução válida encontrada será menor e vai substituir este valor.
    melhor_tamanho = n + 1
    melhor_subconjunto = []
    
    # Calcula o total de combinações possíveis: 2 elevado a 'n'.
    # O operador '<<' desloca bits. Fazer (1 << 5) resulta no número 32 (0 a 31).
    total_combinacoes = 1 << n
    
    # Inicia um loop de 1 até o total de combinações.
    # Começa no 1 para pular o 0 (pois o zero seria tentar ligar nenhum irrigador).
    for i in range(1, total_combinacoes):
        
        # Lista vazia para guardar quais irrigadores vamos testar nesta rodada (ex: [0, 4])
        subconjunto_atual = []
        
        # Loop para olhar cada parcela (de 0 até n-1) e decidir se vai ou não irrigador nela
        for j in range(n):
            # A MÁGICA BINÁRIA: o operador '&' checa se o bit da posição 'j' 
            # dentro do número 'i' é igual a 1. Se for, colocamos um irrigador nessa parcela 'j'.
            if i & (1 << j):
                subconjunto_atual.append(j)
                
        # Otimização (Poda): se a quantidade de irrigadores que vamos testar agora
        # já é igual ou MAIOR do que a melhor quantidade que já achamos antes, 
        # o 'continue' faz pular a verificação, pois não queremos piorar o resultado!
        if len(subconjunto_atual) >= melhor_tamanho:
            continue
            
        # Chama a função lá de cima para ver se essa combinação molha a fazenda toda
        if verifica_cobertura(matriz, subconjunto_atual, n):
            # Se molha, e já sabemos que usa menos aspersores (por causa do IF anterior),
            # atualizamos nossa melhor resposta!
            melhor_tamanho = len(subconjunto_atual)
            melhor_subconjunto = subconjunto_atual
            
    # No fim de todas as milhões de combinações, retorna o menor subconjunto que cobriu tudo
    return melhor_subconjunto

# ====================================================================
# EXECUÇÃO DO PROGRAMA
# ====================================================================
if __name__ == "__main__":
    print("--- Otimização de Irrigadores (Conjunto Dominante) ---")
    
    # MUDE O NOME DO ARQUIVO AQUI NA HORA DA APRESENTAÇÃO!
    arquivo_teste = 'instancia_30.txt' 
    
    print(f"Lendo dados do arquivo: {arquivo_teste}...")
    
    numero_de_parcelas, matriz_adjacencia = ler_matriz_do_arquivo(arquivo_teste)
    print(f"Total de parcelas agrícolas: {numero_de_parcelas}")
    
    print("A calcular a distribuição ótima de irrigadores (Força-Bruta)...")
    
    # --- INÍCIO DO CRONÓMETRO ---
    tempo_inicio = time.time()
    
    # Roda o Algoritmo
    solucao_otima = forca_bruta_irrigadores(matriz_adjacencia, numero_de_parcelas)
    
    # --- FIM DO CRONÓMETRO ---
    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio
    
    # 3. Exibe o Resultado
    print("\n[ RESULTADO ]")
    print(f"Número mínimo de irrigadores necessários: {len(solucao_otima)}")
    print(f"Instalar irrigadores nas parcelas: {solucao_otima}")
    
    # O ":.4f" serve para mostrar apenas 4 casas decimais e deixar o visual limpo
    print(f"Tempo de execução: {tempo_total:.4f} segundos")