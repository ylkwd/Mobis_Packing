import operator

from py3dbp import Packer, Bin, Item
# import Dataset as Dataset
import json
from py3dbp import visualize as vis2
from py3dbp.constants import RotationType, Axis


# def packing():
#     next_items
# Dataset.test_example()
def Mul_packing():
    packer = Packer()
    Box_Quantity = []
    next_items = {}

    container = {}
    count = 0
    Count = 0
    unfittedQuantity =[]
    filename ='input002-2'
    with open('../{}.json'.format(filename), 'r') as outfile:
        data = json.load(outfile)
    # with open('input_example1.json', 'r') as outfile:
    #     data = json.load(outfile)
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
        serial_box = data[p_ind]['Box Serials']
        print(len(boxes))
        total_value = data[p_ind]['total value']
        box_count = data[p_ind]['number']
        boxes_Id = []
        boxes_Serial = []

        # for i in range(len(truck_dimension)):

        # packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 700000.0))
        for each in boxes:
            Box_Quantity.append(each[4])

        # for i in range(0, len(packages)):
        #     # print(each)
        #     # print(serial_box[i][0])
        #     # print(packages[i][2])
        #     packer.add_item(Item(packages[i][2], serial_box[i][0], packages[i][3], packages[i][5], packages[i][4], 2))
        #     boxes_Id.append(packages[i][2])
        #     boxes_Serial.append(serial_box[i][0])
    ColorPair = {}
    count = 0
    color_index, Color_Id = vis2.draw(pieces=packages, title="True Solution Packing")
    print(color_index)

    print(Color_Id)

    for each in Color_Id:
        print(each)

        # index = Color_Id.index(each)
        color = Color_Id[each]
        # print(boxes_Serial[index])
        ColorPair[count+1] = {serial_box[count][0]: color}
        count += 1
    cratevolume = float(truck_dimension[0]*truck_dimension[1]*truck_dimension[2])
    print(cratevolume)


    for quantity in Box_Quantity:
        print(Box_Quantity.index(quantity))
        packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 700000.0))
        for i in range(0, quantity):
            packer.add_item(
                Item(packages[Box_Quantity.index(quantity)][2], serial_box[Box_Quantity.index(quantity)][0],
                     packages[Box_Quantity.index(quantity)][3],
                     packages[Box_Quantity.index(quantity)][5], packages[Box_Quantity.index(quantity)][4], 2))
            boxes_Id.append(packages[Box_Quantity.index(quantity)][2])
            boxes_Serial.append(serial_box[Box_Quantity.index(quantity)][0])

        print(boxes_Id, boxes_Serial)
        packer.pack()
        next_items = {}
        results = []
        layout = []
        finalresult = {}
        boxesvolume = 0

        # print(ColorPair)
        # exit()
        # print(len(color_index[0]),len(color_index[2]))

        for b in packer.bins:
            print(":::::::::::", b.string())

            print("FITTED ITEMS:")
            for item in b.items:
                print("====> ", item.string())
                boxesvolume += float(item.width * item.depth * item.height)
                if item.rotation_type == RotationType.RT_WHD:
                    results.append(
                        [int(item.Id), float(item.position[0]), float(item.position[2]), float(item.position[1]),
                         float(item.width),
                         float(item.depth), float(item.height), item.name])

                else:
                    results.append(
                        [int(item.Id), float(item.position[0]), float(item.position[2]), float(item.position[1]),
                         float(item.depth),
                         float(item.width), float(item.height), item.name])
            layout.append(results)
            print(len(results))

            unfittedQuantity.append(int(quantity%len(results)))

            print("***************************************************")
            print("***************************************************")
            ####Write results in file######
            for each in layout:
                # print(each)
                sorted_result = sorted(each, key=operator.itemgetter(3))
                print(sorted_result, len(sorted_result))
                # exit()

                finalresult[Count] = {'Crate dimension':truck_dimension,'Color index': color_index[1][Count],
                                      'crate quantity':int(quantity/len(results)),
                                      'volume percent': boxesvolume / cratevolume * 100.0,
                                       'box quantity': len(sorted_result),'box layout':sorted_result}
                    #####Write results in file######
                with open('{}output_Mutiple{}.json'.format(filename,Count + 1), 'w') as outfile:
                    json.dump(finalresult, outfile)
                    #####Write results in file######

                    #### Show in graphic
                vis2.draw(each, color_index, truck_dimension,
                         title="Figure {},# of boxes: {},volume percent:{}, crate quantity:{}, {} "
                          .format(Count + 1, len(each),boxesvolume / cratevolume * 100.0,int(quantity/len(results)), ColorPair))
                # ####

                # vis2.draw(each, color_index,truck_dimension,
                #           title="Figure {} levels: {},# of boxes: {},{} ".format(Count + 1, Count, count, ColorPair))

            # for each in sorted_result:
        Count +=1
        packer.items = []
        packer.bins = []
        boxes_Id = []
        boxes_Serial =[]

    print("***************************************************")
    print("***************************************************")
    print("***************************************************")
    print("***************************************************")

    print(unfittedQuantity)

    for quantity in unfittedQuantity:
        for i in range(0, quantity):
            packer.add_item(
                Item(packages[unfittedQuantity.index(quantity)][2], serial_box[unfittedQuantity.index(quantity)][0],
                     packages[unfittedQuantity.index(quantity)][3],
                     packages[unfittedQuantity.index(quantity)][5], packages[unfittedQuantity.index(quantity)][4], 2))
            boxes_Id.append(packages[unfittedQuantity.index(quantity)][2])
            boxes_Serial.append(serial_box[unfittedQuantity.index(quantity)][0])

    print(boxes_Id, boxes_Serial)
    packer.add_bin(Bin('large-2-box', 2, truck_dimension[0], truck_dimension[2], truck_dimension[1], 7000.0))

    while len(packer.items) > 0:

        packer.pack()
        next_items = {}
        results = []
        layout = []
        finalresult = {}

        boxesvolume = 0
        for b in packer.bins:
            print(":::::::::::", b.string())

            print("FITTED ITEMS:")
            for item in b.items:
                print("====> ", item.string())
                boxesvolume += float(item.width*item.depth*item.height)
                if item.rotation_type == RotationType.RT_WHD:
                    results.append(
                        [int(item.Id), float(item.position[0]), float(item.position[2]), float(item.position[1]),
                         float(item.width),
                         float(item.depth), float(item.height), item.name])

                else:
                    results.append(
                        [int(item.Id), float(item.position[0]), float(item.position[2]), float(item.position[1]),
                         float(item.depth),
                         float(item.width), float(item.height), item.name])
            layout.append(results)

                    ####Write results in file######
            for each in layout:
                # print(each)
                sorted_result = sorted(each, key=operator.itemgetter(3))
                print(sorted_result, len(sorted_result))
                # exit()

                finalresult[Count] = {'Crate dimension':truck_dimension,'Color index': color_index[1],
                                      'volume percent':boxesvolume/cratevolume*100.0,
                                       'box quantity': len(sorted_result),'box layout':sorted_result}
                    #####Write results in file######
                with open('Mixedoutput_Mutiple{}.json'.format(Count + 1), 'w') as outfile:
                    json.dump(finalresult, outfile)
                    #####Write results in file######
                    #### Show in graphic
                vis2.draw(each, color_index, truck_dimension,
                              title="Figure {},# of boxes: {},volume percent: {},{} ".format(Count + 1, len(each),
                                                                                              boxesvolume/cratevolume*100.0,ColorPair))
                    ####

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
#
