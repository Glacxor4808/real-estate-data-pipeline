import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('digital_trace.db')

query = """
SELECT location, 
       COUNT(*) as total_ads,
       AVG(Amount_Clean / Area_Clean) as price_per_unit
FROM houses
WHERE Amount_Clean IS NOT NULL 
  AND Area_Clean IS NOT NULL 
  AND location IS NOT NULL
GROUP BY location
HAVING total_ads > 100 -- Берем только крупные города для точности
ORDER BY price_per_unit DESC
LIMIT 10
"""

df_analysis = pd.read_sql(query, conn)

plt.figure(figsize=(12, 7))
plt.barh(df_analysis['location'], df_analysis['price_per_unit'], color='#004a99')
plt.xlabel('Средняя цена за единицу площади')
plt.title('Топ-10 самых дорогих локаций (на основе чистых данных)')
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig('price_analysis.png')
plt.show()

conn.close()