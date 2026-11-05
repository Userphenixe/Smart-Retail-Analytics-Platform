# Smart Retail Analytics Platform

## Overview

Smart Retail Analytics Platform is an end-to-end Analytics Engineering project designed to simulate a modern retail data platform.

The project covers the complete analytics lifecycle:

- API Data Ingestion
- Change Data Capture (CDC) Simulation
- Workflow Orchestration with Airflow
- Data Transformation with dbt
- Kimball Data Warehouse Modeling
- Data Quality Testing
- Snapshot Management
- Business Intelligence with Metabase

---

## Architecture

```text
DummyJSON APIs
       |
       v
Python Extract Layer
       |
       v
PostgreSQL Raw Layer
       |
       v
CDC Simulation
       |
       v
Apache Airflow
       |
       v
dbt Transformations
       |
       v
Kimball Star Schema
       |
       v
Metabase Dashboards
```

---

## Tech Stack

| Layer | Technology |
|---------|---------|
| Source | DummyJSON API |
| Ingestion | Python |
| Storage | PostgreSQL |
| Orchestration | Apache Airflow |
| Transformation | dbt Core 1.11 |
| Modeling | Kimball |
| Testing | dbt Tests |
| BI | Metabase |
| Containerization | Docker |

---

## Data Domains

### Products

Product catalog information.

### Customers

Customer profile information.

### Recipes

Recipes and product-related cooking content.

### Carts

Shopping carts and sales transactions.

---

## CDC Simulation

The platform simulates incremental data ingestion every 6 hours.

Generated records:

| Domain | New Records |
|----------|----------|
| Products | 3 |
| Customers | 2 |
| Carts | 5 |
| Recipes | 2 |

---

## Airflow DAG

```text
generate_products
generate_users
generate_carts
generate_recipes
         |
         v
dbt build
```

---

## Data Warehouse Layers

```text
raw
   |
staging
   |
intermediate
   |
marts
```

---

## Star Schema

### Dimensions

- dim_customer
- dim_product
- dim_recipe
- dim_date

### Facts

- fct_sales

---

## Project Goals

The purpose of this project is to demonstrate:

- Incremental Data Pipelines
- CDC Processing
- Data Warehouse Design
- Analytics Engineering Best Practices
- dbt Development
- Airflow Orchestration
- Testing and Documentation
