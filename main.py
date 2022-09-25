import random, datetime, pytz

cartelas_file = open('cartelas.txt')
cartelas = []
cartelas_sorteadas = []
numeros_disponiveis = [i for i in range (1, 51)]
numeros_sorteados = []
cartela_selecionada = 0
cartela_vencedora = None

primeira_jogada = True
trocou_cartela = False
cartela_selecionada_completou = False
outra_cartela_completou = False
fim_de_jogo = False

def extrair_cartelas():
  """Para cada linha no arquivo txt original, remove o control character de quebra de linha, separa os números em strings individuais e adiciona a lista resultante à lista 'cartela'."""
  
  for linha_original in cartelas_file:
      linha = [elemento.rjust(2) for elemento in linha_original.rstrip().split(",")]
      cartelas.append(linha)


def sorteia_cartelas():
  """Sorteia quatro listas da lista 'cartelas' e as adiciona à lista 'cartelas_sorteadas'."""

  for _ in range(4):
    index = random.randint(0, len(cartelas) -1)
    cartelas_sorteadas.append(cartelas[index])


def mostra_header():
  """Exibe o cabeçalho do bingo, que pode conter uma mensagem informando o número sorteado ou a nova cartela escolhida pelo usuário, a depender da última ação tomada."""

  global trocou_cartela
  mensagem = ""
  print()
  if trocou_cartela:
    mensagem = f"VOCÊ AGORA É DONO DA CARTELA {cartela_selecionada+1}"
    trocou_cartela = False
  else:
    mensagem = f"NÚMERO SORTEADO: {numeros_sorteados[-1]} "
  print(74 * "#")
  num_espacos = 72 - len(mensagem)
  print("#" + (num_espacos // 2) * " " + f"{mensagem}" + (num_espacos // 2) * " " + "#")
  print(74 * "#")


def mostra_cartelas():
  """Exibe as cartelas sorteadas, fazendo uso da função 'destacar' para destacar os números sorteados e a cartela vencedora."""

  def destacar(num_cartela):
    """Destaca os números sorteados em cada cartela, e, no fim do jogo, destaca toda a cartela vencedora."""
  
    nonlocal separador
    str_destaque_off = 4 * " "
    if num_cartela == cartela_vencedora:
      str_destaque_titulo = 10 * "*"
      str_destaque_on = 4 * "*"
      separador = "*"
    else:
      str_destaque_titulo = 10 * " "
      str_destaque_on = 4 * "-"
      separador = "|"
  
    print(str_destaque_titulo, end = 2 * " ")
    for i in range(len(cartelas_sorteadas)+1):
      print(str_destaque_on if cartelas_sorteadas[num_cartela][i] in numeros_sorteados else str_destaque_off, end = " ")
    print()

  
  if not primeira_jogada:
    mostra_header()
  indicador_selecao = 35 * "<"
  separador = "|"
  for i in range(len(cartelas_sorteadas)):
      if i == cartela_selecionada:
        destacar(i)
        print("Cartela {0}: {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}  {12}".format(
          i+1,
          separador,
          cartelas_sorteadas[i][0],
          separador,
          cartelas_sorteadas[i][1],
          separador,
          cartelas_sorteadas[i][2],
          separador,
          cartelas_sorteadas[i][3],
          separador,
          cartelas_sorteadas[i][4],
          separador,
          indicador_selecao)
        )
        destacar(i)
      else:
        destacar(i)
        print("Cartela {0}: {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}".format(
          i+1,
          separador,
          cartelas_sorteadas[i][0],
          separador,
          cartelas_sorteadas[i][1],
          separador,
          cartelas_sorteadas[i][2],
          separador,
          cartelas_sorteadas[i][3],
          separador,
          cartelas_sorteadas[i][4],
          separador)
        )
        destacar(i)


def mostra_footer():
  """Exibe o rodapé do bingo, que permite que o usuário escolha entre sortear um novo número ou trocar sua cartela."""
  
  global primeira_jogada, cartela_selecionada, trocou_cartela
  primeira_jogada = False
  cartelas_livres = [i for i in range(0, len(cartelas_sorteadas))]
  cartelas_livres.remove(cartela_selecionada)
  print()
  resposta = input(f"# SELECIONE OUTRA CARTELA ({cartelas_livres[0]+1}, {cartelas_livres[1]+1} ou {cartelas_livres[2]+1}) ou PRESSIONE ENTER PARA SORTEAR: ")
  if resposta == "":
    sorteia_numero()
  else:
    cartela_selecionada = int(resposta) - 1
    trocou_cartela = True

def checa_se_vencedor():
  """Por meio de uma comparação entre as listas 'cartelas_sorteadas' e 'numeros_sorteados', define se o jogo finalizou e altera o valor de variáveis booleanas correspondentes às possibilidades."""
  
  global cartela_selecionada_completou, outra_cartela_completou, cartela_vencedora
  for cartela in range(len(cartelas_sorteadas)):
    acertos = 0
    for num in cartelas_sorteadas[cartela]:
      if num in numeros_sorteados:
        acertos += 1
    if acertos == 5:
      cartela_vencedora = cartela
      if cartela == cartela_selecionada:
        cartela_selecionada_completou = True
      else:
        outra_cartela_completou = True

def sorteia_numero():
  """Sorteia um novo número dentro da lista 'numeros_disponiveis', o remove dessa lista, e adiciona o número à lista 'numeros_sorteados'. Por fim, executa a função 'checa_se_vencedor' para checar se o número sorteado finalizou o jogo."""
  
  num_sorteado = numeros_disponiveis[random.randint(0, len(numeros_disponiveis) -1)]
  numeros_sorteados.append(str(num_sorteado).rjust(2))
  numeros_disponiveis.remove(num_sorteado)
  checa_se_vencedor()


def rol_vencedores():
  """No caso de vitória do jogador, solicita seu nome e o insere no arquivo de texto 'vencedores.txt' com a data e hora atuais no fuso horário BRT."""
  
  vencedores = open("vencedores.txt", "a")
  print("# PARABÉNS! VOCÊ VENCEU!!!")
  nome = input("# Entre o seu nome para constar no rol de vencedores: ")
  timezone = pytz.timezone("Brazil/East")
  data = datetime.datetime.now().astimezone(timezone).strftime("%d/%m/%Y às %H:%M:%S")
  vencedores.write(f"{nome} - {data} (BRT)\n")
  vencedores.close()


extrair_cartelas()
sorteia_cartelas()

while not fim_de_jogo:
  mostra_cartelas()
  mostra_footer()
  fim_de_jogo = cartela_selecionada_completou or outra_cartela_completou
  if fim_de_jogo:
    mostra_cartelas()

if cartela_selecionada_completou:
  rol_vencedores()
else:
  print("""\n# OUTRA CARTELA FOI COMPLETADA!
# Melhor sorte na próxima vez!""")

cartelas_file.close()