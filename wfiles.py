xmen_file = open('xmen_base.txt', 'r')
print(xmen_file)

print(xmen_file.read()) ### read from the cursor position. 

print(xmen_file.read(xmen_file.seek(6)))

xmen_file.seek(0) ### comment this to see seek imp. 
for line in xmen_file:
    print(line,end="")


#xmen_file.close()

new_xmen = open('new_xmen.txt', 'w')
new_xmen.write(xmen_file.read())
new_xmen.close()

new_xmen = open(new_xmen.name, 'r+')

print(new_xmen.read())
new_xmen.seek(0)
new_xmen.write("Beast\n")
new_xmen.write("Phoenix\n")

print(new_xmen.read())

new_xmen.close()

with open(xmen_file.name, 'a') as f:
    f.write("\nXavier\n")