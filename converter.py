# RESOLVER PROBLEMA DO TAB NO ASSEMBLY!!

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
    "WAIT"  : "11100000",
    ''      : "1111", 
}

VARIABLE_TO_BIN = {
      "AA"   :  "0000",
      "BB"   :  "0001",
      "RR"   :  "0010",
      "AB"   :  "0011",
      "BA"   :  "0100",
      "AR"   :  "0101",
      "RA"   :  "0110",
      "BR"   :  "0111",
      "RB"   :  "1000",
    #   "A 10"   :  "1001", (casos tratados a parte)
    #   "B 10"   :  "1010",
    #   "R 10"   :  "1011",
      "A" :  "1100",
      "B" :  "1101",
      "R" :  "1110",
    #   "10" :  "1111", (só número)
}

#EXEMPLO: o valor 00010100 representa "SUB B, A"
#EXEMPLO2: o valor 01101111 representa o JMP para algum endereço dado em decimal (armazenado em binário na linha seguinte do .mif)

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

'''
Função que codifica os comando em assembly para binário. Recebe uma lista (matriz) 
com os comandos separados e em texto e retorna uma lista com os comandos em binário 
(uma palavra de 8 bits para cada linha do assembly). 
'''
def codifica_bin(lista_texto):
    listaB = []

    loop_start = -1 # Armazena a linha do início do loop
    contador = 1
    for item in lista_texto:
        IR = '' # Variavel que armazena a instrução (comando + variaveis)

        # Codifica os comandos
        comando = item[0]
        if comando in COMMAND_TO_BIN:
            IR = COMMAND_TO_BIN[comando]
        elif comando == "LOOP_START:":
            IR = "11111111"     # Código para o início do LOOP (ignorado no vhdl)
            loop_start = contador   
            listaB.append(IR)
            continue
        elif comando == "END_LOOP:":
            IR = "11111111"  
            listaB.append(IR)
            continue
        else:
            listaB.append("comando-nao-identificado")

        # Codifica a combinação de variáveis
        variaveis = item[1] + item[2]
        if variaveis in VARIABLE_TO_BIN:
            print("variaveis: " + variaveis)
            IR = IR + VARIABLE_TO_BIN[variaveis]
            listaB.append(IR)

        # Caso em que há um imediato (número)
        else:
            indice = 2
            if item[1] == "A":
                IR = IR + "1001"

            elif item[1] == "B":
                IR = IR + "1010"

            elif item[1] == "R":
                IR = IR + "1011"
            
            else: # caso de ser só o imediato
                IR = IR + "1111"
                indice = 1

            listaB.append(IR)

            num_bin = 0
            if item[1] == "LOOP_START":
                num_bin = bin(loop_start)[2:]   # Pega o endereço (linha) do inicio do loop
            else:
                num_bin = bin(int(item[indice]))[2:]
                
            num_bin = '{0:0>8}'.format(num_bin) # Garante que o número tenha 8 bits
            # adiciona o número no endereço seguinte
            listaB.append(num_bin) 
        
        contador = contador+1

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
leitura_bin = codifica_bin(leitura_txt)
print_lista(leitura_bin)
modifica_mif(leitura_bin)


# OBS: ESSE CÓDIGO CONSIDERA QUE TODOS OS NÚMEROS PASSADO PELO ASSEMBLY ESTÃO EM DECIMAL (INCLUINDO ENDEREÇOS)