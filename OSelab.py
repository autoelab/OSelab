import os, json, ctypes, base64, requests
ctypes.windll.kernel32.SetConsoleTitleW('OSelab')
answers = requests.get('https://api.myjson.com/bins/KEY').json()

session = requests.Session()
api = 'https://care.srmist.edu.in/srmos/api/'
data = {"username": input('Username: '), "password": input('Password: ')}
headers = {'User-Agent': 'Chrome/76.0.3809.132', 'Content-Type': 'application/json'}
login = session.post(api+'auth/login', data=json.dumps(data), headers=headers).json()['response']
headers.update({'role': 'S', 'token': login['token'], 'username': login['username']})
print('\n')

def evaluate(code):
    lang = 'CPP' if '<iostream>' in code else 'C'
    data = {"courseName": "OPERATING-SYSTEMS", "code": code, "language": lang, "sid": questioncode, "qid": question['_id']}
    result = session.post(api+'student/question/evaluate', data=json.dumps(data), headers=headers)
    status = True if result.json()['response']['score'] == 100 else False
    if status: 
        try:
            report = session.post(api+'shared/wkhtml', data=json.dumps(data), headers=headers).json()['response']
            if not os.path.isdir('Reports'): 
                os.mkdir('Reports')
            open('Reports\\'+str(count).rjust(2,'0')+'.jpg', 'wb').write(base64.b64decode(report))
        except: pass
    return(status)

count = 0
for sno in range(11, 21):
    for qno in range(11, 21):
        count+= 1
        questioncode = '15'+str(sno)+'1'+str(qno)
        data = {"courseName": "OPERATING-SYSTEMS", "questionID": questioncode}
        question = session.post(api+'student/question', data=json.dumps(data), headers=headers).json()['response']
        print(str(count).rjust(3,' ')+'. '+(question['sessionName'].strip()+': '+question['questionName'].strip()).ljust(69,' '), end='')

        questionid = str(question['_id'])
        if questionid in list(answers.keys()):
            if evaluate(answers[questionid]): 
                print('Solved')
        else:
            if evaluate(question['code']):
                answers.update({questionid: question['code']})
                print('Solved and Added to Database')
            else:
                print('No Solutions Found')

requests.put('https://api.myjson.com/bins/KEY', json=answers)

message = '''
There is no database of solutions for OS elab, so we're just gonna have to make one ourselves!
Contribute to the database by adding new solutions. Anyone who uses OSelab will have their answers 
indexed into the database, which will then be used to solve that same question for everyone else.
We have {} solutions indexed so far. Keep em coming!
'''
input(message.format(len(answers)))
