import decimal as dc
dc.getcontext().prec=17
def fc_1(x,IBC):
    try:        return dc.Decimal('1')/(x*(IBC['B']['1']*IBC['C_0']['1']*(IBC['C_0']['1'] - x)))
    except Exception as e:
        print(e)
        print("fc exeption")
        return "NULL"
def links():
    return [fc_1]
