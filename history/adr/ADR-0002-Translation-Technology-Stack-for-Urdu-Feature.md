# ADR-2: Translation Technology Stack for Urdu Feature

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-19
- **Feature:** Urdu Translation Button
- **Context:** Need to implement Urdu translation functionality for textbook content with caching and rate limiting to provide good user experience while managing costs and API usage.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- **Translation Service**: Google Cloud Translation API for Urdu translation
- **Caching Strategy**: 24-hour cache for translated content using in-memory storage
- **Rate Limiting**: Token bucket algorithm limiting 100 requests per user per hour
- **Quality Assurance**: Target 85% accuracy rate for Urdu translations
- **Implementation**: REST API with authentication token integration

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Well-established translation service with good Urdu support
- Caching strategy reduces API costs and improves response times
- Rate limiting prevents abuse and manages API quota usage
- Quality target ensures translations are comprehensible to users
- Clear API integration path with established authentication

### Negative

- Vendor lock-in to Google Cloud Translation API
- Potential ongoing costs as translation usage increases
- Caching may serve outdated translations within 24-hour window
- Rate limiting could impact user experience for active users
- Dependency on external service availability and performance

## Alternatives Considered

- **Alternative A: Open-source translation models (e.g., MarianMT)**: Self-hosted translation models for complete control - Rejected due to complexity of deployment, maintenance overhead, and lower quality for Urdu specifically
- **Alternative B: Multiple translation API providers**: Using AWS Translate or Azure Translator - Rejected as Google Cloud Translation showed better Urdu quality scores and better free tier limits
- **Alternative C: Different caching strategies**: Shorter TTL (1 hour) or longer TTL (7 days) - Rejected as 24-hour TTL provides good balance between freshness and performance
- **Alternative D: Different rate limiting approaches**: Fixed window vs sliding window - Token bucket chosen for smoother user experience vs fixed limits

## References

- Feature Spec: specs/001-urdu-translation-button/spec.md
- Implementation Plan: specs/001-urdu-translation-button/plan.md
- Related ADRs: ADR-0001 (Textbook System Architecture)
- Research Document: specs/001-urdu-translation-button/research.md
