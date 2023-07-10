import csv
import os
import requests
from tika import parser
import time

# URL path
url_path = 'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document({})/Resource' #change the path to the one you need

# CSV file path
csv_file_path = '/Users/ekaterinamazur/PycharmProjects/tk_topics/api_documents.csv'  #change the path to the one you need

# Output CSV file path
output_csv_path = '/Users/ekaterinamazur/PycharmProjects/tk_topics/50000.csv' #!!put the name of the file you want to save!!!

# Limit the number of documents to retrieve or make boundaries (code for that at the end)
limit = 50000

# Delay between requests (in seconds)
request_delay = 0.01  # Adjust as needed, better remove delay , otherwise it will take ages

# Maximum number of retries for failed requests , better not to retry, most of retries fail because of the 404 error
max_retries = 5

# Read the CSV file and extract IDs
document_ids = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    count = 0  # Counter for limiting the number of documents

    for row in csv_reader:
        if count >= limit:
            break

        document_id = row['Id']  # Modify the column name if necessary
        document_ids.append(document_id)

        count += 1

# Fetch document contents and build CSV data
csv_data = []
for i, document_id in enumerate(document_ids, start=1):
    # Retry failed requests up to max_retries times
    for attempt in range(max_retries):
        try:
            # Construct the document URL
            document_url = url_path.format(document_id)

            # Send a GET request to the document URL
            response = requests.get(document_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the text content using Apache Tika
                parsed_data = parser.from_buffer(response.content)
                text_content = parsed_data['content']

                csv_data.append({'Id': document_id, 'Content': text_content})

                # Log a message for every 5000 documents written
                if i % 2500 == 0:
                    print(f"{i} documents written.")

                # Write CSV data to the output file after each successful iteration
                with open(output_csv_path, 'w', newline='') as output_csv_file:
                    fieldnames = ['Id', 'Content']
                    writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)

                    writer.writeheader()
                    writer.writerows(csv_data)

                break  # Break out of the retry loop if successful

            else:
                raise Exception(f"Failed to retrieve document {document_id}. Error code: {response.status_code}")

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retrying document {document_id} ({attempt + 1}/{max_retries})...")
                time.sleep(request_delay)
            else:
                print(f"Failed to retrieve document {document_id} after {max_retries} attempts. Error: {str(e)}")
                break  # Move on to the next document

    # Add a delay between requests
    time.sleep(request_delay)

# Write CSV data to the output file
with open(output_csv_path, 'w', newline='') as output_csv_file:
    fieldnames = ['Id', 'Content']
    writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(csv_data)

print("Extraction complete. Data saved to CSV file.")


