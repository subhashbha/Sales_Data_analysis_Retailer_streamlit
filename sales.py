
##1. import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

##2.create Dataset
np.random.seed(42)  ## set random seed for reproducibility  i.e random values will not change even if you try multiple times

## create a synthetic dataset dictionaries
data={
    'product_id':range(1,21),
    'product_name':[f'Product{i}'for i in range(1,21)],
        'category':np.random.choice(["electronics",'clothing','home','sports'],20),
        'units_sold':np.random.poisson(lam=20,size=20),  ##poisson distribution
        'sales_date':pd.date_range(start='2023-01-01',periods=20,freq='D')
     }
##print(data)
## 3.have putted the dictionary to dataframe so that it will be n dimensional array
sales_data=pd.DataFrame(data) 
print("Sales_Data:")  ##prints table name
print(sales_data)


## 4.saving data in the form of csv
sales_data.to_csv("sales_data.csv",index=False);

import os
os.getcwd()
print("path of file:",os.getcwd()) 

##5. descriptive stats (mean,median,mode)

descriptive_stats=sales_data['units_sold'].describe();
print("\n Descriptive statistics for unit sold")
print(descriptive_stats)
'''
path of file: c:\DataScience\DS

 Descriptive statistics for unt sold
count    20.000000
mean     18.800000
std       3.302312
min      13.000000
25%      17.000000
50%      18.500000
75%      21.000000
max      25.000000
Name: units_sold, dtype: float64
'''

#additional stats
mean_sales=sales_data['units_sold'].mean() ##18.8
median_sales=sales_data['units_sold'].median()##18.5
mode_sales=sales_data['units_sold'].mode()[0] 
'''o/p 
0    17
1    21
Name: units_sold, dtype: int32'''
variance_sales=sales_data['units_sold'].var() ##10.90526
std_deviation_sales=sales_data['units_sold'].std() #3.3023

## group by category and calculate total and average sales
category_stats=sales_data.groupby('category')['units_sold'].agg(['sum','mean','std']).reset_index()
'''           category  sum       mean       std
0     clothing   21  21.000000       NaN
1  electronics   73  18.250000  2.217356
2         home  181  20.111111  3.723051
3       sports  101  16.833333  2.714160

'''
## arrange the coloumnNames so that they are more meaningfull
category_stats.columns=['Category','Total Units sold','avg Units Sold','Std Dev of Units Sold'];
'''      Category  Total Units sold  avg Units Sold  Std Dev of Units Sold
0     clothing                21       21.000000                    NaN
1  electronics                73       18.250000               2.217356
2         home               181       20.111111               3.723051
3       sports               101       16.833333               2.714160
'''
print("\nStatistical Analysis:")
print(f"Mean Units Sold:{mean_sales}")
print(f"Median Units Sold:{median_sales}")
print(f"Mode Units Sold:{mode_sales}")
print(f"Variance Units Sold:{variance_sales}")
print(f"Standar Deviation of Units Sold:{std_deviation_sales}")
print(f"categorical_stats:\n{category_stats}")

##6.Infrential stats

confidence_level=0.95
degrees_freedom=len(sales_data['units_sold'])-1;##19
sample_mean=mean_sales
sample_standard_error=std_deviation_sales/np.sqrt(len(sales_data['units_sold'])
                                                  )
#t_score for the confidence level
t_score=stats.t.ppf((1+confidence_level)/2,degrees_freedom)
margin_of_error=t_score*sample_standard_error

confidence_interval=(sample_mean-margin_of_error,sample_mean+margin_of_error)
print(f"Confidence Interval:{confidence_interval}")##(20.34552949217643), np.float64(17.254470507823573))

##7. Hypothesis testing
##Null hypothesis: mean units sold is 20
##alternative hypothesis :mean units sold is not=20
t_statistics,p_value=stats.ttest_1samp(sales_data['units_sold'],20)

print("/n Hypothesis testing:")
print(f"T-statistics:{t_statistics},p-value:{p_value}")
if(p_value<0.05):
    print("Reject null hypothesis: the mean units sold is significantly different from 20")
else:
    print("Fail to reject null hypothesis: the mean units sold is not significantly different from 20")
    
    ##8.Visualization
    sns.set_theme(style="whitegrid")

# Plot distribution of units sold
plt.figure(figsize=(10, 6))
sns.histplot(sales_data['units_sold'], bins=10, kde=True)
plt.title('Distribution of Units Sold')
plt.xlabel('Units Sold')
plt.ylabel('Frequency')
plt.axvline(mean_sales, color='red', linestyle='--', label='Mean')
plt.axvline(median_sales, color='blue', linestyle='--', label='Median')
plt.axvline(mode_sales, color='green', linestyle='--', label='Mode')
##plt.legend()
plt.show()

# Boxplot for units sold by category
plt.figure(figsize=(10, 6))
sns.boxplot(x='category', y='units_sold', data=sales_data)
plt.title('Boxplot of Units Sold by Category')
plt.xlabel('Category')
plt.ylabel('Units Sold')
plt.legend()
plt.show()

# Bar plot for total units sold by category
plt.figure(figsize=(10, 6))
sns.barplot(x='Category', y='Total Units sold', data=category_stats)
plt.title('Total Units Sold by Category')
plt.xlabel('Category')
plt.ylabel('Total Units Sold')
plt.legend()
plt.show()