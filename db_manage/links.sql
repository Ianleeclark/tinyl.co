CREATE TABLE IF NOT EXISTS links (
    url     text primary key,
    enc	    text,
    fullenc text
);

INSERT INTO links(url, enc, fullenc) VALUES('http://google.com/', '1', '1');
INSERT INTO links(url, enc, fullenc) VALUES('http://facebook.com/', '2', '2');
