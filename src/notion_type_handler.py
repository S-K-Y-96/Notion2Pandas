import os
import json
import pandas as pd 

class NotionTypeHandler:

    @staticmethod
    def title(series):
        return series.apply(lambda x: x["title"][0]['text']['content'] if x["title"] else "Untitled")
    @staticmethod
    def checkbox(series):
        return series.apply(lambda x: x["checkbox"])
    @staticmethod
    def number(series):
        return series.apply(lambda x: x["number"])
    def formula(series):
        TYPE = series[0]["formula"]['type']
        return series.apply(lambda x: x["formula"][TYPE])
    @staticmethod
    def status(series):
        return series.apply(lambda x: x["status"]['name'])
    @staticmethod
    def date(series):
        return series.apply(lambda x: x["date"]['start'][:10] if x["date"] else "")
    @staticmethod
    def select(series):
        return series.apply(lambda x: x["select"]["name"] if x["select"] else "")
    @staticmethod
    def multi_select(series):
        def join_multi_select(x):
            res = ""
            for item in x["multi_select"]:
                res += item["name"] + ", "
            return res[:-2]
        return series.apply(join_multi_select)
    @staticmethod
    def rich_text(series):
        def join_plain_text(x):
            res = ""
            for item in x["rich_text"]:
                res += item["plain_text"]
            return res
        return series.apply(join_plain_text)
    @staticmethod
    def people(series):
        def join_people(x):
            res = ""
            for item in x["people"]:
                res += item["id"][:8] + "..., "
            return res[:-2]
        return series.apply(join_people)

    @staticmethod
    def convert_series(series):
        TYPE = series[0]['type']
        match TYPE:
            case "title":
                series = NotionTypeHandler.title(series)
            case "checkbox":  # | "number":
                series = NotionTypeHandler.checkbox(series)
            case "number":
                series = NotionTypeHandler.number(series)
            case "formula":
                series = NotionTypeHandler.formula(series)
            case "date":
                series = NotionTypeHandler.date(series)
            case "status":
                series = NotionTypeHandler.status(series)
            case "select":
                series = NotionTypeHandler.select(series)        
            case "multi_select":
                series = NotionTypeHandler.multi_select(series)
            case "rich_text":
                series = NotionTypeHandler.rich_text(series)
            case "people":
                series = NotionTypeHandler.people(series)
            case _:
                return None
        return series

    @staticmethod
    def convert_dataframe(df, column_list=None):
        if not column_list:
            column_list = df.columns
        new_columns = []
        for column in column_list:
            series = df[column]
            new_series = NotionTypeHandler.convert_series(series)
            if isinstance(new_series, pd.Series):
                new_columns.append(new_series)
                    
        new_df = pd.concat(new_columns, axis=1)
        return new_df


def notion_to_pandas(notion_results):
    with open('./result.json', 'w', encoding='utf8') as f:
        json.dump(notion_results, f, ensure_ascii=False)

    df = pd.read_json('./result.json')
    df.properties.to_json('./result.json', orient='records', force_ascii=False)
    df = pd.read_json('./result.json')

    os.remove('./result.json')
    return df


# from notion_client import Client

# notion = Client(auth="...")
# db = notion.databases.query(database_id="...")["results"]
# df = notion_to_pandas(db)
# df = NotionTypeHandler.convert_dataframe(df)
# df.to_csv(path, index=False)
# df