# Urdu Translation Button - Research Findings

## 1. Translation API Research

### 1.1 Google Cloud Translation API
- **Decision**: Use Google Cloud Translation API for Urdu translation
- **Rationale**: Well-established, supports Urdu, good quality translations with reasonable pricing for free tier
- **Alternatives considered**:
  - AWS Translate: Reliable, good Urdu support, but slightly higher cost
  - OpenAI GPT-based translation: Higher quality but significantly more expensive
  - LibreTranslate: Cost-effective but lower quality and reliability concerns

### 1.2 Caching Strategy
- **Decision**: Cache translated content for 24 hours
- **Rationale**: Good balance between freshness and performance, reduces API calls while keeping content reasonably current
- **Alternatives considered**:
  - No caching: Highest quality but highest cost and slower performance
  - 1-week caching: Better performance but content may become stale
  - Indefinite caching: Best performance but requires complex invalidation

## 2. Authentication Requirements

### 2.1 Account Verification Level
- **Decision**: Basic account registration required
- **Rationale**: Maximizes accessibility while maintaining tracking of bonus points
- **Alternatives considered**:
  - Verified email required: Moderate verification level but might reduce adoption
  - Multi-factor authentication: Highest security but high friction
  - Special permission level: Restricted access but more control

## 3. Bonus Points System

### 3.1 Points Retention Strategy
- **Decision**: Retain bonus points permanently
- **Rationale**: Points should be a permanent record of user achievement and engagement
- **Alternatives considered**:
  - 30-day retention: Motivates continued engagement but demotivates long-term users
  - 1-year retention: Balance between retention and freshness but still temporary
  - Until account deletion: Points persist as long as account exists

## 4. Translation Quality Requirements

### 4.1 Quality Threshold
- **Decision**: 85% accuracy rate for Urdu translations
- **Rationale**: Good balance between quality and feasibility for technical content
- **Alternatives considered**:
  - 95% accuracy: Very high quality but may require expensive service
  - 75% accuracy: Acceptable quality but cost-effective solution
  - Human reviewed: Highest quality but very expensive and time-consuming

## 5. Technical Implementation Research

### 5.1 Frontend Integration
- **Research**: Docusaurus v3 custom component development
- **Findings**: Docusaurus supports custom React components that can be injected into MDX content
- **Best Practice**: Use React hooks for state management and API calls

### 5.2 Right-to-Left Text Support
- **Research**: CSS and React implementation for RTL languages
- **Findings**: CSS `direction: rtl` property and `text-align: right` for proper Urdu rendering
- **Best Practice**: Test with actual Urdu content and native speakers