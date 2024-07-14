import boto3
import os
import random
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

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
    product_id = UnicodeAttribute(range_key = True)
    first_name = UnicodeAttribute(null = True)
    last_name = UnicodeAttribute(null = True)

def query():
    for user in UserModel.query("2", UserModel.order_id.between("20", "40")):
        # print("in query")
        print(user.first_name, user.last_name, user.order_id, user.user_id)

# for GSI CHanging Meta data
class ViewIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'product_id-user_id-index'
        projection = AllProjection
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_private_key_id = os.getenv("AWS_SECRET_KEY")

    user_id = UnicodeAttribute(range_key=True)
    product_id = UnicodeAttribute(hash_key=True)

# Making Model for GSI, uses in GSI Query 
class GSI_Query_Model(Model):
    class Meta:
        table_name = os.getenv('TABLE_NAME')
    user_id = UnicodeAttribute(range_key=True)
    product_id = UnicodeAttribute(hash_key=True)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)

def gsi_Query():
    # rangekey_condition = GSI_Query_Model.product_id.between("2000", "4000")
    for prod in GSI_Query_Model.query("2","114"):
        print(prod.first_name, prod.last_name)

def main():
    for _ in range(100):
        response = UserModel(
            user_id = random.randint(1,9).__str__(),
            product_id = random.randint(1, 100).__str__(),
            first_name = fake.first_name().__str__(),
            last_name = fake.last_name().__str__(),
        ).save()

        print(response)
        
if __name__== "__main__":
    # main()
    gsi_Query()
    # query()