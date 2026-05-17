from typing import Final

class NodeLabels:
    USER: Final = "User"
    POST: Final = "Post"
    ANIMAL: Final = "Animal"
    COMMENT: Final = "Comment"
    TAG: Final = "Tag"
    TAXON: Final = "Taxon"

class RelationTypes:
    TAGGED: Final = "TAGGED"
    LIKED: Final = "LIKED"
    FOLLOWED: Final = "FOLLOWED"
    REPLIED_TO: Final = "REPLIED_TO"
    BELONGED_TO: Final = "BELONGED_TO"
    AUTHORED: Final = "AUTHORED"
    OBSERVED: Final = "OBSERVED"
    ON: Final = "ON"

class PaginationConst:
    DEFAULT_LIMIT: Final = 20
    MAX_LIMIT: Final = 100

class PostConst:
    DEFAULT_LIMIT: Final = 20
    MAX_LIMIT: Final = 100

class CommentCost:
    DEFAULT_LIMIT: Final = 20
    MAX_LIMIT: Final = 50

class UserConst:
    DEFAULT_LIMIT: Final = 20
    MAX_LIMIT: Final = 100

class AnimalConst:
    DEFAULT_LIMIT: Final = 20
    MAX_LIMIT: Final = 100

class SystemConst:
    MAX_IMPORT_FILE_BYTES: Final = 100 * 1024 * 1024