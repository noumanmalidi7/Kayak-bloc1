# Kayak Project

# 🏖️ Kayak France – Destination Recommender (Data Pipeline MVP)

> **Project Status**: Prototype / Proof of Concept  
> **Target Audience**: Marketing Team – Inspiring users to travel to France based on real-time weather and hotel availability.

---

## 📖 Table of Contents
1. [Project Overview](#-project-overview)
2. [Business Problem & Goal](#-business-problem--goal)
3. [High-Level Architecture](#-high-level-architecture)
4. [Tech Stack](#-tech-stack)
5. [Repository Structure](#-repository-structure)
6. [Setup & Installation](#-setup--installation)
7. [Environment Variables & Configuration](#-environment-variables--configuration)
8. [Pipeline Step-by-Step](#-pipeline-step-by-step)
   - [Step 1: Hotel Scraping (Booking.com)](#step-1-hotel-scraping-bookingcom)
   - [Step 2: Geocoding & Weather Data](#step-2-geocoding--weather-data)
   - [Step 3: Data Lake – AWS S3](#step-3-data-lake--aws-s3)
   - [Step 4: ETL – AWS RDS (Data Warehouse)](#step-4-etl--aws-rds-data-warehouse)
   - [Step 5: Visualization – Interactive Maps](#step-5-visualization--interactive-maps)
9. [Database Schema (RDS)](#-database-schema-rds)
10. [Deliverables](#-deliverables)
11. [Known Limitations & Future Improvements](#-known-limitations--future-improvements)
12. [Disclaimer](#-disclaimer)

---

## 📌 Project Overview

Kayak's marketing team discovered that **70% of users want destination information before booking**, but they distrust content from unknown brands. This MVP solves that by recommending the **Top 5 French cities** to visit right now, backed by **real-time weather data** and **live hotel inventory from our Booking.com ecosystem**.

**Scope**: 35 top-tourist cities in France (as listed by *One Week In*).  
**Output**: Two interactive maps showing the best destinations and the best hotels in those areas.
