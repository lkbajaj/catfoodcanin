from food_cl import CaninKittenWet24Case, CaninKittenDry3lb
import numpy as np
import matplotlib.pyplot as plt
import calendar
from datetime import datetime, date, timedelta

MONTHLY_FOOD_BUDGET = 80.00
SINGLE_BAG_WEIGHT = 1360.5442176870747
START_MONTH = 7
START_DAY = 30
CAT_AGE_MONTHS = 3 # age of the cat when it arrives in months

start_year = datetime.now().year

def bag_feeding_solo(month=START_MONTH,year=start_year,day=START_DAY,budget=MONTHLY_FOOD_BUDGET):
    bag_feeding_schedule = [29,49,49,67,67,68,68,68,59,59,59,51] # amount of food needed in grams
    bag_feeding_schedule = bag_feeding_schedule[CAT_AGE_MONTHS-1:]
  
    months = []
    # build the months array using improved calendar logic
    for grams in bag_feeding_schedule:
        days_in_month = calendar.monthrange(year,month)[1]

        if len(months) == 0:
            feeding_days = days_in_month - day + 1
        else: 
            feeding_days = days_in_month
            
        months.append(np.full(feeding_days,grams))

        # increment month and handle new year rollover
        month += 1
        if month > 12:
            month = 1
            year += 1

    months = np.concatenate(months)

    days = np.arange(1,len(months)+1)

    capacity = np.zeros(len(months))
    kibble_bag = CaninKittenDry3lb()

    available_budget = np.full(len(months),budget-kibble_bag.price)
    bagcount = np.full(len(months),1)

    for i in range(len(months)):
        day = days[i]
        if day % 30 == 0 and (i+1 < len(available_budget)): # every month let us refill our budget
            available_budget[i+1:] += budget

        capacity[i] += kibble_bag.weight 
        daily_food_intake = months[i]
        if (kibble_bag.weight  < daily_food_intake):
            if i+1 > len(months):
                break
            
            if kibble_bag.weight > 0:
                capacity[i+1] = kibble_bag.weight

            kibble_bag = CaninKittenDry3lb() # order and open a new bag
            available_budget[i+1:] -= kibble_bag.price
            bagcount[i+1:] += 1

        kibble_bag.remove_weight(daily_food_intake)

    # I want to get rid of the step behavior and simply plot the indices where I see a change [1,2,3,...,max]
    bagcountmax = np.max(bagcount)
    bagcountmin = np.min(bagcount)

    # make a new array that goes from [bagcountmin, bagcountmin + 1, bagcountmin + 2, ... , bagcountmax]
    # make a new array with same length as the counter that stores the day that corresponds to when the counter goes up
    bagcounter = np.arange(bagcountmin,bagcountmax+1)

    # find the minimum indices at which the number of bags goes up
    bagcounter_days = np.searchsorted(bagcount, bagcounter) + 1

    bagcounter_days = bagcounter_days + 1 # add one to each index to get the day at which this happens
    start_date = date(year, month, day)
    bag_purchase_dates = [start_date + timedelta(days=int(day)-1) for day in bagcounter_days]
    formatted_dates = [d.strftime("%B %-d %Y") for d in bag_purchase_dates]

    for i, (day,label) in enumerate(zip(bagcounter_days, formatted_dates)):
        if i > 0:
            print(f'Bag #{i+1:<2}:  Day {day:<3}, {label}')

    plt.plot(days, capacity/SINGLE_BAG_WEIGHT,c='b')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('capacity')
    plt.title('food capacity')
    plt.show()

    plt.plot(bagcounter_days, bagcounter, c='b',marker='o')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('# bags')
    plt.title('bags of food used')
    plt.show()


    plt.plot(days,available_budget,c='b')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('money available')
    plt.title('positive cashflow')
    plt.show()
    plt.close('all')

    # print(capacity/SINGLE_BAG_WEIGHT)
    # print(bagcount)
    # print(available_budget)


