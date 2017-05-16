from Tkinter import *
import tkFileDialog
import ttk
import numpy as np
import pandas as pd
import sys
from pgmpy.models import DynamicBayesianNetwork
from pgmpy.DynamicBayesian.estimators import MaximumLikelihoodEstimator
from pgmpy.DynamicBayesian.inference import DBNInferenceRewritten
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
        plt.bar([1, 2, 3, 4, 5], Distribution[('DPQ', time1)])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("design process quality " + str(time1+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 2)
        plt.bar([1, 2, 3, 4, 5], Distribution[('C', time1)])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("complexity " + str(time1+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 3)
        plt.bar([1, 2, 3, 4, 5], Distribution[('OU', time1)])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("operational usage " + str(time1+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 4)
        plt.bar([1, 2, 3, 4, 5], Distribution[('TQ', time1)])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("Test quality " + str(time1+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 5)
        plt.plot(self.state_names[('DI', time1)], Distribution[('DI', time1)])
        plt.title("defects inserted " + str(time1+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 6)
        plt.plot(self.state_names[('DFT', time1)], Distribution[('DFT', time1)])
        plt.title("defects found in testing " + str(time1+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 7)
        plt.plot(self.state_names[('RD', time1)], Distribution[('RD', time1)])
        plt.title("residual defects " + str(time1+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 8)
        plt.plot(self.state_names[('DFO', time1)], Distribution[('DFO', time1)])
        plt.title("defects found in operation " + str(time1+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 9)
        plt.bar([1, 2, 3, 4, 5], Distribution[('DPQ', time2)])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("design process quality " + str(time2+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 10)
        plt.bar([1, 2, 3, 4, 5], Distribution[('C', time2)])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("complexity " + str(time2+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 11)
        plt.bar([1, 2, 3, 4, 5], Distribution[('OU', time2)])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("operational usage " + str(time2+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 12)
        plt.bar([1, 2, 3, 4, 5], Distribution[('TQ', time2)])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("Test quality " + str(time2+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 13)
        plt.plot(self.state_names[('DI', time2)], Distribution[('DI', time2)])
        plt.title("defects inserted " + str(time2+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 14)
        plt.plot(self.state_names[('DFT', time2)], Distribution[('DFT', time2)])
        plt.title("defects found in testing " + str(time2+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 15)
        plt.plot(self.state_names[('RD', time2)], Distribution[('RD', time2)])
        plt.title("residual defects " + str(time2+1))
        plt.ylabel('probability')

        plt.subplot(4, 4, 16)
        plt.plot(self.state_names[('DFO', time2)], Distribution[('DFO', time2)])
        plt.title("defects found in operation " + str(time2+1))
        plt.ylabel('probability')

        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.4, wspace=0.4)

    def processBox(self):
        if not hasattr(self, 'file_path'):
            print"chua chon file"
            exit()
        pr = {}
        # 'very low', 'low', 'medium', 'high', 'very high'
        # print type(self.dpq_box.get())
        if self.dpq_box.get() == 'unknown':
            if ('DPQ', 0) in pr.keys():
                del pr[('DPQ', 0)]
        elif self.dpq_box.get() == 'very low':
            pr[('DPQ', 0)] = 0
        elif self.dpq_box.get() == 'low':
            pr[('DPQ', 0)] = 1
        elif self.dpq_box.get() == 'medium':
            pr[('DPQ', 0)] = 2
        elif self.dpq_box.get() == 'high':
            pr[('DPQ', 0)] = 3
        elif self.dpq_box.get() == 'very high':
            pr[('DPQ', 0)] = 4
        else:
            pass

        if self.c_box.get() == 'unknown':
            if ('C', 0) in pr.keys():
                del pr[('C', 0)]
        elif self.c_box.get() == 'very low':
            pr[('C', 0)] = 0
        elif self.c_box.get() == 'low':
            pr[('C', 0)] = 1
        elif self.c_box.get() == 'medium':
            pr[('C', 0)] = 2
        elif self.c_box.get() == 'high':
            pr[('C', 0)] = 3
        elif self.c_box.get() == 'very high':
            pr[('C', 0)] = 4
        else:
            pass

        if self.tq_box.get() == 'unknown':
            if ('TQ', 0) in pr.keys():
                del pr[('TQ', 0)]
        elif self.tq_box.get() == 'very low':
            pr[('TQ', 0)] = 0
        elif self.tq_box.get() == 'low':
            pr[('TQ', 0)] = 1
        elif self.tq_box.get() == 'medium':
            pr[('TQ', 0)] = 2
        elif self.tq_box.get() == 'high':
            pr[('TQ', 0)] = 3
        elif self.tq_box.get() == 'very high':
            pr[('TQ', 0)] = 4
        else:
            pass

        if self.ou_box.get() == 'unknown':
            if ('OU', 0) in pr.keys():
                del pr[('OU', 0)]
        elif self.ou_box.get() == 'very low':
            pr[('OU', 0)] = 0
        elif self.ou_box.get() == 'low':
            pr[('OU', 0)] = 1
        elif self.ou_box.get() == 'medium':
            pr[('OU', 0)] = 2
        elif self.ou_box.get() == 'high':
            pr[('OU', 0)] = 3
        elif self.ou_box.get() == 'very high':
            pr[('OU', 0)] = 4
        else:
            pass
        return pr

    def process(self):
        def add_cpds_to_model(model, data):
            mle = MaximumLikelihoodEstimator(model, data)
            cpds = []
            nodes = model.get_slice_nodes(0) + model.get_slice_nodes(1)
            for node in nodes:
                cpds.append(mle.estimate_cpd(node))
            model.add_cpds(*cpds)
            model.state_names = mle.state_names

        def calculate_distribution_nodes_input():
            for key in pr.keys():
                Distribution[key] = [1 - abs(np.sign(pr[key] - i)) for i in range(5)]
                Distribution[(key[0], 1)] = Distribution[key]
                Distribution[(key[0], 2)] = Distribution[key]
                nodes.remove(key)
                nodes2.remove((key[0], 1))
 
        def query_time_frame_1():
            print 'query 1', pr, nodes
            query = infer.query(nodes, evidence=pr)
            for key, value in query.iteritems():
                Distribution[key] = value.values

        def query_time_frame_2():
            global pr2
            for key, value in pr.iteritems():
                pr2[(key[0], 1)] = pr[key]

            print 'query 2', pr2, nodes2
            query = infer.query(nodes2, evidence=pr2)
            for key, value in query.iteritems():
                Distribution[key] = value.values

        def query_time_frame_3():
            # Dynamic Bayesian Network only supports 2-time slice, 2 time frame. Hence, create new DBN with 
            # datas of time 2 and time 3 to query nodes in time 3.
            data23 = self.data.rename(columns={
                'DPQ2': ('DPQ', 0), 'C2': ('C', 0), 'TQ2': ('TQ', 0), 'OU2': ('OU', 0), 'DI2': ('DI', 0),
                'DFT2': ('DFT', 0), 'RD2': ('RD', 0), 'DFO2': ('DFO', 0), 
                'DPQ3': ('DPQ', 1), 'C3': ('C', 1), 'TQ3': ('TQ', 1), 'OU3': ('OU', 1), 'DI3': ('DI', 1),
                'DFT3': ('DFT', 1), 'RD3': ('RD', 1), 'DFO3': ('DFO', 1)})
            data23 = data23.drop(['DPQ','C', 'TQ', 'OU', 'DI', 'DFT', 'RD', 'DFO'], 1)

            self.model23 = DynamicBayesianNetwork()
            self.model23.add_edges_from([(('DPQ', 0), ('DI', 0)), (('C', 0), ('DI', 0)), (('TQ', 0), ('DFT', 0)),
              (('DI', 0), ('DFT', 0)), (('DI', 0), ('RD', 0)), (('DFT', 0), ('RD', 0)), (('RD', 0), ('DFO', 0)),
              (('OU', 0), ('DFO', 0)),
              (('DPQ', 0), ('DPQ', 1)), (('C', 0), ('C', 1)), (('TQ', 0), ('TQ', 1)), (('OU', 0), ('OU', 1)),
              (('RD', 0), (('DI', 1)))])

            add_cpds_to_model(self.model23, data23)
            # save state names to draw graph
            for key, names in self.model23.state_names.iteritems():
                if key[1] == 1:
                    self.state_names[(key[0], 2)] = names

            pr3 = pr2
            nodes3 = nodes2
            print 'query 3', pr3, nodes3 # pr = {('DPQ', 1): 1,...} | nodes = [('DPQ', 1),...]
            infer3 = DBNInferenceRewritten(self.model23)
            query = infer3.query(nodes3, evidence=pr3)
            for key, value in query.iteritems():
                Distribution[(key[0], 2)] = value.values

        # sketch number axis with max values = max values DI + 1
        def stretch_distributions(max_value_di):
            remove_nodes = []
            for time in range(3):
                remove_nodes.append(('DPQ', time))
                remove_nodes.append(('C', time))
                remove_nodes.append(('OU', time))
                remove_nodes.append(('TQ', time))

            ns = nodes + nodes2 + [(node[0], 2) for node in nodes]
            for key in ns: 
                if key not in remove_nodes:
                    if self.state_names[key][-1] == max_value_di:
                        self.state_names[key].append(max_value_di+1)
                        Distribution[key] = np.append(Distribution[key], [0])
                    elif self.state_names[key][-1] < max_value_di:
                        self.state_names[key].extend([self.state_names[key][-1]+1, max_value_di+1])
                        Distribution[key] = np.append(Distribution[key], [0, 0])

        def standarlize_distribution():
            # use when data size is too small and length(DPQ or C or TQ or OU) < 5 => error when draw graph
            ns = ['DPQ', 'TQ', 'C', 'OU']
            for node in ns:
                exist_in_pr = False
                for key in pr.keys():
                    if key[0] == node:
                        exist_in_pr = True
                        break
                if not exist_in_pr:
                    for index in range(5):
                        if index not in self.model.state_names[(node, 0)]:
                            Distribution[(node, 0)].insert(index, 0)
                            Distribution[(node, 1)].insert(index, 0)
                            Distribution[(node, 2)].insert(index, 0)

        if self.history_file != self.file_path:
            self.data = pd.read_csv(self.file_path)  # "fisrm.csv"
            self.data_size = len(self.data)
            self.history_file = self.file_path
            self.state_names = {}

            self.model = DynamicBayesianNetwork()
            self.model.add_edges_from([(('DPQ', 0), ('DI', 0)), (('C', 0), ('DI', 0)), (('TQ', 0), ('DFT', 0)),
              (('DI', 0), ('DFT', 0)), (('DI', 0), ('RD', 0)), (('DFT', 0), ('RD', 0)), (('RD', 0), ('DFO', 0)),
              (('OU', 0), ('DFO', 0)),
              (('DPQ', 0), ('DPQ', 1)), (('C', 0), ('C', 1)), (('TQ', 0), ('TQ', 1)), (('OU', 0), ('OU', 1)),
              (('RD', 0), (('DI', 1)))])

        global pr
        global pr2
        global pr3
        pr = self.processBox()
        pr2 = {}
        pr3 = {}
        nodes = self.model.get_slice_nodes(0)
        nodes2 = self.model.get_slice_nodes(1)
        Distribution = {}

        # Rename and drop data columns to use MaximumLikelyHood
        data12 = self.data.rename(columns={'DPQ': ('DPQ', 0), 'C': ('C', 0), 'TQ': ('TQ', 0),
                                   'DI': ('DI', 0), 'DFT': ('DFT', 0), 'RD': ('RD', 0), 'DFO': ('DFO', 0), 
                                   'OU': ('OU', 0), 'DPQ2': ('DPQ', 1), 'C2': ('C', 1), 'TQ2': ('TQ', 1), 
                                   'OU2': ('OU', 1), 'DI2': ('DI', 1), 'DFT2': ('DFT', 1), 'RD2': ('RD', 1), 
                                   'DFO2': ('DFO', 1)})
        data12 = data12.drop(['DPQ3','C3', 'TQ3', 'OU3', 'DI3', 'DFT3', 'RD3', 'DFO3'], 1)
        add_cpds_to_model(self.model, data12)
        self.state_names = self.model.state_names
        
        infer = DBNInferenceRewritten(self.model)
        calculate_distribution_nodes_input()
        query_time_frame_1()
        query_time_frame_2()
        query_time_frame_3()
        max_value_di = self.state_names[('DI', 0)][-1] # array has been sorted
        stretch_distributions(max_value_di)
        # standarlize_distribution()
        self.draw_subplots(Distribution, 0, 1, max_value_di)
        self.draw_subplots(Distribution, 1, 2, max_value_di)
        self.draw_subplots(Distribution, 0, 2, max_value_di)
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
