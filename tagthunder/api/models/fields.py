import pydantic

HTML: str = pydantic.Field(
    default="",
    title="HTML",
    description="HTML without computed styles."
)

HTMLP: str = pydantic.Field(
    default="",
    title="HTML+",
    description="HTML with computed styles in attributes.",
)

HTMLPP: str = pydantic.Field(
    default="",
    title="HTML++",
    description="Cleaned HTML+."
)