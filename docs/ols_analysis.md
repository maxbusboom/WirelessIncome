# OLS Regression Analysis: Determinants of Fixed Broadband Speed by Census Tract

## Executive Summary

This analysis examines the relationship between household income, population density, geographic classification, and fixed broadband download speeds at the census tract level using Q1 2022 data. The model includes 81,291 observations with county and urban classification fixed effects.

**Key Finding:** Geography—not income—is the dominant predictor of internet speed. The urban-rural divide accounts for speed differences of up to 89 Mbps, while a one standard deviation increase in income yields only ~6 Mbps improvement. Population density has a comparable effect to income.

---

## Model Specification

```
avg_d_kbps_fixed ~ median_income + pop_density + C(urban_core_type) + C(county)
```

| Specification      | Value                               |
| ------------------ | ----------------------------------- |
| Dependent Variable | Average fixed download speed (kbps) |
| Observations       | 81,291                              |
| Model Parameters   | 314                                 |
| Covariance Type    | HC3 (heteroskedasticity-robust)     |

---

## Model Fit Statistics

| Metric             | Value       | Interpretation                                    |
| ------------------ | ----------- | ------------------------------------------------- |
| R-squared          | 0.460       | Model explains 46% of variance in download speeds |
| Adjusted R-squared | 0.458       | Adjusted for number of predictors                 |
| F-statistic        | 428.5       | Model is jointly significant                      |
| Prob (F-statistic) | 0.000       | Highly significant                                |
| Condition Number   | 299         | Acceptable (no severe multicollinearity)          |
| Log-Likelihood     | -9.88 × 10⁵ | —                                                 |
| AIC                | 1.977 × 10⁶ | —                                                 |
| BIC                | 1.980 × 10⁶ | —                                                 |

---

## Primary Coefficients of Interest

### Income Effect

| Variable      | Coefficient | Std. Error | z     | P>\|z\| | 95% CI         |
| ------------- | ----------- | ---------- | ----- | ------- | -------------- |
| median_income | 5,677.0     | 172.4      | 32.93 | 0.000   | [5,339, 6,015] |

**Interpretation:** Income is log-transformed then standardized to z-scores:
- **+1 SD in log(income)** → +5,677 kbps (~5.7 Mbps faster)
- **+2 SD in log(income)** → +11,354 kbps (~11.4 Mbps faster)
- A tract at the 84th percentile of income has ~5.7 Mbps faster internet than one at the 50th percentile

The income effect is statistically significant but economically modest relative to geographic factors.

### Population Density Effect

| Variable    | Coefficient | Std. Error | z     | P>\|z\| | 95% CI         |
| ----------- | ----------- | ---------- | ----- | ------- | -------------- |
| pop_density | 6,454.9     | 197.2      | 32.73 | 0.000   | [6,068, 6,841] |

**Interpretation:** Population density is standardized to z-scores:
- **+1 SD in density** → +6,455 kbps (~6.5 Mbps faster)
- **+2 SD in density** → +12,910 kbps (~12.9 Mbps faster)

Population density has a slightly larger effect than income. This reflects the economics of infrastructure investment—denser areas justify greater capital expenditure per square mile.

### Comparing Income and Density Effects

Because both variables are z-scored, their coefficients are directly comparable:

| Variable      | Coefficient | Effect per SD |
| ------------- | ----------- | ------------- |
| pop_density   | 6,455       | +6.5 Mbps     |
| median_income | 5,677       | +5.7 Mbps     |

Population density has a **14% larger effect** than income on broadband speeds.

### Urban-Rural Classification

Reference category: **Metro Core**

| Classification  | Coefficient | Std. Error | z       | P>\|z\| | Effect (Mbps) |
| --------------- | ----------- | ---------- | ------- | ------- | ------------- |
| Metro Core      | (baseline)  | —          | —       | —       | 0             |
| Micro Core      | -27,030     | 733        | -36.87  | 0.000   | **-27 Mbps**  |
| Small Town Core | -50,340     | 1,270      | -39.65  | 0.000   | **-50 Mbps**  |
| Rural           | -89,440     | 562        | -159.18 | 0.000   | **-89 Mbps**  |

