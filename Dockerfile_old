# Utiliser l'image de base Python
FROM continuumio/miniconda3

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le code de l'application dans le conteneur
COPY dashboard.py .

# Définir un répertoire de données
# VOLUME /app/data

# Installer les dépendances
RUN pip install streamlit geopandas plotly matplotlib ipywidgets pandas

# Exposer le port 8501 (port par défaut de Streamlit)
EXPOSE 8501

# Commande pour exécuter l'application quand le conteneur démarre
CMD ["streamlit", "run", "--server.port", "8501", "dashboard.py"]



# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN pip install pandas scikit-learn streamlit matplotlib seaborn plotly numpy

# CMD streamlit run --server.port $PORT app.py
