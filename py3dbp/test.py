from py3dbp import Packer, Bin, Item
import Dataset as Dataset
import json
from py3dbp import visualize as vis2
from py3dbp.constants import RotationType, Axis


# def packing():
#     next_items
# Dataset.test_example()
def Mul_packing():
    packer = Packer()

    next_items = {}

    container = {}
    count = 0
    Count = 0

    with open('../input.json', 'r') as outfile:
        data = json.load(outfile)
    # container  = Dataset.test_example()
    # # container = dataset
    # print(container)
    # exit()
    problem_indices = list(data.keys())
    for p_ind in problem_indices:
        truck_dimension = data[p_ind]['truck dimension']
        packages = data[p_ind]['solution']
        print(len(packages))
        boxes = data[p_ind]['boxes']
        print(len(boxes))
        total_value = data[p_ind]['total value']
        box_count = data[p_ind]['number']

        # for i in range(len(truck_dimension)):

        packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 700000.0))

        # for i in range(0, 84):
        #     packer.add_item(Item('50g [powder 1]', 25, 860, 400, 360, 1))
        # for i in range(0, 48):
        #     packer.add_item(Item('50g [powder 2]', 25, 860, 610, 310, 2))

        for box in packages:
            packer.add_item(Item('Box', box[2], box[3], box[5], box[4], 2))

    while len(packer.items) > 0:
        packer.pack()
        next_items = {}
        results = []
        finalresult = []


        color_index, ColorPair = vis2.draw(pieces=packages, title="True Solution Packing")
        for b in packer.bins:
            print(":::::::::::", b.string())

            print("FITTED ITEMS:")
            for item in b.items:
                print("====> ", item.string())
                if item.rotation_type == RotationType.RT_WHD:
                    results.append(
                        [float(item.position[0]), float(item.position[2]), float(item.position[1]), float(item.width),
                         float(item.depth), float(item.height)])
                else:
                    results.append(
                        [float(item.position[0]), float(item.position[2]), float(item.position[1]), float(item.depth),
                         float(item.width), float(item.height)])
            finalresult.append(results)

            with open('output_{file_count}.json'.format(file_count=Count), 'w') as outfile:
                json.dump(finalresult, outfile)
            # print(results)
            print(finalresult)
            # print(color_index)

            print("UNFITTED ITEMS:")
            # exit(0)
            count = 0
            for item in b.unfitted_items:
                print("====> ", item.string())

                # print(item.name,int(item.width),type(item.width))
                next_items[count] = {'Id': item.Id, 'name': item.name, 'width': int(item.width),
                                     'height': int(item.height),
                                     "depth": int(item.depth), "weight": int(item.weight)}
                count += 1

            packer.unfitted_items = []
            print(count)
            print("***************************************************")
            print("***************************************************")
            print(truck_dimension[0], truck_dimension[1])
            for each in finalresult:
                # print(each)
                vis2.draw(each, color_index, title="Figure {},{} ".format(Count + 1, ColorPair))
        packer.items = []
        packer.bins = []
        for i in list(next_items.keys()):
            # print()
            packer.add_item(
                Item(next_items[i]['Id'], next_items[i]['name'], next_items[i]['width'], next_items[i]['height'],
                     next_items[i]['depth'],
                     next_items[i]['weight']))
        packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 7000.0))
        print(len(packer.items))
        print(len(packer.unfitted_items))
        print(len(packer.bins))
        Count += 1

Mul_packing()