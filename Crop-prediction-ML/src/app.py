from flask import Flask, request, render_template, jsonify
# Alternatively can use Django, FastAPI, or anything similar
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

@app.route('/')
def home_page():
    return render_template('index.html')  # Pass final_result to template

@app.route('/predict', methods=['POST', "GET"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")
    else:
        data = CustomData(
            N=float(request.form.get('N')),
            P=float(request.form.get('P')),
            K=float(request.form.get("K")),
            pH=float(request.form.get("pH")),
            rainfall=float(request.form.get("rainfall")),
            temperature=float(request.form.get("temperature")),
            Area_in_hectares=float(request.form.get('Area_in_hectares')),
            State_Name=request.form.get("State_Name"),
            Crop_Type=request.form.get("Crop_Type"),
            Crop=request.form.get("Crop")
        )

        new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(new_data)

        production = round(pred[0], 2)
        yield_value = round(production / data.Area_in_hectares, 2)  # Calculate yield

        # Pass final_result and yield_value to index.html
        final_result = f"Predicted Crop Production: {production} tons"
        yield_result = f"Predicted Yield: {yield_value} tons/hectare"

        return render_template("index.html", final_result=final_result, yield_result=yield_result)

if __name__ == "__main__":
    app.run(debug=True)


