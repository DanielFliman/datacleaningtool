import csv
from collections import Counter

def analyze_data(data):
    # Analyze the data to identify issues, such as missing values or duplicates
    issues = {}
    num_rows = len(data)
    for column in data[0].keys():
        # Check for missing values
        num_missing = sum([row[column] == "" for row in data])
        if num_missing > 0:
            issues[f"Missing values in {column}"] = num_missing
        
        # Check for duplicates
        values = [row[column] for row in data]
        counter = Counter(values)
        num_duplicates = sum([count > 1 for count in counter.values()])
        if num_duplicates > 0:
            issues[f"Potential duplicates in {column}"] = num_duplicates
            for value, count in counter.items():
                if count > 1:
                    rows_with_value = [i+2 for i, row in enumerate(data) if row[column] == value]
                    if rows_with_value:
                        key = f"  - {value} ({count} occurrences): rows {', '.join(map(str, rows_with_value))}"
                        if key in issues:
                            issues[key] += 1
                        else:
                            issues[key] = 1
    
    # Check for rows with all missing values
    num_rows_all_missing = sum([all(row.values()) == "" for row in data])
    if num_rows_all_missing > 0:
        issues["Rows with all missing values"] = num_rows_all_missing
    
    # Return the issues
    return issues


def suggest_cleaning_steps(issues):
    # Suggest cleaning and preprocessing steps based on the identified issues
    steps = []
    if "Potential duplicates" in issues:
        steps.append("Remove duplicates")
    if "Missing values" in issues:
        steps.append("Fill in missing values")
    return steps

def apply_cleaning_steps(data, steps):
    # Apply the selected cleaning and preprocessing steps
    for step in steps:
        if step == "Remove duplicates":
            values = [row.values() for row in data]
            unique_values = list(set([tuple(row) for row in values]))
            data = [dict(zip(data[0].keys(), row)) for row in unique_values]
        elif step == "Fill in missing values":
            for row in data:
                for key in row.keys():
                    if row[key] == "":
                        if key in data[0].keys():
                            row[key] = [r[key] for r in data if r[key] != ""][0]
    # Return the cleaned data
    return data

def write_data(data, filename):
    # Write the cleaned data to a new CSV file
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    # Prompt the user for the filename of the raw dataset
    filename = input("Enter the filename of the raw dataset (CSV format): ")
    
    # Read the data
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    
    # Analyze the data
    issues = analyze_data(data)
    if len(issues) == 0:
        print("No issues found in the data.")
    else:
        print("Issues found in the data:")
        for issue, count in issues.items():
            print(f"- {issue}: {count}")
            if issue == "Potential duplicates":
                print("\nPotential duplicates found in the following columns:")
                for subissue, subcount in issues[issue].items():
                    print(f"\n{subissue} ({subcount} values):")
                    for value in subissue.split(":"):
                        rows_with_value = [i+2 for i, row in enumerate(data) if row[subissue.split(":")[0]] == value]
                        print(f"  - {value} ({len(rows_with_value)} rows): {', '.join(map(str, rows_with_value))}")
    
    # Suggest cleaning and preprocessing steps
    steps = suggest_cleaning_steps(issues)
    if len(steps) == 0:
        print("No cleaning and preprocessing steps suggested.")
    else:
        print("\nCleaning and preprocessing steps suggested:")
        for i, step in enumerate(steps):
            print(f"{i+1}. {step}")
        
        # Ask the user to select the cleaning and preprocessing steps to apply
        selected_steps = input("Enter the numbers of the cleaning and preprocessing steps to apply (separated by commas): ")
        selected_steps = [int(step) for step in selected_steps.split(",")]
        selected_steps = [steps[i-1] for i in selected_steps]
        
        # Apply the selected cleaning and preprocessing steps
        cleaned_data = apply_cleaning_steps(data, selected_steps)
        
        # Write the cleaned data to a new CSV file
        cleaned_filename = f"cleaned_{filename}"
        write_data(cleaned_data, cleaned_filename)
        print(f"Cleaned data written to {cleaned_filename}")




if __name__ == "__main__":
    main()