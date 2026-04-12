---
name: cloud-cost-optimization
description: Cloud cost optimization strategies for AWS, Azure, and GCP. Use for cost analysis, right-sizing, reserved instances, and cost governance.
---

# Cloud Cost Optimization

A comprehensive guide to cloud cost optimization strategies across AWS, Azure, and GCP.

---

## When to Use This Skill

Use this skill when:
- Analyzing cloud spending
- Optimizing resource costs
- Planning reserved capacity
- Implementing cost governance
- Right-sizing resources
- Creating cost allocation strategies

---

## Cost Optimization Framework

### Pillar 1: Right-Sizing
**Goal:** Match resource capacity to actual usage

**Actions:**
- Analyze utilization metrics (CPU, memory, disk, network)
- Downsize over-provisioned resources
- Upsize under-provisioned resources (avoid performance issues)
- Use automated scaling where possible

### Pillar 2: Purchasing Options
**Goal:** Leverage discounted pricing models

**Actions:**
- Reserved Instances / Savings Plans for steady workloads
- Spot / Preemptible instances for fault-tolerant workloads
- Committed use discounts for predictable usage
- Enterprise agreements for large organizations

### Pillar 3: Architecture Optimization
**Goal:** Design cost-efficient architectures

**Actions:**
- Use managed services vs. self-managed
- Implement auto-scaling
- Use serverless for variable workloads
- Optimize data transfer costs

### Pillar 4: Governance
**Goal:** Maintain cost discipline

**Actions:**
- Implement tagging strategy
- Set up budgets and alerts
- Regular cost reviews
- Chargeback/showback to teams

---

## Right-Sizing Patterns

### Compute Right-Sizing

#### Analysis Metrics
| Metric | Optimal Range | Action if Outside |
|--------|---------------|-------------------|
| CPU Utilization | 40-70% | <40%: Downsize, >70%: Upsize |
| Memory Utilization | 50-80% | <50%: Downsize, >80%: Upsize |
| Network | <70% of limit | >70%: Consider network optimization |
| Disk IOPS | <70% of provisioned | >70%: Increase IOPS or optimize queries |

#### Azure Right-Sizing
```hcl
# Before: Over-provisioned
resource "azurerm_app_service_plan" "main" {
  sku {
    tier = "Premium"
    size = "P2"  # $342/month
  }
}

# After: Right-sized based on metrics
resource "azurerm_app_service_plan" "main" {
  sku {
    tier = "Standard"  # Based on actual usage
    size = "S1"        # $74.90/month (78% savings)
  }
}
```

#### AWS Right-Sizing
```hcl
# Before: Over-provisioned
resource "aws_instance" "main" {
  instance_type = "m5.2xlarge"  # $280/month
}

# After: Right-sized
resource "aws_instance" "main" {
  instance_type = "m5.large"  # $70/month (75% savings)
}
```

### Auto-Scaling Configuration

#### Azure Auto-Scaling
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
    
    rule {
      metric_trigger {
        metric_name  = "CpuPercentage"
        statistic    = "Average"
        time_window  = "PT10M"
        operator     = "LessThan"
        threshold    = 30
      }
      
      scale_action {
        direction    = "Decrease"
        type         = "ChangeCount"
        value        = "1"
        cooldown     = "PT10M"
      }
    }
  }
}
```

#### AWS Auto-Scaling
```hcl
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "${var.project}-scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.project}-cpu-high"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 70
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.main.name
  }
  
  alarm_actions = [aws_autoscaling_policy.scale_up.arn]
}
```

---

## Purchasing Options

### Reserved Instances / Savings Plans

#### When to Use
| Workload Pattern | Recommendation | Potential Savings |
|-----------------|----------------|-------------------|
| Steady state (24/7) | Reserved Instances (3-year) | Up to 72% |
| Steady state (24/7) | Savings Plans (3-year) | Up to 72% |
| Predictable baseline | Reserved Instances (1-year) | Up to 50% |
| Variable with baseline | Savings Plans + On-Demand | Up to 50% |

#### Azure Reserved VM Instances
```hcl
# Reservation for predictable workloads
# Purchase via Azure Portal or API
# Example savings calculation:

# On-Demand: 10 × D4s v3 × $140/month = $1,400/month
# Reserved (1-year): 10 × D4s v3 × $85/month = $850/month
# Savings: $550/month (39%)
```

#### AWS Savings Plans
```hcl
# Compute Savings Plans
# - Flexible across instance families
# - Flexible across regions
# - Commitment: $10/hour for 3 years
# - Savings: Up to 66% vs On-Demand

