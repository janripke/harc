delimiter |

CREATE TRIGGER jobs_bu
  BEFORE UPDATE ON jobs
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

