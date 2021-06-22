#!/usr/bin/env python
# coding: utf-8

# ## Flight Seat Discount
# **Validations:**
# 
# * Email ID is valid
# * The mobile phone is valid
# * Ticketing date is before travel date
# * PNR is 6 characters and Is alphanumeric
# * The booked cabin is valid (one of Economy, Premium Economy,Business, First)
# 
# **FareClass insights and validation error message**
# * Fare class A - E will
# have discount code OFFER_20, F - K will have discount code OFFER_30, L - R will have OFFER_25;
# rest will have no offer code
# * Each failing record should have an additional field that will contain the reason(s) for
# the validation failure.

# In[1]:


import pandas as pd
import numpy as np
from validate_email import validate_email
cabin=['Economy', 'Premium Economy','Business','First']


# In[2]:


df=pd.read_csv("input.csv", header=0)
dfo=df
reason={}


# In[3]:


df.info


# In[4]:


df.head()


# # Validation Steps

# In[5]:


def pnrvalidate(element):
    if element:
        element=str(element).strip()
        return len(element)==6 and element.isalnum()
    else:
        return False  


# In[6]:


def validation_error_log(l,error):
    for a in l:
        if a in reason.keys():
            reason[a]+=error
        else:
            reason[a]=error
reason


# In[7]:


boolpnrvalidate=df['PNR'].astype(str).apply(lambda x:pnrvalidate(x))
l=list(df[np.logical_not(boolpnrvalidate)].index)
if len(l)>0:
    validation_error_log(l,'PNR corrupted;')

df=df[boolpnrvalidate]

df
reason


# In[8]:


def mobilevalidate(element):
    if element:
        return len(element)==10 and element.isalnum()
    else:
        return False


# In[9]:


boolmobilevalidate=df['Mobile_phone'].astype(str).apply(lambda x:mobilevalidate(x))
l=list(df[np.logical_not(boolmobilevalidate)].index)
if len(l)>0:
    validation_error_log(l,'Mobile phone value corrupted;')
df=df[boolmobilevalidate]


# In[10]:



booldatevalidate=pd.to_datetime(df['Travel_date'], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')>=pd.to_datetime(df['Ticketing_date'], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
l=list(df[np.logical_not(booldatevalidate)].index)
if len(l)>0:
    validation_error_log(l,'Travel date value corrupted;')
df=df[booldatevalidate]
df


# In[11]:


boolemailvalidate=df['Email'].astype(str).apply(lambda x:validate_email(x))
l=list(df[np.logical_not(booldatevalidate)].index)
if len(l)>0:
    validation_error_log(l,'Email value corrupted;')
df=df[boolemailvalidate]


# In[12]:



boolcabinvalidate=df['Booked_cabin'].apply(lambda x:str(x) in cabin)
l=list(df[np.logical_not(boolcabinvalidate)].index)
if len(l)>0:
    validation_error_log(l,'Booked cabin value corrupted;')
df=df[boolcabinvalidate]
df


# Fare class A - E will
# have discount code OFFER_20, F - K will have discount code OFFER_30, L - R will have OFFER_25;
# rest will have no offer code

# # Add Fareclass to validated data

# In[13]:


def code(el):
    el=str(el)
    if el>='A' and el <= 'E':
        return "OFFER_20"
    elif el>='F' and el <= 'K':
        return "OFFER_30"
    elif el>='L' and el <= 'R':
        return "OFFER_25"
    else:
        return None
    


# In[14]:


df['Discount_code']=df['Fare_class'].apply(code)


# In[15]:


validated=df


# In[16]:


invalidated=dfo.loc[list(reason.keys()),:]


# In[17]:


invalidated["validation_failure_reason"]=reason


# In[18]:


invalidated["validation_failure_reason"].replace(reason, inplace=True)


# # Export Validated and invalidated data to separate files

# In[19]:



validated.to_csv(r'validated.csv',index=False)
invalidated.to_csv(r'invalidated.csv',index=False)

