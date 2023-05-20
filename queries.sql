CREATE TABLE employers
(
	employer_id varchar PRIMARY KEY,
	employer_name varchar,
	url varchar,
	description varchar
);
CREATE TABLE vacancies
(
	employer_id varchar,
	id_vacancy varchar PRIMARY KEY,
	vacancies_name varchar,
	vacancies_url varchar,
	salary int,
	requirement text,
	responsibility text
);
ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employer_id FOREIGN KEY(employer_id) REFERENCES employers(employer_id);


SELECT * FROM vacancies
SELECT * FROM employers
DELETE FROM vacancies;
DELETE FROM employers;