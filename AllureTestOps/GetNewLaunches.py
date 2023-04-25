import requests
import json
import pandas as pd
from datetime import date, timedelta, datetime

apiToken = 'd4f9de5c-39bb-4099-84b6-02fcb7d55848'

def getAllProjects(list):
    response = requests.get('https://allure.kznexpress.ru/api/rs/project?page=0&size=100&sort=id%2CASC', headers={'Authorization': 'Api-Token ' + apiToken})
    projects = json.loads(response.text)

    for project in projects['content']:
        if project['name'] == 'Обучающий курс':
            continue

        list.append({'ID': project['id'], 'NAME': project['name']})

def getLaunches(AllureProject, list):
    yesterday = date.today() - timedelta(days = 1)
    yesterdayMiliSeconds = datetime.strptime(yesterday.strftime('%Y-%m-%d'), '%Y-%m-%d').timestamp() * 1000

    response = requests.get('https://allure.kznexpress.ru/api/rs/launch?projectId=' + str(AllureProject['ID']) + '&search=W3siaWQiOiJjaSIsInR5cGUiOiJib29sZWFuIiwidmFsdWUiOiJ0cnVlIn1d&size=5&sort=created_date%2CDESC', headers={'Authorization': 'Api-Token ' + apiToken})
    launches = json.loads(response.text)

    for launch in launches['content']:

        if launch['createdDate'] > yesterdayMiliSeconds:

            passed = 0
            failed = 0
            skipped = 0
            broken = 0

            response = requests.get('https://allure.kznexpress.ru/api/rs/launch/' + str(launch['id']) + '/statistic', headers={'Authorization': 'Api-Token ' + apiToken})
            launchStatistic = json.loads(response.text)

            response = requests.get('https://allure.kznexpress.ru/api/rs/launch/' + str(launch['id']) + '/job', headers={'Authorization': 'Api-Token ' + apiToken})
            launchJobInfo = json.loads(response.text)
            
            type(launchJobInfo[0]['createdDate'])
            launchStartTime = datetime.fromtimestamp(launchJobInfo[0]['createdDate'] / 1000)
            launchEndTime = datetime.fromtimestamp(launchJobInfo[0]['lastModifiedDate'] / 1000)
            launchDuration = (launchEndTime-launchStartTime).total_seconds() / 60.0

            for status in launchStatistic:
                if 'status' in status:
                    if 'passed' == status['status']:
                        passed = status['count']
                    if 'failed' == status['status']:
                        failed = status['count']
                    if 'skipped' == status['status']:
                        skipped = status['count']
                    if 'broken' == status['status']:
                        broken = status['count']

            list.append({'ID': launch['id'], 'PROJECT_NAME': AllureProject['NAME'], 'NAME': launch['name'], 'DURATION': launchDuration, 'CREATED': launchStartTime.strftime('%Y-%m-%d %H:%M:%S'), 
                        'STARTED_BY': launch['createdBy'], 'PASSED': passed, 'FAILED': failed, 'SKIPPED': skipped, 'BROKEN': broken})
        
    print('Project DONE:' + AllureProject['NAME'])




dataFrameOfLaunches = pd.DataFrame()
dataFrameOfProjects = pd.DataFrame()

listOfLaunches = [] 
listOfAllureProjects = []
getAllProjects(listOfAllureProjects)
for project in listOfAllureProjects:  
   getLaunches(project, listOfLaunches)

dataFrameOfLaunches = pd.DataFrame(listOfLaunches)
print(dataFrameOfLaunches)