create table customers{
	id SERIAL PRIMARY KEY,
	name VARCHAR(64) NOT NULL,
	mail VARCHAR(127) UNIQUE NOT NULL,
	password VARCHAR(256) NOT NULL,
	created_at TIMESTAMP,
	updated_at TIMESTAMP
}
