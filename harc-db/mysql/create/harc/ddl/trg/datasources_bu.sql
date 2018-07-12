delimiter |

CREATE TRIGGER datasources_bu
  BEFORE UPDATE ON datasources
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