def can_feeding_solo(month=START_MONTH,year=2025,day=START_DAY,budget=MONTHLY_FOOD_BUDGET):
    # from "feeding instructions under chewy.com" 4 months +
    # https://www.chewy.com/royal-canin-feline-health-nutrition/dp/33914?utm_source=google-product&utm_medium=cpc&utm_campaign=22387212139&utm_content=&gad_source=1&gad_campaignid=22387216051&gbraid=0AAAAADmQ2V39quEK8DwxjJtLTYy3nE3II&gclid=Cj0KCQjw097CBhDIARIsAJ3-nxeT67wxaXcmicMlUJGliY2RnlQzrE2oh6tNhCKliAoR3JYLr3Xh6VgaAiL1EALw_wcB
    can_feeding_schedule = [4,4.25,4.25,4.25,4,4,4,4] 
    orig_month = month
    orig_day = day
    orig_year = year

    months = []
    # build the months array using improved calendar logic
    for cans in can_feeding_schedule:
        days_in_month = calendar.monthrange(year,month)[1]

        if len(months) == 0:
            feeding_days = days_in_month - day + 1
        else: 
            feeding_days = days_in_month
            
        months.append(np.full(feeding_days,cans))

        # increment month and handle new year rollover
        month += 1
        if month > 12:
            month = 1
            year += 1
    
    months = np.concatenate(months)
    days = np.arange(1,len(months)+1)

    capacity = np.zeros(len(months))
    can_case = CaninKittenWet24Case()

    available_budget = np.full(len(months),budget-can_case.price)
    cancount = np.full(len(months),1)


    for i in range(len(months)):
        day = days[i]
        if day % 30 == 0 and (i+1 < len(available_budget)): # every month let us refill our budget
            available_budget[i+1:] += budget

        capacity[i] += can_case.weight 
        daily_food_intake = months[i]
        if (can_case.weight < daily_food_intake):
            if i+1 > len(months):
                break
            
            if can_case.weight > 0:
                capacity[i+1] = can_case.weight

            can_case = CaninKittenWet24Case() # order and open a new bag
            available_budget[i+1:] -= can_case.price
            cancount[i+1:] += 1

        can_case.remove_weight(daily_food_intake)
    
    # I want to get rid of the step behavior and simply plot the indices where I see a change [1,2,3,...,max]
    cancountmax = np.max(cancount)
    cancountmin = np.min(cancount)

    # make a new array that goes from [bagcountmin, bagcountmin + 1, bagcountmin + 2, ... , bagcountmax]
    # make a new array with same length as the counter that stores the day that corresponds to when the counter goes up
    cancounter = np.arange(cancountmin,cancountmax+1)

    # find the minimum indices at which the number of bags goes up
    cancounter_days = np.searchsorted(cancount, cancounter) + 1

    cancounter_days = cancounter_days + 1 # add one to each index to get the day at which this happens
    start_date = date(orig_year, orig_month, orig_day)
    bag_purchase_dates = [start_date + timedelta(days=int(day)-1) for day in cancounter_days]
    formatted_dates = [d.strftime("%B %-d %Y") for d in bag_purchase_dates]

    for i, (day,label) in enumerate(zip(cancounter_days, formatted_dates)):
        if i > 0:
            print(f'Case #{i+1:<2}:  Day {day:<3}, {label}')

    plt.plot(days, capacity/24,c='b')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('capacity')
    plt.title('food capacity')
    plt.show()

    plt.plot(cancounter_days, cancounter, c='b',marker='o')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('# cans')
    plt.title('cans of food used')
    plt.show()


    plt.plot(days,available_budget,c='b')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('money available')
    plt.title('positive cashflow')
    plt.show()
    plt.close('all')

