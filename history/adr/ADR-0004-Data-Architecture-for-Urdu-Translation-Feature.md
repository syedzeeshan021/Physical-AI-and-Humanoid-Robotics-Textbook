# ADR-4: Data Architecture for Urdu Translation Feature

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-19
- **Feature:** Urdu Translation Button
- **Context:** Need to store translation session data and maintain relationships between users and translated content while using the existing Neon PostgreSQL database.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- **Database**: Neon PostgreSQL (extension of existing ADR-0001 architecture)
- **User Account Entity**: user_id (UUID), auth_status, translation_usage_history (JSONB)
- **Translation Session Entity**: session_id (UUID), user_id (FK), original_content_ref, translated_content, chapter_reference, cache_expires_at
- **Data Relationships**: Foreign key relationships between entities, JSONB for flexible usage tracking
- **Caching Integration**: cache_expires_at field for 24-hour TTL management

## Consequences

### Positive

- Consistent with existing database architecture (Neon PostgreSQL)
- Proper normalization with foreign key relationships ensures data integrity
- JSONB field allows flexible tracking of translation usage patterns
- Cache expiration field enables automatic cleanup of expired translations
- Clear separation of concerns between user and session data
- Efficient querying for translation history

### Negative

- Additional database schema complexity with two new entities
- Potential performance impact from joins between related entities
- JSONB field may be harder to query than structured columns
- Need for additional database migration scripts
- Increased storage requirements for translated content
- Potential for data inconsistency if foreign key constraints are not properly maintained

## Alternatives Considered

- **Alternative A: NoSQL Database**: Using MongoDB or similar for translation data - Rejected as it would introduce additional complexity and not align with existing PostgreSQL architecture
- **Alternative B: Single combined entity**: Storing all translation data in user table - Rejected as it would lead to data duplication and violate normalization principles
- **Alternative C: External caching service**: Using Redis for session and translation caching - Rejected as PostgreSQL with JSONB provides sufficient caching capability and reduces infrastructure complexity
- **Alternative D: Different data relationships**: No foreign keys, relying on application-level references - Rejected as foreign keys provide better data integrity and consistency

## References

- Feature Spec: specs/001-urdu-translation-button/spec.md
- Implementation Plan: specs/001-urdu-translation-button/plan.md
- Related ADRs: ADR-0001 (Textbook System Architecture)
- Data Model: specs/001-urdu-translation-button/data-model.md
