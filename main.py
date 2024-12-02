#Aluno: Felipe Antelo Machado de Oliveira
#Matrícula: 2210872
#Professor: Herrman


#programa - INICIO varlist MONITOR varlist EXECUTE cmds TERMINO
#varlist - id varlist | id
#cmds - cmd cmds | cmd
#cmd - id = id

#varlist -> lista de variaveis separadas por virgula
#INICIO -> Inicio do programa
#MONITOR -> sinaliza o inicio da varlist
#Essas variaveis devem ser impressas
#EXECUTE -> Após ele vem uma sequencia de comandos
#TERMINO -> Termino do programa
#cmd -> ENQUANTO id FACA cmds FIM (loop)
#enquanto id !=0 FACA cmds FIM

#Devemos complementar a linguagem com os comandos:
#IF-THEN e IF-THEN-ELSE
#Eval(num1,num2,cmds): recebe lista de cmds, 2 numeros, executa os
#comandos até que val1 = val2. cada cmd val1 = val1-1

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

from typing import DefaultDict
from ply.lex import lex
from ply.yacc import yacc

global monitor
monitor = []

#Definindo os Tokens:
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
# t_ID = r'(?!IGUAL|INICIO|MONITOR|EXECUTE|TERMINO|ENQUANTO|FIM|FACA|IF|THEN|ELSE|VIRGULA|NUMBERS|SPECIALS|PAR_O|PAR_C|ZERO|EVAL)[a-zA-Z_][a-zA-Z0-9_]*'
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
  print("Caractere Inválido: '%s'" % t.value[0])
  t.lexer.skip(1)

#Adições -------------------------------------------------------------------
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t
  #-------------------------------------------------------------------


#  Construindo o analisador lexico
lexer = lex.lex()

#  Construindo o parser
parser = yacc.yacc(debug = True)

#Definindo as regras de expressão



def p_programa(p):
    #'programa : INICIO varlist MONITOR varlist EXECUTE cmds TERMINO'
    'programa : cmds'
    p[0] = ('programa', p[1])

def p_num(p):
  '''num : NUMBERS
           | ID'''
  p[0] = p[1]


#Varlist - define a lista de variaveis que serão utilizadas no programa
#Variavel Unica - varlist = ID


def p_var(p):
  'varlist : ID'
  #Só uma var
  p[0] = p[1]


#Lista de var separada por virgula
def p_varlist(p):
  'varlist : ID VIRGULA varlist'
  #varlist = ID, varlist
  p[0] = '%s, %s' % (p[1], p[3])


