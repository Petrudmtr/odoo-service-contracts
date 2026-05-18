# Service Contracts — Odoo 17

Custom Odoo module for managing service contracts, support requests and automatic expiry reminders.

## Features

- **Contract Management** — create and manage service contracts with customers
- **State Machine** — Draft → Active → Expired / Cancelled workflow
- **Service Lines** — multiple services per contract with automatic subtotal calculation
- **Support Requests** — tickets linked to contracts with priority levels
- **Kanban View** — visual board grouped by contract status
- **PDF Report** — printable contract document with company header and signature lines
- **Expiry Reminders** — automatic email notification 30 days before expiry
- **Scheduled Action** — daily cron job that marks expired contracts and sends reminders
- **Security Groups** — separate access for Users and Managers

## Technical Concepts

| Concept | Implementation |
|---|---|
| Custom ORM models | `service.contract`, `service.contract.line`, `service.request` |
| Computed fields | `total_value`, `days_remaining`, `subtotal` |
| State machine | Selection field + action buttons + statusbar widget |
| One2many / Many2one | Contract ↔ Lines, Contract ↔ Requests |
| Related field | `partner_id` on request (from contract) |
| Kanban view | Grouped by state, custom card template |
| QWeb PDF report | `ir.actions.report` + HTML template |
| Mail template | `mail.template` with dynamic content |
| Scheduled action | `ir.cron` calling a model method |
| Security groups | `res.groups` + `ir.model.access.csv` |
| Chatter | `mail.thread` + `mail.activity.mixin` inheritance |
| Demo data | XML fixtures referencing base partners |

## Module Structure

```
addons/service_contracts/
├── models/
│   ├── service_contract.py       ← main contract model
│   ├── service_contract_line.py  ← contract line items
│   └── service_request.py        ← support requests / tickets
├── views/
│   ├── service_contract_views.xml  ← list, form, kanban views
│   ├── service_request_views.xml   ← list, form views
│   └── menu.xml                    ← navigation menus
├── report/
│   ├── contract_report_action.xml  ← report action
│   └── contract_report.xml         ← QWeb PDF template
├── data/
│   └── mail_template.xml           ← email template + cron job
├── security/
│   ├── security.xml                ← groups definition
│   └── ir.model.access.csv         ← model access rights
└── demo/
    └── demo_data.xml               ← sample data
```

## Workflow

1. Manager creates a **Service Contract** for a customer with services and validity period
2. Manager activates the contract (Draft → Active)
3. Customers or agents create **Support Requests** linked to the contract
4. Daily cron job monitors expiry dates and sends **email reminders** at 30 days
5. Manager prints a **PDF report** for signing or archiving

## Installation

### Requirements

- Docker Desktop
- Docker Compose

### Setup

```bash
# Clone the repository
git clone https://github.com/Petrudmtr/odoo-service-contracts.git
cd odoo-service-contracts

# Start containers
docker-compose up -d

# Open http://localhost:8069
# Create database: name=odoo_dev, password=admin123, load demo data
# Activate Developer Mode: Settings → Activate Developer Mode
# Apps → search "Service Contracts" → Install
```

Add Administrator to the **Service Contracts / Manager** group:
Settings → Users → Administrator → Service Contracts: Manager

## Credentials

| | Value |
|---|---|
| URL | http://localhost:8069 |
| Admin user | admin |
| Admin password | admin123 |
