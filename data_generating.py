import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def positive_normal_random_gen(mu = 15, sigma = 30, size = 1000):
    count = 0
    ran_list = []
    while (count < size):
        a = np.random.normal(mu, sigma)
        if (a >= 0):
            ran_list.append(int(a))
            count = count + 1
            if (count >= size):
                break
    return ran_list
    # count = np.zeros(300)
    # for a in ran_list:
    #     count[a] = count[a]+1
    # plt.figure(1)
    # plt.plot(count)
    # return np.array(ran_list)

# generate data

data_size = 5000

data = pd.DataFrame(np.random.randint(low=0, high=5, size=(data_size, 4)), columns=['TQ','DPQ', 'C', 'OU'])

data['DI'] = positive_normal_random_gen(mu=30,sigma=20,size=data_size)
data['DFT'] = [np.random.randint(low=0, high=DI+1) for DI in data['DI']]
data['RD'] = [a - b for a, b in zip(data['DI'], data['DFT'])]
data['DFO'] = [np.random.randint(low=0, high=RD+1) for RD in data['RD']]

data['DI2'] = data['RD']
data['DFT2'] = [np.random.randint(low=0, high=DI+1) for DI in data['DI2']]
data['RD2'] = [a - b for a, b in zip(data['DI2'], data['DFT2'])]
data['DFO2'] = [np.random.randint(low=0, high=RD+1) for RD in data['RD2']]

data['DI3'] = data['RD2']
data['DFT3'] = [np.random.randint(low=0, high=DI+1) for DI in data['DI3']]
data['RD3'] = [a - b for a, b in zip(data['DI3'], data['DFT3'])]
data['DFO3'] = [np.random.randint(low=0, high=RD+1) for RD in data['RD3']]

data.to_csv("fisrm.csv", index=False);
