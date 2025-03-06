import os.path
import pandas as pd
import matplotlib.pyplot as plt

# Indstiller til læsbart float-format i pandas
pd.options.display.float_format = '{:.2f}'.format

# 1a.
housing_prices = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/", "DKHousingPricesSample100k.csv"))
# 1b.
print(housing_prices.head(10))

# 2a.
regional_prices = housing_prices.groupby("region")
# 2b.
avg_regional_prices = regional_prices["purchase_price"].mean()
# 2c.
print(avg_regional_prices)

# 3a-b.
regional_house_type_prices = housing_prices.groupby(["house_type", "region"])
# 3c.
avg_regional_house_type_prices = regional_house_type_prices["purchase_price"].mean()
# 3d.
# Matplotlib er indbygget i Pandas, så man kan plotte direkte herigennem
# Unstackes for at udskille i de forskellige grupperinger på grafen
bar_chart = avg_regional_house_type_prices.unstack().plot.bar()
# Man kunne egentlig definere title og labels etc. direkte som parametre i ovenstående funktion, men så kan man ikke justere size, style etc. uden dobbeltkonfekt
plt.title("Average purchase prices of different house types across regions", size="x-large", weight="bold")
plt.xlabel("House types", size="large")
plt.ylabel("Average purchase price (in DKK)", size="large")
plt.legend(title="Region")

# Label på hver søjle (det er næsten CSS lol)
for container in bar_chart.containers:
    bar_chart.bar_label(
        container,
        fmt="{:,.0f}",
        size="small",
        color="white",
        alpha=0.8,
        rotation=-90,
        position=(-1.5, -47.5)
    )

# Formatering af akser
ax = plt.gca()
ax.tick_params(axis="both", labelsize="small", labelrotation=0)
# Ingen direkte måde at sætte ticklabel fontstyle på i tick_params, så er nødt til at gendefinere xticks med nuværende værdier og labels:
xticks, xticklabels, yticks = ax.get_xticks(), ax.get_xticklabels(), ax.get_yticks()
ax.set_xticks(xticks, xticklabels, fontstyle="italic")
# I API'en kan man ændre fra videnskabelig notation til fulde tal med plt.gca().ticklabel_format(axis="y", style="plain"), men her kan man så ikke formatere tusindtalsseparatorerne, så endnu engang gendefinerer jeg:
ax.set_yticks(yticks, [f"{x:,.0f}" for x in yticks], fontstyle="italic") # f-streng evt. fulgt af ".replace(',', '.')" for dansk format
ax.yaxis.minorticks_on()

# Gitterlinjer
# Gitteret tegnes af en eller anden grund ikke under grafen som standard
ax.set_axisbelow(True)
plt.grid(True, "major", "y")

plt.show()

# 4.
