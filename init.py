import sqlite3
import discord

def init():
  sql = """ CREATE TABLE IF NOT EXISTS link (
                                          id integer PRIMARY KEY,
                                          user_id integer,
                                          username text
                                      ); """

  conn = sqlite3.connect("main.db")         
  c = conn.cursor()             

  c.execute(sql)
  conn.commit()
