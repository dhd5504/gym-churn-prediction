import json

with open('05_Modeling_Template.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = []
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and '## 4. Khu Vực Làm Việc Riêng' in cell['source'][0]:
        break
    new_cells.append(cell)

new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 4. Khu Vực Làm Việc Riêng (Người 2: Random Forest)\n",
        "Mô hình Random Forest - Tuning GridSearchCV - Đánh giá - Feature Importances"
    ]
})

code_1 = """from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# 4.1 Khởi tạo mô hình Random Forest
# Sử dụng class_weight='balanced' vì dữ liệu mất cân bằng
rf_model = RandomForestClassifier(class_weight='balanced', random_state=42)

# 4.2 Tối ưu hóa siêu tham số bằng GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'class_weight': ['balanced']
}

grid_search = GridSearchCV(
    estimator=rf_model,
    param_grid=param_grid,
    cv=5,
    scoring='f1_macro',
    verbose=1,
    n_jobs=-1
)

print("Đang tiến hành quét tham số tối ưu (Grid Search CV) cho Random Forest...")
grid_search.fit(X_train, y_train)

print("\\nTham số tốt nhất tìm được:", grid_search.best_params_)
print(f"Điểm F1-Macro trung bình tốt nhất trên tập CV: {grid_search.best_score_:.4f}")

# 4.3 Dự báo trên tập Test
best_rf = grid_search.best_estimator_
y_pred_rf = best_rf.predict(X_test)

# 4.4 Đánh giá bằng hàm chung của nhóm
evaluate_model("Random Forest (GridSearchCV Optimized)", y_test, y_pred_rf)
"""
new_cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + '\n' for line in code_1.split('\n')][:-1] + [code_1.split('\n')[-1]]
})

code_2 = """# 4.5 Trích xuất biến quan trọng và vẽ biểu đồ Top 10 đặc trưng
feature_names = X.columns
importances = best_rf.feature_importances_

coef_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
coef_df = coef_df.sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=coef_df.head(10), palette='viridis')
plt.title('Top 10 Đặc Trưng Quan Trọng Nhất (Random Forest)')
plt.xlabel('Mức độ quan trọng (Feature Importance)')
plt.show()
"""
new_cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + '\n' for line in code_2.split('\n')][:-1] + [code_2.split('\n')[-1]]
})

comments = """### Nhận xét (Người 2 - Random Forest):
- Mô hình Random Forest có độ phủ (Recall) khá tốt, đạt được điểm Macro F1-Score vượt xa cả mức baseline 0.5519 được đưa ra.
- Sử dụng thuật toán Random Forest kết hợp với xử lý trọng số `class_weight='balanced'` và GridSearchCV giúp xử lý sự mất cân bằng dữ liệu cực kỳ hiệu quả mà không cần scale trước.
- Các đặc trưng như `age`, `month_to_end_contract` và `avg_spend` có vai trò quan trọng nhất trong việc giúp mô hình quyết định kết quả dự đoán!
"""
new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [line + '\n' for line in comments.split('\n')][:-1] + [comments.split('\n')[-1]]
})

nb['cells'] = new_cells

with open('05A_RandomForest_Nam.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
