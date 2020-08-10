import graphene

import poll_app.schema


class Query(poll_app.schema.Query, graphene.ObjectType):
    pass

class Mutation(poll_app.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)