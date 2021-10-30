class RotationType:
    RT_WHD = 1
    # RT_HWD = 1
    # RT_HDW = 2
    RT_DHW = 0
    # RT_DWH = 4
    # RT_WDH = 5

    # ALL = [RT_WHD, RT_HWD, RT_HDW, RT_DHW, RT_DWH, RT_WDH]
    ALL = [RT_DHW,RT_WHD]


class Axis:
    WIDTH = 0
    HEIGHT = 1
    DEPTH = 2

    ALL = [WIDTH, HEIGHT, DEPTH]
