#Aluno: Felipe Antelo Machado de Oliveira
#Matrícula: 2210872
#Professor: Edward Hermann Haeusler
#Monitor: Eduardo Dantas Luna

#INICIO -> Incluir variáveis diversas
#armazena -> sinaliza o inicio da varlist
#Essas variaveis devem ser impressas
#EXECUTE -> Após ele vem uma sequencia de comandos
#TERMINO -> Termino do programa
#cmd -> ENQUANTO id FACA cmds FIM (loop)
#enquanto id !=0 FACA cmds FIM

#Devemos complementar a linguagem com os comandos:

#AQUI!!!!!!!!!!!!!
#programa → cmds
# cmds → cmd cmds | cmd
# cmd → atribuicao | impressao | operacao | repeticao
# atribuicao → FACA var SER num.
# impressao → MOSTRE var. | MOSTRE operacao.
# operacao → SOME var COM var. | SOME var COM num. | SOME num COM num.
# repeticao → REPITA num VEZES : cmds FIM

#Condicional
# cmd → condicional
# condicional → SE condicao ENTAO cmd FIM
#             | SE condicao ENTAO cmd SENAO cmd FIM
# condicao → num | var

#Multiplicacao
# operacao → MULTIPLIQUE var POR var.
#          | MULTIPLIQUE var POR num.
#          | MULTIPLIQUE num POR num.

#Recursão a esquerda?
#cmds → cmd cmds'
#cmds' → cmd cmds' | ε

from ply.lex import lex #necessário??
from ply.yacc import yacc #necessário??

global armazena
armazena = []

#Definindo os Tokens:
#def t_token(t):
tokens = (
    'FACA', #Inicio de uma atribuição
    'SER',  #Utilizado na atribuição para definir o valor da variável
    'MOSTRE', #Imprimir variável ou resultado de operação
    'SOME', #Inicio de uma operação de soma
    'COM',  #Especifica o segundo operador de SOMA
    'MULTIPLIQUE', #Inicio de uma operação de multiplicação
    'REPITA', #Inicio de Laço de Loop
    'VEZES', #Especifica o segundo operador de MULTIPLIQUE
    'DOISPONTOS',  #Especifica o bloco de laço de loop
    'FIM', #Fim de um bloco de repetição ou condição
    'SE',  #Inicia condicional
    'ENTAO', #Utilizado na estrutura condicional após a condição
    'SENAO',
    'PONTO',
    'VAR',
    'NUM', #Utilizado na estrutura condicional para definir o bloco alternativo
    #'var',  #identificador de variável formados por letras
    #'num',   #identificador de variável formados por numeros
    #'SPECIALS',
    #'PAR_O',
    #'PAR_C',
)

#Expressões regulares para os Tokens Simples
# t_INICIO = r'INICIO' NOTA: Necessário??
t_FACA = r'FACA'
t_SER = r'SER'
t_MOSTRE = r'MOSTRE'
t_SOME = r'SOME'
t_COM = r'COM'
t_MULTIPLIQUE = r'MULTIPLIQUE'
t_POR = r'POR'
t_REPITA = r'REPITA'
t_VEZES = r'VEZES'
t_DOISPONTOS = r':'
t_FIM = r'FIM'
t_SE = r'SE'
t_ENTAO = r'ENTAO'
t_SENAO = r'SENAO'
t_PONTO = r'\.'
#t_VAR = r'[a-zA-Z]+' NOTA: Necessário??
#t_NUM = r'\d+'  NOTA: Necessário??
t_ignore = ' \t' #Espaço em branco


def t_newLine(t):
  r'\n+'
  t.lexer.lineno += len(t.value)


#Erros:
def t_error(t):
  print(f"Caractere inválido '{t.value[0]}' na linha {t.lineno}")
  t.lexer.skip(1)

#Adições -------------------------------------------------------------------
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VARIAVEL(t):
    r'[a-zA-Z]+'
    return t
  #-------------------------------------------------------------------


#  Construindo o analisador lexico
lexer = lex.lex(debug=True)

#  Construindo o parser
parser = yacc.yacc(debug = True)

#Definindo as regras de expressão



def p_programa(p): #ADD #NECESSÁRIO???
    #'programa : cmds NOTA:
    'programa : cmds'
    p[0] = ('programa', p[1])

