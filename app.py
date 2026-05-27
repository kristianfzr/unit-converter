from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert/<unit_type>", methods=["GET", "POST"])
def convert(unit_type):
    result = None
    
    all_units = {
        "length": ["millimeter", "centimeter", "meter", "kilometer", "inch", "foot", "yard", "mile"],
        "weight": ["milligram", "gram", "kilogram", "ounce", "pound"],
        "temperature": ["celsius", "fahrenheit", "kelvin"],
    }
    
    conversion_factors = {
        "length": {
            "millimeter": 0.001,
            "centimeter": 0.01, 
            "meter": 1, 
            "kilometer": 1000, 
            "inch": 0.0254, 
            "foot": 0.3048, 
            "yard": 0.9144, 
            "mile": 1609.34
        },
        "weight": {
            "milligram": 0.000001,
            "gram": 0.001,
            "kilogram": 1,
            "ounce": 0.0283495,
            "pound": 0.453592
        },
    }

    to_celsius = {
        "celsius": lambda x: x,
        "fahrenheit": lambda x: (x - 32) * 5.0 / 9.0,
        "kelvin": lambda x: x - 273.15,
        },

    from_celsius = {
        "celsius": lambda x: x,
        "fahrenheit": lambda x: (x * 9.0 / 5.0) + 32,
        "kelvin": lambda x: x + 273.15,
    }
    
    from_unit = None
    units = all_units.get(unit_type, [])
    to_unit = None
    
    if request.method == "POST":
        from_unit = request.form.get("from_unit")
        to_unit = request.form.get("to_unit")
        value = float(request.form.get("value"))
        
        if unit_type == "temperature":
            values_in_celsius = to_celsius[from_unit](value)
            result = from_celsius[to_unit](values_in_celsius)
        else:
            factors = conversion_factors[unit_type]
            value_in_base = value * factors[from_unit]
            result = value_in_base / factors[to_unit]
        
    return render_template("convert.html", unit_type=unit_type, units=units, result=result, from_unit=from_unit, to_unit=to_unit)
        

if __name__ == "__main__":
    app.run(debug=True)