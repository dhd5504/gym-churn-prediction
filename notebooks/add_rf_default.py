import json

with open('05A_RandomForest_Nam.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find where to insert: right before "4.2 Tối ưu hóa siêu tham số bằng GridSearchCV"
cells = nb['cells']
insert_idx = len(cells) - 3 # We know the last three are: grid search, feature importance, comments

# But wait, grid search code is the 3rd from the end.
# Let's search inside the sources.
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code':
        if len(cell['source']) > 0 and 'GridSearchCV' in "".join(cell['source']):
            insert_idx = i
            break

new_code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "from sklearn.ensemble import RandomForestClassifier\n",
        "# Huấn luyện Random Forest mặc định (Không Tuning) để làm cơ sở so sánh\n",
        "rf_default = RandomForestClassifier(class_weight='balanced', random_state=42)\n",
        "rf_default.fit(X_train, y_train)\n",
        "\n",
        "y_pred_default = rf_default.predict(X_test)\n",
        "evaluate_model(\"Random Forest (Default / No Tuning)\", y_test, y_pred_default)\n"
    ]
}

cells.insert(insert_idx, new_code_cell)
nb['cells'] = cells

with open('05A_RandomForest_Nam.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
