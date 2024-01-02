from flask import Flask,redirect,url_for,render_template,request,session,flash
import bcrypt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import ex
from pymongo import MongoClient



client = MongoClient()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/logout')
def logout():
    session.pop('login_user',None)
    return redirect(url_for('patientlogin'))

@app.route('/patientprofile')
def patientprofile():
    return render_template("patientprofile.html")


@app.route('/doctorlogin',methods=['POST','GET'])
def doctorlogin():
    if request.method =='POST':
        db1 = client.doctors
        doctor=db1.my_collection
        login_user = doctor.find_one({'name' : request.form['username']})
        if login_user:
            if request.form['pass'] == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            
        return 'Invalid credentials'
    return render_template('doctor.html')

@app.route('/patientlogin',methods=['POST','GET'])
def patientlogin():
    if request.method =='POST':
        db2 = client.patients
        patient=db2.my_collection
        login_user = patient.find_one({'name' : request.form['username']})
        if login_user:
            if request.form['pass'] == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('patientprofile'))

        return 'Invalid credentials'
    return render_template("patient.html")

@app.route('/prediction',methods=['POST','GET'])
def prediction():
    if request.method=='POST':
        to_predict_list=[]
        for key in request.form.keys():
            to_predict_list = request.form.getlist(key)
        standard_list = '''itching skin_rash nodal_skin_eruptions continuous_sneezing shivering chills joint_pain stomach_pain acidity ulcers_on_tongue	muscle_wasting vomiting burning_micturition spotting_urination fatigue weight_gain anxiety cold_hands_and_feets mood_swings weight_loss restlessness lethargy patches_in_throat irregular_sugar_level cough high_fever sunken_eyes breathlessness sweating dehydration indigestion headache yellowish_skin dark_urine nausea loss_of_appetite pain_behind_the_eyes back_pain constipation abdominal_pain diarrhoea mild_fever yellow_urine yellowing_of_eyes acute_liver_failure fluid_overload swelling_of_stomach swelled_lymph_nodes malaise blurred_and_distorted_vision phlegm throat_irritation redness_of_eyes sinus_pressure runny_nose congestion chest_pain weakness_in_limbs fast_heart_rate pain_during_bowel_movements pain_in_anal_region bloody_stool irritation_in_anus neck_pain dizziness cramps bruising obesity swollen_legs swollen_blood_vessels puffy_face_and_eyes enlarged_thyroid brittle_nails swollen_extremeties excessive_hunger extra_marital_contacts drying_and_tingling_lips slurred_speech knee_pain hip_joint_pain muscle_weakness stiff_neck swelling_joints movement_stiffness spinning_movements loss_of_balance unsteadiness weakness_of_one_body_side loss_of_smell bladder_discomfort foul_smell_of urine continuous_feel_of_urine passage_of_gases internal_itching toxic_look_(typhos) depression irritability muscle_pain altered_sensorium red_spots_over_body belly_pain abnormal_menstruation dischromic_patches watering_from_eyes increased_appetite polyuria family_history mucoid_sputum rusty_sputum lack_of_concentration visual_disturbances receiving_blood_transfusion receiving_unsterile_injections coma stomach_bleeding distention_of_abdomen history_of_alcohol_consumption fluid_overload blood_in_sputum prominent_veins_on_calf palpitations painful_walking pus_filled_pimples blackheads scurring skin_peeling silver_like_dusting small_dents_in_nails inflammatory_nails blister red_sore_around_nose yellow_crust_ooze'''
        nlist=[]
        standard_list=standard_list.replace("\s+"," ")
        for x in standard_list.split(" "):
            if x in to_predict_list:
                nlist.append(1)
            else:
                nlist.append(0)
        result=ex.ValuePredictor(nlist)
        return render_template("prediction.html",result=result)

    return render_template("prediction.html")

@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=='POST':
        data=client.doctors
        doctor=data.my_collection
        spl=request.form['specialisation']
        result=doctor.find_one({'specialisation':spl})
        return render_template("search.html",name=result['name'],specialisation=result['specialisation'],info=result['info'])
    return render_template("search.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/doctorsignup', methods=['POST', 'GET'])
def doctorsignup():
     if request.method == 'POST':
        db1 = client.doctors
        doctor=db1.my_collection
        existing_user = doctor.find_one({'name' : request.form['username']})
        if existing_user is None:
            doctor.insert({'name' : request.form['username'], 'password' : request.form['pass'],'specialisation' : request.form['specialisation'],'info' : request.form['contact']})
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        
        return ('Username already exists!')
     return render_template("doctorsignup.html")
    
@app.route('/patientsignup', methods=['POST', 'GET'])
def patientsignup():
    if request.method == 'POST':
        db2 = client.patients
        patient=db2.my_collection
        existing_user = patient.find_one({'name' : request.form['username']})
        if existing_user is None:
            patient.insert({'name' : request.form['username'], 'password' : request.form['pass']})
            session['username'] = request.form['username']
            return redirect(url_for('patientlogin'))
        
        return ('Username already exists!')
    return render_template("patientsignup.html")

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)