from tika import parser
import csv
import os
import requests

#test the working of tika:

# # Provide the file path
# file_path = 'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document?$top=1'
# # Extract content
# parsed_data = parser.from_file(file_path)
# text_content = parsed_data['content']
# print(text_content)


# URL path
url_path = 'https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document({})'

# CSV file path
csv_file_path = '/Users/ekaterinamazur/PycharmProjects/tk_topics/api_documents.csv'

# Output directory path
output_dir = '/Users/ekaterinamazur/PycharmProjects/tk_topics'

# Limit the number of documents to retrieve, adjust the number if needed
limit = 100

# Read the CSV file and extract IDs
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    next(csv_reader)  # Skip header if present
    count = 0  # Counter for limiting the number of documents

    for row in csv_reader:
        if count >= limit:
            break

        document_id = row['Id']

        # Construct the document URL
        document_url = url_path.format(document_id)

        # Send a GET request to the document URL
        response = requests.get(document_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the text content using Apache Tika
            parsed_data = parser.from_buffer(response.content)
            text_content = parsed_data['content']

            # Create a file with the document ID as the filename
            output_file_path = os.path.join(output_dir, f'{document_id}.txt')

            # Save the text content to the file
            with open(output_file_path, 'w') as output_file:
                output_file.write(text_content)

            count += 1
            print(f"Document {document_id} saved.")

        else:
            print(f"Failed to retrieve document {document_id}.")

print("Extraction complete.")
