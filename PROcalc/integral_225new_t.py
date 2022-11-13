#!/usr/bin/python3
# -*- coding: utf-8 -*-
import decimal as dc
import time
import traceback

TIMEOUT = 12
TIMEOUT = TIMEOUT*60

dc.getcontext().prec=16
import numpy as np
CHUNCK_SIZE = 15
VERSION = 17072021
class Quadrature:
    """Базовые определения для квадратурных формул"""
    __sum = dc.Decimal('0.0')
    __nseg = dc.Decimal('1')  # число отрезков разбиения
    __ncalls = 0 # считает число вызовов интегрируемой функции

    def __restart(func,IBC, x0, x1, nseg0, reset_calls = True):
        """Обнуление всех счётчиков и аккумуляторов.
           Возвращает интеграл методом трапеций на начальном разбиении"""
        if reset_calls:
            Quadrature.__ncalls = 0
        Quadrature.__nseg = nseg0
        # вычисление суммы для метода трапеций с начальным числом отрезков разбиения nseg0
        
        Quadrature.__sum = dc.Decimal('0.5') * (func(x0,IBC) + func(x1,IBC))
        dx = (x1 - x0) / nseg0
        for i in np.arange(1, nseg0):
            Quadrature.__sum += func(x0 + i * dx,IBC)

        Quadrature.__ncalls += 1 + nseg0
        return Quadrature.__sum * dx

    def __double_nseg(func,IBC, x0, x1):
        """Вдвое измельчает разбиение.
           Возвращает интеграл методом трапеций на новом разбиении"""
        nseg = Quadrature.__nseg
        dx = (x1 - x0) / nseg
        x = x0 + dc.Decimal('0.5') * dx
        i = 0
        AddedSum = dc.Decimal('0.0')
        for i in np.arange(nseg):
            AddedSum += func(x + i * dx,IBC)

        Quadrature.__sum += AddedSum
        Quadrature.__nseg *= 2
        Quadrature.__ncalls += nseg
        return Quadrature.__sum * dc.Decimal('0.5') * dx

    def trapezoid(func,IBC, x0, x1, rtol = 1e-10, nseg0 = 1):
        """Интегрирование методом трапеций с заданной точностью.
           rtol - относительная точность,
           nseg0 - число отрезков начального разбиения"""
        ans = Quadrature.__restart(func,IBC, x0, x1, nseg0)
        old_ans = 0.0
        err_est = max(1, abs(ans))
        while (err_est > abs(rtol * ans)):
            old_ans = ans
            ans = Quadrature.__double_nseg(func,IBC, x0, x1)
            err_est = abs(old_ans - ans)

        #print("Total function calls: " + str(Quadrature.__ncalls))
        return ans

    def simpson(func,IBC, x0, x1, rtol, nseg0 = 1,assert_max = 513):
        """Интегрирование методом парабол с заданной точностью.
           rtol - относительная точность,
           nseg0 - число отрезков начального разбиения"""
        old_trapez_sum = Quadrature.__restart(func,IBC, x0, x1, nseg0)
        new_trapez_sum = Quadrature.__double_nseg(func,IBC, x0, x1)
        ans = (dc.Decimal('4') * new_trapez_sum - old_trapez_sum) / dc.Decimal('3')
        old_ans = dc.Decimal('0.0')
        err_est = max(1, abs(ans))
        while (err_est > abs(rtol * ans)):
            old_ans = ans
            old_trapez_sum = new_trapez_sum
            new_trapez_sum = Quadrature.__double_nseg(func,IBC, x0, x1)
            ans = (dc.Decimal('4') * new_trapez_sum - old_trapez_sum) / dc.Decimal('3')
            err_est = abs(old_ans - ans)
            if (Quadrature.__ncalls > assert_max):
                print("E: Assert n_assert")
                break

        #print("Total function calls: " + str(Quadrature.__ncalls))
        return ans.copy_abs()
