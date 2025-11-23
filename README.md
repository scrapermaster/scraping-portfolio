# Advanced Web Scraping & Automation Portfolio

**Automation Engineer** with 7+ years of experience architecting distributed scraping pipelines.
Specializing in **anti-bot evasion** (Cloudflare, Akamai, PerimeterX), **browser fingerprinting**, and **high-load data extraction**.

## 🛠 Core Tech Stack
* **Browser Automation:** Playwright, Selenium, Puppeteer, Camoufox (Stealth)
* **Anti-Bot Evasion:** TLS Fingerprinting, Canvas Spoofing, Rotating Residential Proxies, Undetected-Chromedriver
* **Data & Infrastructure:** Python, SQL (MySQL/PostgreSQL), Google Sheets API, Docker
* **Architecture:** Distributed Systems, Queue Management

---

## 📂 Featured Projects

### 1. E-Commerce Inventory Scraper (Vans.com)
**Technique:** Browser Fingerprinting & Playwright
* **Challenge:** The target site uses **PerimeterX** and strict bot detection. Standard Selenium/Puppeteer scripts were immediately blocked.
* **Solution:** Implemented **Playwright** with **Camoufox** to spoof TLS fingerprints, WebRTC leaks, and Canvas hashes.
* **Result:** Successfully extracts full product inventory, pricing, and variants daily without detection.
* **File:** [`vans_inventory.py`](./vans_inventory.py)

### 2. High-Scale Retail Data Extraction (MattressFirm)
**Technique:** Cloudflare Bypass & Shadow DOM Handling
* **Challenge:** Target protected by **Cloudflare Turnstile** and heavily utilizes Shadow DOM, making standard element selection difficult.
* **Solution:** Built a scraper using `undetected-chromedriver` with custom patches. Implemented logic to traverse Shadow roots dynamically and handle "Try In-Store" geolocation logic.
* **Result:** Aggregates inventory from nationwide locations into a centralized SQL database.
* **File:** [`mattress_firm_scraper.py`](./mattress_firm_scraper.py)

### 3. Real Estate Transaction Aggregator (Zillow)
**Technique:** Distributed Scraping & Human Emulation
* **Challenge:** Zillow employs sophisticated behavioral analysis (mouse movements, scroll patterns) and IP reputation checks.
* **Solution:** Designed a distributed system with **SQL-backed job queues**. Utilized strict IP hygiene (rotating residential proxies) and randomized user-agent/header rotation.
* **Result:** Tracks sold home history and agent performance data across specific regions.
* **File:** [`zillow_listings.py`](./zillow_listings.py)

### 4. Human-Like Messaging Bot (Peerspace)
**Technique:** Behavioral Analysis & Workflow Automation
* **Challenge:** Automating host-guest communication required strictly mimicking human behavior to avoid account flagging.
* **Solution:** Created a dual-worker system (Collector & Sender) that introduces randomized delays, mouse jitter, and natural scrolling behavior using Selenium.
* **File:** [`peerspace_messenger.py`](./peerspace_messenger.py)

### 5. Financial Market Data Hub (EEX)
**Technique:** Complex DOM Navigation & Reporting
* **Challenge:** Extracting settlement prices for complex futures (Year/Quarter/Month) across multiple countries from a dynamic JS-heavy table.
* **Solution:** Automated the selection of dropdown matrixes and parsed dynamic HTML tables. Integrated directly with Google Sheets API for automated reporting.
* **File:** [`market_data_hub.py`](./market_data_hub.py)

---

## 🔒 Note on Privacy
*The code in this repository has been sanitized to remove client credentials, database connection strings, and proprietary API keys. The core logic and architecture remain intact.*
