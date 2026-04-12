---
description: CI/CD pipeline rules and guidelines for GitHub Actions, Azure DevOps, GitLab CI, and deployment automation
applyTo: '**/.github/workflows/**,**/azure-pipelines.yml,**/.gitlab-ci.yml'
---

# CI/CD Rules

CI/CD pipeline rules and guidelines for GitHub Actions, Azure DevOps, GitLab CI, and deployment automation.

## Pipeline Standards

### General Pipeline Principles
✅ **All pipelines must:**
- Be defined in code (YAML)
- Be version controlled in Git
- Go through pull request review
- Run on every commit/PR
- Include security scanning
- Have proper error handling
- Send notifications on failure
- Be documented

### Pipeline Stages
✅ **Standard stages:**
1. **Validate**: Build and compile
2. **Test**: Unit, integration, E2E tests
3. **Security**: SAST, DAST, dependency scanning
4. **Package**: Build artifacts/containers
5. **Deploy Staging**: Deploy to staging environment
6. **Integration**: Integration tests
7. **Deploy Production**: Deploy to production (with approval)
8. **Smoke Tests**: Production verification

## GitHub Actions Best Practices

### Workflow Structure
```yaml
# ✅ Good: Well-organized workflow
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  DOTNET_VERSION: '8.0.x'
  NODE_VERSION: '18.x'

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ env.DOTNET_VERSION }}
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.nuget/packages
          key: ${{ runner.os }}-nuget-${{ hashFiles('**/packages.lock.json') }}
          restore-keys: |
            ${{ runner.os }}-nuget-
      
      - name: Restore
        run: dotnet restore
      
      - name: Build
        run: dotnet build --configuration Release --no-restore
      
      - name: Test
        run: dotnet test --configuration Release --no-build --collect:"XPlat Code Coverage"
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: '**/coverage.cobertura.xml'
          fail_ci_if_error: false

  security:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          format: 'sarif'
          output: 'trivy-results.sarif'

  deploy:
    needs: [build, security]
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy
        run: ./scripts/deploy.sh
        env:
          AZURE_CREDENTIALS: ${{ secrets.AZURE_CREDENTIALS }}
```

### Secrets Management
```yaml
# ✅ Good: Secrets in vault
steps:
  - name: Deploy
    run: ./deploy.sh
    env:
      DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
      API_KEY: ${{ secrets.API_KEY }}
      AZURE_CREDENTIALS: ${{ secrets.AZURE_CREDENTIALS }}

# ❌ Bad: Hardcoded secrets
steps:
  - name: Deploy
    run: |
      export DB_PASSWORD="MySecretPassword123"
      ./deploy.sh
```

### Matrix Builds
```yaml
# ✅ Good: Matrix for multiple configurations
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        dotnet: ['6.0.x', '7.0.x', '8.0.x']
        exclude:
          - os: macos-latest
            dotnet: '6.0.x'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ matrix.dotnet }}
      
      - name: Test
        run: dotnet test
```

### Caching
```yaml
# ✅ Good: Cache dependencies
steps:
  - name: Cache NuGet packages
    uses: actions/cache@v3
    with:
      path: ~/.nuget/packages
      key: ${{ runner.os }}-nuget-${{ hashFiles('**/packages.lock.json') }}
      restore-keys: |
        ${{ runner.os }}-nuget-
  
  - name: Cache node modules
    uses: actions/cache@v3
    with:
      path: node_modules
      key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-

# ❌ Bad: No caching
# Dependencies downloaded on every run
```

## Deployment Strategies

### Blue-Green Deployment
```yaml
# ✅ Blue-green deployment
jobs:
  deploy-blue-green:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to green slot
        run: |
          az webapp deployment slot swap \
            --resource-group ${{ secrets.RG }} \
            --name ${{ secrets.APP_NAME }} \
            --slot green \
            --target-slot production
      
      - name: Verify deployment
        run: ./scripts/smoke-tests.sh
      
      - name: Swap if successful
        run: |
          az webapp deployment slot swap \
            --resource-group ${{ secrets.RG }} \
            --name ${{ secrets.APP_NAME }} \
            --slot green \
            --target-slot production
      
      - name: Rollback on failure
        if: failure()
        run: |
          az webapp deployment slot swap \
            --resource-group ${{ secrets.RG }} \
            --name ${{ secrets.APP_NAME }} \
            --slot production \
            --target-slot green
```

### Canary Deployment
```yaml
# ✅ Canary deployment
jobs:
  canary:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to 10% of traffic
        run: |
          kubectl set image deployment/app app=myapp:${{ github.sha }} --namespace=production
          kubectl patch service/app -p '{"spec":{"selector":{"canary":"true"}}}' --namespace=production
      
      - name: Monitor metrics for 10 minutes
        run: |
          ./scripts/monitor-canary.sh --duration=600
      
      - name: Promote canary
        if: success()
        run: |
          kubectl set image deployment/app app=myapp:${{ github.sha }} --namespace=production
          kubectl patch service/app -p '{"spec":{"selector":{"canary":"false"}}}' --namespace=production
      
      - name: Rollback canary
        if: failure()
        run: |
          kubectl rollout undo deployment/app --namespace=production
```

