# -*- coding: utf-8 -*-

import csv
import random
import math
import operator

#	Para carregar o dataset é preciso que o arquivo contido no link abaixo esteja
#	salvo na mesma pasta do script, com o nome de "iris.data".
#	https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data 
def carregarDataset(nomeArquivo, divisor, setTreinamento=[] , setTeste=[]):
	with open(nomeArquivo, 'rb') as csvfile: #abre um arquivo como csv
	    linhas = csv.reader(csvfile)
	    dataset = list(linhas)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y]) #pega do dataset só os 4 primeiros valores, que são os dados das plantas 
	        if random.random() < divisor: #divide aleatoriamente o dataset em dados de treinamento e dados de teste
	            setTreinamento.append(dataset[x]) 
	        else:
	            setTeste.append(dataset[x])
 

#   Calcula a distância euclidiana entre dois pontos/dados
def distanciaEuclidiana(ponto1, ponto2, tamanho):
	distancia = 0
	for x in range(tamanho):
		distancia += pow((ponto1[x] - ponto2[x]), 2)
	return math.sqrt(distancia)

 
#   Calcula o vizinho mais próximo de um dado, aquele que tem a menor distância
def nearestNeighbor(setTreinamento, instanciaTeste):
	distancias = []
	tamanho = len(instanciaTeste)-1
	for x in range(len(setTreinamento)):
		distancia = distanciaEuclidiana(instanciaTeste, setTreinamento[x], tamanho)
		distancias.append((setTreinamento[x], distancia))
	distancias.sort(key=operator.itemgetter(1))
	vizinho = distancias[0][0]
	return vizinho
 
def respostaCerta(vizinho):
	resposta = vizinho[-1]
	return resposta

def calculaAcuracia(setTeste, predicoes):
	certas = 0
	for x in range(len(setTeste)):
		if setTeste[x][-1] == predicoes[x]:
			certas += 1
	return (certas/float(len(setTeste))) * 100.0
	

setTreinamento=[]
setTeste=[]
divisor = 0.67
carregarDataset('iris.data', divisor, setTreinamento, setTeste)
print 'Set de treinamento: ' + repr(len(setTreinamento))
print 'Set de teste: ' + repr(len(setTeste))

predicoes=[]
for x in range(len(setTeste)):
	vizinho = nearestNeighbor(setTreinamento, setTeste[x])
	resultado = respostaCerta(vizinho)
	predicoes.append(resultado)
	print('> previsto=' + repr(resultado) + ', resultado real=' + repr(setTeste[x][-1]))
acuracia = calculaAcuracia(setTeste, predicoes)
print('Acurácia: ' + repr(acuracia) + '%')
	
