"""
Knowledge Management Module for VentAI Enterprise

This module implements AI-driven knowledge management features including
knowledge repository, search, updates, and analytics.
"""

import os
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Setup logging
logger = logging.getLogger(__name__)

class KnowledgeManagement:
    """
    A class to manage AI-driven knowledge management features.
    """
    def __init__(self, config: Dict[str, Any], data_dir: str):
        """
        Initialize the KnowledgeManagement with configuration and data directory.

        Args:
            config (Dict[str, Any]): Configuration dictionary for knowledge management.
            data_dir (str): Directory for storing data files.
        """
        self.config = config
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        logger.info("Initialized KnowledgeManagement with config")

    def add_knowledge_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds a new knowledge article to the repository with metadata and categorization.

        Args:
            article_data (Dict[str, Any]): Data for the knowledge article including title, content, and metadata.

        Returns:
            Dict[str, Any]: Stored article data with unique ID and metadata.
        """
        logger.info(f"Adding knowledge article: {article_data.get('title', 'Untitled')}")
        try:
            article_id = article_data.get('article_id', f"article_{datetime.now().strftime('%Y%m%d%H%M%S%f')}")
            title = article_data.get('title', 'Untitled Article')
            content = article_data.get('content', '')
            category = article_data.get('category', self._categorize_article(content))
            tags = article_data.get('tags', self._generate_tags(content))
            
            stored_article = {
                "article_id": article_id,
                "title": title,
                "content": content,
                "category": category,
                "tags": tags,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": 1,
                "status": "active"
            }
            
            # Save article data
            article_file = os.path.join(self.data_dir, f"article_{article_id}.json")
            with open(article_file, 'w') as f:
                json.dump(stored_article, f, indent=2)
            logger.info(f"Saved knowledge article to {article_file}")
            
            return stored_article
        except Exception as e:
            logger.error(f"Error adding knowledge article {article_data.get('title', 'Untitled')}: {str(e)}")
            raise

    def _categorize_article(self, content: str) -> str:
        """
        Categorizes a knowledge article based on its content.

        Args:
            content (str): The content of the knowledge article.

        Returns:
            str: Determined category for the article.
        """
        content_lower = content.lower()
        if any(kw in content_lower for kw in ["troubleshoot", "error", "fix", "issue", "problem", "bug", "crash"]):
            return "technical_support"
        elif any(kw in content_lower for kw in ["billing", "payment", "invoice", "charge", "cost", "price", "refund"]):
            return "billing_information"
        elif any(kw in content_lower for kw in ["account", "login", "password", "profile", "user", "signup"]):
            return "account_management"
        elif any(kw in content_lower for kw in ["how to", "guide", "tutorial", "instructions", "use", "feature"]):
            return "product_usage"
        elif any(kw in content_lower for kw in ["policy", "terms", "conditions", "privacy", "compliance"]):
            return "policies_and_compliance"
        else:
            return "general_information"

    def _generate_tags(self, content: str) -> List[str]:
        """
        Generates tags for a knowledge article based on its content.

        Args:
            content (str): The content of the knowledge article.

        Returns:
            List[str]: List of relevant tags for the article.
        """
        content_lower = content.lower()
        tags = []
        if "login" in content_lower or "password" in content_lower:
            tags.append("login_issues")
        if "billing" in content_lower or "payment" in content_lower:
            tags.append("billing")
        if "error" in content_lower or "bug" in content_lower or "crash" in content_lower:
            tags.append("technical_error")
        if "how to" in content_lower or "guide" in content_lower:
            tags.append("tutorial")
        if "account" in content_lower or "profile" in content_lower:
            tags.append("account_settings")
        if "feature" in content_lower or "functionality" in content_lower:
            tags.append("product_feature")
        if not tags:
            tags.append("general")
        return tags

    def search_knowledge_base(self, query: str, category: Optional[str] = None, tags: Optional[List[str]] = None, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Searches the knowledge base for articles matching the query, category, and tags.

        Args:
            query (str): Search query to match against article titles and content.
            category (Optional[str]): Category filter for search results.
            tags (Optional[List[str]]): Tags to filter search results.
            max_results (int): Maximum number of results to return.

        Returns:
            List[Dict[str, Any]]: List of matching knowledge articles sorted by relevance.
        """
        logger.info(f"Searching knowledge base for query: {query}")
        try:
            articles = []
            query_lower = query.lower()
            for filename in os.listdir(self.data_dir):
                if filename.startswith("article_") and filename.endswith(".json"):
                    with open(os.path.join(self.data_dir, filename), 'r') as f:
                        article = json.load(f)
                        title_lower = article.get("title", "").lower()
                        content_lower = article.get("content", "").lower()
                        article_category = article.get("category", "")
                        article_tags = article.get("tags", [])
                        
                        # Basic relevance scoring based on query match
                        relevance_score = 0
                        if query_lower in title_lower:
                            relevance_score += 3
                        if query_lower in content_lower:
                            relevance_score += 1
                        if category and category == article_category:
                            relevance_score += 2
                        if tags and any(tag in article_tags for tag in tags):
                            relevance_score += 1
                        
                        if relevance_score > 0:
                            article["relevance_score"] = relevance_score
                            articles.append(article)
            
            # Sort by relevance score and limit to max_results
            articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
            return articles[:max_results]
        except Exception as e:
            logger.error(f"Error searching knowledge base for query {query}: {str(e)}")
            raise

    def suggest_knowledge_updates(self, article_id: str) -> Dict[str, Any]:
        """
        Suggests updates to an existing knowledge article based on usage trends and feedback.

        Args:
            article_id (str): ID of the article to check for updates.

        Returns:
            Dict[str, Any]: Suggestions for content updates or related articles to create.
        """
        logger.info(f"Suggesting updates for article: {article_id}")
        try:
            article_file = os.path.join(self.data_dir, f"article_{article_id}.json")
            if not os.path.exists(article_file):
                logger.error(f"Article {article_id} not found")
                raise ValueError(f"Article {article_id} not found")
            
            with open(article_file, 'r') as f:
                article = json.load(f)
            
            # Simulated AI analysis for update suggestions
            suggestions = {
                "article_id": article_id,
                "title": article.get("title", "Untitled"),
                "current_category": article.get("category", ""),
                "current_tags": article.get("tags", []),
                "suggested_updates": [],
                "suggested_related_articles": []
            }
            
            # Example logic for update suggestions
            if "login" in article.get("content", "").lower():
                suggestions["suggested_updates"].append("Update troubleshooting steps for login issues based on recent user feedback.")
                suggestions["suggested_related_articles"].append("Common Login Errors and Fixes")
            if "billing" in article.get("content", "").lower():
                suggestions["suggested_updates"].append("Review billing policies for recent changes in payment processing.")
                suggestions["suggested_related_articles"].append("Billing FAQ")
            if not suggestions["suggested_updates"]:
                suggestions["suggested_updates"].append("General content review recommended based on article age.")
            if not suggestions["suggested_related_articles"]:
                suggestions["suggested_related_articles"].append(f"{article.get('title', 'Untitled')} - Advanced Guide")
            
            logger.info(f"Generated update suggestions for article {article_id}")
            return suggestions
        except Exception as e:
            logger.error(f"Error suggesting updates for article {article_id}: {str(e)}")
            raise

    def generate_knowledge_analytics_report(self, report_type: str = "summary") -> Dict[str, Any]:
        """
        Generates analytics reports on knowledge base usage and effectiveness.

        Args:
            report_type (str): Type of report to generate (summary, detailed, usage_trends, content_gaps).

        Returns:
            Dict[str, Any]: Report data with insights on knowledge base metrics.
        """
        logger.info(f"Generating knowledge analytics report: {report_type}")
        try:
            articles_count = 0
            categories = {}
            tags_usage = {}
            for filename in os.listdir(self.data_dir):
                if filename.startswith("article_") and filename.endswith(".json"):
                    articles_count += 1
                    with open(os.path.join(self.data_dir, filename), 'r') as f:
                        article = json.load(f)
                        category = article.get("category", "uncategorized")
                        tags = article.get("tags", [])
                        
                        categories[category] = categories.get(category, 0) + 1
                        for tag in tags:
                            tags_usage[tag] = tags_usage.get(tag, 0) + 1
            
            report = {
                "report_type": report_type,
                "generated_at": datetime.now().isoformat(),
                "total_articles": articles_count,
                "category_distribution": categories,
                "tags_usage": tags_usage,
                "insights": []
            }
            
            if report_type == "summary":
                report["insights"].append(f"Total knowledge articles: {articles_count}")
                most_common_category = max(categories.items(), key=lambda x: x[1], default=("none", 0))[0]
                report["insights"].append(f"Most common category: {most_common_category}")
            elif report_type == "detailed":
                report["insights"].append("Detailed breakdown of content by category and tags provided.")
            elif report_type == "usage_trends":
                report["insights"].append("Usage trends simulation: High usage in technical support articles.")
            elif report_type == "content_gaps":
                if "technical_support" not in categories or categories.get("technical_support", 0) < 5:
                    report["insights"].append("Content gap: Insufficient technical support articles.")
                if "billing_information" not in categories or categories.get("billing_information", 0) < 3:
                    report["insights"].append("Content gap: Insufficient billing information articles.")
                if not report["insights"]:
                    report["insights"].append("No significant content gaps identified.")
            
            logger.info(f"Generated {report_type} knowledge analytics report")
            return report
        except Exception as e:
            logger.error(f"Error generating {report_type} knowledge analytics report: {str(e)}")
            raise
