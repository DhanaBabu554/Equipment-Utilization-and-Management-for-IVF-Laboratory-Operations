import numpy as np
import pandas  as pd 
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv(r"C:\Users\91950\Desktop\IVF project\IVF_project_dataset.csv")

data.dtypes

num_cols = [
    'max_capacity_hrs','utilization_hrs','utilization_pct',
    'idle_hrs','technical_downtime_hrs',
    'planned_maintenance_hrs','workflow_delay_events','avg_delay_minutes',
    'total_cases_day_lab'
]

for col in num_cols:
    
    print(f"\nstatistical for {col}")
    
    print(f"\nmean: {data[col].mean()}") #First Moment Business Decision
    
    print(f"\nmedian:{data[col].median()}") #First Moment Business Decision
    
    print(f"\nmode:{data[col].mode()[0]}") #First Moment Business Decision
    
    print(f"\nvariance:{data[col].var()}") #Second Moment Business Decision
    
    print(f"\nstandard devition:{data[col].std()}")  #Second Moment Business Decision
    
    print(f"\nrange:{data[col].max()-data[col].min()}")  #Second Moment Business Decision
    
    print(f"\nskewness:{data[col].skew()}")  #Third Moment Business Decision
    
    print(f"\nkurtosis:{data[col].kurt()}")  #Fourth Moment Business Decision
    
    

#### graphical representation ####

data.head()

data.info()
    
plt.figure()
data.isnull().sum().plot(kind="bar")
plt.title("Missing Values Count per Column")
plt.xlabel("Columns")
plt.ylabel("Missing Values")
plt.show()

plt.figure()
plt.hist(data["utilization_pct"], bins=30)
plt.title("Distribution of Utilization Percentage")
plt.xlabel("Utilization Percentage")
plt.ylabel("Frequency")
plt.show()


plt.figure()
plt.boxplot(data["utilization_hrs"].dropna())
plt.title("Boxplot of Utilization Hours")
plt.ylabel("Utilization Hours")
plt.show()

plt.figure()
data.boxplot(column="utilization_pct", by="equipment_type")
plt.title("Utilization Percentage by Equipment Type")
plt.suptitle("")
plt.xlabel("Equipment Type")
plt.ylabel("Utilization Percentage")
plt.show()


plt.figure()
plt.scatter(data["total_cases_day_lab"], data["utilization_pct"])
plt.title("Total Cases per Day vs Utilization Percentage")
plt.xlabel("Total Cases per Day")
plt.ylabel("Utilization Percentage")
plt.show()


# Auto EDA do in jupyter notebook



# data preprocessing
#check data types
data.dtypes

#change the data types
data["date"] = pd.to_datetime(data["date"])

#once ckeck the data types
data.dtypes

#check the data types
data.isnull().sum()

#drop the null values 
data = data.dropna(subset=["date"])

#after drop null values check the data set shape
data.shape

#Check duplicate rows
data.duplicated().sum()
 
#view duplicate rows
data[data.duplicated()]

#drop duplicates rows 
data = data.drop_duplicates()

#After remove duplicates once check the data set shape
data.shape

#Find outliers for utilization_pct 
Q1 = data["utilization_pct"].quantile(0.25)
Q3 = data["utilization_pct"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

data["utilization_pct"] = data["utilization_pct"].clip(lower, upper)

#once check the outliers using boxplot
plt.boxplot(data["utilization_pct"])
plt.title("Boxplot of utilization_pct")
plt.show()

#Doing four business moments After data cleaning
num_cols = [
    'max_capacity_hrs','utilization_hrs','utilization_pct',
    'idle_hrs','technical_downtime_hrs',
    'planned_maintenance_hrs','workflow_delay_events','avg_delay_minutes',
    'total_cases_day_lab'
]

for col in num_cols:
    
    print(f"\nstatistical for {col}")
    
    print(f"\nmean: {data[col].mean()}") #First Moment Business Decision
    
    print(f"\nmedian:{data[col].median()}") #First Moment Business Decision
    
    print(f"\nmode:{data[col].mode()[0]}") #First Moment Business Decision
    
    print(f"\nvariance:{data[col].var()}") #Second Moment Business Decision
    
    print(f"\nstdev:{data[col].std()}")  #Second Moment Business Decision
    
    print(f"\nrange:{data[col].max()-data[col].min()}")  #Second Moment Business Decision
    
    print(f"\nskewness:{data[col].skew()}")  #Third Moment Business Decision
    
    print(f"\nkurtosis:{data[col].kurt()}")  #Fourth Moment Business Decision
    
#draw the histogram plot for all numerical columns
for col in num_cols:
    plt.hist(data[col], bins=20, color='skyblue', edgecolor='black')
    plt.title(f'Histogram of {col}')
    plt.xlabel(col)
    plt.ylabel('sum')
    plt.show()
    
#draw the box plot for all numerical columns
for col in num_cols:
    plt.figure()
    plt.boxplot(data[col])
    plt.title(f"Box Plot of {col}")
    plt.ylabel(col)
    plt.show()
    
import matplotlib.pyplot as plt


#Draw the scatter plot for all columns
scatter_pairs = [
    ("max_capacity_hrs", "utilization_hrs"),
    ("utilization_hrs", "total_cases_day_lab"),
    ("utilization_hrs", "utilization_pct"),
    ("utilization_hrs", "idle_hrs"),
    ("idle_hrs", "technical_downtime_hrs"),
    ("technical_downtime_hrs", "planned_maintenance_hrs"),
    ("workflow_delay_events", "avg_delay_minutes"),
    ("avg_delay_minutes", "workflow_delay_events"),
    ("utilization_hrs", "total_cases_day_lab")
]

for x, y in scatter_pairs:
    plt.figure(figsize=(6,4))
    plt.scatter(data[x], data[y], alpha=0.6)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"{y} vs {x}")
    plt.grid(True)
    plt.show()
    
