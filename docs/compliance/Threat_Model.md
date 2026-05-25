# Threat Model - Warehouse Management Service

## Overview

### Service Purpose
The Warehouse Management Service is a Django REST Framework (DRF) based web application that provides a content publishing platform. The service enables users to create, read, update, and delete articles, engage with content through comments, follow other users, and organize content using tags. Despite its naming, this service implements a blogging/publishing platform similar to Medium or RealWorld specifications.

### Service Scope
- **Technology Stack**: Django 1.10.5, Django REST Framework 3.4.4, Python
- **Authentication**: JWT (JSON Web Tokens) using PyJWT 1.4.2
- **Database**: SQLite3 (development)
- **API Type**: RESTful API with JSON responses
- **Deployment Model**: Web service with CORS support

### Key Functionality
1. User registration and authentication
2. Article management (CRUD operations)
3. Comment system for articles
4. User profile management
5. Social features (following users, favoriting articles)
6. Tag-based content organization
7. Article feed generation

## Data Flow Diagram

```
┌─────────────┐
│   Client    │
│ Application │
│  (Browser/  │
│   Mobile)   │
└──────┬──────┘
       │
       │ HTTPS/HTTP
       │ (CORS Enabled)
       │
       ▼
┌──────────────────────────────────────────────┐
│         Django Application Server            │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │     CORS Middleware                    │ │
│  └────────────────┬───────────────────────┘ │
│                   │                          │
│  ┌────────────────▼───────────────────────┐ │
│  │     Authentication Middleware          │ │
│  │     (JWT Token Validation)             │ │
│  └────────────────┬───────────────────────┘ │
│                   │                          │
│  ┌────────────────▼───────────────────────┐ │
│  │     URL Router                         │ │
│  └────────────────┬───────────────────────┘ │
│                   │                          │
│  ┌────────────────▼───────────────────────┐ │
│  │     API Views                          │ │
│  │  • Authentication (Login/Register)     │ │
│  │  • Articles (CRUD)                     │ │
│  │  • Comments                            │ │
│  │  • Profiles                            │ │
│  │  • Tags                                │ │
│  └────────────────┬───────────────────────┘ │
│                   │                          │
│  ┌────────────────▼───────────────────────┐ │
│  │     Serializers / Validators           │ │
│  └────────────────┬───────────────────────┘ │
│                   │                          │
│  ┌────────────────▼───────────────────────┐ │
│  │     Django ORM                         │ │
│  └────────────────┬───────────────────────┘ │
│                   │                          │
└───────────────────┼──────────────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │   SQLite3 DB    │
           │                 │
           │  • Users        │
           │  • Profiles     │
           │  • Articles     │
           │  • Comments     │
           │  • Tags         │
           └─────────────────┘
```

## Dependencies

### Python Libraries
| Dependency | Version | Purpose | Security Considerations |
|------------|---------|---------|------------------------|
| Django | 1.10.5 | Web framework | **CRITICAL**: Known vulnerabilities in older version, requires upgrade |
| djangorestframework | 3.4.4 | REST API framework | **HIGH**: Older version, may contain security issues |
| django-cors-middleware | 1.3.1 | CORS handling | Misconfiguration could lead to unauthorized access |
| django-extensions | 1.7.1 | Development utilities | Should not be used in production |
| PyJWT | 1.4.2 | JWT token generation | **HIGH**: Older version with potential vulnerabilities |
| six | 1.10.0 | Python 2/3 compatibility | Low risk utility library |

### Infrastructure Dependencies
- **Database**: SQLite3 (not suitable for production at scale)
- **Web Server**: WSGI-compatible server (e.g., Gunicorn, uWSGI)
- **Python Runtime**: Python 3.5.2 or compatible

### External Services
- None identified in current configuration (self-contained service)

## Entry Points

### 1. Authentication Endpoints
- **POST /api/users** - User registration
  - Input: username, email, password
  - Authentication: None (public)
  - Risk Level: High (account creation)

- **POST /api/users/login** - User login
  - Input: email, password
  - Authentication: None (public)
  - Risk Level: High (credential validation)

- **GET/PUT /api/user** - Get/Update current user
  - Input: user data (email, username, bio, image)
  - Authentication: JWT token required
  - Risk Level: Medium (authenticated)

