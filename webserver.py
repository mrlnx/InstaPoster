from flask import Flask
from multiprocessing import Process, Queue

from instaposter import InstaPoster

app = Flask(__name__)
#ip = InstaPoster('yourgreenchoice', 'Geborenin1992?')
ip = InstaPoster()
scheduler_data = {}

@app.route('/api/v1.0/scheduler/start', methods=['GET'])
def start_scheduler():
    scheduler_data['running'] = True
    q.put(scheduler_data)
    return 'Scheduler started!'

@app.route('/api/v1.0/scheduler/stop', methods=['GET'])
def stop_scheduler():
    scheduler_data['running'] = False

    q.put(scheduler_data)
    return 'Scheduler stopped!'

@app.route('/api/v1.0/scheduler/login', methods=['GET'])
def login():
    scheduler_data['username'] = 'yourgreenchoice'
    scheduler_data['password'] = 'Geborenin1992?'
    scheduler_data['running'] = False

    q.put(scheduler_data)

    return 'Loggedin'

@app.route('/api/v1.0/scheduler/logout', methods=['POST'])
def logout():
    return 'Loggedout'

@app.route('/api/v1.0/scheduler/csv', methods=['GET'])
def download():
    return 'download csv'

@app.route('/api/v1.0/scheduler/csv', methods=['POST'])
def upload():
    return 'upload csv'

if __name__ == "__main__":

    print('Webserver in running on: http://localhost:5000')
    q = Queue()
    p = Process(target=ip.setup_scheduler, args=(q,))
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
