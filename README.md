# XAI - Loan Approval

## Description

**XAI - Loan Approval** is a showcase of Explainable AI (XAI) applied to a loan application using the dataset from Lending Club. 
The project utilizes SHAP (SHapley Additive exPlanations) for model interpretability and explanation, providing insights into the loan approval process.

## Installation

To run this project, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a new Conda environment and install the required dependencies using the following command:

   ```bash
   conda create --name xai_loan_approval --file requirements.txt
   ```

   This will create a Conda environment named `xai_loan_approval` and install all the necessary packages specified in the `requirements.txt` file.

4. Activate the Conda environment:

   ```bash
   conda activate xai_loan_approval
   ```
   
## Usage

After activating the Conda environment, you can run the project using the following command:

```
python app.py
```

## Project Structure

The project directory structure is as follows:

- **Jupyter**: Contains Jupyter Notebook files and datasets.
  - **Datasets**: Directory containing dataset files.
    - `LCDataDictionary.xlsx`: Data dictionary for the loan dataset.
    - `accepted_2007_to_2018Q4.csv.gz`: Accepted loan data.
    - `rejected_2007_to_2018Q4.csv.gz`: Rejected loan data.
    - **states**: Directory containing state-related data.
      - `cost-of-living-index-by-state-[updated-june-2023].csv`: Cost of living index by state.
      - `state-abbrevs.csv`: State abbreviations.
  - `LendingClub.ipynb`: Jupyter Notebook with project code.
  - `X.csv`: Dataset file containing features values.
  - `y.csv`: Dataset file containing loan status.
  - `catboost_model.cbm`: Pre-trained CatBoost model.
  - **images**: Directory for project images.

- `README.md`: This file.

- `app.py`: Python script for running the web application.

- `helper.py`: Python script containing functions for loan data preprocessing, predictions, model explanations, and visualization.

- `requirements.txt`: List of required Python packages.

- **resources**: Directory containing project resources.
  - `inputs.yaml`: YAML file with input features information.

- **static**: Directory for static web assets.
  - `script.js`: JavaScript code for the web application.
  - `style.css`: CSS styles for the web application.
  - `summary.png`: Summary Plot from Catboost model.

- **templates**: Directory containing HTML templates for the web application.
  - `dtiModal.html`: HTML template for the DTI (Debt-to-Income) modal.
  - `index.html`: HTML template for the project's homepage.
  - `result.html`: HTML template for displaying application result and its explanation.
