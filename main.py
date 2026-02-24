import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dataset = pd.read_csv('store_dataset.csv', encoding='latin1')

#total sales
total_sales = np.sum(dataset.Sales)
print(total_sales)

#total profit
total_profit = np.sum(dataset.Profit)
print(total_profit)

#profit margin
profit_margin = (total_profit/total_sales)*100
print(profit_margin)

#camparison b/t sales and profit
corr = dataset["Sales"].corr(dataset["Profit"])
print(corr)
sns.scatterplot(x = dataset["Sales"], y = dataset["Profit"])
plt.show()
product_corr = dataset.groupby('Product Name')['Sales'].corr(dataset['Profit'])
negative_products = product_corr[product_corr < 0]

#excel file
negative_products_df = negative_products.reset_index()
negative_products_df.columns = ["Product Name", "Correlation"]
negative_products_df.to_excel("negative_correlation_products.xlsx", index=False)

#Sales Growth By Year
dataset["Order Date"] = pd.to_datetime(dataset["Order Date"], errors='coerce')
dataset["Year"] = dataset["Order Date"].dt.year
yearly_sales = dataset.groupby("Year")["Sales"].sum().reset_index()
yearly_sales["Growth %"] = yearly_sales["Sales"].pct_change() * 100
print(yearly_sales)
# #visualization
plt.figure(figsize=(8,5))
plt.plot(yearly_sales["Year"], yearly_sales["Growth %"], marker='o')
plt.title("Yearly Sales Growth Visualization")
plt.xlabel("Year")
plt.ylabel("Growth %")
plt.grid(True)
plt.tight_layout()
plt.show()

#profit growth by year
dataset["Order Date"] = pd.to_datetime(dataset["Order Date"], errors='coerce')
dataset["Year"] = dataset["Order Date"].dt.year
yearly_profit = dataset.groupby("Year")["Profit"].sum().reset_index()
yearly_profit["Profit %"] = yearly_profit["Profit"].pct_change() * 100
print(yearly_profit)
#visualization
plt.figure(figsize=(8,5))
plt.plot(yearly_profit["Year"], yearly_profit["Profit %"], marker='o')
plt.title("Yearly Profit Growth Visualization")
plt.xlabel("Year")
plt.ylabel("Profit %")
plt.grid(True)
plt.tight_layout()
plt.show()

#**********************Geographical Insights******************#
region_sales = dataset.groupby("Region")["Sales"].sum().sort_values(ascending=False)
print(region_sales)

region_sales.plot(kind="bar", color="skyblue")
plt.title("Total Sales by Region")
plt.ylabel("Sales")
plt.show()
#top 10 states by  sales
top_states_sales = dataset.groupby("State")["Sales"].sum().sort_values(ascending=False).head(10)
print(top_states_sales)

top_states_sales.plot(kind="bar", color="green")
plt.title("Top 10 States by Sales")
plt.ylabel("Sales")
plt.show()

#********************Customer Segment Performance***************#
segment_sales = dataset.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
print(segment_sales)

segment_sales.plot(kind="bar")
plt.title("Total Revenue by Segment")
plt.ylabel("Total Sales")
plt.show()

#********************Customer Behavior Insights*************#
purchase_freq = dataset.groupby("Customer ID")["Order ID"].nunique()
avg_purchase_frequency = purchase_freq.mean()
print("Average Purchase Frequency:", avg_purchase_frequency)
#Average Order Value
order_sales = dataset.groupby(["Order ID", "Segment"])["Sales"].sum().reset_index()
aov_segment = order_sales.groupby("Segment")["Sales"].mean().sort_values(ascending=False)
print(aov_segment)

aov_segment.plot(kind="bar")
plt.title("Average Order Value by Segment")
plt.ylabel("Average Order Value")
plt.show()

#***********⃣Product and Category Analysis *************
category_summary = dataset.groupby("Category")[["Sales", "Profit"]].sum().sort_values(by="Sales", ascending=False)
print(category_summary)

category_summary["Sales"].plot(kind="bar")
plt.title("Total Sales by Category")
plt.ylabel("Sales")
plt.show()

