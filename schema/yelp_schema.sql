DROP TABLE IF EXISTS Business CASCADE;
DROP TABLE IF EXISTS Yelp_User CASCADE;
DROP TABLE IF EXISTS Reviews CASCADE;
DROP TABLE IF EXISTS Tips CASCADE;
DROP TABLE IF EXISTS Checkins CASCADE;
DROP TABLE IF EXISTS Media CASCADE;
DROP TABLE IF EXISTS Friend_Of CASCADE;

CREATE TABLE IF NOT EXISTS Business (
    business_id VARCHAR(128),
    name VARCHAR(128),
    address VARCHAR(128),
    city VARCHAR(128),
    state VARCHAR(128),
    postal_code VARCHAR(20),
    review_count INTEGER,
    categories_list TEXT,
    avg_stars REAL,
    to_go BOOLEAN,
    wifi BOOLEAN,
    ambience TEXT,
    parking BOOLEAN,
    price_range INTEGER,
    open_hours TEXT,
    PRIMARY KEY (business_id),
    CHECK (NOT (avg_stars < 0 OR avg_stars > 5)),
    CHECK (review_count >= 0)
);

CREATE TABLE IF NOT EXISTS Yelp_User(
    user_id VARCHAR(128),
    name VARCHAR(128),
    registration_date DATE,
    fans INTEGER,
    avg_stars REAL,
    review_count INTEGER,
    PRIMARY KEY (user_id),
    CHECK (NOT (avg_stars < 0 OR avg_stars > 5)),
    CHECK (review_count >= 0)
);

CREATE TABLE IF NOT EXISTS Reviews (
    review_id VARCHAR(128),
    --review_id SERIAL, -- change to serial for auto-increment
    business_id VARCHAR(128) NOT NULL, -- Reviews must be for a business
    user_id VARCHAR(128) NOT NULL, -- Reviews must be written by a user
    review_date DATE,
    stars INTEGER, -- Note star rating is an integer here but not avg_stars.
    review_text TEXT,
    useful_count INTEGER,
    PRIMARY KEY (review_id),
    FOREIGN KEY (business_id)
        REFERENCES Business
            ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES Yelp_User
            ON DELETE CASCADE,
    CHECK (NOT (stars < 0 OR stars > 5)),
    CHECK (useful_count >= 0),
    CHECK (review_date <= NOW())
);

CREATE TABLE IF NOT EXISTS Tips (
    business_id VARCHAR(128) NOT NULL, -- Tips must be for a business
    user_id VARCHAR(128) NOT NULL, -- Tips must be given by a user
    compliment_count INTEGER,
    tip_date DATE,
    tip_text TEXT,
    --PRIMARY KEY (business_id, user_id), -- update
    FOREIGN KEY (business_id)
        REFERENCES Business
            ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES Yelp_User
            ON DELETE CASCADE,
    CHECK (compliment_count >= 0),
    CHECK (tip_date <= NOW())
);

CREATE TABLE IF NOT EXISTS Checkins (
    business_id VARCHAR(128) NOT NULL, -- update
    checkin_date DATE NOT NULL, -- update
    FOREIGN KEY (business_id)
        REFERENCES Business
            ON DELETE CASCADE,
    CHECK (checkin_date <= NOW())
);

CREATE TABLE IF NOT EXISTS Media (
    photo_id VARCHAR(128),
    business_id VARCHAR(128),
    blob_data BYTEA,
    caption TEXT,
    PRIMARY KEY (photo_id), -- update
    FOREIGN KEY (business_id)
        REFERENCES Business
            ON DELETE CASCADE
);

-- Design Considerations:
-- user_one_id is a friend of user_two_id implies that user_two_id is a friend of user_two_id.
CREATE TABLE IF NOT EXISTS Friend_Of (
    friendship_id SERIAL, -- Enforce friendship uniqueness when doing INSERT.
    user_one_id VARCHAR(128) NOT NULL, -- update
    user_two_id VARCHAR(128) NOT NULL, -- update
    PRIMARY KEY (friendship_id),
    FOREIGN KEY (user_one_id)
        REFERENCES Yelp_User
            ON DELETE CASCADE,
    FOREIGN KEY (user_two_id)
        REFERENCES Yelp_User
            ON DELETE CASCADE,
    CHECK (NOT(user_one_id = user_two_id))
);
