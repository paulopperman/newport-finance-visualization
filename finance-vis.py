from flask import Flask, render_template
import pandas as pd



app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/revenue')
def revenue():

    scale = 1 # scaling term

    # load in dataset
    datafile = '../../Datasets/newport-finances/newport-annual-budget-actuals-2014-2016.csv'
    actuals = pd.read_csv(datafile, skiprows=4)
    actuals = actuals.dropna(subset=['Unnamed: 2'], axis=0)
    # convert currency strings to ints
    actuals[['2014-15 Actual', '2015-16 Actual']] = actuals[['2014-15 Actual', '2015-16 Actual']].replace(',', '',regex=True).astype('int')
    grouped = actuals.groupby('Unnamed: 0')

    # structure the data for display
    cons = {}
    for name, group in grouped:
        sums = group.groupby('Unnamed: 1')['2014-15 Actual'].sum()
        cons[name] = sums

    revenues = []
    for i in cons['Revenues'].index:
        if cons['Revenues'][i] > 0 :
            revenues.extend([(i, 'Incomes', cons['Revenues'][i]/scale)])


    for i, row in grouped.get_group('Revenues').iterrows():
        if row['2014-15 Actual'] > 0:
            revenues.extend([(row['Unnamed: 2'], row['Unnamed: 1'], row['2014-15 Actual']/scale)])

    expenses = []
    for i in cons['Expenses'].index:
        expenses.extend([(i, 'Expensesa', cons['Expenses'][i])])

    return render_template('revenue.html', revenues=revenues, expenses=expenses)


if __name__ == '__main__':
    app.run()
