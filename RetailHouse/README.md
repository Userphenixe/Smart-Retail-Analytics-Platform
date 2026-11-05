# RetailHouse dbt Project

## Overview

RetailHouse is the transformation layer of the Smart Retail Analytics Platform.

The project transforms raw retail data into a Kimball-style analytical data warehouse using dbt.

---

## dbt Version

```text
dbt Core 1.11
dbt-postgres 1.11
```

---

## Project Structure

```text
models/

├── sources
│
├── staging
│   ├── stg_products
│   ├── stg_customers
│   ├── stg_carts
│   └── stg_recipes
│
├── intermediate
│   ├── int_products_enriched
│   ├── int_customer_profile
│   ├── int_product_reviews
│   ├── int_recipes_enriched
│   └── int_sales
│
└── marts
    ├── dim_customer
    ├── dim_product
    ├── dim_recipe
    ├── dim_date
    └── fct_sales
```

---

## Sources

### raw.products

Product master data.

### raw.users

Customer data.

### raw.carts

Shopping cart transactions.

### raw.recipes

Recipe information.

---

## Seeds

### seed_product_categories

Category-to-department mapping.

Example:

```text
beauty -> Personal Care
groceries -> Food
furniture -> Home
```

---

### seed_availability_status

Product availability mapping.

```text
In Stock
Low Stock
Out of Stock
```

---

### seed_rating_band

Rating segmentation.

```text
Poor
Average
Excellent
```

---

### seed_recipe_difficulty

Recipe difficulty score.

```text
Easy -> 1
Medium -> 2
Hard -> 3
```

---

## Incremental Processing

The staging layer uses incremental loading based on:

```sql
ingestion_timestamp
```

Watermark pattern:

```sql
where ingestion_timestamp >
(
    select max(ingestion_timestamp)
    from {{ this }}
)
```

---

## Snapshots

Implemented using dbt snapshots.

### Products Snapshot

Tracks historical product changes.

### Customers Snapshot

Tracks historical customer changes.

### Recipes Snapshot

Tracks historical recipe changes.

---

## Testing

### Unit Tests

Implemented for:

- int_products_enriched
- int_customer_profile
- int_recipes_enriched

### Generic Tests

Implemented for:

- unique
- not_null
- relationships
- accepted_values

### Singular Tests

Implemented for business validation rules.

---

## Intermediate Layer Logic

### int_products_enriched

Product enrichment using seeds.

### int_customer_profile

Customer standardization and segmentation.

### int_product_reviews

Review extraction and rating normalization.

### int_recipes_enriched

Recipe enrichment with difficulty scoring.

### int_sales

Sales transaction enrichment.

---

## Kimball Model

### Dimensions

- dim_customer
- dim_product
- dim_recipe
- dim_date

### Fact

- fct_sales

---

## Running the Project

### Install dependencies

```bash
dbt deps
```

### Run models

```bash
dbt run
```

### Execute tests

```bash
dbt test
```

### Run snapshots

```bash
dbt snapshot
```

### Generate documentation

```bash
dbt docs generate
```

### Open documentation

```bash
dbt docs serve
```

---

## Key Concepts Demonstrated

- Incremental Models
- Snapshots
- Seeds
- Macros
- Jinja
- Unit Tests
- Generic Tests
- Singular Tests
- Kimball Modeling
- CDC Processing
- Source Freshness