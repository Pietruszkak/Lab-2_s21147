import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Generowanie prostego zbioru danych
def generate_data():
    X = np.vstack([
    np.random.normal(loc=[1, 1], scale=[1, 1], size=(50, 2)),
    np.random.normal(loc=[4, 4], scale=[1, 1], size=(50, 2))
    ])
    y=np.array([0] * 50 + [1] * 50)

    return X, y
# Trenowanie prostego modelu regresji logistycznej
def train_model():
    X, y = generate_data()
    # Podział na zbiór treningowy i testowy

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Trenowanie modelu
    model = LogisticRegression()
    model.fit(X_train, y_train)
    # Predykcja na zbiorze testowym
    y_pred= model.predict(X_test)
    # Wyliczenie dokładności
    accuracy = np.sum(y_test == y_pred) / len(y_test)
    # Zapis wyniku
    f = open("accuracy.txt", "w")
    f.write(f"Model trained with accuracy: {accuracy * 100:.2f}%")
    f.close()
    print(f"Model trained with accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    train_model()
