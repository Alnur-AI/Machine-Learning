'''
Простая сеть для достижения xor логической функции (метод градиентного спуска Нестерова)
'''
import numpy as np
import math

x_train = np.array([[0,1],[1,0],[0,0],[1,1]])
y_train = np.array([1,1,0,0])

# Обучение
weight = np.random.random((3,3))
old_weight = np.random.random((3,3))

grade = np.zeros((3,3))
last_grade = np.zeros((3,3))

output = np.zeros((3,2))
loss = np.zeros((3))
rate = 0.1

discount = 0.9

def sigmoid(x):
    return 1.0/(1.0 + math.exp(-x))

def grad_sigmoid(x):
    return math.exp(-x)/((1+math.exp(-x))**2)

def fit(x,y):
    global weight,output,loss,grade
    # Форвард расчет
    output[0,0] = x[0]*weight[0,0] + x[1]*weight[0,1] + weight[0,2]   #z = w'x +b
    output[0,1] = sigmoid(output[0,0])                                #y1 = sigmoid(z)

    output[1,0] = x[0]*weight[1,0] + x[1]*weight[1,1] + weight[1,2]   #z = w'x + b
    output[1,1] = sigmoid(output[1,0])                                # y2 = sigmoid(z)

    output[2,0] = output[0,1]*weight[2,0] + output[1,1]*weight[2,1] + weight[2,2] #z=w'(y1,y2)+b
    output[2,1] = sigmoid(output[2,0])                                            #y = sigmoid(z)

    # Обратный расчет потерь и угада
    loss[2] = (output[2,1] - y)*grad_sigmoid(output[2,0]) #

    grade[2,0] +=loss[2]*output[0,1]
    grade[2,1] +=loss[2]*output[1,1]
    grade[2,2] +=loss[2]

    loss[1] = loss[2]*weight[2,1]*grad_sigmoid(output[1,0])
    grade[1,0] +=loss[1]*x[0]
    grade[1,1] +=loss[1]*x[1]
    grade[1,2] +=loss[1]

    loss[0] = loss[2]*weight[2,0]*grad_sigmoid((output[0,0]))
    grade[0,0] +=loss[0]*x[0]
    grade[0,1] +=loss[0]*x[1]
    grade[0,2] +=loss[0]

    return (output[2,1]-y)**2

def preTrain():
    global last_grade,weight,rate,discount,old_weight
    old_weight = np.copy(weight)
    for i in range(0,3):
        for j in range(0,3):
            weight[i,j] = weight[i,j] - rate*discount*last_grade[i,j]

def postTrain():
    global old_weight,weight
    weight = old_weight

def updateGrade():
    global grade,weight,rate,discount,last_grade
    for i in range(0,3):
        for j in range(0,3):
            last_grade[i,j] = last_grade[i,j]*discount + grade[i,j]
            weight[i,j] = weight[i,j] - rate*last_grade[i,j]

    grade = np.zeros((3,3))

def predict(x):
    a = sigmoid(x[0]*weight[0,0]+x[1]*weight[0,1] + weight[0,2])
    b = sigmoid(x[0]*weight[1,0]+x[1]*weight[1,1] + weight[1,2])
    return sigmoid(a*weight[2,0] + b*weight[2,1] + weight[2,2])

for epoch in range(0,1000):
    preTrain()
    # Импорт данных
    allLoss  = 0
    for i in range(0,len(x_train)):
        allLoss +=fit(x_train[i],y_train[i])
    postTrain()

    # Обновить градиент
    updateGrade()

    print("epoch: %d-loss: %f" % (epoch, allLoss))

print(weight)

# Прогноз x_train = np.array ([[0,1], [1,0], [0,0], [1,1]])
for i in range(0,len(x_train)):
    print("data: (%d,%d),predict:%f"%(x_train[i,0],x_train[i,1],predict(x_train[i])))
