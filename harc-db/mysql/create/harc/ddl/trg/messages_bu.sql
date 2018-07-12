delimiter |

CREATE TRIGGER messages_bu
  BEFORE UPDATE ON messages
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

