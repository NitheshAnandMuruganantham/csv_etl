from sqlalchemy import and_, or_, text


class FilterParser:
    def __init__(self, model):
        self.model = model

    def parse_filters(self, filters):
        query_filters = []
        for key, value in filters.items():
            if isinstance(value, dict):
                sub_filters = self.parse_filters(value)
                if key.lower() == 'and':
                    query_filters.append(and_(*sub_filters))
                elif key.lower() == 'or':
                    query_filters.append(or_(*sub_filters))
            else:
                column, operator = key.split('__')
                if operator == 'gt':
                    query_filters.append(getattr(self.model, column) > value)
                elif operator == 'lt':
                    query_filters.append(getattr(self.model, column) < value)
                elif operator == 'eq':
                    query_filters.append(getattr(self.model, column) == value)
                elif operator == 'ne':
                    query_filters.append(getattr(self.model, column) != value)
                elif operator == 'like':
                    query_filters.append(
                        getattr(self.model, column).like(value))
                elif operator == 'ilike':
                    query_filters.append(
                        getattr(self.model, column).ilike(value))
                elif operator == 'in':
                    query_filters.append(
                        getattr(self.model, column).in_(value))
                elif operator == 'not_in':
                    query_filters.append(
                        getattr(self.model, column).notin_(value))
                elif operator == 'is_null':
                    query_filters.append(getattr(self.model, column).is_(None))
                elif operator == 'is_not_null':
                    query_filters.append(
                        getattr(self.model, column).isnot(None))
                elif operator == 'raw':
                    query_filters.append(text(value))

        return query_filters
