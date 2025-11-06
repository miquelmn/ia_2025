import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from Perceptron import Perceptron

# Generació del conjunt de mostres
X, y = make_classification(n_samples=100, n_features=2, n_redundant=0, n_repeated=0,
                           n_classes=2, n_clusters_per_class=1, class_sep=1.25,
                           random_state=0)

y[y == 0] = -1  # La nostra implementació esta pensada per tenir les classes 1 i -1.


perceptron = Perceptron()
perceptron.fit(X, y)  # Ajusta els pesos
y_prediction = perceptron.predict(X)  # Prediu

#  Resultats
plt.figure(1)
plt.scatter(X[:, 0], X[:, 1], c=y_prediction)  # Mostram el conjunt de mostres el color indica la classe
plt.show()
