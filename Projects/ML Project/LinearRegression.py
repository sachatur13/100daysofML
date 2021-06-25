'''
Author - Saket Chaturvedi

Title - Script for linear regression model

'''

## Importing Linear Regression Library from sklearn
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,OneHotEncoder,LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

### Training and testing split
def get_training_testing_data(input_data,test_size,y):
    
    X = input_data.drop(y,axis = 1)
    X = X.fillna(method = 'ffill')
    y = input_data[y]
    train_X,test_X,train_y,test_y = train_test_split(X,y
                                                     ,test_size=test_size
                                                     ,random_state = 42)
    return train_X,test_X,train_y,test_y

### Test for linear regression assumptions
def test_linear_regression_assumptions(y,selected_column,input_data,
                                       test_type,validation,predicted=False):
    
    ## linear_assumption_1. Linear Relationship between variables.
    
    ## Tested using scatterplot
    if test_type == 'Linearity':
        pair_plot = sns.pairplot(input_data,x_vars = [selected_column],y_vars = y)
        return pair_plot
    
    ## Linear assumption 2 , zero residual mean
    if test_type == 'Residual Mean':
        residuals = validation.values - predicted
        mean_residuals = np.round(np.mean(residuals),2)
        return mean_residuals
    
    ## Linear Assumption 3 , check for equal variance 
    if test_type == 'Homoscedasticity' or test_type == 'Autocorrelation':
        residuals = validation.values - predicted
        residual_plot = sns.scatterplot(predicted,residuals)            
        plt.xlabel('predicted')
        plt.ylabel('residuals')
        plt.xlim(0,200)
        plt.ylim(-80,80)
        residual_plot = sns.lineplot(x= [0,1000],y=[0,0],color = 'blue')
        
        return residual_plot
    
    ## Normal distribution of error terms
    if test_type == 'Normality':
        residuals = validation.values - predicted
        error_plot = sns.distplot(residuals)            
        return error_plot
    
    ## Multicollinearity check
    if test_type == 'Multicollinearity':
        corr_plot = sns.heatmap(input_data.corr(),annot = True)
        return corr_plot
    

## Data preprocessing for training data. Scaler is used for encoding the test data.
def data_preprocessing_training(train_X,test_X):
    scaler = StandardScaler()
    encoder = LabelEncoder()
    train_X = train_X.fillna(method = 'ffill')
    test_X = test_X.fillna(method = 'ffill')
    train_X_transformed = scaler.fit_transform(train_X)
    test_X_transformed = scaler.transform(test_X)
    pickle.dump(scaler,open('numerical_scaler.pkl','wb'))
    
    return train_X_transformed,test_X_transformed

## Data preprocessing for testing data. Scaler from training is used.    
def data_preprocessing_predictions(input_data):
    scaler = pickle.load(open('numerical_scaler.pkl','rb'))
    transformed_input = scaler.transform(input_data)
    
    return transformed_input    

## Fitting predictive model.
def fit_linear_regression_model(train_X,test_X,train_y,test_y):
    
    ''' Fitting linear regression model.'''
    
    
    train_X_transformed,test_X_transformed = data_preprocessing_training(train_X,test_X)
    
    ## Get training and testing splits
        
    regressor = LinearRegression()
    
    regressor.fit(train_X_transformed,train_y)
    
    prediction_y = regressor.predict(test_X_transformed)
    
    from sklearn.metrics import r2_score
    
    r2 = np.round(r2_score(test_y,prediction_y),2)
    
    return regressor,prediction_y,r2

## Predictions using Linear regression model
def make_predictions_using_linear_regression(input_data,regressor):
    
   
    encoded_data = data_preprocessing_predictions(input_data)
    input_data = input_data
    prediction = regressor.predict(encoded_data)
    
    
    return encoded_data,input_data,prediction
    
    
