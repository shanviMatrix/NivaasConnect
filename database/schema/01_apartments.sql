CREATE TABLE apartments (
    apartment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    building_name VARCHAR(100) NOT NULL,
    flat_number VARCHAR(20) NOT NULL,
    floor_number INTEGER CHECK (floor_number >= 0),
    UNIQUE (building_name, flat_number)
);
