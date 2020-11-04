
from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_HALF_EVEN, InvalidOperation

def round_number(number, decimal_num=None, direction=None):
    number = Decimal("{:.6f}".format(float(number)))
    getcontext().prec = 20
    decimal_place = '1.'
    if decimal_num == None:
        decimal_num = 2
    while decimal_num > 0:
        decimal_place += '0'
        decimal_num -= 1

    value = 0
    try:
        if direction == 'up':
            value = Decimal(number).quantize(Decimal(decimal_place), rounding=ROUND_HALF_UP)
        elif direction == 'even':
            value = Decimal(number).quantize(Decimal(decimal_place), rounding=ROUND_HALF_EVEN)
        elif direction == 'down':
            value = Decimal(number).quantize(Decimal(decimal_place), rounding=ROUND_HALF_DOWN)
        else:
            value = Decimal(number).quantize(Decimal(decimal_place), rounding=ROUND_HALF_UP)
    except InvalidOperation as e:
        value = Decimal(number).quantize(Decimal('1.00'), rounding=ROUND_HALF_UP)
    return value