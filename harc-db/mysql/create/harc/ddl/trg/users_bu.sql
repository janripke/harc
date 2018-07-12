delimiter |

CREATE TRIGGER users_bu
  BEFORE UPDATE ON users
    FOR EACH ROW BEGIN
      SET NEW.password=MD5(new.password);
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

