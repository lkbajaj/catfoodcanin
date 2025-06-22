from food_cl import CaninKittenWet3oz, CaninKittenDry3lb
import numpy as np
import matplotlib.pyplot as plt
import calendar
from datetime import datetime, date, timedelta

MONTHLY_FOOD_BUDGET = 50.00
SINGLE_BAG_WEIGHT = 1360.5442176870747
START_MONTH = 7
START_DAY = 30
CAT_AGE_MONTHS = 3 # age of the cat when it arrives in months

bag_feeding_schedule = [29,49,49,67,67,68,68,68,59,59,59,51] # amount of food needed in grams
bag_feeding_schedule = bag_feeding_schedule[CAT_AGE_MONTHS-1:]
start_year = datetime.now().year

months = []
month = START_MONTH
year = start_year
day = START_DAY

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
print(len(days))

capacity = np.zeros(len(months))
kibble_bag = CaninKittenDry3lb()

available_budget = np.full(len(months),MONTHLY_FOOD_BUDGET-kibble_bag.price)
bagcount = np.full(len(months),1)

for i in range(len(months)):
    day = days[i]
    if day % 30 == 0 and (i+1 < len(available_budget)): # every month let us refill our budget
        available_budget[i+1:] += MONTHLY_FOOD_BUDGET

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
start_date = date(start_year, START_MONTH, START_DAY)
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

print(capacity/SINGLE_BAG_WEIGHT)
print(bagcount)
print(available_budget)

