# google-adk-ignite

This project outlines a **multi-agent architecture** designed to extract market intelligence from PDF documents and produce insightful market reports using both human-in-the-loop input and advanced AI tools.

> **Note:** This system is built using the latest **Google Agent Development Kit (ADK)**, enabling robust agent orchestration, communication, and tool integration.

## 📊 Overview

The system is composed of five distinct agents, each responsible for a specific step in the pipeline. The flow is designed to be **modular, parallelizable**, and optionally extensible with agent-to-agent orchestration (A2A).

### ✅ Agents and Responsibilities

- **Agent ParseBot**  
  Parses PDF documents to extract structured entity data.

- **Agent Clarifier**  
  Presents the extracted entities for **human input/verification**.

- **Agent PriceProbe**  
  Uses the **Yahoo Tool** with **MCP (Market Clearing Price)** logic to fetch current market prices.

- **Agent DataSage**  
  Leverages **Gemini LLM** to generate product market reports from **historical data**.

- **Agent InsightX**  
  Consolidates information from other agents to generate a **final market report**.

## 🧰 Technology Stack

- **Google Agent Development Kit (ADK)** – Core framework for defining and managing agents  
- **Gemini LLM** – For historical data analysis and report generation  
- **Yahoo Finance APIs** – For real-time market pricing  

## 🔀 Flow Diagram

The system follows a partially parallel workflow:

```mermaid
flowchart LR
    A["<b>Agent ParseBot</b><br>Parse PDF for Entity Extraction"] --> B["<b>Agent Clarifier</b><br>Return list of Entities for Human input"]
    B --> C["<b>Agent PriceProbe</b><br>Use Yahoo Tool for Market Price using MCP"]
    B --> D["<b>Agent DataSage</b><br>Product Market Report on History Data from Gemini LLM"]
    C --> E["<b>Agent InsightX</b><br>Produce Market Report"]
    D --> E

classDef agentStyle fill:#f9f,stroke:#333,stroke-width:4px
class A,B,C,D,E agentStyle
'''