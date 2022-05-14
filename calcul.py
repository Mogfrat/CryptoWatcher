import math


def nxtPayoutPol(tUnpaid, ethPerMin):
    global unpaid
    unpaid = tUnpaid/1000000000000000000
    global ethPerDay
    ethPerDay = (ethPerMin*60)*24
    global remainToTreshold
    remainToTreshold = 0.005 - unpaid
    NxtPayout = remainToTreshold/ethPerDay
    return NxtPayout

def nxtPayout(tUnpaid, ethPerMin, payout):
    global unpaid
    unpaid = tUnpaid/1000000000000000000
    payout =  payout/1000000000000000000

    global ethPerDay
    ethPerDay = (ethPerMin*60)*24
    global remainToTreshold
    remainToTreshold = payout - unpaid
    NxtPayout = remainToTreshold/ethPerDay
    return NxtPayout


def nxtPayout_min():
    return(remainToTreshold/ethPerDay)*25


def ceil(a):
    return math.ceil(a)

def floor(a):
    return math.floor(a)

def unpaid():
    return unpaid