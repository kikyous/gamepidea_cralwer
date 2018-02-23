import os
import sqlite3

class GamepediaScrapyPipeline(object):
    collection_name = 'scrapy_items'

    def open_spider(self, spider):
        self.conn = sqlite3.connect('example.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS items
                     (id integer PRIMARY KEY,
                     name text NOT NULL UNIQUE, en_name text, content text)''')


    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute(
                "INSERT OR IGNORE INTO items (name) VALUES (?)", (item['name'],)
        )
        self.c.execute(
                "UPDATE items set en_name = ?, content = ? where name = ?",
                (item['en_name'], item['content'], item['name'])
        )
        return item
