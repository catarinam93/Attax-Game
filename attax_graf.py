#Catarina Monteiro - PL3
import math
import time
import copy
from os import system
import sys, pygame
pygame.init()

#Constantes utilizadas
class Constantes:
    SIZE = 600 #tamanho da janela gráfica
    NTABS = 6 #número de tabuleiros disponíveis
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)  

#Operadores
class movimento:
    def __init__(self, xi = 0, yi = 0, xf = 0, yf = 0, jog = 0, tipo = 0):
        self.xi = xi #coordenadas iniciais
        self.yi = yi
        self.xf = xf #coordenadas finais
        self.yf = yf
        self.jog = jog
        self.tipo = tipo

#Estado do Jogo/Tabuleiro
class Metodos:
    nMovs = 0 
    N = 8 # N - tamanho Tabul usado
    screen = pygame.Surface((0,0))
    sq = (math.trunc(Constantes.SIZE / float(N)))

    @staticmethod
    def copia(tabuleiro):
       return copy.deepcopy(tabuleiro)

    # Dado o jogador atual retorna qual o outro jogador
    @staticmethod
    def outroJog(jog):
        if jog == 1:
            return 2
        else:
            return 1

    # Assinala (ou desassinala tipo=0) uma quadricula x,y
    @staticmethod
    def assinala_quad(x, y, atip):
        col = Constantes.WHITE
        if atip == 1:
            col = Constantes.BLACK
        elif atip == 2:
            col = Constantes.RED

        pygame.draw.circle(Metodos.screen, col, (x*Metodos.sq+5, y*Metodos.sq+5), 4)
        pygame.draw.circle(Metodos.screen, col, (x*Metodos.sq+Metodos.sq-5, y*Metodos.sq+5), 4)
        pygame.draw.circle(Metodos.screen, col, (x*Metodos.sq+5, y*Metodos.sq+Metodos.sq-5), 4)
        pygame.draw.circle(Metodos.screen, col, (x*Metodos.sq+Metodos.sq-5, y*Metodos.sq+Metodos.sq-5), 4)

    # Mostra o tabuleiro em modo grafico
    @staticmethod
    def mostra_tabul(tabuleiro):
        cor = Constantes.BLACK
        i = 0
        while i<Metodos.N:
            j = 0
            while j<Metodos.N:
                cor = Constantes.WHITE
                if tabuleiro[i][j] == 8:
                    cor = Constantes.BLACK
                pygame.draw.rect(Metodos.screen, cor, pygame.Rect(j*Metodos.sq+1, i*Metodos.sq+1, Metodos.sq-1, Metodos.sq-1)) #quadrado preto/branco
                if tabuleiro[i][j] == 1 or tabuleiro[i][j] == 2:
                    if tabuleiro[i][j] == 1:
                        cor = Constantes.BLUE
                    else:
                        cor = Constantes.GREEN
                    pygame.draw.circle(Metodos.screen, cor, (j*Metodos.sq+Metodos.sq/2, i*Metodos.sq+Metodos.sq/2), (Metodos.sq/2) - 2) #peca
                j += 1
            i += 1
    
    # Lê o jogo do ficheiro
    @staticmethod
    def le_jogo(tabuleiro, nome):
        try:
            with open(nome, "r") as fich:
                primeira = True
                i = -1
                for line in fich:
                    if primeira:
                        Metodos.N = int(line)
                        Metodos.sq = math.trunc(Constantes.SIZE / float(Metodos.N))
                        primeira = False
                    else:
                        tabuleiro[i] = list(map(int, line.split()))
                    i +=1
        except IOError:
            print("Impossivel ler {0}".format(nome))

    # Grava o estado do jogo num ficheiro
    @staticmethod
    def grava_jogo(tabuleiro):
        try:
            with open("jogo.txt", "w") as fich:
                fich.write(Metodos.N + "\n")
                i = 0
                while i<Metodos.N:
                    j = 0
                    while j<Metodos.N:
                        fich.write(tabuleiro[i][j])
                        j += 1
                    fich.write("\n")
                    i += 1
        except IOError:
            print("Impossivel gravar jogo.txt")

    # Inicializa o Tabuleiro lendo sucessivamente os varios tabs de ficheiros
    def inicia_tabul(tabuleiro):
        nome = list("tabX.txt")
        num = 1
        condition = True
        while condition:
            nome[3]=num #Exemplo tab2.txt
            Metodos.le_jogo(tabuleiro, "".join([str(elem) for elem in nome]))
            Metodos.screen.fill(Constantes.BLACK)
            Metodos.mostra_tabul(tabuleiro)
            num += 1
            if num> Constantes.NTABS:
                num = 1
            pygame.display.update()
            start = time.time()
            while time.time() - start < 1: #esperar 1 segundo pelo click até passar ao próximo
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        condition = False
        print("tabuleiro escolhido ", num)

    # Pede ao utlizador que escolha um dos modos de jogo possíveis e a sua dificuldade se for o caso
    @staticmethod
    def tipo_jogo():
        return int(input("Jogo de Attax\nEscolha o modo de jogo: \n1-Hum/Hum 2-Hum/PC 3-PC/Hum 4-PC/PC 5-Hum/MiniMax 6-MiniMax/MiniMax\n")) #2,3,4 o pc joga aleatório; 5,6 o pc usa o algoritmo minimax

    @staticmethod
    def dificuldade(jog):
        return int(input("\nEscolha a dificuldade do jogador " + str(jog) + ": \n1 - Fácil (depth 1), 2 - Intermédio (depth 2), 3 - Díficil (depth 3)\n")) #caso se tenha escolhido a opção 5 ou 6

    # Finaliza o jogo indicando quem venceu ou se foi empate
    @staticmethod
    def finaliza(venc):
        Metodos.screen.fill(Constantes.BLACK)
        pygame.display.update()
        font = pygame.font.SysFont(None, 24)
        img = pygame.Surface((0,0))
        
        if venc == 0:
            img = font.render("Empate!!!\n", True, Constantes.RED)
        elif venc == 1:
            img = font.render("Venceu o Jogador 1 - Azul!", True, Constantes.BLUE)
        else:
            img = font.render("Venceu o Jogador 2 - Verde!", True, Constantes.GREEN)
        Metodos.screen.blit(img, (Constantes.SIZE/2-100, Constantes.SIZE/2))
        pygame.display.update()

    # Indica se (x,y) está dentro do tabuleiro
    @staticmethod
    def dentro(x, y):
        return (x>=0 and x<=Metodos.N-1 and y>=0 and y<=Metodos.N-1)

    # Indica se mov se verifica entre duas coordenadas adjacentes a 1 ou 2 de distancia
    @staticmethod
    def adjacente(mov, dist):
        return (abs(mov.xi-mov.xf)==dist and abs(mov.yi-mov.yf)<=dist or abs(mov.yi-mov.yf)==dist and abs(mov.xi-mov.xf)<=dist)
    
    #indica se mov é um movimento valido e qual o seu tipo
    @staticmethod
    def movimento_valido(tabuleiro, mov):
        if (not Metodos.dentro(mov.xi, mov.yi)) or not Metodos.dentro(mov.xf, mov.yf):
            return False #fora do tabuleiro
        if tabuleiro[mov.yi][mov.xi]==mov.jog and tabuleiro[mov.yf][mov.xf]==0 and Metodos.adjacente(mov, 1):
            mov.tipo = 0
            return True #expansao da peca
        if tabuleiro[mov.yi][mov.xi]==mov.jog and tabuleiro[mov.yf][mov.xf]==0 and Metodos.adjacente(mov, 2):
            mov.tipo = 1
            return True #movimento da peca
        return False

    #converte as peças adjacentes
    def multiplica(tabuleiro, mov):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if mov.yf+dy >= 0 and mov.yf+dy < Metodos.N and mov.xf+dx >= 0 and mov.xf+dx < Metodos.N and tabuleiro[mov.yf+dy][mov.xf+dx]==Metodos.outroJog(mov.jog):
                    tabuleiro[mov.yf+dy][mov.xf+dx]=mov.jog

    # Executa o movimento mov do tipo tipo
    def executa_movimento(tabuleiro, mov):
        tabuleiro[mov.yf][mov.xf] = mov.jog
        if mov.tipo==1:
            tabuleiro[mov.yi][mov.xi] = 0 #movimento
        Metodos.multiplica(tabuleiro, mov)

    #Heurística
    def conta_pecas(tabuleiro, num):
        cp = 0
        i = 0
        while i<Metodos.N:
            j = 0
            while j<Metodos.N:
                if tabuleiro[i][j]==num:
                    cp += 1
                j += 1
            i += 1
        return cp

    # Função de Avaliação
    def avalia(tabuleiro, jog):
        return Metodos.conta_pecas(tabuleiro, jog)-Metodos.conta_pecas(tabuleiro, Metodos.outroJog(jog))

    # Movimento do Computador - Joga Aleatorio
    def jogada_PC(tabuleiro, jog):
        mov = movimento(0,0,0,0,jog,0)
        bestmov = movimento()
        bestav = -1000
        
        print("\nAnálise\n")
        yi = 0
        while yi<Metodos.N:
            xi = 0
            while xi<Metodos.N:
                yf = 0
                while yf<Metodos.N:
                    xf = 0
                    while xf<Metodos.N:
                        mov.yi = yi
                        mov.xi = xi
                        mov.yf = yf
                        mov.xf = xf
                        if Metodos.movimento_valido(tabuleiro, mov):
                            aux = Metodos.copia(tabuleiro)
                            Metodos.executa_movimento(aux, mov)
                            av = Metodos.avalia(aux, jog)
                            if av>=bestav:
                                bestav = av
                                bestmov = copy.deepcopy(mov)
                            print("{0:d} {1:d} -> {2:d} {3:d} ({4:d}): {5:d}".format(mov.yi+1, mov.xi+1, mov.yf+1, mov.xf+1, mov.tipo, av))
                        xf += 1
                    yf += 1
                xi += 1
            yi += 1
        print("\nJogada efetiva\n{0:d} {1:d} -> {2:d} {3:d} ({4:d}): {5:d}".format(bestmov.yi+1, bestmov.xi+1, bestmov.yf+1, bestmov.xf+1, bestmov.tipo, bestav))
        Metodos.executa_movimento(tabuleiro, bestmov)
        time.sleep(0.3)

    #Jogada PC - Usa minimax
    def jogada_PC_MiniMax(tabuleiro, jog, dificuldade):
        bestmov = movimento()
        bestmov = Metodos.minimax(Metodos.copia(tabuleiro), dificuldade, jog == 1, -math.inf, math.inf)[1]
        if bestmov is not None:
            Metodos.executa_movimento(tabuleiro, bestmov)

    #Minimax
    def minimax(state, depth, playerMax, alpha, beta):
        print("depth {0}, playerMax {1: <1}, alpha {2: <4}, beta {3: <3}".format(depth, playerMax, alpha, beta), end="\r")

        if depth==0 or Metodos.fim_jogo(state, 1 if playerMax else 2) >= 0: 
            return (Metodos.avalia(state, 1), None) # avalia sempre o jog 1

        movs = [movimento() for _ in range(500)]
        best_move = movimento()

        if playerMax:
            maxEval = -math.inf
            count = Metodos.jogadas_validas(state, 1, movs)
            for i in range(count):
                aux = Metodos.copia(state)
                Metodos.executa_movimento(aux, movs[i])
                evaluation = Metodos.minimax(aux, depth-1, False, alpha, beta)
                maxEval = max(maxEval, evaluation[0])
                if maxEval == evaluation[0]:
                    best_move = movs[i]
                alpha = max(alpha, evaluation[0])
                if beta <= alpha: break
            return (maxEval, best_move)

        minEval = math.inf
        count = Metodos.jogadas_validas(state, 2, movs)
        for i in range(count):
            aux = Metodos.copia(state)
            Metodos.executa_movimento(aux, movs[i])
            evaluation = Metodos.minimax(aux, depth-1, True, alpha, beta)
            minEval = min(minEval, evaluation[0])
            if minEval == evaluation[0]:
                best_move = movs[i]
            beta = min(beta, evaluation[0])
            if beta <= alpha: break
        return (minEval, best_move)

    #Determina todas as jogadas validas de um jogador
    @staticmethod
    def jogadas_validas(tabuleiro, jog, movs, tipoAss = 0):
        nmovs = 0
        i = 0
        while i<Metodos.N:
            j = 0
            while j<Metodos.N:
                if tabuleiro[i][j]== jog:
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            movs[nmovs].jog = jog
                            movs[nmovs].yi = i
                            movs[nmovs].xi = j
                            movs[nmovs].yf = i+k
                            movs[nmovs].xf = j+l
                            if Metodos.movimento_valido(tabuleiro, movs[nmovs]):
                                #Metodos.assinala_quad(j+l,i+k,tipoAss) #assinala as jogadas possíveis do computador mas, por uma questão de gestão de tempo/memória foi deixado comentado
                                nmovs += 1
                j += 1
            i += 1
        #pygame.display.update()
        #time.sleep(0.5)
        return nmovs

    #Determina todas as jogadas validas de uma dada peça
    @staticmethod
    def jogadas_validas_pos(tabuleiro, jog, xi, yi, movs, tipoAss):
        nmovs = 0
        if tabuleiro[yi][xi]== jog:
            k = 0
            while k<Metodos.N:
                l = 0
                while l<Metodos.N:
                    movs[nmovs].jog = jog
                    movs[nmovs].yi = yi
                    movs[nmovs].xi = xi
                    movs[nmovs].yf = k
                    movs[nmovs].xf = l
                    if Metodos.movimento_valido(tabuleiro, movs[nmovs]):
                        Metodos.assinala_quad(l,k,tipoAss)
                        nmovs += 1
                    l += 1
                k += 1
        return nmovs
     
    # Verificar se o jogo terminou retornando o vencedor
    @staticmethod
    def fim_jogo(tabuleiro, jog):
        movs = [movimento() for _ in range(500)]
        if Metodos.jogadas_validas(tabuleiro, Metodos.outroJog(jog), movs, Metodos.outroJog(jog)) > 0:
            return -1 #existem jogadas
        if Metodos.avalia(tabuleiro, jog)>0:
            return jog
        elif Metodos.avalia(tabuleiro, jog)<=0:
            return Metodos.outroJog(jog)
        else:
            return 0 #empate
    
    # Jogada do Humano 
    @staticmethod
    def jogada_Humano(tabuleiro, jog):
        movs = [movimento() for _ in range(500)]
        mov = movimento(0,0,0,0,jog)
        px = 0
        py = 0
        cl = 0
        condition = True
        while condition:
            pygame.event.get()
            pos = pygame.mouse.get_pos()
            px = math.trunc(pos[0]/Metodos.sq) # ou será round()
            py = math.trunc(pos[1]/Metodos.sq) # ou será round()
            if pygame.mouse.get_pressed()[2]:
                Metodos.le_jogo("jogo.txt")
                Metodos.screen.fill(0,0,0)
                Metodos.mostra_tabul()
            if pygame.mouse.get_pressed()[1]:
                Metodos.grava_jogo()
                Metodos.mostra_tabul()
            if pygame.mouse.get_pressed()[0]:
                if cl == 0 and tabuleiro[py][px]==jog:
                    cl = 1
                    mov.xi=px
                    mov.yi=py
                    Metodos.assinala_quad(px,py,1)
                    Metodos.jogadas_validas_pos(tabuleiro, jog, px, py, movs,1)
                elif cl == 1:
                    cl = 0
                    mov.xf=px
                    mov.yf=py
                    Metodos.assinala_quad(mov.xi,mov.yi,0)
                    Metodos.jogadas_validas_pos(tabuleiro, jog, mov.xi, mov.yi, movs,0)
            pygame.display.update()
            time.sleep(0.1)
            condition = cl == 1 or not Metodos.movimento_valido(tabuleiro, mov)
        Metodos.executa_movimento(tabuleiro, mov)

    # Dependendo do modo de jogo e do numero da jogada pede uma jogada ao humano ou calcula uma jogada para o PC
    def jogada(tabuleiro, n, jog, tJog, dificuldade, dificuldade1):
        if math.fmod(n, 2) == 1:
            if tJog<=2 or tJog == 5:
                Metodos.jogada_Humano(tabuleiro, jog)
            else:
                if tJog != 6:
                    Metodos.jogada_PC(tabuleiro, jog)
                else:
                    Metodos.jogada_PC_MiniMax(tabuleiro, jog, dificuldade1)
        else:
            if tJog == 1 or tJog == 3:
                Metodos.jogada_Humano(tabuleiro, jog)
            else:
                if tJog == 2 or tJog == 4:
                    Metodos.jogada_PC(tabuleiro, jog)
                else:
                    Metodos.jogada_PC_MiniMax(tabuleiro, jog, dificuldade)

