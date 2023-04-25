from cgi import test
import requests
import json
import pandas as pd

apiToken = 'd4f9de5c-39bb-4099-84b6-02fcb7d55848'

def getAllProjects(list):
    response = requests.get('https://allure.kznexpress.ru/api/rs/project?page=0&size=100&sort=id%2CASC', headers={'Authorization': 'Api-Token ' + apiToken})
    projects = json.loads(response.text)

    for project in projects['content']:
        if project['name'] == 'Обучающий курс':
            continue

        env = 'Web'

        if 'Android' in project['name'] or 'iOS' in project['name'] or 'Mobile' in project['name']:
            env = 'Mobile'

        list.append({'ID': project['id'], 'NAME': project['name'], 'ENV': env})

def getTestCases(AllureProject, list):
    response = requests.get('https://allure.kznexpress.ru/api/rs/testcase?projectId=' + str(AllureProject['ID']) + '&size=1500&sort=createdDate%2CDESC', headers={'Authorization': 'Api-Token ' + apiToken})
    testCases = json.loads(response.text)

    for testCase in testCases['content']:
        testLayer = ""
        severity = ""

        response = requests.get('https://allure.kznexpress.ru/api/rs/testcase/' + str(testCase['id']) + '/cfv', headers={'Authorization': 'Api-Token ' + apiToken})
        testCaseCustomFields = json.loads(response.text)

        if 'testLayer' in testCase:
            testLayer = testCase['testLayer']['name']
        for fields in testCaseCustomFields:
            if fields['customField']['name'] == "Severity":
                severity = fields['name']

        list.append({'ID': testCase['id'], 'NAME': testCase['name'], 'IS_AUTOMATED': testCase['automated'], 'TEST_LAYER': testLayer,
                     'SEVERITY': severity, 'PROJECT': AllureProject['NAME'], 'ENV': AllureProject['ENV']})
    
    print('Project DONE:' + AllureProject['NAME'])




dataFrameOfCases = pd.DataFrame()
dataFrameOfProjects = pd.DataFrame()

listOfTestCases = [] 
listOfAllureProjects = []
getAllProjects(listOfAllureProjects)
for project in listOfAllureProjects:  
   getTestCases(project, listOfTestCases)

dataFrameOfCases = pd.DataFrame(listOfTestCases)
print(dataFrameOfCases)