# EC2 Instance Savings Plans
# - Specific instance family in a region
# - Higher savings but less flexible
# - Commitment: $10/hour for 3 years
# - Savings: Up to 72% vs On-Demand
```

### Spot / Preemptible Instances

#### Use Cases
| Workload Type | Spot Suitable | Considerations |
|--------------|---------------|----------------|
| Batch processing | ✅ Yes | Can be interrupted |
| CI/CD runners | ✅ Yes | Retry on interruption |
| Dev/Test environments | ✅ Yes | Not for production |
| Stateless web servers | ⚠️ Maybe | Need graceful handling |
| Databases | ❌ No | Stateful, need persistence |
| Production critical | ❌ No | Unpredictable eviction |

#### Azure Spot VMs
```hcl
resource "azurerm_linux_virtual_machine" "spot" {
  name                = "${var.project}-spot-vm"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  size                = "Standard_D4s_v3"
  priority            = "Spot"
  
  eviction_policy     = "Deallocate"
  max_bid_price       = -1  # Maximum willing to pay (-1 = don't be evicted for price)
  
  # Handle eviction gracefully
  user_data = base64encode(templatefile("${path.module}/scripts/spot-handler.sh", {
    graceful_shutdown = true
  }))
}
```

#### AWS Spot Instances
```hcl
resource "aws_spot_instance_request" "spot" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "m5.large"
  spot_price             = "0.05"  # Maximum bid price
  wait_for_fulfillment   = true
  
  # Handle interruption
  user_data = <<-EOF
    #!/bin/bash
    # Spot interruption handler
    curl http://169.254.169.254/latest/meta-data/spot/termination-time
  EOF
  
  interruptible          = true
}
```

---

## Serverless Patterns

### When to Use Serverless

| Workload Characteristic | Serverless Suitable | Cost Impact |
|------------------------|---------------------|-------------|
| Variable/unpredictable traffic | ✅ Yes | Pay only for usage |
| Low average utilization (<30%) | ✅ Yes | No idle cost |
| Event-driven processing | ✅ Yes | No always-on cost |
| Steady high utilization (>70%) | ❌ No | VMs cheaper |
| Long-running processes | ❌ No | Timeout limits |
| Consistent baseline | ❌ No | Reserved cheaper |

### Azure Functions Cost Optimization
```hcl
# Consumption Plan (pay per execution)
resource "azurerm_app_service_plan" "consumption" {
  kind     = "FunctionApp"
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

# Premium Plan (for predictable workloads)
resource "azurerm_app_service_plan" "premium" {
  kind     = "FunctionApp"
  sku {
    tier = "Premium"
    size = "EP1"
  }
}
```

### AWS Lambda Cost Optimization
```hcl
# Memory optimization (affects both compute and duration cost)
resource "aws_lambda_function" "optimized" {
  function_name = "${var.project}-function"
  runtime       = "python3.9"
  handler       = "index.handler"
  
  # Right-size memory based on profiling
  memory_size = 512  # Not default 128MB if needed
  
  # Timeout optimization
  timeout = 30  # Not default 3 seconds if needed
}
```

---

## Storage Cost Optimization

### Storage Tiering

#### Azure Blob Storage Tiers
| Tier | Use Case | Cost/GB | Access Cost |
|------|----------|---------|-------------|
| Hot | Frequently accessed | $0.0184 | Low |
| Cool | Infrequently accessed (<30 days) | $0.01 | Medium |
| Archive | Rarely accessed (>180 days) | $0.00099 | High |

```hcl
# Lifecycle management for automatic tiering
resource "azurerm_storage_account" "main" {
  # ...
  
  blob_properties {
    change_feed_enabled = true
    
    delete_retention_policy {
      days = 30
    }
  }
}

resource "azurerm_storage_management_policy" "main" {
  storage_account_id = azurerm_storage_account.main.id
  
  rule {
    name    = "archive-old-blobs"
    enabled = true
    type    = "Blob"
    
    actions {
      base_blob {
        tier_to_cool_after_days_since_modification_greater_than = 30
        tier_to_archive_after_days_since_modification_greater_than = 90
      }
    }
    
    filters {
      blob_types = ["block_blob"]
    }
  }
}
```

#### AWS S3 Lifecycle
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id
  
  rule {
    id     = "archive-old-objects"
    status = "Enabled"
    
    transition {
      days          = 30
      storage_class = "STANDARD_IA"  # Infrequent Access
    }
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    
    expiration {
      days = 365  # Delete after 1 year
    }
  }
}
```

---

## Cost Allocation & Governance

### Tagging Strategy

#### Required Tags
| Tag | Purpose | Example Values |
|-----|---------|----------------|
| `Environment` | Cost allocation | `dev`, `staging`, `prod` |
| `CostCenter` | Billing | `cc-12345`, `engineering` |
| `Project` | Project tracking | `myapp`, `website` |
| `Owner` | Responsibility | `team-platform`, `john.doe` |
| `ManagedBy` | IaC identification | `Terraform`, `Manual` |

#### Tag Enforcement
```hcl
resource "azurerm_policy_definition" "require_tags" {
  name         = "require-resource-tags"
  policy_type  = "Custom"
  mode         = "All"
  display_name = "Require tags on all resources"
  
  policy_rule = jsonencode({
    if = {
      anyOf = [
        { field = "tags['Environment']", exists = false },
        { field = "tags['CostCenter']", exists = false },
        { field = "tags['Owner']", exists = false }
      ]
    }
    then = {
      effect = "deny"
    }
  })
}
```

### Budget Alerts

#### Azure Budget
```hcl
resource "azurerm_consumption_budget" "main" {
  name              = "${var.project}-budget"
  resource_group_id = azurerm_resource_group.main.id
  amount            = 1000  # Monthly budget
  time_grain        = "Monthly"
  
  notification {
    enabled       = true
    threshold     = 50  # Alert at 50% of budget
    operator        = "EqualTo"
    contact_emails  = ["team@example.com"]
  }
  
  notification {
    enabled       = true
    threshold     = 80  # Alert at 80% of budget
    operator        = "EqualTo"
    contact_emails  = ["team@example.com", "manager@example.com"]
  }
  
  notification {
    enabled       = true
    threshold     = 100  # Alert at 100% of budget
    operator        = "EqualTo"
    contact_emails  = ["team@example.com", "manager@example.com", "exec@example.com"]
  }
}
```

#### AWS Budget
```hcl
resource "aws_budgets_budget" "main" {
  name              = "${var.project}-budget"
  budget_type       = "COST"
  limit_amount      = "1000.0"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["team@example.com"]
  }
  
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["team@example.com", "manager@example.com"]
  }
}
```

---

## Cost Estimation Template

```markdown
# Cost Estimation: {Project Name}

## Monthly Cost Breakdown

### Compute
| Resource | Quantity | Unit Cost | Monthly Cost |
|----------|----------|-----------|--------------|
| App Service (S1) | 2 | $74.90 | $149.80 |
| Azure Functions | ~1M exec | ~$0.20/1M | $50.00 |

### Storage
| Resource | Quantity | Unit Cost | Monthly Cost |
|----------|----------|-----------|--------------|
| Blob Storage (100 GB) | 100 GB | $0.0184/GB | $1.84 |
| SQL Database (Basic) | 1 | $5.00 | $5.00 |

### Networking
| Resource | Quantity | Unit Cost | Monthly Cost |
|----------|----------|-----------|--------------|
| Load Balancer | 1 | $18.25 | $18.25 |
| Bandwidth (10 GB) | 10 GB | $0.087/GB | $0.87 |

### Monitoring
| Resource | Quantity | Unit Cost | Monthly Cost |
|----------|----------|-----------|--------------|
| Application Insights | ~1GB | ~$25/GB | $25.00 |

### Total Estimated Monthly Cost: ~$250.76

## Cost Optimization Opportunities
1. Reserved Instances: Save 39% on App Service (~$58/month)
2. Auto-scaling: Reduce instances during off-peak (~$30/month)
3. Storage tiering: Archive old blobs (~$1/month)

**Potential Monthly Savings: ~$89 (35%)**
```

---

## Related Skills

- **infrastructure-as-code-patterns** — IaC cost tagging
- **ci-cd-patterns** — Pipeline cost optimization
- **security-audit-checklist** — Security vs cost trade-offs

---

## Output Format

When using this skill, provide:
1. **Current cost analysis** with breakdown
2. **Right-sizing recommendations** with savings
3. **Purchasing options** analysis (RI, spot, etc.)
4. **Architecture optimization** suggestions
5. **Governance implementation** (tags, budgets, alerts)
6. **Cost estimation** for proposed changes
7. **ROI analysis** for optimization efforts
