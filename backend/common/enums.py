from enum import Enum, unique


@unique
class QueueEnum(str, Enum):
    """查询操作符枚举"""
    none = "None"
    not_none = "not None"
    date = "date"
    month = "month"
    like = "like"
    eq = "eq"
    in_ = "in"
    between = "between"
    ne = "ne"
    gt = "gt"
    ge = "ge"
    lt = "lt"
    le = "le"
