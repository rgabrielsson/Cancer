def get_data():
    infile = open("cancerTrainingData.txt","r")
    for i in range(32):
        infile.readline()

    mal = [0]*10
    ben = [0]*10
    mal_count = 0
    ben_count = 0
    for line in infile:
        line = line.strip()
        line = line.split(",")
        line.pop()                  #get rid of ID
        #add means to appropriate list
        if line[-1] == "M":
            mal_count += 1
            for i in range(10):
                mal[i] += float(line[i])
        else:
            ben_count += 1
            for i in range(10):
                ben[i] += float(line[i])

    infile.close()

    for i in range(len(mal)):
        mal[i] = mal[i]/mal_count
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
        
            
def main(file):
    mal, ben = get_data()

    infile = open(file,"r")
    for i in range(32):
        infile.readline()

    num_correct = 0
    num_wrong = 0
    for line in infile:
        line = line.strip()
        line = line.split(",")
        data = line[1:11]
        for i in range(len(data)):
            data[i] = float(data[i])
        answer = line[-1]
        prediction = predict_tumor(mal,ben,data)
        if answer == prediction:
            num_correct += 1
        else:
            num_wrong += 1
    print(f"Correct: {num_correct}")
    print(f"Incorrect: {num_wrong}")

main("cancerTestingData.txt")