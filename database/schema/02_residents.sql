CREATE TABLE residents (
    resident_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(15),
    apartment_id INTEGER NOT NULL REFERENCES apartments(apartment_id)
);
