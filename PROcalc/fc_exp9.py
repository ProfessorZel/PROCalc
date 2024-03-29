import decimal as dc
dc.getcontext().prec=17


def fc_1(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - x)+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['1'])**(IBC['lambda']['2']/IBC['lambda']['1'])))+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - (IBC['C_0']['3']*(x/IBC['C_0']['1'])**(IBC['lambda']['3']/IBC['lambda']['1'])))+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - (IBC['C_0']['4']*(x/IBC['C_0']['1'])**(IBC['lambda']['4']/IBC['lambda']['1'])))+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - (IBC['C_0']['5']*(x/IBC['C_0']['1'])**(IBC['lambda']['5']/IBC['lambda']['1'])))+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - (IBC['C_0']['6']*(x/IBC['C_0']['1'])**(IBC['lambda']['6']/IBC['lambda']['1'])))+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - (IBC['C_0']['7']*(x/IBC['C_0']['1'])**(IBC['lambda']['7']/IBC['lambda']['1'])))+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - (IBC['C_0']['8']*(x/IBC['C_0']['1'])**(IBC['lambda']['8']/IBC['lambda']['1'])))+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - (IBC['C_0']['9']*(x/IBC['C_0']['1'])**(IBC['lambda']['9']/IBC['lambda']['1'])))))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"


def fc_2(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['2'])**(IBC['lambda']['1']/IBC['lambda']['2'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - x)+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - (IBC['C_0']['3']*(x/IBC['C_0']['2'])**(IBC['lambda']['3']/IBC['lambda']['2'])))+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - (IBC['C_0']['4']*(x/IBC['C_0']['2'])**(IBC['lambda']['4']/IBC['lambda']['2'])))+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - (IBC['C_0']['5']*(x/IBC['C_0']['2'])**(IBC['lambda']['5']/IBC['lambda']['2'])))+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - (IBC['C_0']['6']*(x/IBC['C_0']['2'])**(IBC['lambda']['6']/IBC['lambda']['2'])))+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - (IBC['C_0']['7']*(x/IBC['C_0']['2'])**(IBC['lambda']['7']/IBC['lambda']['2'])))+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - (IBC['C_0']['8']*(x/IBC['C_0']['2'])**(IBC['lambda']['8']/IBC['lambda']['2'])))+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - (IBC['C_0']['9']*(x/IBC['C_0']['2'])**(IBC['lambda']['9']/IBC['lambda']['2'])))))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"


def fc_3(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['3'])**(IBC['lambda']['1']/IBC['lambda']['3'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['3'])**(IBC['lambda']['2']/IBC['lambda']['3'])))+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - x)+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - (IBC['C_0']['4']*(x/IBC['C_0']['3'])**(IBC['lambda']['4']/IBC['lambda']['3'])))+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - (IBC['C_0']['5']*(x/IBC['C_0']['3'])**(IBC['lambda']['5']/IBC['lambda']['3'])))+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - (IBC['C_0']['6']*(x/IBC['C_0']['3'])**(IBC['lambda']['6']/IBC['lambda']['3'])))+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - (IBC['C_0']['7']*(x/IBC['C_0']['3'])**(IBC['lambda']['7']/IBC['lambda']['3'])))+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - (IBC['C_0']['8']*(x/IBC['C_0']['3'])**(IBC['lambda']['8']/IBC['lambda']['3'])))+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - (IBC['C_0']['9']*(x/IBC['C_0']['3'])**(IBC['lambda']['9']/IBC['lambda']['3'])))))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"


def fc_4(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['4'])**(IBC['lambda']['1']/IBC['lambda']['4'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['4'])**(IBC['lambda']['2']/IBC['lambda']['4'])))+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - (IBC['C_0']['3']*(x/IBC['C_0']['4'])**(IBC['lambda']['3']/IBC['lambda']['4'])))+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - x)+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - (IBC['C_0']['5']*(x/IBC['C_0']['4'])**(IBC['lambda']['5']/IBC['lambda']['4'])))+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - (IBC['C_0']['6']*(x/IBC['C_0']['4'])**(IBC['lambda']['6']/IBC['lambda']['4'])))+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - (IBC['C_0']['7']*(x/IBC['C_0']['4'])**(IBC['lambda']['7']/IBC['lambda']['4'])))+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - (IBC['C_0']['8']*(x/IBC['C_0']['4'])**(IBC['lambda']['8']/IBC['lambda']['4'])))+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - (IBC['C_0']['9']*(x/IBC['C_0']['4'])**(IBC['lambda']['9']/IBC['lambda']['4'])))))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"


def fc_5(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['5'])**(IBC['lambda']['1']/IBC['lambda']['5'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['5'])**(IBC['lambda']['2']/IBC['lambda']['5'])))+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - (IBC['C_0']['3']*(x/IBC['C_0']['5'])**(IBC['lambda']['3']/IBC['lambda']['5'])))+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - (IBC['C_0']['4']*(x/IBC['C_0']['5'])**(IBC['lambda']['4']/IBC['lambda']['5'])))+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - x)+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - (IBC['C_0']['6']*(x/IBC['C_0']['5'])**(IBC['lambda']['6']/IBC['lambda']['5'])))+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - (IBC['C_0']['7']*(x/IBC['C_0']['5'])**(IBC['lambda']['7']/IBC['lambda']['5'])))+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - (IBC['C_0']['8']*(x/IBC['C_0']['5'])**(IBC['lambda']['8']/IBC['lambda']['5'])))+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - (IBC['C_0']['9']*(x/IBC['C_0']['5'])**(IBC['lambda']['9']/IBC['lambda']['5'])))))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"


