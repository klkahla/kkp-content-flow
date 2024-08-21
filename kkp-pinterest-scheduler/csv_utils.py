import csv

def read_csv_file(csv_file_path):
    pins = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            pins.append(row)
    return pins

def write_csv_output(scheduled_pins, selected_board_name, output_file_path):
    headers = ["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for pin in scheduled_pins:
            media_url = f"https://kkp-pinterest-scheduler.s3.us-west-2.amazonaws.com/{pin['file_name']}"
            pin['media_url'] = media_url
            writer.writerow({
                "Title": pin['pin_title'],
                "Media URL": pin['media_url'],
                "Pinterest board": selected_board_name,
                "Thumbnail": "", 
                "Description": pin['description'],
                "Link": pin['link'],
                "Publish date": pin['scheduled_time'],
                "Keywords": "idaho, wedding, elegant, luxury, garden theme, european inspired"
            })