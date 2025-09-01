#!/usr/bin/env python3

import os
from typing import List
from github import Github
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("GitHub PR Reviewer")

# Load GitHub credentials
github_token = os.getenv("GITHUB_TOKEN")
github_username = os.getenv("GITHUB_USERNAME")

if not github_token or not github_username:
    raise ValueError("GITHUB_TOKEN and GITHUB_USERNAME must be set in .env file")

github = Github(github_token)

@mcp.tool()
async def get_my_review_prs(limit: int = 10) -> str:
    """Fetch GitHub pull requests that need your review.
    
    Args:
        limit: Maximum number of PRs to return (default: 10)
    
    Returns:
        Formatted list of PRs needing review
    """
    try:
        user = github.get_user()
        prs_needing_review = []
        
        # Search for open PRs where the user is requested as a reviewer
        query = f"type:pr state:open review-requested:{github_username}"
        
        search_results = github.search_issues(query, sort="updated", order="desc")
        
        count = 0
        for issue in search_results:
            if count >= limit:
                break
            
            # Get the actual PR object
            repo = github.get_repo(issue.repository.full_name)
            pr = repo.get_pull(issue.number)
            
            # Check if PR still needs review (not already reviewed by user)
            reviews = pr.get_reviews()
            user_reviewed = any(review.user.login == github_username for review in reviews)
            
            if not user_reviewed:
                pr_info = {
                    "title": pr.title,
                    "url": pr.html_url,
                    "repository": issue.repository.full_name,
                    "author": pr.user.login,
                    "created_at": pr.created_at.strftime("%Y-%m-%d %H:%M UTC"),
                    "updated_at": pr.updated_at.strftime("%Y-%m-%d %H:%M UTC"),
                    "summary": pr.body[:200] + "..." if pr.body and len(pr.body) > 200 else pr.body or "No description provided",
                    "number": pr.number,
                    "draft": pr.draft,
                    "additions": pr.additions,
                    "deletions": pr.deletions,
                    "changed_files": pr.changed_files
                }
                prs_needing_review.append(pr_info)
                count += 1
        
        if not prs_needing_review:
            return "🎉 No pull requests currently need your review!"
        
        # Format the response
        response_text = f"📋 **{len(prs_needing_review)} Pull Request{'s' if len(prs_needing_review) != 1 else ''} Needing Your Review:**\n\n"
        
        for i, pr in enumerate(prs_needing_review, 1):
            draft_indicator = " 🚧 [DRAFT]" if pr["draft"] else ""
            response_text += f"**{i}. {pr['title']}{draft_indicator}**\n"
            response_text += f"   📁 Repository: {pr['repository']}\n"
            response_text += f"   👤 Author: {pr['author']}\n"
            response_text += f"   🔗 Link: {pr['url']}\n"
            response_text += f"   📅 Created: {pr['created_at']}\n"
            response_text += f"   📝 Updated: {pr['updated_at']}\n"
            response_text += f"   📊 Changes: +{pr['additions']} -{pr['deletions']} ({pr['changed_files']} files)\n"
            response_text += f"   📄 Summary: {pr['summary']}\n\n"
        
        return response_text
        
    except Exception as e:
        return f"❌ Error fetching PRs: {str(e)}"

if __name__ == "__main__":
    mcp.run()