def fc_6(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['6'])**(IBC['lambda']['1']/IBC['lambda']['6'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['6'])**(IBC['lambda']['2']/IBC['lambda']['6'])))+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - (IBC['C_0']['3']*(x/IBC['C_0']['6'])**(IBC['lambda']['3']/IBC['lambda']['6'])))+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - (IBC['C_0']['4']*(x/IBC['C_0']['6'])**(IBC['lambda']['4']/IBC['lambda']['6'])))+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - (IBC['C_0']['5']*(x/IBC['C_0']['6'])**(IBC['lambda']['5']/IBC['lambda']['6'])))+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - x)+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - (IBC['C_0']['7']*(x/IBC['C_0']['6'])**(IBC['lambda']['7']/IBC['lambda']['6'])))+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - (IBC['C_0']['8']*(x/IBC['C_0']['6'])**(IBC['lambda']['8']/IBC['lambda']['6'])))+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - (IBC['C_0']['9']*(x/IBC['C_0']['6'])**(IBC['lambda']['9']/IBC['lambda']['6'])))))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"


def fc_7(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['7'])**(IBC['lambda']['1']/IBC['lambda']['7'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['7'])**(IBC['lambda']['2']/IBC['lambda']['7'])))+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - (IBC['C_0']['3']*(x/IBC['C_0']['7'])**(IBC['lambda']['3']/IBC['lambda']['7'])))+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - (IBC['C_0']['4']*(x/IBC['C_0']['7'])**(IBC['lambda']['4']/IBC['lambda']['7'])))+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - (IBC['C_0']['5']*(x/IBC['C_0']['7'])**(IBC['lambda']['5']/IBC['lambda']['7'])))+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - (IBC['C_0']['6']*(x/IBC['C_0']['7'])**(IBC['lambda']['6']/IBC['lambda']['7'])))+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - x)+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - (IBC['C_0']['8']*(x/IBC['C_0']['7'])**(IBC['lambda']['8']/IBC['lambda']['7'])))+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - (IBC['C_0']['9']*(x/IBC['C_0']['7'])**(IBC['lambda']['9']/IBC['lambda']['7'])))))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"


def fc_8(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['8'])**(IBC['lambda']['1']/IBC['lambda']['8'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['8'])**(IBC['lambda']['2']/IBC['lambda']['8'])))+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - (IBC['C_0']['3']*(x/IBC['C_0']['8'])**(IBC['lambda']['3']/IBC['lambda']['8'])))+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - (IBC['C_0']['4']*(x/IBC['C_0']['8'])**(IBC['lambda']['4']/IBC['lambda']['8'])))+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - (IBC['C_0']['5']*(x/IBC['C_0']['8'])**(IBC['lambda']['5']/IBC['lambda']['8'])))+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - (IBC['C_0']['6']*(x/IBC['C_0']['8'])**(IBC['lambda']['6']/IBC['lambda']['8'])))+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - (IBC['C_0']['7']*(x/IBC['C_0']['8'])**(IBC['lambda']['7']/IBC['lambda']['8'])))+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - x)+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - (IBC['C_0']['9']*(x/IBC['C_0']['8'])**(IBC['lambda']['9']/IBC['lambda']['8'])))))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"


def fc_9(x, IBC):
    try:
        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['9'])**(IBC['lambda']['1']/IBC['lambda']['9'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['9'])**(IBC['lambda']['2']/IBC['lambda']['9'])))+IBC['B']['3']*IBC['C_0']['3']*(IBC['C_0']['3'] - (IBC['C_0']['3']*(x/IBC['C_0']['9'])**(IBC['lambda']['3']/IBC['lambda']['9'])))+IBC['B']['4']*IBC['C_0']['4']*(IBC['C_0']['4'] - (IBC['C_0']['4']*(x/IBC['C_0']['9'])**(IBC['lambda']['4']/IBC['lambda']['9'])))+IBC['B']['5']*IBC['C_0']['5']*(IBC['C_0']['5'] - (IBC['C_0']['5']*(x/IBC['C_0']['9'])**(IBC['lambda']['5']/IBC['lambda']['9'])))+IBC['B']['6']*IBC['C_0']['6']*(IBC['C_0']['6'] - (IBC['C_0']['6']*(x/IBC['C_0']['9'])**(IBC['lambda']['6']/IBC['lambda']['9'])))+IBC['B']['7']*IBC['C_0']['7']*(IBC['C_0']['7'] - (IBC['C_0']['7']*(x/IBC['C_0']['9'])**(IBC['lambda']['7']/IBC['lambda']['9'])))+IBC['B']['8']*IBC['C_0']['8']*(IBC['C_0']['8'] - (IBC['C_0']['8']*(x/IBC['C_0']['9'])**(IBC['lambda']['8']/IBC['lambda']['9'])))+IBC['B']['9']*IBC['C_0']['9']*(IBC['C_0']['9'] - x)))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"
def links():
    return [fc_1, fc_2, fc_3, fc_4, fc_5, fc_6, fc_7, fc_8, fc_9]
