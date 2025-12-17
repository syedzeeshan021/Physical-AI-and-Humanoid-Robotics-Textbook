# Urdu Translation Button - Data Model

## 1. Entity Definitions

### 1.1 User Account
- **Entity Name**: UserAccount
- **Description**: Represents a registered user in the system
- **Fields**:
  - `user_id`: UUID (Primary Key, Required)
    - Unique identifier for the user
    - Auto-generated on creation
  - `auth_status`: String (Enum: 'unverified', 'verified', 'active', Required)
    - Current authentication status of the user
    - Determines access to translation feature
  - `bonus_points_balance`: Integer (Default: 0, Required)
    - Total bonus points accumulated by the user
    - Updated when translation bonus points are awarded
  - `translation_usage_history`: JSONB (Optional)
    - Array of translation session IDs
    - Tracks user's translation activity
  - `created_at`: Timestamp (Required)
    - When the account was created
  - `updated_at`: Timestamp (Required)
    - When the account was last updated

### 1.2 Translation Session
- **Entity Name**: TranslationSession
- **Description**: Represents a single translation event
- **Fields**:
  - `session_id`: UUID (Primary Key, Required)
    - Unique identifier for the translation session
    - Auto-generated on creation
  - `user_id`: UUID (Foreign Key to UserAccount, Required)
    - References the user who initiated the translation
  - `original_content_ref`: Text (Required)
    - Reference to the original English content
    - Could be a hash or identifier of the content
  - `translated_content`: Text (Required)
    - The translated Urdu content
    - Stored for caching purposes
  - `chapter_reference`: Text (Required)
    - Identifier for the chapter being translated
  - `translation_timestamp`: Timestamp (Required)
    - When the translation was performed
  - `is_cached`: Boolean (Default: true, Required)
    - Whether this translation is cached
  - `cache_expires_at`: Timestamp (Required)
    - When the cached translation expires (24 hours from creation)

### 1.3 Bonus Points Record
- **Entity Name**: BonusPointsRecord
- **Description**: Tracks bonus points awarded to users
- **Fields**:
  - `points_id`: UUID (Primary Key, Required)
    - Unique identifier for the points record
    - Auto-generated on creation
  - `user_id`: UUID (Foreign Key to UserAccount, Required)
    - References the user who earned the points
  - `points_earned`: Integer (Default: 50, Required)
    - Number of points earned in this transaction
    - Fixed at 50 for translation feature usage
  - `chapter_id`: Text (Required)
    - Identifier for the chapter where points were earned
  - `earned_at`: Timestamp (Required)
    - When the points were awarded
  - `is_first_time`: Boolean (Default: true, Required)
    - Whether this was the first time translation was used for this chapter
  - `total_points_earned`: Integer (Required)
    - Total points for the user after this transaction

## 2. Relationships

### 2.1 UserAccount to TranslationSession
- **Relationship Type**: One-to-Many
- **Description**: A user can have multiple translation sessions
- **Constraint**: When a user is deleted, related translation sessions are preserved for analytics

### 2.2 UserAccount to BonusPointsRecord
- **Relationship Type**: One-to-Many
- **Description**: A user can earn multiple bonus points records
- **Constraint**: When a user is deleted, related bonus points records are preserved for analytics

### 2.3 TranslationSession to BonusPointsRecord
- **Relationship Type**: One-to-One (Optional)
- **Description**: A translation session may result in a bonus points award
- **Constraint**: Only awarded for first-time translation per chapter

## 3. Validation Rules

### 3.1 UserAccount Validation
- `auth_status` must be one of the defined enum values
- `bonus_points_balance` cannot be negative
- `user_id` must be unique

### 3.2 TranslationSession Validation
- `user_id` must reference an existing user account
- `translated_content` must not be empty
- `cache_expires_at` must be 24 hours after `translation_timestamp`
- `chapter_reference` must be valid

### 3.3 BonusPointsRecord Validation
- `user_id` must reference an existing user account
- `points_earned` must be 50 for translation feature
- `chapter_id` must be valid
- `is_first_time` can only be true once per user-chapter combination

## 4. Indexes

### 4.1 TranslationSession Indexes
- Index on `user_id` for efficient user-based queries
- Index on `chapter_reference` for chapter-based queries
- Index on `cache_expires_at` for cache cleanup operations

### 4.2 BonusPointsRecord Indexes
- Index on `user_id` for user points queries
- Index on `chapter_id` for chapter-based analytics
- Composite index on (`user_id`, `chapter_id`) for first-time checks

## 5. State Transitions

### 5.1 UserAccount State Transitions
- `unverified` → `verified` when email is confirmed
- `verified` → `active` when user engages with platform
- No reverse transitions allowed

### 5.2 TranslationSession State Transitions
- No state transitions - sessions are immutable after creation
- `is_cached` remains true until `cache_expires_at` is reached