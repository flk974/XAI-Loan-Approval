import os

import pandas as pd
import shap
from catboost import (CatBoostClassifier, Pool)
from matplotlib import pyplot as plt

model_dir = 'Jupyter'
states_dataset_dir = os.path.join('Jupyter', 'Datasets', 'states')

model = CatBoostClassifier()
model.load_model(os.path.join(model_dir, 'catboost_model.cbm'))

X = pd.read_csv(os.path.join(model_dir, 'X.csv'))
y = pd.read_csv(os.path.join(model_dir, 'y.csv'))
cat_features = ['purpose']

states_info = pd.read_csv(os.path.join(states_dataset_dir, 'cost-of-living-index-by-state-[updated-june-2023].csv'))
states_abbrevs = pd.read_csv(os.path.join(states_dataset_dir, 'state-abbrevs.csv'))
states_cost_of_living = (
    pd
    .merge(states_info[['2023', 'state']], states_abbrevs, on='state')
    .drop('state', axis=1)
    .rename(columns={'2023': 'state_cost_living', 'abbreviation': 'addr_state'})
)


def preprocess_data(data: dict) -> pd.DataFrame:
    df_in = pd.DataFrame([data])
    features_order = X.columns
    return pd.merge(df_in, states_cost_of_living, on='addr_state').drop('addr_state', axis=1)[features_order]


def predict(preprocessed_data) -> str:
    return model.predict(preprocessed_data)


def get_explainer():
    return shap.TreeExplainer(model)


def get_shap_values(explainer, instance_df, predict_df):
    shap_values = explainer.shap_values(Pool(instance_df, predict_df, cat_features=cat_features))
    return shap_values


def get_summary_plot(explainer, force=False):
    if os.path.isfile('static/summary.png') and not force:
        return 'static/summary.png'
    shap_values = get_shap_values(explainer, X, y)
    shap.summary_plot(shap_values, X, feature_names=X.columns, show=False)
    plt.savefig('static/summary.png')
    return 'static/summary.png'


def get_local_explanations(explainer, instance_df, predict_df):
    shap_values = get_shap_values(explainer, instance_df, predict_df)
    return get_force_plot(explainer, instance_df, shap_values), get_detail_explanation(instance_df, shap_values)


def map_column(column_name: str):
    if column_name == 'purpose':
        return 'Purpose'
    elif column_name == 'loan_amnt':
        return 'Loan Amount'
    elif column_name == 'dti':
        return 'DTI'
    elif column_name == 'emp_length':
        return 'Employment Length'
    elif column_name == 'state_cost_living':
        return "State's Cost of Living (derived from Address State)"
    else:
        return "Unknown feature"


def get_detail_explanation(instance_df, shap_values):
    explanation = ''
    columns = [map_column(column_name) for column_name in instance_df.columns]
    zipped = list(zip(shap_values[0], columns))
    zipped = sorted(zipped, key=lambda x: abs(x[0]), reverse=True)
    for i, (shap_value, feature) in enumerate(zipped[:5], start=1):
        if shap_value < 0:
            explanation += f'\t{i} - Your <b>{feature}</b> had a <span class="positive">positive</span> impact on the output\n'
        elif shap_value > 0:
            explanation += f'\t{i} - Your <b>{feature}</b> had a <span class="negative">negative</span> impact on the output\n'
        else:
            explanation += f'\t{i} - Your <b>{feature}</b> had no impact on the output\n'

    final_explanation = (f"Based on the provided data and our analysis, "
                         f"here's a detailed breakdown of the features sorted by influence:\n"
                         f"{explanation}")
    return final_explanation


def get_force_plot(explainer, instance_df, shap_values):
    shap.initjs()
    force_plot = shap.force_plot(explainer.expected_value, shap_values, instance_df,
                                 feature_names=instance_df.columns, matplotlib=False)
    shap_html = f'<head>{shap.getjs()}</head><body>{force_plot.html()}</body>'
    return shap_html