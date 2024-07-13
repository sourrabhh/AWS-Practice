import boto3
import os
import random
from pynamodb.models import Model
from pynamodb.attributes import *
from dotenv import load_dotenv
load_dotenv()

from faker import Faker

fake =Faker()  # Fake Data Library

dynamodb = boto3.client('dynamodb')

class UserModel(Model):
    class Meta:
        table_name = os.getenv('TABLE_NAME')
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_private_key_id = os.getenv("AWS_SECRET_KEY")
    
    user_id = UnicodeAttribute(hash_key = True)
    order_id = UnicodeAttribute(range_key = True)
    first_name = UnicodeAttribute(null = True)
    last_name = UnicodeAttribute(null = True)

def main():

    print(f"Table {os.getenv('AWS_ACCESS_KEY')}")
    for i in range(100):
        response = UserModel(
            user_id = random.randint(1,8).__str__(),
            order_id = random.randint(10, 1000).__str__(),
            first_name = fake.first_name().__str__(),
            last_name = fake.last_name().__str__(),
        ).save()

        print(response)
        
if __name__== "__main__":
    main()
    