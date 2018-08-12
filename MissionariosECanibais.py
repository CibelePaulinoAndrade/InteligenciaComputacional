#Cibele Paulino Andrade
#Curso: Engenharia de Computação
#Disciplina: Inteligência Computacional

#Atividade: Problema dos Missionários e Canibais
#Descrição: Você deve ajudar a travessia dos missionários e dos canibais até o outro lado do rio.
#########Os missionários não podem ficar em menor número, em qualquer uma das margens, ou os canibais os devorarão.

class Margem ():
    #Guarda os valores possiveis para as margens
    
    esquerda = 0
    direita = 1

class Cenario ():
    
    def __init__(self, missionariosEsq, canibaisEsq, missionariosDir, canibaisDir, margemBarco):
        #---------------------------------------------------------------------------------------#
        
        self.missionariosEsq = missionariosEsq
        self.canibaisEsq = canibaisEsq
        self.missionariosDir = missionariosDir
        self.canibaisDir = canibaisDir
        self.margemBarco = margemBarco
        
        self.anterior = None
        self.posterior = []

    def validacaoParcialDoCenario(self):
        #Verifica se a quantidade de cada grupo em cada margem não são negativos
        #e se não existem mais canibais que missionários em alguma das margens

        if ((self.missionariosEsq < 0) or (self.canibaisEsq < 0) or (self.missionariosDir < 0) or (self.canibaisDir < 0)):
            return False

        if ((self.missionariosEsq == 0) or (self.missionariosEsq >= self.canibaisEsq)):
            if ((self.missionariosDir == 0) or (self.missionariosDir >= self.canibaisDir)):
                return True

    def validacaoFinaldoCenario (self) :
        #Verifica se todos os missionários e todos os canibais se encontram na margem direita
        #(considero a margem esquerda como inicial)

        if ((self.missionariosEsq == self.canibaisEsq == 0) and (self.missionariosEsq == self.canibaisEsq == 0)):
            if ((self.missionariosDir == self.canibaisDir == 3) and (self.missionariosDir == self.canibaisDir == 3)):
                return True

        else:
            return False

    def buscaCenario (self):
        #Procura por possíveis caminhos para solução do problema

        if (self.margemBarco == Margem.direita):
            novaMargemBarco = Margem.esquerda
        else:
            novaMargemBarco = Margem.direita

        acoesPossiveis = [
            {'m' : 2, 'c' : 0},             #2 missionarios
            {'m' : 1, 'c' : 0},             #1 missionario 
            {'m' : 1, 'c' : 1},             #1 missionario + 1 canibal
            {'m' : 0, 'c' : 2},             #2 canibais
            {'m' : 0, 'c' : 1},             #1 canibal
            ]

        for acoes in acoesPossiveis :
            if self.margemBarco == Margem.direita:
                novoMissionariosEsq = self.missionariosEsq + acoes['m']
                novoCanibaisEsq = self.canibaisEsq + acoes['c']
                novoMissionariosDir = self.missionariosDir - acoes['m']
                novoCanibaisDir = self.canibaisDir - acoes['c']

            else:
                novoMissionariosEsq = self.missionariosEsq - acoes['m']
                novoCanibaisEsq = self.canibaisEsq - acoes['c']
                novoMissionariosDir = self.missionariosDir + acoes['m']
                novoCanibaisDir = self.canibaisDir + acoes['c']

            cenario = Cenario (novoMissionariosEsq, novoCanibaisEsq, novoMissionariosDir, novoCanibaisDir, novaMargemBarco)
            cenario.anterior = self

            if cenario.validacaoParcialDoCenario():
                self.posterior.append(cenario)
                
    def pegaAnterior (self):
        #Pega o cenario anterior ao atual
        solucao = []
        cenario = self
        
        while cenario.anterior:
            
            solucao.insert(0, cenario.anterior)
            cenario = cenario.anterior

        return solucao

    def __str__(self):
        #imprime o cenário
        
        return "Esq.: M = {}, C = {}".format(self.missionariosEsq, self.canibaisEsq) + "\nDir.: M = {}, C = {}".format(self.missionariosDir, self.canibaisDir) + "\n"
        
    

class MissionariosECanibais():
    #Retorna a primeira solução encontrada que resolve o problema

    def __init__(self):
        #-------------#
        cenarioInicial = Cenario(3, 3, 0, 0, Margem.esquerda)
        self.cenarios = [cenarioInicial]
        self.solucaoPossivel = []

    def procuraSolucao(self):
        #Para cada cenario procura cenarios posteriores validos. Se o cenario for a meta do desafio ele adiciona no array possivelCenario
        
        for possivelCenario in self.cenarios:
            
            if (possivelCenario.validacaoFinaldoCenario()):
                self.solucaoPossivel.append(possivelCenario)

                self.solucaoPossivel = possivelCenario.pegaAnterior() + self.solucaoPossivel

                return 

            possivelCenario.buscaCenario()
            self.cenarios.extend(possivelCenario.posterior)
        


problema = MissionariosECanibais()
problema.procuraSolucao()

for cenario in problema.solucaoPossivel:
    print(cenario)
    

    

        


               
               
               