### Rolling Update
```yaml
# ✅ Rolling update with health checks
jobs:
  rolling-update:
    runs-on: ubuntu-latest
    steps:
      - name: Start rolling update
        run: |
          kubectl set image deployment/app app=myapp:${{ github.sha }} --namespace=production
      
      - name: Monitor rollout
        run: |
          kubectl rollout status deployment/app --namespace=production --timeout=600s
      
      - name: Verify deployment
        run: |
          ./scripts/health-check.sh --endpoint=https://app.example.com/health
      
      - name: Rollback if needed
        if: failure()
        run: |
          kubectl rollout undo deployment/app --namespace=production
```

## Security in CI/CD

### Security Scanning
```yaml
# ✅ Comprehensive security scanning
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Dependency scanning
        uses: snyk/actions/dotnet@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        continue-on-error: true
      
      - name: Container scanning
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Code scanning
        uses: github/codeql-action/analyze@v2
        with:
          languages: 'csharp'
      
      - name: Upload security results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### Protected Environments
```yaml
# ✅ Environment protection
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy
        run: ./deploy.sh

# Environment settings (configured in GitHub):
# - Required reviewers: 2
# - Wait timer: 5 minutes
# - Deployment branches: main only
```

## Pipeline Metrics

### Performance Targets
```markdown
## Pipeline Performance Targets
- **Build Time**: < 5 minutes
- **Test Time**: < 10 minutes
- **Security Scan**: < 5 minutes
- **Deployment**: < 5 minutes
- **Total Pipeline**: < 25 minutes

## Quality Gates
- Code coverage > 80%
- No critical security vulnerabilities
- No high security vulnerabilities
- All tests passing
- Build successful
- No linting errors
```

### Monitoring
```yaml
# ✅ Pipeline monitoring
name: Pipeline Metrics
on:
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]

jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Calculate metrics
        run: |
          echo "Build Duration: ${{ needs.build.outputs.duration }}"
          echo "Test Duration: ${{ needs.test.outputs.duration }}"
          echo "Coverage: ${{ needs.test.outputs.coverage }}"
      
      - name: Send to monitoring
        run: |
          curl -X POST ${{ secrets.MONITORING_WEBHOOK }} \
            -d '{
              "duration": "${{ github.job }}",
              "status": "${{ job.status }}",
              "workflow": "${{ github.workflow }}"
            }'
```

## Quality Checklist

### Pipeline Quality
- [ ] Pipeline executes successfully
- [ ] Tests run on every commit
- [ ] Security scanning enabled
- [ ] Deployments automated
- [ ] Approval gates for production
- [ ] Rollback procedures defined
- [ ] Notifications configured
- [ ] Metrics tracked

### Security
- [ ] Secrets in vault (not in code)
- [ ] Least privilege for service accounts
- [ ] Security scanning in pipeline
- [ ] Artifact signing
- [ ] Dependency updates automated
- [ ] Pipeline access restricted

### Reliability
- [ ] Timeout configured
- [ ] Retry logic for flaky steps
- [ ] Error handling implemented
- [ ] Caching for dependencies
- [ ] Matrix builds for testing
- [ ] Parallel execution where possible

### Performance
- [ ] Build time < 5 minutes
- [ ] Test time < 10 minutes
- [ ] Dependencies cached
- [ ] Parallel test execution
- [ ] Incremental builds
- [ ] Docker layer caching

## Common Patterns

### Pull Request Validation
```yaml
name: PR Validation
on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: dotnet build
      - name: Test
        run: dotnet test
      - name: Lint
        run: dotnet format --verify-no-changes
      - name: Security Scan
        run: dotnet list package --vulnerable
```

### Scheduled Maintenance
```yaml
name: Weekly Maintenance
on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Update dependencies
        run: dotnet outdate --fail-on-outdated
      
      - name: Create PR
        uses: peter-evans/create-pull-request@v5
        with:
          title: 'chore: update dependencies'
          branch: 'chore/update-dependencies'
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [GitLab CI Documentation](https://docs.gitlab.com/ee/ci/)
- [Continuous Delivery](https://continuousdelivery.com/) - Jez Humble, David Farley
- [Accelerate](https://www.oreilly.com/library/view/accelerate/9781484236765/) - Nicole Forsgren

## Remember

- You are implementing CI/CD pipelines
- **Automate everything** - manual steps are error-prone
- **Fast feedback** - developers should know quickly
- **Security** - scan for vulnerabilities in every build
- **Reliability** - pipelines should be reproducible
- **Metrics** - measure and improve pipeline performance
- **Documentation** - document procedures and runbooks
