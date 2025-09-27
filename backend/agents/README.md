# Autonomous Recruitment Agents

This directory contains Fetch.ai autonomous agents that handle various aspects of the recruitment process. Each agent is designed to work independently while coordinating with the main backend API and database.

## Agent Documentation Guidelines

When creating new agents, follow these documentation standards to ensure optimal discoverability and functionality across Agentverse and ASI:One platforms.

### Key Documentation Elements

#### 1. Descriptive Title
- Use specific, keyword-rich titles that clearly describe the agent's purpose
- Examples:
  - ✅ "Senior Software Engineer Candidate Sourcing Agent"
  - ✅ "Technical Interview Scheduling Coordinator Agent"
  - ❌ "RecruitmentBot"
  - ❌ "Agent1"

#### 2. Overview Section
Provide a clear 2-4 sentence summary covering:
- **Purpose**: What the agent does
- **Audience**: Who uses this agent (recruiters, hiring managers, candidates)
- **Key Capabilities**: Main functions and features
- **Integration**: How it connects with other system components

Example:
```
This autonomous sourcing agent specializes in discovering and engaging qualified candidates for technical roles. It targets recruiters and hiring managers seeking to automate the initial stages of talent acquisition. The agent searches multiple platforms, evaluates candidate fit using AI matching, and initiates personalized outreach campaigns via AgentMail. It integrates seamlessly with our PostgreSQL database and communicates with the main FastAPI backend for job configuration and status updates.
```

#### 3. Use Case Examples
Include 2-3 practical tasks the agent can perform:

**Example Use Cases:**
- **Automated Candidate Discovery**: Searches LinkedIn, GitHub, and job boards to find candidates matching specific technical requirements for a Senior Python Developer role
- **Personalized Outreach**: Sends tailored email sequences to discovered candidates, following up based on response patterns and engagement levels
- **Candidate Qualification**: Evaluates candidate profiles against job requirements and automatically schedules initial screening calls for promising matches

#### 4. Capabilities and APIs
Describe major functions in natural language:

**Core Capabilities:**
- **Multi-Platform Search**: Integrates with LinkedIn API, GitHub API, and various job boards to discover candidates
- **AI-Powered Matching**: Uses machine learning algorithms to score candidates against job requirements
- **Email Campaign Management**: Sends personalized outreach emails via AgentMail with automated follow-up sequences
- **Database Integration**: Logs all activities, candidate interactions, and results to PostgreSQL database
- **Real-time Status Updates**: Provides live updates on sourcing progress and candidate engagement metrics

**Input/Output Specifications:**
- **Input**: Job details (title, requirements, company info), search criteria, email templates
- **Output**: Candidate profiles, engagement metrics, email delivery status, activity logs

#### 5. Interaction Modes
Specify how the agent communicates:

- **Direct Message**: Receives job configuration and sourcing requests from backend API
- **ASI Chat Response**: Responds to status queries and provides sourcing updates
- **Webhook Integration**: Sends real-time notifications about candidate discoveries and email responses
- **Database Events**: Triggers on job posting updates and candidate profile changes

#### 6. Limitations and Scope
Clearly state what the agent does NOT do:

**Current Limitations:**
- Does not conduct technical interviews or assessments
- Cannot access private candidate information beyond public profiles
- Limited to email-based outreach (no phone calls or direct messaging)
- Requires manual approval for final candidate recommendations
- Operates only during business hours (9 AM - 6 PM EST)

#### 7. Relevant Keywords and Tags
Use consistent domain terms for better searchability:

**Primary Keywords:**
- candidate sourcing, talent acquisition, recruitment automation
- technical recruiting, software engineer hiring, developer recruitment
- LinkedIn automation, GitHub candidate search, job board integration
- email outreach, candidate engagement, recruitment AI

**Technical Tags:**
- `fetch-ai`, `uagents`, `agentmail`, `postgresql`, `fastapi`
- `candidate-sourcing`, `recruitment-automation`, `email-outreach`
- `linkedin-api`, `github-api`, `ai-matching`

### Documentation Template

```markdown
# [Agent Name]

## Overview
[2-4 sentence description of purpose, audience, capabilities, and integration]

## Use Cases
1. **[Use Case 1]**: [Detailed description]
2. **[Use Case 2]**: [Detailed description]  
3. **[Use Case 3]**: [Detailed description]

## Capabilities
- **[Capability 1]**: [Description and technical details]
- **[Capability 2]**: [Description and technical details]
- **[Capability 3]**: [Description and technical details]

## Interaction Modes
- **[Mode 1]**: [How agent receives requests/commands]
- **[Mode 2]**: [How agent provides responses/updates]
- **[Mode 3]**: [How agent integrates with external systems]

## Limitations
- [Specific limitation 1]
- [Specific limitation 2]
- [Specific limitation 3]

## Configuration
[Environment variables, API keys, and setup requirements]

## Dependencies
[List of required libraries and services]

## Keywords
`keyword1`, `keyword2`, `keyword3`, `keyword4`
```

### Best Practices

1. **Semantic Richness**: Write clear, informative content using natural language
2. **Markdown Format**: Use proper markdown formatting for better retrieval
3. **Consistent Terminology**: Use the same domain-specific terms throughout
4. **Placeholder Links**: Include intentional placeholders for future integration points
5. **English Language**: Write documentation in English for optimal platform compatibility
6. **Regular Updates**: Keep documentation current with agent capabilities

### Agent Development Checklist

Before deploying a new agent:

- [ ] Descriptive title with relevant keywords
- [ ] Clear overview section (2-4 sentences)
- [ ] 2-3 practical use case examples
- [ ] Detailed capabilities description
- [ ] Interaction modes specification
- [ ] Limitations and scope clearly defined
- [ ] Relevant keywords and tags included
- [ ] Configuration requirements documented
- [ ] Dependencies listed
- [ ] Code comments explaining major functions
- [ ] Error handling and logging implemented
- [ ] Database integration configured
- [ ] AgentMail integration tested

## Current Agents

### Sourcing Agent (`sourcing_agent.py`)
Autonomous candidate discovery and outreach agent that searches multiple platforms, evaluates candidate fit, and manages personalized email campaigns.

**Key Features:**
- Multi-platform candidate search (LinkedIn, GitHub, job boards)
- AI-powered candidate matching and scoring
- Automated email outreach via AgentMail
- Real-time activity logging and status updates
- Configurable search criteria and email templates

**Status**: Ready for deployment
**Dependencies**: uagents, agentmail, postgresql, linkedin-api, github-api

---

*For questions about agent development or documentation, please refer to the main project README or contact the development team.*
