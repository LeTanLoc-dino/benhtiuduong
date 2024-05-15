from django.shortcuts import render, redirect
from .models import Patient, HealthInfo, MedicalHistory
from django.http import HttpResponse
import joblib
import requests
import json
import pandas as pd
import numpy as np
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def member(request):
    return render(request,'member.html')

def signIn(request):
    return render(request,'signIn.html')

def signUp(request):
    return render(request,'signUp.html')

def add_patient(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        age = request.POST['age']
        gender = request.POST.get('gender', False)
        gender = 'Nam' if gender == 'male' else 'Nữ'
        phone_number = request.POST['phone_number']

        # Kiểm tra nếu các trường thông tin không trống
        if full_name and age and phone_number:
            
            # Tạo đối tượng Patient chỉ khi các trường thông tin không trống
            patients = Patient.objects.create(
                full_name=full_name,
                age=age,
                gender=gender,
                phone_number=phone_number
            )
            # Lưu patient.id vào session
            request.session['patient_id'] = patients.id

            return render(request, 'chuandoanBN.html', {'patient_id': patients.id})
        else:
            # Trả về trang thêm thông tin bệnh nhân nếu có trường thông tin trống
            return render(request, 'thongtinBN.html', {'error_message': 'Vui lòng nhập đầy đủ thông tin.'})
    return render(request, 'thongtinBN.html')

def add_health_info(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ request.POST
        patient_id = request.POST['patients_id']
        checkup_date = request.POST['checkup_date']
        # blood_pressure = request.POST['hypertension']
        # heart_disease = request.POST['heart_disease']
        blood_pressure = request.POST.get('hypertension')  
        heart_disease = request.POST.get('heart_disease')
        bmi = request.POST['bmi']
        hba1c = request.POST['HbA1c_level']
        blood_glucose = request.POST['blood_glucose_level']
        result = request.POST['ketqua']

        # Tạo bản ghi HealthInfo
        health_info = HealthInfo.objects.create(
            patient_id=patient_id,
            checkup_date=checkup_date,
            blood_pressure=blood_pressure,
            heart_disease=heart_disease,
            bmi=bmi,
            hba1c=hba1c,
            blood_glucose=blood_glucose
        )

        # Tạo bản ghi MedicalHistory
        medical_history = MedicalHistory.objects.create(
            patient_id=patient_id,
            result=result
        )

        return redirect('home')  # Chuyển hướng về trang chính
        
        # return render(request, 'result.html', {'result': result})  # Render trang kết quả

    # Nếu là GET request, render lại trang chủ hoặc trang khác tương ứng
    return render(request, 'chuandoanBN.html')


def chuandoanBN(request):
    #code dưới đã chuẩn :D
    ketqua = None
    patient_id = request.session.get('patient_id', None)
    if request.method == 'POST':
        model = joblib.load('random_forest_model.pkl')
        
        

        # Lấy dữ liệu từ request.POST và chuyển đổi thành kiểu số
        age = float(request.POST['age'])
        # hypertension = float(request.POST['hypertension'])
        # heart_disease = float(request.POST['heart_disease'])
        hypertension = float(request.POST.get('hypertension')) 
        heart_disease = float(request.POST.get('heart_disease'))
        bmi = float(request.POST['bmi'])
        HbA1c_level = float(request.POST['HbA1c_level'])
        blood_glucose_level = float(request.POST['blood_glucose_level'])

        # # Tạo DataFrame từ dữ liệu nhập vào
        # data = pd.DataFrame([[age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level]],
        #                     columns=['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level'])

        data = pd.DataFrame([[age, blood_glucose_level, HbA1c_level, bmi, hypertension, heart_disease]],
                            columns=['age', 'blood_glucose_level', 'HbA1c_level', 'bmi', 'hypertension','heart_disease'])

        # Chạy dữ liệu qua model để dự đoán
        prediction = model.predict(data)
        
        # Xác định kết quả chẩn đoán
        if prediction[0] == 1:
            ketqua = "Co nguy co benh tieu duong"
        else:
            ketqua = "Khong co nguy co benh tieu duong"
        
    return render(request, 'chuandoanBN.html', {'ketqua': ketqua, 'patient_id': patient_id})

#___________ :D
# chatbot tư vấn

def chatbot(request):
    return render(request,'chatbot.html')

def send_coze_api_request(request):
    # Lấy giá trị từ input trên giao diện web
    query = request.GET.get('query', '')

    # Thông tin API và dữ liệu để gửi
    COZE_URL = 'https://api.coze.com/open_api/v2/chat'
    token = 'pat_HQNySEElrxV2xc4wJ2bpR0cWIySc5ORZThqBXcE5mVUCI9G4XX0I2d8uBiW6HJIX'
    COZE_HEADERS = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
    }
    data = json.dumps({
        "conversation_id": "demo-0",
        "bot_id": "7359622199839899649",
        "user": "demo-user",
        "query": query,  # Sử dụng giá trị query từ input
        "stream": True
    })

    # # Gửi yêu cầu tới API stream:false
    # try:
    #     response = requests.post(COZE_URL, data=data, headers=COZE_HEADERS)
    #     if response.status_code == 200:
    #         response_data = response.json()
    #         # Trích xuất nội dung của tin nhắn đầu tiên từ danh sách 'messages'
    #         bot_response = response_data['messages'][0]['content']
    #     else:
    #         bot_response = f'Failed to send request to Coze API: {response.status_code}'
    # except Exception as e:
    #     bot_response = f'An error occurred: {str(e)}'

    # # Trả về một template với kết quả từ API
    # return render(request, 'chatbot.html', {'bot_response': bot_response, 'query':query})

    # Gửi yêu cầu tới API stream:true
    try:
        response = requests.post(COZE_URL, data=data, headers=COZE_HEADERS)
        if response.status_code == 200:
            # Lọc ra các phản hồi từ dữ liệu phản hồi của API
            response_data = response.json()
            for message in response_data:
                if 'message' in message:
                    bot_response = message['message']['content']
                    print(bot_response)  # In ra kết quả của phản hồi
        else:
            bot_response = f'Failed to send request to Coze API: {response.status_code}'
    except Exception as e:
        bot_response = f'An error occurred: {str(e)}'

    # Trả về một template với kết quả từ API
    return render(request, 'chatbot.html', {'bot_response': bot_response, 'query':query})
