**Interpretation:** Holding income, density, and county constant:
- Rural tracts average **89 Mbps slower** than metro core tracts
- Small town tracts average **50 Mbps slower** than metro core tracts
- Micropolitan tracts average **27 Mbps slower** than metro core tracts

The urban-rural hierarchy is stark and precisely estimated (all p < 0.001). Note that these effects persist even after controlling for population density, indicating that urban classification captures infrastructure investment patterns beyond what density alone explains.

---

## County Fixed Effects

The model includes 311 county fixed effects (reference county omitted). Selected notable effects:

### Counties with Largest Positive Effects (vs. Reference)

| County FIPS | Coefficient | Effect (Mbps) | P-value |
| ----------- | ----------- | ------------- | ------- |
| 036         | +112,500    | +113          | 0.014   |
| 471         | +64,710     | +65           | <0.001  |
| 570         | +61,580     | +62           | 0.001   |
| 530         | +58,570     | +59           | 0.002   |
| 640         | +60,330     | +60           | 0.022   |

### Counties with Largest Negative Effects (vs. Reference)

| County FIPS | Coefficient | Effect (Mbps) | P-value |
| ----------- | ----------- | ------------- | ------- |
| 461         | -92,790     | -93           | <0.001  |
| 455         | -91,730     | -92           | <0.001  |
| 503         | -85,590     | -86           | <0.001  |
| 483         | -84,530     | -85           | <0.001  |
| 750         | -83,120     | -83           | <0.001  |

These severely underserved counties have speeds 80-90+ Mbps below the reference county, representing critical infrastructure gaps.

---

## Effect Size Comparison

To illustrate the relative magnitude of predictors:

| Scenario                           | Speed Change  |
| ---------------------------------- | ------------- |
| Move from Rural to Metro Core      | **+89 Mbps**  |
| Move from worst to best county     | **+205 Mbps** |
| Move from Small Town to Metro Core | **+50 Mbps**  |
| Move from Micro Core to Metro Core | **+27 Mbps**  |
| +1 SD in population density        | **+6.5 Mbps** |
| +1 SD in log(income)               | **+5.7 Mbps** |

**Key insight:** The Rural penalty (-89 Mbps) is equivalent to **15.7 standard deviations** of the income effect. Put another way, a rural tract would need to be nearly 16 SD above average in income to offset the geographic penalty—a statistical impossibility. Geography is destiny.

---

## Diagnostic Assessment

### Multicollinearity

| Indicator        | Value | Threshold | Assessment   |
| ---------------- | ----- | --------- | ------------ |
| Condition Number | 299   | <1,000    | ✅ Acceptable |

Dropping state fixed effects and standardizing continuous variables resolved the multicollinearity from earlier specifications.

### Spatial Autocorrelation

| Indicator     | Value | Ideal | Assessment                         |
| ------------- | ----- | ----- | ---------------------------------- |
| Durbin-Watson | 1.139 | ~2.0  | ⚠️ Positive autocorrelation remains |

Neighboring tracts still have correlated residuals. County fixed effects help but don't fully capture within-county spatial dependence. For publication, consider:
- Clustering standard errors at a finer geographic level
- Spatial lag or spatial error models (PySAL/spreg)

### Residual Normality

| Test        | Statistic | P-value | Assessment          |
| ----------- | --------- | ------- | ------------------- |
| Omnibus     | 1,389.9   | 0.000   | Reject normality    |
| Jarque-Bera | 2,636.8   | 0.000   | Reject normality    |
| Skewness    | 0.093     | —       | Minimal (near zero) |
| Kurtosis    | 3.863     | —       | Slightly fat tails  |

With n = 81,291, OLS estimates remain consistent by the Central Limit Theorem. The slight positive skew and excess kurtosis suggest some outlier tracts with unusually high or low speeds. Consider:
- Log-transforming the dependent variable for elasticity interpretation
- Winsorizing extreme values

---

## Substantive Interpretation

### The Digital Divide is Fundamentally Geographic

This analysis confirms that internet speed disparities in the United States are primarily determined by where people live, not how much they earn. Three key patterns emerge:

1. **The urban-rural gap is massive and persistent.** Rural tracts are 89 Mbps slower than metro cores even after controlling for income, density, and county. This gap exceeds what most households need for basic broadband (25 Mbps by FCC definition).

