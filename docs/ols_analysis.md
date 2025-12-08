# OLS Regression Analysis: Determinants of Fixed Broadband Speed by Census Tract

## Executive Summary

This analysis examines the relationship between household income, geographic classification, and fixed broadband download speeds at the census tract level using Q1 2022 data. The model includes 82,249 observations with state, county, and urban classification fixed effects.

**Key Finding:** Geography—not income—is the dominant predictor of internet speed. The urban-rural divide accounts for speed differences of up to 91 Mbps, while doubling household income yields only ~6.5 Mbps improvement.

---

## Model Specification

```
avg_d_kbps_fixed ~ median_income + C(urban_core_type) + C(state) + C(county)
```

| Specification      | Value                               |
| ------------------ | ----------------------------------- |
| Dependent Variable | Average fixed download speed (kbps) |
| Observations       | 82,249                              |
| Model Parameters   | 362                                 |
| Covariance Type    | HC3 (heteroskedasticity-robust)     |

---

## Model Fit Statistics

| Metric             | Value       | Interpretation                                      |
| ------------------ | ----------- | --------------------------------------------------- |
| R-squared          | 0.515       | Model explains 51.5% of variance in download speeds |
| Adjusted R-squared | 0.513       | Adjusted for number of predictors                   |
| F-statistic        | 0.555       | ⚠️ Problematic (see diagnostics)                     |
| Prob (F-statistic) | 0.456       | ⚠️ Not significant at conventional levels            |
| Log-Likelihood     | -9.96 × 10⁵ | —                                                   |
| AIC                | 1.993 × 10⁶ | —                                                   |
| BIC                | 1.997 × 10⁶ | —                                                   |

---

## Primary Coefficients of Interest

### Income Effect

| Variable            | Coefficient | Std. Error | z     | P>\|z\| | 95% CI          |
| ------------------- | ----------- | ---------- | ----- | ------- | --------------- |
| median_income (log) | 9,329.9     | 364.4      | 25.60 | 0.000   | [8,616, 10,044] |

**Interpretation:** Since income is log-transformed:
- **10% increase in income** → +890 kbps (~0.9 Mbps faster)
- **Doubling income** → +6,467 kbps (~6.5 Mbps faster)

The income effect is statistically significant but economically modest relative to geographic factors.

### Urban-Rural Classification

Reference category: **Metro Core**

| Classification  | Coefficient | Std. Error | z       | P>\|z\| | Effect (Mbps) |
| --------------- | ----------- | ---------- | ------- | ------- | ------------- |
| Metro Core      | (baseline)  | —          | —       | —       | 0             |
| Micro Core      | -26,300     | 711        | -36.99  | 0.000   | **-26 Mbps**  |
| Small Town Core | -47,750     | 1,221      | -39.10  | 0.000   | **-48 Mbps**  |
| Rural           | -90,970     | 529        | -172.07 | 0.000   | **-91 Mbps**  |

**Interpretation:** Holding income and location constant:
- Rural tracts average **91 Mbps slower** than metro core tracts
- Small town tracts average **48 Mbps slower** than metro core tracts
- Micropolitan tracts average **26 Mbps slower** than metro core tracts

The urban-rural hierarchy is stark and precisely estimated (all p < 0.001).

---

## State Fixed Effects

Reference category: **Alabama (FIPS 01)**

### Fastest States (Relative to Alabama)

| Rank | State         | FIPS | Coefficient | Effect (Mbps) | P-value |
| ---- | ------------- | ---- | ----------- | ------------- | ------- |
| 1    | New Jersey    | 34   | +34,940     | +35           | <0.001  |
| 2    | Delaware      | 10   | +33,590     | +34           | <0.001  |
| 3    | New Hampshire | 33   | +32,230     | +32           | <0.001  |
| 4    | Rhode Island  | 44   | +24,720     | +25           | <0.001  |
| 5    | Maryland      | 24   | +23,140     | +23           | <0.001  |
| 6    | Tennessee     | 47   | +21,100     | +21           | <0.001  |

### Slowest States (Relative to Alabama)

| Rank | State       | FIPS | Coefficient | Effect (Mbps) | P-value |
| ---- | ----------- | ---- | ----------- | ------------- | ------- |
| 1    | Puerto Rico | 72   | -107,100    | -107          | <0.001  |
| 2    | Idaho       | 16   | -46,300     | -46           | <0.001  |
| 3    | Wyoming     | 56   | -45,880     | -46           | <0.001  |
| 4    | New Mexico  | 35   | -43,460     | -43           | <0.001  |
| 5    | Montana     | 30   | -42,730     | -43           | <0.001  |
| 6    | Iowa        | 19   | -33,060     | -33           | <0.001  |

### States Not Significantly Different from Alabama (p > 0.05)

- District of Columbia (11)
- Florida (12)
- Indiana (18)
- Kentucky (21)
- Maine (23)
- Mississippi (28)
- North Dakota (38)
- Vermont (50)
- West Virginia (54)

---

## County Effects

The model includes 309 county fixed effects. Selected notable effects:

