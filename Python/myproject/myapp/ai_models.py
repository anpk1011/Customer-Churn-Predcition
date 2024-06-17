import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
import joblib

# Đọc dữ liệu.
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

# Train model
model_xgb = xgb.XGBClassifier()

param_grid = {
    'max_depth': [3, 4, 5],
    'learning_rate': [0.1, 0.01, 0.001],
    'n_estimators': [100, 200, 300]
}

grid_search = GridSearchCV(model_xgb, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Chỉ định tên file để lưu model
model_filename = 'xgboost_model.joblib'

# Lưu model XGBoost
joblib.dump(grid_search, model_filename)