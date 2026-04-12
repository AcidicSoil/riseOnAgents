---
name: cost-estimation
description: Cloud cost estimation and optimization. Use when estimating cloud infrastructure costs, comparing cloud providers, cost optimization strategies, or TCO analysis. Supports AWS, Azure, GCP pricing models.
license: Apache 2.0
---

# Cloud Cost Estimation

Cloud infrastructure cost estimation, optimization strategies, and Total Cost of Ownership (TCO) analysis for AWS, Azure, and GCP.

## When to Use This Skill

Use this skill when:
- Estimating cloud infrastructure costs for new projects
- Comparing cloud provider pricing (AWS vs Azure vs GCP)
- Cost optimization planning
- Total Cost of Ownership (TCO) analysis
- Budget planning for cloud migration
- Rightsizing recommendations
- Reserved Instance vs On-Demand analysis
- FinOps implementation

## Core Cost Categories

### 1. Compute Costs
**Instance Types:**
- General purpose (balanced CPU/memory)
- Compute optimized (high CPU)
- Memory optimized (high RAM)
- Storage optimized (high IOPS)
- GPU/FPGA (specialized workloads)

**Pricing Models:**
- On-Demand: Pay per hour/second
- Reserved Instances: 1-3 year commitment (up to 72% discount)
- Spot Instances: Unused capacity (up to 90% discount)
- Savings Plans: Commitment to usage ($/hour)

### 2. Storage Costs
**Storage Types:**
- Block Storage (EBS, Managed Disks)
- Object Storage (S3, Blob Storage)
- File Storage (EFS, Files)
- Archive Storage (Glacier, Archive)

**Cost Factors:**
- Storage capacity (GB/month)
- IOPS/throughput provisioned
- Data retrieval (for archive)
- Replication (multi-AZ, multi-region)

### 3. Network Costs
**Cost Components:**
- Data transfer out (egress)
- Data transfer in (usually free)
- Inter-region transfer
- Cross-AZ transfer
- CDN costs
- Load balancer costs

### 4. Database Costs
**Pricing Factors:**
- Instance size and type
- Storage (SSD vs HDD)
- IOPS provisioned
- Backup storage
- Multi-AZ replication
- Read replicas

### 5. Additional Services
- Monitoring and logging
- Security services
- Management tools
- Serverless functions
- Container orchestration
- AI/ML services

## Cost Estimation Framework

### Step 1: Requirements Gathering
**Workload Profile:**
- Compute: CPU, memory, storage per instance
- Quantity: Number of instances per tier
- Availability: Single-AZ, Multi-AZ, Multi-region
- Traffic: Data transfer estimates (GB/month)
- Database: Size, IOPS, throughput
- Storage: Capacity, access patterns

### Step 2: Resource Mapping
| Component | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| **VMs** | EC2 | Virtual Machines | Compute Engine |
| **Object Storage** | S3 | Blob Storage | Cloud Storage |
| **Block Storage** | EBS | Managed Disks | Persistent Disks |
| **Database** | RDS | SQL Database | Cloud SQL |
| **Load Balancer** | ELB/ALB | Load Balancer | Cloud Load Balancing |
| **CDN** | CloudFront | CDN | Cloud CDN |

### Step 3: Cost Calculation
**Formula:**
```
Total Monthly Cost = 
  (Compute × Hours × Price) +
  (Storage × GB × Price) +
  (Network × GB × Price) +
  (Database × Hours × Price) +
  (Services × Usage × Price)
```

### Step 4: TCO Analysis
**Time Horizon:** 3-5 years
**Components:**
- Infrastructure costs
- Operational costs (staff, tools)
- Migration costs
- Training costs
- Downtime costs
- Opportunity costs

## Pricing Comparison (Sample)

