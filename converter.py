VARIABLE_TO_BIN = {
    'A' : '00',
    'B' : '01',
    'R' : '10'}
# 11 = imediato

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
}

# variaveis para os endereços de loop_start e end_loop
addr_loopstart = 0
addr_endloop = 0

def converte_hex(lista):
    lista_hex = []
    for item in lista:
        decimal = int(item, 2)
        it_hex = hex(decimal)[2:].upper()
        it_hex = it_hex.zfill(2)
        lista_hex.append(it_hex)
    return lista_hex

def print_lista(lista):
    for item in lista:
        print(item)

def criar_arquivo_hex(nome_arquivo, dados_hex):
    try:
        with open(nome_arquivo, 'w') as arquivo:
            for dado in dados_hex:
                arquivo.write(dado + '\n')  # Escreve cada valor hexadecimal em uma nova linha
    except Exception as e:
        print(f"Erro ao criar o arquivo: {e}")

# função que completa as linhas para que todas tenham tamanho 3
def make_all_items_len_three(assembly_splitted_rows):
    for item in assembly_splitted_rows:
        while len(item) < 3:
            item.append('')

def ler_arquivo():
    assembly_raw_input = open("assembly.asm", "r")

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

def endereca_labels(lista_texto):
    global addr_loopstart, addr_endloop

    contador = 0
    for item in lista_texto:

        # Codifica os comandos
        comando = item[0]
        if not comando in COMMAND_TO_BIN:
            if comando == "LOOP_START:":
                addr_loopstart = contador
            elif comando == "END_LOOP:":
                addr_endloop = contador

        else:
            # análise do segundo termo
            if len(item) > 1 and item[1] != '':
                # é registrador
                if item[1] in VARIABLE_TO_BIN: 
                    if item[0] in ('JMP','JGR', 'JEQ'):
                        contador += 1 
                    elif item[0] == 'NOT':
                        contador += 1
                    else:
                        if len(item) > 2 and item[2] == '':
                            contador += 1

                # é decimal
                elif item[1].isdecimal():
                    contador += 2

                # é label
                else:
                    contador += 2
            else:
                contador += 1

            if len(item) > 2 and item[2] != '':
                if item[2] in VARIABLE_TO_BIN:
                    contador += 1
                else:
                    contador += 2
                

'''
Função que codifica os comando em assembly para binário. Recebe uma lista (matriz) 
com os comandos separados e em texto e retorna uma lista com os comandos em binário 
(uma palavra de 8 bits para cada linha do assembly). 
'''
def codifica_bin(lista_texto):
    global addr_loopstart, addr_endloop
    print(f"LOOP START: {addr_loopstart} LOOP END: {addr_endloop}")
    listaB = []

    contador = 0
    for item in lista_texto:
        print(f"Item atual: {item}")
        IR = '' # Variavel que armazena a instrução (comando + variaveis)

        # Codifica os comandos
        comando = item[0]
        if comando in COMMAND_TO_BIN:

            IR = COMMAND_TO_BIN[comando]
            print(f"comando: {IR}")

            # análise do segundo termo
            if len(item) > 1 and item[1] != '':
                # é registrador
                if item[1] in VARIABLE_TO_BIN: 
                    if item[0] in ('JMP','JGR', 'JEQ'):
                        IR = IR + "00" + VARIABLE_TO_BIN[item[1]]
                        listaB.append(IR)
                        contador += 1 
                    elif item[0] == 'NOT':
                        IR = IR + VARIABLE_TO_BIN[item[1]] + "00"
                        listaB.append(IR)
                        contador += 1
                    else:
                        IR = IR + VARIABLE_TO_BIN[item[1]]
                        if len(item) > 2 and item[2] == '':
                            IR = IR + "00"
                            listaB.append(IR)
                            contador += 1

                # é decimal
                elif item[1].isdecimal():
                    IR = IR + "0011"
                    listaB.append(IR)
                    num_bin = bin(int(item[1]))[2:]
                    num_bin = '{0:0>8}'.format(num_bin) # Garante que o número tenha 8 bits
                    listaB.append(num_bin)
                    contador += 2

                # é label
                else:
                    IR = IR + "0011"
                    listaB.append(IR)
                    if item[1] == "LOOP_START":
                        num_bin = bin(addr_loopstart)[2:]
                        num_bin = '{0:0>8}'.format(num_bin) # Garante que o número tenha 8 bits
                        print(f"BINARIO: {num_bin}")
                        listaB.append(num_bin)
                    else:
                        num_bin = bin(addr_endloop)[2:]
                        num_bin = '{0:0>8}'.format(num_bin) # Garante que o número tenha 8 bits
                        print(f"BINARIO: {num_bin}")
                        listaB.append(num_bin)
                    contador += 1
                print(f"comando: {IR}")
            else:
                listaB.append(IR)
                contador += 1

            if len(item) > 2 and item[2] != '':
                if item[2] in VARIABLE_TO_BIN:
                    IR = IR + VARIABLE_TO_BIN[item[2]]
                    listaB.append(IR)
                    contador += 1
                else:
                    IR = IR + "11"
                    listaB.append(IR) #imediato
                    num_bin = bin(int(item[2]))[2:]
                    num_bin = '{0:0>8}'.format(num_bin) # Garante que o número tenha 8 bits
                    listaB.append(num_bin)
                    contador += 2
                print(f"comando: {IR}")
        print(f"Contador: {contador}")
                

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

        # Reescreve o arquivo com o novo conteúdo
        with open("dados.mif", "w") as file:
            file.writelines(linhas)

    except FileNotFoundError:
        print("O arquivo 'dados.mif' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


leitura_txt = ler_arquivo()
print_lista(leitura_txt)
endereca_labels(leitura_txt)
leitura_bin = codifica_bin(leitura_txt)
print_lista(leitura_bin)
modifica_mif(leitura_bin)
leitura_hex = converte_hex(leitura_bin)
print_lista(leitura_hex)
criar_arquivo_hex("instrucoes.hex", leitura_hex)

# OBS: ESSE CÓDIGO CONSIDERA QUE TODOS OS NÚMEROS PASSADO PELO ASSEMBLY ESTÃO EM DECIMAL (INCLUINDO ENDEREÇOS)