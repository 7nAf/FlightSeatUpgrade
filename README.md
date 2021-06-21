# FlightSeatUpgrade
DS project

A major airline wants to send an email, offering a discount on upgrade to a higher class, to all the
passengers who have booked tickets on its flights. For this, the data will be received in a file at a
particular time.
The program needs to read this data, perform some validations and then write it to a different file. The
records that fail the validation, need to be put into a different file so that someone can look at them and
fix the problem. Each failing record should have an additional field that will contain the reason(s) for
the validation failure.
Apart from the validation, we need to add a new column called discount code to the processed records
file whose value will be calculated based on the fare class field in the input record. Fare class A - E will
have discount code OFFER_20, F - K will have discount code OFFER_30, L - R will have OFFER_25;
rest will have no offer code
