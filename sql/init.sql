create database backend;

create table post(
	id varchar(256),
	created_at datetime,
	status_id varchar(256),
	items_oid varchar(256),
	image_uri varchar(256)
);

create table status(
	id varchar(256),
	name varchar(256),
	posted datetime,
	received datetime,
	certified boolean
);

create table certifications(
	id varchar(256),
	post_id varchar(256),
	certified_at datetime,
	certifier_name varchar(256)
);
