import xml.etree.ElementTree as ET
import os

def problems_parser(problem_id):
    file_name = problem_id+".xml"
    tree = ET.parse(os.path.join("data", "problem", file_name))
    root = tree.getroot()
    problem_name = root.attrib['display_name']

    question = ""
    if root[0].tag == "text":
        for content in root[0].iter():
            if content.tag == "br" and content.tail:
                question += content.tail
            if content.text:
                # print(content.tail)
                question += content.text
        choices = ["no choices"]
        answer = "no answer provided"
    else:
        for p in tree.findall('p'):
            for content in p.iter():
                if content.tag == "br" and content.tail:
                    question += content.tail
                if content.text:
                    #print(content.tail)
                    question += content.text

        # getting the multiple choices, storing them in an array
        choices = []
        answer = ""
        for choice in root.iter('choice'):
            choices.append(choice.text)
            # getting the correct choice
            if choice.attrib['correct'] == "true":
                answer = choice.text

    # the result is an array of 4 elements, problem_name/question/answer are strings, and
    # choices is an array of strings of the choices
    result = [problem_name, question, choices, answer]
    return result


# TESTING THE FUNCTION
# -------------------------------------------------------------------------------
PROBLEM_WEIGHT = {
        "27a9876d7b714ae2b190e085857f4663": 1,
        "d5146af552274e4fb0527e97365b970c": 1,
        "cb4951aacaf648af88111b92d51440a4": 0.8,
        "d8600cf2a37a4f72a0aa4f254ee48455": 1,
        "1af6e55439e44d8dafc21d6e68aed133": 0.8,
        "78dbdda4564a426380a51fd883b816f3": 1,
        "b6b4903ef1b64d57bca60897bf46e1e0": 1,
        "dc8191c3ed124824a3003efd938da298": 1,
        "d3c1c1156dca420789b8bc0c833bf34a": 1,
        "7a80a33c74bf479f9afba6de23f5c5c5": 1,
        "dc8191c3ed124824a3003efd938da298": 0.6,
        "821bc15e0bed4e179ddc1c802b313eec": 0.9,
        "d1dfc14002cc41aab7a6cb31c3b6aa18": 1,
        "6ccd36c6142240b6b1f982930db75622": 0.6,
        "7a80a33c74bf479f9afba6de23f5c5c5": 1,
        "ab45468270db4ef885c3885b4254461b": 0.7,
        "b45eb7410f12464ca3ba317d3fe46090": 0.8,
        "662484c514da42fea6a0a3780cec52f8": 1,
        "c1843fce4a3d42bab62f4a3c73ac6578": 1,
        "5bd7465357c5444494e9fb486556ab0c": 1,
        "b6e3a9b75d8b48a5b6e71847ccf5c757": 0.8,
        "17333909316240a0b59c679ab6c7ede1": 1,
        "8a899a153c85442793502aacb6d8aaac": 1,
        "6a1cd786f82941879009c3c225420ac0": 0.8,
        "46e45e1fc5e24dd2b9e8a93382e97f5b": 1,
        "10304a0ce9e742eebbce0705664f4b7e": 1,
        "d1a830217d7646209bd2fd5f5ca8e3a4": 0.8,
        "e9e80ea651854365a88bdf81624948c6": 1,
        "0eccc6a390844ac9b8d5a92eef410848": 0.4,
        "265841130b8040bda63f205373944857": 0.6,
        "050ab84aae0840c8863053c6bd287f94": 0.8,
        "7d10011449bf4ce7b07df4fbe8422472": 1,
        "8c700934d68b45f590c0b752f30a685a": 0.6,
        "991cc7716ac646c68b27e475b057d4a6": 0.8,
        "09844ac1b2014df880816bd5c77b24d7": 0.8,
        "0585087903c84435a345da01dffe442a": 0.8,
        "cfc225cf7bad433aa98373abfc35d3a5": 0.7,
        "180f93865c8b40d6a06f6dca6d2bf741": 1,
        "2879f5a8c65745bc8e945bb9ee7e798a": 1,
        "6cb2e5deec9541199a8805efaafbaabe": 1,
        "059c362029d64987b822a949b96d7905": 1,
        "67f04dce356846219650e2514958f048": 1,
        "0792a1e4ce5c428eafbb9467566c7a1c": 0.5,
        "b80ac7b29ad74e71bc334c2b3a072315": 1,
        "29ad9230a63f45eea3f5a325b33d2393": 1,
        "050ab84aae0840c8863053c6bd287f94": 0.6,
        "662484c514da42fea6a0a3780cec52f8": 1,
        "4cedbce4d76c4363ab4184cc9e7477ee": 1,
        "5bd7465357c5444494e9fb486556ab0c": 0.8,
        "6f0dbbb84ab84d24b9262c89328063d1": 0.5,
        "7c08c9f8749f4b12800dd952f86fa27e": 1,
        "18fb0ef71659465db38b88dee53d8064": 0.8,
        "42b340fc56784e66a83a9cd390f99fc7": 0.7,
        "a905261536f649598b60a51086917547": 0.6,
        "cf4d14c6564d486e9418a2220540b0d3": 1,
        "df08d62b3c324d9e8dfa345cbb3436c5": 1,
        "5e4d503eb8084cca9f8ebf5397921420": 1,
        "c9fec2c277df4bb89862b4f5f913b910": 0.8,
        "1ba04e4caddd4b9fb32d28248763db9d": 1,
        "6860730d8ab84d3cab8fb0f2351182e2": 1,
        "a1268f53b50c45fe9b7fb62e2d06a989": 1,
        "5e4d503eb8084cca9f8ebf5397921420": 1,
        "6eb17330e2184f538a9791af6de10146": 0.8,
        "368ab6f9eb4e4160a267bbd1f0c80fc2": 0.8,
        "5e4d503eb8084cca9f8ebf5397921420": 0.7,
        "0792a1e4ce5c428eafbb9467566c7a1c": 0.6,
        "050ab84aae0840c8863053c6bd287f94": 0.6,
        "7d10011449bf4ce7b07df4fbe8422472": 0.5,
        "c9fec2c277df4bb89862b4f5f913b910": 0.6,
        "7f03405fb68145bf9ca94c2f6a2b250b": 0.8,
        "f317883654264eb2ba5485e991bdeac3": 1,
        "1ba04e4caddd4b9fb32d28248763db9d": 0.6,
        "3d6a0718c19542b1a9c02ec9a4984a73": 0.3,
        "4b04d93a120140bbba88b690c58445ab": 0.4,
        "6eb17330e2184f538a9791af6de10146": 0.7,
        "6f0dbbb84ab84d24b9262c89328063d1": 0.4,
        "8c700934d68b45f590c0b752f30a685a": 0.6,
        "11e90d73267640b5abc84a88eb921a8d": 0.6,
        "99ea6a3095ef4a999b6d6980291e9952": 1,
        "09844ac1b2014df880816bd5c77b24d7": 0.6,
        "17221fd099574b8691f279fbf53a5cdd": 0.6,
        "25186cfe6ad445f39709d7f5549f381c": 0.7,
        "a1268f53b50c45fe9b7fb62e2d06a989": 0.7,
        "c9afbcc40f794d6cbef24588d08d2680": 0.8,
        "c29c4caceb2a4eccaeecdfe9732767f3": 0.5,
        "f819e50f696a48678cad2fadd4b5f485": 0.6,
        "a7b066155ce5435984635e11f8a666f3": 0.6,
        "6031b3c8f6cd4cf1a04d009273e298db": 0.6,
        "6d6a425cf0da4a268f637fb33572d1a3": 1,
        "752316b1a0e74fca975fb98df6149e7c": 0.6,
        "e8d9667fde24460f98d922631256b04a": 0.8,
}


# the problem_id is passed by a variable type of string
for file in PROBLEM_WEIGHT.keys():
    file_name = file
    print(file_name)
    result = problems_parser(file_name)
    print("-----------------------------------------------")
    print("quiz name: ")
    print(result[0])
    print("------------")
    print("question: ")
    print(result[1])
    print("------------")
    print("multiple choices: ")
    for item in result[2]:
        print(item)
    print("------------")
    print("answer: ")
    print(result[3])

