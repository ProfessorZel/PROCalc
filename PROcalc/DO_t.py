import decimal as dc
import json
import traceback

import pymysql
from pymysql.cursors import DictCursor

from . import a_pass as RD

VERSION = 14112022


def do_by_id(request):
    data_id = int(request['id'])
    con = pymysql.connect(host=RD.host, user=RD.user, password=RD.password, database=RD.db)
    cur = con.cursor(DictCursor)
    try:
        req = (
            "SELECT `data`.*, functions.canonical_name as `f_name`,"
            "ibc.id as `ibc_id`,ibc.n as `ibc_n`,ibc.B as "
            "`ibc_B`,ibc.lambda as `ibc_L`,ibc.C_0 as `ibc_C0`,"
            "INFORMATION_SCHEMA.TABLES.`table_rows` as `rows_count` FROM `data` INNER JOIN `tasks` ON ("
            "data.taskID=tasks.id) INNER JOIN `ibc` ON (tasks.ibc=ibc.id) INNER JOIN `functions` ON (functions.id "
            "=tasks.function) INNER JOIN INFORMATION_SCHEMA.TABLES ON (`data`.`table_name` = "
            "INFORMATION_SCHEMA.TABLES.`table_name`)  WHERE (data.id={0})".format(data_id))
        cur.execute(req)
        data = cur.fetchone()
        print(data)
        if data is None:
            raise Exception('No task {0} found'.format(data_id))

        n = data['ibc_n']
        params = json.loads(data['params'])
        inputs = json.loads(data['inputs'])
        data_table = data['table_name']
        count = data['rows_count']
        state = data['state']

        if state == 8:
            print('Вычисление запрещено!')
            return

        ibc = {'B': json.loads(data['ibc_B']),
               'lambda': json.loads(data['ibc_L']),
               'C_0': json.loads(data['ibc_C0']),
               'id': data['ibc_id']
               }
        for i in range(1, n + 1):
            ibc['B'][str(i)] = dc.Decimal(ibc['B'][str(i)])
            ibc['lambda'][str(i)] = dc.Decimal(ibc['lambda'][str(i)])
            ibc['C_0'][str(i)] = dc.Decimal(ibc['C_0'][str(i)])

        f_sel = data['f_name']
        if f_sel == 'f29':
            from . import function_29 as f29
            f29.run(con, data_id, n, ibc, data_table, inputs, params, count, RD)
        elif f_sel == 'int225':
            from . import integral_225new_t as i225
            i225.run(con, data_id, n, ibc, data_table, inputs, params, count, RD)
        elif f_sel == 'f47':
            from . import function47_t as f47
            f47.run(con, data_id, n, ibc, data_table, inputs, params, count, RD)
            # f47.run(con,IBC,D, RD)
        elif f_sel == 'f47_x_normalised':
            from . import function47_x_norm as f47_x_norm
            f47_x_norm.run(con, data_id, n, ibc, data_table, inputs, params, count, RD)
        elif f_sel == 'valid_t':
            from . import validate_t as vt
            vt.run(con, data_id, n, ibc, data_table, inputs, params, count, RD)
        elif f_sel == 'xmax_t_f47':
            from . import xmax_t_f47 as xm
            xm.run(con, data_id, n, ibc, data_table, inputs, params, count, RD)
        elif f_sel == 'xmax_t_f47_x_normalised':
            from . import xmax_t_f47_x_norm as xn
            xn.run(con, data_id, n, ibc, data_table, inputs, params, count, RD)
        else:
            print("Function UNKNOWN")
    except Exception as error:
        if not con or not con.open or not cur:
            con = pymysql.connect(host=RD.host, user=RD.user, password=RD.password, database=RD.db)
            cur = con.cursor(pymysql.cursors.DictCursor)
            print("con reopened! DO_t")
        err = traceback.format_exc()
        print(err)

        # update of data state, time and version
        req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW() WHERE id={2}".format(VERSION, 4, data_id)
        cur.execute(req)

        # add log record
        req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) " \
              "VALUES (NOW(), '3', %s, 'data', %s, 'calculate', %s) "
        cur.execute(req, (RD.ACC_ID, data_id, str(error) + ";\n" + str(err)))

        con.commit()
        con.close()
