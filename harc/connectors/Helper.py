import types


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def cursor_to_json(cursor):
        results = cursor.fetchall()
        response = []
        for r in xrange(len(results)):
            descriptions = cursor.description
            record = {}
            for i in xrange(0, len(cursor.description)):
                field_name = descriptions[i][0].lower()
                if str(results[r][i]) == 'None':
                    record[field_name] = None
                else:
                    record[field_name] = str(results[r][i])
            response.append(record)
        return response

    @staticmethod
    def statement(statement, *args):
        splits = statement.split("{}")
        result = splits[0]
        count = len(args)
        for i in xrange(count):
            if type(args[i]) in [types.UnicodeType, types.StringType]:
                result = result + "'" + str(args[i]).encode('string_escape') + "'" + splits[i+1]
            elif type(args[i]) == types.NoneType:
                result = result + "''" + splits[i+1]
            else:
                splits[i+1]
                result = result + str(args[i]).encode('string_escape') + splits[i+1]
        return result
