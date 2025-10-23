# GitHub Personal Access Token Setup for RuvScan

RuvScan needs a GitHub Personal Access Token (PAT) to scan repositories and access README files. This guide shows you exactly what scopes to enable.

---

## 🎯 Why Do You Need a Token?

RuvScan scans GitHub repositories to:
- Read repository metadata (name, description, topics, stars)
- Fetch README files for analysis
- List repositories in organizations
- Search for repositories by topic

**Without a token:**
- Rate limit: 60 requests/hour
- Can't access private repos
- Can't access org-level data

**With a token:**
- Rate limit: 5,000 requests/hour
- Can access your private repos (if you want)
- Can scan your organization's repositories

---

## 🔑 Required Scopes (Minimum)

For **public repository scanning only**, you need these scopes:

### Classic Token (Recommended for beginners)

✅ **`public_repo`** - Access public repositories
- Allows reading public repo data
- Lets RuvScan fetch READMEs
- **This is the minimum scope needed**

### Fine-Grained Token (More secure, recommended for production)

✅ **Repository permissions:**
- **Metadata**: Read-only ✅ (automatically included)
- **Contents**: Read-only ✅ (for READMEs)

---

## 🏢 Optional Scopes (For Organizations)

If you want to scan **private repos or organizations**, add:

### Classic Token

✅ **`repo`** - Full control of private repositories
- Includes `public_repo` plus private repo access
- Use this if scanning private repos

✅ **`read:org`** - Read organization data
- Required for organization scanning
- Allows listing org repositories

### Fine-Grained Token

✅ **Repository permissions:**
- **Contents**: Read-only ✅
- **Metadata**: Read-only ✅

✅ **Organization permissions:**
- **Members**: Read-only (for org listing)

---

## 📝 Step-by-Step: Create a Classic Token (Easiest)

### 1. Go to GitHub Settings

Visit: https://github.com/settings/tokens

Or:
1. Click your profile picture (top right)
2. Settings
3. Developer settings (bottom left)
4. Personal access tokens
5. Tokens (classic)

### 2. Generate New Token

Click **"Generate new token"** → **"Generate new token (classic)"**

### 3. Configure Token

**Note (name)**: `RuvScan - Public Repos`