def combo_feeding(month=START_MONTH,year=2025,day=START_DAY,budget=MONTHLY_FOOD_BUDGET):
    # from "feeding instructions under chewy.com" 4 months +
    # https://www.chewy.com/royal-canin-feline-health-nutrition/dp/33914?utm_source=google-product&utm_medium=cpc&utm_campaign=22387212139&utm_content=&gad_source=1&gad_campaignid=22387216051&gbraid=0AAAAADmQ2V39quEK8DwxjJtLTYy3nE3II&gclid=Cj0KCQjw097CBhDIARIsAJ3-nxeT67wxaXcmicMlUJGliY2RnlQzrE2oh6tNhCKliAoR3JYLr3Xh6VgaAiL1EALw_wcB
    if isinstance(budget, (int,float)):
        monthly_budgets = np.full(10,float(budget))
    elif isinstance(budget, (list,np.ndarray)):
        monthly_budgets = np.array(budget,dtype=float)
        if monthly_budgets.shape[0] != 10:
            raise ValueError("Budget array must have exactly 10 monthly values")
    else:
        raise TypeError('Budget must be a int,float, or list/NumPy array of length 10')
    
    can_feeding_schedule = np.full(10,1) 
    bag_feeding_schedule = [27,45,45,46,46,46,37,37,37,30] # amount of food needed in grams
    
    orig_month = month
    orig_day = day
    orig_year = year

    months_cans = []
    months_bags = []
  
    # build the months array using improved calendar logic
    for i in range(len(can_feeding_schedule)):
        days_in_month = calendar.monthrange(year,month)[1]

        if len(months_cans) == 0:
            feeding_days = days_in_month - day + 1
        else: 
            feeding_days = days_in_month
            
        months_cans.append(np.full(feeding_days,can_feeding_schedule[i]))
        months_bags.append(np.full(feeding_days,bag_feeding_schedule[i]))
            
        # increment month and handle new year rollover
        month += 1
        if month > 12:
            month = 1
            year += 1
    
    months_cans = np.concatenate(months_cans)
    months_bags = np.concatenate(months_bags)

    days = np.arange(1,len(months_cans)+1)

    capacity_cans = np.zeros(len(months_cans))
    capacity_bags = np.zeros(len(months_bags))

    can_case = CaninKittenWet24Case()
    kibble_bag = CaninKittenDry3lb()

    # initialize budget by taking the monthly start and subtract the price of a case and a bag
    available_budget = np.full(len(months_cans),monthly_budgets[0]-can_case.price-kibble_bag.price)

    casecount = np.full(len(months_cans),1)
    bagcount = np.full(len(months_bags),1)

    current_date = date(orig_year, orig_month, orig_day)
    month_index = 0


    for i in range(len(months_cans)):
        if current_date.day == 1 and i + 1 < len(available_budget) and month_index < len(monthly_budgets): 
            available_budget[i+1:] += monthly_budgets[month_index]
            month_index += 1

        capacity_cans[i] += can_case.weight 
        capacity_bags[i] += kibble_bag.weight
        daily_can_intake = months_cans[i]
        daily_kibble_intake = months_bags[i]

        if (can_case.weight < daily_can_intake):
            if i+1 > len(months_cans): 
                break
            
            if can_case.weight > 0:
                capacity_cans[i+1] = can_case.weight

            can_case = CaninKittenWet24Case() # order and open a new case
            available_budget[i+1:] -= can_case.price
            casecount[i+1:] += 1
        
        if (kibble_bag.weight < daily_kibble_intake):
            if i+1 > len(months_cans):
                break
            
            if can_case.weight > 0:
                capacity_bags[i+1] = kibble_bag.weight

            kibble_bag = CaninKittenDry3lb() # order and open a new bag
            available_budget[i+1:] -= kibble_bag.price
            bagcount[i+1:] += 1

        can_case.remove_weight(daily_can_intake)
        kibble_bag.remove_weight(daily_kibble_intake)

        current_date += timedelta(days=1)

    
    # I want to get rid of the step behavior and simply plot the indices where I see a change [1,2,3,...,max]
    cancountmax = np.max(casecount)
    cancountmin = np.min(casecount)

    bagcountmax = np.max(bagcount)
    bagcountmin = np.min(bagcount)
    
    # make a new array that goes from [bagcountmin, bagcountmin + 1, bagcountmin + 2, ... , bagcountmax]
    # make a new array with same length as the counter that stores the day that corresponds to when the counter goes up
    cancounter = np.arange(cancountmin,cancountmax+1)
    bagcounter = np.arange(bagcountmin,bagcountmax+1)

    # find the minimum indices at which the number of bags goes up
    cancounter_days = np.searchsorted(casecount, cancounter) + 1
    bagcounter_days = np.searchsorted(bagcount, bagcounter) + 1

    cancounter_days = cancounter_days + 1 # add one to each index to get the day at which this happens
    bagcounter_days = bagcounter_days + 1 # add one to each index to get the day at which this happens

    combined_events = [("case", day) for day in cancounter_days] + \
                      [("bag", day) for day in bagcounter_days]

    combined_events.sort(key=lambda x: x[1])
    
    case_num = 1
    bag_num = 1

    for item_type, day in combined_events:
        event_date = date(orig_year, orig_month, orig_day) + timedelta(days=int(day)-1)
        formatted_date = event_date.strftime('%B %-d %Y')

        if item_type == 'case':
            case_num += 1
            if case_num > 2:
                print(f'Case #{case_num-2}: Day {day}, {formatted_date}')
        else:
            bag_num += 1
            if bag_num > 2:
                print(f'Bag #{bag_num-2}: Day {day}, {formatted_date}')
    
    plt.plot(days, capacity_cans/24,label='cans')
    plt.plot(days, capacity_bags/SINGLE_BAG_WEIGHT, label='bags')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('capacity')
    plt.title('food capacity')
    plt.legend()
    plt.show()

    plt.plot(cancounter_days,cancounter,marker='o', label='cans')
    plt.plot(bagcounter_days,bagcounter,marker='o', label='bags')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('# cans')
    plt.title('cans of food used')
    plt.legend()
    plt.show()


    plt.plot(days,available_budget,c='b')
    plt.grid()
    plt.xlabel('day')
    plt.ylabel('money available')
    plt.title('positive cashflow')
    plt.show()
    plt.close('all')

available_budget = np.asarray([120,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0])
combo_feeding(month=8,day=30,year=2025,budget=available_budget)