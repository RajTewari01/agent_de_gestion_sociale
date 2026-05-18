# Authentication Architecture — From Zero to Production

> Tags: #learning #architecture #auth #security
> Confidence: 🟡 Building Understanding
> Related: [[Agent de Gestion Sociale]]

---

## Part 1: What Problem Does Auth Solve?

Auth answers two questions for every request:

1. **Authentication (AuthN)** — "WHO are you?" → Identity
2. **Authorization (AuthZ)** — "WHAT can you do?" → Permissions

They're different things. You can be authenticated (logged in) but not authorized (can't access admin panel).

---

## Part 2: The OAuth 2.0 Flow (How "Sign in with Google" Works)

OAuth is a **delegation protocol** — your app never sees the user's Google password. Google confirms the identity and hands you a token.

### The 4 Actors

| Actor | Role |
|---|---|
| **Resource Owner** | The user (Raj) |
| **Client** | Your app (Agent de Gestion Sociale) |
| **Authorization Server** | Google's OAuth server |
| **Resource Server** | Google's API (user profile, email, etc.) |

### The Flow Step by Step

**Step 1 — Registration (one-time setup)**

Before anything works, you register your app with Google at [console.cloud.google.com](https://console.cloud.google.com):

```
You give Google:
  → App name: "Agent de Gestion Sociale"
  → Redirect URI: "https://yourapp.com/auth/callback"

Google gives you:
  → CLIENT_ID:     "abc123.apps.googleusercontent.com"
  → CLIENT_SECRET: "GOCSPX-xxxxxxx"
```

These two values are how Google identifies YOUR app.

**Step 2 — User clicks "Sign in with Google"**

Your backend builds a URL and redirects the user:

```
https://accounts.google.com/o/oauth2/v2/auth?
  client_id=abc123.apps.googleusercontent.com
  &redirect_uri=https://yourapp.com/auth/callback
  &response_type=code
  &scope=openid email profile
  &state=random_csrf_token_xyz
```

Breaking this down:

| Parameter | Purpose |
|---|---|
| `client_id` | Tells Google WHICH app is asking |
| `redirect_uri` | Where to send the user after login |
| `response_type=code` | "Give me an authorization code, not a token directly" |
| `scope` | What data you want (email, profile picture, etc.) |
| `state` | Random string to prevent CSRF attacks — you verify this later |

**Step 3 — User logs in on Google's page**

Google shows its own login page. User enters their email/password.
Your app NEVER sees the password. This is the whole point of OAuth.

**Step 4 — Google redirects back to your app**

After login, Google sends the user to your redirect URI:

```
https://yourapp.com/auth/callback?
  code=4/0AX4XfWj...very_long_string
  &state=random_csrf_token_xyz
```

The `code` is a **one-time authorization code**. It's useless on its own — it must be exchanged.

**Step 5 — Your backend exchanges the code for tokens**

Your backend makes a **server-to-server** POST request (user never sees this):

```python
# This happens on YOUR server, not in the browser
POST https://oauth2.googleapis.com/token

{
    "code": "4/0AX4XfWj...",        # The code from step 4
    "client_id": "abc123...",         # Your app's ID
    "client_secret": "GOCSPX-...",   # Your app's secret (NEVER expose this)
    "redirect_uri": "https://yourapp.com/auth/callback",
    "grant_type": "authorization_code"
}
```

Google responds with:

```json
{
    "access_token":  "ya29.a0AfH6SM...",   // Use this to call Google APIs
    "id_token":      "eyJhbGciOiJSUzI...", // JWT with user info
    "refresh_token": "1//0gdJ3...",        // Use this to get new access tokens
    "expires_in":    3599,                 // Access token expires in 1 hour
    "token_type":    "Bearer"
}
```

**Step 6 — Decode the ID token to get user info**

The `id_token` is a JWT (JSON Web Token). Decode it:

```json
{
    "sub": "10769150350006150715113082367",  // Google's unique user ID
    "email": "raj@gmail.com",
    "email_verified": true,
    "name": "Raj Tewari",
    "picture": "https://lh3.googleusercontent.com/...",
    "iat": 1716000000,  // Issued at
    "exp": 1716003600   // Expires at
}
```

**Step 7 — Create or find the user in YOUR database**

```python
# Pseudocode
user = db.find_user(provider="google", provider_id=id_token["sub"])

if user is None:
    # First login — create account
    user = db.create_user(
        email=id_token["email"],
        name=id_token["name"],
        avatar=id_token["picture"],
        provider="google",
        provider_id=id_token["sub"],
    )

# Update last login
db.update_last_login(user.id)
```

**Step 8 — Issue YOUR OWN tokens**

Now you create your own session. Google's tokens are for calling Google's APIs. You need your own tokens for your own API.

```python
# Create YOUR access token (short-lived)
access_token = create_jwt(
    payload={"user_id": user.id, "role": user.role},
    secret=YOUR_SECRET_KEY,
    expires_in=timedelta(minutes=15),
)

# Create YOUR refresh token (long-lived)
refresh_token = create_random_token()  # Random 256-bit string
db.store_refresh_token(user.id, refresh_token, expires_in=timedelta(days=30))
```

**Step 9 — Send tokens to the frontend**

```python
response = redirect("/dashboard")
response.set_cookie(
    "access_token",
    access_token,
    httponly=True,    # JavaScript can't read it (prevents XSS)
    secure=True,      # Only sent over HTTPS
    samesite="lax",   # Prevents CSRF
    max_age=900,      # 15 minutes
)
response.set_cookie(
    "refresh_token",
    refresh_token,
    httponly=True,
    secure=True,
    samesite="lax",
    max_age=2592000,  # 30 days
)
```

> [!IMPORTANT] Why httpOnly cookies?
> If you store tokens in `localStorage`, any XSS attack (injected JavaScript) can steal them. `httpOnly` cookies are **invisible to JavaScript** — only the browser sends them automatically with each request. This is the industry standard.

---

## Part 3: JWTs (JSON Web Tokens)

A JWT is just a signed JSON object. It has 3 parts separated by dots:

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWJjMTIzIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
|_____header_____|._______payload________.|________signature________|
```

### Header
```json
{"alg": "HS256", "typ": "JWT"}
```
Says "this token is signed with HMAC-SHA256."

### Payload
```json
{
    "user_id": "abc123",
    "role": "admin",
    "iat": 1716000000,     // Issued at (Unix timestamp)
    "exp": 1716000900      // Expires at (15 min later)
}
```
The actual data. **This is NOT encrypted** — anyone can decode it (it's just base64). The signature proves it wasn't tampered with.

### Signature
```python
HMAC_SHA256(
    base64(header) + "." + base64(payload),
    YOUR_SECRET_KEY
)
```

If someone changes the payload (e.g., `role: "admin"` to `role: "superadmin"`), the signature won't match and your backend rejects it.

### JWT vs Session ID — When To Use What

| | JWT (Stateless) | Session ID (Stateful) |
|---|---|---|
| **Stored where** | Inside the token itself | Server-side (Redis/DB) |
| **DB lookup needed?** | No — just verify signature | Yes — every request |
| **Revocation** | Hard — must wait for expiry | Easy — delete from DB |
| **Scalability** | Better — no shared state | Needs shared Redis |
| **Best for** | API authentication | Web sessions with logout |

> [!TIP] The industry pattern
> Use **short-lived JWTs** (15 min) for API auth + **long-lived refresh tokens** in the database for re-issuing. This gives you stateless speed + the ability to revoke access.

---

## Part 4: Token Refresh — How Users Stay Logged In

Users don't re-login every 15 minutes. Here's the refresh cycle:

```
Minute 0:   Login → get access_token (15 min) + refresh_token (30 days)
Minute 14:  Frontend calls API → access_token still valid → works
Minute 16:  Frontend calls API → access_token EXPIRED → 401 error
            Frontend automatically calls /auth/refresh with refresh_token
            Backend validates refresh_token in DB → issues NEW access_token
            Frontend retries the original request → works
Day 30:     refresh_token expires → user must log in again
```

### The refresh endpoint

```python
@app.post("/auth/refresh")
def refresh(request):
    refresh_token = request.cookies.get("refresh_token")

    # Look up in database
    stored = db.find_refresh_token(refresh_token)

    if stored is None or stored.is_expired:
        return 401  # Force re-login

    # Issue new access token
    new_access_token = create_jwt(
        payload={"user_id": stored.user_id},
        expires_in=timedelta(minutes=15),
    )

    # OPTIONAL: Rotate refresh token (more secure)
    new_refresh_token = create_random_token()
    db.delete_refresh_token(refresh_token)
    db.store_refresh_token(stored.user_id, new_refresh_token)

    response = jsonify({"status": "refreshed"})
    response.set_cookie("access_token", new_access_token, httponly=True, ...)
    response.set_cookie("refresh_token", new_refresh_token, httponly=True, ...)
    return response
```

> [!WARNING] Refresh Token Rotation
> Every time you use a refresh token, **invalidate the old one** and issue a new one. If an attacker steals a refresh token, the next time the real user refreshes, the stolen token becomes invalid and you can detect the breach.

---

## Part 5: Auth Middleware (The Guard)

Every API request passes through this before reaching your route handler:

```python
from functools import wraps
import jwt

SECRET_KEY = "your-256-bit-secret"

def require_auth(func):
    """Decorator that protects a route."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.cookies.get("access_token")

        if not token:
            return {"error": "No token provided"}, 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401

        # Attach user info to request
        request.user_id = payload["user_id"]
        request.role = payload.get("role", "user")

        return func(request, *args, **kwargs)
    return wrapper


# Usage
@app.get("/api/posts")
@require_auth
def get_posts(request):
    # request.user_id is available here
    posts = db.get_posts_for_user(request.user_id)
    return posts
```

### Authorization (role-based)

```python
def require_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        @require_auth  # Must be authenticated first
        def wrapper(request, *args, **kwargs):
            if request.role not in allowed_roles:
                return {"error": "Insufficient permissions"}, 403
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

# Only admins can delete users
@app.delete("/api/users/{user_id}")
@require_role("admin")
def delete_user(request, user_id):
    db.delete_user(user_id)
```

---

## Part 6: The Users Table (Database Schema)

```sql
-- Core user identity
CREATE TABLE users (
    id              TEXT PRIMARY KEY,   -- UUID
    email           TEXT UNIQUE NOT NULL,
    name            TEXT,
    avatar_url      TEXT,
    role            TEXT DEFAULT 'user', -- user, admin, etc.
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at   TIMESTAMP
);

-- OAuth provider links (one user can have Google + GitHub)
CREATE TABLE oauth_accounts (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    provider        TEXT NOT NULL,       -- 'google', 'github'
    provider_id     TEXT NOT NULL,       -- Google's unique ID for this user
    access_token    TEXT,                -- Google's access token (for their API)
    refresh_token   TEXT,                -- Google's refresh token
    UNIQUE(provider, provider_id)
);

-- YOUR refresh tokens (for your own auth system)
CREATE TABLE refresh_tokens (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    token_hash      TEXT NOT NULL,       -- Store HASHED, never plain text
    expires_at      TIMESTAMP NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

> [!CAUTION] Never store refresh tokens in plain text
> Hash them with SHA-256 before storing. When validating, hash the incoming token and compare hashes. Same principle as password storage — if your DB leaks, the tokens are useless to attackers.

---

## Part 7: Security Checklist

### Must-Do (Non-Negotiable)

- [ ] **httpOnly cookies** for all tokens — prevents XSS theft
- [ ] **Secure flag** on cookies — only sent over HTTPS
- [ ] **SameSite=Lax** — prevents CSRF attacks
- [ ] **Short-lived access tokens** — 15 minutes max
- [ ] **Hash refresh tokens** in the database
- [ ] **Rotate refresh tokens** on every use
- [ ] **Validate `state` parameter** in OAuth callback — prevents CSRF
- [ ] **Validate `redirect_uri`** — prevent open redirect attacks
- [ ] **Rate limit** login and refresh endpoints

### Should-Do (Production Hardening)

- [ ] **CORS whitelist** — only your frontend domain
- [ ] **Token binding** — tie tokens to IP or device fingerprint
- [ ] **Audit logging** — log every login, logout, token refresh
- [ ] **Anomaly detection** — flag logins from new countries/devices
- [ ] **Brute force protection** — lock account after N failed attempts

---

## Part 8: What To Read Next

### Source Code (Best Way to Learn)

| Repo | Why Read It |
|---|---|
| [lucia-auth](https://github.com/lucia-auth/lucia) | Minimal, clear — you can read the whole thing in an afternoon |
| [next-auth](https://github.com/nextauthjs/next-auth) | See how a production OAuth library handles 20+ providers |
| [supabase/gotrue](https://github.com/supabase/gotrue) | Go-based auth microservice — see how Supabase does it |

### Concepts to Deep-Dive

| Topic | Why |
|---|---|
| **PKCE (Proof Key for Code Exchange)** | Required for mobile/SPA OAuth — prevents code interception |
| **OpenID Connect (OIDC)** | The identity layer built on top of OAuth 2.0 |
| **RBAC vs ABAC** | Role-Based vs Attribute-Based access control |
| **Passkeys / WebAuthn** | The passwordless future — biometric auth |

### RFCs (The Specifications)

| RFC | What It Defines |
|---|---|
| RFC 6749 | OAuth 2.0 framework |
| RFC 7519 | JWT specification |
| RFC 7636 | PKCE extension |
| RFC 6750 | Bearer token usage |

---

## Part 9: How This Maps to Your Project

For **Agent de Gestion Sociale**, here's the recommended architecture:

| Component | Technology | Owner |
|---|---|---|
| Google OAuth flow | `authlib` | Backend (you) |
| JWT creation/validation | `PyJWT` or `python-jose` | Backend (you) |
| Auth middleware | Custom decorator (see Part 5) | Backend (you) |
| User DB | SQLite (you already have `db/base.py`) | Backend (you) |
| Login UI | Next.js page | Frontend (me) |
| Token storage | httpOnly cookies | Set by backend |
| Token refresh | Automatic on 401 | Frontend (me) |

Your plugin system can have an `AuthService.xml` manifest:

```xml
<plugin id="auth_service">
    <modules>
        <module name="oauth">src.backend.auth.oauth</module>
        <module name="tokens">src.backend.auth.tokens</module>
        <module name="middleware">src.backend.auth.middleware</module>
    </modules>
    <dependencies>
        <package version=">=1.3.0">authlib</package>
        <package version=">=2.8.0">PyJWT</package>
    </dependencies>
</plugin>
```

---

## Related
- [[Plugin Architecture]]
- [[Agent de Gestion Sociale]]
- [[Dependencies Tracker]]
