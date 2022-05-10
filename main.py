import requests
import time

# --- UPDATE WITH YOUR SERVER HERE ---- #

url = 'https://siddhi1.bpmcep.ics.unisg.ch/engine-rest/external-task/'  # Replace "siddhix" with your instance if you're using Camunda on our server.
# url = 'https://siddhix.bpmcep.ics.unisg.ch/engine-rest/external-task/' # Use this url if you're using Camunda on your machine.

# ------- #

# This is the payload of the request
fetchAndLockPayload = {"workerId": "myExampleWorker",  # ID of the resource to which the task is assigned
                       "maxTasks": 1,  # get only one running instance of the process
                       "usePriority": False,  # don't sort instance by priority
                       "topics":
                           [{"topicName": "charge-card",
                             # name of task's topic (identifies the nature of the work to be performed)
                             "lockDuration": 30000  # duration of the lock
                             }]
                       }

try:

    while True:

        # Prepare the url to run the method fetchAndLock
        fetchAndLock_url = url + 'fetchAndLock'

        # Call API FetchAndLock with prepared url
        response = requests.post(fetchAndLock_url, json=fetchAndLockPayload)

        print('Fetch and lock status code: ', response.status_code)
        print('Fetch and lock response: ', response.text)

        responseJson = response.json()  # JSON of the response
        if len(responseJson) != 0:

            # Get the first item of the response
            task = responseJson[0]

            taskId = task['id']  # get ID of the task
            value = task['variables']['amount']['value']  # get value of variable amount

            # Put you Business Logic here...
            # Example: Print the value of the receipt if the amount is greater than 24
            print_rec_value = (int(value)>24)

            # Prepare the new request...
            # Example: add to the request the values that you want to send back to Camunda server, e.g., print_rec = true
            new_request = {
                "workerId": "myExampleWorker",
                "variables": {"print_rec": {"value": print_rec_value}}
            }

            # Complete the task and update the process variables
            # Method: POST /task/{id}/complete

            # Prepare the url to run the method complete
            complete_url = (url + str(taskId) + '/complete')

            # Call method "complete" with prepared url
            complete = requests.post(complete_url, json=new_request)
            print('complete status code: ', complete.status_code)
        else:
            time.sleep(2)

except KeyboardInterrupt:
    print('Script interrupted by user.')
# except:
#    print('Engine is down')
