CREATE TABLE UserPosts (
    usertag VARCHAR(255),
    date_time DATETIME,
    post TEXT,
    label VARCHAR(50),
    PRIMARY KEY (usertag,date_time)
);
