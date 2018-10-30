import csv
import random
import math
import operator
import pandas as pd
import numpy as np

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

def dmc(trainingSet, testInstance):
  classes = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
  centroids = [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]]
  length = testInstance.shape[1]
  cont = 0
  for x in range(len(classes)):
    for y in range(len(trainingSet)):
      current = [trainingSet.iloc[y]['SepalLength'],trainingSet.iloc[y]['SepalWidth'],trainingSet.iloc[y]['PetalLength'],trainingSet.iloc[y]['PetalWidth']]
      irisClass = trainingSet.iloc[y][-1] 
      if irisClass == classes[x]:
        cont += 1
        centroids[x] = [centroids[x][0]+current[0], centroids[x][1]+current[1], centroids[x][2]+current[2], centroids[x][3]+current[3]]
      
    for i in range(len(centroids[x])):
      centroids[x][i]= centroids[x][i]/cont

    centroids[x].append(classes[x])
    cont = 0
  
  testCentroid = pd.DataFrame(centroids)
  distances = {}
  sort = {}
  print("Centroides: ")
  print(testCentroid)


  length = testInstance.shape[1]
  for x in range(len(testCentroid)):
		
    dist = euclideanDistance(testInstance, testCentroid.iloc[x], length)
    distances[x] = dist[0]
 
  sorted_d = sorted(distances.items(), key=operator.itemgetter(1))
	
  neighbor = sorted_d[0][0]
  response = testCentroid.iloc[neighbor][4]
	
  return (response, neighbor)

setTest = []
setTreinamento = []
divisor = 0.67

carregarDataset('iris.data', divisor, setTreinamento, setTest)

resultado,vizinho = dmc(setTreinamento, setTest)
