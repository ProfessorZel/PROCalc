import decimal as dc
dc.getcontext().prec=17
def fc_1(x,IBC):
    try:        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - x)+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - (IBC['C_0']['2']*(x/IBC['C_0']['1'])**(IBC['lambda']['2']/IBC['lambda']['1'])))))
    except Exception as e:
        print(e)
        print("fc exeption")
        return "NULL"
def fc_2(x,IBC):
    try:        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - (IBC['C_0']['1']*(x/IBC['C_0']['2'])**(IBC['lambda']['1']/IBC['lambda']['2'])))+IBC['B']['2']*IBC['C_0']['2']*(IBC['C_0']['2'] - x)))
    except Exception as e:
        print(e)
        print("fc exeption")
        return "NULL"
def links():
    return [fc_1,fc_2]
