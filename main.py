from flask import Flask
import logging
import sys

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=["GET"])
def hello_world():
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
    return prefix_google + "Hello World"



@app.route('/logger')
def printMsg():
    app.logger.warning('Hi i am log')
    script = """
    <script>
    console.log('coucou la console')
    </script>
    """
    #print('Hello world!', file=sys.stdout)
    return "Check your console" + script

if __name__ == '__main__':
    app.run(debug=True)