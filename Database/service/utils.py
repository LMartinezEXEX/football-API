def default_if_none(
    val: any, 
    default: any
    ) -> any:
    return default if val is None else val