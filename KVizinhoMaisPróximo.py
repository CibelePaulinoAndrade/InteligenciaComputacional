# -*- coding: utf-8 -*-

import csv
import random
import math
import operator

#	Para carregar o dataset é preciso que o arquivo contido no link abaixo esteja
#	salvo na mesma pasta do script, com o nome de "iris.data".
#	https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data 
def carregarDataset(nomeArquivo, divisor, setTreinamento=[] , setTeste=[]):
	with open(nomeArquivo, 'rb') as csvfile:
	    linhas = csv.reader(csvfile)
	    dataset = list(linhas)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < divisor:
	            setTreinamento.append(dataset[x])
	        else:
	            setTeste.append(dataset[x])
 

def distanciaEuclidiana(ponto1, ponto2, tamanho):
	distancia = 0
	for x in range(tamanho):
		distancia += pow((ponto1[x] - ponto2[x]), 2)
	return math.sqrt(distancia)

 
def kNearestNeighbor(setTreinamento, instanciaTeste, k):
	distancias = []
	tamanho = len(instanciaTeste)-1
	for x in range(len(setTreinamento)):
		distancia = distanciaEuclidiana(instanciaTeste, setTreinamento[x], tamanho)
		distancias.append((setTreinamento[x], distancia))
	distancias.sort(key=operator.itemgetter(1))
	vizinhos = []
	for x in range(k):
		vizinhos.append(distancias[x][0])
	return vizinhos

def respostaCerta(vizinhos):
	votos = {}
	for x in range(len(vizinhos)):
		resposta = vizinhos[x][-1]
		if resposta in votos:
			votos[resposta] += 1
		else:
			votos[resposta] = 1

	votosOrdenados = sorted(votos.iteritems(), key=operator.itemgetter(1), reverse=True)
	return votosOrdenados[0][0]

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
k = 3
for x in range(len(setTeste)):
	vizinho = kNearestNeighbor(setTreinamento, setTeste[x], k)
	resultado = respostaCerta(vizinho)
	predicoes.append(resultado)
	print('> previsto=' + repr(resultado) + ', resultado real=' + repr(setTeste[x][-1]))
acuracia = calculaAcuracia(setTeste, predicoes)
print('Acurácia: ' + repr(acuracia) + '%')
	