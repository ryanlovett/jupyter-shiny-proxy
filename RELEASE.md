# Release Procedure

This document outlines the steps to publish a new version of `jupyter-shiny-proxy` to PyPI using our GitHub Actions Trusted Publishing setup.

## One-Time Setup (PyPI)

Before the first automated release, PyPI was configured to trust this GitHub repository.

1. In the project on PyPI: **Manage -> Publishing -> Add a new publisher**.
2. Select **GitHub**.
3. Fill in the details:
   - **Owner:** `ryanlovett`
   - **Repository:** `jupyter-shiny-proxy`
   - **Workflow name:** `publish.yml`
   - **Environment name:** `pypi`

## Standard Publishing Workflow

### 1. Develop and Merge
1. Create a branch for your new feature or bug fix.
2. Make your code changes.
3. Submit a Pull Request to the default branch (e.g., `main` or `master`).
4. Review and merge the Pull Request.

### 2. Bump the Version
When you are ready to cut a new release, you need to update the version number.
1. Open `pyproject.toml`.
2. Update the `version` field (e.g., change `version = "1.4"` to `version = "1.5"`).
3. Commit this change and push it to the default branch (you can do this directly or via a "Release 1.5" PR).

### 3. Tag and Release (Triggers Automation)
The publishing workflow is configured to run automatically when a GitHub Release is published. Once the version bump is merged into the default branch, you should tag the release and publish it on GitHub.

You can create and push the tag via Git CLI:
```bash
# Ensure you are up to date on the main branch
git checkout main
git pull

# Create the tag (e.g., for version 1.5)
git tag v1.5

# Push the tag to GitHub
git push origin v1.5
```

After pushing the tag, you still need to create the Release on GitHub to trigger the workflow:
1. Go to the repository on GitHub.
2. On the right-hand sidebar, click on **Releases**, then click **Draft a new release**.
3. Click **Choose a tag** and select your newly pushed tag (e.g., `v1.5`).
4. Set the Release title (e.g., "Release v1.5") and optionally add release notes.
5. Click the green **Publish release** button.

### 4. The Workflow Runs
1. Publishing the GitHub release immediately triggers the `.github/workflows/publish.yml` workflow.
2. You can watch the progress in the **Actions** tab on GitHub.
3. The workflow will:
   - Check out the code.
   - Install build tools and build the `.tar.gz` (sdist) and `.whl` (wheel) using `hatchling`.
   - Securely request a short-lived OIDC token from GitHub.
   - Send the token and the built packages to PyPI.
4. Once the action succeeds, the new version is live on PyPI!

## Alternative: Manual Publishing

If you ever need to publish *without* creating a GitHub Release (for example, if a previous publish failed due to a PyPI outage and you need to retry), you can trigger it manually.

1. Ensure the version in `pyproject.toml` is correct on your default branch.
2. Go to the **Actions** tab in the GitHub repository.
3. Click on **Publish to PyPI** on the left sidebar.
4. Click the **Run workflow** dropdown on the right.
5. Select the branch (usually `main`) and click **Run workflow**.
