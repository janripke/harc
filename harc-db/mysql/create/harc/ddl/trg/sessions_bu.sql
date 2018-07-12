delimiter |

CREATE TRIGGER session_bu
  BEFORE UPDATE ON sessions
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

