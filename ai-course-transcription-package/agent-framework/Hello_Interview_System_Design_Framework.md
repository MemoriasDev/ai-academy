# Hello Interview System Design Framework

**Source:** Hello Interview YouTube Channel - URL Shortener Tutorial  
**Generated from:** Whisper transcription analysis  
**Purpose:** Enterprise-grade system design methodology for Claude agents

---

## Overview

Hello Interview's systematic approach to system design interviews provides a structured, linear framework that prevents candidates from getting overwhelmed or going too deep too early. This methodology emphasizes requirements-driven design and evolutionary architecture.

### Core Philosophy

> "By following this framework, our mind is just working linearly so that even if we're given a problem that we haven't seen before, we can just build the design step by step."

**Key Principles:**
- **Linear progression** - Each step builds on the previous
- **Requirements-driven** - All design decisions trace back to explicit requirements
- **Evolutionary architecture** - Start simple, then evolve to meet non-functional requirements
- **Math when meaningful** - Do calculations only when they inform design decisions

---

## The Complete Framework

### 1. Requirements Definition (15-20 minutes)

#### 1.1 Functional Requirements
**Objective:** Identify the top 2-3 core features that are necessary and achievable within the interview timeframe.

**Process:**
- Use "users can/should be able to" statements
- Focus on primary use cases only
- If unfamiliar with the system, ask clarifying questions
- Explicitly state what's out of scope

**Example (URL Shortener):**
- ✅ Users can create a short URL from a long URL
- ✅ Users can be redirected to the original URL from the short URL  
- ✅ Optional: Support custom aliases
- ✅ Optional: Support expiration times

#### 1.2 Non-Functional Requirements
**Objective:** Define system qualities using "the system should" statements.

**Process:**
- Go through quality attributes methodically (latency, scalability, consistency, etc.)
- Choose only those uniquely relevant to this system
- Quantify where possible
- Consider CAP theorem implications

**Key Areas to Consider:**
- **Latency** - What operations need to be fast? (e.g., "200ms for redirects")
- **Scale** - How many users/operations? (e.g., "100M daily active users")
- **Consistency vs. Availability** - Do you need strong read-after-write consistency?
- **Uniqueness** - Any uniqueness constraints? (e.g., "unique short codes")

**CAP Theorem Decision Framework:**
```
Ask: "Do I need strong read-after-write consistency?"
- If YES → Choose Consistency (banking, ticketing)
- If NO → Choose Availability (social media, URL shortening)
```

#### 1.3 Skip Upfront Calculations
**Why:** Calculations done upfront rarely change your design approach and often just confirm "it's a big distributed system."

**Instead:** Do math during design when calculations will directly inform a decision.

### 2. Core Entities (5 minutes)

**Objective:** List the main data entities without full schema design.

**Process:**
- Think of these as table names or primary objects
- Don't define full schemas yet
- Keep it simple and high-level

**Communication:** Explicitly tell the interviewer you'll detail the schema later.

### 3. API Design (10 minutes)

**Objective:** Define the contract between client and backend.

**Process:**
- Map functional requirements to API endpoints (usually 1:1)
- Use REST conventions (POST for create, GET for read, etc.)
- Focus on core endpoints, not edge cases
- Reference core entities in request/response

**Structure:**
```
POST /urls
Body: {
  originalUrl: string,
  customAlias?: string,
  expirationTime?: timestamp
}
Returns: ShortUrl

GET /{shortCode}
Returns: 302 Redirect to originalUrl
```

### 4. High-Level Design (15-20 minutes)

**Objective:** Create a simple design that satisfies functional requirements only.

**Process:**
- Go through each API endpoint
- Draw the necessary components for that endpoint
- Focus on satisfying functional requirements
- Ignore scaling and performance for now

**Key Components Usually Include:**
- Client
- Load Balancer/Web Server
- Application Server
- Database
- Any necessary third-party services

### 5. Deep Dives (20-25 minutes)

**Objective:** Evolve the high-level design to meet each non-functional requirement.

**Process:**
- Go through non-functional requirements one by one
- For each requirement, identify what needs to change in the design
- Make specific architectural decisions
- Do calculations when they inform design choices

#### 5.1 Typical Deep Dive Areas

**Uniqueness (if applicable):**
- Hash-based approach vs. Counter-based approach
- Trade-offs between collision probability and performance

**Latency:**
- Caching strategies (Redis, CDN)
- Geographic distribution
- Database query optimization

**Scale:**
- Horizontal scaling of application servers
- Database sharding strategies
- Load balancing approaches

**Availability:**
- Redundancy and failover
- Database replication
- Service health monitoring

---

## Comparison with System Design Primer Framework

| Aspect | Hello Interview | System Design Primer |
|--------|----------------|---------------------|
| **Step 1** | Requirements (Functional + Non-functional) | Use cases, constraints, assumptions |
| **Step 2** | Core Entities | High-level design |
| **Step 3** | API Design | Core components |
| **Step 4** | High-Level Design | Scale the design |
| **Step 5** | Deep Dives | (Integrated throughout) |
| **Math** | Only when decision-relevant | Upfront back-of-envelope |
| **Evolution** | Linear, requirements-driven | Iterative refinement |

---

## Key Insights for Claude Agent Design

### 1. Structure and Linearity
- Provide clear step-by-step progression
- Prevent premature optimization
- Ensure each step builds on previous work

### 2. Requirements-Driven Decisions
- Always trace design choices back to requirements
- Make requirements explicit and quantified
- Distinguish between functional and non-functional clearly

### 3. Practical Calculation Strategy
- Avoid upfront calculations that don't inform decisions
- Use math strategically during design phases
- Focus on calculations that drive architectural choices

### 4. Evolutionary Architecture
- Start with simplest design that works
- Systematically address each quality requirement
- Show clear progression from simple to complex

### 5. Communication Patterns
- Explicitly communicate what you're doing and why
- Set expectations about when you'll address certain aspects
- Use structured language ("users can", "system should")

---

## Implementation Notes for Claude Agent

This framework provides the foundation for creating a Claude agent that can:

1. **Guide Requirements Gathering**: Help users articulate both functional and non-functional requirements systematically
2. **Prevent Analysis Paralysis**: Provide clear next steps at each phase
3. **Enable Systematic Scaling**: Show how to evolve simple designs into scalable architectures
4. **Make Informed Trade-offs**: Provide decision frameworks for common architectural choices
5. **Ensure Completeness**: Check that all requirements are addressed in the final design

The agent should embody this linear, requirements-driven approach while maintaining the flexibility to adapt to different problem domains.
