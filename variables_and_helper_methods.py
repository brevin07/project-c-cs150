import pandas as pd

# =============================================================================
# Constants & Helper Functions
# =============================================================================

# Mortgage assumptions
INTEREST_RATE_ANNUAL = 0.0672  # 6.72% annual
MONTHS = 360  # 30 years
INTEREST_RATE_MONTHLY = INTEREST_RATE_ANNUAL / 12
PROPERTY_TAX = 658
INSURANCE = 66

# Gas assumptions
MILES_PER_MONTH = 1258
MPG = 33.5

# Electricity assumptions
KWH_PER_MONTH = 1023

# Healthcare assumption (to get monthly cost)
HEALTHCARE_DIVISOR = 24


def monthly_mortgage(listing_price):
    principal = 0.80 * listing_price
    r = INTEREST_RATE_MONTHLY
    n = MONTHS
    M = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return M + PROPERTY_TAX + INSURANCE


def monthly_gas_cost(gas_price):
    return (gas_price / MPG) * MILES_PER_MONTH


def monthly_elec_cost(elec_price):
    return elec_price * KWH_PER_MONTH


def monthly_healthcare_cost(billing_amount):
    return billing_amount / HEALTHCARE_DIVISOR


def load_csv(path, date_col="observation_date"):
    df = pd.read_csv(path)
    df[date_col] = pd.to_datetime(df[date_col])
    return df
