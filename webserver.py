from flask import Flask
from multiprocessing import Process, Queue

from instaposter import InstaPoster

app = Flask(__name__)
ip = InstaPoster('lilandsue', 'Geborenin1941?')

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

if __name__ == "__main__":

    print('Webserver in running on: http://localhost:5000')
    q = Queue()
    p = Process(target=ip.setup_scheduler, args=(q,))
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
