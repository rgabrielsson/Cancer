def get_tumor_info(line):
    data = [0]*10
    line = line.strip()
    line = line.split(",")
    tumorID = line[0]
    line.pop(0)                  #get rid of ID
    for i in range(10):
        data[i] += float(line[i])
    status = line[-1]
    if status != "B" and status != "M":
        status = None
    return tumorID, data, status

def train():
    infile = open("cancerTrainingData.txt","r")
    for i in range(32):
        infile.readline()
    mal = [0]*10
    ben = [0]*10
    mal_count = 0
    ben_count = 0
    for line in infile: 
        tumorID, data, status = get_tumor_info(line)
        #add means to appropriate list
        if status == "M":
            mal_count += 1
            for i in range(10):
                mal[i] += float(data[i])
        elif status == "B":
            ben_count += 1
            for i in range(10):
                ben[i] += float(data[i])
    infile.close()

    for i in range(len(mal)):
        mal[i] = mal[i] / mal_count
    for i in range(len(ben)):
        ben[i] = ben[i]/ben_count

    return mal, ben

def predict_tumor(mal,ben,data):
    mal_points = 0
    ben_points = 0
    for i in range(len(data)):
        #default add points to mal, since its worse
        if abs(data[i] - mal[i]) <= abs(data[i] - ben[i]):
            mal_points += 1
        else:
            ben_points += 1
    if mal_points >= ben_points:
        guess = "M"
    else:
        guess = "B"
    return guess


def test(mal, ben, file):
    infile = open(file,"r")
    for i in range(32):
        infile.readline()
    num_correct = 0
    num_wrong = 0
    for line in infile:
        tumorID, data, status = get_tumor_info(line)
        prediction = predict_tumor(mal,ben,data)
        if status == prediction:
            num_correct += 1
        else:
            num_wrong += 1
    percentage = (num_correct)/(num_correct+num_wrong)*100
    print(f"Accurary: {percentage:.2f}%")

def classify(mal, ben, fname):
    infile = open(fname, "r")
    for i in range(32):
        infile.readline()
        
    outfile = open("Predictions.csv", "w")
    
    for line in infile:
        tumorID, data, status = get_tumor_info(line)
        status = predict_tumor(mal, ben, data)
        print(tumorID,status,file = outfile)
    

def main():
    mal, ben = train()
    test(mal, ben, "cancerTestingData.txt")
    classify(mal, ben, "unknowns.txt")


main()