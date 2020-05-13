import os
from flask import Flask, request, session, escape, jsonify
from multiprocessing import Process, Queue
from instaposter import InstaPoster

app = Flask(__name__)

app.secret_key = os.urandom(16)

ip = InstaPoster()
scheduler_data = {}

@app.route('/api/v1.0/scheduler/start', methods=['GET'])
def start_scheduler():
    scheduler_data['running'] = True
    q.put(scheduler_data)

    data = {}
    data['username'] = session['username']
    data['message'] = 'Scheduler started!'
    data['status'] = '200'

    return jsonify(data)

@app.route('/api/v1.0/scheduler/stop', methods=['GET'])
def stop_scheduler():
    scheduler_data['running'] = False
    q.put(scheduler_data)

    data = {}
    data['username'] = session['username']
    data['message'] = 'Scheduler stopped!'
    data['status'] = '200'

    return jsonify(data)

@app.route('/api/v1.0/scheduler/status', methods=['GET'])
def status():

    status = 'is not'

    if p.is_alive():
        status = 'is'

    data = {}
    data['username'] = session['username']
    data['message'] = 'process %s running' % (status)
    data['status'] = '200'

    return jsonify(data)

@app.route('/api/v1.0/scheduler/csv', methods=['GET'])
def download():
    data = {}
    data['username'] = session['username']
    data['message'] = 'csv downloaded'
    data['status'] = '200'

    return jsonify(data)

@app.route('/api/v1.0/scheduler/csv', methods=['POST'])
def upload():

    data = {}
    data['username'] = session['username']
    data['message'] = 'csv uploaded'
    data['status'] = '200'

    return jsonify(data)

@app.route('/api/v1.0/user/login', methods=['POST'])
def login():

    data = {}

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        run_scheduler = request.form['run']

        if username is not None and password is not None:

            scheduler_data['username'] = username
            scheduler_data['password'] = password
            scheduler_data['running'] = run_scheduler

            q.put(scheduler_data)

            while True:
                try:

                    login_info = q.get(False)
                    print(login_info)

                    session['username'] = username

                    data['username'] = session['username']
                    data['status'] = login_info['status']

                    break
                except Exception as e:
                    pass


    return jsonify(data)

@app.route('/api/v1.0/user/logout', methods=['POST'])
def logout():

    session.clear()

    # destroy session
    data = {}
    data['username'] = session['username']
    data['message'] = 'loggedout'
    data['status'] = '200'

    return jsonify(data)


@app.route('/api/v1.0/user/info', methods=['GET'])
def userinfo():

    userinfo = 'Login first!'

    if 'username' in session:
        userinfo = '%s is loggedin!' % session['username']

    data = {}
    data['username'] = session['username']
    data['info'] = userinfo
    data['message'] = 'loggedout'
    data['status'] = '200'

    return jsonify(data)

if __name__ == "__main__":

    print('Webserver in running on: http://localhost:5000')

    q = Queue()
    p = Process(target=ip.setup_scheduler, args=(q,))
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
