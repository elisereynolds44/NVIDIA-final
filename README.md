# NVIDIA vs The Market: A Performance Deep Dive

This is my final course project for CS-150, built using Dash by Plotly. The project
explores the performance of NVIDIA compared to major market indices and its closest competitors in
the tech sector. 

# Project Summary 

This interactive dashboard answers the question: 

**Is NVIDIA simply riding the tech wave - or is it driving the market itself?**

By analyzing stock performance, correlations, and earnings-related spikes, this dashboard investigates 
NVIDIA's influence on broader market trends using real (and sometimes simulated) data. 

# What is in the Dashboard 

**Data**
This folder contains all datasets and supporting files used by the Dash app. These files either feed into the 
visualizations or support features like dropdown filters and earnings highlights. 
    
    Contents:   
    - NVDA-2023.csv, NVDA-2024.csv - NVIDIA stock prices
    - AMD-2023.csv, AMD-2024.csv - AMD stock prices
    - INTC-2023.csv, INTC-2024.csv - Intel stock prices
    - MSFT-2023.csv, MSFT-2024.csv - Microsoft stock prices
    - DELL-2023.csv, DELL-2024.csv - Dell stock prices
    - HPE-2023.csv, HPE-2024.csv - Hewlett Packard Enterprise stock prices
    - SMCI-2023.csv, SMCI-2024.csv - SuperMicro stock prices
    - SPY-2023.csv, SPY-2024.csv - S&P 500 EFT
    - QQQ-2023.csv, QQQ-2024.csv - NASDAQ-100 ETF
    - combine-data.py - a helper scrpit that merges all the individual stock CSVs into one combined dataset. 
        This makes it easier to analyze multiple stocks together and feed into interactive charts. 
    - time_series_backup.csv - a pre-processed version of the combined dataset, where stock prices are already 
        normalized for quick loading and visulation in the "Price Trends" tab of the dashboard. 

ALL from yahoofinance 

**Visuals** - Chart & Graph Generation
This folder contains the custom visualization functions used to run the interactive graphs in the dashboard. Each chart 
dynamically responds to user input, helping illustrate key stock performance trends & relationships. 

Files included: 
- time_series.py: generates a multi-line time series chart showing normalized stock growth over time. 
  - Purpose: Visualize how selected companies (like NVIDIA, AMD, ect.) have grown relative to each other, starting at the same
    baseline (100)
  - Features:
    - Normalizes prices to show percentage-based growth
    - allows filtering by company and date range
    - annotate NVIDIA earnings dates with vertical dashed lines and tooltips 
- correlation_heatmap.py: renders a heatmap to show how closely the selected stock prices move together. 
  - Purpose: explore correlation patterns across companies and indices from 2023-2024
  - Features:
    - Heatmap 
    - Values range from 0 to 1 (perfect correlation)
    - highlights how NVIDIA tracks w (or diverges from) market benchmarks 

**Other Important Files:**
- app.py = main entry point for the Dash application. 
- tabs.py = organized the layout & structure of the dashboard into seperate tabs. Each tab corresponds to a different part of the 
user experience
- callbacks.py = interactive logic 