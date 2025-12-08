# Textbook Generation Data Model

## Core Entities

### User
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier |
| email | String | Unique, Nullable | User email address |
| preferences | JSON | Nullable | User preferences (language, theme, etc.) |
| progress | JSON | Nullable | Learning progress tracking |
| created_at | Timestamp | Not Null | Record creation time |
| updated_at | Timestamp | Not Null | Record update time |

### Chapter
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier |
| title | String | Not Null | Chapter title |
| content | Text | Not Null | Chapter content in markdown |
| order | Integer | Not Null | Chapter sequence order |
| word_count | Integer | Not Null | Number of words in chapter |
| created_at | Timestamp | Not Null | Record creation time |
| updated_at | Timestamp | Not Null | Record update time |

### Embedding
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier |
| chapter_id | UUID | Foreign Key, Not Null | Reference to chapter |
| content | Text | Not Null | Text snippet for embedding |
| embedding_vector | Vector | Not Null | Embedding vector data |
| token_count | Integer | Not Null | Number of tokens in content |
| created_at | Timestamp | Not Null | Record creation time |

### ChatSession
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier |
| user_id | UUID | Foreign Key, Nullable | Reference to user (optional) |
| created_at | Timestamp | Not Null | Session creation time |
| updated_at | Timestamp | Not Null | Session update time |

### ChatMessage
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier |
| session_id | UUID | Foreign Key, Not Null | Reference to chat session |
| role | Enum | Not Null | Message role (user/assistant) |
| content | Text | Not Null | Message content |
| created_at | Timestamp | Not Null | Message creation time |

## Relationships

### User → ChatSession
- One-to-Many relationship
- User can have multiple chat sessions
- ChatSession.user_id references User.id

### Chapter → Embedding
- One-to-Many relationship
- Chapter can have multiple embeddings
- Embedding.chapter_id references Chapter.id

### ChatSession → ChatMessage
- One-to-Many relationship
- ChatSession can have multiple messages
- ChatMessage.session_id references ChatSession.id

## Indexes

### User Table
- Index on email (for authentication)
- Index on created_at (for querying)

### Chapter Table
- Index on order (for sorting)
- Index on created_at (for querying)

### Embedding Table
- Index on chapter_id (for querying)
- Index on created_at (for querying)

### ChatSession Table
- Index on user_id (for querying)
- Index on created_at (for querying)

### ChatMessage Table
- Index on session_id (for querying)
- Index on created_at (for ordering)

## Validation Rules

### User
- Email format validation if provided
- Unique email constraint

### Chapter
- Title must not be empty
- Content must not be empty
- Order must be positive integer
- Word count must match actual content

### Embedding
- Content length must be within reasonable limits
- Embedding vector must have correct dimensions
- Token count must match actual content

### ChatSession
- User_id must reference valid user if provided

### ChatMessage
- Role must be either 'user' or 'assistant'
- Content must not be empty
- Session_id must reference valid session