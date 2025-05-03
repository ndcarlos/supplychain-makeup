# 📦 Supply Chain Analysis: Inventory Optimization & Demand Forecasting

This folder contains Python scripts and models created to optimize inventory levels and forecast demand for a Fashion & Beauty startup.

Using data from [this Kaggle dataset](https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis) I worked through several stages:
* Inventory health checks
* Demand forecasting (with synthetic data generation)
* Replenishment planning
* Bottleneck and supplier analysis (in progress)

## Table of Contents

*   🙋 [Project Overview](#project-overview)
*   📝 [Scripts](#scripts)

*   🌐 [Global Dependencies](#global-dependencies)
   *   📚 [Libraries](#libraries)
*   ⏬ [Install](#install)
*   🔮 [Future plans](#future-plans)
*   🤝 [Contribute](#contribute)
*   ©️ [License](#license)
*   🔌 [Sources](#sources)

## 🙋 Project Overview
This repository aims to showcase real-world supply chain analytics workflows, including:

* 📦 **Inventory Optimization**: Analyzing stock imbalances, calculating ideal stock levels, and optimizing reorder points to minimize carrying costs.
* 🔮 **Demand Forecasting**: Generating synthetic data to model annual demand trends and predict future stock needs more accurately.
* 🔁 **Replenishment Planning**: Creating SKU-level reorder plans that account for lead times, demand variability, and service level targets.
* 🔍 **Key goal**: Demonstrate how data-driven inventory strategies can help businesses reduce stockouts, avoid overstocking, and improve fulfillment efficiency.

## 📝 Scripts
  * ```inventory_optimization.py```: Analyzes stock levels, and highlights overstocked and understocked SKUs.
  * ```demand_forecasting.py```: Generates synthetic demand data and forecasts future stock needs.
  * ```replenishment_plan.py```: Calculates reorder points (ROP) and recommended reorder quantities.
  * ```synthetic_data_generation.py```: Generates a year-long synthetic dataset to support demand forecasting and inventory analysis.
  * ```bottleneck_analysis.py```: *(Planned)* Will analyze process bottlenecks causing supply delays.
  * ```supplier_analysis.py```: *(Planned)* Will assess supplier performance and lead times.

## 🌐 Global dependencies
_Note: local dependencies for each script are specified in the script headers_
  * ### 📚 Libraries
    This project uses the following core Python libraries:
      * ```pandas```
      * ```numpy```
      * ```matplotlib```
      * ```seaborn```
      * ```scikit-learn``` (for synthetic data generation and modeling)

Make sure to install them using the provided requirements file or individually.

## ⏬ Install
Clone this repository to your local machine:

```bash
git clone https://github.com/ndcarlos/supplychain-makeup
cd supplychain-makeup
```

Install dependencies using ```pip```:

``` pip install -r requirements.txt ```


## 🔮 Future Plans

## 🤝 Contribute
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## ©️ License
[MIT](https://choosealicense.com/licenses/mit/)

## 🔌 Sources

[react-markdown][react-markdown] - Project which served as an inspiration for this README

[Blog post templates][blog-post-templates] - Used to structure this template as an easy-to-read blog post

[About markdown][about-markdown] - Why should you use markdown?

[Markdown Cheat Sheet][markdown-cheatsheet] - Get a fast overview of the syntax

[//]: # "Source definitions"
[blog-post-templates]: https://backlinko.com/hub/content/blog-post-templates "Backlinko blog post templates"
[about-markdown]: https://www.markdownguide.org/getting-started/ "Introduction to markdown"
[markdown-cheatsheet]: https://www.markdownguide.org/cheat-sheet/ "Markdown Cheat Sheet"

>>>>>>> d46ed75aff37d176b88889cda74f9a5aaf22aab5