2. **Population density matters, but not enough.** Denser areas have faster internet, reflecting infrastructure economics. However, the urban classification effects persist after controlling for density, suggesting that investment decisions follow administrative boundaries and market definitions, not just density gradients.

3. **Income effects are real but small.** Wealthier tracts have modestly faster internet, possibly reflecting ability to pay for premium tiers or correlation with housing stock quality. But the effect is dwarfed by location factors—a one standard deviation income advantage buys only 5.7 Mbps, while rural location costs 89 Mbps.

### Policy Implications

1. **Infrastructure investment** in rural and small-town areas would have far greater impact than income-based subsidies for internet access.

2. **County-level variation** is substantial (205 Mbps spread), suggesting that local regulatory environments, ISP competition, and historical investment patterns matter significantly.

3. **The "last mile" problem** is real—even controlling for density, rural classification carries a large penalty, indicating that sparse population alone doesn't fully explain underinvestment.

---

## Technical Notes

### Variables

| Variable         | Description                                  | Transformation                 |
| ---------------- | -------------------------------------------- | ------------------------------ |
| avg_d_kbps_fixed | Mean fixed broadband download speed by tract | None (kbps)                    |
| median_income    | Tract median household income                | Log-transformed, then z-scored |
| pop_density      | Population per square mile                   | Z-scored (no log transform)    |
| urban_core_type  | RUCA-based classification                    | Categorical (4 levels)         |
| county           | County FIPS code                             | Categorical fixed effects      |

### Standardization

Both continuous predictors are standardized to z-scores (mean = 0, SD = 1), making their coefficients directly comparable. The coefficient represents the change in download speed (kbps) associated with a one standard deviation increase in the predictor.

### Model Comparison

| Specification                                | R²    | Condition No. | F-stat (p)    |
| -------------------------------------------- | ----- | ------------- | ------------- |
| Income + Urban + State + County              | 0.515 | 6.88 × 10¹⁴   | 0.56 (0.456)  |
| Income + Density + Urban + County (z-scored) | 0.460 | 299           | 428.5 (0.000) |

The simpler model (without state effects, with standardized predictors) is preferred due to:
- Resolved multicollinearity
- Significant F-statistic
- Interpretable, comparable coefficients
- Stable coefficient estimates

---

## Appendix: Full Model Output

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       avg_d_kbps_fixed   R-squared:                       0.460
Model:                            OLS   Adj. R-squared:                  0.458
Method:                 Least Squares   F-statistic:                     428.5
Date:                Sun, 07 Dec 2025   Prob (F-statistic):               0.00
Time:                        21:30:32   Log-Likelihood:            -9.8827e+05
No. Observations:               81291   AIC:                         1.977e+06
Df Residuals:                   80976   BIC:                         1.980e+06
Df Model:                         314                                         
Covariance Type:                  HC3                                         

Key Coefficients:
=========================================================================================================
                                            coef    std err          z      P>|z|      [0.025      0.975]
---------------------------------------------------------------------------------------------------------
Intercept                              2.207e+05   1095.160    201.555      0.000    2.19e+05    2.23e+05
C(urban_core_type)[T.Micro core]      -2.703e+04    733.155    -36.872      0.000   -2.85e+04   -2.56e+04
C(urban_core_type)[T.Rural]           -8.944e+04    561.878   -159.175      0.000   -9.05e+04   -8.83e+04
C(urban_core_type)[T.Small town core] -5.034e+04   1269.647    -39.651      0.000   -5.28e+04   -4.79e+04
median_income                          5676.9803    172.412     32.927      0.000    5339.059    6014.901
pop_density                            6454.8773    197.230     32.728      0.000    6068.314    6841.441

Diagnostics:
==============================================================================
Omnibus:                     1389.933   Durbin-Watson:                   1.139
Prob(Omnibus):                  0.000   Jarque-Bera (JB):             2636.785
Skew:                           0.093   Prob(JB):                         0.00
Kurtosis:                       3.863   Cond. No.                         299.
==============================================================================

Notes:
[1] Standard Errors are heteroscedasticity robust (HC3)
```

---

*Analysis conducted December 2025. Data source: Ookla/M-Lab speed test data merged with ACS demographic data, Q1 2022.*