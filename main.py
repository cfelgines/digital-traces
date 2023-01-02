from flask import Flask
import logging
import requests 
from pytrends.request import TrendReq
import os
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'deta-app-373515-35e1e0cfd6a0.json'

# LE NUMERO DE LA VUE DESSOUS EST A CACHER DANS LE .ENV

VIEW_ID = "281216621" # str(os.getenv("View_ID")) # Get from env

logging.info("LOLLL")
logging.info(VIEW_ID)
logging.info("LOLL2")
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-251006635-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-251006635-1');
    </script>
    """

@app.route('/', methods=["GET"])
def hello_world():
    return prefix_google + "Hello Worldd"



@app.route('/logger')
def printMsg():
    app.logger.warning('Hi i am log')
    script = """
    <body>
    <script>
    console.log('coucou la console')
    function formdata() 
    {
    var consolelogggg= document.getElementById("name").value;
    console.log(consolelogggg)
    }
    </script>
    <input type="text" id="name"/><br><br>
    <input type="submit" value="Submit" onclick="formdata()"/><br>

    </body>
    """
    return "Check your console" + script +prefix_google

@app.route('/visits', methods = ['GET', 'POST'])
def get_nb_visitors():

    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    nb_visitor = print_response(response)
    return "Number of visitors : " + str(nb_visitor) 

@app.route('/cookie', methods=["GET","POST"])
def mycookies():
    req = requests.get("https://www.google.com/")
    return req.cookies.get_dict() 

@app.route('/cookieganalytics', methods=["GET","POST"])
def mycookieganalytics():
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a251006635w345098879p281216621/%3F_u..nav=default")
    return req.text

@app.route('/frequentation', methods=["GET","POST"])
def mycookiefrequentation():
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a251006635w345098879p281216621/%3F_u..nav=default")
    return req.text

# @app.route('/tp3gtfirstreq', methods=["GET","POST"])
# def googletrendrequestone():
#     pytrends = TrendReq(hl='en-US', tz=360)
#     pytrends.build_payload(kw_list=['france'])
#     que = pytrends.interest_over_time()
#     return que['france'].tolist()

# @app.route('/tp3gtsecondreq', methods=["GET","POST"])
# def googletrendrequesttwo():
#     pytrends = TrendReq(hl='en-US', tz=360)
#     pytrends.build_payload(kw_list=['france'])
#     que = pytrends.interest_over_time()
#     quer=que['france'].tolist()
#     date = str(que.index)
#     script = """
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js">
#     <canvas id="myChart" width="400" height="400"></canvas>

#     // Line chart
#     new Chart(document.getElementById("myChart"), {
#         type: 'line',
#         data: {
#             labels: """ + date + """,
#             datasets: [{
#                 data: """ + quer + """,
#                 label: "france",
#                 borderColor: "#3e95cd",
#                 fill: false
#             }
#             ]
#         },
#         options: {
#             title: {
#                 display: true,
#                 text: 'Number of research of france'
#             },
#             hover: {
#                 mode: 'index',
#                 intersect: true
#             },
#         }
#     });
#     </script>
#     """
    
#     return script

if __name__ == '__main__':
    app.run(debug=True)

## To get number of visitors

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.
  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.
  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': []
          #'dimensions': [{'name': 'ga:country'}]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.
  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ', dimension)

      for i, values in enumerate(dateRangeValues):
        print('Date range:', str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          visitors = value
  return str(visitors)
