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
        consumption_cost = request.form.get('consumption_cost')
        if consumption_cost == None:
            return render_template('index.html')
        consumption_cost_int = int(consumption_cost)            
        unit_cost = [5.2, 6.5, 7.0]
        units_consumed = [] #Per month
        for i in range(len(unit_cost)):
            units_consumed.append(consumption_cost_int/unit_cost[i])
        #print(units_consumed)
        units_generated = make_preds_return_average("C:/Users/csvel/OneDrive/Desktop/Codecode/bestest3.h5", "C:/Users/csvel/OneDrive/Desktop/Codecode/gen_test.csv")
        delta = []
        for i in range(len(units_generated)):
            delta.append(units_generated[i] - units_consumed[i])

        money = []
        for i in range(len(delta)):
            if delta[i]>0:
                money.append(f"{delta[i]*9*12:.2f}")
            else:
                money.append(f"{delta[i] * unit_cost[i]:.2f}")
        money = [float(x) for x in money]
        avg_return_3 = sum(money)/len(money)
        resp_3 = ""
        if avg_return_3>0:
            min_time_3 = f"{150000/avg_return_3:.2f}"
            max_time_3 = f"{300000/avg_return_3:.2f}"
            resp_3+=f"Capital may be made back in a range of {min_time_3} to {max_time_3} years"
        else:
            resp_3+="This capacity of solar may not be feasible in the near future"
        print(money)

        units_generated_5 = make_preds_return_average("C:/Users/csvel/OneDrive/Desktop/Codecode/bestest5.h5", "C:/Users/csvel/OneDrive/Desktop/Codecode/gen_test_5kwh.csv")
        delta_5 = []
        for i in range(len(units_generated_5)):
            delta_5.append(units_generated_5[i] - units_consumed[i])

        money_5 = []
        for i in range(len(delta_5)):
            if delta_5[i]>0:
                money_5.append(f"{delta_5[i]*9*12:.2f}")
            else:
                money_5.append(f"{delta_5[i] * unit_cost[i]:.2f}")
        money_5 = [float(x) for x in money_5]
        avg_return_5 = sum(money_5)/len(money_5)
        resp_5 = ""
        if avg_return_5>0:
            min_time_5 = f"{283500/avg_return_5:.2f}"
            max_time_5 = f"{355500/avg_return_5:.2f}"
            resp_5+=f"Capital may be made back in a range of {min_time_5} to {max_time_5} years"
        else:
            resp_5+="This capacity of solar may not be feasible in the near future"

        units_generated_7 = make_preds_return_average("C:/Users/csvel/OneDrive/Desktop/Codecode/bestest75.h5", "C:/Users/csvel/OneDrive/Desktop/Codecode/gen_test_75kwh.csv")
        delta_7 = []
        for i in range(len(units_generated_7)):
            delta_7.append(units_generated_7[i] - units_consumed[i])

        money_7 = []
        for i in range(len(delta_7)):
            if delta_7[i]>0:
                money_7.append(f"{delta_7[i]*9*12:.2f}")
            else:
                money_7.append(f"{delta_7[i] * unit_cost[i]:.2f}")
        money_7 = [float(x) for x in money_7]
        avg_return_7 = sum(money_7)/len(money_7)
        resp_7 = ""
        if avg_return_7>0:
            min_time_7 = f"{494594/avg_return_7:.2f}"
            max_time_7 = f"{697137/avg_return_7:.2f}"
            resp_7+=f"Capital may be made back in a range of {min_time_7} to {max_time_7} years"
        else:
            resp_7+="This capacity of solar may not be feasible in the near future"
        # Process the form data and generate the table data (replace this with your logic)
        table_data = [{'topic': '2017 Returns (in Rs)', '3': money[0], '5': money_5[0], '7.5': money_7[0]},
                      {'topic': '2018 Returns (in Rs)', '3': money[1], '5': money_5[1], '7.5': money_7[1]},
                      {'topic': '2019 Returns (in Rs)', '3': money[2], '5': money_5[2], '7.5': money_7[2]},
                      {'topic': 'Feasibility', '3': resp_3, '5': resp_5, '7.5': resp_7}]

    # Render the index.html template with the consumption cost and table data
    return render_template('index.html', consumption_cost=consumption_cost, table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)
