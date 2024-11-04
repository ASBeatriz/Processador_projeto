COMMAND_TO_BIN = {
    "ADD"   : "0000",
    "SUB"   : "0001",        
    "AND"   : "0010",        
    "OR"    : "0011",       
    "NOT"   : "0100",        
    "CMP"   : "0101",        
    "JMP"   : "0110",        
    "JEQ"   : "0111",        
    "JGR"   : "1000",        
    "LOAD"  : "1001",         
    "STORE" : "1010",          
    "MOV"   : "1011",        
    "IN"    : "1100",       
    "OUT"   : "1101",        
    "WAIT"  : "1110",
    ''      : "1111", 
}

# Precisa ter 4 bits também, caso esteja no mesmo arquivo de memória
VARIABLE_TO_BIN = {
    "A" : "0000",
    "B" : "0001",
    "R" : "0010",
}

# função que completa as linhas para que todas tenham tamanho 3
def make_all_items_len_three(assembly_splitted_rows):
    for item in assembly_splitted_rows:
        while len(item) < 3:
            item.append('')

def ler_arquivo():
    assembly_raw_input = open("assembly.txt", "r")

    # divide o conteúdo do código assemply em linhas
    assembly_rows = assembly_raw_input.read().split("\n")

    # divide as linhas em colunas, separando cada comando e valor
    assembly_splitted_rows = []
    for row in assembly_rows:
        assembly_splitted_rows.append(row.split(' '))

    make_all_items_len_three(assembly_splitted_rows)

    # tira as vírgulas que foram consideradas na divisão por colunas
    for linha in assembly_splitted_rows:
        for i in range(len(linha)):
            if not linha[i] == '':
                if linha[i][-1] == ',':
                    linha[i] = linha[i][0:-1]

    return assembly_splitted_rows

def print_lista(lista):
    for item in lista:
        print(item)

def lista_bin(lista_texto):
    listaB = []
    for item in lista_texto:
        for i in range(len(item)):
            comando = item[i]
            if comando == '':
                continue
            if comando in COMMAND_TO_BIN:
                listaB.append(COMMAND_TO_BIN[comando])

            elif comando in VARIABLE_TO_BIN:
                listaB.append(VARIABLE_TO_BIN[comando])

            else:
                listaB.append(comando)
    return listaB

'''
Função que adiciona os valores em binário dos comandos em assembly no arquivo de memória (.mif).
Considera-se que o arquivo já exista e tenha a estrutura base.
'''
def modifica_mif(conteudo):
    linha_content = "CONTENT BEGIN"
    linha_depth = "DEPTH"
    depth = len(conteudo)

    try:
        # Lê e armazena as linhas do arquivo 
        with open("dados.mif", "r") as file:
            linhas = file.readlines()

        if not linhas:  # Verifica se o arquivo está vazio
            print("O arquivo 'dados.mif' está vazio.")
            return

        # Procura pelo inicio de onde se deve colocar os valores e endereços
        content_index = None
        for index, linha in enumerate(linhas):
            if linha_content in linha:
                content_index = index
                break

        # Adiciona os endereços e valores
        endereco = 0
        for item in conteudo:
            linhas.insert(content_index + 1, f"\t{endereco} : {item};\n")  
            endereco += 1
            content_index += 1

        # Atualiza a linha de profundidade
        for index, linha in enumerate(linhas):
            if linha_depth in linha:
                linhas[index] = f"DEPTH={depth}; \n"
                break

        # Reescreve o arquivo com o novo conteúdo
        with open("dados.mif", "w") as file:
            file.writelines(linhas)

    except FileNotFoundError:
        print("O arquivo 'dados.mif' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


leitura_txt = ler_arquivo()
print_lista(leitura_txt)
leitura_bin = lista_bin(leitura_txt)
print_lista(leitura_bin)
modifica_mif(leitura_bin)
