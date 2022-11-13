#!/usr/bin/python3
# -*- coding: utf-8 -*-


VERSION = 14112022


def run(con, data_id, n, IBC, table_name, inputs, params, count, RD):
    import pymysql
    import decimal as dc
    dc.getcontext().prec = 16
    cur = con.cursor(pymysql.cursors.DictCursor)

    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW(), `attempt` = `attempt` + 1 WHERE id={2}".format(VERSION, 1, data_id)
    cur.execute(req)
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) " \
          "VALUES (NOW(), '0', %s, 'data', %s, 'calculation', %s)"
    cur.execute(req, (RD.ACC_ID, data_id, "begin"))
    con.commit()

    cmpr = ">="
    if count > 0:
        req = ("SELECT MAX(`x`) as `max_x` FROM `{0}`;".format(table_name))
        cur.execute(req)
        curr_dat = cur.fetchone()
        max_x = dc.Decimal(curr_dat['max_x'])
        if max_x > dc.Decimal(params['x_min']):
            cmpr = ">"
            params['x_min'] = curr_dat['max_x']
    fields = []
    for i in range(1, n + 1):
        fields.append("`{0}`.`C_{1}` as `C_{1}`".format(inputs['int225'], i))
    fields = ", ".join(fields)
    req = (
        "SELECT {0},{1}.`x` FROM {1} WHERE (`{1}`.`x`=ROUND(`{1}`.`x`,{2})) and(`{1}`.`x`{3}{4})and(`{1}`.`x`<={5})".format(
            fields, inputs['int225'], params['x_step'], cmpr, params['x_min'], params['x_max']))
    print(req)
    cur.execute(req)

    RAWDATA = cur.fetchall()
    # MATH#
    ANSWERS = []
    dub = params['calc'].copy()
    calc = []
    for i in params['calc']:
        dub.remove(i)
        for j in dub:
            calc.append([i, j])
    for i, j in calc:
        print(str(i) + "." + str(j))

    for row in RAWDATA:
        ans = {'x': row['x']}
        for i, j in calc:
            if (row["C_{0}".format(i)] is None) or (row["C_{0}".format(j)] is None):
                ans[str(i) + "." + str(j)] = "NULL"
            else:
                ans[str(i) + "." + str(j)] = row["C_{0}".format(i)] - IBC['C_0'][str(i)] * (
                            row["C_{0}".format(j)] / IBC['C_0'][str(j)]) ** (
                                                         IBC['lambda'][str(i)] / IBC['lambda'][str(j)])

        # print (ans)
        ANSWERS.append(ans)

    if len(ANSWERS) > 0:
        data = []
        fields = []
        for i, j in calc:
            fields.append("`A_" + str(i) + "_" + str(j) + "`")
        for row in ANSWERS:
            arr = []
            arr.append(str(row['x']))
            for i, j in calc:
                arr.append(str(row[str(i) + "." + str(j)]))
            data.append("({0})".format(','.join(arr)))
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
