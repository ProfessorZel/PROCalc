def gexp(n):
    a = "import decimal as dc\ndc.getcontext().prec=17\n"
    for k in range(1, n + 1):
        a += '''\n\ndef fc_{0}(x, IBC):\n    try:\n'''.format(k)
        summ = []
        for i in range(1, n + 1):
            if i == k:
                ri = "x"
            else:
                ri = "(IBC['C_0']['{0}']*(x/IBC['C_0']['{1}'])**(IBC['lambda']['{0}']/IBC['lambda']['{1}']))".format(i, k)
            summ.append("IBC['B']['{0}']*IBC['C_0']['{0}']*(IBC['C_0']['{0}'] - {1})".format(i, ri))
        a += '''        return dc.Decimal('1')/(x*({0}))
    except Exception as e:
        print(e)
        print("fc exception")
        return "NULL"
'''.format('+'.join(summ))

    a += "\n\ndef links():\n"
    fs = []
    for i in range(1, n + 1):
        fs.append("fc_{0}".format(i))
    a += "    return [{0}]\n".format(', '.join(fs))
    return a


def generate(n, name="fc_exp"):
    filename = "{0}.py".format(name)
    file = open(filename, 'w')
    a = gexp(n)
    file.write(a)
    file.close()