def p_num(p): #ADD
  '''num : NUMBERS
           | ID'''
  p[0] = p[1]


#Varlist - define a lista de variaveis que serão utilizadas no programa
#Variavel Unica - varlist = ID


def p_var(p): #ADD
  'varlist : ID'
  #Só uma var
  p[0] = p[1]


#Lista de var separada por virgula


#Sequencia de comandos - cmds : cmd cmds
def p_cmds(p):
    '''cmds : cmd cmds
            | cmd'''
    if len(p) == 3:
        p[0] = p[1] + p[2]  # Lista de comandos
    else:
        p[0] = p[1]


#Comando Unico - cmd : cmd2
def p_cmd(p):
    '''cmd : atribuicao
           | impressao
           | operacao
           | repeticao
           | condicional'''
    p[0] = p[1]

def p_atribuicao(p): #NOTAS:Correto?
    '''atribuicao : FACA VAR SER NUM PONTO
                  | FACA VAR SER VAR PONTO'''
    x1= p[2]
    x2= p[4]
    p[0] = f'{x1}={x2};'

def p_impressao(p): #Print para variáveis
    '''impressao : MOSTRE VAR PONTO
                 | MOSTRE NUM PONTO'''
    imprimido = p[2]
    p[0] = f'printf ({imprimido});'

#Há como juntar todas as somas?
def p_operacao_soma(p):
    '''operacao : SOME VAR COM VAR PONTO
                | SOME VAR COM NUM PONTO
                | SOME NUM COM VAR PONTO
                | SOME NUM COM NUM PONTO'''
    operador1 = p[2]
    operador2 = p[4]
    p[0] = f'{operador1} = {operador1} + {operador2};'
    #p[0] = ('soma', p[2], p[4])

#Considerar para tabela
# def execute_soma(operando1, operando2):
#     valor1 = obter_valor(operando1)
#     valor2 = obter_valor(operando2)
#     if isinstance(operando1, str):  # Se é uma variável
#         tabela_variaveis[operando1] = valor1 + valor2
#     else:
#         print("Erro: O primeiro operando deve ser uma variável para armazenar o resultado.")

def p_operacao_multiplique(p):
    '''operacao : MULTIPLIQUE VAR POR VAR PONTO
                | MULTIPLIQUE VAR POR NUM PONTO
                | MULTIPLIQUE NUM POR VAR PONTO
                | MULTIPLIQUE NUM POR NUM PONTO'''
    operador1 = p[2]
    operador2 = p[4]
    p[0] = f'{operador1} = {operador1} * {operador2};'
    #p[0] = ('multiplicacao', operador1, operador2) #Perguntar
    #p[0] = ('multiplicacao', p[2], p[4]) #Opção 1 ou Opção 2?

contador = 0
def p_repeticao(p): #Checar se esta correto
    '''repeticao : REPITA NUM VEZES DOISPONTOS cmds FIM
                 | REPITA VAR VEZES DOISPONTOS cmds FIM'''
    #cmds_indentado = "\n\t".join(p[5].split("\n"))  NOTA: ALTERAR
    #p[0] = f"for i in range({p[2]}):\n\t" + cmds_indentado NOTA: ALTERAR
    numero_vezes = p[2]
    comandos = p[5]
    p[0] = f'for(int i_{contador}=0;i_{contador}<{numero_vezes};i_{contador}++)' + '{' + f'{comandos}' + '}'
    contador+=1
    #codigo_comandos = '\n'.join(comandos)
    #p[0] = ('repeticao', numero_vezes, comandos)

def p_condicional_se(p):
    '''condicional : SE condicao ENTAO cmds FIM
                   | SE NUM ENTAO cmds FIM
                   | SE VAR ENTAO cmds FIM
                   | SE NUM ENTAO cmds SENAO cmds FIM
                   | SE VAR ENTAO cmds SENAO cmds FIM'''
    if isinstance(p[2], str):
       checaTipo = p[2]
    else:
       checaTipo == (p[2 != 0]) #Se for igual a zero, recebe false. Se for diferente de zero, recebe True.
    # if len(p) == 6: # Caso sem SENAO
    #     p[0] = ('condicional_se', p[2], p[4])
    # else:
    #     # Caso com SENAO
    #     p[0] = ('condicional_se_senao', p[2], p[4], p[6])

    p[0] = ('condicional_se', p[2], p[4])

