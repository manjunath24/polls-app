import graphene
import graphql_jwt

import poll_app.schema
import user.schema


class Query(user.schema.Query, poll_app.schema.Query, graphene.ObjectType):
    pass

class Mutation(poll_app.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)