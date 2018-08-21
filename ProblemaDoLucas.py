Cibele Paulino Andrade
#Curso: Engenharia de Computação
#Disciplina: Inteligência Computacional

#Atividade: Problema do Lucas
#Descrição: Todas os sapos devem terminar no lado oposto ao que começaram
#OBS: O exemplo usado em sala de aula usava SETAS no lugar de SAPOS

import copy

class Time:
    AZUL = 1
    ROSA = -1 

class Sapo:
    def __init__(self, time, lagoa):
        self.time = time           #Considera-se do mesmo time todos os sapos que começaram juntos de um mesmo lado
        self.lagoa = lagoa

    def proximaPosicao(self, posicaoAtualSapo):
        #Verifica se pode andar. Se tiver um espaço alcançavel, e esse espaço
        #não tiver ninguém do mesmo time(além dele mesmo) ao redor, ele pode andar.
        #Começa a analisar as possibilidades pelo sapo mais proximo do destino,
        #segue-se analisando os sapos do mesmo lado até não haver mais movimentos possivéis.
        

        posicaoEspacoVazio = None

        if self.lagoa.espacos[posicaoAtualSapo + self.time].sapo == None:
            posicaoEspacoVazio = posicaoAtualSapo + self.time
        elif self.lagoa.espacos[posicaoAtualSapo + 2*self.time].sapo == None:
            posicaoEspacoVazio = posicaoAtualSapo + 2*self.time
            
        if posicaoEspacoVazio == None:
            return posicaoAtualSapo

        #checa se existe posições depois do espaço vazio
        if self.lagoa.estaNosLimites(posicaoEspacoVazio + self.time) == False:
            return posicaoEspacoVazio

        if self.lagoa.espacos[posicaoEspacoVazio + self.time].sapo.time == self.time:
            return posicaoAtualSapo

        return posicaoEspacoVazio

    def saltar(self, posicaoOrigem, posicaoDestino):
        
        sapoAtual = self.lagoa.espacos[posicaoOrigem].sapo
        self.lagoa.espacos[posicaoOrigem].sapo = None
        self.lagoa.espacos[posicaoDestino].sapo = sapoAtual

        #eh o sapo do time, entao muda variavel da lagoa
        if posicaoOrigem == self.lagoa.posiceosPrimeirosSapos[self.time]:
            self.lagoa.posiceosPrimeirosSapos[self.time] = posicaoDestino

            #se o primeiro sapo chegou no limite atualiza os limites da lagoa
            if posicaoDestino == self.lagoa.limites.inicio:
                self.lagoa.limites.inicio += 1

                #atualiza primeiro sapo
                self.lagoa.atualizaPrimeirosDoTime(self.time)
            elif posicaoDestino == self.lagoa.limites.fim - 1:
                self.lagoa.limites.fim -= 1

                #atualiza primeiro sapo
                self.lagoa.atualizaPrimeirosDoTime(self.time)
                
    def __str__(self):
        return "AZUL" if self.time == Time.AZUL else "ROSA"
        
class Espaco:
    def __init__(self, sapo = None):
        self.sapo = sapo

    def __str__(self):
        return "["+ (self.sapo.__str__() if self.sapo != None else "    ") + "]"    

class LimitesLagoa:
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim

class Lagoa:
    def __init__(self, qntSapos = 4):

        self.espacos = []
        for sapo in range(qntSapos):
            self.espacos.append(Espaco(Sapo(Time.AZUL, self)))
        self.espacos.append(Espaco())
        for sapo in range(qntSapos):
            self.espacos.append(Espaco(Sapo(Time.ROSA, self)))
        
        self.limites = LimitesLagoa(0, len(self.espacos))
        
        self.posiceosPrimeirosSapos = {
            Time.AZUL : qntSapos - 1,
            Time.ROSA : qntSapos + 1
        }

    def estaNosLimites(self, posicao):
        if posicao >= self.limites.inicio and posicao < self.limites.fim:
            return True
        else:
            return False

    def atualizaPrimeirosDoTime(self, time):
        posicaoProximoPrimeiroSapo = self.posicaoDoAnteriorDoTime(self.posiceosPrimeirosSapos[time])
        if posicaoProximoPrimeiroSapo != None:
            self.posiceosPrimeirosSapos[time] = posicaoProximoPrimeiroSapo
    
    def posicaoDoAnteriorDoTime(self, posicaoSapoAtual):
        #Acha o proximo sapo a ser verificado do time atual

        sapoAtual = self.espacos[posicaoSapoAtual].sapo

        posicaoFim = self.limites.inicio -1 if sapoAtual.time == Time.AZUL else self.limites.fim
        for posicaoCorrente in range(posicaoSapoAtual - sapoAtual.time, posicaoFim, -sapoAtual.time):
            if self.estaNosLimites(posicaoCorrente):
                if self.espacos[posicaoCorrente].sapo != None: 
                    if self.espacos[posicaoCorrente].sapo.time == sapoAtual.time:
                        return posicaoCorrente
        return None


    def computarRodada(self, time):
        #Faz uma rodada do time atual enquanto houverem jogadas possiveis para ele

        posicaoSapoAtual = self.posiceosPrimeirosSapos[time]
        sapoAtual = self.espacos[posicaoSapoAtual].sapo

        existirPossibilidades = True
        proximaPosicaoSapo = None
        
        while existirPossibilidades:
            proximaPosicaoSapo = sapoAtual.proximaPosicao(posicaoSapoAtual)
            sapoAtual.saltar(posicaoSapoAtual, proximaPosicaoSapo)

            #se nao se moveu
            if proximaPosicaoSapo == posicaoSapoAtual:
                existirPossibilidades = False
            else:
                #procura proximo sapo do mesmo time
                posicaoSapoAtual = proximaPosicaoSapo
                posicaoSapoAtual = self.posicaoDoAnteriorDoTime(posicaoSapoAtual)
                if posicaoSapoAtual != None:
                    sapoAtual = self.espacos[posicaoSapoAtual].sapo
                else:
                    existirPossibilidades = False

    def gerarResultado(self):
        #faz uma rodada para cada time até todos do mesmo time estarem do lado
        #oposto ao que começaram
        #Considera-se uma rodada todos os movimentos possivéis para cada membro do mesmo time

        #Retorna a situação final de cada rodada até atingir a condição final
        
        while self.limites.fim > self.limites.inicio + 1:
            lagoa.computarRodada(Time.AZUL)      
            print(lagoa)
            lagoa.computarRodada(Time.ROSA)      
            print(lagoa)

    def __str__(self):
        lagoaString = ""
        for espaco in self.espacos:
            lagoaString += espaco.__str__()


        return lagoaString     
        
lagoa = Lagoa()
print(lagoa)

lagoa.gerarResultado()

