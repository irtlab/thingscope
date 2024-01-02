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
'''
│  Aalto.py
│  Aalto_filename.pkl
│  country_org_label.py
│  Data Preprocessing.ipynb
│  data.py
│  feature encoding.py
│  feature_selection.py
│  IPCC_to_number.csv
│  IPOrg_to_number.csv
│  label.py
│  list.txt
│  model.py
│  README.md
│  UNSW List_Of_Devices.xlsx
│  UNSW_device.pkl
│  
└─Aalto
'''
