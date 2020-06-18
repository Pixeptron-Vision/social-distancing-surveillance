def writeToCSV(filename, data):    
    import csv  
    file = open(str(filename)+'.csv', 'w+', newline ='') 
    
    fields = ['Camera IP', 'Camera Tag']
    with file:     
        write = csv.writer(file)
        write.writerow(fields) 
        write.writerows(data)

def readFromCSV(filename):
    import csv
    sources = []

    with open(str(filename)+'.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            sources.append(row)
    
    return sources

'''
data =  [['../Dataset/PNNLParkingLot2.avi','t1'],
                ['../Dataset/PNNL_Parking_LOT(1).avi','t2'],
                ['../Dataset/PNNLParkingLot2.avi','t3'],
                ['../Dataset/walking.avi',''],
                ['../Dataset/PNNL_Parking_LOT(1).avi',''],
                ['../Dataset/PNNLParkingLot2.avi','']]

filename = 'CameraIPData'
writeToCSV(filename, data)

sources = readFromCSV(filename)
print(sources)

if data == sources:
    print("True")
'''