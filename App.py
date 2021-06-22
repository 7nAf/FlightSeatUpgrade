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


import pandas as pd
import numpy as np
from validate_email import validate_email
from validation import Validation


class flightseatdata:

    def __init__(self, file):
        self.cabin = ['Economy', 'Premium Economy', 'Business', 'First']
        self.reason = {}
        self.validate = Validation()
        self.df = self.read_csv(file)
        self.dfo = self.df.copy()


    def import_csv(self,file):
        return pd.read_csv(file, header=0)



    def validation_error_log(self,l,error):
        for a in l:
            if a in self.reason.keys():
                self.reason[a] += error
            else:
                self.reason[a] = error


    def processmobile(self):
        boolmobilevalidate = self.df['Mobile_phone'].astype(str).apply(lambda x: validate.mobilevalidate(x))
        l = list(self.df[np.logical_not(boolmobilevalidate)].index)
        if len(l) > 0:
            self.validation_error_log(l, 'Mobile phone value corrupted;')
        self.df = self.df[boolmobilevalidate]


    def processdate(self):
        booldatevalidate = pd.to_datetime(self.df['Travel_date'], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S') >= pd.to_datetime(
        self.df['Ticketing_date'], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
        l = list(self.df[np.logical_not(booldatevalidate)].index)
        if len(l) > 0:
            self.validation_error_log(l, 'Travel date value corrupted;')
        self.df = self.df[booldatevalidate]



    def processemail(self):
        boolemailvalidate = self.df['Email'].astype(str).apply(lambda x: validate_email(x))
        l = list(self.df[np.logical_not(boolemailvalidate)].index)
        if len(l) > 0:
            self.validation_error_log(l, 'Email value corrupted;')
        self.df = self.df[boolemailvalidate]


    def processcabin(self):
        boolcabinvalidate = self.df['Booked_cabin'].apply(lambda x: str(x) in cabin)
        l = list(self.df[np.logical_not(boolcabinvalidate)].index)
        if len(l) > 0:
            self.validation_error_log(l, 'Booked cabin value corrupted;')
        self.df = self.df[boolcabinvalidate]

    def processpnr(self):
        boolpnrvalidate = self.df['PNR'].astype(str).apply(lambda x: self.validate.pnrvalidate(x))
        l = list(self.df[np.logical_not(boolpnrvalidate)].index)
        if len(l) > 0:
            self.validation_error_log(l, 'PNR corrupted;')

        return self.df[boolpnrvalidate]


    def process(self):
        self.processemail()
        self.processdate()
        self.processmobile()
        self.processpnr()

    def code(el):
        el = str(el)
        if el >= 'A' and el <= 'E':
            return "OFFER_20"f
        elif el >= 'F' and el <= 'K':
            return "OFFER_30"
        elif el >= 'L' and el <= 'R':
            return "OFFER_25"
        else:
            return None

    def addfare_class(self):
        self.df['Discount_code'] = self.df['Fare_class'].apply(self.code)
        return self.df.copy()



    def exportvalidatedcsv(self):

    def exportinvalidatedcsv(self):









if __name__ == 'main':
    f_instance=flightseatdata("input.csv")
    f_instance.process()
    validated = f_instance.addfare_class()
    invalidated = f_instance.dfo.loc[list(f_instance.reason.keys()), :]
    invalidated["validation_failure_reason"] = f_instance.reason
    invalidated["validation_failure_reason"].replace(f_instance.reason, inplace=True)
    validated.to_csv(r'validated.csv', index=False)
    invalidated.to_csv(r'invalidated.csv', index=False)