# envcheck

A fast, zero-dependency CLI utility that validates `.env` files against `.env.example` so missing or blank environment variables never break a build or production deploy.

## Why?
Apps often fail at runtime when a new variable is added to `.env.example` during code review, or when a deployment environment has an empty secret. `envcheck` catches both in one command using only the Python standard library.

## Usage

```bash
# Check .env against .env.example in the current directory
python3 envcheck.py

# Specify custom file paths
python3 envcheck.py --env .env.production --example .env.template

# Allow keys with empty values
python3 envcheck.py --allow-empty