#ALTENATIVAMENTE
# def p_condicional_se(p):
#     'condicional : SE condicao ENTAO cmd FIM'
#     p[0] = ('condicional_se', p[2], p[4])

# def p_condicional_se_senao(p):
#     'condicional : SE condicao ENTAO cmd SENAO cmd FIM'
#     p[0] = ('condicional_se_senao', p[2], p[4], p[6])

# def p_error(p):
#     if p:
#         print(f"Erro de sintaxe próximo ao token '{p.value}' na linha {p.lineno}")
#     else:
#         print("Erro de sintaxe no final da entrada")


#Erro de sintaxe
def p_error(p):
  print("Erro de sintaxe"+ str(p))

parser = yacc(debug=True)

nomeArq="NomeDoArquivo.txt"
with open(nomeArq, "r") as file:
        data = file.read() #Armazena a data do arquivo que sera "traduzido"


lexer.input(data)
for tok in lexer:
  print(tok)

result = parser.parse(data)
#if result == True:
  #print("Código gerado com sucesso para {nomeArq}"")
  #export_to_obj(result,nomeArq)
#print(result)




# def indent_python_code(code):
#   # Divide as linhas em colunas, cada item é uma linha
#   lines = code.strip().split('\n')
#   # Manter a indentação da última linha
#   indented_code = []
#   indent_level = 0
#   # Nível de indentação do último if
#   #Evitar o problema com o else
#   last_if_indent_level = 0
#   # Ajeita a indentação de acordo com a quantidade de \n - Maneira de arruma a identação
#   previous_line_empty = False

#   for line in lines:
#       stripped_line = line.strip()

#       # Caso tenha \n\n volta 1 nível
#       if not stripped_line:
#           if previous_line_empty:
#               indent_level -= 1
#           previous_line_empty = True
#           continue
#       else:
#           previous_line_empty = False

#       # Se a linha atual contém 'return', ajusta a indentação para 1
#       if 'return' in stripped_line:
#           # Teremos apenas um retorno por função e ele sempre ficará na indentação correta
#           indented_code.append('    ' * 1 + stripped_line)
#           continue

#       # Verifica se a linha atual é 'else:', 'elif:', 'except:', ou 'finally:'
#       # Esses precisam estar no mesmo nível que o bloco anterior
#       if stripped_line.split()[0] in ['else:', 'elif:', 'except:', 'finally:']:
#           indent_level = last_if_indent_level

#       # Adiciona a linha com a indentação correta
#       indented_code.append('    ' * indent_level + stripped_line)

#       # Verifica se a linha atual termina com ':'
#       # Toda vez que temos um : precisamos incrementar a indentação
#       if stripped_line[-1] == ':':
#           # Se a linha atual é 'if', salva o nível de indentação
#           if stripped_line.startswith('if'):
#               last_if_indent_level = indent_level
#           indent_level += 1

#   # Junta as linhas novamente
#   return '\n'.join(indented_code)

# result = indent_python_code(result)


def add_print(code, armazena):
  # Dividir o código em linhas
  lines = code.split('\n')

  # Lista para armazenar as novas linhas de código
  new_lines = []

  # Percorrer cada linha e verificar se alguma variável é atualizada
  for line in lines:
      new_lines.append(line)
      stripped_line = line.strip()
      for var in armazena:
          #Vejo se possuo Z = ...
          if stripped_line.startswith(var + " ="):
              # Determinar a indentação da linha
              #Linha segue a id da ultima
              indent = line[:len(line) - len(line.lstrip())]
              # Adicionar a linha de impressão com a indentação correta
              new_lines.append(f"{indent}print({var})")

  # Juntar as linhas novamente em uma única string
  new_lines.append("\n\nfunc()")
  new_code = '\n'.join(new_lines)
  return new_code


#Normalizando a lista de variaveis
#Separando cada var em um elemento da lista
#data=data.split(',')
#Strip - Tira espaços em branco

print(result)

#Seção para exportar o meu código teste

def export_to_obj(code, file_name):
  with open(file_name, 'w') as file:
    file.write(code)
  print("Compilado com sucesso!")

export_to_obj(result, 'Exemplo.py')
