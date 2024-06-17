import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE



df = pd.read_csv("E:\MyDemoOU\DoAN\Python\Churn_Modelling.csv")

# Bỏ 3 cột RowNumber, CustomerId, Surname
df.drop(["RowNumber", "CustomerId", "Surname"], axis=1, inplace=True)


# Tách cột Exited , gán nhãn dán mục tiêu là Exited
X = df.drop('Exited', axis=1)
y = df['Exited']


# Scale duữ liệu
continuous_columns = ['CreditScore','Age','Tenure','Balance','NumOfProducts','EstimatedSalary']
scaler = MinMaxScaler()
X[continuous_columns] = scaler.fit_transform(X[continuous_columns])


# Lấy các cột object và bắt đầu fit
categorical_cols = X.select_dtypes(include='object')

le = LabelEncoder()

for feature in categorical_cols:
    X[feature] = le.fit_transform(X[feature])
   

# Cân bằng dữ liệu
smote = SMOTE(sampling_strategy='minority')
X_sm, y_sm = smote.fit_resample(X, y)

# Chia thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X_sm, y_sm, test_size=0.2, random_state=15, stratify=y_sm)

# Tải model XGBoost từ tệp đã lưu
model_filename = 'xgboost_model.joblib'
model = joblib.load(model_filename)


# Chọn ngẫu nhiên một chỉ mục hàng (dòng) từ 0 đến số lượng mẫu trong X_test - 1
random_row_index = np.random.randint(0, X_test.shape[0])

# Lấy hàng (dòng) tương ứng từ X_test bằng .iloc
new_data = X_test.iloc[random_row_index]

# Dự đoán trên mẫu dữ liệu mới
y_pred_new = model.predict([new_data])

# In kết quả dự đoán
print("Predicted Label for New Data:", y_pred_new)

