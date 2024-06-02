#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


# In[3]:


df = pd.read_csv("movies.csv")


# In[4]:


df.head(5)


# In[5]:


df.shape


# In[6]:


df.columns


# In[7]:


df.isnull().sum()


# In[8]:


# Drop unnecessary columns (with null values)

df.drop(columns = ["id", "imdb_id", "cast", "homepage", "tagline", "overview", "budget_adj", "revenue_adj"], inplace = True)


# In[9]:


df.head(5)


# In[95]:


df.isnull().sum()


# In[11]:


df.dropna(how = "any", subset = ["genres", "director"], inplace = True)


# In[94]:


df["production_companies"] = df["production_companies"].fillna(0)
df["keywords"] = df["keywords"].fillna(0)


# In[13]:


df


# In[14]:


df["popularity"] = df["popularity"].round(2)


# In[15]:


df


# In[16]:


df.insert(3, 'profit', df.revenue - df.budget)


# In[17]:


df


# In[18]:


df.insert(4, 'roi', df.profit / df.budget)
df["roi"] = df["roi"].round(2)


# In[19]:


df


# In[33]:


df1 = df[["popularity", "budget", "revenue", "profit", "roi", "vote_count", "vote_average", "release_year"]]


# In[28]:


df.isnull().sum()


# In[29]:


df.roi.value_counts()


# In[30]:


non_finite_values = ~np.isfinite(df["roi"])


# In[31]:


non_finite_values.sum()


# In[32]:


df["roi"] = df["roi"].replace([np.inf, -np.inf], np.nan)


# In[34]:


df1.hist(bins = 20, figsize = (16,12))
plt.show


# In[35]:


df.popularity.value_counts()


# In[36]:


df2 = df.groupby("release_year")["roi"].sum()
df2


# In[37]:


df2 = df.groupby("release_year")["roi"].mean()
df2.plot(kind = "line")


# In[38]:


df3 = df.groupby("release_year")["popularity"].plot(kind="line")


# In[39]:


df3 = df.groupby("release_year")["popularity"].sum()
df3.plot(kind="line", color = "green")
plt.xlabel("Year", fontsize = 12)
plt.ylabel("Popularity")


# In[40]:


df4 = df.groupby("release_year")["vote_average"].mean()
df4.plot(kind="line")
plt.xlabel("Year", fontsize = 12)
plt.ylabel("Rating")


# In[41]:


df5 = df.plot.scatter(x = "popularity", y = "vote_average", c = "green", figsize = (6,4))
df5.set_xlabel("Popularity", color = "DarkGreen")
df5.set_ylabel("Vote Average", color = "DarkGreen")
df5.set_title("Popularity vs Vote Average", fontsize = 17)


# In[42]:


df.genres.value_counts()


# In[43]:


split = ["genres"]
for i in split:
    df[i]=df[i].apply(lambda x: x.split("|"))
df.head(3)


# In[ ]:


# Explode does not work due to package deprecation - update pandas library
# df_exploded = df.explode('genres')
# df_exploded


# In[ ]:


# df7 = df.groupby("genres")["popularity"].sum().sort_values(ascending = True)
# df7


# In[ ]:


# df7.plot.barh(x = "genres", y = "popularity", color = "blue", figsize = 12, 6)


# In[ ]:





# In[49]:


df.head(1)


# In[47]:


df.dtypes


# In[46]:


# Change datatype of release_date into datetime
df["release_date"] = pd.to_datetime(df["release_date"])


# In[48]:


df.dtypes


# In[50]:


# Insert new month column
df["extracted_month"] = df["release_date"].dt.month
df.head(5)


# In[52]:


df8 = df.groupby("extracted_month")["popularity"].sum()
df8


# In[53]:


df8.index


# In[55]:


df8.values


# In[56]:


# Creating a dataframe 
data = {
    "extracted_month": df8.index,
    "popularity": df8.values
}
df8 = pd.DataFrame(data)
df8


# In[57]:


# Assign names to the months instead of numbers
index_to_month = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}


# In[59]:


# Mapping the index_to_month to the dataframe
df8.extracted_month = df8.extracted_month.map(index_to_month)
df8


# In[60]:


df8.plot(kind = "bar", x = "extracted_month", y = "popularity", color = "silver")


# In[64]:


df9 = df.groupby("extracted_month")["revenue"].sum()
df9


# In[67]:


data = {
    "extracted_month": df9.index,
    "revenue": df9.values
}
df9 = pd.DataFrame(data)
df9


# In[68]:


index_to_month = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}


# In[69]:


df9.extracted_month = df9.extracted_month.map(index_to_month)
df9


# In[78]:


df9.plot(kind = "bar", x = "extracted_month", y = "revenue", color = "red")
plt.title("Revenue by Month", size = 18)
plt.xlabel("Month", size = 14)
plt.ylabel("Revenue", size = 14)
plt.show()


# In[79]:


df.head()


# In[83]:


df.groupby("original_title")["profit"].sum().sort_values (ascending = False)


# In[84]:


df10 = df.groupby("original_title")["profit"].sum().sort_values (ascending = False).head(5)
df10


# In[88]:


df10.plot(kind = "pie", autopct = "%1.1f%%", startangle = 90)
plt.title("Top 5 Movies by Profit", size = 16)


# In[107]:


df11 = df.production_companies.value_counts().head(5)
df11


# In[110]:


df11.index


# In[120]:


explode_list = [0,0.2,0,0,0] #hightlight or separate from pie chart 
df11.plot(kind = "pie", figsize = (14, 6), autopct = "%1.1f%%", startangle = 90, colors = plt.cm.Paired.colors, labels = None, pctdistance = 1.1, explode = explode_list)
plt.title("Top 5 Production Companies by Profit", size = 16)
plt.legend(labels = df11.index, loc = "upper right")
plt.axis("equal")
plt.show()


# In[ ]:





# In[ ]:





# In[121]:


df.head()


# In[123]:


df.keywords


# In[154]:


df12 = df.keywords.value_counts().head(10)
df12


# In[ ]:





# In[155]:


df12.index


# In[156]:


df12.values


# In[157]:


data = {
    "keywords": df12.index,
    "value": df12.values
}
df12 = pd.DataFrame(data)
df12


# In[ ]:





# In[159]:


fig = px.treemap(df12, path = ["keywords"], values = "value")
fig.show()


# In[ ]:




