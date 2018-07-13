BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `pricequotation_pricelevel` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 200 ) NOT NULL UNIQUE,
	`isactive`	bool NOT NULL,
	`QuickbookListId`	varchar ( 200 ) UNIQUE
);
INSERT INTO `pricequotation_pricelevel` (id,name,isactive,QuickbookListId) VALUES (3,'2018 HV',1,'800000BB-1503682314'),
 (4,'Stinger 1.1',1,'8000004F-1378053725'),
 (5,'2018 Dist 1',1,'800000BF-1503682567'),
 (6,'2018 Dist',1,'800000BE-1503682510'),
 (7,'2018 HV Mid Yr',1,'800000CB-1524151559'),
 (8,'2018 HV .05 Mid Yr',1,'800000CC-1525115058'),
 (9,'2018 Dist Mid Yr',1,'800000CE-1525193465'),
 (10,'2018 Dist 1 Mid Yr',1,'800000CD-1525189195'),
 (11,'2017 HV Dressing $ increase',1,'800000B7-1493998887');
COMMIT;
