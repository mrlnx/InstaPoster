from flask import Flask
from multiprocessing import Process

from instaposter import InstaPoster

app = Flask(__name__)

insta_poster = InstaPoster()


if __name__ == "__main__":

    print('Webserver in running on: http://localhost:5000')

    p = Process(target=insta_poster.setup_scheduler())
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