def run(con,data_id,n,IBC,table_name,inputs,params,count,RD):
    global CHUNCK_SIZE
    global TIMEOUT
    degin_time = time.time()
    script_time = time.time()
    times = []
    import pymysql
    from scipy import integrate
    
    if not con or not con.open:
        con = pymysql.connect(RD.host, RD.user, RD.password , RD.db)
        print("con reopened!")
    cur  = con.cursor(pymysql.cursors.DictCursor)
        
    
    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW() WHERE id={2}".format(VERSION,1,data_id)
    cur.execute(req)
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) VALUES (NOW(), '0', '7', 'data', %s, 'calculation', %s)"
    cur.execute(req, (data_id,"begin"))
    con.commit()
    
    t = dc.Decimal(params['t'])
    ACCURACY = dc.Decimal(params['accuracy'])
    
    fields=[]
    for i in range(1,n+1):
        fields.append("`C-_{0}` as `C-_{0}`".format(i))
    fields = ", ".join(fields)
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
    req = "SELECT `x`, {0} FROM `{1}` WHERE (`x`=ROUND(`x`,{2})) and(`x`{3}{4})and(`x`<={5})".format(fields,inputs['f29'],params['x_step'], cmpr, params['x_min'],params['x_max'])
    print(req)
    cur.execute(req)
    
    F291 = cur.fetchall()
    
    #MATH#
    Delta = dc.Decimal('0.1')**ACCURACY
    if (n==1):
        from . import fc_exp1 as fc
    if (n==2):
        from . import fc_exp2 as fc
    if (n==3):
        from . import fc_exp3 as fc
    if (n==4):
        from . import fc_exp4 as fc
    if (n==5):
        from . import fc_exp5 as fc
    if (n==6):
        from . import fc_exp6 as fc
    if (n==7):
        from . import fc_exp7 as fc
    if (n==8):
        from . import fc_exp8 as fc
    if (n==9):
        from . import fc_exp9 as fc
    if (n==10):
        from . import fc_exp10 as fc
    if (n==11):
        from . import fc_exp11 as fc
    if (n==12):
        from . import fc_exp12 as fc
    if (n>12):
        raise "n > 12, no pre-generated links"
    f = fc.links()
    
    
    base = None
    m = dc.Decimal('-1');
    params['calc'] =  [str(i) for i in params['calc']]
    if ("auto" in params['calc']):
        params['calc'].remove("auto")
        if (len(params['calc']) == 0): params['calc'] = [str(i) for i in range(1,n+1)]
        for i in params['calc']:
            if (m < IBC['C_0'][i]):
                m = IBC['C_0'][i]
                base = i;
        params['calc'] = [base]
    else:
        for i in params['calc']:
            if (m < IBC['C_0'][i]):
                m = IBC['C_0'][i]
                base = i;
    if (base == None):
        raise "Консенсус по базовому параметру оптимизации не состоялся"
    sub_calc =[]
    for i in range(1,n+1):
        i = str(i)
        if not(i in params['calc']):
            sub_calc.append(i)
    print(params['calc'], sub_calc)
    chunck = []
    res={}
    state={}
    for f291 in F291:
        x = f291['x']

        if (not x.is_zero()):
            for i in params['calc']:
                try:
                    Need = IBC['lambda'][i]*(t-x)
                    Cm = f291['C-_'+i]
                    if ((i in res) and not(res[i] == 'NULL')):
                        #print("Used res:", res,"; i=" ,i);
                        Cp = res[i]
                        if((Cp<Cm) or (Cp >= IBC['C_0'][i])):
                            print("(Cp<Cm) or (Cp >= IBC['C_0'][i]): true")
                            Cp = Cm
                        
                    else:
                        #print("No res to use, defaulted")
                        Cp = Cm
                    
                    if ((i in state) and (state[i] != "NULL")):
                        #print("Used state:", state,"; i=" ,i);
                        st = state[i]
                        Depth = st['Depth']
                        plus = False
                    else:
                        #print("No state to use, defaulted")
                        Depth = dc.Decimal('1')
                        plus = False

                    
                    IntStep = dc.Decimal('0.1')**Depth
                    if(plus):
                        Step = IntStep
                    else:
                        Step = dc.Decimal('-1')*IntStep
                            
                    S = dc.Decimal('-1')
                    
                    best = [dc.Decimal('10000000'),'NULL']
                    
                    if (Need<=0):
                        print("No calc! Need <=0! best[1]=Cm=",Cm);
                        best[1] = Cm
                    else:    
                        while (abs(Need-S) >Delta):
                            if (time.time()-degin_time>90):
                                print("E: Assert Execution Time")
                                break;
                            
                            if (Depth>ACCURACY+1):
                                print("E: Assert ACCURACY")
                                break;
                            #print("(f[",int(i)-1,"], IBC, ",Cm,", ",Cp,",",IntStep,")")
                            S = Quadrature.simpson(f[int(i)-1], IBC, Cm, Cp,IntStep)
                            #print("S=",S,"; Need=", Need, "; Cp=", Cp)
                                
                            if (S == "NULL"):
                                Cp-=Step
                                Depth += dc.Decimal('1')
                                Step = dc.Decimal('0.1')**Depth
                                Cp +=Step
                                S = dc.Decimal('-1')
                            else:
                                smneed = abs(S-Need)
                                if (best[1]=='NULL'):
                                    best[0]= smneed
                                    best[1]= Cp
                                if (smneed < best[0]):
                                    best[0]= smneed
                                    best[1]= Cp
                           
                                if (S < Need):
                                    if (not(plus)):
                                        Depth += dc.Decimal('1')
                                        Step = dc.Decimal('0.1')**Depth
                                        IntStep = dc.Decimal('0.1')**Depth
                                        plus = True
                                if (S > Need):
                                    if(plus):
                                        Depth += dc.Decimal('1')
                                        #it is optimal! think about n2 power, then minus goes to plus
                                        Step = dc.Decimal('-1')*dc.Decimal('0.1')**Depth
                                        IntStep = dc.Decimal('0.1')**Depth
                                        plus = False
                                        #print("(Depth+,dir+)")
                                Cp +=Step
                            while ((Cp<Cm)or(Cp>IBC['C_0'][i])):
                                Cp-=Step
                                Depth += dc.Decimal('1')
                                Step *= dc.Decimal('0.1')
                                Cp +=Step
                                S = dc.Decimal('-1')
                except:
                    print("E: Exception accured!")
                    traceback.print_exc()
                    best[1]="NULL"
                
                
                #state save
                if ((best[1]!="NULL") and (i in res) and (res[i]!="NULL")):
                    
                    #определить Depth по изменению значения c интерполяцией по old_st
                    diff = res[i] - best[1]
                    if(not diff.is_zero()):
                        #old_st = state[i] if (i in state) else "NULL"
                        st = {}
                        new_depth = min(ACCURACY, max(2, -np.ceil(np.log10(abs(diff)))))
                        #if (old_st!="NULL"):
                        #    st['Depth'] = new_depth + min(-1, (new_depth - old_st['Depth']))
                        #else:
                        st['Depth'] = new_depth - 1
                        state[i] = st
                        #print("diff=", diff,"; Depth=", st['Depth'])
                    #else:
                        #print("diff is 0, no changes in state")
                else:
                    state[i] = "NULL"
                    
                res[i]=best[1]


            if (res[base]=="NULL"):
                for i in sub_calc:
                    res[i] = "NULL"
            else:
                for i in sub_calc:
                    res[i] = IBC['C_0'][i]*(res[base]/IBC['C_0'][base])**(IBC['lambda'][i]/IBC['lambda'][base])
                
        else:
            for i in range(1,n+1):
                res[str(i)] = IBC['C_0'][str(i)]
        rt = time.time()-degin_time
        degin_time = time.time()
        print("Result(",x,"):",res)
        print("Result in", rt ,"s; Global time",script_time,"s;")
        times.append(rt)
        
        vals= [str(x),str(rt)]
        
        for i in range(1,n+1):
            vals.append(str(res[str(i)]))
        
        print(vals)
        vals = '({0})'.format(", ".join(vals))
        
        chunck.append(vals);
        
        #time based CHUNK_SIZE
        active_time = time.time() - script_time 
        if (active_time >= TIMEOUT*0.7):
            CHUNCK_SIZE = max(1, (TIMEOUT*0.9-active_time) / (sum(l) / float(len(l))) * 0.9)
            print("new time based CHUNCK_SIZE:", CHUNCK_SIZE)
        #print("CHUNCK_SIZE:",CHUNCK_SIZE)
        if (len(chunck)>=CHUNCK_SIZE):
            
            if not con or not con.open or not cur:
                con = pymysql.connect(RD.host, RD.user, RD.password , RD.db)
                cur  = con.cursor(pymysql.cursors.DictCursor)
                print("con reopened!")
            fields=['`x`','`t`']
            for i in range(1,n+1):
                fields.append("`C_{0}`".format(i))
            fields = ", ".join(fields)
            req = "INSERT INTO `{0}` ({1}) VALUES {2}; ".format(table_name,fields, (",".join(chunck)))
            print("send_chunck")
            try:
                cur.execute(req)
                con.commit()
                chunck = []
            except Exception as error:
                req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) VALUES (NOW(), '3', '7', 'data', %s, 'calculation', %s)"
                    #print(req)
                cur.execute(req, (data_id,str(error)))
                con.commit()
    if not con or not con.open or not cur:
        con = pymysql.connect(RD.host, RD.user, RD.password , RD.db)
        cur  = con.cursor(pymysql.cursors.DictCursor)
        print("con reopened!")
    if (len(chunck)>0):
        fields=['`x`','`t`']
        for i in range(1,n+1):
            fields.append("`C_{0}`".format(i))
        fields = ", ".join(fields)
        req = "INSERT INTO `{0}` ({1}) VALUES {2}; ".format(table_name,fields,",".join(chunck))
        print("send_tail_chunck")
            
        try:
            cur.execute(req)
            con.commit()
            chunck = []
        except Exception as error:
            req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) VALUES (NOW(), '3', '7', 'data', %s, 'calculation', %s)"
            cur.execute(req, (data_id,str(error)))
            con.commit()
    
    req = "UPDATE `data` SET `version`={0},`state`={1},`time`=NOW() WHERE id={2}".format(VERSION,2,data_id)
    cur.execute(req)
    req = "INSERT INTO `LOG` (`date`, `lvl`, `executor`, `object`, `object_id`, `action`, `arguments`) VALUES (NOW(), '0', '7', 'data', %s, 'calculation', %s)"
    cur.execute(req, (data_id,"complete"))
    con.commit()

    con.close()
    