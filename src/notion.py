from notion_client import Client


class Notion:
    def __init__(self, token_v2):
        self.client = Client(auth=token_v2)

    def get_database(self, database_id):
        return self.client.databases.retrieve(database_id)

    def get_database_entries(self, database_id):
        return self.client.databases.query(database_id)

    def get_page(self, page_id):
        return self.client.pages.retrieve(page_id)

    def create_page(self, parent, properties):
        return self.client.pages.create(parent=parent, properties=properties)

    def update_page(self, page_id, properties):
        return self.client.pages.update(page_id, properties=properties)

    def delete_page(self, page_id):
        return self.client.pages.update(page_id, archived=True)