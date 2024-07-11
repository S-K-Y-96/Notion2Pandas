import os

from dotenv import load_dotenv
from notion_client import Client

from src.burp import BurpConfig
from src.notion_type_handler import notion_to_pandas, NotionTypeHandler

load_dotenv()

if __name__ == "__main__":
    
    NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
    BURP_PATH = os.getenv("BURP_PATH")
    with BurpConfig(BURP_PATH) as burp:
        notion = Client(auth=NOTION_API_TOKEN)
        database_id = input("Enter the database id: ").strip()
        filename = input("Enter your desired output filename: ").strip()
        response = notion.databases.query(database_id)
        filename = response["request_id"] if not filename else filename
        db = response["results"]
        df = notion_to_pandas(db)
        df = NotionTypeHandler.convert_dataframe(df)
        df.to_csv(f"{filename}.csv", index=False)
        print(df)