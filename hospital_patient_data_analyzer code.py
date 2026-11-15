"""
Hospital Patient Data Analyzer
Project: PS No. 16

Required files:
    hospital_patient_analyzer.py
    patients.csv

Install required packages:
    pip install pandas matplotlib

Run:
    python hospital_patient_analyzer.py
"""

import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "patients.csv"


def load_and_clean_data(file_name):
    """Load the CSV file and clean duplicate, missing and invalid values."""
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"\nError: '{file_name}' was not found.")
        print("Keep patients.csv in the same folder as this Python file.")
        return None
    except Exception as error:
        print("\nCould not read the CSV file:", error)
        return None

    # Remove extra spaces from column names and text values.
    df.columns = df.columns.str.strip()

    required_columns = [
        "Patient_ID", "Age", "Gender", "Department",
        "Admit_Date", "Discharge_Date"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print("\nCSV is missing these columns:", ", ".join(missing_columns))
        print("Required columns:", ", ".join(required_columns))
        return None

    # Clean text columns.
    for column in ["Patient_ID", "Gender", "Department"]:
        df[column] = df[column].astype("string").str.strip()

    # Convert age and dates to usable data types.
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df.loc[df["Age"] < 0, "Age"] = pd.NA

    df["Admit_Date"] = pd.to_datetime(df["Admit_Date"], errors="coerce")
    df["Discharge_Date"] = pd.to_datetime(df["Discharge_Date"], errors="coerce")

    # Remove rows missing essential information (Age is handled separately).
    essential_columns = [
        "Patient_ID", "Gender", "Department", "Admit_Date", "Discharge_Date"
    ]
    df = df.dropna(subset=essential_columns)

    # Remove rows with a discharge date before the admission date.
    df = df[df["Discharge_Date"] >= df["Admit_Date"]]

    # Remove duplicate patients, keeping the first record.
    duplicate_count = int(df.duplicated(subset=["Patient_ID"]).sum())
    df = df.drop_duplicates(subset=["Patient_ID"], keep="first").copy()

    # Fill missing/invalid ages with the median age.
    missing_age_count = int(df["Age"].isna().sum())
    if not df["Age"].dropna().empty:
        median_age = df["Age"].median()
        df["Age"] = df["Age"].fillna(median_age)
    else:
        median_age = 0
        df["Age"] = df["Age"].fillna(median_age)
        print("Warning: no valid ages were available; missing ages were set to 0.")

    df["Age"] = df["Age"].round().astype(int)

    # Calculate length of stay in days.
    df["Stay_Days"] = (df["Discharge_Date"] - df["Admit_Date"]).dt.days

    print("\n========== DATA CLEANING SUMMARY ==========")
    print("Duplicate records removed:", duplicate_count)
    print("Missing/invalid ages filled:", missing_age_count)
    print("Valid patient records:", len(df))
    print("===========================================\n")

    return df


def show_department_analysis(df):
    """Option 1: Show department-wise and gender-wise patient counts."""
    print("\n--- Department-wise Patient Count ---")
    department_counts = df.groupby("Department").size()

    for department, count in department_counts.items():
        print(f"{department}: {count}")

    print("Total patients:", len(df))

    print("\n--- Gender-wise Patient Count ---")
    gender_counts = df.groupby("Gender").size()
    for gender, count in gender_counts.items():
        print(f"{gender}: {count}")

    # Bar chart for department-wise patient count.
    department_counts.plot(kind="bar", title="Patients by Department")
    plt.xlabel("Department")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def show_average_stay(df):
    """Option 2: Calculate average length of hospital stay."""
    print("\n--- Average Length of Stay ---")

    average_stay = df["Stay_Days"].mean()

    # Show average stay for each department as well.
    department_stay = df.groupby("Department")["Stay_Days"].mean()

    for department, days in department_stay.items():
        print(f"{department}: {days:.2f} days")

    print(f"Average stay: {average_stay:.2f} days")


def show_stay_and_age_analysis(df):
    """Option 3: Show average stay, age groups and a Matplotlib chart."""
    print("\n--- Stay and Age Group Analysis ---")

    average_stay = df["Stay_Days"].mean()
    print(f"Average stay: {average_stay:.2f} days")

    # Age groups: 0-40, 41-60 and 61+.
    age_groups = pd.cut(
        df["Age"],
        bins=[-1, 40, 60, float("inf")],
        labels=["0-40", "41-60", "61+"]
    )

    age_counts = age_groups.value_counts().reindex(
        ["0-40", "41-60", "61+"], fill_value=0
    )

    print(
        "Age groups: "
        + " | ".join(
            f"{group}: {count}" for group, count in age_counts.items()
        )
    )

    # Matplotlib bar chart.
    age_counts.plot(kind="bar", title="Patients by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def main():
    print("======================================")
    print("     HOSPITAL PATIENT DATA ANALYZER")
    print("======================================")

    patients = load_and_clean_data(CSV_FILE)

    if patients is None:
        return

    if patients.empty:
        print("No valid patient records are available for analysis.")
        return

    while True:
        print("\nChoose an analysis:")
        print("1. Department-wise and gender-wise patient count")
        print("2. Length of hospital stay")
        print("3. Stay and age-group analysis with bar chart")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            show_department_analysis(patients)
        elif choice == "2":
            show_average_stay(patients)
        elif choice == "3":
            show_stay_and_age_analysis(patients)
        elif choice == "4":
            print("\nThank you for using Hospital Patient Data Analyzer!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
