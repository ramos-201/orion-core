from ariadne import MutationType


mutation = MutationType()


@mutation.field('setMessageHello')
def resolve_set_message_hello(_, info, message):
    current_message = f'Result mutation, set message hello: {message}.'
    return current_message
