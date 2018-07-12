delimiter |

CREATE TRIGGER jobs_bi
  BEFORE INSERT ON jobs
    FOR EACH ROW BEGIN
	  SET NEW.created_at=NOW();
      SET NEW.created_by=CURRENT_USER();
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

