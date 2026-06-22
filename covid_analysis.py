import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
confirmed = pd.read_csv("time_series_covid19_confirmed_global.csv")

# Preview data
print(confirmed.head())

# Dataset info
print(confirmed.shape)
print(confirmed.describe())


# Find latest date
latest_date = confirmed.columns[-1]

# Top countries
top_countries = confirmed.groupby("Country/Region")[latest_date].sum()

print(top_countries.sort_values(ascending=False).head(10))


# Bar chart
top_10 = top_countries.sort_values(ascending=False).head(10)

plt.figure()
top_10.plot(kind="bar")

plt.title("Top 10 Countries by Confirmed COVID Cases")
plt.xlabel("Country")
plt.ylabel("Confirmed Cases")
plt.xticks(rotation=45)

plt.savefig("top_10_covid_cases.png", bbox_inches="tight")
plt.show()


# US cases over time
us_cases = confirmed[confirmed["Country/Region"] == "US"].iloc[:,4:].sum()

plt.figure()
us_cases.plot(kind="line")

plt.title("COVID Cases Over Time in the US")
plt.xlabel("Date")
plt.ylabel("Confirmed Cases")

plt.savefig("us_covid_cases_over_time.png", bbox_inches="tight")
plt.show()


# World map
country_cases = (
    confirmed.groupby("Country/Region")[latest_date]
    .sum()
    .reset_index()
)

country_cases = country_cases.rename(
    columns={latest_date: "Total Cases"}
)

fig = px.choropleth(
    country_cases,
    locations="Country/Region",
    locationmode="country names",
    color="Total Cases",
    color_continuous_scale="Reds",
    title=f"COVID-19 Total Confirmed Cases by Country as of {latest_date}",
)

fig.write_html("covid_world_map.html")
fig.show()


print("COVID-19 Analysis Complete")
print("Highest case country:", top_countries.idxmax())
print("Highest case count:", top_countries.max())