import time
import requests
import json
import csv


def search(category, types, areas, states, file_name):
    """
    :param category: str
        The category of places to be scrape (Eg: 'shopping malls')
    :param types: str
        The place types (can be refer to https://developers.google.com/places/web-service/supported_types)
    :param areas: list
        The list of areas to be scrape
    :param states: list
        The list of states to be scrape
    :param file_name:
        The output csv file name (Eg: 'output.csv')
    :return: None
    """

    api_url = ''
    api_key = ''

    total_data = 0
    total_error = 0

    # set delay time to 200ms
    delay_time = 0.2

    params = {
        'type': types,
        'key': api_key
    }

    output_file = open('data/' + file_name, 'a', newline='', encoding='utf-8')
    output_write = csv.writer(output_file)

    for i in range(len(states)):
        state = states[i]

        for j in range(len(areas[i])):
            query = category + ' in ' + areas[i][j] + ' ' + state
            params['query'] = query

            try:
                response = requests.get(api_url, params=params)
                results = json.loads(response.content)

                print('area: ' + str(areas[i][j]) + ', ' + state)
                time.sleep(delay_time * 10)  # allow more time to fetch
                data = results['results']

                # print the first twenty responses
                for x in range(len(data)):
                    name = data[x]['name']
                    lat = data[x]['geometry']['location']['lat']
                    lng = data[x]['geometry']['location']['lng']

                    try:
                        print(name, lat, lng)
                        output_write.writerow([name, areas[i][j], state, types, lat, lng])
                        total_data += 1
                    except UnicodeEncodeError:
                        pass  # continue execution to avoid data loss

                # time.sleep(delay_time)

                # print the next twenty (up to forty) responses
                while 'next_page_token' in results:
                    params['pagetoken'] = results['next_page_token']
                    response = requests.get(api_url, params=params)
                    results = json.loads(response.content)

                    time.sleep(delay_time * 10)
                    data = results['results']

                    for x in range(len(data)):
                        name = data[x]['name']
                        lat = data[x]['geometry']['location']['lat']
                        lng = data[x]['geometry']['location']['lng']

                        try:
                            print(name, lat, lng)
                            output_write.writerow([name, areas[i][j], state, types, lat, lng])
                            total_data += 1
                        except UnicodeEncodeError:
                            pass  # continue execution to avoid data loss

                    time.sleep(delay_time)

            # except any errors that occurred
            except Exception as e:
                print('error occurred: ' + str(e))
                total_error += 1

            # reset 'pagetoken' key in params dictionary
            if 'pagetoken' in params:
                del params['pagetoken']

            time.sleep(delay_time)

    print('total data: ' + str(total_data))
    print('total error: ' + str(total_error))



