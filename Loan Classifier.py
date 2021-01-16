# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:26:58 2020

Going to try using some machine learning techniques on the Loan_data.csv file
from my Big Data class

@author: lando
"""

import pandas as pd
#import numpy as np
import tensorflow as tf
import tensorflow.compat.v2.feature_column as fc


### Load and look at data
df = pd.read_csv('C:/Users/lando/Desktop/Spring 2020/Big Data/Loan_data.csv')

# I randomized the order of the entries the first time I did this
# df = df.sample(frac=1).reset_index(drop=True)
# df.to_csv('C:/Users/lando/Desktop/Spring 2020/Big Data/Loan_data.csv')

# print(df.columns)
### Variables
# ID, Loan Status Target (Charged Off: investor has given up on being paid,
#                         Current: investee is still paying,
#                         Fully Paid: all paid off),
# Funded Amount: Money that has been received by the borrower,
# Funded Amount from Investors: Money committed by investors,
# Term Length, Annual Income, Loan Amount: the agreed upon size of the loan,
# Outstanding Principal, Total Payments, Total Recovered Principal,
# Total Recovered Interest, Total Recovered Late Fees,
# Recoveries: amount received after being charged off

# Loan Amount >= Funded Amount >= Funded Amount from Investors

### Make sure our target value is a category column 
### and then convert them to numbers
df['Loan_Status_Target'] = df['Loan_Status_Target'].astype('category')

# Here are the categories in number form
# cats = df['Loan_Status_Target'].cat.categories
# for i in range(len(cats)):
#     print(str(i)+':',cats[i])
# 0: Charged Off
# 1: Current
# 2: Fully Paid

df['Loan_Status_Target'][0:20]
df['Loan_Status_Target'] = df['Loan_Status_Target'].cat.rename_categories(
                                {'Charged Off':0,'Current':1,'Fully Paid':2})
STATUSES = ['Charged Off','Current','Fully Paid']

df = df.dropna(how='any')

### The classifier model wasn't taking 'term' as a categorical feature column
#   It wasn't taking any columns as categorical columns
df['term'] = df['term'].str.strip().str.replace(' months','').astype('int64')

### Split into training and testing sets
# len(df) - len(df)//10
df_train = df[0:38106]
y_train = df_train['Loan_Status_Target']
df_train.drop(['Loan_Status_Target','funded_amnt_inv','id'], axis=1)

df_test = df[38106:]
y_test = df_test['Loan_Status_Target']
df_test.drop(['Loan_Status_Target','funded_amnt_inv','id'], axis=1)

### Set up the feature columns
# print(df.dtypes)

#There should be 10 (The predicted value is not one of the feature columns)
integer_columns = ['term','funded_amnt','loan_amnt']
float_columns = ['annual_inc','out_prncp',
                 'total_pymnt','total_rec_prncp','total_rec_int',
                 'total_rec_late_fee','recoveries']

feature_columns = []
for column in integer_columns:
    feature_columns.append(fc.numeric_column(column,dtype = tf.int64)) #Stop saying there's an error goshdarnit
for column in float_columns:
    feature_columns.append(fc.numeric_column(column,dtype = tf.float64))

### Input function

def input_function(features, labels, shuffle=True, batch_size=256):
    # Convert the inputs to a Dataset.
    ds = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle and repeat if you are in training mode.
    if shuffle:
        ds = ds.shuffle(1000).repeat()
    
    return ds.batch(batch_size)

### Building the linear classifier model

classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units = [10],
    n_classes = 3,
    model_dir = 'C:/Users/lando/Desktop/Python/Loan Classifier')

### Training the model
classifier.train(
    input_fn=lambda: input_function(df_train,y_train,shuffle=True),
    steps=5000)

### And testing the model
test_result = classifier.evaluate(
    input_fn=lambda: input_function(df_test,y_test,shuffle=False)
    )

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**test_result))

# The test dataset contains 657 charged off accounts
# and 370 current accounts, so it's really doing its job

### Now let's make some predictions
# New input function
def input_function_2(features, batch_size=256):
    # Converts the Dataframe into a Dataset without labels
    return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)

# Predictions
# Since I don't know how to come up with numbers off the top of my head,
# I am just going to feed it a subset of the test dataset
predictions = classifier.predict(input_fn=lambda: input_function_2(df_test))
i = 0
pred_table = [[0,0,0], # Rows will be actual
              [0,0,0], # Columns will predictions
              [0,0,0]]
for ans in predictions:
    class_id = ans['class_ids'][0]
    pred_table [y_test.values[i]][class_id] += 1
    i+=1
    
line = '\t\t\t'+STATUSES[0]+'\t\t'+STATUSES[1]+'\t\t'+STATUSES[2]+'\n'
for i in range(len(STATUSES)):
    line += STATUSES[i] + ('\t\t' if i == 1 else '\t')
    for j in range(len(pred_table[i])):
        line += str(pred_table[i][j]) + ('\t\t\t\t' if j != 2 else '\n')
        # print(pred_table[i][j])
    # line += '\n'
    
print(line)
