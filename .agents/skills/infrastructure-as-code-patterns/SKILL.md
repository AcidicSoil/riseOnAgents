---
name: infrastructure-as-code-patterns
description: Patterns and best practices for Infrastructure as Code using Terraform, Bicep, CloudFormation, and Pulumi. Use when designing, implementing, or reviewing IaC.
---

# Infrastructure as Code Patterns

A comprehensive catalog of patterns and best practices for Infrastructure as Code (IaC) using Terraform, Bicep, CloudFormation, and Pulumi.

---

## When to Use This Skill

Use this skill when:
- Designing cloud infrastructure
- Writing Terraform/Bicep/CloudFormation code
- Reviewing IaC for best practices
- Setting up state management
- Implementing modular infrastructure
- Establishing IaC standards

---

## Core Principles

### 1. Everything in Code
- ✅ All resources defined in IaC
- ✅ No manual resource creation
- ✅ Version controlled in Git
- ✅ Reviewed via pull requests

### 2. State Management
- ✅ Remote state (S3, Azure Storage, GCS)
- ✅ State locking enabled
- ✅ State encrypted at rest
- ✅ Separate states per environment
- ✅ Never commit state files

### 3. Modular Design
- ✅ Reusable modules
- ✅ Clear module interfaces
- ✅ Versioned modules
- ✅ Module registry usage

### 4. Security
- ✅ No secrets in code
- ✅ Least privilege IAM
- ✅ Encryption enabled
- ✅ Security scanning in CI/CD

---

## File Structure Patterns

### Terraform Structure
```
terraform/
├── main.tf              # Provider and backend configuration
├── variables.tf         # Variable definitions
├── outputs.tf           # Output values
├── providers.tf         # Provider configurations
├── versions.tf          # Version constraints
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── production/
│       ├── main.tf
│       └── terraform.tfvars
└── modules/
    ├── networking/
    ├── compute/
    └── database/
```

### Bicep Structure
```
bicep/
├── main.bicep           # Main deployment file
├── parameters/
│   ├── dev.parameters.json
│   ├── staging.parameters.json
│   └── production.parameters.json
├── modules/
│   ├── networking.bicep
│   ├── compute.bicep
│   └── database.bicep
└── shared/
    └── constants.bicep  # Shared constants and types
```

---

## Resource Naming Pattern

### Consistent Naming Convention
```hcl
# ✅ Good: project-environment-resource-type-name
resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.env}-rg"
  location = var.location
}

resource "azurerm_app_service" "main" {
  name                = "${var.project}-${var.env}-app"
  resource_group_name = azurerm_resource_group.main.name
}

# ❌ Bad: Inconsistent naming
resource "azurerm_resource_group" "rg" {
  name = "my-rg"
}
```

### Naming Standards by Resource

| Resource Type | Pattern | Example |
|---------------|---------|---------|
| Resource Group | `{project}-{env}-rg` | `myapp-prod-rg` |
| App Service | `{project}-{env}-app` | `myapp-prod-app` |
| SQL Database | `{project}-{env}-sql` | `myapp-prod-sql` |
| Storage Account | `{project}{env}store` | `myappprodstorage` |
| Key Vault | `{project}-{env}-kv` | `myapp-prod-kv` |
| VNet | `{project}-{env}-vnet` | `myapp-prod-vnet` |

---

## Tagging Pattern

### Comprehensive Tagging
```hcl
locals {
  common_tags = {
    Environment   = var.environment
    Project       = var.project_name
    ManagedBy     = "Terraform"
    Owner         = var.owner
    CostCenter    = var.cost_center
    CreatedDate   = timestamp()
  }
}

resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.env}-rg"
  location = var.location
  
  tags = local.common_tags
}
```

### Required Tags
| Tag | Purpose | Example |
|-----|---------|---------|
| `Environment` | Cost allocation | `dev`, `staging`, `prod` |
| `Project` | Project tracking | `myapp`, `website` |
| `ManagedBy` | IaC identification | `Terraform`, `Bicep` |
| `Owner` | Responsibility | `team-platform` |
| `CostCenter` | Billing | `cc-12345` |

---

## Variable Validation Pattern

### Input Validation
```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "instance_size" {
  description = "VM instance size"
  type        = string
  
  validation {
    condition     = can(regex("^[A-Z][0-9]+[m]?$", var.instance_size))
    error_message = "Instance size must be valid (e.g., B2s, D4s, D8m)."
  }
}

variable "enable_ssl" {
  description = "Enable SSL for the application"
  type        = bool
  default     = true
}
```

---

## Module Pattern

### Module Structure
```
modules/
└── networking/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

### Module Definition
```hcl
# modules/networking/main.tf
resource "azurerm_virtual_network" "main" {
  name                = var.vnet_name
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = var.address_space
}

resource "azurerm_subnet" "public" {
  name                 = "PublicSubnet"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = var.public_subnet_cidr
}

resource "azurerm_subnet" "private" {
  name                 = "PrivateSubnet"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = var.private_subnet_cidr
}
```

### Module Usage
```hcl
module "networking" {
  source = "./modules/networking"
  
  vnet_name             = "${var.project_name}-vnet"
  location              = azurerm_resource_group.main.location
  resource_group_name   = azurerm_resource_group.main.name
  address_space         = ["10.0.0.0/16"]
  public_subnet_cidr    = ["10.0.1.0/24"]
  private_subnet_cidr   = ["10.0.2.0/24"]
  environment           = var.environment
}
```

---

## State Management Pattern

### Remote Backend (Azure)
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstatestorage"
    container_name       = "tfstate"
    key                  = "${var.environment}.terraform.tfstate"
  }
}
```