#Draw the PAIRPLOT for all columns
#*****************MULTIVARIANT PLOTS***********8

#max_capacity_hrs (Capacity vs Usage & Workload)

plt.figure(figsize=(6,4))
plt.scatter(data["utilization_hrs"], data["total_cases_day_lab"],
            c=data["max_capacity_hrs"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Total Cases per Day")
plt.title("Capacity vs Utilization & Workload")
plt.colorbar(label="Max Capacity Hours")
plt.show()


#utilization_hrs (Usage vs Workload & Idle)

plt.figure(figsize=(6,4))
plt.scatter(data["utilization_hrs"], data["total_cases_day_lab"],
            c=data["idle_hrs"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Total Cases per Day")
plt.title("Utilization vs Workload & Idle Time")
plt.colorbar(label="Idle Hours")
plt.show()


#utilization_pct (Efficiency vs Usage & Idle)

plt.figure(figsize=(6,4))
plt.scatter(data["utilization_hrs"], data["idle_hrs"],
            c=data["utilization_pct"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Idle Hours")
plt.title("Efficiency vs Usage & Idle Time")
plt.colorbar(label="Utilization Percentage")
plt.show()


#idle_hrs (Idle vs Usage & Downtime)

plt.figure(figsize=(6,4))
plt.scatter(data["utilization_hrs"], data["idle_hrs"],
            c=data["technical_downtime_hrs"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Idle Hours")
plt.title("Idle Time vs Usage & Downtime")
plt.colorbar(label="Technical Downtime Hours")
plt.show()


#technical_downtime_hrs (Downtime vs Idle & Maintenance)
plt.figure(figsize=(6,4))
plt.scatter(data["idle_hrs"], data["technical_downtime_hrs"],
            c=data["planned_maintenance_hrs"], alpha=0.6)
plt.xlabel("Idle Hours")
plt.ylabel("Technical Downtime Hours")
plt.title("Downtime vs Idle & Maintenance")
plt.colorbar(label="Planned Maintenance Hours")
plt.show()


#planned_maintenance_hrs (Maintenance vs Downtime & Idle)

plt.figure(figsize=(6,4))
plt.scatter(data["technical_downtime_hrs"], data["idle_hrs"],
            c=data["planned_maintenance_hrs"], alpha=0.6)
plt.xlabel("Technical Downtime Hours")
plt.ylabel("Idle Hours")
plt.title("Maintenance Impact on Downtime & Idle")
plt.colorbar(label="Planned Maintenance Hours")
plt.show()

#workflow_delay_events (Delays vs Delay Time & Usage)

plt.figure(figsize=(6,4))
plt.scatter(data["workflow_delay_events"], data["avg_delay_minutes"],
            c=data["utilization_hrs"], alpha=0.6)
plt.xlabel("Workflow Delay Events")
plt.ylabel("Average Delay Minutes")
plt.title("Workflow Delays vs Delay Duration & Usage")
plt.colorbar(label="Utilization Hours")
plt.show()

#avg_delay_minutes (Delay Time vs Events & Idle)

plt.figure(figsize=(6,4))
plt.scatter(data["workflow_delay_events"], data["avg_delay_minutes"],
            c=data["idle_hrs"], alpha=0.6)
plt.xlabel("Workflow Delay Events")
plt.ylabel("Average Delay Minutes")
plt.title("Delay Duration vs Events & Idle Time")
plt.colorbar(label="Idle Hours")
plt.show()


#total_cases_day_lab (Workload vs Usage & Efficiency)

plt.figure(figsize=(6,4))
plt.scatter(data["utilization_hrs"], data["total_cases_day_lab"],
            c=data["utilization_pct"], alpha=0.6)
plt.xlabel("Utilization Hours")
plt.ylabel("Total Cases per Day")
plt.title("Workload vs Usage & Efficiency")
plt.colorbar(label="Utilization Percentage")
plt.show()

#do Auto EDA
import dtale
dtale.show(data)



    
    
    
    