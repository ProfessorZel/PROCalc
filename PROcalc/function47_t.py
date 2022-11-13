#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json


def by(analysis, key, val, pos):
    if (analysis == None): return
    if (key == None): return
    if (val == None): return
    if (pos == None): return
    mkey = "max_"+key
    if (mkey in analysis):
        if (analysis[mkey] <= val):
            analysis[mkey] = val
            analysis[mkey+"_pos"] = pos
    else:
        analysis[mkey] = val
        analysis[mkey+"_pos"] = pos
        
    
    mskey = "maxs_"+key    
    if (mskey in analysis):
        if (analysis[mskey] < val):
            analysis[mskey] = val
            analysis[mskey+"_pos"] = pos
    else:
        analysis[mskey] = val
        analysis[mskey+"_pos"] = pos    
        
    lkey = "min_"+key
    if (lkey in analysis):
        if (analysis[lkey] >= val):
            analysis[lkey] = val
            analysis[lkey+"_pos"] = pos
    else:
        analysis[lkey] = val
        analysis[lkey+"_pos"] = pos
    
    lskey = "mins_"+key
    if (lskey in analysis):
        if (analysis[lskey] > val):
            analysis[lskey] = val
            analysis[lskey+"_pos"] = pos
    else:
        analysis[lskey] = val
        analysis[lskey+"_pos"] = pos
def str_(a):
    if (a==None):
        return "NULL"
    else:
        return str(a)
VERSION = 23052021
def run_OPTIM(con, IBC, D, RD):
    import pymysql
    import os
    #global RD
    #global dc
    import decimal as dc
    dc.getcontext().prec=16
    cur  = con.cursor(pymysql.cursors.DictCursor)
    
    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW() WHERE id={2}".format(VERSION,1,D.ID)
    cur.execute(req)
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) VALUES (NOW(), '0', %s, 'data', %s, 'calculation', %s)"
    cur.execute(req, (RD.ACC_ID,D.ID,"begin"))
    con.commit()
    
    max_x = -1
    cmpr = ">="
    if (D.count>0):
        req = ("SELECT MAX(`x`) as `max_x` FROM `{0}`;".format(D.table))
        #print(req)
        cur.execute(req)
        curr_dat = cur.fetchone()
        max_x = dc.Decimal(curr_dat['max_x']);
        if (max_x>dc.Decimal(D.params['x_min'])):
            cmpr = ">"
            D.params['x_min'] = curr_dat['max_x']
    fields=[]
    for i in range(1,IBC.n+1):
        fields.append("`{0}`.`C_{1}` as `C_{1}`".format(D.inputs['int225'],i))
    fields = ", ".join(fields)
    fields2=[]
    for i in range(1,IBC.n+1):
        fields2.append("`{0}`.`C-_{1}` as `C-_{1}`".format(D.inputs['f29'],i))
    fields2 = ", ".join(fields2)
    req = ("SELECT {0},{1},{2}.`x` FROM {2} INNER JOIN `{3}` ON (`{2}`.`x` = `{3}`.`x`) WHERE (`{2}`.`x`=ROUND(`{2}`.`x`,{4})) and(`{2}`.`x`{5}{6})and(`{2}`.`x`<={7})".format(fields,fields2, D.inputs['int225'],D.inputs['f29'],D.params['x_step'], cmpr, D.params['x_min'],D.params['x_max']))
    cur.execute(req)
    
    RAWDATA = cur.fetchall()
    
    #MATH#
    ANSWERS =[]

    for row in RAWDATA:
        if (row['x']==0):
            #F 2.12#
            B = 0
            for i in range(1,IBC.n+1):
                B += (IBC.B[str(i)]*(IBC.C0[str(i)]**2)*IBC.L[str(i)])
            #lamb = IBC['lambda_1']*IBC['c0_1']+IBC['lambda_2']*IBC['c0_2']
            left_hand = (dc.Decimal('1')/B)*(dc.Decimal('1')-(-B*dc.Decimal(D.params['t'])).exp())
            ans = {'x':0}
            for i in range(1,IBC.n+1):
                val = IBC.L[str(i)]*IBC.C0[str(i)]*left_hand
                ans[str(i)]=val
            
        else:
            ans = {'x':row['x']}
            down = dc.Decimal('0');
            for i in range(1,IBC.n+1):
                down +=IBC.B[str(i)]*IBC.C0[str(i)]*(IBC.C0[str(i)]-row['C-_'+str(i)])
                #print("Down",down)
            for i in range(1,IBC.n+1):
                if (row['C_'+str(i)]==None):
                    S = None
                else:
                    #print("C_-C-_",row['C_'+str(i)]-row['C-_'+str(i)])
                    S = (row['C_'+str(i)]-row['C-_'+str(i)])/down
                    #print("S",S)
                    if (S<0):
                        #print("E: S <0!")
                        S = 0
                ans[str(i)]=S
        Sum = dc.Decimal('0');
        for i in range(1,IBC.n+1):
            if (ans[str(i)]==None):
                Sum=None;
                break;
            else:
                Sum +=ans[str(i)];
        ans["Sum"]=Sum
        print (ans)
        ANSWERS.append(ans)
   
    
    data=[]
    fields=[]
    analysis = {}
    for i in range(1,IBC.n+1):
        fields.append("`S_"+str(i)+"`") 
    for row in ANSWERS:
        arr =[]
        arr.append(str_(row['x']))
        arr.append(str_(row['Sum']))
        by(analysis,"SumS",row['Sum'], row['x'])
        for i in range(1,IBC.n+1):
            arr.append(str_(row[str(i)]))
            by(analysis,"S_"+str(i),row[str(i)], row['x'])
        data.append("({0})".format(','.join(arr)))
    req = "INSERT INTO `{0}` (`x`,`SumS`, {1}) VALUES {2}; ".format(D.table,",".join(fields),",".join(data))
    #print(req)
    #input()
    cur.execute(req)
    con.commit()
    analysis = json.dumps(analysis,default=str)
    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW(), `analysis`=%s WHERE id={2}".format(VERSION,2,D.ID)
    cur.execute(req, (analysis))
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) VALUES (NOW(), '0', %s, 'data', %s, 'calculation', %s)"
    cur.execute(req, (RD.ACC_ID,D.ID,"complete"))
    con.commit()
    
    #print("END")
    con.close()
