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

    def draw_subplots(self, Distribution, time1, time2, max_value_di):
        plt.figure()
        plt.subplot(4, 4, 1)
        plt.bar([1, 2, 3, 4, 5], Distribution['DPQ' + time1])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("design process quality " + time1)
        plt.ylabel('probability')

        plt.subplot(4, 4, 2)
        plt.bar([1, 2, 3, 4, 5], Distribution['C' + time1])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("complexity " + time1)
        plt.ylabel('probability')

        plt.subplot(4, 4, 3)
        plt.bar([1, 2, 3, 4, 5], Distribution['OU' + time1])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("operational usage " + time1)
        plt.ylabel('probability')

        plt.subplot(4, 4, 4)
        plt.bar([1, 2, 3, 4, 5], Distribution['TQ' + time1])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("Test quality " + time1)
        plt.ylabel('probability')

        plt.subplot(4, 4, 5)
        plt.plot(self.model.state_names['DI' + time1] + [max_value_di+1], Distribution['DI' + time1])
        plt.title("defects inserted " + time1)
        plt.ylabel('probability')

        plt.subplot(4, 4, 6)
        plt.plot(self.model.state_names['DFT' + time1] + [max_value_di+1], Distribution['DFT' + time1])
        plt.title("defects found in testing " + time1)
        plt.ylabel('probability')

        plt.subplot(4, 4, 7)
        plt.plot(self.model.state_names['RD' + time1] + [max_value_di+1], Distribution['RD' + time1])
        plt.title("residual defects " + time1)
        plt.ylabel('probability')

        plt.subplot(4, 4, 8)
        plt.plot(self.model.state_names['DFO' + time1] + [max_value_di+1], Distribution['DFO' + time1])
        plt.title("defects found in operation " + time1)
        plt.ylabel('probability')

        plt.subplot(4, 4, 9)
        plt.bar([1, 2, 3, 4, 5], Distribution['DPQ' + time2])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("design process quality " + time2)
        plt.ylabel('probability')

        plt.subplot(4, 4, 10)
        plt.bar([1, 2, 3, 4, 5], Distribution['C' + time2])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("complexity " + time2)
        plt.ylabel('probability')

        plt.subplot(4, 4, 11)
        plt.bar([1, 2, 3, 4, 5], Distribution['OU' + time2])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("operational usage " + time2)
        plt.ylabel('probability')

        plt.subplot(4, 4, 12)
        plt.bar([1, 2, 3, 4, 5], Distribution['TQ' + time2])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("Test quality " + time2)
        plt.ylabel('probability')

        plt.subplot(4, 4, 13)
        plt.plot(self.model.state_names['DI' + time2] + [max_value_di+1], Distribution['DI' + time2])
        plt.title("defects inserted " + time2)
        plt.ylabel('probability')

        plt.subplot(4, 4, 14)
        plt.plot(self.model.state_names['DFT' + time2] + [max_value_di+1], Distribution['DFT' + time2])
        plt.title("defects found in testing " + time2)
        plt.ylabel('probability')

        plt.subplot(4, 4, 15)
        plt.plot(self.model.state_names['RD' + time2] + [max_value_di+1], Distribution['RD' + time2])
        plt.title("residual defects " + time2)
        plt.ylabel('probability')

        plt.subplot(4, 4, 16)
        plt.plot(self.model.state_names['DFO' + time2] + [max_value_di+1], Distribution['DFO' + time2])
        plt.title("defects found in operation " + time2)
        plt.ylabel('probability')

        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.4, wspace=0.4)

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

        if self.history_file != self.file_path:
            self.data = pd.read_csv(self.file_path)  # "fisrm.csv"
            self.data_size = len(self.data)
            self.history_file = self.file_path

            self.model = BayesianModel(
                [('TQ', 'DFT'), ('DPQ', 'DI'), ('C', 'DI'), ('DI', 'DFT'), ('DI', 'RD'), ('DFT', 'RD'), ('RD', 'DFO'),
                ('OU', 'DFO'),
                ('DPQ', 'DPQ2'), ('C', 'C2'), ('TQ', 'TQ2'), ('OU', 'OU2'), ('RD', 'DI2'), 
                ('DI2', 'DFT2'), ('DI2', 'RD2'), ('DFT2', 'RD2'), ('RD2', 'DFO2'), ('OU2', 'DFO2'),
                ('DPQ2', 'DPQ3'), ('C2', 'C3'), ('TQ2', 'TQ3'), ('OU2', 'OU3'),
                ('RD2', 'DI3'), ('DI3', 'DFT3'), ('DI3', 'RD3'), ('DFT3', 'RD3'), ('RD3', 'DFO3'), ('OU3', 'DFO3')])

            self.model.fit(self.data, estimator_type=BayesianEstimator, prior_type="BDeu",
                      equivalent_sample_size=10)  # default equivalent_sample_size=5
            print self.model.state_names

        infer = VariableElimination(self.model)

        nodes = ['DPQ', 'C', 'TQ', 'DI', 'DFT', 'RD', 'OU', 'DFO']
        Distribution = {}

        for key in pr.keys():
            Distribution[key] = [1 - abs(np.sign(pr[key] - i)) for i in range(5)]
            Distribution[key+'2'] = Distribution[key]
            Distribution[key+'3'] = Distribution[key]
            nodes.remove(key)

        max_value_di = self.model.state_names['DI'][-1] # array has been sorted

        print 'query 1', pr, nodes
        query = infer.query(nodes, evidence=pr)
        for key, value in query.iteritems():
            Distribution[key] = value.values

        for key in [x for x in nodes if x not in ['DPQ', 'C', 'TQ', 'OU']]:
            if Distribution[key][-1] < max_value_di:
                Distribution[key] = np.append(Distribution[key], [0])

        pr_new = {}
        for key, value in pr.iteritems():
            pr_new[key+'2'] = pr[key]
        pr = pr_new
        for key, value in pr.iteritems():
            if key[-1] != '2':
                del pr[key]

        for i in range(len(nodes)):
            nodes[i] = nodes[i] + '2'


        print 'query 2', pr, nodes
        query = infer.query(nodes, evidence=pr)
        for key, value in query.iteritems():
            Distribution[key] = value.values

        for key in [x for x in nodes if x not in ['DPQ2', 'C2', 'TQ2', 'OU2']]:
            if Distribution[key][-1] < max_value_di:
                Distribution[key] = np.append(Distribution[key], [0])

        pr_new = {}
        for key, value in pr.iteritems():
            pr_new[key[:-1]+'3'] = pr[key]
        pr = pr_new
        for i in range(len(nodes)):
            nodes[i] = nodes[i][:-1] + '3'


        print 'query 3', pr, nodes
        query = infer.query(nodes, evidence=pr)
        for key, value in query.iteritems():
            Distribution[key] = value.values

        for key in [x for x in nodes if x not in ['DPQ3', 'C3', 'TQ3', 'OU3']]:
            if Distribution[key][-1] < max_value_di:
                Distribution[key] = np.append(Distribution[key], [0])

        self.draw_subplots(Distribution, '', '2', max_value_di)
        self.draw_subplots(Distribution, '2', '3', max_value_di)
        self.draw_subplots(Distribution, '', '3', max_value_di)
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
        self.history_file = ''

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
