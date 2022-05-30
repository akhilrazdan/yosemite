import requests
from requests.exceptions import HTTPError
import threading
from datetime import datetime

POLL_AFTER = 2.0 # seconds
DATES_TO_MONITOR = ['2022-06-02', '2022-06-03', '2022-06-04', '2022-06-05', '2022-06-06']
DATES_TO_ALERT = ['2022-06-02', '2022-06-03', '2022-06-04']
def date_summary(json,date):
    return json['facility_availability_summary_view_by_local_date'][date]["tour_availability_summary_view_by_tour_id"]["10086746"]

def main():
    threading.Timer(POLL_AFTER, main).start()
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    url = 'https://www.recreation.gov/api/timedentry/availability/facility/10086745/monthlyAvailabilitySummaryView'
    params = {
        'year': '2022',
        'month': '06',
        'inventoryBucket': 'FIT',
        'tourId' : '10086746'
    }
    headers = {'Content-Type': 'application/json; charset=utf-8',
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
          } # Some headers are needed, or you will get forbidden.
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        jsonResponse = response.json()    
        # print("Entire JSON response")
        # print(jsonResponse) # Uncomment this to see what the JSON looks like. 
        print("-----Time checked : " + current_time + " -----")
        for date in DATES_TO_MONITOR:
            dateJson = date_summary(jsonResponse, date)
            output_str = "Reservation for " + date + "? " + str(dateJson['reservable']) + " / " + str(dateJson['scheduled_count'] )

            if dateJson['has_reservable']:
                if (date in DATES_TO_ALERT):
                    print(output_str + " AVAILABLE ‼️‼️‼️‼️‼️‼️‼️")
                else:
                    print(output_str + " Available‼️  ")

            else:
                print(output_str)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

if __name__ == '__main__':
    main()


