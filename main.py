import os
import sys
import requests
import time
import colorful


def main():
    HOST = "https://api.reflect.run/v1"
    headers = {"X-API-KEY": os.environ["INPUT_REFLECT_API_KEY"]}
    suite_id = os.environ["INPUT_REFLECT_SUITE_ID"]

    execute_res = requests.post(f'{HOST}/suites/{suite_id}/executions', headers=headers)
    execution_id = execute_res.json()['executionId']

    is_finished = False
    while not is_finished:
        time.sleep(10)
        execution_status_res = requests.get(f'{HOST}/suites/{suite_id}/executions/{execution_id}', headers=headers)
        execution_status_json = execution_status_res.json()
        is_finished = execution_status_json['isFinished']
        if not is_finished:
            print('Execution in prgoress')
        else:
            status = execution_status_json["status"]
            url = execution_status_json["url"]
            message = f'Execution is finished\nStatus is {status}\nTests URL {url}'
            if status in ['passed', 'pending', 'canceled']:
                print(colorful.green(message))
                sys.exit(0)
            print(colorful.red(message))
            sys.exit(1)


if __name__ == "__main__":
    main()