### 2. Article Endpoints
- **GET /api/articles** - List articles
  - Input: query parameters (tag, author, favorited, limit, offset)
  - Authentication: Optional
  - Risk Level: Low (read-only)

- **POST /api/articles** - Create article
  - Input: title, description, body, tagList
  - Authentication: JWT token required
  - Risk Level: Medium (content creation)

- **GET /api/articles/{slug}** - Get article details
  - Input: slug parameter
  - Authentication: Optional
  - Risk Level: Low (read-only)

- **PUT /api/articles/{slug}** - Update article
  - Input: article data
  - Authentication: JWT token required (must be author)
  - Risk Level: Medium (content modification)

- **DELETE /api/articles/{slug}** - Delete article
  - Input: slug parameter
  - Authentication: JWT token required (must be author)
  - Risk Level: Medium (content deletion)

- **GET /api/articles/feed** - Get personalized feed
  - Input: pagination parameters
  - Authentication: JWT token required
  - Risk Level: Low (read-only, authenticated)

- **POST/DELETE /api/articles/{slug}/favorite** - Favorite/Unfavorite article
  - Input: slug parameter
  - Authentication: JWT token required
  - Risk Level: Low (metadata modification)

### 3. Comment Endpoints
- **GET /api/articles/{slug}/comments** - List comments
  - Input: article slug
  - Authentication: Optional
  - Risk Level: Low (read-only)

- **POST /api/articles/{slug}/comments** - Create comment
  - Input: comment body
  - Authentication: JWT token required
  - Risk Level: Medium (content creation)

- **DELETE /api/articles/{slug}/comments/{id}** - Delete comment
  - Input: article slug, comment id
  - Authentication: JWT token required (must be author)
  - Risk Level: Medium (content deletion)

### 4. Profile Endpoints
- **GET /api/profiles/{username}** - Get user profile
  - Input: username parameter
  - Authentication: Optional
  - Risk Level: Low (read-only)

- **POST/DELETE /api/profiles/{username}/follow** - Follow/Unfollow user
  - Input: username parameter
  - Authentication: JWT token required
  - Risk Level: Low (relationship modification)

### 5. Tag Endpoints
- **GET /api/tags** - List all tags
  - Input: None
  - Authentication: None
  - Risk Level: Low (read-only)

