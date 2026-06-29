-- Create channels table
CREATE TABLE IF NOT EXISTS channels (

    id SERIAL PRIMARY KEY,

    channel_name VARCHAR(255) UNIQUE NOT NULL
);


-- Create messages table

CREATE TABLE IF NOT EXISTS messages (

    id SERIAL PRIMARY KEY,

    message_id BIGINT,

    channel_id INTEGER,

    message_text TEXT,

    message_date TIMESTAMP,

    views INTEGER,

    forwards INTEGER,

    has_media BOOLEAN,

    image_path TEXT,

    FOREIGN KEY (channel_id)
        REFERENCES channels(id)
);