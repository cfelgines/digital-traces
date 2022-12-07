from flask import Flask
import logging
import requests 


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=G-PZD5P4M93D"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-PZD5P4M93D');
    </script>
    """

@app.route('/', methods=["GET"])
def hello_world():
    
    return prefix_google + "Hello World"



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

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/cookie', methods=["GET","POST"])
def mycookies():
    req = requests.get("https://www.google.com/")
    return req.cookies.get_dict() 

@app.route('/cookieganalytics', methods=["GET","POST"])
def mycookieganalytics():
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a251006635w345098879p281216621/%3F_u..nav=default")
    return req.text