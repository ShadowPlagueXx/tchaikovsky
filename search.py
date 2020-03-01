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


# reference: https://ms.wikipedia.org/wiki/Senarai_daerah_bagi_setiap_negeri_di_Malaysia_mengikut_populasi
list_of_state = ['penang', 'johor', 'kedah', 'kelantan', 'melaka', 'negeri sembilan', 'pahang', 'perak', 'selangor',
                 'terengganu', 'perlis', 'wilayah persekutuan', 'sabah', 'sarawak']
list_of_area = [
    ['timur laut', 'barat daya', 'seberang perai utara', 'seberang perai tengah', 'seberang perai selatan'],
    ['johor bahru', 'batu pahat', 'kluang', 'kulai', 'muar', 'kota tinggi', 'segamat', 'pontian', 'tangkak',
     'mersing'],
    ['sungai petani', 'alor setar', 'kulim', 'kubang pasu', 'baling', 'pendang', 'langkawi', 'yan', 'sik',
     'padang terap', 'pokok sena', 'bandar baharu'],
    ['kota bharu', 'pasir mas', 'tumpat', 'bachok', 'tanah merah', 'pasir puteh', 'kuala krai', 'machang', 'gua musang',
     'jeli', 'lojing'],
    ['melaka tengah', 'alor gajah', 'jasin'],
    ['seremban', 'jempol', 'port dickson', 'tampin', 'kuala pilah', 'rembau', 'jelebu'],
    ['kuantan', 'temerloh', 'bentong', 'maran', 'rompin', 'pekan', 'bera', 'raub', 'jerantut', 'lipis',
     'cameron highlands'],
    ['kinta', 'larut matang selama', 'manjung', 'kerian', 'batang padang', 'kuala kangsar', 'perak tengah', 'hulu',
     'kampar', 'muallim', 'bagan datuk'],
    ['petaling', 'hulu langat', 'klang', 'gombak', 'kuala langat', 'sepang', 'kuala', 'hulu', 'sabak bernam'],
    ['kuala', 'kemaman', 'dungun', 'besut', 'marang', 'hulu', 'setiu', 'kuala nerus'],
    ['arau', 'kaki bukit', 'kangar', 'kuala', 'padang besar', 'simpang empat'],
    ['kuala lumpur', 'labuan', 'putrajaya'],
    ['kota kinabalu', 'tawau', 'sandakan', 'lahad datu', 'keningau', 'kinabatangan', 'semporna', 'papar', 'penampang',
     'beluran', 'tuaran', 'ranau', 'kota belud', 'kudat', 'kota marudu', 'beaufort', 'kunak', 'tenom', 'putatan',
     'pitas', 'tambunan', 'tongod', 'sipitang', 'nabawan', 'kuala penyu'],
    ['kuching', 'miri', 'sibu', 'bintulu', 'serian', 'samarahan', 'sri aman', 'marudi', 'betong', 'sarikei', 'kapit',
     'bau', 'limbang', 'saratok', 'mukah', 'simunjan', 'lawas', 'belaga', 'lundu', 'asajaya', 'daro', 'tatau',
     'maradong', 'kanowit', 'lubok antu', 'selangau', 'song', 'dalat', 'matu', 'julau', 'pakan', 'padawan']
]

search('schools', 'school', list_of_area, list_of_state, 'output-school.csv')
# search('tuition centres', 'tuition_centre', list_of_area, list_of_state, 'output-tc.csv')