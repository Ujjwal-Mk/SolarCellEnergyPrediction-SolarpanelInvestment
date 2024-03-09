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
        
        # Process the form data and generate the table data (replace this with your logic)
        table_data = [{'kWh': '3 kWh', 'text1': 'Value 1', 'text2': 'Value 2'},
                      {'kWh': '5 kWh', 'text1': 'Value 3', 'text2': 'Value 4'},
                      {'kWh': '7.5 kWh', 'text1': 'Value 5', 'text2': 'Value 6'}]

    # Render the index.html template with the consumption cost and table data
    return render_template('index.html', consumption_cost=consumption_cost, table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)
