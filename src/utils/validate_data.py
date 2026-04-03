import pandas as pd
from typing import Tuple, List

def validate_telco_data(df) -> Tuple[bool, List[str]]:
    """
    Comprehensive data validation for Telco Customer Churn dataset using pandas.
    """
    print("🔍 Starting data validation with Pandas...")
    failed_expectations = []
    
    # === SCHEMA VALIDATION - ESSENTIAL COLUMNS ===
    required_cols = [
        "customerID", "gender", "Partner", "Dependents", "PhoneService",
        "InternetService", "Contract", "tenure", "MonthlyCharges", "TotalCharges"
    ]
    for col in required_cols:
        if col not in df.columns:
            failed_expectations.append(f"Missing col: {col}")
            
    if "customerID" in df.columns and df["customerID"].isnull().any():
        failed_expectations.append("customerID contains nulls")

    # === BUSINESS LOGIC VALIDATION ===
    if "gender" in df.columns and not df["gender"].isin(["Male", "Female"]).all():
        failed_expectations.append("Invalid gender")
        
    for col in ["Partner", "Dependents", "PhoneService"]:
        if col in df.columns and not df[col].isin(["Yes", "No"]).all():
            failed_expectations.append(f"Invalid {col}")
            
    if "Contract" in df.columns and not df["Contract"].isin(["Month-to-month", "One year", "Two year"]).all():
        failed_expectations.append("Invalid Contract")

    if "InternetService" in df.columns and not df["InternetService"].isin(["DSL", "Fiber optic", "No"]).all():
        failed_expectations.append("Invalid InternetService")

    # === NUMERIC RANGE VALIDATION ===
    if "tenure" in df.columns and (df["tenure"].dropna() < 0).any():
        failed_expectations.append("tenure < 0")
    if "MonthlyCharges" in df.columns and (df["MonthlyCharges"].dropna() < 0).any():
        failed_expectations.append("MonthlyCharges < 0")
        
    # We copy df for total charges check
    val_df = df.copy()
    val_df['TotalCharges'] = pd.to_numeric(val_df['TotalCharges'], errors='coerce').fillna(0)
    if (val_df["TotalCharges"] < 0).any():
        failed_expectations.append("TotalCharges < 0")

    # === STATISTICAL VALIDATION ===
    if "tenure" in df.columns and (df["tenure"].dropna() > 120).any():
        failed_expectations.append("tenure > 120")
    if "MonthlyCharges" in df.columns and (df["MonthlyCharges"].dropna() > 200).any():
        failed_expectations.append("MonthlyCharges > 200")
        
    if "tenure" in df.columns and df["tenure"].isnull().any():
        failed_expectations.append("Null tenure")
    if "MonthlyCharges" in df.columns and df["MonthlyCharges"].isnull().any():
        failed_expectations.append("Null MonthlyCharges")

    # === DATA CONSISTENCY CHECKS ===
    if "MonthlyCharges" in df.columns:
        inconsistent = (val_df["TotalCharges"] < val_df["MonthlyCharges"]).sum()
        if inconsistent / len(val_df) > 0.05:
            failed_expectations.append("TotalCharges < MonthlyCharges in >5% of rows")

    total_checks = 13
    failed_checks = len(failed_expectations)
    passed_checks = total_checks - failed_checks
    
    success = failed_checks == 0
    if success:
        print(f"✅ Data validation PASSED: {passed_checks}/{total_checks} checks successful")
    else:
        print(f"❌ Data validation FAILED: {failed_checks}/{total_checks} checks failed")
        print(f"   Failed expectations: {failed_expectations}")
    
    return success, failed_expectations
