# Set up and intro
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


iowa_file_path = '../input/house-prices-advanced-regression-techniques/train.csv'
home_data = pd.read_csv(iowa_file_path)
home_data
home_data.columns


# Feature specifications, experiment with possible different features / explanatory variables.
features1 = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']  # simple model / possible baseline
features2 = ['LotArea', 'YearBuilt', 'BedroomAbvGr', 'TotRmsAbvGrd', 'KitchenQual', 'FullBath', 'GrLivArea', 'OverallQual', 'GarageCars', 'GarageArea', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF']
features3 = 
features4 =


##### First things first
# Descriptive statistics summaries
home_data['SalePrice'].describe()     # the max value seems like an outliner considering the standard deviation and mean of our sales prices. check into removing outliers


plt.hist(home_data['SalePrice'], bins = 100) # distribution looks to be right skewed, not normal.
sns.distplot(home_data['SalePrice']) # seaborn makes it easier to graph with a line going around the distribution, harder to do with matplotlib

print("Skewness: %f" % home_data['SalePrice'].skew()) # scipy-stats skewness computed as fisher-pearson coefficient of sample skewness, 
# normal distribution would have skew of 0 or close to 0

print("Kurtosis: %f" % home_data['SalePrice'].kurt()) # scipy stats kurtosis, >3 value indicates higher number of outliers than normal distribution, extreme deviations from mean



##### Data exploration in explanatory variables & relationships with dependent variable(saleprice)

sns.boxplot(x='KitchenQual', y='SalePrice', data=home_data) # somewhat positive correlation between kitchen quality & price, ORDINAL data, encode
sns.relplot(x='GrLivArea', y='SalePrice', data=home_data) # strong positive linearity between Y & X
    # 2 outliers in bottom right when we plot this relationship, best to remove them to avoid it pulling regression line. Be careful however, outliers could contain critical information
    # regarding the data, best to look into those 2 samples and see what's going on before impulsively removing them.
    
sns.boxplot(x='FullBath', y='SalePrice', data=home_data) # somewhat positive linearity between # baths & price in the range of 1-3 bathrooms
sns.boxplot(x='TotRmsAbvGrd', y='SalePrice', data=home_data) # weak positive linearity between bedrooms & price. It only seems significant increase in price from increase in number of rooms
# in the range of 7-9 rooms.

sns.catplot(x='BedroomAbvGr', y='SalePrice', data=home_data) # weak positive linearity, possible check effects with higher sqft houses? (Interaction term differences)
sns.catplot(x='YearBuilt', y='SalePrice', data=home_data) # weak positive linearity, check interaction terms with other variables. Decently important variable in real world for house
# pricing, of course other matters about the house can change significance but generally newer houses are correlated with higher prices, whether this relationship is linear is hard to tell.

sns.catplot(x='Condition1', y='SalePrice', data=home_data) # weak linearity
sns.boxplot(x='OverallQual', y='SalePrice', data=home_data) # decent positive linearity, however i'm suspicious about how this metric was measured, could be suspect to measurement error 
# and make our coefficient estimates biased.

sns.catplot(x='OverallCond', y='SalePrice', data=home_data) # week/no linearity between values 5-10
sns.relplot(x='TotalBsmtSF', y='SalePrice', data=home_data) # strong positive linearity but this is a surprise to me, why is basement square footage so important?
# I suspect this is a characteristic of Iowa or in general areas similar to Iowa where houses have basements, this is where domain knowledge kicks in and suggests further research.
# I also see an outlier in the bottom right, house with 6000 basement sf but ~ 200k? Have to look into this sample

sns.relplot(x='PoolArea', y='SalePrice', data=home_data) # pools are important features in housing price usually, however it seems like very few people own a pool in Iowa therefore we
# wont incorporate a dummy variable about whether a house has a pool or not. Econometric literature usually incorporates pools into their housing price models however, of course domain
# matters as well, not all regions of homes are equal, (ie west coast and east coast)

sns.relplot(x='1stFlrSF', y='SalePrice', data=home_data) # strong positive linearity
sns.relplot(x='2ndFlrSF', y='SalePrice', data=home_data) # positive linearity, however there are many houses that don't have a 2nd floor, should we turn this into a dummy variable?

sns.boxplot(x='BedroomAbvGr', y='SalePrice', data=home_data) # no correlation between bedrooms and price

### check markdown on kaggle kernel

In summary on the graphs plotted above, some important explanatory variables include **"GrLivArea", "TotalBsmtSF", "OverallQual", "YearBuilt", "1stFlrSF", "2ndFlrSF".**

Some variables that are runner ups are "FullBath", "KitchenQual", i'm dissapointed 'KitchenQual' does not have better correlation with 'SalePrice' because I've often heard the saying that "Kitchens sell houses" and how important kitchen size and quality are in residential real estate. My source of knowledge comes my father who works in residential real estate.

These were the variables that fist came to my mind from my past experiences and domain knowledge, however now we will do a more breadth of analysis regarding the explanatory variables in this dataset.

###

##### Data exploration / visualization continued
%matplotlib inline


# Visualizing how neighborhood categories are associated with price to address categorical variable encoding issue
# 1 method is to group the neighborhoods by 2 categories, rich and poor, for this I try to see if there significant differences in price across neighborhoods
# Visually I don't see much evidence for this so I don't thinks this method of encoding would be useful.
sns.relplot(x='LotArea', y='SalePrice', data=home_data, hue='Neighborhood')
plt.xlim(0,80000)

avgprice = home_data['SalePrice'].mean()
avgprice

sns.catplot(x='Neighborhood', y='SalePrice', data=home_data) # average seems to lie ~ 200k and only see 1 neighborhood that has noticeably higher prices


##### Extended Analyses

# Correlation Matrices

homecorrelation = home_data.corr()
f, ax = plt.subplots(figsize=(14, 11))
sns.heatmap(homecorrelation, vmax=.8, square=True)  # Variables that are shown to have correlation with Saleprice that are interesting, 'Fullbath', 'GarageCars', 'GarageArea'
# ah, how could I forget how important garages are! However all these garage variables look too correlated with one another, I sense some multicollinearity. In addition if we look
# deeper into these variables, it makes sense they contain similar information therefore indicating multicollinearity occurs. (Ie, more garagearea -> more garage cars)