#Sequencia de comandos - cmds : cmd cmds
def p_cmds(p):
    '''cmds : cmd cmds
            | cmd'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Lista de comandos
    else:
        p[0] = [p[1]]


#Comando Unico - cmd : cmd2
def p_cmd(p):
    '''cmd : atribuicao
           | impressao
           | operacao
           | repeticao
           | condicional'''
    p[0] = p[1]

def p_atribuicao(p): #NOTAS:Correto?
    'atribuicao : FACA VAR SER NUM PONTO'
    p[0] = ('atribuicao', p[2], p[4])

#Comando - contas - ID = ID
def p_iguala_var(p):
  'cmd : ID SPECIALS num'
  if p[2] == '=':
      p[0] = '%s = %s\n' % (p[1], p[3])


def p_contas(p):
  'num : num SPECIALS num'
  if p[2] == "+":
    p[0] = '%s + %s' % (p[1], p[3])
  elif p[2] == "*":
    p[0] = '%s * %s' % (p[1], p[3])


#Comando de While - Enquanto id != 0 processa lista de cmds
def p_cmd_enquanto(p):
  'cmd : ENQUANTO ID FACA cmds FIM'
  p[0] = 'while %s:\n%s\n%s = %s -1\n' % (p[2], p[4], p[2], p[2])


#Comando If sem else
def p_cmd_if(p):
  'cmd : IF ID THEN cmds'
  p[0] = 'if %s:\n%s\n' % (p[2], p[4])


#Comando If com else
def p_cmd_if_else(p):
  'cmd : IF ID THEN cmds ELSE cmds'
  p[0] = 'if %s:\n%s\nelse:\n%s\n' % (p[2], p[4], p[6])


def p_cmd_zero(p):
  'cmd : ZERO PAR_O ID PAR_C'
  p[0] = '%s = 0\n' % p[3]


def p_eval(p):
  'cmd : EVAL PAR_O num VIRGULA num VIRGULA cmds PAR_C'
  p[0] = 'while %s != %s:\n%s\n%s = %s - 1\n' % (p[3], p[5], p[7], p[5], p[5])

def p_id_eval(p):
  'cmd : ID SPECIALS EVAL PAR_O num VIRGULA num VIRGULA cmds PAR_C'
  if p[2] == '=':
    p[0] = 'while %s != %s:\n%s%s = %s - 1\n' % (p[5], p[7], p[9], p[7], p[7])


#Erro de sintaxe
def p_error(p):
  print("Erro de Sintaxe\n", p.value)


parser = yacc(debug=True)

data = '''
INICIO X, Y, L
MONITOR Z
EXECUTE
ZERO(Z)
X = 5
Y = 0
L = 1
IF Y THEN
Z = EVAL(X, L, Z=Z*L)
ELSE
Z = EVAL(X, L, Z=Z*X)
TERMINO
'''


lexer.input(data)
for tok in lexer:
  print(tok)

result = parser.parse(data)
#print(result)




def indent_python_code(code):
  # Divide as linhas em colunas, cada item é uma linha
  lines = code.strip().split('\n')
  # Manter a indentação da última linha
  indented_code = []
  indent_level = 0
  # Nível de indentação do último if
  #Evitar o problema com o else
  last_if_indent_level = 0
  # Ajeita a indentação de acordo com a quantidade de \n - Maneira de arruma a identação
  previous_line_empty = False

  for line in lines:
      stripped_line = line.strip()

      # Caso tenha \n\n volta 1 nível
      if not stripped_line:
          if previous_line_empty:
              indent_level -= 1
          previous_line_empty = True
          continue
      else:
          previous_line_empty = False

      # Se a linha atual contém 'return', ajusta a indentação para 1
      if 'return' in stripped_line:
          # Teremos apenas um retorno por função e ele sempre ficará na indentação correta
          indented_code.append('    ' * 1 + stripped_line)
          continue

      # Verifica se a linha atual é 'else:', 'elif:', 'except:', ou 'finally:'
      # Esses precisam estar no mesmo nível que o bloco anterior
      if stripped_line.split()[0] in ['else:', 'elif:', 'except:', 'finally:']:
          indent_level = last_if_indent_level

      # Adiciona a linha com a indentação correta
      indented_code.append('    ' * indent_level + stripped_line)

      # Verifica se a linha atual termina com ':'
      # Toda vez que temos um : precisamos incrementar a indentação
      if stripped_line[-1] == ':':
          # Se a linha atual é 'if', salva o nível de indentação
          if stripped_line.startswith('if'):
              last_if_indent_level = indent_level
          indent_level += 1

  # Junta as linhas novamente
  return '\n'.join(indented_code)

result = indent_python_code(result)


def add_print(code, monitor):
  # Dividir o código em linhas
  lines = code.split('\n')

  # Lista para armazenar as novas linhas de código
  new_lines = []

  # Percorrer cada linha e verificar se alguma variável é atualizada
  for line in lines:
      new_lines.append(line)
      stripped_line = line.strip()
      for var in monitor:
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
monitor = monitor[0].split(',')
#Strip - Tira espaços em branco
monitor = [var.strip() for var in monitor]


result = add_print(result, monitor)
print(result)

#Exportando o codigo em OBJ

def export_to_obj(code, file_name):
  with open(file_name, 'w') as file:
    file.write(code)
  print("Compilado com sucesso!")

export_to_obj(result, 'Exemplo3.py')
