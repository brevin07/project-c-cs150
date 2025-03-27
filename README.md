# Cost of Living Dashboard

**Name:** Brevin Tating  
**Course:** CS150

## Region of Focus

**Region:** Southern California (Los Angeles County, Orange County, and Ventura County)  
**Reason for Selection:**  
Southern California is known for its diverse economic landscapes and high cost of living, particularly in housing, utilities, and healthcare. By focusing on this region, the dashboard provides valuable insights into how median incomes compare with various expenses, helping both residents and policymakers make informed decisions.

## Datasets and Data Sources

The dashboard integrates 9 datasets from two primary sources:

### Median Income Data
- `median_income_LA_county.csv`
- `median_income_OC.csv`
- `median_income_ventura_county.csv`

### Cost of Living Data
- **Housing Listing Prices:**  
  - `avg_house_listing_price_LA_county.csv`  
  - `avg_house_listing_price_OC.csv`  
  - `avg_housing_listing_ventura_county.csv`
- **Utilities:**  
  - `avg_elec_price_LA_LB_ANHM.csv` (Electricity)  
  - `avg_price_gas_LA_LB_ANHM_reg.csv` (Gas)
- **Healthcare:**  
  - `healthcare_dataset.csv`

**Data Source Citations:**

- **FRED (Federal Reserve Economic Data):**  
  Website: [https://fred.stlouisfed.org/](https://fred.stlouisfed.org/)  
  License: Data on FRED are generally in the public domain as they are produced by U.S. Government agencies.  
  

  - **Median Income Data:**
    - U.S. Census Bureau, Estimate of Median Household Income for Los Angeles County, CA [MHICA06037A052NCEN], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/MHICA06037A052NCEN, March 26, 2025.
    - U.S. Census Bureau, Estimate of Median Household Income for Ventura County, CA [MHICA06111A052NCEN], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/MHICA06111A052NCEN, March 26, 2025.
    - U.S. Census Bureau, Estimate of Median Household Income for Orange County, CA [MHICA06059A052NCEN], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/MHICA06059A052NCEN, March 26, 2025.
  - **Utilities:**
    - U.S. Bureau of Labor Statistics, Average Price: Electricity per Kilowatt-Hour in Los Angeles-Long Beach-Anaheim, CA (CBSA) [APUS49A72610], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/APUS49A72610, March 26, 2025.
    - U.S. Bureau of Labor Statistics, Average Price: Gasoline, Unleaded Regular (Cost per Gallon/3.785 Liters) in Los Angeles-Long Beach-Anaheim, CA (CBSA) [APUS49A74714], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/APUS49A74714, March 26, 2025.
  - **Housing Listing Prices:**
    - Realtor.com, Housing Inventory: Median Listing Price in Los Angeles County, CA [MEDLISPRI6037], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/MEDLISPRI6037, March 26, 2025.
    - Realtor.com, Housing Inventory: Median Listing Price in Orange County, CA [MEDLISPRI6059], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/MEDLISPRI6059, March 26, 2025.
    - Realtor.com, Housing Inventory: Median Listing Price in Ventura County, CA [MEDLISPRI6111], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/MEDLISPRI6111, March 26, 2025.


- **Kaggle:**  
  Website: [https://www.kaggle.com/](https://www.kaggle.com/)  
  Dataset License: CC0: Public Domain
  Attribution: Provided by Prasad Patil on Kaggle under CC0: Public Domain license

These datasets were selected because together they offer a comprehensive view of the cost of living challenges in Southern California, providing both income and expense perspectives.

## Visualization Strategies (Inspired by Storytelling with Data)

To ensure that the visualization is both effective and engaging, the following strategies have been employed:

- **Responsive Layout:**  
  The dashboard is built using Dash Bootstrap Components (dbc), ensuring that the layout adapts well on both large and small screens.
  
- **Tabbed Navigation:**  
  Content is organized into three tabs ("Learn", "Play", and "Raw Data") for context, interactive exploration, and raw data access.
  
- **Interactive Components:**  
  The dashboard includes input components (radio buttons, sliders, dropdowns, and buttons) to allow users to filter and dynamically update the visualizations.
  
- **Clear Visual Differentiation:**  
  Distinct colors, line styles (solid for expenses, dashed for salary traces), and annotations (hover text and legends) are used to improve readability and storytelling.
  
- **Multiple Visualizations:**  
  Two main visualizations are provided:  
  1. A line graph showing annual costs, median income, and a dynamic "Selected Salary" (which, if a career is chosen, displays the salary trend over the years).  
  2. A yearly summary bar graph that compares the average annual salary from the data, user-selected salary, and combined expenses for a selected year.

## Example Scenarios

Exploring this dashboard can yield multiple insights. For example:

1. **Residential Affordability Analysis:**  
   A potential homebuyer can compare median incomes with housing costs (converted to annual mortgage payments) to determine which county offers a better balance between income and housing affordability.

2. **Policy Evaluation:**  
   Local government officials can explore how changes in utility prices and healthcare costs over time compare with median incomes. This can inform policies aimed at reducing the cost burden on residents.

3. **Career and Financial Planning:**  
   A jobseeker can use the dashboard to explore how different career paths (with dynamic salary trends from 2020 to 2023) compare against living expenses in various counties, helping them make an informed career decision relative to local costs.

## Conclusion

This Cost of Living Dashboard provides an interactive, responsive platform for exploring how various economic factors impact residents in Southern California. By combining data from FRED and Kaggle, and leveraging dynamic visualizations and input components, the dashboard offers actionable insights for homebuyers, policymakers, and career seekers alike.

Data source citations, appropriate licensing, and thorough attributions are included to ensure transparency and compliance with data usage guidelines.

