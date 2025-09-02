# GitHub PR Review MCP Server

A Model Context Protocol (MCP) server that helps you fetch GitHub pull requests that need your review and integrates with Claude Code.

## Features

- Fetches open pull requests where you are requested as a reviewer
- Filters out PRs you've already reviewed
- Returns detailed information including PR title, link, summary, author, and change statistics
- Easy integration with Claude Code

## Setup Instructions

### 1. Installation

```bash
cd ~/Desktop/github-pr-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. GitHub Authentication

1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate a new token with these scopes: `read:user`, `repo`

2. Create your `.env` file:
```bash
touch .env
```

3. Edit `.env` and add your credentials:
```
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_USERNAME=your_github_username
```

### 3. Test the Server

Run the server directly to test:
```bash
python fastmcp_server.py
```

### 4. Claude Code Integration

Add this configuration to your Claude Code MCP settings (usually in `~/.config/claude-code/mcp_servers.json`):

```json
{
  "github-pr-reviewer": {
    "command": "/opt/homebrew/bin/python3.12",
    "args": ["/Users/lynn_kong/Desktop/github-pr-mcp/fastmcp_server.py"],
    "env": {
      "PYTHONPATH": "/Users/lynn_kong/Desktop/github-pr-mcp/venv/lib/python3.12/site-packages"
    },
    "cwd": "/Users/lynn_kong/Desktop/github-pr-mcp"
  }
}
```

### 5. Usage in Claude Code

Once configured, you can ask Claude Code:
- "What PRs need my review?"
- "Show me pull requests I need to review"
- "Get my GitHub review queue"

The tool will return a formatted list with:
- PR title and draft status
- Repository name
- Author
- Direct link to the PR
- Creation and update dates
- Change statistics (additions, deletions, files changed)
- Brief summary

## Tool Parameters

- `limit` (optional): Maximum number of PRs to return (default: 10)

## Error Handling

The server includes comprehensive error handling for:
- Missing GitHub credentials
- API rate limits
- Network issues
- Invalid repositories

## Dependencies

- `mcp>=0.9.0` - Model Context Protocol framework
- `PyGithub>=2.1.1` - GitHub API client
- `python-dotenv>=1.0.0` - Environment variable management

## Requirements

- Python 3.8+
- GitHub Personal Access Token with `read:user` and `repo` scopes
- Claude Code with MCP support