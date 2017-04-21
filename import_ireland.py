a=[]
p=[]
s=[]
k=[]
fg=[]
n=[]
import csv
with open('ireland_input.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        a.append(row)

with open('ireland_popdens.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        p.append(row)


with open('ireland_seg.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        s.append(row)

with open('ireland_cap_1.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        k.append(row)

with open('flood_gev.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        fg.append(row)

with open('ainmneacha.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        n.append(row)


vsl = 9.444821238556;
mu = 0.01;
rho = 0.518144214230081;
