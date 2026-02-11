import numpy as np
from sqlalchemy import (
    create_engine, Table, Column, Integer, Float,
    DateTime, MetaData, ForeignKey, select
)
from datetime import datetime
from dateutil.relativedelta import relativedelta
 
DATABASE_URI = "postgresql+psycopg2://datalake:datalake@localhost:5433/dw_simulado"
 
engine = create_engine(DATABASE_URI)
metadata = MetaData()
 
contratos = Table("contratos", metadata, autoload_with=engine)
 
historico_mensal = Table(
    "historico_mensal",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_contrato", Integer, ForeignKey("contratos.id_contrato")),
    Column("data_referencia", DateTime),
    Column("meses_desde_concessao", Integer),
    Column("saldo_devedor", Float),
    Column("prestacao", Float),
    Column("dti", Float),
    Column("ltv_dinamico", Float),
    Column("desemprego", Float),
    Column("inflacao", Float),
    Column("hpi", Float),
    Column("dias_atraso", Integer),
    Column("bucket", Integer),
    Column("prob_default", Float),
    Column("default_flag", Integer),
)
 
metadata.create_all(engine)
 
END_DATE = datetime(2024,12,31)
 
UNEMPLOYMENT = {2015:0.08,2016:0.11,2017:0.12,2018:0.11,2019:0.09,
                2020:0.13,2021:0.12,2022:0.10,2023:0.08,2024:0.07}
 
INFLATION = {2015:0.09,2016:0.08,2017:0.04,2018:0.04,2019:0.03,
             2020:0.06,2021:0.10,2022:0.09,2023:0.05,2024:0.04}
 
HPI = {2015:0.05,2016:0.03,2017:0.02,2018:0.03,2019:0.04,
       2020:0.06,2021:0.08,2022:0.05,2023:0.03,2024:0.02}
 
def price_payment(pv, annual_rate, years):
    i = annual_rate/12
    n = years*12
    return pv*(i*(1+i)**n)/((1+i)**n-1)
 
def generate_monthly_history():
 
    with engine.connect() as conn:
        contratos_result = conn.execute(select(contratos)).fetchall()
 
    records = []
 
    for row in contratos_result:
 
        contract_id = int(row.id_contrato)
        start_date = row.data_concessao
        pv = float(row.valor_financiado)
        annual_rate = float(row.taxa_juros)
        years = int(row.prazo_anos)
        renda = float(row.renda_cliente)
        score = float(row.score_credito)
 
        payment = price_payment(pv,annual_rate,years)
 
        balance = pv
        current_date = start_date
        meses = 0
 
        while current_date <= END_DATE and balance > 0:
 
            year = current_date.year
 
            unemployment = UNEMPLOYMENT.get(year,0.09)
            inflation = INFLATION.get(year,0.05)
            hpi = HPI.get(year,0.03)
 
            # Atualiza valor do imóvel
            valor_imovel_atual = float(row.valor_imovel)*(1+hpi)**(year-start_date.year)
 
            ltv_dinamico = balance/valor_imovel_atual
            dti = payment/renda
 
            # Simulação atraso
            atraso_prob = min(0.02 + dti*0.2 + unemployment*0.3,0.5)
            atraso_evento = np.random.binomial(1,atraso_prob)
 
            dias_atraso = 0
            bucket = 0
 
            if atraso_evento==1:
                dias_atraso = int(np.random.choice([30,60,90]))
                bucket = dias_atraso//30
 
            # PD estrutural + comportamental
            prob_default = (
                0.01 +
                0.30*((700-score)/400) +
                0.25*ltv_dinamico +
                0.20*dti +
                0.15*unemployment +
                0.10*bucket
            )
 
            prob_default = min(max(prob_default,0),0.95)
 
            default_flag = np.random.binomial(1,prob_default)
 
            records.append({
                "id_contrato":contract_id,
                "data_referencia":current_date,
                "meses_desde_concessao":meses,
                "saldo_devedor":balance,
                "prestacao":payment,
                "dti":dti,
                "ltv_dinamico":ltv_dinamico,
                "desemprego":unemployment,
                "inflacao":inflation,
                "hpi":hpi,
                "dias_atraso":dias_atraso,
                "bucket":bucket,
                "prob_default":prob_default,
                "default_flag":int(default_flag)
            })
 
            if default_flag==1:
                break
 
            monthly_interest = balance*(annual_rate/12)
            amortization = payment-monthly_interest
            balance -= amortization
 
            current_date += relativedelta(months=1)
            meses += 1
 
    with engine.begin() as conn:
        conn.execute(historico_mensal.insert(),records)
 
    print("Histórico nível mestrado gerado.")
 
generate_monthly_history()
