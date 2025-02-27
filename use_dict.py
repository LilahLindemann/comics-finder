import ast
with open('appearances_dict.txt') as f: 
    data = f.read()
mydata = ast.literal_eval(data)

def find_intersection(chars):
    if len(chars) < 1:
        return set()
    result = mydata[chars[0]]
    for char in chars[1:]:
        result = result & mydata[char]
    return result
