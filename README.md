# Risco de Crédito - Resolução 4966

Simulação , modelagem de PD / LGD / EAD e pipeline auditável usando Airflow + MLflow.

## 📌 Visão Sobre o Projeto

Este projeto implementa um framework completo de risco de crédito imobiliário, com:

- Geração de dados sintéticos realistas
- Estrutura Relacional em Postgres
- Histórico mensal e longitudinal
- Modelagem de PD, LGD e EAD
- Cálculo de ECL conforme IFRS 9 / resiolução 4966
- Pipeline orquestrado com Airflow
- Versionamento e rasteabilidade de experimentos com MLflow

O objetivo é construir uma arquitetura auditável, reproduzível e alinhada com boas práticas bancárias, simulando um ambiente real de risco de crédito, e , além disso, ser um projeto maduro no que tange a Engenharia de Dados, Orquestração e MLOps.

## Objetivo do TCC

O tcc tem como objetivo principal desenvolver um sistema completo de Estimativa de Perda Esperada para risco de crédito imobiliário, utilizando técnicas de simulação de dados, modelagem estatística e machine learning, e orquestração de pipelines com Airflow. Ele deve ser aplicável ao contexto regulatório bancário brasileiro (Resolução 4966/ IFRS ).

O projeto demonstrará ter:

- Governança de Modelos;
- Separação entre dados, modelos e métricas;
- Rastreabilidade total dos experimentos;
- Versionamento de código e artefatos;
- Reprodutibilidade dos resultados;
- Arquitetura de produção.

## Arquitetura do Projeto
