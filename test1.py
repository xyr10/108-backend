print("Test 1")

# Dictionary

user = {

    "name": "Xyrone",
    "last_name": "Ocampo",
    "age": 42
}


print(user)

print(type(user))

print(user["name"] + "" + user["last_name"])

# INV Homework: String formating in Python
# f string in python


# List
numbers = [1, 2, 3]

# add
numbers.append(4)
numbers.append(5)

print(numbers)

# length
print(len(numbers))
print(len(user["name"]))


####

ages = [32, 74, 20, 69, 52]


def exc1():
    # print all the numbers
    total = 0
    for age in ages:
        # print(age)
        total = total + age

        print(total)


def exc2():
    # print all number greater than 21

    for age in ages:
        if age > 20:
            print(age)


def exc3():
    count = 0
    for age in ages:
        if age >= 21:
            print(age)
            count += 1


def exc4():
    # count how many users are between 30 and 40 years old
    count = 0
    for age in ages:
        if age >= 30 and age <= 40:
            count += 1

    print("There are " + str(count) + " users between 30 and 40")


# call your functions
exc1()
exc2()
exc3()
exc4()
