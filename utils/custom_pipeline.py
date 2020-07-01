def create_user(strategy, details, backend, response, user=None, *args, **kwargs):

    response_email_id, backend_name = "", ""
    if backend.name == "linkedin-oauth2":
        response_email_id = response["emailAddress"]
        backend_name = "linkedin"
    elif backend.name == "github":
        response_email_id = response["email"]
        backend_name = "github"
    elif backend.name == "twitter":
        backend_name = "twitter"

    if user:

        user.meta[backend_name] = response
        return {'is_new': False}
    else:
        user_data = {
            "email": response_email_id,
            "meta": {backend_name: response},
            "username": details.get("username"),
            "name": details.get("fullname")
        }
        return {
            'is_new': True,
            'user': strategy.create_user(**user_data)
        }
