# Laboratory Reagent and Consumable Database - Project Overview

## Project Description
A comprehensive laboratory management system designed to track reagents, consumables, and equipment while providing advanced quality control capabilities for laboratory assays.

## Core Objectives

### Primary Functions
1. **Centralized Inventory Management**
   - Maintain real-time stock counts for all laboratory reagents and consumables
   - Track usage patterns and consumption rates
   - Alert system for low stock levels

2. **Supply Relationship Tracking**
   - Detailed relationship mapping between different supplies and reagents
   - Multi-level ingredient/component tracking via relationship tables
   - Traceability from raw materials to final reagents

3. **Barcoding System**
   - Barcode/QR code generation and management for reagents, supplies, and equipment
   - Integration ready for barcode scanner applications
   - Unique identification system for all tracked items

4. **Digital Coversheet System**
   - Electronic logging of reagents, supplies, and equipment used in laboratory assays
   - Replace paper-based tracking with digital workflow
   - Link assay runs to specific inventory items

5. **Quality Management & Control**
   - Generate quality control plots including Levy-Jennings charts
   - Connect QC data to specific reagent lots, supplies, and equipment used
   - Statistical process control for assay performance monitoring

## Technical Architecture

### Backend Infrastructure
- **Database**: PostgreSQL for robust data management
- **Web Framework**: Flask application server with server-side rendering
- **ORM**: SQLAlchemy for database abstraction and relationships
- **Templates**: Jinja2 templating engine for dynamic HTML generation

### Frontend Design
- **Framework**: Bootstrap for responsive, professional UI
- **Architecture**: Traditional web application with server-rendered pages
- **Scripting**: Minimal JavaScript for enhanced user experience
- **Visualization**: Plotly for quality control data display (current implementation)
- **Design Philosophy**: Simple, functional interface prioritizing usability

### Development & Deployment
- **Development Environment**: Docker containerization
- **Version Control**: Git repository management
- **Production Deployment**: Kubernetes cluster on Google Cloud Services
- **Scalability**: Cloud-native architecture for growth

## Legacy Integration

### Migration from MS Access System
- **Current System**: MS Access "grandfather" database in active laboratory use
- **Existing Functions**: Database management and coversheet functionality
- **Migration Strategy**: Preserve underlying file structure with minimal alterations
- **Key Limitation**: Legacy system cannot generate graphical interfaces or quality control plots

### Enhancement Goals
- Maintain compatibility with existing workflows
- Add advanced visualization capabilities
- Implement modern web-based interface
- Extend functionality while preserving data integrity

## Project Scope

### Phase 1: Core Functionality & Scanner Integration
- Integrate HTML scanner application and demonstrate basic functionality
- Demonstrate basic creation of new records (reagents, supplies, and equipment)
- **Milestone**: Push to Kubernetes/Google Cloud (overwrite current prototype)

### Phase 2: Complete Migration & Barcoding
- Complete port of existing table structure from MS Access
- Port over barcoding rules and reagent/supplies/equipment barcode logic
- Implement extended business logic from legacy system
- **Milestone**: Push to Kubernetes/Google Cloud

### Phase 3: Advanced Features & Quality Control
- Integrate digital coversheet functionality
- Integrate Levy-Jennings plots (currently implemented in Plotly)
- Complete quality management system implementation
- **Milestone**: Push to Kubernetes/Google Cloud

## Success Criteria
- Seamless migration of existing laboratory data
- Improved efficiency in inventory management
- Enhanced quality control capabilities
- User adoption by laboratory staff
- Scalable system ready for future expansion
