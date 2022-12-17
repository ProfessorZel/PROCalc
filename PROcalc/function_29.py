#!/usr/bin/python3
# -*- coding: utf-8 -*-

VERSION = 14112022


def run(con, data_id, n, IBC, table_name, inputs, params, count, RD):
    import pymysql
    import numpy as np
    import decimal as dc
    dc.getcontext().prec = 17
    cur = con.cursor(pymysql.cursors.DictCursor)

    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW(), `attempt` = `attempt` + 1 WHERE id={2}"\
        .format(VERSION, 1, data_id)
    cur.execute(req)
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) " \
          "VALUES (NOW(), '0', %s, 'data', %s, 'calculation', %s)"
    cur.execute(req, (RD.ACC_ID, data_id, "begin"))
    con.commit()

    secrun = False
    if count > 0:
        req = ("SELECT MAX(`x`) as `max_x` FROM `{0}`;".format(table_name))
        cur.execute(req)
        curr_dat = cur.fetchone()
        max_x = dc.Decimal(curr_dat['max_x'])
        if max_x > dc.Decimal(params['x_min']):
            params['x_min'] = curr_dat['max_x']
            secrun = True
    # MATH#
    if (secrun):
        X = np.arange(dc.Decimal(params['x_min']) + dc.Decimal('0.1') ** dc.Decimal(params['step']),
                      dc.Decimal(params['x_max']), dc.Decimal('0.1') ** dc.Decimal(params['step']))
    else:
        X = np.arange(dc.Decimal(params['x_min']), dc.Decimal(params['x_max']),
                      dc.Decimal('0.1') ** dc.Decimal(params['step']))
    R = []
    for x in X:
        row = [x]
        for i in range(1, n + 1):
            lx = -IBC['lambda'][str(i)] * x
            row.append(IBC['C_0'][str(i)] * lx.exp())
        R.append(row)

    if len(R) > 0:
        data = []
        fields = []
        for i in range(1, n + 1):
            fields.append("`C-_" + str(i) + "`")
        for row in R:
            data.append("({0})".format(','.join([str(i) for i in row])))
        req = "INSERT INTO `{0}` (`x`, {1}) VALUES {2}; ".format(table_name, ",".join(fields), ",".join(data))
        cur.execute(req)
        con.commit()

    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW() WHERE id={2}".format(VERSION, 2, data_id)
    cur.execute(req)
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) " \
          "VALUES (NOW(), '0', %s, 'data', %s, 'calculation', %s)"
    cur.execute(req, (RD.ACC_ID, data_id, "complete"))
    con.commit()

    print("END")
    con.close()
