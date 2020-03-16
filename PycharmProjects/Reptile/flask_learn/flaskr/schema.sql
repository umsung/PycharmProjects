DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  nickname VARCHAR(20),
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  click INTEGER DEFAULT 0,
  img VARCHAR,
  islike TEXT DEFAULT '0',
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  comment_time TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  comment_update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  commentator TEXT NOT NULL,
  ctitle TEXT NOT NULL,
  content TEXT NOT NULL,
  reply_content TEXT,
  cimg VARCHAR,
  islike TEXT DEFAULT '0',
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (post_id) REFERENCES post (id) 
);
