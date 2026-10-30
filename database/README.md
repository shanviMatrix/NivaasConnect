# NivaasConnect Database

Database engine: PostgreSQL 18

## Setup order

1. Create the database `nivaasconnect_db`.
2. Execute `schema/01_apartments.sql` through `schema/11_society_events.sql` in order.
3. Execute `schema/12_indexes.sql`.
4. Execute seed files `01_apartments.sql` through `11_society_events.sql` in order.
5. Run queries from the `queries/` directory as required.

## Directories

- `schema/`: table definitions and indexes
- `seeds/`: demonstration data for a fresh database
- `queries/`: reusable SQL and reports

## Important

Seed files are for a fresh database and should be executed once.
Do not rerun them on a database that already contains the sample records.

The `initial_*_snapshot.sql` files preserve earlier SQL work.
