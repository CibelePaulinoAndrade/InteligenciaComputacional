# -*- coding: utf-8 -*-

import csv
import random
import math
import operator

def carregarDataset(nomeArquivo, divisor, setTreinamento=[] , setTeste=[]):
	with open(nomeArquivo, newline='') as csvfile:
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
print ('Set de treinamento KNN: ' + repr(len(setTreinamento)))
print ('Set de teste NN: ' + repr(len(setTeste)))

predicoes = []
for x in range(len(setTeste)):
  vizinho = nearestNeighbor(setTreinamento, setTeste[x])
  resultado = respostaCerta(vizinho)
  predicoes.append(resultado)
  print('> previsto NN=' + repr(resultado) + ', resultado real=' + repr(setTeste[x][-1]))
acuracia = calculaAcuracia(setTeste, predicoes)
print('Acurácia NN: ' + repr(acuracia) + '%')

setTreinamento2=[]
setTeste2=[]
divisor = 0.67
carregarDataset('iris.data', divisor, setTreinamento2, setTeste2)
print ('Set de treinamento KNN: ' + repr(len(setTreinamento2)))
print ('Set de teste KNN: ' + repr(len(setTeste2)))

predicoes2 = []
for x in range(len(setTeste2)):
	vizinho2 = kNearestNeighbor(setTreinamento2, setTeste2[x], 5)
	resultado2 = respostaCerta(vizinho2)
	predicoes2.append(resultado2)
	print('> previsto KNN=' + repr(resultado2) + ', resultado real KNN=' + repr(setTeste2[x][-1]))

acuracia2 = calculaAcuracia(setTeste2, predicoes2)
print('Acurácia KNN: ' + repr(acuracia2) + '%')
