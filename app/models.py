from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, redirect, request, url_for
from datetime import datetime

db = SQLAlchemy()

class Acceptance(db.Model):
    __tablename__ = 'rdb_v3_tbl_acceptance_testing'
    
    accept_code = db.Column(db.Integer, primary_key=True)
    acceptance_criteria = db.Column(db.String(250))
    
    def __repr__(self):
        return f'<Acceptance {self.acceptance_criteria}>'

class Locations(db.Model):
    __tablename__ = 'rdb_v3_tbl_locations'
    
    location_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(250))
    
    def __repr__(self):
        return f'<Location {self.location}>'

# Reagent Type Model
class ReagentType(db.Model):
    __tablename__ = 'rdb_v3_tbl_reagent_types'
    
    reagent_type_id = db.Column(db.Integer, primary_key=True)
    reagent_type = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<ReagentType {self.reagent_type}>'

# Reagent Model
class Reagent(db.Model):
    __tablename__ = 'rdb_v3_tbl_reagents'
    
    reagent_id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(255))
    reagent_name = db.Column(db.String(255))
    stability = db.Column(db.Integer)
    disc = db.Column(db.Boolean)
    entered_by = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_users.user_id'))
    min_stock = db.Column(db.Integer)
    current_stock = db.Column(db.Integer)
    cs_deplete = db.Column(db.Boolean)
    mandatory = db.Column(db.Boolean)
    reagent_type = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_reagent_types.reagent_type_id'))
    
    # Relationships
    lots = db.relationship('ReagentLot', backref='reagent', lazy=True)
    reagent_type_info = db.relationship('ReagentType', foreign_keys=[reagent_type])

    def __repr__(self):
        return f'<Reagent {self.reagent_name}>'

# Reagent Lot Model
class ReagentLot(db.Model):
    __tablename__ = 'rdb_v3_tbl_reagent_lots'
    
    reagent_lot_id = db.Column(db.Integer, primary_key=True)
    reagent_id = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_reagents.reagent_id'))
    prep_rec_date = db.Column(db.Date)
    prep_user = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_users.user_id'))
    lot_no = db.Column(db.String(50))
    barcode_r = db.Column(db.String(255))
    exp_date = db.Column(db.Date)
    in_use_from_date = db.Column(db.Date)
    in_use_to_date = db.Column(db.Date)
    disc_date = db.Column(db.Date)
    comment = db.Column(db.String(255))
    tested_date = db.Column(db.Date)
    acceptance = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_acceptance_testing.accept_code'))
    accept_user = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_users.user_id'))
    remedial = db.Column(db.String(255))
    location = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_locations.location_id'))
    
    # Relationships
    acceptance_info = db.relationship('Acceptance', backref='reagent_lots', lazy=True)
    prep_user_info = db.relationship('Users', foreign_keys=[prep_user], backref='prepared_reagent_lots', lazy=True)
    accept_user_info = db.relationship('Users', foreign_keys=[accept_user], backref='accepted_reagent_lots', lazy=True)
    location_info = db.relationship('Locations', backref='reagent_lots', lazy=True)

    def __repr__(self):
        return f'<ReagentLot {self.lot_no}>'

# Define models for SQL here (probably want to move this into a separate file at some point)
class Supplies(db.Model):
    __tablename__ = 'rdb_v3_tbl_supplies'
    
    supply_id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(250))
    manufacturer = db.Column(db.String(50))
    product = db.Column(db.String(50))
    cas = db.Column(db.String(255))
    type = db.Column(db.String(50))
    grade = db.Column(db.String(50))
    purity_quant = db.Column(db.String(50))
    storage_temp = db.Column(db.String(50))
    stability = db.Column(db.String(50))
    comment = db.Column(db.String(250))
    min_stock = db.Column(db.Integer)
    supply_current_stock = db.Column(db.Integer)
    one_shot = db.Column(db.Boolean)
    
    # Relationship with lots
    lots = db.relationship('SuppliesLots', backref='supply', lazy=True)
    
    def __repr__(self):
        return f'<Supply {self.supply_name}>'

class SuppliesLots(db.Model):
    __tablename__ = 'rdb_v3_tbl_supplies_lots'
    
    supply_lot_id = db.Column(db.Integer, primary_key=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_supplies.supply_id'))
    lot_no = db.Column(db.String(50))
    barcode_s = db.Column(db.String(255))
    quant = db.Column(db.String(50))
    condition = db.Column(db.Boolean)
    use_by_date = db.Column(db.Date)
    rec_date = db.Column(db.Date)
    open_date = db.Column(db.Date)
    disc_date = db.Column(db.Date)
    comment = db.Column(db.String(250))
    accept = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_acceptance_testing.accept_code'))
    entered_by = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_users.user_id'))
    location = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_locations.location_id'))

    # Relationships
    acceptance_info = db.relationship('Acceptance', backref='supplies_lots', lazy=True)
    location_info = db.relationship('Locations', backref='supplies_lots', lazy=True) 
    entered_by_user = db.relationship('Users', backref='entered_supplies_lots', lazy=True)
    
    def __repr__(self):
        return f'<SupplyLot {self.lot_no}>'

# Users Model (placeholder - adjust based on your actual users table structure)
class Users(db.Model):
    __tablename__ = 'rdb_v3_tbl_users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    # Add other fields as needed
    
    def __repr__(self):
        return f'<User {self.username}>'

class QCData(db.Model):
    __tablename__ = 'rdb_v3_tbl_qc_data'
    
    qc_data_id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(25), nullable=False)
    reagent_lot_id = db.Column(db.String(25), nullable=False)
    qc_level = db.Column(db.String(25), nullable=False)
    measurement_value = db.Column(db.Numeric(10,4), nullable=False)
    measurement_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    instrument_id = db.Column(db.String(25))
    cs_id = db.Column(db.String(25))
    user_id = db.Column(db.String(25))
    target_mean = db.Column(db.Numeric(10,4), nullable=False)
    target_sd = db.Column(db.Numeric(10,4), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'qc_data_id': self.qc_data_id,
            'test_id': self.test_id,
            'reagent_lot_id': self.reagent_lot_id,
            'qc_level': self.qc_level,
            'measurement_value': float(self.measurement_value),
            'measurement_date': self.measurement_date.isoformat(),
            'instrument_id': self.instrument_id,
            'cs_id': self.cs_id,
            'user_id': self.user_id,
            'target_mean': float(self.target_mean),
            'target_sd': float(self.target_sd)
        }
    
    def __repr__(self):
        return f'<QCData {self.test_id}-{self.qc_level}: {self.measurement_value}>'