def run(con,data_id,n,IBC,table_name,inputs,params,count, RD):
    import pymysql
    import os
    import decimal as dc
    dc.getcontext().prec=16
    cur  = con.cursor(pymysql.cursors.DictCursor)
    
    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW() WHERE id={2}".format(VERSION,1,data_id)
    cur.execute(req)
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) VALUES (NOW(), '0', %s, 'data', %s, 'calculation', %s)"
    cur.execute(req, (RD.ACC_ID,data_id,"begin"))
    con.commit()
    
    max_x = -1
    cmpr = ">="
    if (count>0):
        req = ("SELECT MAX(`x`) as `max_x` FROM `{0}`;".format(table_name))
        #print(req)
        cur.execute(req)
        curr_dat = cur.fetchone()
        max_x = dc.Decimal(curr_dat['max_x']);
        if (max_x>dc.Decimal(params['x_min'])):
            cmpr = ">"
            params['x_min'] = curr_dat['max_x']
    fields=[]
    for i in range(1,n+1):
        fields.append("`{0}`.`C_{1}` as `C_{1}`".format(inputs['int225'],i))
    fields = ", ".join(fields)
    fields2=[]
    for i in range(1,n+1):
        fields2.append("`{0}`.`C-_{1}` as `C-_{1}`".format(inputs['f29'],i))
    fields2 = ", ".join(fields2)
    req = ("SELECT {0},{1},{2}.`x` FROM {2} INNER JOIN `{3}` ON (`{2}`.`x` = `{3}`.`x`) WHERE (`{2}`.`x`=ROUND(`{2}`.`x`,{4})) and(`{2}`.`x`{5}{6})and(`{2}`.`x`<={7})".format(fields,fields2, inputs['int225'],inputs['f29'],params['x_step'], cmpr, params['x_min'],params['x_max']))
    cur.execute(req)
    
    RAWDATA = cur.fetchall()
    
    #MATH#
    ANSWERS =[]

    

    
    #S1_max = [val,0]
    for row in RAWDATA:
        if (row['x']==0):
            #F 2.12#
            B = 0
            for i in range(1,n+1):
                B += (IBC['B'][str(i)]*(IBC['C_0'][str(i)]**2)*IBC['lambda'][str(i)])
            #lamb = IBC['lambda_1']*IBC['c0_1']+IBC['lambda_2']*IBC['c0_2']
            left_hand = (dc.Decimal('1')/B)*(dc.Decimal('1')-(-B*dc.Decimal(params['t'])).exp())
            ans = {'x':0}
            for i in range(1,n+1):
                val = IBC['lambda'][str(i)]*IBC['C_0'][str(i)]*left_hand
                ans[str(i)]=val
            
        else:
            ans = {'x':row['x']}
            down = dc.Decimal('0');
            for i in range(1,n+1):
                down +=IBC['B'][str(i)]*IBC['C_0'][str(i)]*(IBC['C_0'][str(i)]-row['C-_'+str(i)])
                #print("Down",down)
            for i in range(1,n+1):
                if (row['C_'+str(i)]==None):
                    S = None
                else:
                    #print("C_-C-_",row['C_'+str(i)]-row['C-_'+str(i)])
                    S = (row['C_'+str(i)]-row['C-_'+str(i)])/down
                    #print("S",S)
                    if (S<0):
                        #print("E: S <0!")
                        S = 0
                ans[str(i)]=S
        Sum = dc.Decimal('0');
        for i in range(1,n+1):
            if (ans[str(i)]==None):
                Sum=None;
                break;
            else:
                Sum +=ans[str(i)];
        ans["Sum"]=Sum
        print (ans)
        ANSWERS.append(ans)
   
    
    data=[]
    fields=[]
    analysis = {}
    for i in range(1,n+1):
        fields.append("`S_"+str(i)+"`") 
    for row in ANSWERS:
        arr =[]
        arr.append(str_(row['x']))
        arr.append(str_(row['Sum']))
        by(analysis,"SumS",row['Sum'], row['x'])
        for i in range(1,n+1):
            arr.append(str_(row[str(i)]))
            by(analysis,"S_"+str(i),row[str(i)], row['x'])
        data.append("({0})".format(','.join(arr)))
    req = "INSERT INTO `{0}` (`x`,`SumS`, {1}) VALUES {2}; ".format(table_name,",".join(fields),",".join(data))
    #print(req)
    #input()
    cur.execute(req)
    con.commit()
    analysis = json.dumps(analysis,default=str)
    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW(), `analysis`=%s WHERE id={2}".format(VERSION,2,data_id)
    cur.execute(req, (analysis))
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) VALUES (NOW(), '0', %s, 'data', %s, 'calculation', %s)"
    cur.execute(req, (RD.ACC_ID,data_id,"complete"))
    con.commit()
    
    #print("END")
    con.close()
