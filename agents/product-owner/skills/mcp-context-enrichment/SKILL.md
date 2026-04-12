---
name: mcp-context-enrichment
description: Skills for using MCP tools to enrich architectural analysis with external context. Use when researching patterns, gathering documentation, analyzing codebases, or accessing organizational knowledge.
---

## What I do

I provide guidance on which MCP tools to use for different types of context enrichment during architectural work. I help select the right tool for:
- Web research and latest patterns
- Documentation lookup
- Codebase analysis
- Organizational context
- Microsoft technology research

## When to use me

Use this skill when you need to:
- Research architectural patterns and best practices
- Find documentation for technologies or frameworks
- Analyze existing repository structures
- Gather context about organizational standards
- Look up Microsoft technology documentation
- Search for latest industry trends and patterns

## MCP Selection Guide

### Web Research and Pattern Discovery

**Use: brave-search**

When to use:
- Searching for latest architectural patterns and trends
- Finding best practices for specific technologies
- Researching industry standards (OWASP, ISO, etc.)
- Looking for comparison between technology options
- Finding tutorials or guides on specific topics

Example triggers:
- "What are the latest microservices patterns?"
- "Compare API gateway solutions"
- "Find OWASP security recommendations"

### Documentation and Project Research

**Use: brave-search or context7**

When to use brave-search:
- Public documentation lookup
- General technology documentation
- Open-source project research
- Community best practices

When to use context7:
- Internal organizational documentation
- Project-specific context (RFCs, ADRs, guidelines)
- Team-specific conventions and standards
- Enterprise architecture decisions

Example triggers:
- "Find documentation for Kubernetes networking"
- "Look up our team's API design standards"
- "Check existing ADRs for authentication approach"

### Microsoft Technology Research

**Use: microsoft-learn**

When to use:
- Azure architecture and services
- .NET, C#, ASP.NET Core documentation
- Microsoft 365, Teams, Power Platform
- Azure DevOps, GitHub Actions
- Microsoft identity and security frameworks

Example triggers:
- "Azure architecture best practices"
- ".NET 8 performance optimization"
- "Azure Kubernetes Service networking"
- "Microsoft identity platform patterns"

### Codebase and Repository Analysis

**Use: github**

When to use:
- Analyzing existing code structure
- Finding patterns in current codebase
- Checking repository for existing implementations
- Analyzing commit history and decisions
- Finding related projects or libraries

Example triggers:
- "Find similar implementations in the codebase"
- "Check how authentication is done in other services"
- "Analyze the existing domain model structure"

## How to invoke

When you need context enrichment, use the appropriate MCP:

1. **brave-search** for web research:
   ```
   Use web search to find latest documentation and patterns
   ```

2. **context7** for organizational context:
   ```
   Use context7 to query organizational documentation and decisions
   ```

3. **microsoft-learn** for Microsoft tech:
   ```
   Use microsoft-learn to find official Microsoft documentation
   ```

4. **github** for codebase analysis:
   ```
   Use github MCP to analyze repository structure and code
   ```

## Best Practices

- Always use the most specific tool for your need
- Prefer context7 over brave-search for internal knowledge
- Use microsoft-learn for official Microsoft documentation
- Use github MCP before writing new code to find existing patterns
- Chain MCPs when needed (e.g., find pattern with brave-search, then check internal docs with context7)

## Example Workflows

### Architecture Research
1. Use brave-search to find latest patterns
2. Use context7 to check internal standards
3. Use microsoft-learn for Microsoft-specific guidance
4. Use github to analyze existing implementations

### ADR Creation
1. Use context7 to find related ADRs
2. Use brave-search for industry patterns
3. Use github to find supporting examples in codebase
