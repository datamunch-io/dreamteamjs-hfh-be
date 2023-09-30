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

INSERT INTO post (id, created_at, description, addr_1, addr_2, city, state, zip, status_id, image_uri)
VALUES
('4384998e-2b92-49dd-8803-99f0a020b497', NOW(), 'an entire house full of wooden planks', '123 Fake St', NULL, 'Miami', 'FL', 33156, 2, 'gs://hackathon-h4h-imgpub/lots-o-lumber.jpeg')

INSERT INTO post (id, created_at, description, addr_1, addr_2, city, state, zip, status_id, image_uri)
VALUES
('28c39a6e-b31d-460f-a0fd-527176d63398', NOW(), 'several piles of wooden planks', '456 False Ave', NULL, 'Miami', 'FL', 32359, 2, 'gs://hackathon-h4h-imgpub/lumber.jpeg')

INSERT INTO post (id, created_at, description, addr_1, addr_2, city, state, zip, status_id, image_uri)
VALUES
('4c0db792-7bd6-443e-8a06-c22f2aac9750', NOW(), 'a series of assorted metal pipes and rods', '1205 Thompson Road', 'Tallahassee', 'FL', 32301, 3, 'gs://hackathon-h4h-imgpub/metals.jpeg')

INSERT INTO post (id, created_at, description, addr_1, addr_2, city, state, zip, status_id, image_uri)
VALUES
('44cc4684-2b1a-45ee-ab1c-aff391d375ec', NOW(), 'at least 100 steel beams', '789 Johnson Road', 'Tamarac', 'FL', 33321, 3, 'gs://hackathon-h4h-imgpub/steel-beams.jpeg')

INSERT INTO post (id, created_at, description, addr_1, addr_2, city, state, zip, status_id, image_uri)
VALUES
('73ec31a8-0ab8-44c6-8db5-02b7a649adc0', NOW(), 'a collection of rusty-looking metal pipes', '9572 123rd St', 'FL', 33149, 1, 'gs://hackathon-h4h-imgpub/tubing.jpeg')

INSERT INTO certifications (id, post_id, certified_at, certifier_name)
VALUES
('1a32b1d2-045b-4dc7-ac8a-6cccb3e87dd6', '4c0db792-7bd6-443e-8a06-c22f2aac9750', NOW(), 'Alice')

INSERT INTO certifications (id, post_id, certified_at, certifier_name)
VALUES
('90519a08-3651-40c2-9e6a-275021ee3025', '44cc4684-2b1a-45ee-ab1c-aff391d375ec', NOW(), 'Bob')
