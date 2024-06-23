import pandas as pd

def main():
    rows = getRows('GPA Calculator/Gradebook.xlsx', 'Senior Year')
    points = 0.00
    totalcredits = 0
    for row in rows:
        difficulty = row[0]
        credits = row[2]
        totalcredits += credits
        grade = row[3]
        points += (gradepoints(grade) + difficultypoints(difficulty))*credits
    seniorgpa = points/totalcredits
    rows = getRows('GPA Calculator/Gradebook.xlsx', 'Junior Year')
    points = 0.00
    totalcredits = 0
    for row in rows:
        difficulty = row[0]
        credits = row[2]
        totalcredits += credits
        grade = row[3]
        points += (gradepoints(grade) + difficultypoints(difficulty))*credits
    juniorgpa = points/totalcredits
    rows = getRows('GPA Calculator/Gradebook.xlsx', 'Sophomore Year')
    points = 0.00
    totalcredits = 0
    for row in rows:
        difficulty = row[0]
        credits = row[2]
        totalcredits += credits
        grade = row[3]
        points += (gradepoints(grade) + difficultypoints(difficulty))*credits
    sophomoregpa = points/totalcredits
    rows = getRows('GPA Calculator/Gradebook.xlsx', 'Freshmen Year')
    points = 0.00
    totalcredits = 0
    for row in rows:
        difficulty = row[0]
        credits = row[2]
        totalcredits += credits
        grade = row[3]
        points += (inflatedpoints(grade) + difficultypoints(difficulty))*credits
    freshmengpa = points/totalcredits
    print("Freshmen Gpa: " + str(freshmengpa))
    print("Sophomore Gpa: " + str(sophomoregpa))
    print("Junior Gpa: " + str(juniorgpa))
    print("Senior Gpa: " + str(seniorgpa))
    finalgpa = (juniorgpa + sophomoregpa + freshmengpa + seniorgpa)/4.0
    print("Final Gpa: " + str(finalgpa))
    return(finalgpa)



def getRows(excel_file, sheet_name, start_row = 1):
    excel_data = pd.read_excel(excel_file, sheet_name, header=None)
    #print(excel_data)
    size = excel_data.shape
    row_num = size[0]
    datax = []
    for i in range(start_row, row_num):
        data = excel_data.iloc[i].values.tolist()
        datax.append(data)
    return datax

def inflatedpoints(grade):
    point = 0.00
    if(grade == "A+"):
        point = (4.6)
    elif(grade == "A"):
        point = (4.3)
    elif(grade == "A-"):
        point = (4.0)
    elif(grade == "B+"):
        point = (3.6)
    elif(grade == "B"):
        point = (3.3)
    elif(grade == "B-"):
        point = (3.00)
    elif(grade == "C+"):
        point = (2.6)
    elif(grade == "C"):
        point = (2.3)
    elif(grade == "C-"):
        point = (2.00)
    elif(grade == "D"):
        point = (1.6)
    elif(grade == "D-"):
        point = (1.3)
    else:
        point = (0)
    return point

def gradepoints(grade):
    point = 0.00
    if(grade == "A+"):
        point = (4.33)
    elif(grade == "A"):
        point = (4.0)
    elif(grade == "A-"):
        point = (3.67)
    elif(grade == "B+"):
        point = (3.33)
    elif(grade == "B"):
        point = (3.0)
    elif(grade == "B-"):
        point = (2.67)
    elif(grade == "C+"):
        point = (2.33)
    elif(grade == "C"):
        point = (2.0)
    elif(grade == "C-"):
        point = (1.67)
    elif(grade == "D"):
        point = (1.33)
    elif(grade == "D-"):
        point = (1.0)
    else:
        point = (0)
    return point

def difficultypoints(difficulty):
    point = 0.00
    if(difficulty == "AP"):
        point = 2.0
    elif(difficulty == "Honors"):
        point = 1.0
    else:
        point = 0
    return point

main()