### 6. Admin Interface
- **GET/POST /admin/** - Django admin interface
  - Input: Various admin operations
  - Authentication: Django session (staff/superuser required)
  - Risk Level: Critical (full system access)

## Exit Points

### 1. HTTP Responses
- **JSON API Responses** - All API endpoints return JSON
  - Risk: Information disclosure through error messages
  - Risk: Exposure of internal system details
  - Data: User data, articles, comments, profiles

### 2. Database Writes
- **SQLite3 Database** - All data persisted to database
  - Risk: Data corruption or injection
  - Risk: Unauthorized data access if file permissions incorrect
  - Data: All application data

### 3. Authentication Tokens
- **JWT Token Generation** - Tokens issued at login/registration
  - Risk: Token theft enables impersonation
  - Risk: Weak signing key compromise
  - Data: User ID, expiration timestamp

### 4. Error Messages and Logs
- **Django Debug Output** - When DEBUG=True
  - Risk: Information disclosure of system internals
  - Risk: Stack traces reveal code structure
  - Data: Configuration, file paths, database schema

### 5. CORS Headers
- **Cross-Origin Resource Sharing** - Headers allowing cross-origin requests
  - Risk: Overly permissive CORS could enable attacks
  - Risk: Credential exposure to unauthorized origins
  - Configured Origins: localhost:4000, 0.0.0.0:4000

## Assets

### 1. Critical Assets

#### User Credentials
- **Description**: User passwords (hashed), email addresses
- **Storage**: Database (authentication_user table)
- **Sensitivity**: Critical
- **Impact of Compromise**: Account takeover, identity theft

#### JWT Secret Key
- **Description**: Secret key used to sign JWT tokens
- **Storage**: settings.py (SECRET_KEY)
- **Sensitivity**: Critical
- **Impact of Compromise**: Complete authentication bypass, ability to forge any user token
- **Current Risk**: Hardcoded in source code

#### Authentication Tokens
- **Description**: JWT tokens for authenticated sessions
- **Storage**: Client-side (localStorage/cookies)
- **Sensitivity**: Critical
- **Impact of Compromise**: Session hijacking, unauthorized actions

### 2. High-Value Assets

#### User Articles
- **Description**: Article content (title, description, body)
- **Storage**: Database (articles_article table)
- **Sensitivity**: High
- **Impact of Compromise**: Content manipulation, intellectual property theft

#### User Profiles
- **Description**: Profile data (bio, image URLs, followers)
- **Storage**: Database (profiles_profile table)
- **Sensitivity**: Medium-High
- **Impact of Compromise**: Privacy violation, reputation damage

#### User Email Addresses
- **Description**: Primary email for each user account
- **Storage**: Database (authentication_user table)
- **Sensitivity**: High
- **Impact of Compromise**: Spam, phishing attacks, privacy violation

### 3. Medium-Value Assets

#### Comments
- **Description**: User comments on articles
- **Storage**: Database (articles_comment table)
- **Sensitivity**: Medium
- **Impact of Compromise**: Content manipulation, reputation damage

#### Social Graph
- **Description**: User following relationships
- **Storage**: Database (profiles_profile_follows table)
- **Sensitivity**: Medium
- **Impact of Compromise**: Privacy violation, social engineering

#### Favorites
- **Description**: Articles favorited by users
- **Storage**: Database (profiles_profile_favorites table)
- **Sensitivity**: Low-Medium
- **Impact of Compromise**: Privacy violation, preference manipulation

#### Tags
- **Description**: Content categorization tags
- **Storage**: Database (articles_tag table)
- **Sensitivity**: Low
- **Impact of Compromise**: Content organization disruption

### 4. System Assets

#### Database File
- **Description**: SQLite database file containing all data
- **Storage**: File system (db.sqlite3)
- **Sensitivity**: Critical
- **Impact of Compromise**: Complete data breach

#### Application Source Code
- **Description**: Python application code
- **Storage**: File system
- **Sensitivity**: Medium
- **Impact of Compromise**: Vulnerability discovery, logic bypass

#### Admin Interface
- **Description**: Django admin panel for system management
- **Storage**: /admin/ endpoint
- **Sensitivity**: Critical
- **Impact of Compromise**: Full system control

## Trust Levels

### Level 0: Unauthenticated Users (Anonymous)
- **Description**: Public internet users without accounts
- **Access Rights**:
  - View public articles
  - View public profiles
  - View comments
  - View tags
  - Register new account
  - Login to existing account
- **Trust Boundaries**: No access to write operations or authenticated content
- **Validation**: Rate limiting, input validation on registration/login

### Level 1: Authenticated Users (Standard Users)
- **Description**: Registered users with valid JWT tokens
- **Access Rights**:
  - All Level 0 rights
  - Create articles
  - Edit/delete own articles
  - Create comments
  - Delete own comments
  - Follow/unfollow users
  - Favorite/unfavorite articles
  - View personalized feed
  - Update own profile
- **Trust Boundaries**: Cannot modify other users' content, cannot access admin interface
- **Validation**: JWT signature verification, ownership checks for modifications

### Level 2: Content Owners
- **Description**: Authenticated users accessing their own content
- **Access Rights**:
  - All Level 1 rights
  - Modify own articles
  - Delete own articles
  - Delete own comments
  - Update own profile
- **Trust Boundaries**: Limited to own content only
- **Validation**: Ownership verification through foreign key relationships

### Level 3: Staff Users
- **Description**: Users with is_staff=True flag
- **Access Rights**:
  - All Level 2 rights
  - Access Django admin interface
  - View all database records via admin
- **Trust Boundaries**: Can view but may have limited modification rights depending on admin configuration
- **Validation**: is_staff flag verification, Django admin permissions

### Level 4: Superusers (Administrators)
- **Description**: Users with is_superuser=True flag
- **Access Rights**:
  - Complete system access
  - Full database read/write via admin interface
  - User account management
  - System configuration
- **Trust Boundaries**: None
- **Validation**: is_superuser flag verification

### External Systems Trust Levels

#### Database
- **Trust Level**: Trusted
- **Validation**: Implicit trust in data integrity
- **Risk**: SQL injection could compromise this trust

#### CORS Origins
- **Trust Level**: Semi-trusted (configured whitelist)
- **Validation**: Origin header checking
- **Risk**: Misconfiguration could allow unauthorized origins

## STRIDE Threat List

### Spoofing Identity

#### S-1: JWT Token Forgery
- **Threat**: Attacker forges JWT tokens to impersonate users
- **Component**: Authentication system
- **Severity**: Critical
- **Details**: 
  - Hardcoded SECRET_KEY in settings.py (easily discoverable)
  - Weak or predictable secret key enables token forgery
  - Old PyJWT version (1.4.2) may have vulnerabilities
- **Attack Vector**: Access to source code or brute force attack on weak secret
- **Impact**: Complete authentication bypass, access to any user account

#### S-2: Session Hijacking via Token Theft
- **Threat**: Attacker steals JWT token to impersonate user
- **Component**: Token storage and transmission
- **Severity**: High
- **Details**:
  - Tokens transmitted in HTTP headers
  - XSS could enable token theft from client storage
  - Long token expiration (60 days) increases exposure window
- **Attack Vector**: XSS, man-in-the-middle, compromised client
- **Impact**: Account takeover for token validity period

#### S-3: Email/Username Enumeration
- **Threat**: Attacker enumerates valid email addresses or usernames
- **Component**: Registration and login endpoints
- **Severity**: Medium
- **Details**:
  - Different error messages for invalid email vs wrong password
  - Registration may reveal if email already exists
- **Attack Vector**: Automated scanning of registration/login endpoints
- **Impact**: User enumeration for targeted attacks, privacy violation

### Tampering

#### T-1: Unauthorized Content Modification
- **Threat**: Attacker modifies articles or comments they don't own
- **Component**: Article and comment update/delete endpoints
- **Severity**: High
- **Details**:
  - Authorization checks may have logic flaws
  - IDOR (Insecure Direct Object Reference) vulnerabilities
  - Weak ownership verification
- **Attack Vector**: Parameter manipulation, API request crafting
- **Impact**: Content integrity violation, defacement

#### T-2: SQL Injection
- **Threat**: Attacker injects SQL commands to manipulate database
- **Component**: Database queries, ORM usage
- **Severity**: Critical
- **Details**:
  - Django ORM generally prevents SQL injection
  - Raw queries or improper ORM usage could be vulnerable
  - Slug fields and query parameters potential entry points
- **Attack Vector**: Malicious input in slugs, search parameters, filters
- **Impact**: Data manipulation, data breach, database corruption

#### T-3: Mass Assignment Vulnerabilities
- **Threat**: Attacker modifies fields they shouldn't have access to
- **Component**: Serializers and model updates
- **Severity**: High
- **Details**:
  - DRF serializers may expose unintended fields
  - User could modify is_staff, is_superuser, or other protected fields
  - Weak field filtering in serializers
- **Attack Vector**: Additional parameters in API requests
- **Impact**: Privilege escalation, data integrity violation

#### T-4: CSRF Attacks
- **Threat**: Attacker tricks user into performing unwanted actions
- **Component**: State-changing endpoints
- **Severity**: Medium
- **Details**:
  - API uses JWT tokens (not cookies), reducing CSRF risk
  - CSRF middleware enabled but may not fully protect API
  - CORS configuration could enable CSRF-like attacks
- **Attack Vector**: Malicious website making requests on behalf of user
- **Impact**: Unauthorized actions performed as victim

### Repudiation

#### R-1: Insufficient Activity Logging
- **Threat**: Users deny performing actions with no audit trail
- **Component**: Logging system
- **Severity**: Medium
- **Details**:
  - No evidence of comprehensive activity logging
  - Difficult to prove who performed actions
  - No audit trail for sensitive operations
- **Attack Vector**: Performing malicious actions and denying responsibility
- **Impact**: Cannot investigate security incidents, accountability issues

#### R-2: Lack of Content Change Tracking
- **Threat**: Article/comment modifications not tracked
- **Component**: Article and comment models
- **Severity**: Low-Medium
- **Details**:
  - Models have created_at but limited update history
  - No versioning or change log for content
  - Cannot prove what content existed at specific time
- **Attack Vector**: Edit content to remove evidence of malicious statements
- **Impact**: Dispute resolution difficulties, legal liability

#### R-3: No Authentication Event Logging
- **Threat**: Login/logout events not logged
- **Component**: Authentication system
- **Severity**: Medium
- **Details**:
  - No evidence of login attempt logging
  - Cannot detect brute force attacks
  - Cannot prove when user accessed system
- **Attack Vector**: Brute force attacks, unauthorized access
- **Impact**: Cannot detect or investigate account compromises

### Information Disclosure

#### I-1: Debug Mode Enabled
- **Threat**: Sensitive system information exposed via debug pages
- **Component**: Django debug mode
- **Severity**: Critical
- **Details**:
  - DEBUG=True in settings.py
  - Error pages reveal code, configuration, file paths
  - Database query details exposed
- **Attack Vector**: Triggering errors to view debug information
- **Impact**: Information gathering for targeted attacks, configuration disclosure

#### I-2: Hardcoded Secret Key
- **Threat**: Cryptographic secret exposed in source code
- **Component**: settings.py
- **Severity**: Critical
- **Details**:
  - SECRET_KEY hardcoded as '2^f+3@v7$v1f8yt0!s)3-1t$)tlp+xm17=*g))_xoi&&9m#2a&'
  - Exposed in version control
  - Same key used for all security operations
- **Attack Vector**: Source code access, repository analysis
- **Impact**: Complete security compromise, token forgery, session hijacking

#### I-3: Verbose Error Messages
- **Threat**: Error messages reveal system internals
- **Component**: Exception handling
- **Severity**: Medium
- **Details**:
  - API may return detailed error messages
  - Stack traces in development mode
  - Database constraint violations reveal schema
- **Attack Vector**: Sending malformed requests, observing responses
- **Impact**: Information gathering for attacks, schema discovery

#### I-4: Unrestricted Profile Information
- **Threat**: User profile data accessible without authorization
- **Component**: Profile API endpoints
- **Severity**: Low-Medium
- **Details**:
  - Profiles publicly accessible
  - Email addresses may be exposed
  - Following relationships visible
- **Attack Vector**: Scraping profile API
- **Impact**: Privacy violation, data harvesting

#### I-5: CORS Misconfiguration
- **Threat**: Sensitive data exposed to unauthorized origins
- **Component**: CORS middleware
- **Severity**: Medium
- **Details**:
  - CORS whitelist includes localhost and 0.0.0.0
  - May allow credentials to untrusted origins
  - Potential for data exfiltration
- **Attack Vector**: Malicious website making API requests
- **Impact**: Data leakage to unauthorized parties

### Denial of Service

#### D-1: Resource Exhaustion via Unbounded Queries
- **Threat**: Attacker exhausts resources with expensive queries
- **Component**: API endpoints, database
- **Severity**: High
- **Details**:
  - No evidence of rate limiting
  - SQLite not suitable for high concurrency
  - Large limit parameters in pagination
  - No query timeouts visible
- **Attack Vector**: Automated requests with maximum page sizes, complex filters
- **Impact**: Service unavailability, performance degradation

#### D-2: Mass Registration/Content Creation
- **Threat**: Attacker creates large numbers of accounts or content
- **Component**: Registration and content creation endpoints
- **Severity**: Medium
- **Details**:
  - No CAPTCHA or bot prevention
  - No account creation rate limiting visible
  - No content creation throttling
- **Attack Vector**: Automated account and content creation
- **Impact**: Database bloat, resource exhaustion, spam content

#### D-3: Large Payload Attacks
- **Threat**: Attacker sends extremely large request bodies
- **Component**: Request handling
- **Severity**: Medium
- **Details**:
  - No evidence of request size limits
  - Article body field is TextField (unlimited)
  - Could exhaust memory or disk space
- **Attack Vector**: Sending massive article or comment bodies
- **Impact**: Memory exhaustion, disk space exhaustion

#### D-4: Regex DoS (ReDoS)
- **Threat**: Malicious input causes catastrophic regex backtracking
- **Component**: URL routing, slug validation
- **Severity**: Low-Medium
- **Details**:
  - Slug patterns use regex: [-\w]+
  - Complex username or slug patterns could cause slowdown
- **Attack Vector**: Crafted slugs or URLs
- **Impact**: CPU exhaustion, request timeout

### Elevation of Privilege

#### E-1: Privilege Escalation via Mass Assignment
- **Threat**: User modifies privileged fields to gain admin access
- **Component**: User update endpoint, serializers
- **Severity**: Critical
- **Details**:
  - User serializer may not properly filter fields
  - is_staff, is_superuser fields could be modifiable
  - Weak field validation in PUT /api/user
- **Attack Vector**: Adding privileged fields to user update request
- **Impact**: Attacker gains admin access

#### E-2: Authorization Bypass via IDOR
- **Threat**: Attacker accesses/modifies resources by manipulating IDs
- **Component**: All resource endpoints
- **Severity**: High
- **Details**:
  - Authorization checks may be incomplete
  - Slug-based lookups could have logic flaws
  - Foreign key relationships may not properly enforce ownership
- **Attack Vector**: Changing article slugs, comment IDs, usernames in requests
- **Impact**: Unauthorized data access and modification

#### E-3: Admin Interface Access
- **Threat**: Attacker gains access to Django admin interface
- **Component**: /admin/ endpoint
- **Severity**: Critical
- **Details**:
  - Admin interface provides full database access
  - Weak password policies allow brute force
  - Default admin URL predictable
- **Attack Vector**: Credential brute force, social engineering, credential stuffing
- **Impact**: Complete system compromise

#### E-4: JWT Algorithm Confusion Attack
- **Threat**: Attacker exploits JWT algorithm confusion
- **Component**: JWT token validation
- **Severity**: High
- **Details**:
  - Old PyJWT version (1.4.2) vulnerable to algorithm switching
  - Could allow "none" algorithm or switch from HS256 to RS256
  - Improper algorithm verification
- **Attack Vector**: Crafting JWT with "none" algorithm or different signing method
- **Impact**: Authentication bypass, complete system access

#### E-5: Python Code Injection
- **Threat**: Attacker injects Python code for execution
- **Component**: Template rendering, eval() usage, serialization
- **Severity**: Critical
- **Details**:
  - Django templates generally safe
  - Pickle deserialization could be vulnerable
  - Any eval() or exec() usage is critical risk
- **Attack Vector**: Malicious input in fields processed by unsafe functions
- **Impact**: Remote code execution, complete server compromise

## Countermeasures

### Authentication & Authorization

#### CM-1: Upgrade PyJWT and Implement Secure Token Management
- **Addresses**: S-1, S-2, E-4
- **Priority**: Critical
- **Implementation**:
  - Upgrade PyJWT to latest version (2.x)
  - Explicitly specify and validate JWT algorithm (HS256)
  - Disable "none" algorithm support
  - Reduce token expiration from 60 days to 24 hours or less
  - Implement refresh token mechanism
  - Add token revocation capability (blacklist)
  - Store tokens securely on client (HttpOnly cookies for web)

#### CM-2: Externalize and Rotate Secret Keys
- **Addresses**: I-2, S-1
- **Priority**: Critical
- **Implementation**:
  - Remove SECRET_KEY from settings.py
  - Load secret from environment variable
  - Use cryptographically strong random key (minimum 50 characters)
  - Implement key rotation mechanism
  - Never commit secrets to version control
  - Use secret management service (e.g., AWS Secrets Manager, HashiCorp Vault)

#### CM-3: Implement Comprehensive Authorization Checks
- **Addresses**: T-1, E-1, E-2
- **Priority**: High
- **Implementation**:
  - Verify ownership before all update/delete operations
  - Use Django REST Framework permissions consistently
  - Implement custom permission classes for resource ownership
  - Validate user has rights to access requested resources
  - Use explicit field whitelisting in serializers (exclude sensitive fields)
  - Never trust client-provided IDs without verification

#### CM-4: Implement Multi-Factor Authentication (MFA)
- **Addresses**: S-1, S-2, E-3
- **Priority**: High
- **Implementation**:
  - Add TOTP-based 2FA for sensitive accounts
  - Require MFA for admin users
  - Implement backup codes
  - Add device fingerprinting
  - Monitor for suspicious login patterns

### Input Validation & Sanitization

#### CM-5: Comprehensive Input Validation
- **Addresses**: T-2, T-3, E-5
- **Priority**: High
- **Implementation**:
  - Validate all input fields with strict schemas
  - Use DRF serializer validation consistently
  - Implement field-level validators for length, format, content
  - Sanitize HTML content in articles/comments (use bleach library)
  - Validate file uploads (if implemented)
  - Reject malformed JSON requests
  - Implement whitelist-based validation where possible

#### CM-6: Parameterized Queries and ORM Best Practices
- **Addresses**: T-2
- **Priority**: High
- **Implementation**:
  - Never use raw SQL with string concatenation
  - Use Django ORM exclusively or properly parameterized queries
  - Audit all database queries for injection vulnerabilities
  - Use ORM methods (.filter(), .get()) instead of raw queries
  - Validate and sanitize slug parameters

#### CM-7: Content Security Policy (CSP)
- **Addresses**: S-2, I-3
- **Priority**: Medium
- **Implementation**:
  - Implement strict CSP headers
  - Disable inline scripts and styles
  - Whitelist trusted script sources
  - Add X-Content-Type-Options: nosniff
  - Add X-Frame-Options: DENY
  - Add X-XSS-Protection: 1; mode=block

### Rate Limiting & DoS Prevention

#### CM-8: Implement Rate Limiting
- **Addresses**: D-1, D-2, E-3
- **Priority**: High
- **Implementation**:
  - Use django-ratelimit or DRF throttling classes
  - Implement per-IP rate limits on authentication endpoints (e.g., 5 attempts per 15 minutes)
  - Throttle API requests per user (e.g., 1000 requests per hour)
  - Implement stricter limits for anonymous users
  - Add rate limiting to registration endpoint
  - Rate limit content creation (articles, comments)
  - Return 429 Too Many Requests with Retry-After header

#### CM-9: Request Size and Complexity Limits
- **Addresses**: D-1, D-3
- **Priority**: Medium
- **Implementation**:
  - Set maximum request body size (e.g., 1MB)
  - Limit article body length (e.g., 100,000 characters)
  - Limit comment length (e.g., 10,000 characters)
  - Set maximum pagination page size (e.g., 100 items)
  - Implement query timeouts
  - Add complexity limits to GraphQL if implemented

#### CM-10: Database Optimization and Protection
- **Addresses**: D-1
- **Priority**: High
- **Implementation**:
  - Migrate from SQLite to production database (PostgreSQL, MySQL)
  - Add database connection pooling
  - Implement query optimization and indexing
  - Use select_related() and prefetch_related() to prevent N+1 queries
  - Add database query monitoring
  - Set statement timeouts

### Logging & Monitoring

#### CM-11: Comprehensive Security Logging
- **Addresses**: R-1, R-2, R-3
- **Priority**: High
- **Implementation**:
  - Log all authentication events (login, logout, registration, failures)
  - Log authorization failures
  - Log all content modifications (create, update, delete)
  - Log admin actions
  - Include timestamp, user ID, IP address, user agent
  - Send logs to centralized logging system (e.g., ELK, Splunk)
  - Implement log retention policy
  - Do NOT log sensitive data (passwords, tokens)

#### CM-12: Security Monitoring and Alerting
- **Addresses**: S-1, S-2, E-3, D-1, D-2
- **Priority**: Medium
- **Implementation**:
  - Monitor for brute force attempts
  - Alert on multiple failed login attempts
  - Monitor for unusual API usage patterns
  - Track rate of account creation
  - Monitor for privilege escalation attempts
  - Implement intrusion detection system (IDS)
  - Set up automated incident response

### Configuration & Deployment

#### CM-13: Secure Production Configuration
- **Addresses**: I-1, I-3
- **Priority**: Critical
- **Implementation**:
  - Set DEBUG=False in production
  - Configure ALLOWED_HOSTS restrictively
  - Remove django-extensions in production
  - Use environment-specific settings files
  - Implement custom error pages (400, 403, 404, 500)
  - Configure secure error handling (no stack traces)
  - Disable directory listing
  - Remove or secure /admin/ endpoint (change URL, add IP whitelist)

#### CM-14: HTTPS/TLS Implementation
- **Addresses**: S-2, I-5
- **Priority**: Critical
- **Implementation**:
  - Enforce HTTPS for all connections
  - Set SECURE_SSL_REDIRECT=True
  - Set SESSION_COOKIE_SECURE=True
  - Set CSRF_COOKIE_SECURE=True
  - Implement HSTS headers
  - Use TLS 1.2 or higher
  - Configure strong cipher suites
  - Implement certificate pinning for mobile apps

#### CM-15: CORS Configuration Hardening
- **Addresses**: I-5, T-4
- **Priority**: Medium
- **Implementation**:
  - Restrict CORS_ORIGIN_WHITELIST to production domains only
  - Never use wildcard origins in production
  - Set CORS_ALLOW_CREDENTIALS carefully
  - Validate Origin header on server side
  - Implement separate CORS policies for different endpoints
  - Remove development origins (localhost, 0.0.0.0) from production

### Dependency Management

#### CM-16: Upgrade Vulnerable Dependencies
- **Addresses**: S-1, T-2, E-4, Multiple
- **Priority**: Critical
- **Implementation**:
  - Upgrade Django to latest LTS version (3.2+ or 4.2+)
  - Upgrade Django REST Framework to latest version (3.14+)
  - Upgrade PyJWT to latest version (2.x)
  - Update all dependencies to latest secure versions
  - Implement automated dependency scanning (e.g., Safety, Snyk, Dependabot)
  - Regular security patch application schedule
  - Test upgrades in staging environment first

#### CM-17: Dependency Vulnerability Monitoring
- **Addresses**: All threats (proactive)
- **Priority**: High
- **Implementation**:
  - Use pip-audit or Safety to scan for known vulnerabilities
  - Integrate security scanning in CI/CD pipeline
  - Subscribe to security advisories for used libraries
  - Implement automated alerts for new vulnerabilities
  - Maintain updated requirements.txt with pinned versions
  - Regular security review of third-party packages

### Data Protection

#### CM-18: Sensitive Data Protection
- **Addresses**: I-4, I-2
- **Priority**: High
- **Implementation**:
  - Hash passwords with strong algorithm (Django's PBKDF2 default is acceptable, consider Argon2)
  - Never log or display passwords
  - Implement proper password policies (minimum length, complexity)
  - Encrypt sensitive data at rest (if applicable)
  - Mask email addresses in public APIs (show only partial)
  - Implement data retention policies
  - Add PII data encryption for highly sensitive fields

#### CM-19: Secure Password Policies
- **Addresses**: E-3, S-1
- **Priority**: High
- **Implementation**:
  - Enforce minimum password length (12+ characters)
  - Require password complexity
  - Implement password strength meter
  - Check against common password lists
  - Implement password history (prevent reuse)
  - Force password reset on compromise
  - Implement account lockout after failed attempts

### Testing & Validation

#### CM-20: Security Testing Program
- **Addresses**: All threats (proactive)
- **Priority**: High
- **Implementation**:
  - Implement automated security testing in CI/CD
  - Perform regular penetration testing
  - Conduct code security reviews
  - Use SAST tools (e.g., Bandit for Python)
  - Use DAST tools for runtime testing
  - Implement fuzz testing for API endpoints
  - Regular vulnerability scanning
  - Bug bounty program consideration

#### CM-21: API Security Best Practices
- **Addresses**: Multiple
- **Priority**: Medium
- **Implementation**:
  - Implement API versioning
  - Add request signing for sensitive operations
  - Implement request/response validation
  - Add API gateway with security policies
  - Implement IP whitelisting for admin APIs
  - Add request correlation IDs for tracing
  - Implement circuit breakers for external calls

### Incident Response

#### CM-22: Incident Response Plan
- **Addresses**: All threats (reactive)
- **Priority**: High
- **Implementation**:
  - Document incident response procedures
  - Define roles and responsibilities
  - Implement security incident detection
  - Create incident classification and escalation procedures
  - Establish communication protocols
  - Implement automated incident response playbooks
  - Regular incident response drills
  - Post-incident review process

### Additional Recommendations

#### CM-23: Security Headers Implementation
- **Priority**: Medium
- **Headers to Implement**:
  - Strict-Transport-Security: max-age=31536000; includeSubDomains
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
  - Referrer-Policy: strict-origin-when-cross-origin
  - Permissions-Policy: geolocation=(), microphone=(), camera=()

#### CM-24: Admin Interface Hardening
- **Priority**: High
- **Implementation**:
  - Change admin URL from /admin/ to non-obvious path
  - Implement IP whitelist for admin access
  - Require MFA for admin users
  - Add admin action logging
  - Implement admin session timeout
  - Regular admin access audits

#### CM-25: Content Validation and Moderation
- **Priority**: Medium
- **Implementation**:
  - Implement content moderation queue
  - Add spam detection
  - Implement profanity filters
  - Add malware scanning for uploads
  - Implement CAPTCHA for anonymous actions
  - Rate limit content creation by new users

---

## Review and Maintenance

This threat model should be reviewed and updated:
- Quarterly or after any significant system changes
- After security incidents
- When new features are added
- When new vulnerabilities are discovered in dependencies
- As part of compliance audit preparation

**Last Updated**: [Current Date]
**Next Review Date**: [Current Date + 90 days]
**Document Owner**: Security Team
**Approved By**: [Approval Authority]
