import csv
import scrython
UPLOAD_FOLDER = 'T:/Python_Practice/Dragon Lookup/uploads'
###
ifile  = open(UPLOAD_FOLDER + "/case_inventory.csv", "rt", encoding="utf8")
read = csv.reader(ifile)
next(read, None)
size = read.line_num
for row in read:
    row = str(row)
    row = row[2:size - 3]
    print (row)

    scryCard = scrython.cards.Named(fuzzy=row)
    print(scryCard.name())
    print(scryCard.image_uris(0, "small"))
    print(scryCard.mana_cost())