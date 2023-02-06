import csv

with open('toronto-neighbourhoods-2020-1-OnlyWeekdays-MonthlyAggregate.csv', 'r') as inp, open('reduced-toronto-neighbourhoods-2020-1-OnlyWeekdays-MonthlyAggregate.csv', 'w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        try:
            if int(row[0]) == int(row[1]):
                continue
            if int(row[3]) > 300:
                continue
            if int(row[2]) == 1:
            #if int(row[0]) < 20 and int(row[1]) < 20:
                writer.writerow(row)
        except:
            writer.writerow(row)