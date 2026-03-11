from pydantic import BaseModel, ConfigDict


class ThorestModel(BaseModel):
    """
    Defines the base schema model for Thorest API
    """

    model_config = ConfigDict(
        extra="ignore",  # drop extra response fields
        validate_by_name=True,  # allow alias values
        serialize_by_alias=True,  # serialise to alias
        arbitrary_types_allowed=True,
    )
