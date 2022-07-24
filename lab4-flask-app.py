from flask import Flask, render_template, request
import  os
import pickle
import pandas as pd
app = Flask(__name__,template_folder='templates', static_folder='static')
filename = 'model-files/model.pkl'
loaded_model = pickle.load(open(filename, 'rb'))
columns = ['Length1', 'Length2', 'Length3', 'Height', 'Width', 'Species_Bream',
       'Species_Parkki', 'Species_Perch', 'Species_Pike', 'Species_Roach',
       'Species_Smelt', 'Species_Whitefish']
port = int(os.environ.get("PORT", 8000))

@app.route('/')
def index():
    return render_template(r'index.html')

@app.route('/predict_weight', methods=['POST'])
def predict_weight():
    print(dict(request.form))
    form_dict = dict(request.form)
    new_dict = {}
    for i,v in form_dict.items():
        if i=='species':
            species_list = ['Bream','Parkki','Perch','Pike','Roach','Smelt','Whitefish']
            index_ = species_list.index(v)
            species_val = [1 if i==index_ else 0 for i,x in enumerate(species_list) ]
            print(species_val,'species val---')
        else:
            new_dict[i] = float(v)

    first_list = list(new_dict.values())
    print(first_list)
    first_list.extend(species_val)
    print(first_list)
    df_dict = {key:val for key,val in zip(columns,first_list)}
    df = pd.DataFrame(df_dict,index=[0])

    if request.method == 'POST':
        predicted_weight= loaded_model.predict(df)
        print(predicted_weight)
        return render_template('result.html', weight=round(abs(predicted_weight[0]),4))


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=port)