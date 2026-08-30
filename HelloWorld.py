##name = input('Enter your name: ')
#age = input('Enter your age: ')

#print(f'Hello, {name}! You are {age} years old.')
def minimumLoss(price):
    min_loss = float('inf')

    for i in range(len(price)):
        for j in range(i + 1, len(price)):
            if price[i] > price[j]:
                min_loss = min(min_loss, price[i] - price[j])

    return min_loss


n = int(input())
price = list(map(int, input().split()))

print(minimumLoss(price))