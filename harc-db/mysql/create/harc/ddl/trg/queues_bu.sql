delimiter |

CREATE TRIGGER queues_bu
  BEFORE UPDATE ON queues
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

