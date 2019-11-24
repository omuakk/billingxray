/*File used to create tables using data in S3 */

CREATE TABLE medicare_data_xray_2012
(
npi int,
nppes_provider_last_org_name varchar(255),
nppes_provider_first_name varchar(255),
nppes_provider_mi varchar(255),
nppes_credentials varchar(255),
nppes_provider_gender varchar(255),
nppes_entity_code varchar(255),
nppes_provider_street1 varchar(255),
nppes_provider_street2 varchar(255),
nppes_provider_city varchar(255),
nppes_provider_zip varchar(255),
nppes_provider_state varchar(255),
nppes_provider_country varchar(255),
provider_type varchar(255),
medicare_participation_indicator varchar(255),
place_of_Service varchar(255),
hcpcs_code varchar(255),
hcpcs_description varchar(255),
hcpcs_drug_indicator varchar(255),
line_srvc_cnt int,
bene_unique_cnt int,
bene_day_srvc_cnt int,
average_Medicare_allowed_amt float,
stdev_Medicare_allowed_amt1 float,
average_submitted_chrg_amt float,
stdev_submitted_chrg_amt1 float,
average_Medicare_payment_amt float,
stdev_Medicare_payment_amt1 float,
average_Medicare_standard_amt float
);
LOAD DATA FROM S3 's3://dollarxray-medicare/Medicare_Provider_Util_Payment_PUF_CY2012.txt' INTO TABLE medicare_data_xray_2012 FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
ALTER TABLE medicare_data_xray_2012 ADD INDEX (npi);
ALTER TABLE medicare_data_xray_2012 ADD COLUMN year INT DEFAULT 2012;