order = 2
pair = (('<START>',), 'a')
context, token = (('<START>',), 'a')
same = True
for ind in range(order-1):
    if context[ind] != pair[0][ind]:
        same *= False
    same*= pair[1]==token
print(same)
if same:
    print("wtf")