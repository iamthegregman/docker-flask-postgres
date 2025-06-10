@echo off
kubectl exec -it postgres-db-697dbfbfc4-zx9v8 -- psql -U herman -d reagentdb -c "TRUNCATE TABLE rdb_v3_tbl_supplies_lots, rdb_v3_tbl_reagent_lots, rdb_v3_tbl_supplies, rdb_v3_tbl_reagents, rdb_v3_tbl_locations, rdb_v3_tbl_acceptance_testing, rdb_v3_tbl_reagent_types, rdb_v3_tbl_users CASCADE;"
echo Data cleared successfully!
pause