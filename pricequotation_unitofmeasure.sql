BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `pricequotation_unitofmeasure` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 200 ) NOT NULL UNIQUE
);
INSERT INTO `pricequotation_unitofmeasure` (id,name) VALUES (1,'1 gal'),
 (2,'5 gal'),
 (3,'30 gal'),
 (4,'55 gal'),
 (5,'32 oz'),
 (6,'12 oz'),
 (7,'each'),
 (8,'2.5 liter');
COMMIT;
