# Fall 2023

Folder for all 2023 projects.

# Intrdoction
Internet of Things (IoT) devices have been widely implemented across different environments,
such as smart homes, smart cities, and various business networks. Examples of IoT devices include
smart speakers like Amazon Echo Dot, smart cameras, and smart light bulbs. They significantly
enhance our daily lives and communities by boosting convenience, efficiency, and quality.
Although IoT devices only provide limited functions and communicate with a finite number of
endpoints, they present numerous challenges in terms of security management due to the vast
range of manufacturers and operating modes, along with their low cost, resulting in vulnerable
firmware. This project aims to develop a security gateway to identify IoT devices within a network
using traffic data and Internet Protocol (IP) utilities, enabling the gateway to recognize each device
and retrieve their corresponding Manufacturer Usage Descriptions (MUD) profiles.

# Processing Overview
Initially, we gathered and examined data from IoT devices in the Internet Real-Time (IRT) Lab
to understand their traffic patterns. Following this, we processed PCAP files from a public dataset,
created flow files using Tranalyzer, and conducted necessary data cleaning to eliminate irrelevant
traffic. Our initial approach was to utilize numerical flow-level features for device identification.
However, after an in-depth analysis of IoT device traffic behaviors, we incorporated non-numerical,
protocol-based features, a method we believe to be a novel approach in our research group. We
then repeatedly tested the effectiveness of each feature to create a final feature vector. Ultimately,
we trained several machine learning models using this feature vector and evaluated our model’s
performance on both the original and additional datasets.
# File Structure

1. data.py -flow generation
2. Data Preprocessing.ipynb -data cleaning
3. label.py -data labelling for UNSW datset
4. feature_selection.py -feature selection methods
5. feature encoding.py -feature encoding methods
6. country_org_label.py -encoding IP country and IP organization
7. IPCC_to_number.csv -encoded IP country
8. IPOrg_to_number.csv -encoded IP organization
9. model.py -Machine Learning models
10. Aalto.py -test on Aalto dataset
11. unsw.py  -test on UNSW dataset
12. Dataset -public datasets and real data we collected