### Largest Negative County Effects

| County FIPS | Coefficient | Effect (Mbps) | P-value |
| ----------- | ----------- | ------------- | ------- |
| 461         | -112,300    | -112          | <0.001  |
| 455         | -111,400    | -111          | <0.001  |
| 503         | -106,000    | -106          | <0.001  |
| 750         | -104,000    | -104          | <0.001  |
| 483         | -104,100    | -104          | <0.001  |

These represent severely underserved counties with speeds more than 100 Mbps below the reference county.

---

## Diagnostic Concerns

### 1. Severe Multicollinearity

| Indicator           | Value        | Threshold | Assessment           |
| ------------------- | ------------ | --------- | -------------------- |
| Condition Number    | 6.88 × 10¹⁴  | <30       | ⛔ **Critical**       |
| Smallest Eigenvalue | 2.19 × 10⁻²³ | —         | Near-singular matrix |

**Problem:** The model includes both state and county fixed effects, but counties nest within states. This creates perfect or near-perfect collinearity. Evidence includes:
- Connecticut (FIPS 09) coefficient: 9.13 × 10¹⁴ with SE of 1.23 × 10¹⁵
- Several county coefficients with SEs in the 10⁷ range
- F-statistic not significant despite highly significant individual coefficients

**Recommendation:** Remove state fixed effects and retain only county fixed effects, OR cluster standard errors at county level without county dummies:

```python
# Option A: County FE only
model = smf.ols('avg_d_kbps_fixed ~ median_income + C(urban_core_type) + C(county)', 
                data=df).fit(cov_type='HC3')

# Option B: State FE with clustered SEs at county
model = smf.ols('avg_d_kbps_fixed ~ median_income + C(urban_core_type) + C(state)', 
                data=df).fit(cov_type='cluster', cov_kwds={'groups': df['county_fips']})
```

### 2. Spatial Autocorrelation

| Indicator     | Value | Ideal | Assessment                 |
| ------------- | ----- | ----- | -------------------------- |
| Durbin-Watson | 1.245 | ~2.0  | ⚠️ Positive autocorrelation |

Neighboring tracts have correlated residuals. Even with county fixed effects, within-county spatial dependence persists.

### 3. Non-Normal Residuals

| Test        | Statistic | P-value | Assessment              |
| ----------- | --------- | ------- | ----------------------- |
| Omnibus     | 1,473.9   | 0.000   | Reject normality        |
| Jarque-Bera | 3,046.6   | 0.000   | Reject normality        |
| Skewness    | 0.034     | —       | Minimal                 |
| Kurtosis    | 3.940     | —       | Fat tails (leptokurtic) |

With n = 82,249, OLS estimates remain consistent, but confidence intervals may be unreliable. Consider log-transforming the dependent variable.

---

## Substantive Interpretation

### The Digital Divide is Geographic, Not Economic

To illustrate the relative magnitude of effects:

| Scenario                        | Speed Change |
| ------------------------------- | ------------ |
| Move from Rural to Metro Core   | +91 Mbps     |
| Move from Alabama to New Jersey | +35 Mbps     |
| Double household income         | +6.5 Mbps    |

A rural household would need to increase income by approximately **14x** to offset the rural penalty through income alone—an impossibility for most families.

### Policy Implications

1. **Infrastructure investment** in rural and underserved areas would have far greater impact than income-based subsidies
2. **State-level variation** suggests policy and regulatory environments matter
3. **Puerto Rico** faces a 107 Mbps deficit requiring targeted intervention

---

## Recommendations for Model Improvement

1. **Fix multicollinearity:** Use county OR state fixed effects, not both
2. **Address spatial autocorrelation:** Consider spatial lag/error models (PySAL/spreg)
3. **Add predictors:** ISP competition, fiber availability, population density
4. **Log-transform DV:** May improve residual normality and provide elasticity interpretation
5. **Report separately:** Present urban effects and geographic effects in separate tables for clarity

---

## Appendix: Model Output

```
Dep. Variable:       avg_d_kbps_fixed   R-squared:                       0.515
Model:                            OLS   Adj. R-squared:                  0.513
No. Observations:               82249   Covariance Type:                  HC3
Df Model:                         362   Condition No.:                6.88e+14

Key Coefficients:
                                        coef      std err       P>|z|
---------------------------------------------------------------------------
Intercept                           1.244e+05     4495.877      0.000
C(urban)[T.Micro core]             -2.630e+04      711.084      0.000
C(urban)[T.Rural]                  -9.097e+04      528.674      0.000
C(urban)[T.Small town core]        -4.775e+04     1221.129      0.000
median_income                       9329.9180      364.389      0.000

Diagnostics:
  Durbin-Watson:     1.245
  Omnibus:           1473.876 (p=0.000)
  Jarque-Bera:       3046.581 (p=0.000)

Notes:
[1] Standard Errors are heteroscedasticity robust (HC3)
[2] Severe multicollinearity detected - design matrix near-singular
```

---

*Analysis conducted December 2025. Data source: FCC/Ookla speed test data, Q1 2022.*