import tensorflow as tf
import pandas as pd
def make_preds_return_average(model_path, csv_path, start_date='2017-01-01', end_date='2019-12-31'):
    ds = pd.read_csv(csv_path)
    test_data = ds[["Temperature_C", "apparent_zenith", "azimuth", "poa_global"]]
    model_1 = tf.keras.models.load_model(model_path)
    predictions = model_1.predict(test_data)
    predictions_df = pd.DataFrame(predictions, columns=['preds'])
    predictions_df.index = pd.date_range(start=start_date, end=end_date, freq='D')
    return list(predictions_df.resample("M").sum().resample("Y").mean()["preds"])


from flask import Flask, render_template, request

app = Flask(__name__)

# Define the index route to render the index.html template
@app.route('/', methods=['GET', 'POST'])
def index():
    consumption_cost = None
    table_data = None
    
    # Check if the form has been submitted
    if request.method == 'POST':
        # Get the consumption cost from the form
        consumption_cost = int(request.form.get('consumption_cost'))
        unit_cost = [5.2, 6.5, 7.0]
        units_consumed = [] #Per month
        for i in range(len(unit_cost)):
            units_consumed.append(consumption_cost/unit_cost[i])
        #print(units_consumed)
        units_generated = make_preds_return_average('../bestest.h5', "../gen_test.csv")
        delta = []
        for i in range(len(units_generated)):
            delta.append(units_generated[i] - units_consumed[i])

        money = []
        for i in range(len(delta)):
            if delta[i]>0:
                money.append(delta[i]*9*12)
            else:
                money.append(delta[i]*unit_cost[i])

        print(money)
        # Process the form data and generate the table data (replace this with your logic)
        table_data = [{'kWh': '3 kWh', 'text1': 'Value 1', 'text2': 'Value 2'},
                      {'kWh': '5 kWh', 'text1': 'Value 3', 'text2': 'Value 4'},
                      {'kWh': '7.5 kWh', 'text1': 'Value 5', 'text2': 'Value 6'}]

    # Render the index.html template with the consumption cost and table data
    return render_template('index.html', consumption_cost=consumption_cost, table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)
