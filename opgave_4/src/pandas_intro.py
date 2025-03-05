import os.path
import pandas as pd

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
