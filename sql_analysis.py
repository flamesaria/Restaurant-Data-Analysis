import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
os.makedirs("plots", exist_ok=True)

sns.set(style="whitegrid")

conn = sqlite3.connect("restaurants.db")

# Top 10 restaurants by rating
query = """
SELECT name, rating, review_count
FROM restaurants
ORDER BY rating DESC, review_count DESC
LIMIT 10
"""

df = pd.read_sql_query(query, conn)

print("Top 10 restaurants by rating:")
print(df.to_string(index=False))

# Number of restaurants by price category
query1 = '''
SELECT price, COUNT (*) 
FROM restaurants
WHERE price IS NOT NULL
GROUP BY price
ORDER BY price
'''

price_map = {
    "$": "Cheap",
    "$$": "Moderate",
    "$$$": "Expensive",
    "$$$$": "Luxury"
}

df1 = pd.read_sql_query(query1, conn)

df1["price_clean"] = df1["price"].map(price_map)

print("Number of restaurants by price category:")
print(df1.to_string(index=False))


# Average rating for each category
query2 = '''
SELECT category, ROUND(AVG(rating), 1) as 'average rating'
FROM restaurants
GROUP BY category
'''

df2 = pd.read_sql_query(query2, conn)

print("Average rating for each category:")
print(df2.to_string(index=False))


# Number of restaurants in each area
zip_to_district = {
    "00": "Śródmieście",
    "01": "Wola",
    "02": "Ochota",
    "03": "Praga-Północ",
    "04": "Praga-Południe",
    "05": "Wawer",
    "06": "Targówek",
    "07": "Rembertów",
    "08": "Wesoła",
    "09": "Białołęka",
    "10": "Bielany",
    "11": "Żoliborz",
    "12": "Mokotów",
    "13": "Ursynów",
    "14": "Wilanów",
    "15": "Ursus",
    "16": "Bemowo"
}

district_to_coords = {
    "Śródmieście": (52.2297, 21.0122),
    "Wola": (52.2356, 20.9784),
    "Ochota": (52.2196, 20.9824),
    "Praga-Północ": (52.2560, 21.0381),
    "Praga-Południe": (52.2419, 21.0825),
    "Wawer": (52.1950, 21.1856),
    "Targówek": (52.2846, 21.0542),
    "Rembertów": (52.2568, 21.1741),
    "Wesoła": (52.2557, 21.2613),
    "Białołęka": (52.3222, 21.0327),
    "Bielany": (52.2912, 20.9356),
    "Żoliborz": (52.2720, 20.9780),
    "Mokotów": (52.2001, 21.0346),
    "Ursynów": (52.1486, 21.0497),
    "Wilanów": (52.1650, 21.0903),
    "Ursus": (52.2000, 20.8655),
    "Bemowo": (52.2519, 20.9083)
}

query3 = '''
SELECT SUBSTR(zip_code, 1, 2) as "postal area", COUNT(*) as "restaurant count"
FROM restaurants
WHERE zip_code IS NOT NULL
GROUP BY "postal area"
ORDER BY "postal area"
'''

df3 = pd.read_sql_query(query3, conn)
conn.close()

df3["district"] = df3["postal area"].map(zip_to_district)
df3 = df3.dropna(subset=["district"])
df3 = df3[["district", "restaurant count"]].sort_values(by="restaurant count", ascending=False)
df3["latitude"] = df3["district"].map(lambda x: district_to_coords.get(x, (None, None))[0])
df3["longitude"] = df3["district"].map(lambda x: district_to_coords.get(x, (None, None))[1])

print("The number of restaurants in each area:")
print(df3.to_string(index=False))

try:
    plt.figure(figsize=(10, 6))
    ratings = df.sort_values("rating", ascending=True)
    plt.barh(ratings["name"], ratings["rating"], color="skyblue")
    plt.title("Top-10 Restaurants by Rating")
    plt.xlabel("Rating")
    plt.ylabel("Restaurant")
    plt.xlim(4.7, 5)
    plt.tight_layout()
    plt.savefig("plots/plot_top10_rating.png")
    plt.close()
    print("✅ plot_top10_rating saved")
except Exception as e:
    print("❌ Error in plot_top10_rating:", e)

try:
    plt.figure(figsize=(8, 5))
    sns.barplot(x="price_clean", y="COUNT (*)", data=df1, palette="viridis")
    plt.title("Number of Restaurants by Price Category")
    plt.xlabel("Price Category")
    plt.ylabel("Number of Restaurants")
    plt.tight_layout()
    plt.savefig("plots/plot_by_price.png")
    plt.close()
    print("✅ plot_by_price saved")
except Exception as e:
    print("❌ Error in plot_by_price:", e)

try:
    plt.figure(figsize=(10, 6))
    sns.barplot(x="average rating", y="category", data=df2.sort_values("average rating", ascending=False), palette="coolwarm")
    plt.title("Average Rating by Category")
    plt.xlabel("Average Rating")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig("plots/plot_avg_rating_by_category.png")
    plt.close()
    print("✅ plot_avg_rating_by_category saved")
except Exception as e:
    print("❌ Error in plot_avg_rating_by_category:", e)

try:
    plt.figure(figsize=(10, 6))
    districts = df3.sort_values("restaurant count", ascending=True)
    plt.barh(districts["district"], districts["restaurant count"], color="salmon")
    plt.title("Number of Restaurants by District")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("District")
    plt.tight_layout()
    plt.savefig("plots/plot_restaurants_by_district.png")
    plt.close()
    print("✅ plot_restaurants_by_district saved")
except Exception as e:
    print("❌ Error in plot_restaurants_by_district:", e)

df.to_csv("top_10_restaurants.csv", index=False)
df1.to_csv("restaurants_by_price.csv", index=False)
df2.to_csv("average_rating_by_category.csv", index=False)
df3.to_csv("restaurants_by_district.csv", index=False)
