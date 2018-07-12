delimiter |

CREATE TRIGGER commands_bu
  BEFORE UPDATE ON commands
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