### Remote Backend (AWS)
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "${var.environment}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### State Locking
```hcl
# AWS DynamoDB table for locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  
  hash_key = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

---

## Secrets Management Pattern

### Key Vault Integration
```hcl
resource "azurerm_key_vault" "main" {
  name                        = "${var.project}-${var.env}-kv"
  location                    = azurerm_resource_group.main.location
  resource_group_name         = azurerm_resource_group.main.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
  
  sku_name = "standard"
}

resource "azurerm_key_vault_secret" "connection_string" {
  name         = "database-connection-string"
  value        = var.database_connection_string
  key_vault_id = azurerm_key_vault.main.id
}
```

### Accessing Secrets
```hcl
data "azurerm_key_vault_secret" "connection_string" {
  name         = "database-connection-string"
  key_vault_id = azurerm_key_vault.main.id
}

resource "azurerm_app_service" "main" {
  # ...
  
  app_settings = {
    "ConnectionString" = data.azurerm_key_vault_secret.connection_string.value
  }
}
```

---

## Network Security Pattern

### Network Segmentation
```hcl
resource "azurerm_subnet" "database" {
  name                 = "DatabaseSubnet"
  virtual_network_name = azurerm_virtual_network.main.name
  resource_group_name  = azurerm_resource_group.main.name
  address_prefixes     = ["10.0.3.0/24"]
  
  delegation {
    name = "delegation"
    service_delegation {
      name = "Microsoft.Sql/servers"
    }
  }
}

resource "azurerm_network_security_group" "database" {
  name                = "${var.project}-${var.env}-db-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  security_rule {
    name                       = "AllowSQL"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "1433"
    source_address_prefix      = "10.0.2.0/24"  # App subnet only
    destination_address_prefix = "*"
  }
}
```

---

## Encryption Pattern

### Storage Encryption
```hcl
resource "azurerm_storage_account" "main" {
  name                     = "${var.project}storage"
  location                 = azurerm_resource_group.main.location
  resource_group_name      = azurerm_resource_group.main.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  customer_managed_key {
    key_vault_key_id = azurerm_key_vault_key.main.id
  }
}
```

### Database Encryption
```hcl
resource "azurerm_sql_server" "main" {
  name                         = "${var.project}-sql"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.admin_username
  administrator_login_password = var.admin_password
  
  # TDE enabled by default
}
```

---

## Cost Optimization Pattern

### Right-Sizing
```hcl
resource "azurerm_app_service_plan" "main" {
  name                = "${var.project}-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  # Right-size based on environment
  sku {
    tier = var.environment == "production" ? "Standard" : "Basic"
    size = var.environment == "production" ? "S1" : "B1"
  }
}
```

### Auto-Scaling
```hcl
resource "azurerm_monitor_autoscale_setting" "main" {
  name                = "${var.project}-autoscale"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  target_resource_id  = azurerm_app_service_plan.main.id
  
  profile {
    name = "default"
    capacity {
      default = 2
      minimum = 1
      maximum = 10
    }
    
    rule {
      metric_trigger {
        metric_name  = "CpuPercentage"
        statistic    = "Average"
        time_window  = "PT5M"
        time_grain   = "PT1M"
        operator     = "GreaterThan"
        threshold    = 70
      }
      
      scale_action {
        direction    = "Increase"
        type         = "ChangeCount"
        value        = "1"
        cooldown     = "PT5M"
      }
    }
  }
}
```

---

## Compliance Pattern

### Resource Locks
```hcl
resource "azurerm_resource_lock" "production" {
  name                 = "production-lock"
  scope                = azurerm_resource_group.production.id
  lock_level           = "CanNotDelete"
  notes                = "Production resources - requires approval for deletion"
}
```

### Diagnostic Logging
```hcl
resource "azurerm_monitor_diagnostic_setting" "main" {
  name               = "${var.project}-diagnostics"
  target_resource_id = azurerm_app_service.main.id
  
  enabled_log {
    category = "AppServiceHTTPLogs"
    
    retention_policy {
      enabled = true
      days    = 90
    }
  }
  
  metric {
    category = "AllMetrics"
    enabled  = true
    
    retention_policy {
      enabled = true
      days    = 90
    }
  }
}
```

---

## Quality Checklist

### Code Quality
- [ ] Resources named consistently
- [ ] Tags applied to all resources
- [ ] Variables used (no hardcoding)
- [ ] Outputs defined
- [ ] Comments for complex logic
- [ ] Documentation updated

### Security
- [ ] No secrets in code
- [ ] Encryption enabled
- [ ] Network security configured
- [ ] Least privilege IAM
- [ ] Diagnostic logging enabled

### Cost
- [ ] Resources right-sized
- [ ] Auto-scaling enabled
- [ ] Reserved instances considered
- [ ] Cost tags applied
- [ ] Unused resources removed

### State Management
- [ ] Remote backend configured
- [ ] State locking enabled
- [ ] State encrypted
- [ ] Separate states per environment
- [ ] State files in .gitignore

---

## Related Skills

- **ci-cd-patterns** — CI/CD pipeline patterns
- **security-audit-checklist** — Security assessments
- **cloud-cost-optimization** — Cost optimization strategies

---

## Output Format

When using this skill, provide:
1. **IaC code** following patterns above
2. **File structure** for the project
3. **Module definitions** for reusability
4. **Variable validation** for inputs
5. **State management** configuration
6. **Security controls** implemented
7. **Cost optimization** applied
