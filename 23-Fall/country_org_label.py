import pandas as pd
import os
# label method to encode category features. This is the example of organizations.
# input root and list of csv files, save mapped file (org name - mapped number)
# exclude "private network" and "-", remain valid org name
def category_label(root, filename):
    all_org = []
    for f in filename:
        f = os.path.join(root, f)
        df = pd.read_csv(f, low_memory=False)
        if 'dstIPOrg' in df.columns:
            unique_org = df['dstIPOrg'].unique()
            all_org.extend(unique_org)
            # print(num_unique_countries)
    all_unique_org = list(set(all_org))
    valid_org = [org for org in all_unique_org if
                 org not in ('"Private network"', '"-"') and not any(char.isdigit() for char in org)]
    org_to_number = {org: i + 1 for i, org in enumerate(valid_org)}
    print(org_to_number)
    org_df = pd.DataFrame(list(org_to_number.items()), columns=['Org', 'Number'])
    org_list = list(org_to_number.items())

    # Write to CSV
    org_df.to_csv('IPOrg_to_number.csv', index=False)

def get_file(file_path):
    roots = []
    csv_file = []
    files = []
    for root, dirs, file in os.walk(file_path, topdown=False):
        files.append(file)
        filename = [f for f in file if (f.split('.')[-1]) == 'csv']
        csv_file.append(filename)
        roots.append(root)
    csv_file.remove([])
    roots.pop(-1)
    return roots, dirs, csv_file


# open UNSW dir ./UNSW/UNSW/01.pcap, 02.pcap...
root, dir, filename = get_file("UNSW")
root = str(root[0])
filename = filename[0]

# Read the CSV file
country_df = pd.read_csv('IPCC_to_number.csv', dtype={'Number': int})
org_df = pd.read_csv('IPOrg_to_number.csv', dtype={'Number': int})
# Convert DataFrame back to dictionary
country_list = country_df.set_index(['Country'])['Number'].to_dict()
org_list = org_df.set_index(['Org'])['Number'].to_dict()


for f in filename:
    newf = f
    f = os.path.join(root, f)
    df = pd.read_csv(f, low_memory=False)

    ##### map country geolocation
    df['IpCountry'] = df.apply(lambda row: row['dstIPCC'] if row['%dir'] == 'A' else row['srcIPCC'], axis=1)
    df['map_IpCountry'] = df['IpCountry'].map(country_list)
    # if no map, label as 0 (already filter, only remain DNS and DHCP)
    df['map_IpCountry'] = df['map_IpCountry'].fillna(0)
    df = df[~df['map_IpCountry'].isna()]

    ####### map ISP
    df['IpOrg'] = df.apply(lambda row: row['dstIPOrg'] if row['%dir'] == 'A' else row['srcIPOrg'], axis=1)
    df['map_IpOrg'] = df['IpOrg'].map(org_list)
    df['map_IpOrg'] = df['map_IpOrg'].fillna(0)


    ##### save
    df.to_csv('processunsw/new_filtered1204/' + newf)


