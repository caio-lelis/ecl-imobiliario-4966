import numpy as np
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, DateTime, MetaData
from datetime import datetime, timedelta
import random
 
DATABASE_URI = "postgresql+psycopg2://datalake:datalake@localhost:5433/dw_simulado"
 
engine = create_engine(DATABASE_URI)
metadata = MetaData()
 
contratos = Table(
    "contratos",
    metadata,
    Column("id_contrato", Integer, primary_key=True, autoincrement=True),
    Column("data_concessao", DateTime),
    Column("valor_imovel", Float),
    Column("valor_financiado", Float),
    Column("ltv", Float),
    Column("prazo_anos", Integer),
    Column("taxa_juros", Float),
    Column("renda_cliente", Float),
    Column("score_credito", Float),
    Column("idade_cliente", Integer),
    Column("regiao", String),
)
 
metadata.create_all(engine)
 
def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))
 
def generate_contracts(n=50000):
    np.random.seed(42)
    random.seed(42)
 
    start_date = datetime(2015,1,1)
    end_date = datetime(2022,12,31)
 
    records = []
 
    for _ in range(n):
 
        valor_imovel = max(np.random.normal(500000,150000),200000)
        ltv = np.random.uniform(0.5,0.9)
        valor_financiado = valor_imovel * ltv
 
        record = {
            "data_concessao": random_date(start_date,end_date),
            "valor_imovel": float(valor_imovel),
            "valor_financiado": float(valor_financiado),
            "ltv": float(ltv),
            "prazo_anos": int(np.random.choice([20,25,30])),
            "taxa_juros": float(np.random.uniform(0.07,0.12)),
            "renda_cliente": float(max(np.random.normal(12000,4000),4000)),
            "score_credito": float(np.clip(np.random.normal(700,70),400,900)),
            "idade_cliente": int(np.random.randint(25,65)),
            "regiao": random.choice(["Sudeste","Sul","Nordeste","Centro-Oeste"])
        }
 
        records.append(record)
 
    with engine.begin() as conn:
        conn.execute(contratos.insert(), records)
 
generate_contracts()