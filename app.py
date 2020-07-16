from flask import Flask, render_template, request, url_for, redirect
import utils
import json

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/watchlist')
def watchlistPage():
    return render_template('watchlist.html')

@app.route('/analysis')
def analysisPage():
    return render_template('analysis.html')

@app.route('/list', methods=['GET', 'POST'])
def possibleLsit():
    if request.method == 'POST':
        fuzzy = request.form.get('stock')
        # results_tickers, results_names, prices = utils.getPossibleResults(fuzzy)
        # results = dict(zip(results_tickers, zip(results_names, prices)))
        results_tickers = utils.getPossibleResults(fuzzy)[0]
        results_names = utils.getPossibleResults(fuzzy)[1]
        utils.crawl(fuzzy)
        prices = utils.prices
        results = dict(zip(results_tickers, zip(results_names, prices)))
        return render_template('list.html', data=results)

# @app.route('/quote', methods=['GET', 'POST'])
# def quote():
#     if request.method == 'POST':
#         selected_ticker = request.get_json()
#         selected_ticker = json.dumps(selected_ticker)
#         possible_result_name = utils.possible_result_name
#         index = possible_result_name.index(selected_ticker)
#         price = utils.accessStockPage(possible_result_name, index)
#         return render_template('quote.html', data=price)
#     # return render_template('quote.html')


if __name__ == "__main__":
    app.run(debug=True)
