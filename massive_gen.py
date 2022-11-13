from PROcalc import FC_dynam as FC_gen
for i in range(1, 13):
    FC_gen.generate(i, "fc_exp{0}".format(i))
