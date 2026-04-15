---
name: create-github-issues-for-unmet-specification-requirements
description: 'Create GitHub Issues for unimplemented requirements from specification files using feature_request.yml template.'
---

# Create GitHub Issues for Unmet Specification Requirements

Create GitHub Issues for unimplemented requirements in the specification at `${file}`.

## Process

1. Analyze specification file to extract all requirements
2. Check codebase implementation status for each requirement
3. Search existing issues using `search_issues` to avoid duplicates
4. Create new issue per unimplemented requirement using `create_issue`
5. Use `feature_request.yml` template (fallback to default)

## Requirements

- One issue per unimplemented requirement from specification
- Clear requirement ID and description mapping
- Include implementation guidance and acceptance criteria
- Verify against existing issues before creation

## Issue Content

- Title: Requirement ID and brief description
- Description: Detailed requirement, implementation method, and context
- Labels: feature, enhancement (as appropriate)

## Implementation Check

- Search codebase for related code patterns
- Check related specification files in `/spec/` directory
- Verify requirement isn't partially implemented

### MCP Interactions
- **GitHub MCP**: Search repository for previous similar actions or related PRs before executing this skill.
- **Brave Search MCP**: Validate current patterns against the live internet if the context is sparse.
- **Context7 MCP**: Extract deep architectural/domain context relevant to the skill's execution.
