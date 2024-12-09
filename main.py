# Aluno: Felipe Antelo Machado de Oliveira
# Matrícula: 2210872
# Professor: Edward Hermann Haeusler
# Monitor: Eduardo Dantas Luna

import ply.lex as lex
import ply.yacc as yacc

# Dicionário de palavras reservadas
reserved = {
    'FACA': 'FACA',
    'SER': 'SER',
    'MOSTRE': 'MOSTRE',
    'SOME': 'SOME',
    'COM': 'COM',
    'MULTIPLIQUE': 'MULTIPLIQUE',
    'POR': 'POR',
    'REPITA': 'REPITA',
    'VEZES': 'VEZES',
    'FIM': 'FIM',
    'SE': 'SE',
    'ENTAO': 'ENTAO',
    'SENAO': 'SENAO',
}

# Lista de tokens
tokens = [
    'VAR',
    'NUM',
    'DOISPONTOS',
    'PONTO',
] + list(reserved.values())

# Expressões regulares para tokens simples
t_PONTO = r'\.'
t_DOISPONTOS = r':'
t_ignore = ' \t'

# Função para identificar números
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Função para identificar variáveis e palavras reservadas
def t_VAR(t):
    r'[a-zA-Z]+'
    t.type = reserved.get(t.value, 'VAR')
    return t

# Função para contar linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Função para tratar erros
def t_error(t):
    print(f"Caractere inválido '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Construindo o analisador léxico
lexer = lex.lex()

# Variáveis globais
variables = set()
contador = 0

# Construindo o parser
def p_programa(p):
    'programa : cmds'
    p[0] = p[1]

def p_cmds(p):
    '''cmds : cmd cmds
            | cmd'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Lista de comandos
    else:
        p[0] = [p[1]]

def p_cmd(p): 
    '''cmd : atribuicao
           | impressao
           | operacao
           | repeticao
           | condicional'''
    p[0] = p[1]

def p_atribuicao(p): #Função de atribuição de uma valor a variável
    '''atribuicao : FACA VAR SER NUM PONTO
                  | FACA VAR SER VAR PONTO'''
    var = p[2]
    value = p[4]
    variables.add(var)
    if isinstance(value, int):
        code = f'{var} = {value};'
    else:
        variables.add(value)
        code = f'{var} = {value};'
    p[0] = code

def p_impressao(p): #Função de print geral
    '''impressao : MOSTRE VAR PONTO
                 | MOSTRE NUM PONTO'''
    value = p[2]
    if isinstance(value, int):
        code = f'printf("%d\\n", {value});'
    else:
        variables.add(value)
        code = f'printf("%d\\n", {value});'
    p[0] = code

def p_operacao(p): #Reconhecimento de Operação (SOME ou MULTIPLIQUE)
    '''operacao : operacao_soma
                | operacao_multiplique'''
    p[0] = p[1]

def p_operacao_soma(p): #Operação de SOME X COM Y ponto
    '''operacao_soma : SOME VAR COM VAR PONTO
                     | SOME VAR COM NUM PONTO
                     | SOME NUM COM VAR PONTO
                     | SOME NUM COM NUM PONTO'''
    op1 = p[2]
    op2 = p[4]
    if isinstance(op1, int):
        print("Erro: Não é possível atribuir a um número.")
        p[0] = ''
    else:
        variables.add(op1)
        if isinstance(op2, str):
            variables.add(op2)
        code = f'{op1} = {op1} + {op2};'
        p[0] = code

def p_operacao_multiplique(p): #Operação de MULTIPLIQUE X POR Y ponto
    '''operacao_multiplique : MULTIPLIQUE VAR POR VAR PONTO
                            | MULTIPLIQUE VAR POR NUM PONTO
                            | MULTIPLIQUE NUM POR VAR PONTO
                            | MULTIPLIQUE NUM POR NUM PONTO'''
    op1 = p[2]
    op2 = p[4]
    if isinstance(op1, int):
        print("Erro: Não é possível atribuir a um número.")
        p[0] = ''
    else:
        variables.add(op1)
        if isinstance(op2, str):
            variables.add(op2)
        code = f'{op1} = {op1} * {op2};'
        p[0] = code

def p_repeticao(p): #Operação de Laço Loop
    '''repeticao : REPITA NUM VEZES DOISPONTOS cmds FIM
                 | REPITA VAR VEZES DOISPONTOS cmds FIM'''
    global contador
    contador += 1
    loop_var = f'i_{contador}'
    num_vezes = p[2]
    comandos = '\n'.join(p[5])
    if isinstance(num_vezes, str):
        variables.add(num_vezes)
    code = f'for(int {loop_var} = 0; {loop_var} < {num_vezes}; {loop_var}++) {{\n{comandos}\n}}'
    p[0] = code

def p_condicional(p): #Operação Condicional If-Then / If-Then-Else
    '''condicional : SE condicao ENTAO cmds FIM
                   | SE condicao ENTAO cmds SENAO cmds FIM'''
    cond = p[2]
    if isinstance(cond, str):
        variables.add(cond)
    if len(p) == 6:
        # SE condicao ENTAO cmds FIM
        comandos_then = '\n'.join(p[4])
        code = f'if({cond}) {{\n{comandos_then}\n}}'
    else:
        # SE condicao ENTAO cmds SENAO cmds FIM
        comandos_then = '\n'.join(p[4])
        comandos_else = '\n'.join(p[6])
        code = f'if({cond}) {{\n{comandos_then}\n}} else {{\n{comandos_else}\n}}'
    p[0] = code

def p_condicao(p):
    '''condicao : NUM
                | VAR'''
    p[0] = p[1]

def p_error(p): #Mensagem de Erro
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final da entrada")

parser = yacc.yacc()

def main():
    nomeArq = "teste1.mag"
    try:
        with open(nomeArq, "r") as file:
            data = file.read()
            if not data.strip(): #Leitura de arquivo que não pode ser strip indica que ele esta vazio
                print(f"Erro: O arquivo '{nomeArq}' está vazio.")
                return
    except FileNotFoundError: #Arquivo Inexistente
        print(f"Erro: O arquivo '{nomeArq}' não existe.")
        return

    result = parser.parse(data) #Armaze a data pós-parse em uma variável de result
    generated_code = '\n'.join(result) #join com '\n's para um código gerado

    # Declarar variáveis
    variable_declarations = ''
    if variables:
        variable_declarations = 'int ' + ', '.join(variables) + ';\n'

    # Código completo em C
    full_code = '#include <stdio.h>\n\nint main() {\n' + variable_declarations + generated_code + '\nreturn 0;\n}'

    # Escrever para um arquivo .c
    with open('output1.c', 'w') as f: #Abrir o arquivo output que o aluno/Herrman seleciona
        f.write(full_code) #Escreve código completo

    print("Compilado com sucesso! Código gerado em output.c") #Compilou enfim. Alegria!

if __name__ == '__main__':
    main()  