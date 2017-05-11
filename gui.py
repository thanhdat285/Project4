from Tkinter import *
import tkFileDialog
import ttk
import numpy as np
import pandas as pd
import sys
from pgmpy.models import BayesianModel
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination
import matplotlib.pyplot as plt
from openpyxl.drawing.text import TextField

def positive_normal_random_gen(mu = 15,sigma=30, size=1000):
    count = 0
    ran_list = []
    while (count < size):
        a = np.random.normal(mu, sigma)
        if (a >= 0):
            ran_list.append(int(a))
            count = count + 1
            if (count >= size):
                break
    # count = np.zeros(300)
    # for a in ran_list:
    #     count[a] = count[a]+1
    # plt.figure(1)
    # plt.plot(count)
    return np.array(ran_list)

class Application(Frame):
    def choosefile(self):
        self.file_path = tkFileDialog.askopenfilename()
        self.datafile_label["text"] = self.file_path

    def process(self):
        # print self.dpq_box.get()
        # print self.c_box.get()
        # Check input
        if not hasattr(self, 'file_path'):
            print"chua chon file"
            exit()
        pr = {}
        # 'very low', 'low', 'medium', 'high', 'very high'
        # print type(self.dpq_box.get())
        if self.dpq_box.get() == 'unknown':
            if 'DPQ' in pr.keys():
                del pr['DPQ']
        elif self.dpq_box.get() == 'very low':
            pr['DPQ'] = 0
        elif self.dpq_box.get() == 'low':
            pr['DPQ'] = 1
        elif self.dpq_box.get() == 'medium':
            pr['DPQ'] = 2
        elif self.dpq_box.get() == 'high':
            pr['DPQ'] = 3
        elif self.dpq_box.get() == 'very high':
            pr['DPQ'] = 4
        else:
            pass

        if self.c_box.get() == 'unknown':
            if 'C' in pr.keys():
                del pr['C']
        elif self.c_box.get() == 'very low':
            pr['C'] = 0
        elif self.c_box.get() == 'low':
            pr['C'] = 1
        elif self.c_box.get() == 'medium':
            pr['C'] = 2
        elif self.c_box.get() == 'high':
            pr['C'] = 3
        elif self.c_box.get() == 'very high':
            pr['C'] = 4
        else:
            pass

        if self.tq_box.get() == 'unknown':
            if 'TQ' in pr.keys():
                del pr['TQ']
        elif self.tq_box.get() == 'very low':
            pr['TQ'] = 0
        elif self.tq_box.get() == 'low':
            pr['TQ'] = 1
        elif self.tq_box.get() == 'medium':
            pr['TQ'] = 2
        elif self.tq_box.get() == 'high':
            pr['TQ'] = 3
        elif self.tq_box.get() == 'very high':
            pr['TQ'] = 4
        else:
            pass

        if self.ou_box.get() == 'unknown':
            if 'OU' in pr.keys():
                del pr['OU']
        elif self.ou_box.get() == 'very low':
            pr['OU'] = 0
        elif self.ou_box.get() == 'low':
            pr['OU'] = 1
        elif self.ou_box.get() == 'medium':
            pr['OU'] = 2
        elif self.ou_box.get() == 'high':
            pr['OU'] = 3
        elif self.ou_box.get() == 'very high':
            pr['OU'] = 4
        else:
            pass

        print pr

        data = pd.read_csv(self.file_path)  # "fisrm.csv"
        data_size = len(data)


        model = BayesianModel(
            [('TQ', 'DFT'), ('DPQ', 'DI'), ('C', 'DI'), ('DI', 'DFT'), ('DI', 'RD'), ('DFT', 'RD'), ('RD', 'DFO'),
            ('OU', 'DFO'),
            ('RD', 'DI2'), ('DI2', 'DFT2'), ('DI2', 'RD2'), ('DFT2', 'RD2'), ('RD2', 'DFO2'), ('OU', 'DFO2'),
            ('RD2', 'DI3'), ('DI3', 'DFT3'), ('DI3', 'RD3'), ('DFT3', 'RD3'), ('RD3', 'DFO3'), ('OU', 'DFO3')])

        model.fit(data, estimator_type=BayesianEstimator, prior_type="BDeu",
                  equivalent_sample_size=10)  # default equivalent_sample_size=5


        infer = VariableElimination(model)

        nodes = ['DPQ', 'C', 'TQ', 'DI', 'DFT', 'RD', 'OU', 'DFO', 'DI2', 'DFT2', 'RD2', 'DFO2',
            'DI3', 'DFT3', 'RD3', 'DFO3']
        Distribution = {}

        for key in pr.keys():
            Distribution[key] = [1 - abs(np.sign(pr[key] - i)) for i in range(5)]
            nodes.remove(key)

        
        max_value_di = model.state_names['DI'][-1] # array has been sorted
        for key in nodes:
            Distribution[key] = infer.query([key], evidence=pr)[key].values

        for key in [x for x in nodes if x not in ['DPQ', 'C', 'TQ', 'OU']]:
            length = len(Distribution[key])
            if length < max_value_di:
                model.state_names[key].append(max_value_di + 1)
                Distribution[key] = np.append(Distribution[key], [0])

        plt.figure()

        plt.subplot(4, 4, 1)
        plt.bar([1, 2, 3, 4, 5], Distribution['DPQ'])
        plt.xticks([1.5, 2.5, 3.5, 4.5, 5.5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("design process quality 1")
        plt.ylabel('probability')

        plt.subplot(4, 4, 2)
        plt.bar([1, 2, 3, 4, 5], Distribution['C'])
        plt.xticks([1.5, 2.5, 3.5, 4.5, 5.5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("complexity 1")
        plt.ylabel('probability')

        plt.subplot(4, 4, 3)
        plt.bar([1, 2, 3, 4, 5], Distribution['TQ'])
        plt.xticks([1.5, 2.5, 3.5, 4.5, 5.5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("Test quality 1")
        plt.ylabel('probability')

        plt.subplot(4, 4, 4)
        plt.bar([1, 2, 3, 4, 5], Distribution['OU'])
        plt.xticks([1.5, 2.5, 3.5, 4.5, 5.5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("operational usage 1")
        plt.ylabel('probability')

        plt.subplot(4, 4, 5)
        plt.plot(model.state_names['DI'], Distribution['DI'])
        plt.title("defects inserted 1")
        # plt.xlabel('number')
        plt.ylabel('probability')

        plt.subplot(4, 4, 6)
        plt.plot(model.state_names['DFT'], Distribution['DFT'])
        plt.title("defects found in testing 1")
        plt.ylabel('probability')

        plt.subplot(4, 4, 7)
        plt.plot(model.state_names['RD'], Distribution['RD'])
        plt.title("residual defects 1")
        plt.ylabel('probability')

        plt.subplot(4, 4, 8)
        plt.plot(model.state_names['DFO'], Distribution['DFO'])
        plt.title("defects found in operation 1")
        plt.ylabel('probability')

        # TIME SLICE 2

        plt.subplot(4, 4, 9)
        plt.plot(model.state_names['DI2'], Distribution['DI2'])
        plt.title("defects inserted 2")
        plt.ylabel('probability')

        plt.subplot(4, 4, 10)
        plt.plot(model.state_names['DFT2'], Distribution['DFT2'])
        plt.title("defects found in testing 2")
        plt.ylabel('probability')

        plt.subplot(4, 4, 11)
        plt.plot(model.state_names['RD2'], Distribution['RD2'])
        plt.title("residual defects 2")
        plt.ylabel('probability')

        plt.subplot(4, 4, 12)
        plt.plot(model.state_names['DFO2'], Distribution['DFO2'])
        plt.title("defects found in operation 2")
        plt.ylabel('probability')

        # TIME SLICE 3

        plt.subplot(4, 4, 13)
        plt.plot(model.state_names['DI3'], Distribution['DI3'])
        plt.title("defects inserted 3")
        plt.ylabel('probability')

        plt.subplot(4, 4, 14)
        plt.plot(model.state_names['DFT3'], Distribution['DFT3'])
        plt.title("defects found in testing 3")
        plt.ylabel('probability')

        plt.subplot(4, 4, 15)
        plt.plot(model.state_names['RD3'], Distribution['RD3'])
        plt.title("residual defects 3")
        plt.ylabel('probability')

        plt.subplot(4, 4, 16)
        plt.plot(model.state_names['DFO3'], Distribution['DFO3'])
        plt.title("defects found in operation 3")
        plt.ylabel('probability')

        plt.subplots_adjust(hspace=0.5)
        plt.show()

    def createWidgets(self):
        pad_x = 5
        pad_y = 5
        self.firstlabel = Label(self)
        self.firstlabel["text"] = "Choose_file:__",
        # self.text_datafile["command"] = self.say_hi

        # self.firstlabel.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky=W)

        self.datafile_label = Label(self)
        self.datafile_label["text"] = "no_file",
        self.datafile_label.grid(row=0, column=1, padx=pad_x, pady=pad_y,columnspan=3, sticky=W)

        self.choosefilebutton = Button(self)
        self.choosefilebutton["text"] = "Choose_data_file",
        self.choosefilebutton["command"] = self.choosefile
        self.choosefilebutton.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)

        self.dpq_label = Label(self)
        self.dpq_label["text"] = "design_process_quality",
        self.dpq_label.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky=W)

        # self.dpq_entry = Entry(self, width=10)
        # self.dpq_entry.grid(row=1, column=3, padx=pad_x, pady=pad_y, sticky=W)
        self.dpq_box_value = StringVar()
        self.dpq_box = ttk.Combobox(self, textvariable=self.dpq_box_value)
        self.dpq_box['values'] = ('unknown','very low', 'low', 'medium', 'high', 'very high')
        self.dpq_box.current(0)
        self.dpq_box.grid(row=2, column=2, padx=pad_x, pady=pad_y, sticky=W)

        self.c_label = Label(self)
        self.c_label["text"] = "Complexity",
        self.c_label.grid(row=2, column=3, padx=pad_x, pady=pad_y, sticky=W)

        # self.c_entry = Entry(self, width=10)
        # self.c_entry.grid(row=1, column=5, padx=pad_x, pady=pad_y, sticky=W)
        self.c_box_value = StringVar()
        self.c_box = ttk.Combobox(self, textvariable=self.c_box_value)
        self.c_box['values'] = ('unknown','very low', 'low', 'medium', 'high', 'very high')
        self.c_box.current(0)
        self.c_box.grid(row=2, column=4, padx=pad_x, pady=pad_y, sticky=W)

        self.tq_label = Label(self)
        self.tq_label["text"] = "Test_quality",
        self.tq_label.grid(row=2, column=5, padx=pad_x, pady=pad_y, sticky=W)

        # self.tq_entry = Entry(self, width=10)
        # self.tq_entry.grid(row=1, column=7, padx=pad_x, pady=pad_y, sticky=W)

        self.tq_box_value = StringVar()
        self.tq_box = ttk.Combobox(self, textvariable=self.tq_box_value)
        self.tq_box['values'] = ('unknown','very low','low','medium', 'high','very high')
        self.tq_box.current(0)
        self.tq_box.grid(row=2, column=6, padx=pad_x, pady=pad_y, sticky=W)

        self.ou_label = Label(self)
        self.ou_label["text"] = "operational_usage",
        self.ou_label.grid(row=2, column=7, padx=pad_x, pady=pad_y, sticky=W)

        # self.tq_entry = Entry(self, width=10)
        # self.tq_entry.grid(row=1, column=7, padx=pad_x, pady=pad_y, sticky=W)

        self.ou_box_value = StringVar()
        self.ou_box = ttk.Combobox(self, textvariable=self.ou_box_value)
        self.ou_box['values'] = ('unknown', 'very low', 'low', 'medium', 'high', 'very high')
        self.ou_box.current(0)
        self.ou_box.grid(row=2, column=8, padx=pad_x, pady=pad_y, sticky=W)

        self.processbotton = Button(self)
        self.processbotton["text"] = "Process",
        self.processbotton["command"] = self.process
        self.processbotton.grid(row=3, column=1, padx=pad_x, pady=pad_y, sticky=W)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.grid(row=3, column=2, padx=pad_x, pady=pad_y, sticky=W)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