# Função principal 
def main():
    fim = -1
    jog = 0

    Metodos.screen = pygame.display.set_mode((Constantes.SIZE,Constantes.SIZE))
    pygame.display.set_caption ('ATTAX')
    tabuleiro = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []] # tabuleiro: 0-vazio, 1-peça jog1, 2-peça jog2, 8-impossivel

    while  True:
        Metodos.nMovs = 0
        tipo = Metodos.tipo_jogo() 
        dificuldade = 0
        dificuldade1 = 0
        if tipo == 6:
            dificuldade1 = Metodos.dificuldade(1)
        if tipo == 5 or tipo == 6:
            dificuldade = Metodos.dificuldade(2)

        Metodos.inicia_tabul(tabuleiro) # inicializa o tabuleiro
        condition = True
        while condition:
            Metodos.nMovs += 1
            jog = Metodos.outroJog(jog) # incrementa jogada e troca de jogador
            print("Attax Jogada No: {0:d}  Jogador: {1:d}, Aval: {2:d}".format(Metodos.nMovs, jog, Metodos.avalia(tabuleiro, jog)))
            Metodos.mostra_tabul(tabuleiro) # mostra o tabuleiro no ecran

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()

            Metodos.jogada(tabuleiro, Metodos.nMovs, jog, tipo, dificuldade, dificuldade1) # executa jogada Humano/PC
            fim = Metodos.fim_jogo(tabuleiro, jog) # verifica se o jogo acabou
            condition = fim == -1

        #Mostrar estado final do jogo
        Metodos.mostra_tabul(tabuleiro)
        pygame.display.update()
        time.sleep(3) # 3 segundos
        #Mostrar vencedor
        Metodos.finaliza(fim) # mostra quem venceu o jogo
        system("pause")

if __name__ == "__main__":
    main()