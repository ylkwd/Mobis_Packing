from random import randint
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import json

pallete = ['darkgreen', 'yellow', 'darkblue', 'darkviolet', 'indianred', 'yellowgreen', 'mediumblue', 'cyan',
           'black', 'indigo', 'pink', 'lime', 'sienna', 'plum', 'deepskyblue', 'forestgreen', 'fuchsia', 'brown',
           'turquoise', 'aliceblue', 'blueviolet', 'rosybrown', 'powderblue', 'lightblue', 'skyblue', 'lightskyblue',
           'steelblue', 'dodgerblue', 'lightslategray', 'lightslategrey', 'slategray', 'slategrey', 'lightsteelblue',
           'cornflowerblue', 'royalblue', 'ghostwhite', 'lavender', 'midnightblue', 'navy', 'darkblue', 'blue',
           'slateblue', 'darkslateblue', 'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'darkorchid',
           'darkviolet', 'mediumorchid', 'lightsalmon', 'lightseagreen', 'lavenderblush', 'aquamarine', 'palegreen',
           'yellow', 'firebrick', 'maroon', 'darkred', 'red', 'salmon', 'darksalmon', 'coral', 'orangered',
           'lightcoral', 'chocolate', 'saddlebrown', 'sandybrown', 'olive', 'olivedrab', 'darkolivegreen',
           'greenyellow', 'chartreuse', 'lawngreen', 'darkseagreen', 'lightgreen', 'limegreen',
           'green', 'seagreen', 'mediumseagreen', 'springgreen', 'mediumspringgreen', 'mediumaquamarine',
           'mediumturquoise', 'lightcyan', 'paleturquoise', 'darkslategray',
           'darkslategrey', 'teal', 'darkcyan', 'aqua', 'cyan', 'darkturquoise', 'cadetblue', 'thistle',
           'violet', 'purple', 'darkmagenta', 'magenta', 'orchid', 'mediumvioletred', 'deeppink', 'hotpink',
           'palevioletred', 'crimson', 'lightpink'
           ]
color_pallete = ['lightsalmon', 'lightseagreen', 'lavenderblush', 'aquamarine', 'palegreen', 'yellow', 'firebrick',
                 'maroon', 'darkred', 'red', 'salmon', 'darksalmon', 'coral', 'orangered',
                 'lightcoral', 'chocolate', 'saddlebrown', 'sandybrown', 'olive', 'olivedrab', 'darkolivegreen',
                 'greenyellow', 'chartreuse', 'lawngreen', 'darkseagreen', 'lightgreen', 'limegreen',
                 'green', 'seagreen', 'mediumseagreen', 'springgreen', 'mediumspringgreen', 'mediumaquamarine',
                 'mediumturquoise', 'lightcyan', 'paleturquoise', 'darkslategray',
                 'darkslategrey', 'teal', 'darkcyan', 'aqua', 'cyan', 'darkturquoise', 'cadetblue', 'thistle',
                 'violet', 'purple', 'darkmagenta', 'magenta', 'orchid', 'mediumvioletred', 'deeppink', 'hotpink',
                 'palevioletred', 'crimson', 'lightpink']

# with open('input.json', 'r') as outfile:
#     data = json.load(outfile)
# container  = Dataset.test_example()
# # container = dataset
# print(container)
# exit()
# truck_dimension = []
# problem_indices = list(data.keys())
# for p_ind in problem_indices:
#     truck_dimension = data[p_ind]['truck dimension']


def cuboid_data(o, size=(1, 1, 1)):
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1], o[1], o[1]],
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]
    z = [[o[2], o[2], o[2], o[2], o[2]],
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]
    return np.array(x), np.array(y), np.array(z)


def plotcuboid(pos=(0, 0, 0), size=(1, 1, 1), ax=None, **kwargs):
    # Plotting a cube element at position pos
    if ax is not None:
        X, Y, Z = cuboid_data(pos, size)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, **kwargs)


def draw(pieces, color_index=[], truck_dimension=[], title=""):
    # print(truck_dimension[0],type(truck_dimension[0]))
    # exit()
    positions = []
    boxesId =[]
    sizes = []
    colors = []
    sorted_size = []
    ColorPair = {}

    if len(color_index) == 0:
        for each in pieces:
            # boxesId.append(each[0])
            positions.append(each[:3])
            sizes.append(each[3:])
            sorted_size.append(set(each[3:]))
        # for i in range(len(pallete)):
        #     index = random.randint(0,len(pallete)-1)
        #     colors.append(pallete[index])
        # colors = pallete[randint(0,50)]
        index = 0
        # boxesId = []
        for i in range(0, len(positions)):
            # index = random.randint(0,len(pallete)-1)
            if i >= 1:
                if positions[i][2] == positions[i - 1][2]:
                    colors.append(pallete[index])
                    boxesId.append(positions[i][2])
                    # print(i,index,colors)

                else:
                    index += 1
                    colors.append(pallete[index])
                    boxesId.append(positions[i][2])
                    ColorPair[positions[i][2]] = {pallete[index]}
                    # print(i,index,colors)
            else:
                colors.append(pallete[index])
                boxesId.append(positions[i][2])
                ColorPair[positions[i][2]] = {pallete[index]}
                # print(i,index,colors)
        # print(len(colors),len(boxesId))
        color_index = [sorted_size, colors, boxesId]
        return color_index, ColorPair
    else:
        for each in pieces:
            boxesId.append(each[0])
            positions.append(each[1:4])
            sizes.append(each[4:7])
            sorted_size.append(set(each[4:7]))

        dim = color_index[2]
        clr = color_index[1]
        sorted_pieces = color_index[0]
        clr_index = 0
        print(boxesId,positions)
        for each in boxesId:
            # print(each)
            index = dim.index(each)
            # print(index)
            colors.append(clr[index])
            clr_index += 1
        print(colors)
        # exit()
        # for i in range(len(sorted_pieces)):
        #     if set(each[3:]) == sorted_pieces[i]:
        #         # print(clr[i])
        #         # count += 1
        #         # print(count)
        #         colors.append(clr[i])
        #         print(clr[i])

    # print(colors)
    plt.interactive(False)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # axes =[2260,1320,1100]
    # data = np.ones(axes, dtype=np.bool)
    fig.add_axes(ax)

    for p, s, c in zip(positions, sizes, colors):
        plotcuboid(pos=p, size=s, ax=ax, color=c)
    if len(truck_dimension) != 0:
        ax.set_xlim3d([0.0, float(truck_dimension[0])])
        ax.set_xlabel('X')

        ax.set_ylim3d([0.0, float(truck_dimension[2])])
        ax.set_ylabel('Y')

        ax.set_zlim3d([0.0, float(truck_dimension[1])])
        ax.set_zlabel('Z')
    plt.title(title)
    plt.show()
    print(truck_dimension)
    return color_index

# %%
