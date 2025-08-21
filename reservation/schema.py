import graphene
import reservationapp.schema

class Query(reservationapp.schema.Query, graphene.ObjectType):
    pass

class Mutation(reservationapp.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)