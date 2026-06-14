import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# 06. Churn Personas (K-Means Clustering trên tệp Rủi ro)
Notebook này tập trung vào việc dùng K-Means để phân cụm **RIÊNG NHỮNG NGƯỜI ĐÃ NGHỈ TẬP (is_churn=1)**.
Mục tiêu là tìm ra các **Kiểu Rời bỏ (Typology of Churn)** để từ đó phòng Gym biết chính xác phải áp dụng "bài thuốc" nào cho đúng bệnh."""

code_1 = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)"""

text_2 = """## 1. Load và Lọc dữ liệu
Lọc riêng tập khách hàng đã nghỉ tập (hoặc có rủi ro rất cao)."""

code_2 = """# Đọc dữ liệu
df = pd.read_parquet('../data/gym_churn_master_final.parquet')

# LỌC: Chỉ lấy những người đã Churn
df_churn = df[df['is_churn'] == 1].copy()

# Lựa chọn các đặc trưng hành vi (Feature Selection)
features = ['attendance_momentum', 'avg_time_lag', 'total_visits', 'max_streak', 'seniority_days', 'att_rate']
X = df_churn[features].copy()

X = X.fillna(0)

# Chuẩn hóa dữ liệu (Scaling)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Kích thước dữ liệu đưa vào K-Means (Chỉ những người đã nghỉ): {X_scaled.shape}")"""

text_3 = """## 2. Tìm số lượng Cụm (K) tối ưu"""

code_3 = """wcss = []
silhouette_scores = []
K_range = range(2, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

fig, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('Số lượng cụm (K)')
ax1.set_ylabel('WCSS (Inertia)', color=color)
ax1.plot(K_range, wcss, marker='o', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('Silhouette Score', color=color)  
ax2.plot(K_range, silhouette_scores, marker='s', color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Phương pháp Elbow và Silhouette Score trên tệp Churn')
fig.tight_layout()  
plt.show()"""

text_4 = """## 3. Huấn luyện K-Means với K=3
Ta chọn $K=3$ để có 3 nhóm kiểu rời bỏ rõ rệt."""

code_4 = """optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df_churn['Cluster'] = kmeans.fit_predict(X_scaled)

print("Số lượng khách hàng trong mỗi cụm:")
print(df_churn['Cluster'].value_counts().sort_index())"""

text_5 = """## 4. Phân tích Các Kiểu Rời bỏ (Churn Personas)"""

code_5 = """cluster_centroids = df_churn.groupby('Cluster')[features].mean()
cluster_summary = cluster_centroids.copy()
cluster_summary['User_Count'] = df_churn['Cluster'].value_counts().sort_index()

display(cluster_summary.style.background_gradient(cmap='YlOrRd', axis=0))"""

text_6 = """## 5. Trực quan hóa kết quả bằng PCA 2D"""

code_6 = """pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_churn['PCA1'] = X_pca[:, 0]
df_churn['PCA2'] = X_pca[:, 1]

plt.figure(figsize=(10, 8))
sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', palette='viridis', data=df_churn, alpha=0.6)
plt.title('K-Means Clustering (K=3) Các Kiểu Rời bỏ')
plt.show()"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_1),
    nbf.v4.new_code_cell(code_1),
    nbf.v4.new_markdown_cell(text_2),
    nbf.v4.new_code_cell(code_2),
    nbf.v4.new_markdown_cell(text_3),
    nbf.v4.new_code_cell(code_3),
    nbf.v4.new_markdown_cell(text_4),
    nbf.v4.new_code_cell(code_4),
    nbf.v4.new_markdown_cell(text_5),
    nbf.v4.new_code_cell(code_5),
    nbf.v4.new_markdown_cell(text_6),
    nbf.v4.new_code_cell(code_6)
]

with open('notebooks/06_Customer_Segmentation.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook 06_Customer_Segmentation.ipynb generated.")
