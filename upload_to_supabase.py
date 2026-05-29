import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import math

# Cargar variables de entorno
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

print("Iniciando subida a Supabase...")

# Subir cobertura_movil (400k+ filas en lotes)
print("Subiendo cobertura_movil_clean.csv...")
df_cm = pd.read_csv('cobertura_movil_clean.csv')
# Reemplazar NaN por None para JSON compliance
df_cm = df_cm.where(pd.notnull(df_cm), None)

records = df_cm.to_dict('records')
batch_size = 5000
total_batches = math.ceil(len(records) / batch_size)

for i in range(total_batches):
    batch = records[i * batch_size : (i + 1) * batch_size]
    try:
        supabase.table('cobertura_movil').insert(batch).execute()
        print(f"Lote {i+1}/{total_batches} subido exitosamente.")
    except Exception as e:
        print(f"Error en lote {i+1}: {e}")
        break

print("¡Subida completada!")
