# Service Contracts — Odoo 17 Module

A custom Odoo 17 module for managing service contracts and support requests.  
Built as a portfolio project to demonstrate real-world Odoo development skills.

---

## Features

- **Contract Management** — Create and manage service contracts with customers
- **State Machine** — Draft → Active → Expired / Cancelled workflow with status tracking
- **Service Lines** — Add multiple services per contract with automatic subtotal calculation
- **Support Requests** — Track tickets linked to contracts, with priority levels
- **Kanban View** — Visual board grouped by contract status
- **PDF Report** — Printable contract document with company header and signature lines
- **Expiry Reminders** — Automatic email notification when a contract is expiring (30 days)
- **Scheduled Action** — Daily cron job that marks expired contracts and sends reminders
- **Security Groups** — User / Manager roles with different permissions
- **Demo Data** — Pre-loaded sample contracts and requests for testing

---

## Technical Concepts Demonstrated

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

---

## Module Structure

```
addons/service_contracts/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── service_contract.py       # Main contract model
│   ├── service_contract_line.py  # Contract line items
│   └── service_request.py        # Support requests / tickets
├── views/
│   ├── service_contract_views.xml  # List, Form, Kanban views
│   ├── service_request_views.xml   # List, Form views
│   └── menu.xml                    # Navigation menus
├── report/
│   ├── contract_report_action.xml  # Report action
│   └── contract_report.xml         # QWeb PDF template
├── data/
│   └── mail_template.xml           # Email template + Cron job
├── security/
│   ├── security.xml                # Groups definition
│   └── ir.model.access.csv         # Model access rights
└── demo/
    └── demo_data.xml               # Sample data
```

---

## Installation

### Requirements
- Docker Desktop with WSL2
- Docker Compose

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/odoo-service-contracts.git
cd odoo-service-contracts

# Start Odoo + PostgreSQL
docker-compose up -d

# Open browser
http://localhost:8069
```

Create a new database, then go to **Apps → Service Contracts → Install**.

> **Note:** After installation, go to **Settings → Users → Administrator** and assign the **Service Contracts / Manager** group.

---

## Screenshots

### Kanban View
![Kanban View](docs/screenshots/kanban.png)

### Contract Form
![Contract Form](docs/screenshots/contract_form.png)

### PDF Report
![PDF Report](docs/screenshots/pdf_report.png)

---

## Business Use Case

This module solves a real business need: companies that sell recurring services (IT support, maintenance, consulting) need to:

1. Track which services are included in each client's contract
2. Monitor contract expiration dates proactively
3. Manage support requests linked to specific contracts
4. Generate professional contract documents for signing

---

## Author

Built with [Claude Code](https://claude.ai/code) as an Odoo 17 portfolio project.