### Compute (General Purpose, 4 vCPU, 16GB RAM)
| Provider | Instance | On-Demand | Reserved (1yr) | Spot |
|----------|----------|-----------|----------------|------|
| **AWS** | m5.xlarge | ~$0.192/hr | ~$0.12/hr | ~$0.06/hr |
| **Azure** | D4s v3 | ~$0.192/hr | ~$0.12/hr | ~$0.06/hr |
| **GCP** | n1-standard-4 | ~$0.190/hr | ~$0.12/hr | ~$0.05/hr |

### Storage (Object Storage, Standard)
| Provider | Service | Price/GB/Month | Egress/GB |
|----------|---------|----------------|-----------|
| **AWS** | S3 Standard | ~$0.023 | $0.09 |
| **Azure** | Hot Blob | ~$0.0184 | $0.087 |
| **GCP** | Cloud Storage | ~$0.020 | $0.12 |

### Database (Managed PostgreSQL, 4 vCPU, 15GB RAM, 100GB)
| Provider | Service | Price/Hour | Monthly |
|----------|---------|------------|---------|
| **AWS** | RDS db.m5.large | ~$0.171 | ~$125 |
| **Azure** | SQL Database | ~$0.215 | ~$157 |
| **GCP** | Cloud SQL | ~$0.177 | ~$129 |

## Cost Optimization Strategies

### 1. Rightsizing
**Process:**
1. Monitor actual utilization
2. Compare to instance capacity
3. Downsize over-provisioned instances
4. Use automation tools

**Tools:**
- AWS Trusted Advisor
- Azure Advisor
- GCP Recommender

### 2. Reserved Instances
**When to Use:**
- Predictable, steady-state workloads
- Minimum 1-year horizon
- Production databases
- Core infrastructure

**ROI Calculation:**
```
Breakeven (months) = (Reserved Cost - On-Demand Cost) / Monthly Savings
Example:
  On-Demand: $1,000/month
  Reserved (1yr): $7,000 upfront
  Monthly Savings: $300
  Breakeven: $7,000 / $300 = 23 months
```

### 3. Spot Instances
**Best Use Cases:**
- Batch processing
- CI/CD pipelines
- Development environments
- Stateless workloads
- Fault-tolerant applications

**Strategy:**
- Use diverse instance types
- Implement checkpointing
- Handle interruptions gracefully

### 4. Auto-Scaling
**Benefits:**
- Match capacity to demand
- Reduce idle resources
- Handle traffic spikes

**Configuration:**
- Scale-up threshold: 70% CPU
- Scale-down threshold: 30% CPU
- Cooldown period: 5 minutes

### 5. Storage Optimization
**Strategies:**
- Lifecycle policies (move to cheaper tiers)
- Compression and deduplication
- Archive old data
- Delete unused volumes
- Use appropriate storage class

### 6. Data Transfer Optimization
**Strategies:**
- Minimize cross-AZ traffic
- Use VPC endpoints
- Implement CDN for static content
- Compress data
- Batch transfers

## FinOps Best Practices

### Three Phases of FinOps
1. **Inform**: Visibility and allocation
   - Tag all resources
   - Allocate costs to teams
   - Create dashboards

2. **Optimize**: Reduce waste
   - Rightsizing
   - Reserved capacity
   - Eliminate idle resources

3. **Operate**: Continuous improvement
   - Budgets and alerts
   - Chargeback/showback
   - Regular reviews

### Key Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| **Cost per Transaction** | Total Cost / Transactions | Decreasing trend |
| **Cost per User** | Total Cost / Active Users | Decreasing trend |
| **Cloud Waste** | Idle Resources / Total Cost | < 10% |
| **Reserved Coverage** | Reserved / Total Compute | > 70% for steady-state |

## Cost Estimation Template

