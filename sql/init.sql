create database backend;
use backend;

drop table if exists post;
create table post(
	id varchar(256),
	created_at timestamp,
	description varchar(256),
	addr_1 varchar(256),
	addr_2 varchar(256),
	city varchar(256),
	state varchar(256),
	zip varchar(256),
	status_id varchar(256),
	image_uri varchar(256)
);

drop table if exists status;
create table status(
	id smallint,
	name varchar(256),
);

drop table if exists certifications;
create table certifications(
	id varchar(256),
	post_id varchar(256),
	certified_at timestamp,
	certifier_name varchar(256)
);

INSERT INTO status (id, name)
VALUES
    (1, 'POSTED'),
    (2, 'RECEIVED'),
    (3, 'CERTIFIED');

INSERT INTO post (id, created_at, description, addr_1, addr_2, city, state, zip, status_id, image_uri)
VALUES
('cd4fae52-ada9-499c-874b-de22d44733e1', NOW(), 'bricks and paint', '6701 Hiatus Rd', NULL, 'Tamarac', 'FL', '33321', 1, 'gs://hackathon-h4h-imgpub/bricks-paint.jpeg')
