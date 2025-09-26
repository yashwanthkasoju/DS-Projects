import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import  urlopen
from bs4 import BeautifulSoup
url ="https://www.hubertiming.com/results/2017GPTR10K"
html= urlopen(url)
soup=BeautifulSoup(html,'lxml')
type(soup)
title =soup.title
print(title)
text = soup.get_text
print(soup.text)
soup.find_all('a')
all_links=soup.find_all("a")
#for link in all_links:
    #print(link.get("href"))
print("#printing 10 rows for sanity test")
rows= soup.find_all('tr')
print(rows[:10])
for row in rows:
    row_td=row.find_all('td')
print(row_td)
type(row_td)
str_cells =str(row_td)
cleantext =BeautifulSoup(str_cells,"lxml").get_text()
print(cleantext)
import re
list_rows=[]
for row in rows:
    cells= row.find_all('td')
    str_cells=str(cells)
    clean =re.compile('<.*?>')
    clean2=(re.sub(clean,'',str_cells))
    list_rows.append(clean2)
print(clean2)
type(clean2)
df= pd.DataFrame(list_rows)
df.head(10)

#data manupulation and cleaning
df1=df[0].str.split(',',expand=True)
print(df1.head(10))
df1=df[0].str.split(',',expand=True)
print(df.head(10))

col_labels=soup.find_all('th')
all_header=[]
col_str=str(col_labels)
cleantext2=BeautifulSoup(col_str,"lxml").get_text()
all_header.append(cleantext2)
print(all_header)
df2=pd.DataFrame(all_header)
print(df2.head())
df3=df2[0].str.split(',',expand=True)
print(df3.head())
frames=[df3,df1]
df4=pd.concat(frames)
df4.head()
df5=df4.rename(columns= df4.iloc[0])
df5.head()
print(df5.info())
print(df5.shape)
df6= df5.dropna(axis=0,how='any')
df7=df6.drop(df6.index[0])
print(df7.head())

df7.rename(columns={'[Place':'Place'},inplace=True)
df7.rename(columns={' Team]':'Team'},inplace=True)
print(df7.head())
df7['Team']=df7['Team'].str.strip(']')
print(df7.head())
df7.columns = df7.columns.astype(str).str.replace(r'[\[\]]', '', regex=True).str.strip()
df7.rename(columns={'[Place':'Place'},inplace=True)
df7.rename(columns={'Team]]':'Team'},inplace=True)
print(df7.head())

#data analysis and visualization
time_list = df7['Time'].tolist()
print(time_list)

time_mins=[]
for i in time_list:
    if i.count(":")==1:
        m,s =i.split(':')
        math = ((int(m)*60)+int(s))/60
    elif i.count(":")==2:
        h,m,s =i.split(':')
        math= (int(h)*3600+(int(m)*60)+int(s))/60
    else:
        print("error")
        math=0
    time_mins.append(math)

df7['Runner_mins']=time_mins
print(df7.head())
print(df7.describe(include=[np.number]))

#Box Plot
from pylab import rcParams
rcParams['figure.figsize']=15,5
df7.boxplot(column='Runner_mins')
plt.grid(True,axis='y')
plt.ylabel('Time')
plt.xticks([1],['Runners'])
#plt.show()

#Normal distribution
x=df7['Runner_mins']
ax=sns.distplot(x,hist=True,kde=True,rug=False,color='r',bins=25,hist_kws={'edgecolor':'black'})
#plt.show()

# comparing male and female time to finish
f_fuko=df7.loc[df7['Gender']==' F']['Runner_mins']
m_fuko=df7.loc[df7['Gender']==' M']['Runner_mins']
sns.distplot(f_fuko,hist=True,kde=True,rug=False,hist_kws={'edgecolor':'black'},label='Female')
sns.distplot(m_fuko,hist=False,kde=True,rug=False,hist_kws={'edgecolor':'black'},label='Male')
plt.legend()
#plt.show()

g_stats = df7.groupby("Gender",as_index=True).describe()
print(g_stats)

# plotting comparing M and F  box plots
df7.boxplot(column='Runner_mins',by='Gender')
plt.ylabel('Time')
plt.suptitle("")
plt.show()

