```markdown
# Cost Estimation for {Project}

## Workload Requirements
- Application servers: {count} × {instance type}
- Database: {instance type}, {storage}GB, {IOPS} IOPS
- Storage: {object storage}GB, {block storage}GB
- Data transfer: {egress}GB/month
- Users: {concurrent users} concurrent, {daily active users} DAU

## Provider Comparison

### AWS
- Compute: ${amount}/month
- Database: ${amount}/month
- Storage: ${amount}/month
- Network: ${amount}/month
- **Total: ${amount}/month**

### Azure
- Compute: ${amount}/month
- Database: ${amount}/month
- Storage: ${amount}/month
- Network: ${amount}/month
- **Total: ${amount}/month**

### GCP
- Compute: ${amount}/month
- Database: ${amount}/month
- Storage: ${amount}/month
- Network: ${amount}/month
- **Total: ${amount}/month**

## Optimization Opportunities
1. Reserved Instances: Save {percentage}% (${amount}/month)
2. Rightsizing: Save {percentage}% (${amount}/month)
3. Spot Instances: Save {percentage}% (${amount}/month)
4. Storage Lifecycle: Save {percentage}% (${amount}/month)

## TCO (3 Years)
- Year 1: ${amount}
- Year 2: ${amount} (with {growth}% growth)
- Year 3: ${amount} (with {growth}% growth)
- **Total: ${amount}**

## Budget Recommendation
- Monthly budget: ${amount}
- Contingency (15%): ${amount}
- **Total recommended: ${amount}/month**
```

## Cost Monitoring

### Daily Checks
- Cost anomalies
- Budget alerts
- Resource changes

### Weekly Reviews
- Cost trends
- Optimization opportunities
- Tagging compliance

### Monthly Reports
- Actual vs budget
- Cost allocation by team/project
- Optimization progress
- Forecast vs actual

### Tools
- **AWS**: Cost Explorer, Budgets, Cost Anomaly Detection
- **Azure**: Cost Management, Budgets, Advisor
- **GCP**: Cost Management, Budgets, Recommender
- **Third-party**: CloudHealth, Cloudability, Datadog

## Common Cost Pitfalls

### Avoid These Mistakes
- ❌ Not tagging resources
- ❌ Ignoring data transfer costs
- ❌ Over-provisioning "just in case"
- ❌ Not using reserved capacity for steady workloads
- ❌ Leaving idle resources running
- ❌ Not monitoring costs regularly
- ❌ Multi-AZ without understanding cost impact
- ❌ Not implementing lifecycle policies
- ❌ Using default storage classes
- ❌ Not rightsizing after deployment

## Output Format

When using this skill, create:

1. **Cost Estimation Report** (`/docs/finance/{project}_CostEstimation.md`)
   - Provider comparison
   - Resource breakdown
   - Monthly and TCO estimates

2. **Optimization Plan** (`/docs/finance/{project}_Optimization.md`)
   - Identified savings opportunities
   - Implementation priorities
   - ROI calculations

3. **Budget Recommendation** (`/docs/finance/{project}_Budget.md`)
   - Monthly budget
   - Team allocations
   - Alert thresholds

## Best Practices

1. **Tag Everything**: Enable cost allocation
2. **Monitor Daily**: Catch anomalies early
3. **Review Monthly**: Regular optimization
4. **Use Automation**: Auto-scaling, lifecycle policies
5. **Right-size Continuously**: Workloads change
6. **Commit Wisely**: Reserved for predictable workloads
7. **Consider TCO**: Look beyond infrastructure costs
8. **Implement FinOps**: Culture of cost ownership

## References

- [AWS Pricing Calculator](https://calculator.aws/)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)
- [FinOps Foundation](https://www.finops.org/)
- [AWS Well-Architected Cost Optimization](https://wa.aws.amazon.com/wat.pillar.costoptimization.en.html)
- [Cloud Cost Optimization Strategies](https://aws.amazon.com/blogs/aws/category/cost-optimization/)

### MCP Interactions
- **GitHub MCP**: Search repository for previous similar actions or related PRs before executing this skill.
- **Brave Search MCP**: Validate current patterns against the live internet if the context is sparse.
- **Context7 MCP**: Extract deep architectural/domain context relevant to the skill's execution.
