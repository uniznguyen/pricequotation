BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `pricequotation_unitofpackage` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 200 ) NOT NULL UNIQUE
);
INSERT INTO `pricequotation_unitofpackage` (id,name) VALUES (1,'each'),
 (2,'case');
COMMIT;
