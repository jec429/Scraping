import numpy as np
from flask import Flask, redirect, url_for, render_template, request, Response, abort
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_utils import *
import json
import pandas as pd
import multiprocessing as mp


app = Flask(__name__)
app.url_map.converters['list'] = ListConverter

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/kresult/<list:argus>')
@login_required
def keysearch(argus):
    print(argus)
    keyword, max_res = argus
    max_res = int(max_res)

    pool = mp.Pool(processes=(mp.cpu_count() - 1))
    # results = pool.map(worker, [(keyword, 900), (keyword, 901), (keyword, 902), (keyword, 903), (keyword, 904),
    #                            (keyword, 905), (keyword, 906), (keyword, 907), (keyword, 908), (keyword, 909)])
    results = pool.map(worker, [(keyword, 9)])
    pool.close()
    pool.join()
    joined_results = results[0]
    for r in results[1:]:
        for key in r.keys():
            if key in joined_results.keys():
                aff = joined_results[key][0]
                papers = joined_results[key][1]
                citations = joined_results[key][2]
                joined_results[key] = [aff, papers + r[key][1], citations + r[key][2]]
            else:
                joined_results[key] = r[key]

    df = pd.DataFrame.from_dict(joined_results, orient='index', columns=['Affiliation', 'Publications', 'Citations'])

    df['Name'] = df.index
    print('Shape 1=', df.shape[0])
    df['Z'] = [sum(x) for x in df['Citations']]
    # df['Z'] = [len(x) for x in df['Publications']]
    # df = df.sort_values(by=['Z'], ascending=False)
    df = df[['Name', 'Affiliation', 'Publications', 'Citations']]

    h_indices = []
    for c in df['Citations']:
        h = 0
        for i, p in enumerate(sorted(c, reverse=True)):
            if p > i:
                h += 1
        h_indices.append(h)

    df['Name'] = df['Name'].str.replace('-', ', ')
    df['Index'] = h_indices
    df = df.sort_values(by=['Index'], ascending=False)
    if max_res < 200:
        df = df[:max_res]
    else:
        df = df
    # df = df.drop('Citations', axis=1)
    if df.shape[0] == 0:
        return "<html><body><h1>Keyword not found!</h1><h1><button onclick='goBack()'>Go Back</button><script>function \
        goBack() {window.history.back();}</script></h1></body></html>"
    else:
        string = write_table(df)
        # return render_template('key_results.html')
        return string


@app.route('/cresult/<list:argus>')
def cap_search(argus):
    print(argus)
    fn, ln = argus

    with open('authors_with_patents_9.json') as json_file:
        data = json.load(json_file)

    key = ln + '-' + fn

    if key not in data.keys():
        return "<html><body><h1>Keyword not found!</h1><h1><button onclick='goBack()'>Go Back</button><script>function \
        goBack() {window.history.back();}</script></h1></body></html>"
    else:
        write_html(key, data[key])
        return render_template('key_results.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        # fn = request.form['fn'].replace('/', ' ')
        # ln = request.form['ln'].replace('/', ' ')
        kw = request.form['kw']
        max_res = request.form['max_res']
        # return redirect(url_for('cap_search', argus=[fn, ln, max_res]))
        return redirect(url_for('keysearch', argus=[kw, max_res]))


@app.route('/name_search', methods=['POST', 'GET'])
def name_search():
    if request.method == 'POST':
        fn = request.form['fn'].replace('/', ' ')
        ln = request.form['ln'].replace('/', ' ')
        # kw = request.form['kw']
        return redirect(url_for('cap_search', argus=[fn, ln]))
        # return redirect(url_for('keysearch', argus=[kw, max_res]))


@app.route('/main_search')
@login_required
def main_search():
    return render_template('main_search.html')


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == password:
                login_user(user)
                return redirect(url_for('main_search'))
            else:
                return abort(401)
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            Username:<br>
            <p><input type=text name=username>
            <br>
            Password:<br>
            <p><input type=password name=password>
            <br><br>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


# handle login failed
@app.errorhandler(401)
def page_not_found():
    return render_template('login_failed.html')


# callback to reload the user object
@login_manager.user_loader
def load_user(username):
    user_entry = User.get(username)
    return User(user_entry[0], user_entry[1])


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSANOTHERSECRET"
    app.run(debug=True, port=5000)
