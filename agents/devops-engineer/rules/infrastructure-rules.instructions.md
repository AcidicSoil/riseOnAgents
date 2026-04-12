---
description: Infrastructure as Code rules and guidelines for Terraform, Bicep, CloudFormation, and cloud resource management
applyTo: '**/*.tf,**/*.bicep,**/*.cfn.yaml,**/terraform/**,**/infra/**'
---

# Infrastructure Rules

Infrastructure as Code rules and guidelines for Terraform, Bicep, CloudFormation, and cloud resource management.

## Infrastructure as Code Standards

### General IaC Principles
✅ **All infrastructure must:**
- Be defined in code (Terraform, Bicep, CloudFormation)
- Be version controlled in Git
- Go through pull request review
- Be applied through CI/CD pipelines
- Have documentation
- Use meaningful resource names
- Include tags for cost tracking
- Follow naming conventions

### State Management
✅ **Terraform state must:**
- Be stored remotely (S3, Azure Storage, GCS)
- Have state locking enabled
- Be encrypted at rest
- Use separate states per environment
- Never be committed to Git
- Have backup enabled

## Terraform Best Practices

### File Structure
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
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
└── modules/
    ├── networking/
    ├── compute/
    └── database/
```

### Resource Naming
```hcl
# ✅ Good: Consistent naming with project, resource, environment
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.location
}

resource "azurerm_app_service" "main" {
  name                = "${var.project_name}-${var.environment}-app"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

# ❌ Bad: Inconsistent naming
resource "azurerm_resource_group" "rg" {
  name = "my-rg"
}
```

### Tagging Standards
```hcl
# ✅ Good: Comprehensive tagging
tags = {
  Name          = "${var.project_name}-${var.environment}"
  Environment   = var.environment
  Project       = var.project_name
  ManagedBy     = "Terraform"
  Owner         = var.owner
  CostCenter    = var.cost_center
  CreatedDate   = timestamp()
}

# ❌ Bad: Missing or inconsistent tags
tags = {
  name = "my-resource"
}
```

### Variable Validation
```hcl
# ✅ Good: Input validation
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

# ❌ Bad: No validation
variable "environment" {
  type = string
}
```

### Module Usage
```hcl
# ✅ Good: Modular design
module "networking" {
  source = "./modules/networking"
  
  vnet_name     = "${var.project_name}-vnet"
  address_space = ["10.0.0.0/16"]
  subnets = {
    public  = ["10.0.1.0/24"]
    private = ["10.0.2.0/24"]
  }
  environment = var.environment
}

module "database" {
  source  = "Azure/sql/azurerm"
  version = "1.0.0"
  
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  server_name         = "${var.project_name}-sql"
  database_name       = "${var.project_name}-db"
  environment         = var.environment
}

# ❌ Bad: Monolithic configuration
# All resources in single file without modules
```

### State Locking
```hcl
# ✅ Good: Remote backend with locking
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstatestorage"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"
  }
  
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# ❌ Bad: Local state (no locking, no backup)
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
```

## Security Requirements

### Secrets Management
```hcl
# ✅ Good: Use secret management
resource "azurerm_key_vault_secret" "connection_string" {
  name         = "database-connection-string"
  value        = var.database_connection_string
  key_vault_id = azurerm_key_vault.main.id
}

# App accessing secret via managed identity
data "azurerm_key_vault_secret" "connection_string" {
  name         = "database-connection-string"
  key_vault_id = azurerm_key_vault.main.id
}

# ❌ Bad: Hardcoded secrets
resource "azurerm_app_service" "main" {
  app_settings = {
    "ConnectionString" = "Server=...;Password=MySecretPassword123!"
  }
}
```

### Network Security
```hcl
# ✅ Good: Network segmentation
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

resource "azurerm_subnet_network_security_group_association" "database" {
  subnet_id                 = azurerm_subnet.database.id
  network_security_group_id = azurerm_network_security_group.database.id
}

# ❌ Bad: No network segmentation
# All resources in single subnet
# No NSGs configured
```

### Encryption
```hcl
# ✅ Good: Encryption enabled
resource "azurerm_storage_account" "main" {
  name                     = "${var.project_name}storage"
  location                 = azurerm_resource_group.main.location
  resource_group_name      = azurerm_resource_group.main.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  customer_managed_key {
    key_vault_key_id = azurerm_key_vault_key.main.id
  }
}

resource "azurerm_sql_server" "main" {
  name                         = "${var.project_name}-sql"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.admin_username
  administrator_login_password = var.admin_password
  
  # Encryption at rest enabled by default
}

# ❌ Bad: No encryption
# Storage without encryption
# Database without TDE
```

## Cost Management

### Resource Rightsizing
```hcl
# ✅ Good: Appropriate sizing with comments
resource "azurerm_app_service_plan" "main" {
  name                = "${var.project_name}-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  # S1 for production, B1 for dev
  # Based on: 1000 requests/second, 512MB memory requirement
  sku {
    tier = var.environment == "production" ? "Standard" : "Basic"
    size = var.environment == "production" ? "S1" : "B1"
  }
}

# ❌ Bad: Over-provisioning
resource "azurerm_app_service_plan" "main" {
  sku {
    tier = "Premium"
    size = "P2" # Overkill for this workload
  }
}
```

### Auto-Scaling
```hcl
# ✅ Good: Auto-scaling configured
resource "azurerm_monitor_autoscale_setting" "main" {
  name                = "${var.project_name}-autoscale"
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

## Compliance Requirements

### Resource Locks
```hcl
# ✅ Good: Protection for critical resources
resource "azurerm_resource_lock" "production" {
  name                 = "production-lock"
  scope                = azurerm_resource_group.production.id
  lock_level           = "CanNotDelete"
  notes                = "Production resources - requires approval for deletion"
}

# ❌ Bad: No locks on production
# Production resources can be deleted accidentally
```

### Audit Logging
```hcl
# ✅ Good: Diagnostic settings enabled
resource "azurerm_monitor_diagnostic_setting" "main" {
  name               = "${var.project_name}-diagnostics"
  target_resource_id = azurerm_app_service.main.id
  
  enabled_log {
    category = "AppServiceHTTPLogs"
    retention_policy {
      enabled = true
      days    = 90
    }
  }
  
  enabled_log {
    category = "AppServiceConsoleLogs"
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
- [ ] Security scanning in pipeline

### Cost
- [ ] Resources right-sized
- [ ] Auto-scaling enabled where appropriate
- [ ] Reserved instances considered
- [ ] Cost tags applied
- [ ] Unused resources removed

### Reliability
- [ ] Multi-AZ/region for production
- [ ] Backup enabled
- [ ] Monitoring configured
- [ ] Alerts defined
- [ ] Disaster recovery plan

## References

- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
- [Azure Terraform Best Practices](https://docs.microsoft.com/en-us/azure/developer/terraform/best-practices-planning)
- [AWS Terraform Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-best-practices/welcome.html)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
