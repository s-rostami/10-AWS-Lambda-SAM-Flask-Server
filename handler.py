# 1) Install pymysql to local directory as below:
#   pip install -t $PWD pymysql
import pymysql
import sys
import logging
import json

# configuration values
host = 'ntier.cvvkrojoestg.us-east-1.rds.amazonaws.com'
username = 'admin'
password1 = 'password'
database_name = 'ntier'
print('## ENVIRONMENT VARIABLES')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# connections
try:
    connection = pymysql.connect(
        host, user=username, passwd=password1, db=database_name, connect_timeout=30)
except pymysql.MySQLError as e:
    logger.error('error: could not connect')
    logger.error(e)
    sys.exit()


def lambda_handler(event, context):
    print("hi there", event)
    event_body = json.loads(event['body'])
    name1 = event_body['Name']
    email1 = event_body['Email']
    # name1=event["name"]
    # email1=event["email"]
    print(name1, email1)
    item_count = 0
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO user(name, email) VALUES(%s, %s)", (name1, email1))
    connection.commit()
    cur.execute("SELECT * FROM user")
    for row in cur:
        item_count += 1
        logger.info(row)
        print(row)
    connection.commit()
    cur.close()
    return {
        'statusCode': '200',
        'body': json.dumps({
            'Name and email was added': name1,
            'total items from RDS MySQL USER table': item_count
        }),
        'headers': {}

    }
