
import pickle
import sys
import re

model = {}

with open(str(sys.argv[1]), "r+") as file:
    data = file.read()
    with_numerics = ' '.join((data.rstrip().lstrip().replace("\n", " ").replace('\t', "").replace(",", "").replace(":", "").replace(".", "").replace(";", "").replace("'", "").replace("\"", "").replace("-", "").lower()).split())
    output = re.sub(r'\d+', '', with_numerics)
    file.seek(0)
    file.write(output)
    file.truncate()

with open(str(sys.argv[1]), 'r') as f:
    i = 0
    file = f.read().split(" ")
    while i < len(file)-1:
        curr = file[i]
        if curr in model:
            (model[curr]).append(file[i+1])
        else:
            model[curr] = [file[i+1]]
        i += 1

pickle.dump(model, open(str(sys.argv[2]), 'wb'))