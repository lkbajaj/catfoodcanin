from food_cl import CaninKittenWet3oz, CaninKittenDry3lb
import numpy as np
import matplotlib.pyplot as plt

MONTHLY_FOOD_BUDGET = 50.00
SINGLE_BAG_WEIGHT = 1360.5442176870747

month1 = np.full(30,29)
month2 = np.full(30,49)
month3 = np.full(30,49)
month4 = np.full(30,67)
month5 = np.full(30,67)
months = np.concatenate((month1,month2,month3,month4,month5))

month6 = np.full(30,68)
month7 = np.full(30,68)
month8 = np.full(30,68)
month9 = np.full(30,59)
month10 = np.full(30,59)
month11 = np.full(30,59)
month12 = np.full(30,51)
months = np.concatenate((months,month6,month7,month8,month9,month10,month11,month12))

days = np.arange(1,len(months)+1)

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

plt.plot(days, capacity/SINGLE_BAG_WEIGHT,c='b')
plt.grid()
plt.xlabel('day')
plt.ylabel('capacity')
plt.title('food capacity')
plt.show()

plt.plot(days, bagcount, c='b')
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

print(capacity/SINGLE_BAG_WEIGHT)
print(bagcount)
print(available_budget)

