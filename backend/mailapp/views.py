from rest_framework.views import APIView
from dotenv import load_dotenv
from django.http import JsonResponse
import boto3
import psycopg2
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class MailsReceivedUserGetterEndpoint(APIView):
    def get(self, request, user_mail):
        ENDPOINT = "mailapp-database-instance.c1woi26qsnpj.us-east-1.rds.amazonaws.com"
        DATABASE_ID = "mailapp-database-instance"
        PORT = 5432
        USER = "postgres"
        ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
        SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        PASSWORD = os.environ.get("AWS_DATABASE_PASSWORD")
        REGION = "us-east-1"
        DBNAME = "mail_db"

        rds_client = boto3.client(
            'rds',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=REGION,
        )

        # Get the RDS instance details
        response = rds_client.describe_db_instances(DBInstanceIdentifier=DATABASE_ID)
        rds_endpoint = response['DBInstances'][0]['Endpoint']['Address']

        # Connect to the RDS PostgreSQL database using psycopg2
        connection = psycopg2.connect(
            host=rds_endpoint,
            user=USER,
            password=PASSWORD,
            database=DBNAME,
            port=PORT
        )

        response = {}

        try:
            with connection.cursor() as cursor:
                get_tables_query = f'''
                    SELECT mail_id, sender_email, subject, sent_date FROM mail WHERE receiver_email =  '{user_mail}';
                '''
                cursor.execute(get_tables_query)

                # Fetch the results
                response = {}
                for row in cursor.fetchall():
                    mail_id, sender_email, subject, sent_date = row
                    response[str(mail_id)] = {
                        'sender_email': sender_email,
                        'subject': subject,
                        'sent_date': sent_date.strftime('%Y-%m-%d %H:%M:%S') if sent_date else None
                    }

        except Exception as e:
            # Handle exceptions appropriately
            response = {'error': str(e)}

        finally:
            # Close the database connection when done
            connection.close()

        # Return the JSON response
        return JsonResponse(response)
    
class MailsSentUserGetterEndpoint(APIView):
    def get(self, request, user_mail):
        ENDPOINT = "mailapp-database-instance.c1woi26qsnpj.us-east-1.rds.amazonaws.com"
        DATABASE_ID = "mailapp-database-instance"
        PORT = 5432
        USER = "postgres"
        ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
        SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        PASSWORD = os.environ.get("AWS_DATABASE_PASSWORD")
        REGION = "us-east-1"
        DBNAME = "mail_db"

        rds_client = boto3.client(
            'rds',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=REGION,
        )

        # Get the RDS instance details
        response = rds_client.describe_db_instances(DBInstanceIdentifier=DATABASE_ID)
        rds_endpoint = response['DBInstances'][0]['Endpoint']['Address']

        # Connect to the RDS PostgreSQL database using psycopg2
        connection = psycopg2.connect(
            host=rds_endpoint,
            user=USER,
            password=PASSWORD,
            database=DBNAME,
            port=PORT
        )

        response = {}

        try:
            with connection.cursor() as cursor:
                get_tables_query = f'''
                    SELECT mail_id, receiver_email, subject, sent_date FROM mail WHERE sender_email =  '{user_mail}';
                '''
                cursor.execute(get_tables_query)

                # Fetch the results
                response = {}
                for row in cursor.fetchall():
                    mail_id, receiver_email, subject, sent_date = row
                    response[str(mail_id)] = {
                        'receiver_email': receiver_email,
                        'subject': subject,
                        'sent_date': sent_date.strftime('%Y-%m-%d %H:%M:%S') if sent_date else None
                    }

        except Exception as e:
            # Handle exceptions appropriately
            response = {'error': str(e)}

        finally:
            # Close the database connection when done
            connection.close()

        # Return the JSON response
        return JsonResponse(response)
    
class InformationForMailGetterEndpoint(APIView):
    def get(self, request, mail_id):
        ENDPOINT = "mailapp-database-instance.c1woi26qsnpj.us-east-1.rds.amazonaws.com"
        DATABASE_ID = "mailapp-database-instance"
        PORT = 5432
        USER = "postgres"
        ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
        SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        PASSWORD = os.environ.get("AWS_DATABASE_PASSWORD")
        REGION = "us-east-1"
        DBNAME = "mail_db"

        rds_client = boto3.client(
            'rds',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=REGION,
        )

        # Get the RDS instance details
        response = rds_client.describe_db_instances(DBInstanceIdentifier=DATABASE_ID)
        rds_endpoint = response['DBInstances'][0]['Endpoint']['Address']

        # Connect to the RDS PostgreSQL database using psycopg2
        connection = psycopg2.connect(
            host=rds_endpoint,
            user=USER,
            password=PASSWORD,
            database=DBNAME,
            port=PORT
        )

        response = {}

        try:
            with connection.cursor() as cursor:
                get_tables_query = f'''
                    SELECT * FROM mail WHERE mail_id = '{mail_id}';
                '''
                cursor.execute(get_tables_query)

                # Fetch the results
                for row in cursor.fetchall():
                    mail_id, sender_email, receiver_email, subject, content, folder_id, sent_date  = row
                    response = {
                        'mail_id': mail_id,
                        'sender_email': sender_email,
                        'receiver_email': receiver_email,
                        'subject': subject,
                        'content': content,
                        'folder_id': folder_id,
                        'sent_date': sent_date.strftime('%Y-%m-%d %H:%M:%S') if sent_date else None,
                    }


        except Exception as e:
            # Handle exceptions appropriately
            response = {'error': str(e)}

        finally:
            # Close the database connection when done
            connection.close()

        # Return the JSON response
        return JsonResponse(response)
    
class SendMailPostEndpoint(APIView):
    def post(self, request):
        ENDPOINT = "mailapp-database-instance.c1woi26qsnpj.us-east-1.rds.amazonaws.com"
        DATABASE_ID = "mailapp-database-instance"
        PORT = 5432
        USER = "postgres"
        ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
        SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        PASSWORD = os.environ.get("AWS_DATABASE_PASSWORD")
        REGION = "us-east-1"
        DBNAME = "mail_db"

        rds_client = boto3.client(
            'rds',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=REGION,
        )

        # Get the RDS instance details
        response = rds_client.describe_db_instances(DBInstanceIdentifier=DATABASE_ID)
        rds_endpoint = response['DBInstances'][0]['Endpoint']['Address']

        # Connect to the RDS PostgreSQL database using psycopg2
        connection = psycopg2.connect(
            host=rds_endpoint,
            user=USER,
            password=PASSWORD,
            database=DBNAME,
            port=PORT
        )

        response = {}

        try:
            with connection.cursor() as cursor:
                sender_email = request.POST.get('sender_email')
                receiver_email = request.POST.get('receiver_email')
                subject = request.POST.get('subject')
                content = request.POST.get('content')

                insert_query = f'''
                    INSERT INTO mail (sender_email, receiver_email, subject, content)
                    VALUES ('{sender_email}', '{receiver_email}', '{subject}', '{content}');
                '''
                cursor.execute(insert_query)

                connection.commit()

                # response
                response = {'message': 'Mail sent successfully'}

        except Exception as e:
            # Handle exceptions appropriately
            response = {'error': str(e)}

        finally:
            # Close the database connection when done
            connection.close()

        # Return the JSON response
        return JsonResponse(response)