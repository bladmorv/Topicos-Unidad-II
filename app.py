import streamlit as st
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from PIL import Image
import base64
import time
import random

# Configuración de Couchbase Capella

COUCHDB_URL = "couchbases://cb.i0ymsakyszrjfaeg.cloud.couchbase.com"
COUCHDB_USERNAME = "dev"
COUCHDB_PASSWORD = "FvS!739zDs37"
COUCHDB_BUCKET = "travel-sample"

# Conexión a Couchbase Capella
auth = PasswordAuthenticator(COUCHDB_USERNAME, COUCHDB_PASSWORD)
cluster = Cluster(COUCHDB_URL, ClusterOptions(auth))
bucket = cluster.bucket(COUCHDB_BUCKET)
collection = bucket.default_collection()

# CSS para interfaz cyberpunk y animación de random bars
st.markdown(
    """
    <style>
    body {
        background-color: #0f0f0f;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3 {
        color: #e600ff;
        text-shadow: 0px 0px 8px #ff00ff, 0px 0px 12px #ff1aff;
    }
    .stButton button {
        background: linear-gradient(45deg, #ff1aff, #1affff);
        color: #ffffff;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        transition: 0.5s;
    }
    .stButton button:hover {
        transform: scale(1.1);
        box-shadow: 0px 0px 10px #ff00ff, 0px 0px 15px #1affff;
    }
    .stFileUploader div {
        background: #1a1a1a;
        color: #ffffff;
        border: 1px solid #ff1aff;
        padding: 5px;
    }
    .report-card {
        background: linear-gradient(135deg, #1a1a1a, #3a3a3a);
        color: #ffffff;
        border: 1px solid #ff00ff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0px 0px 10px #1affff;
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .loading-bar {
        display: inline-block;
        width: 4px;
        height: 20px;
        margin: 0 2px;
        background: linear-gradient(45deg, #ff00ff, #1affff);
        animation: grow 1s infinite;
    }
    @keyframes grow {
        0%, 100% { height: 20px; }
        50% { height: 50px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

def loading_animation():
    """Muestra animación de barras aleatorias."""
    st.markdown("""
        <div style="text-align: center;">
            <div class="loading-bar" style="animation-delay: 0s;"></div>
            <div class="loading-bar" style="animation-delay: 0.2s;"></div>
            <div class="loading-bar" style="animation-delay: 0.4s;"></div>
            <div class="loading-bar" style="animation-delay: 0.6s;"></div>
            <div class="loading-bar" style="animation-delay: 0.8s;"></div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2)  # Simular tiempo de carga

def upload_report(name, surname, district, address, title, description, image):
    """Sube un reporte a Couchbase Capella."""
    try:
        encoded_image = base64.b64encode(image.read()).decode('utf-8')
        report_data = {
            "name": name,
            "surname": surname,
            "district": district,
            "address": address,
            "title": title,
            "description": description,
            "image": encoded_image,
        }
        collection.insert(title, report_data)
        st.success("Reporte enviado exitosamente")
    except Exception as e:
        st.error(f"Error: {e}")

def get_reports():
    """Obtiene reportes almacenados en Couchbase Capella usando N1QL."""
    try:
        query = f"SELECT * FROM `{COUCHDB_BUCKET}`;"
        rows = cluster.query(query)
        return [row[COUCHDB_BUCKET] for row in rows]
    except Exception as e:
        st.error(f"Error al obtener reportes: {e}")
        return []

# Interfaz de Streamlit
st.title("🌐 Informes de Problemas Comunitarios")
st.markdown("### Una experiencia para mejorar tu comunidad 🚀")
st.write("Reporta problemas en tu vecindario con estilo.")

# Formulario para subir reportes
st.markdown("## ✍️ Enviar un Informe")
with st.form("report_form"):
    name = st.text_input("👤 Nombre")
    surname = st.text_input("👤 Apellidos")
    district = st.selectbox("📍 Distrito", [
        "Tacna",
        "Alto de la Alianza",
        "Palca",
        "Calana",
        "Ciudad Nueva",
        "Coronel Gregorio Albarracín Lanchipa",
        "Inclán",
        "La Yarada-Los Palos",
        "Pachía",
        "Pocollay",
        "Sama"
    ])
    address = st.text_input("📍 Dirección exacta", placeholder="Ejemplo: Calle Principal 123")
    title = st.text_input("📌 Título del problema", placeholder="Ejemplo: Bache en la calle principal")
    description = st.text_area("📝 Descripción", placeholder="Describe el problema en detalle...")
    image = st.file_uploader("📷 Sube una imagen del problema", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("🚀 Enviar Reporte")

if submitted:
    if name and surname and district and address and title and description and image:
        loading_animation()
        upload_report(name, surname, district, address, title, description, image)
    else:
        st.warning("Por favor, completa todos los campos.")

# Mostrar reportes existentes
st.markdown("## 🗂️ Reportes Recientes")
reports = get_reports()
for report in reports:
    st.markdown(f"""
    <div class="report-card">
        <h4>{report.get("title", "Sin título")}</h4>
        <p><strong>Nombre:</strong> {report.get("name", "Anónimo")} {report.get("surname", "")}</p>
        <p><strong>Distrito:</strong> {report.get("district", "No especificado")}</p>
        <p><strong>Dirección:</strong> {report.get("address", "Sin dirección")}</p>
        <p>{report.get("description", "Sin descripción")}</p>
        {"<img src='data:image/jpeg;base64," + report["image"] + "' width='100%' style='border-radius:10px;' />" if "image" in report else ""}
    </div>
    """,
    unsafe_allow_html=True)
