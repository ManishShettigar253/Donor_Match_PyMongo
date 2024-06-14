from pymongo import MongoClient

# Database connection
client = MongoClient('localhost', 27017)
db = client['bdc']
collection = db['bloodCheck']

# Blood group compatibility map
compatibility_map = {
    1: {1, 2, 7, 8},
    2: {2, 8},
    3: {3, 4, 7, 8},
    4: {4, 7},
    5: {1, 2, 3, 4, 5, 6, 7, 8},
    6: {2, 4, 6, 8},
    7: {7, 8},
    8: {8}
}

def check(dage, dweight, rgroup, dgroup):
    return dage > 18 and dweight > 45 and dgroup in compatibility_map.get(rgroup, set())

bgcode = {1: "A+", 2: "A-", 3: "B+", 4: "B-", 5: "AB+", 6: "AB-", 7: "O+", 8: "O-"}

repeat = True
while repeat:
    print("BLOOD GROUP CODES: ", bgcode)
    
    try:
        rgroup = int(input("Enter Recipient's Blood Group Code: "))
        dage = int(input("Enter Donor's Age: "))
        dweight = int(input("Enter Donor's Weight: "))
        dgroup = int(input("Enter Donor's Blood Group Code: "))
        
        if rgroup not in bgcode or dgroup not in bgcode:
            print("Invalid blood group code. Please try again.")
            continue

        can_donate = check(dage, dweight, rgroup, dgroup)
        result = "Can Donate" if can_donate else "Cannot Donate"
        
        # Inserting data into MongoDB
        document = {
            "recipient": bgcode[rgroup],
            "rage": dage,
            "rweight": dweight,
            "donator": bgcode[dgroup],
            "result": result
        }
        collection.insert_one(document)
        
        print(f"Blood {result.lower()}.")
        
        try_again = input("Do you want to try again? (yes/no): ").strip().lower()
        if try_again != 'yes':
            print("Thank You!!!")
            repeat = False
        
    except ValueError:
        print("Invalid input. Please enter numeric values for age, weight, and blood group codes.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
