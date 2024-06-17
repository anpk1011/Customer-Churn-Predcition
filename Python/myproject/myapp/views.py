from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import Customer
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
import joblib
import os
from django.conf import settings
BASE_DIR = settings.BASE_DIR
# Create your views here.
from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer, PredictionSerializer

class CustomerViewSet(viewsets.ViewSet , viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    parser_classes = [MultiPartParser, ]
    renderer_classes = [JSONRenderer]

    def filter_queryset(self, queryset):
        cus_id = self.request.query_params.get('customer_id')
        if cus_id:
            queryset = queryset.filter(CustomerId=cus_id)
        return queryset
    
@api_view(['GET'])
def predict_customer(request, customer_id):
    try:
        customer = Customer.objects.get(CustomerId=customer_id)

        data = {
                'CreditScore': [customer.CreditScore],
                'Geography': [customer.Geography],
                'Gender': [customer.Gender],
                'Age': [customer.Age],
                'Tenure': [customer.Tenure],
                'Balance': [customer.Balance],
                'NumOfProducts': [customer.NumOfProducts],
                'HasCrCard': [customer.HasCrCard],
                'IsActiveMember': [customer.IsActiveMember],
                'EstimatedSalary': [customer.EstimatedSalary]
            } 
        BASE_DIR = settings.BASE_DIR
        csv_file_path =  os.path.join(BASE_DIR, 'Churn_Modelling.csv')
        df_scale = pd.read_csv(csv_file_path)

        df = pd.DataFrame(data)

        df['Geography'] = df['Geography'].map({'France': 0, 'Germany': 1, 'Spain': 2})
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1})

        continuous_columns = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']

        # Sử dụng sample_data để tính giá trị Min và Max
        sample_min = df_scale[continuous_columns].min()
        sample_max = df_scale[continuous_columns].max()


        # Thực hiện Min-Max scaling dựa trên giá trị Min và Max từ dữ liệu mẫu
        for col in continuous_columns:
            df[col] = (df[col] - sample_min[col]) / (sample_max[col] - sample_min[col])


        # Tải model XGBoost từ tệp đã lưu
        model_filename = 'xgboost_model.joblib'

        model = joblib.load(model_filename)
        
        y_pred_new = model.predict(df.to_numpy())

        print(y_pred_new)
        # Sau khi bạn đã có kết quả dự đoán, trả về nó dưới dạng JSON
        response_data = {'prediction': y_pred_new.tolist()}

        return Response(data=response_data)
    except Customer.DoesNotExist:
        return Response(status=404)