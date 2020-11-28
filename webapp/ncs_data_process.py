import pandas as pd
import hashlib

x = pd.read_csv(
    "/Users/nishantjha/Downloads/Social Network Survey NCS (Responses) - Form Responses 1.csv"
)

d = x.to_dict("records")

new_data = []


def encrypt_string(s):
    return hashlib.sha512(str.encode(s)).hexdigest()


for x in d:
    data = {}
    data["Name"] = encrypt_string(x["Please type your FIRST and LAST name:"])
    data["Age"] = x["How old are you?"]
    data["Grade"] = x[
        "Please select your grade/level of education (2019-2020 school year):"
    ]
    data["Gender"] = x["Please select your gender:"]
    friends = x[
        "Please list the FIRST and LAST name of your three closest friends at school from closest to least close:"
    ].split(",")
    data["Friend1"] = encrypt_string(friends[0].strip())
    data["Friend2"] = encrypt_string(friends[0].strip())
    data["Friend3"] = encrypt_string(friends[0].strip())
    data["Influence"] = x[
        "True/False: I think my friends heavily influence my actions."
    ]
    data["Vape"] = x["True/False: I vape (at least once every two weeks)."]
    new_data.append(list(data.values()))


for x in new_data:
    v = [str(c) for c in x]
    print("\t".join(v))
