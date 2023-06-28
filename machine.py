# 필요한 라이브러리 임포트
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 데이터셋 로드
iris = load_iris()
print(type(iris))
# 특성과 타겟 데이터를 변수에 할당
x = iris['data']
y = iris['target']

# 데이터 분할: 훈련 세트와 테스트 세트로 나눔
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 데이터 스케일링
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# K-NN 분류기 모델 생성과 훈련
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(x_train, y_train)

# 테스트 데이터로 예측 수행
y_pred = knn.predict(x_test)

# 정확도 계산
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)