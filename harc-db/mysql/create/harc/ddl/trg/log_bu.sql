delimiter |

CREATE TRIGGER log_bu
  BEFORE UPDATE ON log
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