#******Top 10 products by sales
top_products_sales = (dataset.groupby("Product Name")["Sales"].sum().sort_values(ascending=False) .head(10))
print(top_products_sales)
#********Top 10 products by profit
top_products_profit = (dataset.groupby("Product Name")["Profit"].sum().sort_values(ascending=False).head(10))
print(top_products_profit)
#margin
subcat_margin = (dataset.groupby("Sub-Category")["Profit"].sum() / dataset.groupby("Sub-Category")["Sales"].sum()).sort_values(ascending=False)
print(subcat_margin)

subcat_margin.plot(kind="bar")
plt.title("Profit Margin by Sub-Category")
plt.ylabel("Profit Margin")
plt.show()

#Does higher discount increase sales
discount_sales_corr = dataset["Discount"].corr(dataset["Sales"])
print("Correlation between Discount and Sales:", discount_sales_corr)
#Does discount reduce profit
discount_sales_corr = dataset["Discount"].corr(dataset["Sales"])
print("Correlation between Discount and Sales:", discount_sales_corr)
#discount vs sales
plt.scatter(dataset["Discount"], dataset["Sales"])
plt.title("Discount vs Sales")
plt.xlabel("Discount")
plt.ylabel("Sales")
plt.show()

#****************Advanced Time Series & Forecasting*******************
dataset["Order Date"] = pd.to_datetime(dataset["Order Date"])

dataset = dataset.sort_values("Order Date")
dataset.set_index("Order Date", inplace=True)

#***********Seasonality & Sales Patterns***********
#by month
monthly_sales = dataset["Sales"].resample("ME").sum()
print(monthly_sales.head())

monthly_sales.plot()
plt.title("Monthly Sales Over Time")
plt.ylabel("Sales")
plt.show()

#quarterly
quarterly_sales = dataset["Sales"].resample("QE").sum()

quarterly_sales.plot()
plt.title("Quarterly Sales")
plt.ylabel("Sales")
plt.show()
#average sale per month
dataset["Month"] = dataset.index.month
avg_monthly_sales = dataset.groupby("Month")["Sales"].mean()
print(avg_monthly_sales)

avg_monthly_sales.plot(kind="bar")
plt.title("Average Sales per Month (Across Years)")
plt.xlabel("Month")
plt.ylabel("Average Sales")
plt.show()

#**********Forecasting
from statsmodels.tsa.arima.model import ARIMA
# Use monthly sales
model = ARIMA(monthly_sales, order=(1,1,1))
model_fit = model.fit()
print(model_fit.summary())

#forecasting for next 6 months
forecast = model_fit.forecast(steps=6)
print(forecast)
plt.figure()
monthly_sales.plot(label="Historical")
forecast.plot(label="Forecast")
plt.legend()
plt.title("Sales Forecast (Next 6 Months)")
plt.show()

#********************* KPI Dashboards & Metrics
total_revenue = dataset["Sales"].sum()
print("Total Revenue:", total_revenue)
#year-over-year growth
dataset["Year"] = dataset.index.year
yearly_sales = dataset.groupby("Year")["Sales"].sum()
yoy_growth = yearly_sales.pct_change() * 100
print(yoy_growth)

#Average Order Value
order_value = dataset.groupby("Order ID")["Sales"].sum()
average_order_value = order_value.mean()
print("Average Order Value:", average_order_value)

#loss percentage
loss_orders = dataset[dataset["Profit"]<0]
loss_percentage = (len(loss_orders) / len(dataset)) * 100
print("Loss Percentage:", loss_percentage)

#Discount Effectiveness
discount_effectiveness = dataset["Discount"].corr(dataset["Sales"])
print("Discount Effectiveness:", discount_effectiveness)

#Profit Margin
total_profit = dataset["Profit"].sum()
profit_margin = (total_profit / total_revenue) * 100
print("Profit Margin:", profit_margin)

kpi_summary = pd.DataFrame({
    "Total Revenue": [total_revenue],
    "Total Profit": [total_profit],
    "Average Order Value": [average_order_value],
    "Profit Margin": [profit_margin],
    "Discount-Sales Correlation": [discount_effectiveness]
})

print(kpi_summary)
