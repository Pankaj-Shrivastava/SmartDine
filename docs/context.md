# SmartDine — Project Context

> Source: [problemStatement.txt](file:///c:/Users/panka/Documents/Pankaj_CodeSpace/AI_Projects/SmartDine/docs/problemStatement.txt)

---

## Problem Statement

**AI-Powered Restaurant Recommendation System (Zomato Use Case)**

Build an AI-powered restaurant recommendation service inspired by Zomato. The system should intelligently suggest restaurants based on user preferences by combining structured data with a Large Language Model (LLM).

---

## Objective

Design and implement an application that:

1. Takes user preferences (such as location, budget, cuisine, and ratings)
2. Uses a real-world dataset of restaurants
3. Leverages an LLM to generate personalized, human-like recommendations
4. Displays clear and useful results to the user

---

## System Workflow

### 1. Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face:
  **[ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)**
- Extract relevant fields such as restaurant name, location, cuisine, cost, rating, etc.

### 2. User Input

Collect user preferences:

| Preference | Examples |
|---|---|
| **Location** | Delhi, Bangalore |
| **Budget** | Low, Medium, High |
| **Cuisine** | Italian, Chinese |
| **Minimum Rating** | e.g., 3.5+ |
| **Additional Preferences** | Family-friendly, Quick service |

### 3. Integration Layer

- Filter and prepare relevant restaurant data based on user input
- Pass structured results into an LLM prompt
- Design a prompt that helps the LLM reason and rank options

### 4. Recommendation Engine

Use the LLM to:

- **Rank** restaurants based on relevance to user preferences
- **Explain** why each recommendation fits the user's criteria
- **Summarize** choices (optional)

### 5. Output Display

Present top recommendations in a user-friendly format with the following fields:

| Field | Description |
|---|---|
| **Restaurant Name** | Name of the recommended restaurant |
| **Cuisine** | Type of cuisine served |
| **Rating** | User/aggregate rating |
| **Estimated Cost** | Approximate cost for a meal |
| **AI-Generated Explanation** | Why this restaurant was recommended |
