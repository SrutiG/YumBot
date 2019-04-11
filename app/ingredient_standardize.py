'''

'''

def calculate_standard_ingredient_amount(amount, unit, ingredient_name):
    '''
    Convert all weights to grams
    :param amount:
    :param unit:
    :param ingredient_name:
    :return:
    '''
    valid_units = {
        'tbsp': 12.7817,
        'g': 1,
        'gram': 1,
        'cup': 128
    }
    unit = unit.lower()

    return 1