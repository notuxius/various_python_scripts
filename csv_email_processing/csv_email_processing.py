import csv


emails_2016 = []

emails_best = []

allemails = []

with open('export_customers_2016.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    # emails = [email.split() for email in csvreader]

    # print(emails)



    iteremails = iter(csvreader)
    next(iteremails)

    for email in csvreader:
        # email = email.split(',')
        # print(email)
        emails_2016.append(email[1] + ' ' +  email[2] + ' - ' +  email[3])

    # print(emails)

with open('export_customers_best.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')


    iteremails = iter(csvreader)
    next(iteremails)

    for email in csvreader:
        # email = email.split(',')
        # print(email)
        emails_best.append(email[1] + ' ' +  email[2] + ' - ' +  email[3])

    # print(emails2)

for email in emails_best:
    if email not in emails_2016:
        allemails.append(email)
        print(email)
    else:
        print('DUPLICATE', email)

seen_lines = []
for email in allemails:
    if email in seen_lines:
        print('ALREADY SEEN', email)
    else:
        print(email)
        seen_lines.append(email)

seen_lines.sort()

with open('unique_emails.txt', 'w') as unique_emails_file:
    for line in seen_lines:
        unique_emails_file.write(str(line) + '\n')