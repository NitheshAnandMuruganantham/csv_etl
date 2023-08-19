from sqlalchemy import or_, and_


def get_group_by_queries(query, model, group_by):
    data = query.group_by(
        getattr(model, group_by), model.id).all()
    result = {}
    for d in data:
        if (getattr(d, group_by) not in result.keys()):
            result[getattr(d, group_by)] = []
        result[getattr(d, group_by)].append(d)
    return result


def filter_parser(query, model, filters):
    filter_body = []
    for key in filters.keys():
        if key == "_or":
            or_filter_body = []
            for or_filter in filters[key]:
                or_filter_body.append(
                    getattr(model, or_filter) == filters[key][or_filter])
            query = query.filter(or_(
                *or_filter_body))
            continue
        filter_body.append(getattr(model, key) == filters[key])
    query = query.filter(and_(
        *filter_body))
    return query


def enum_to_dict(enum):
    forward_lookup = {e.name: e.value for e in enum}
    backward_lookup = {e.value: e.name for e in enum}
    return {"forward_lookup": forward_lookup, "backward_lookup": backward_lookup}


def rowToDict(r): return {c.name: str(getattr(r, c.name))
                          for c in r.__table__.columns}
