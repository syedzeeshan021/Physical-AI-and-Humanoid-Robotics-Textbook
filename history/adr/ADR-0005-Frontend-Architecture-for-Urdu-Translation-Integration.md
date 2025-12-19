# ADR-5: Frontend Architecture for Urdu Translation Integration

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-19
- **Feature:** Urdu Translation Button
- **Context:** Need to integrate translation functionality into existing Docusaurus-based textbook platform with proper RTL support for Urdu, maintain existing user experience while adding new features, and ensure accessibility compliance.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- **Framework**: Docusaurus v3 with TypeScript (consistent with existing architecture)
- **Translation Button Component**: Custom React component placed at chapter start with 44px minimum touch target
- **Language Switching**: Toggle functionality preserving original content in memory with scroll position maintenance
- **RTL Support**: Right-to-left text rendering for Urdu content with appropriate CSS styling
- **User Interface**: "Translate to Urdu" button changing to "Translate back to English" after use
- **Accessibility**: Proper states (hover, active, focus, loading, disabled) and visibility only for logged-in users
- **User Feedback**: Visual feedback for translation actions with integration into user profile

## Consequences

### Positive

- Consistent with existing Docusaurus architecture and development patterns
- Proper accessibility compliance with minimum touch target sizes
- Smooth user experience with preserved scroll position during language switching
- Clear visual feedback for user actions during translation
- Proper RTL support for Urdu text rendering
- Integration with existing authentication checks
- Maintainable component architecture with clear separation of concerns

### Negative

- Additional CSS complexity for RTL layout support
- Potential layout issues with existing components when rendering RTL text
- Increased bundle size with additional translation functionality
- Need for additional testing across different browsers for RTL support
- Potential performance impact from content switching mechanism
- Risk of breaking existing Docusaurus functionality if not properly integrated

## Alternatives Considered

- **Alternative A: Separate translation interface**: Modal or new page for translation instead of inline chapter button - Rejected as it would disrupt the reading flow and reduce discoverability
- **Alternative B: Different frontend framework**: Migrate to Next.js for translation features - Rejected as it would require significant refactoring of existing Docusaurus setup
- **Alternative C: Client-side only translation**: Using browser APIs instead of server API calls - Rejected as it would not support usage tracking and have security concerns
- **Alternative D: Different placement**: Translation button at end of chapter or in navigation - Rejected as the requirement specifies "at the start of each chapter" for immediate access

## References

- Feature Spec: specs/001-urdu-translation-button/spec.md
- Implementation Plan: specs/001-urdu-translation-button/plan.md
- Related ADRs: ADR-0001 (Textbook System Architecture)
- Quickstart Guide: specs/001-urdu-translation-button/quickstart.md
