# Database Models Reference

## Overview
The laboratory database uses SQLAlchemy ORM with PostgreSQL backend. All tables follow the naming convention `rdb_v3_tbl_*` indicating this is version 3 of the reagent database system.

## Core Models

### Acceptance (`rdb_v3_tbl_acceptance_testing`)
Quality control acceptance criteria for reagents and supplies.

**Fields:**
- `accept_code` (Integer, PK) - Unique acceptance code identifier
- `acceptance_criteria` (String 250) - Description of acceptance criteria

**Relationships:**
- Referenced by ReagentLot and SuppliesLots for acceptance tracking

---

### Locations (`rdb_v3_tbl_locations`)
Physical storage locations within the laboratory.

**Fields:**
- `location_id` (Integer, PK) - Unique location identifier  
- `location` (String 250) - Location name/description

**Relationships:**
- Referenced by ReagentLot and SuppliesLots for storage tracking

---

### Users (`rdb_v3_tbl_users`)
Laboratory personnel who can prepare, test, and accept reagents/supplies.

**Fields:**
- `user_id` (Integer, PK) - Unique user identifier
- `username` (String 50) - User login name

**Relationships:**
- Referenced by Reagent (entered_by)
- Referenced by ReagentLot (prep_user, accept_user)
- Referenced by SuppliesLots (entered_by)

---

## Reagent Management Models

### ReagentType (`rdb_v3_tbl_reagent_types`)
Categories/classifications for different reagent types.

**Fields:**
- `reagent_type_id` (Integer, PK) - Unique type identifier
- `reagent_type` (String 255) - Type name/description

**Relationships:**
- One-to-many with Reagent

---

### Reagent (`rdb_v3_tbl_reagents`)
Master reagent definitions and inventory tracking.

**Fields:**
- `reagent_id` (Integer, PK) - Unique reagent identifier
- `test_id` (String 255) - Associated test identifier
- `reagent_name` (String 255) - Reagent name
- `stability` (Integer) - Stability period (likely in days)
- `disc` (Boolean) - Discontinued flag
- `entered_by` (Integer, FK→Users) - User who entered the reagent
- `min_stock` (Integer) - Minimum stock level threshold
- `current_stock` (Integer) - Current stock count
- `cs_deplete` (Boolean) - Coversheet depletion flag
- `mandatory` (Boolean) - Required reagent flag
- `reagent_type` (Integer, FK→ReagentType) - Reagent classification

**Relationships:**
- One-to-many with ReagentLot (`lots`)
- Many-to-one with ReagentType (`reagent_type_info`)

---

### ReagentLot (`rdb_v3_tbl_reagent_lots`)
Individual reagent lot tracking with preparation, testing, and usage data.

**Fields:**
- `reagent_lot_id` (Integer, PK) - Unique lot identifier
- `reagent_id` (Integer, FK→Reagent) - Parent reagent
- `prep_rec_date` (Date) - Preparation/receipt date
- `prep_user` (Integer, FK→Users) - User who prepared the lot
- `lot_no` (String 50) - Lot number
- `barcode_r` (String 255) - Reagent barcode
- `exp_date` (Date) - Expiration date
- `in_use_from_date` (Date) - Start of usage period
- `in_use_to_date` (Date) - End of usage period
- `disc_date` (Date) - Discontinuation date
- `comment` (String 255) - General comments
- `tested_date` (Date) - Quality control testing date
- `acceptance` (Integer, FK→Acceptance) - QC acceptance result
- `accept_user` (Integer, FK→Users) - User who accepted the lot
- `remedial` (String 255) - Remedial action taken
- `location` (Integer, FK→Locations) - Storage location

**Relationships:**
- Many-to-one with Reagent (via `reagent_id`)
- Many-to-one with Acceptance (`acceptance_info`)
- Many-to-one with Users (`prep_user_info`, `accept_user_info`)
- Many-to-one with Locations (`location_info`)

---

## Supplies Management Models

### Supplies (`rdb_v3_tbl_supplies`)
Master supplies/consumables definitions and specifications.

**Fields:**
- `supply_id` (Integer, PK) - Unique supply identifier
- `supply_name` (String 250) - Supply name
- `manufacturer` (String 50) - Manufacturer name
- `product` (String 50) - Product code/identifier
- `cas` (String 255) - CAS registry number
- `type` (String 50) - Supply type/category
- `grade` (String 50) - Chemical/material grade
- `purity_quant` (String 50) - Purity quantification
- `storage_temp` (String 50) - Storage temperature requirements
- `stability` (String 50) - Stability information
- `comment` (String 250) - General comments
- `min_stock` (Integer) - Minimum stock level
- `supply_current_stock` (Integer) - Current stock count
- `one_shot` (Boolean) - Single-use supply flag

**Relationships:**
- One-to-many with SuppliesLots (`lots`)

---

### SuppliesLots (`rdb_v3_tbl_supplies_lots`)
Individual supply lot tracking with receipt, condition, and usage data.

**Fields:**
- `supply_lot_id` (Integer, PK) - Unique supply lot identifier
- `supply_id` (Integer, FK→Supplies) - Parent supply
- `lot_no` (String 50) - Lot number
- `barcode_s` (String 255) - Supply barcode
- `quant` (String 50) - Quantity/amount
- `condition` (Boolean) - Condition status
- `use_by_date` (Date) - Use-by/expiration date
- `rec_date` (Date) - Receipt date
- `open_date` (Date) - Date opened for use
- `disc_date` (Date) - Discontinuation date
- `comment` (String 250) - General comments
- `accept` (Integer, FK→Acceptance) - QC acceptance result
- `entered_by` (Integer, FK→Users) - User who entered the lot
- `location` (Integer, FK→Locations) - Storage location

**Relationships:**
- Many-to-one with Supplies (via `supply_id`)
- Many-to-one with Acceptance (`acceptance_info`)
- Many-to-one with Locations (`location_info`)
- Many-to-one with Users (`entered_by_user`)

---

## Quality Control Model

### QCData (`rdb_v3_tbl_qcdata`)
*Note: Model definition appears incomplete in source file*

Quality control data for laboratory assays and testing.

---

## Database Relationships Summary

### Primary Entity Hierarchies:
```
Reagent (1) ──→ ReagentLot (M)
Supplies (1) ──→ SuppliesLots (M)
```

### Shared Reference Tables:
```
Users ──→ Multiple entities (entered_by, prep_user, accept_user)
Locations ──→ ReagentLot, SuppliesLots (storage tracking)
Acceptance ──→ ReagentLot, SuppliesLots (QC results)
ReagentType ──→ Reagent (classification)
```

### Key Business Logic:
- **Stock Management**: Both Reagent and Supplies track current_stock vs min_stock
- **Traceability**: Lot-level tracking for both reagents and supplies
- **Quality Control**: Acceptance testing integrated at lot level
- **User Accountability**: User tracking for preparation, entry, and acceptance
- **Location Management**: Physical storage location tracking
- **Lifecycle Management**: Dates tracked from receipt through discontinuation

### Barcode Integration:
- `barcode_r` (ReagentLot) - Reagent lot barcodes
- `barcode_s` (SuppliesLots) - Supply lot barcodes

Note - this barcode structure (using _r and _s) is a legacy structure that has/will be replaced by a centralised "barcode" field in a barcode table, this is yet to be implemented in this build. 