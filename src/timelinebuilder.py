class Event:
    def __init__(self, name, year):
        self.name = name
        self.year = year

    def __str__(self):
        return self.name + ": " + str(self.year)


timeline = open("events.csv", "r")

arr = []

for i in timeline:
    vals = i.split(",")
    arr.append(Event(vals[0], int(vals[1])))


arr.sort(key = lambda x: x.year)

i = arr[0].year
j = 0
yearprinted = False

outfile = open("tl.txt", "w")
while i <= arr[-1].year:
    if(j < len(arr) and arr[j].year == i):
        if not yearprinted:
            outfile.write(str(i) + ": ")
            yearprinted = True
        outfile.write(arr[j].name + " ||| ")
        print(str(arr[j]) + " ||| ")
        j+=1
    else:
        outfile.write("\n")
        print(i)
        yearprinted = False
        i+=1
outfile.close()
timeline.close()
