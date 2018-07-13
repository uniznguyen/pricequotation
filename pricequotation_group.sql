BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `pricequotation_group` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 200 ) NOT NULL UNIQUE
);
INSERT INTO `pricequotation_group` (id,name) VALUES (1,'Carwash'),
 (2,'Detail'),
 (3,'Accessories');
COMMIT;
