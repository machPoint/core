# Git Cleanup Instructions - Remove .env from Repository

## ⚠️ IMPORTANT: Your .env file contains secrets and must be removed from Git

Your `.env` file contains your OpenAI API key and should never be committed to version control.

## Steps to Fix This

### 1. Remove .env from the current commit

```powershell
# Unstage the .env file
git reset HEAD .env

# Remove .env from Git tracking (but keep the local file)
git rm --cached .env
```

### 2. Verify .gitignore is working

The `.gitignore` file has been created and includes `.env`. Verify it's there:

```powershell
cat .gitignore
```

You should see `.env` listed in the file.

### 3. Commit the changes

```powershell
# Add the .gitignore file
git add .gitignore .env.example

# Commit without the .env file
git commit -m "Add .gitignore and remove .env from tracking"
```

### 4. Now commit your demo mode changes

```powershell
# Add all other changes
git add .

# Commit
git commit -m "demo mode"

# Push
git push
```

## What We Created

1. **`.gitignore`** - Prevents `.env` and other sensitive files from being tracked
2. **`.env.example`** - Template file showing what environment variables are needed
3. **Settings Page** - New "API Keys" tab where users can configure their OpenAI key

## For Future Users

When someone clones your repository, they should:

1. Copy `.env.example` to `.env`
   ```powershell
   cp .env.example .env
   ```

2. Edit `.env` and add their own API key

3. Or use the Settings page (Settings → API Keys tab) to configure it via the UI

## Security Best Practices

✅ **DO:**
- Keep `.env` in `.gitignore`
- Use `.env.example` as a template
- Store API keys in `.env` files locally
- Rotate your API key if it was exposed

❌ **DON'T:**
- Commit `.env` files to Git
- Share API keys in code or documentation
- Push secrets to public repositories
- Hardcode API keys in source code

## If Your Key Was Already Pushed

If you already pushed the commit with your API key:

1. **Immediately rotate your OpenAI API key** at https://platform.openai.com/api-keys
2. Delete the old key
3. Create a new key
4. Update your local `.env` file with the new key
5. Consider using `git filter-branch` or `BFG Repo-Cleaner` to remove the key from Git history (advanced)

## Need Help?

The Settings page now has an "API Keys" tab where you can:
- Enter your OpenAI API key securely
- Choose your preferred model
- See security information

Navigate to: **Settings → API Keys**
