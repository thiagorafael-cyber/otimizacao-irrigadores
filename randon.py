import random

def gerar_instancia_txt(n, nome_arquivo):
    # Criar uma matriz de adjacência n x n simétrica
    matriz = [[0] * n for _ in range(n)]
    
    # Preencher a matriz com probabilidade de 15% de conexão (para não ficar denso demais)
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.15:
                matriz[i][j] = 1
                matriz[j][i] = 1
    
    with open(nome_arquivo, 'w') as f:
        f.write(f"{n}\n")
        for linha in matriz:
            f.write(" ".join(map(str, linha)) + "\n")

# Gerando os arquivos
gerar_instancia_txt(15, 'instancia_15.txt')
gerar_instancia_txt(35, 'instancia_35.txt')