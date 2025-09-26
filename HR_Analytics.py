'''


from statistics import median

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df= pd.read_csv("https://raw.githubusercontent.com/swapnilsaurav/projects/refs/heads/main/Data%20Cleaning%20for%20HR%20Analytics%20v1.csv")
#removing dublicates
df= df.drop_duplicates()
print(df)
#Handling missing values
df["Name"]=df["Name"].fillna("unknown")
df["Email"]=df["Email"].replace(["unknown","not an email"],np.nan)
df["Email"]=df["Email"].fillna(method="bfill")

df["Age"]=pd.to_numeric(df["Age"],errors='coerce')
df["Age"]=df["Age"].apply(lambda x: x if 18<=x <=70 else np.nan)
df["Age"]=df["Age"].fillna(df["Age"].median())

df["Salary"]=pd.to_numeric(df["Salary"],errors='coerce')
df["Salary"]=df["Salary"].apply(lambda x: x if x >=0 else np.nan)
df["Salary"]=df["Salary"].fillna(df["Salary"].mean())

df["JoinDate"]=pd.to_datetime(df["JoinDate"],errors='coerce')
df["Department"]=df["Department"].fillna("not specified")
df["Remarks"]=df["Remarks"].replace("",np.nan).fillna("No Remarks")
print(df)

#handiling outliers:
Q1= df["Salary"].quantile(0.25)
Q3= df["Salary"].quantile(0.75)
IQR= Q3-Q1
lower_bound,upper_bound= Q1-1.5*IQR,Q3+1.5*IQR
df["Salary"]=np.clip(df["Salary"],lower_bound,upper_bound)

df.to_excel('HR_analytics.xlsx', index=False)   # needs openpyxl installed


#visualization:
# Age distribution
plt.figure(figsize=(8,4))
sns.histplot(df["Age"],bins=30,kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

#Salary distribution
plt.figure(figsize=(8,4))
sns.boxplot(x=df["Salary"])
plt.title("Salary Distribution with outliers Treated")
plt.xlabel("Salary")
plt.show()

#Department Counts
plt.figure(figsize=(8,4))
sns.countplot(y="Department",data =df,order=df["Department"].value_counts().index)
plt.title("Employees per Department")
plt.xlabel("Count")
plt.ylabel("Department")
plt.show()

#Join Date trend
plt.figure(figsize=(10, 4))
df["JoinYear"] = df["JoinDate"].dt.year
sns.countplot(x="JoinYear", data=df.sort_values("JoinYear"))
plt.title("Employee Joining Trend by Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()