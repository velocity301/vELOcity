import json
def writeJson(newData, fileName):
    with open(fileName,'r+') as f:
        fileData = json.load(f)
        print(fileData)
        fileData.append(newData.__dict__)
        f.seek(0)
        json.dump(fileData, f)

def checkJson(checkData, categoryOfData, fileName):
    with open(fileName, 'r+') as f:
        fileData = json.load(f)
        print(fileData)
        for elem in fileData:
            print(elem.get(categoryOfData))
            if (checkData == elem.get(categoryOfData)):
                return True
        return False

print(checkJson("Alkminion", "username", "players.json"))