**Expiration**:
- No expiration (easiest)
- OR 90 days (more secure, you'll need to renew)

**Select scopes:**

For **public repos only**:
```
✅ public_repo
   Access public repositories
```

For **private repos + orgs**:
```
✅ repo
   Full control of private repositories
   (includes public_repo)

✅ read:org
   Read organization and team membership
```

### 4. Generate & Copy Token

1. Click **"Generate token"** (bottom)
2. **COPY THE TOKEN NOW** - You won't see it again!
3. It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 📝 Step-by-Step: Create a Fine-Grained Token (More Secure)

### 1. Go to GitHub Settings

Visit: https://github.com/settings/tokens?type=beta

Or:
1. Click your profile picture
2. Settings
3. Developer settings
4. Personal access tokens
5. Fine-grained tokens

### 2. Generate New Token

Click **"Generate new token"**

### 3. Configure Token

**Token name**: `RuvScan Scanner`

**Expiration**: Your choice (90 days recommended)

**Description**: `Token for RuvScan to scan GitHub repos`

**Resource owner**: Your username (or organization)

**Repository access**:
- **Public repositories (read-only)** - For public scanning
- OR **All repositories** - If you want private repo access

**Permissions**:

Under **Repository permissions**:
- **Contents**: Read-only ✅ (for READMEs)
- **Metadata**: Read-only ✅ (auto-selected, for repo info)

Under **Organization permissions** (if scanning orgs):
- **Members**: Read-only (for listing org repos)

### 4. Generate & Copy

1. Click **"Generate token"**
2. **COPY THE TOKEN** - Starts with `github_pat_`
3. Store it securely

---

## 🔒 Storing Your Token Securely

### Option 1: Environment Variable (Development)

```bash
# Add to your .env file:
echo "GITHUB_TOKEN=ghp_your_token_here" >> .env

# Never commit .env to git!
# (already in .gitignore)
```

### Option 2: Environment Variable (Shell)

```bash
# Add to ~/.bashrc or ~/.zshrc:
export GITHUB_TOKEN="ghp_your_token_here"

# Reload shell:
source ~/.bashrc
```

### Option 3: Docker Secret (Production)

```bash
# Create secret:
echo "ghp_your_token_here" | docker secret create github_token -

# Use in docker-compose:
secrets:
  github_token:
    external: true
```

### Option 4: Kubernetes Secret (Production)

```bash
# Create secret:
kubectl create secret generic github-token \
  --from-literal=token='ghp_your_token_here'

# Reference in deployment:
env:
- name: GITHUB_TOKEN
  valueFrom:
    secretKeyRef:
      name: github-token
      key: token
```

---

## ✅ Verify Your Token Works

### Test with curl:

```bash
# Replace with your token:
export GITHUB_TOKEN="ghp_your_token_here"

# Test the token:
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user

# Should return your user info (JSON)
```

### Test with RuvScan:

```bash
# Start RuvScan:
docker-compose up -d

# Trigger a scan:
./scripts/ruvscan scan org ruvnet --limit 5

# Should see:
# ✅ Scan initiated
# Found 5 repositories
```

---

## 🔐 Security Best Practices

### ✅ DO:
- Use fine-grained tokens when possible (more secure)
- Set expiration dates
- Use minimal scopes needed
- Store in environment variables or secrets
- Rotate tokens regularly
- Use different tokens for different environments

### ❌ DON'T:
- Commit tokens to git
- Share tokens publicly
- Use tokens with more permissions than needed
- Store in plaintext files that get backed up
- Reuse the same token across multiple projects

---

## 🔄 Token Rotation

When your token expires or you need to rotate:

1. **Create new token** (same scopes)
2. **Update environment**:
   ```bash
   # Update .env:
   GITHUB_TOKEN=ghp_new_token_here

   # Restart RuvScan:
   docker-compose restart
   ```
3. **Revoke old token**:
   - Go to https://github.com/settings/tokens
   - Find old token
   - Click "Delete"

---

## ⚠️ Troubleshooting

### "Bad credentials" error

**Problem**: Token is invalid or expired

**Solution**:
```bash
# Check token is set:
echo $GITHUB_TOKEN

# Test token:
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user

# If expired, create new token
```

### "Rate limit exceeded"

**Problem**: Too many requests

**Solution**:
```bash
# Check rate limit:
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit

# With token: 5000/hour
# Without token: 60/hour

# Make sure RuvScan is using your token!
```

### "Not Found" or "Resource not found"

**Problem**: Token doesn't have required scopes

**Solution**:
1. Check token scopes match requirements above
2. For orgs, make sure you have `read:org`
3. For private repos, use `repo` scope

---

## 📊 Scope Comparison

| Use Case | Classic Token | Fine-Grained Token |
|----------|--------------|-------------------|
| **Public repos only** | `public_repo` | Contents: Read-only |
| **Private repos** | `repo` | Contents: Read-only + All repos |
| **Organizations** | `read:org` | Members: Read-only |
| **Your profile** | Auto-included | Metadata: Read-only |

---

## 🎯 Quick Reference

**For most users (public repos)**:
```
Classic Token:
✅ public_repo

Fine-Grained Token:
✅ Contents: Read-only
```

**For organization scanning**:
```
Classic Token:
✅ public_repo
✅ read:org

Fine-Grained Token:
✅ Contents: Read-only
✅ Members: Read-only
```

**For private repos**:
```
Classic Token:
✅ repo
✅ read:org (if needed)

Fine-Grained Token:
✅ Contents: Read-only
✅ Resource owner: All repositories
```

---

## 🚀 Ready to Go!

Once you have your token:

1. **Add to .env**:
   ```bash
   GITHUB_TOKEN=ghp_your_token_here
   ```

2. **Start RuvScan**:
   ```bash
   docker-compose up -d
   ```

3. **Scan away**:
   ```bash
   ./scripts/ruvscan scan org ruvnet
   ```

---

**Questions?** Open an [issue](https://github.com/ruvnet/ruvscan/issues) or check [Discussions](https://github.com/ruvnet/ruvscan/discussions).
