from flask import Flask, request
import pickle

model = pickle.load(open("Model/finalized_model.sav", 'rb'))

NUM = pickle.load(open("Model/Numeric_model.sav", 'rb'))

app = Flask(__name__)

def prediction(Value):
    y_pred = model.predict([Value])
    Predicted_error = y_pred.tolist()[0]
    return int(Predicted_error)

@app.route('/',methods=['GET'])
def index():
    return "Flask is up and running"    

@app.route('/api', methods=['GET','POST'])
def predict():
    region = {'southwest': 3, 'southeast': 2, 'northwest': 1, 'northeast': 0}
    smoker = {'Yes': 1, 'No': 0}
    Gen = {'Male': 1, 'Female': 0}
    Age = request.values.get('age', type=int)
    Gender = request.values.get('gender', type=str)
    BMI = request.values.get('bmi', type=float)
    Child = request.values.get('children', type=int)
    Smoker = request.values.get('smoker', type=str)
    Region = request.values.get('region', type=str)
    bmi = NUM.transform([[BMI]])
    print(type(Age), type(Gender), type(BMI), type(Child), type(Smoker), type(Region))
    Value = [Gen[Gender], smoker[Smoker], region[Region], Age, float(bmi[0]), Child ]
    try:
        cost = prediction(Value)
        return str(cost)
    except Exception as e:
        return e
        
