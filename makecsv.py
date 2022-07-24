import csv

headers = ['ASIN', 'Price', 'Title', 'Stars', 'Ratings', 'Manufacturer', 'Link', 'Description', 'Features']


def make_csv(data, file_name="test"):
    try:
        with open('./{}.csv'.format(file_name), 'w', newline='', encoding='utf-8') as cvs:
            writer = csv.writer(cvs)
            writer.writerow(headers)
            for item in data:
                item_data = [
                    item['asin'], item['price'], item['title'], item['stars'], item['ratings'], item['manufacturer'],
                    item['link'], item['description'], ','.join(item['features'])
                ]
                writer.writerow(item_data)
    except:
        return "Error while making CSV file"
    return "{}.csv has been made successfully".format(file_name)


if __name__ == '__main__':
    print("Import this file")
