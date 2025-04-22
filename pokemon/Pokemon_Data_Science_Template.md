
# 🧪 Pokémon Data Science Project Template

This notebook teaches end-to-end data science using the Pokémon dataset — from loading and cleaning to visualizing and predicting.

---

## 1. 📂 Load the Data

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('Pokemon.csv')
df.head()
df.info()
df.describe()
```

---

## 2. 🔍 Exploratory Data Analysis (EDA)

```python
df['Type 1'].value_counts()
df.groupby('Type 1')['Total'].mean().sort_values(ascending=False)
sns.histplot(df['Attack'], kde=True)
```

---

## 3. 🧼 Data Cleaning

```python
df.isnull().sum()
df['Type 2'].fillna('None', inplace=True)
df.rename(columns={'Sp. Atk': 'Sp_Atk', 'Sp. Def': 'Sp_Def'}, inplace=True)
```

---

## 4. 📊 Visualizations

```python
sns.boxplot(x='Type 1', y='Total', data=df)
sns.heatmap(df.corr(), annot=True)
```

---

## 5. ⚔️ Comparative Analysis

```python
df.groupby('Type 1')[['Attack', 'Speed']].mean().sort_values(by='Attack')
```

---

## 6. 🧠 Feature Engineering

```python
df['IsStrong'] = df['Total'] > 500
df = pd.get_dummies(df, columns=['Type 1'], drop_first=True)
```

---

## 7. 🤖 Prediction (ML)

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X = df[['HP', 'Attack', 'Defense', 'Speed']]
y = df['Legendary']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)
preds = model.predict(X_test)
accuracy_score(y_test, preds)
```

---

## 8. 🧾 Summary

Write up insights here:
- Who are the strongest types?
- How accurate is your model?
- What would you explore next?

Include final plots or export as PDF.
