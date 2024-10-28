import numpy as np
def read_J(file_name):
    with open(file_name) as file:
        datas = file.readlines()
        line_1 = datas[0]
        size = int(line_1.split(" ")[0])
        J = np.zeros((size, size))
        for i in range(1, len(datas)):
            data = datas[i]
            edge = data.split(" ")
            start = int(edge[0])
            end = int(edge[1])
            # value = int(edge[2])
            value = edge[2]
            J[start - 1][end - 1] = value
            J[end - 1][start - 1] = value
        return -1 * J


#Read the file according to the J_ij setting in the paper
def tmp_read_J(file_name):
    with open(file_name) as file:
        datas = file.readlines()
        line_1 = datas[0]
        size = int(line_1.split(" ")[0])
        J = np.zeros((size, size))
        for i in range(1, len(datas)):
            data = datas[i]
            edge = data.split(" ")
            start = int(edge[0])
            end = int(edge[1])
            # value = int(edge[2])
            value = int(edge[2])
            if(value < 0):
                J[start - 1][end - 1] = 0
                J[end - 1][start - 1] = 0
            if(value > 0):
                J[start - 1][end - 1] = 1
                J[end - 1][start - 1] = 1
        return -1 * J
