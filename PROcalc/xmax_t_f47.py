#!/usr/bin/python3
# -*- coding: utf-8 -*-


VERSION = 14112022


def run(con, data_id, n, IBC, table_name, inputs, params, count, RD):
    import pymysql
    import decimal as dc
    import json
    dc.getcontext().prec = 16
    cur = con.cursor(pymysql.cursors.DictCursor)

    req = "UPDATE `data` SET `state`={1},`time`=NOW(), `attempt` = `attempt` + 1 WHERE id={2}"\
        .format(VERSION, 1, data_id)
    cur.execute(req)
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) " \
          "VALUES (NOW(), '0', %s, 'data', %s, 'calculation', %s)"
    cur.execute(req, (RD.ACC_ID, data_id, "begin"))
    con.commit()

    req = "SELECT `host1596090_math`.`data`.* " \
          "FROM `data` INNER JOIN `tasks` ON (data.taskID=tasks.id) INNER JOIN `functions` ON (functions.id=tasks.function)" \
          "WHERE (`functions`.`canonical_name` = 'f47') AND (`tasks`.`ibc`={0}) AND (`data`.`state` IN (2,3,6))".format(IBC['id'])
    print(req)
    cur.execute(req)

    RAWDATA = cur.fetchall()

    # MATH#
    ANSWERS = []

    for row in RAWDATA:
        ans = {}

        # t
        p = json.loads(row['params'])
        ans['t'] = p['t']

        a = json.loads(row['analysis'])
        print(a)

        # max process
        if params['max_mode'] == "left":
            ans['max_SumS'] = str(a['maxs_SumS_pos'])
            for i in range(1, n + 1):
                ans['max_S_' + str(i)] = str(a['maxs_S_' + str(i) + "_pos"])
        elif params['max_mode'] == "right":
            ans['max_SumS'] = str(a['max_SumS_pos'])
            for i in range(1, n + 1):
                ans['max_S_' + str(i)] = str(a['max_S_' + str(i) + "_pos"])
        else:
            ans['max_SumS'] = str((dc.Decimal(a['maxs_SumS_pos']) + dc.Decimal(a['max_SumS_pos'])) / dc.Decimal('2.0'))
            for i in range(1, n + 1):
                ans['max_S_' + str(i)] = str((dc.Decimal(a['maxs_S_' + str(i) + "_pos"])
                                              + dc.Decimal(a['max_S_' + str(i) + "_pos"])) / dc.Decimal('2.0'))

        # min process
        if params['min_mode'] == "left":
            ans['min_SumS'] = str(a['mins_SumS_pos'])
            for i in range(1, n + 1):
                ans['min_S_' + str(i)] = str(a['mins_S_' + str(i) + "_pos"])
        elif params['min_mode'] == "avg":
            ans['min_SumS'] = str((dc.Decimal(a['mins_SumS_pos']) + dc.Decimal(a['min_SumS_pos'])) / dc.Decimal('2.0'))
            for i in range(1, n + 1):
                ans['min_S_' + str(i)] = str((dc.Decimal(a['mins_S_' + str(i) + "_pos"]) + dc.Decimal(
                    a['min_S_' + str(i) + "_pos"])) / dc.Decimal('2.0'))
        else:
            ans['min_SumS'] = str(a['min_SumS_pos'])
            for i in range(1, n + 1):
                ans['min_S_' + str(i)] = str(a['min_S_' + str(i) + "_pos"])
        print(ans)
        ANSWERS.append(ans)
    print(ANSWERS)

    if (len(ANSWERS) > 0):
        data = []
        fields = ['t', 'min_SumS', 'max_SumS']
        for i in range(1, n + 1):
            fields.append('min_S' + str(i))
        for i in range(1, n + 1):
            fields.append('max_S' + str(i))

        for row in ANSWERS:
            arr = []
            arr.append("'" + str(row['t']) + "'")
            arr.append("'" + str(row['min_SumS']) + "'")
            arr.append("'" + str(row['max_SumS']) + "'")
            for i in range(1, n + 1):
                arr.append("'" + row['min_S_' + str(i)] + "'")
            for i in range(1, n + 1):
                arr.append("'" + row['max_S_' + str(i)] + "'")
            data.append("({0})".format(','.join(arr)))
        req = "INSERT INTO `{0}` ({1}) VALUES {2}; ".format(table_name, ",".join(fields), ",".join(data))
        print(req)
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
