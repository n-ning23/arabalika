def erCalc(burst,desc="",onSame=0,offSame=0,onDiff=0,offDiff=0,onNone=0,offNone=0,fixed=0):
    total_energy = 3*onSame + 1.8*offSame + onDiff + 0.6*offDiff + 2*onNone + 1.2*offNone
    temp = burst-fixed-total_energy
    if (total_energy < 0.1*temp):
        raise Exception("Not enough energy to satisfy ER needs.")
    if (total_energy == 0):
        raise Exception("Total energy generated in a rotation is 0.")
    if (temp/total_energy < -1):
        temp = -total_energy
    return desc,1.0+temp/total_energy
