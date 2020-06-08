import copy

potentialNodes = {}


def BFStar_Knapsack(money, prices, values, stockTruths, size, depth, summedPrice, trueUpperBound):
    if depth < size:
        nodes = []
        updateNodeList = False
        stockTruthsNegate = copy.deepcopy(stockTruths)
        #choosing to not include the next item
        stockTruthsNegate[depth] = 0
        nodes.append(getCost(money, prices, values, stockTruthsNegate, size))
        nodes[0].append(summedPrice)
        nodes[0].append(stockTruthsNegate)
        #test to see if next item being added is feasible, do not need to do this with negated choice
        if summedPrice + prices[depth] <= money:
            nodes.append(getCost(money, prices, values, stockTruths, size))
            nodes[1].append(summedPrice + prices[depth])
            nodes[1].append(stockTruths)
       
        for i in range(len(nodes)):
            #if cost is less than or equal to true upper bound,
            #add node to potential node dictionary
            if nodes[i][0] <= trueUpperBound:
                #do this because multiple nodes could have the same cost
                if nodes[i][0] in potentialNodes.keys():
                    potentialNodes[nodes[i][0]].append([nodes[i][1], nodes[i][3], depth+1, nodes[i][2]])
                else:
                    potentialNodes[nodes[i][0]] = [[nodes[i][1], nodes[i][3], depth+1, nodes[i][2]]]
            if nodes[i][1] < trueUpperBound:
                trueUpperBound = nodes[i][1]

    return trueUpperBound

#at every node, if cost is greater than current upper bound, kill that node
def getCost(money, prices, values, stockTruths, size):
    m = money
    cost = 0
    upperBound = 0
    costUpdated = False
    for i in range(size):
        if stockTruths[i] == 1:
            if prices[i] <= m:
                upperBound += values[i]
                m -= prices[i]
            else:
                costUpdated = True
                cost = upperBound + (values[i]/prices[i]) * m
                m = 0
                break
    if costUpdated == False:
        cost = upperBound
    cost = -cost
    upperBound = -upperBound

    return [cost, upperBound]

def updatePotentialNodes():
    keysToDel = []
    for node in potentialNodes:
        if node > trueUpperBound:
            keysToDel.append(node)
    for key in keysToDel:
        del potentialNodes[key]


#driver code
stocks = {'AAPL': (25, 5), 'MSFT': (40, 7), 'SHOP': (20, 5), 'DAL': (34, 9), 'HTZ': (7, 3)}
stocks = ['AAPL', 'MSFT', 'SHOP', 'DAL', 'UAL', 'ETSY']
values = [10, 10, 12, 18]
prices = [2, 4, 6, 9]
size = len(values)
stockTruths = [1] * size
money = 15
depth = 1
trueUpperBound = 0

#get base cost and upperbound for root node before any branching
c, u = getCost(money, prices, values, stockTruths, size)
trueUpperBound = u
#each node will contain the upperBound, which stocks are included for cost and upper bound calculations,
# the depth, and cost of the stocks included up to that point
potentialNodes[c] = [[u, stockTruths, 0, 0]]

#if there are nodes that should still be looked at
while potentialNodes:
    #this is a lowest cost branch and bound method
    leastCost = min(potentialNodes.keys())
    node = potentialNodes[leastCost].pop(0)
    if len(potentialNodes[leastCost]) == 0:
        del potentialNodes[leastCost]
    
    newBound = BFStar_Knapsack(money, prices, values, node[1], size, node[2], node[3], trueUpperBound)

    if newBound != trueUpperBound:
        trueUpperBound = newBound
        updatePotentialNodes()

pickedStocks = []
totalValue = 0
totalCost = 0
for i in range(node[2]):
    if node[1][i] == 1:
        pickedStocks.append(stocks[i])
        totalValue += values[i]
        totalCost += prices[i]

stringStocks = ', '.join(pickedStocks)
print("The stocks picked to buy are: " + stringStocks)
print("The combined value for the picked stocks is: " + str(totalValue))
print("The total cost for the picked stocks is: " + str(totalCost))
print("The remaining amount of purchasing power in the account is: " + str(money - totalCost))


