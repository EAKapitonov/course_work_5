CREATE DATABASE headhunter;

CREATE TABLE employers
ALTER TABLE employers ADD COLUMN employer_id varchar;
ALTER TABLE employers ADD COLUMN employer_name varchar;
ALTER TABLE employers ADD COLUMN url varchar;
ALTER TABLE employers ADD COLUMN description varchar;
ALTER TABLE employers ADD CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id);

CREATE TABLE vacancies
ALTER TABLE vacancies ADD COLUMN employer_id varchar;
ALTER TABLE vacancies ADD COLUMN id_vacancy varchar;
ALTER TABLE vacancies ADD COLUMN vacancies_name varchar;
ALTER TABLE vacancies ADD COLUMN vacancies_url varchar;
ALTER TABLE vacancies ADD COLUMN salary int;
ALTER TABLE vacancies ADD COLUMN requirement text;
ALTER TABLE vacancies ADD COLUMN responsibility text;
ALTER TABLE vacancies ADD CONSTRAINT pk_vacancies_id_vacancy PRIMARY KEY (id_vacancy);
ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employer_id FOREIGN KEY(employer_id) REFERENCES employers(employer_id);

SELECT * FROM vacancies
SELECT * FROM employers