import itertools

def initial_print_statement():
    print("Welcome to Resistance Calculator!")
    print("This program will take as input the resistances you have on hand,")
    print("as well as a desired value, and determine the possible combinations to achieve that value.\n")
    print("Begin by inputting all resistances you have on hand.")
    print("You can either type the exact value of the resistor (e.g. 20000),")
    print("or a comma separated list of the colors (e.g. red,black,brown); ignore the threshold band (e.g. gold).")
    print("When you're finished inputting all resistances, please type in 'end'.\n")

def resistance_input():
    resistor_count = 1;
    overall_list = list()
    while True :
        user_input = input("Resistance %i: " % resistor_count)
        resistor_count += 1
        if str(user_input).lower() == "end":
            break
        if "," in str(user_input):
            # Assume user typed in colours
            colors = str(user_input).split(",")
            value = 0
            if len(colors) == 3:
                # 4-Band resistor
                # TODO: ADD VALIDATION
                value += (digit_dict.get(colors[0])*10 + digit_dict.get(colors[1]))*multiplier_dict.get(colors[2])
                overall_list.append(int(value))
                print("Added %i Ohm resistance!\n" % value)
            elif len(colors) == 4:
                # 5-Band resistor
                value += (digit_dict.get(colors[0]) * 100 + digit_dict.get(colors[1]) * 10 + digit_dict.get(colors[2])) * multiplier_dict.get(colors[3])
                overall_list.append(int(value))
                print("Added %i Ohm resistance!\n" % value)
            else:
                print("Invalid number of colors - please try again!")
                continue
        else:
            overall_list.append(int(user_input))
            print("Added %s Ohm resistance!\n" % user_input)
    return overall_list

def desired_value_input():
    value = input("\nGreat! Now please enter the resistance value you wish to create: ")
    return float(value)

def compute_possibilities(desired_val, resist_list):
    print("Computing possible parallel resistance combinations...")
    result_list = list()
    # First check all double-parallel combinations
    possible_double_combinations = list(itertools.combinations(resist_list, 2))
    for combination in possible_double_combinations:
        value = compute_parallel(combination)
        # If they're approx. equal add to the list
        if approximately_equal(desired_val, value, 5):
            result_list.append(combination)
        # Otherwise try adding a resistor in series if the value was too small
        elif value < desired_val:
            for resist in resist_list:
                if approximately_equal(desired_val, (value + resist), 5):
                    result_list.append([combination, resist])
    # Next, check all triple-parallel combinations
    possible_combinations = list(itertools.combinations(resist_list, 3))
    for combination in possible_combinations:
        value = compute_parallel(combination)
        # If they're approx. equal add to the list
        if approximately_equal(desired_val, value, 5):
            result_list.append(combination)
        # Otherwise try adding a resistor in series if the value was too small
        elif value < desired_val:
            for resist in resist_list:
                if approximately_equal(desired_val, (value + resist), 5):
                    result_list.append([combination, resist])
                    # Last, check all quad-parallel combinations
    possible_combinations = list(itertools.combinations(resist_list, 4))
    for combination in possible_combinations:
        value = compute_parallel(combination)
        # If they're approx. equal add to the list
        if approximately_equal(desired_val, value, 5):
            result_list.append(combination)
        # Otherwise try adding a resistor in series if the value was too small
        elif value < desired_val:
            for resist in resist_list:
                if approximately_equal(desired_val, (value + resist), 5):
                    result_list.append([combination, resist])
    return result_list

def approximately_equal(desired, actual, threshold):
    if desired == actual:
        return True
    if abs((desired-actual)/((desired+actual)/2.))*100 <= threshold:
        return True
    return False

def compute_parallel(input_list):
    resistance_sum = 0
    for item in input_list:
        resistance_sum += 1. / item
    return 1. / resistance_sum


digit_dict = dict(black=0,brown=1,red=2,orange=3,yellow=4,
                 green=5,blue=6,violet=7,grey=8,white=9)
multiplier_dict = dict(black=10**0,brown=10**1,red=10**2,orange=10**3,
                      yellow=10**4,green=10**5,blue=10**6,violet=10**7,
                      grey=10**8,white=10**9)

initial_print_statement()
resistor_list = resistance_input()
resistor_list.sort()
user_input = desired_value_input()
final_list = compute_possibilities(user_input, resistor_list)
if len(final_list) > 0:
    print("Possible parallel/series resistance combinations (parallel are surrounded in brackets): ")
    for element in final_list:
        print(element)
else:
    print("No possible simple combinations found.")